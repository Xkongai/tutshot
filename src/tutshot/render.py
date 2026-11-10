"""Render a :class:`~tutshot.story.Story` to PNG screenshots with Pillow.

Everything is drawn at 2x (times ``scale``) and downsampled with Lanczos at the
end, which gives crisp anti-aliased text without needing a browser.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import fonts as fontlib
from .story import Step, Story
from .textwidth import char_width, has_wide, is_wide, wrap_cells
from .themes import Theme, get_theme

SUPERSAMPLE = 2

# Layout, in output pixels at scale 1.
MONO_SIZE = 17
CJK_SCALE = 1.1  # CJK glyphs look small next to Latin at the same pixel size
LINE_HEIGHT = 1.6
TITLE_SIZE = 14
CAPTION_SIZE = 19
BADGE_SIZE = 26
BAR_HEIGHT = 40
PAD_X = 28
PAD_TOP = 20
PAD_BOTTOM = 22
WINDOW_RADIUS = 12
FRAME_MARGIN = 32
FRAME_TOP = 28
FRAME_BOTTOM = 40
FRAME_RADIUS = 16
CAPTION_GAP = 16
STEP_GAP = 40

CARET = "\x00caret"


class RenderError(RuntimeError):
    """Raised when a story cannot be rendered (usually: a missing font)."""


Segment = tuple[str, tuple[int, int, int], bool]  # text, color, bold
Row = list[Segment]


@dataclass
class _Faces:
    mono: dict[bool, ImageFont.FreeTypeFont]
    mono_fake: dict[bool, bool]
    cjk: dict[bool, ImageFont.FreeTypeFont] | None
    cjk_fake: dict[bool, bool]
    ui: dict[bool, ImageFont.FreeTypeFont]
    ui_fake: dict[bool, bool]


def check_fonts(text: str) -> None:
    """Raise :class:`RenderError` with an install hint if ``text`` cannot be drawn."""
    if fontlib.find_mono() is None:
        raise RenderError(
            "no monospace font found. Install one, e.g. `sudo apt install fonts-dejavu-core`, "
            "or set TUTSHOT_MONO_FONT=/path/to/font.ttf"
        )
    if has_wide(text) and fontlib.find_cjk() is None:
        raise RenderError(fontlib.CJK_INSTALL_HINT)


class Renderer:
    def __init__(self, story: Story, theme: Theme, scale: int = 1):
        if scale not in (1, 2, 3):
            raise ValueError("scale must be 1, 2 or 3")
        check_fonts(story.all_text())
        self.story = story
        self.theme = theme
        self.scale = scale
        self.k = SUPERSAMPLE * scale  # drawing units per output pixel at scale 1
        k = self.k

        mono = fontlib.find_mono()
        cjk = fontlib.find_cjk()
        ui = fontlib.find_ui() or mono
        self.f = _Faces(
            mono={b: mono.face(b).load(MONO_SIZE * k) for b in (False, True)},
            mono_fake={b: mono.face(b).fake_bold for b in (False, True)},
            cjk={b: cjk.face(b).load(round(MONO_SIZE * CJK_SCALE * k)) for b in (False, True)} if cjk else None,
            cjk_fake={b: cjk.face(b).fake_bold if cjk else False for b in (False, True)},
            ui={b: ui.face(b).load(CAPTION_SIZE * k) for b in (False, True)},
            ui_fake={b: ui.face(b).fake_bold for b in (False, True)},
        )
        self._ui_pair, self._cjk_pair = ui, cjk
        self.cell = self.f.mono[False].getlength("M")
        self.line = round(MONO_SIZE * LINE_HEIGHT) * k
        self._glyph_cache: dict[tuple[int, str], bool] = {}

    # ------------------------------------------------------------------ glyphs
    def _supports(self, font: ImageFont.FreeTypeFont, ch: str) -> bool:
        if ch.isspace():
            return True
        key = (id(font), ch)
        hit = self._glyph_cache.get(key)
        if hit is None:
            missing = font.getmask("\uffff")
            mask = font.getmask(ch)
            hit = not (mask.size == missing.size and bytes(mask) == bytes(missing))
            self._glyph_cache[key] = hit
        return hit

    def _mono_font(self, ch: str, bold: bool) -> tuple[ImageFont.FreeTypeFont, bool]:
        if self.f.cjk and (is_wide(ch) or not self._supports(self.f.mono[bold], ch)):
            if is_wide(ch) or self._supports(self.f.cjk[bold], ch):
                return self.f.cjk[bold], self.f.cjk_fake[bold]
        return self.f.mono[bold], self.f.mono_fake[bold]

    def _ui_font(self, ch: str, bold: bool, size: int) -> tuple[ImageFont.FreeTypeFont, bool]:
        if self._cjk_pair and is_wide(ch):
            return self._cjk_pair.face(bold).load(size * self.k), self._cjk_pair.face(bold).fake_bold
        face = self._ui_pair.face(bold)
        return face.load(size * self.k), face.fake_bold

    def _text_len(self, text: str, bold: bool, size: int) -> float:
        return sum(self._ui_font(ch, bold, size)[0].getlength(ch) for ch in text)

    def _draw_ui(self, d: ImageDraw.ImageDraw, x: float, y: float, text: str, size: int, bold: bool, fill) -> None:
        for ch in text:
            font, fake = self._ui_font(ch, bold, size)
            d.text((x, y), ch, font=font, fill=fill, anchor="lm",
                   stroke_width=max(1, self.k // 3) if fake else 0, stroke_fill=fill)
            x += font.getlength(ch)

    # -------------------------------------------------------------------- rows
    def _prompt(self) -> Row:
        t, s = self.theme, self.story
        if s.prompt:
            return [(s.prompt, t.accent, True), (":", t.dim, False), (s.cwd, t.path, True), ("$ ", t.prompt, True)]
        return [("$ ", t.prompt, True)]

    def step_rows(self, step: Step) -> list[Row]:
        t, cols = self.theme, self.story.width
        rows: list[Row] = []
        prompt = self._prompt()
        lead = sum(char_width(c) for seg in prompt for c in seg[0])
        for n, line in enumerate(step.command.split("\n")):
            prefix = prompt if n == 0 else [("> ", t.dim, False)]
            p = lead if n == 0 else 2
            if p >= cols - 8:  # very long prompt: put the command on its own row
                rows.append(list(prefix))
                prefix, p = [], 0
            wrapped = wrap_cells(" " * p + line, cols, indent=2)
            wrapped[0] = wrapped[0][p:]
            rows.append(list(prefix) + [(wrapped[0], t.command, True)])
            rows += [[(w, t.command, True)] for w in wrapped[1:]]
        if step.output:
            for line in step.output.split("\n"):
                rows += [[(w, t.fg, False)] for w in wrap_cells(line, cols)]
        if self.story.caret:
            rows.append(prompt + [(CARET, t.caret, False)])
        return rows

    # ------------------------------------------------------------------ window
    def window(self, step: Step) -> Image.Image:
        """The terminal window for one step, as an RGBA image in drawing units."""
        t, k = self.theme, self.k
        rows = self.step_rows(step)
        w = round(2 * PAD_X * k + self.story.width * self.cell)
        h = (BAR_HEIGHT + PAD_TOP + PAD_BOTTOM) * k + len(rows) * self.line
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        r = WINDOW_RADIUS * k
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=t.window)
        d.rounded_rectangle([0, 0, w - 1, BAR_HEIGHT * k], radius=r, fill=t.bar, corners=(True, True, False, False))
        d.line([0, BAR_HEIGHT * k, w, BAR_HEIGHT * k], fill=t.border, width=max(1, k // 2))
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=t.border, width=max(1, k // 2))

        cy = BAR_HEIGHT * k / 2
        for j, color in enumerate(t.lights):
            cx = (20 + j * 20) * k
            d.ellipse([cx - 6 * k, cy - 6 * k, cx + 6 * k, cy + 6 * k], fill=color)

        title = self.story.window_title
        max_w = w - 2 * 90 * k
        if self._text_len(title, False, TITLE_SIZE) > max_w:
            while title and self._text_len(title + "…", False, TITLE_SIZE) > max_w:
                title = title[:-1]
            title += "…"
        tw = self._text_len(title, False, TITLE_SIZE)
        self._draw_ui(d, (w - tw) / 2, cy, title, TITLE_SIZE, False, t.dim)

        y = (BAR_HEIGHT + PAD_TOP) * k
        for row in rows:
            col = 0
            mid = y + self.line / 2
            for text, color, bold in row:
                if text == CARET:
                    x = PAD_X * k + col * self.cell
                    d.rectangle([x + k, mid - 0.62 * MONO_SIZE * k, x + self.cell - k, mid + 0.62 * MONO_SIZE * k], fill=color)
                    col += 1
                    continue
                for ch in text:
                    cw = char_width(ch)
                    if cw == 0:
                        continue
                    if not ch.isspace():
                        font, fake = self._mono_font(ch, bold)
                        x = PAD_X * k + col * self.cell
                        gx = x + (cw * self.cell - font.getlength(ch)) / 2
                        d.text((gx, mid), ch, font=font, fill=color, anchor="lm",
                               stroke_width=max(1, k // 3) if fake else 0, stroke_fill=color)
                    col += cw
            y += self.line
        return img

    # ------------------------------------------------------------------- cards
    def _caption_lines(self, text: str, max_w: float) -> list[str]:
        words, lines, cur = _tokens(text), [], ""
        for tok in words:
            trial = cur + tok
            if cur and self._text_len(trial, True, CAPTION_SIZE) > max_w:
                lines.append(cur.rstrip())
                cur = tok.lstrip()
            else:
                cur = trial
        if cur.strip():
            lines.append(cur.rstrip())
        return lines or [""]

    def _block(self, number: int, step: Step) -> tuple[Image.Image, list[str]]:
        win = self.window(step)
        lines: list[str] = []
        if step.caption:
            avail = win.width - (BADGE_SIZE + 12) * self.k
            lines = self._caption_lines(step.caption, avail)
        return win, lines

    def _caption_height(self, lines: list[str]) -> int:
        if not lines:
            return 0
        k = self.k
        return max(BADGE_SIZE * k, round(len(lines) * CAPTION_SIZE * 1.5 * k)) + CAPTION_GAP * k

    def _draw_caption(self, d: ImageDraw.ImageDraw, x: int, y: int, number: int, lines: list[str]) -> None:
        t, k = self.theme, self.k
        b = BADGE_SIZE * k
        line_h = CAPTION_SIZE * 1.5 * k
        top = y + max(0, (b - line_h) / 2) if len(lines) == 1 else y
        d.ellipse([x, y, x + b, y + b], fill=t.accent)
        label = str(number)
        size = 14 if number < 10 else 12
        lw = self._text_len(label, True, size)
        self._draw_ui(d, x + (b - lw) / 2, y + b / 2, label, size, True, t.badge_text)
        tx = x + b + 12 * k
        for i, line in enumerate(lines):
            self._draw_ui(d, tx, top + line_h * i + line_h / 2, line, CAPTION_SIZE, True, t.caption)

    def compose(self, blocks: list[tuple[int, Image.Image, list[str]]]) -> Image.Image:
        """Lay out caption + window blocks on a themed, rounded card."""
        t, k = self.theme, self.k
        width = max(win.width for _, win, _ in blocks) + 2 * FRAME_MARGIN * k
        height = FRAME_TOP * k + FRAME_BOTTOM * k
        for i, (_, win, lines) in enumerate(blocks):
            height += self._caption_height(lines) + win.height + (STEP_GAP * k if i else 0)

        card = _gradient((width, height), t.frame_top, t.frame_bottom)
        shadow = Image.new("L", card.size, 0)
        sd = ImageDraw.Draw(shadow)
        placed = []
        y = FRAME_TOP * k
        for i, (number, win, lines) in enumerate(blocks):
            if i:
                y += STEP_GAP * k
            cap_y = y
            y += self._caption_height(lines)
            x = FRAME_MARGIN * k
            sd.rounded_rectangle([x, y + 8 * k, x + win.width, y + win.height + 8 * k],
                                 radius=WINDOW_RADIUS * k, fill=t.shadow)
            placed.append((number, lines, cap_y, x, y, win))
            y += win.height

        shadow = shadow.filter(ImageFilter.GaussianBlur(14 * k))
        card = Image.composite(Image.new("RGB", card.size, (0, 0, 0)), card, shadow).convert("RGBA")
        d = ImageDraw.Draw(card)
        for number, lines, cap_y, x, y, win in placed:
            if lines:
                self._draw_caption(d, x, cap_y, number, lines)
            card.alpha_composite(win, (x, y))

        mask = Image.new("L", card.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, width - 1, height - 1], radius=FRAME_RADIUS * k, fill=255)
        card.putalpha(mask)
        return self.finish(card)

    def finish(self, img: Image.Image) -> Image.Image:
        """Downsample a drawing-unit image to output pixels."""
        f = SUPERSAMPLE
        return img.resize((round(img.width / f), round(img.height / f)), Image.LANCZOS)

    def step_image(self, index: int) -> Image.Image:
        step = self.story.steps[index]
        win, lines = self._block(index + 1, step)
        return self.compose([(index + 1, win, lines)])

    def sheet_image(self) -> Image.Image:
        blocks = []
        for i, step in enumerate(self.story.steps):
            win, lines = self._block(i + 1, step)
            blocks.append((i + 1, win, lines))
        return self.compose(blocks)

    def window_image(self, index: int) -> Image.Image:
        """Just the terminal window (no card, no caption), in output pixels."""
        return self.finish(self.window(self.story.steps[index]))


def _tokens(text: str) -> list[str]:
    """Split a caption into wrap units: Latin words (with trailing space) or single CJK chars."""
    out: list[str] = []
    cur = ""
    for ch in text:
        if is_wide(ch):
            if cur:
                out.append(cur)
                cur = ""
            out.append(ch)
        elif ch == " ":
            out.append(cur + " ")
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def _gradient(size: tuple[int, int], top, bottom) -> Image.Image:
    grad = Image.linear_gradient("L").resize(size)
    return Image.composite(Image.new("RGB", size, bottom), Image.new("RGB", size, top), grad)


def render_story(
    story: Story,
    out_dir: str | Path,
    theme: str | None = None,
    scale: int = 1,
    sheet: bool = True,
) -> list[Path]:
    """Write ``{id}.png`` for every step (and ``story.png``) into ``out_dir``.

    ``theme`` overrides the theme set in the story. Returns the written paths.
    """
    try:
        th = get_theme(theme or story.theme)
    except ValueError as exc:
        raise RenderError(str(exc)) from None
    renderer = Renderer(story, th, scale=scale)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, step in enumerate(story.steps):
        path = out / f"{step.id}.png"
        renderer.step_image(i).save(path, optimize=True)
        written.append(path)
    if sheet:
        path = out / "story.png"
        renderer.sheet_image().save(path, optimize=True)
        written.append(path)
    return written
