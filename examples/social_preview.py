"""Compose docs/images/social-preview.png (1280x640) for the GitHub social card.

Uses tutshot itself to render the terminal window on the right, so the card
always shows real tutshot output. Run from the repository root:

    python examples/social_preview.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from tutshot import fonts, parse_story
from tutshot.fonts import FontFace
from tutshot.render import Renderer
from tutshot.textwidth import is_wide
from tutshot.themes import get_theme

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images" / "social-preview.png"
W, H, S = 1280, 640, 2

BG = (11, 15, 21)
FG = (230, 237, 243)
DIM = (139, 148, 158)
ACC = (57, 197, 207)
GREEN = (63, 185, 80)
CHIP = (22, 27, 34)
CHIP_EDGE = (48, 54, 61)

PREVIEW = parse_story(
    {
        "title": "tutshot",
        "cwd": "~/project",
        "width": 56,
        "steps": [
            {
                "id": "render",
                "command": "tutshot render tutshot.yml",
                "output": (
                    "Rendered 3 step(s) from tutshot.yml with theme dusk:\n"
                    "  docs/images/install.png  1018x276\n"
                    "  docs/images/hello.png    1018x302\n"
                    "  docs/images/story.png    1018x868\n"
                    "\n"
                    "你好，世界 — CJK text just works"
                ),
            }
        ],
    }
)


def face(pair, weight: str) -> FontFace:
    f = pair.regular
    return FontFace(f.path, f.index, weight) if f.variation else pair.face(weight != "Regular")


def main() -> None:
    ui, mono, cjk = fonts.find_ui(), fonts.find_mono(), fonts.find_cjk()
    if ui is None or mono is None or cjk is None:
        raise SystemExit("social_preview.py needs a UI font, a mono font and a CJK font (see `tutshot fonts`)")

    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, W * S, 32 * S):
        for y in range(0, H * S, 32 * S):
            d.ellipse([x - 1.2 * S, y - 1.2 * S, x + 1.2 * S, y + 1.2 * S], fill=(24, 30, 38))
    glow = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(glow).ellipse([int(W * S * 0.45), -H * S // 3, int(W * S * 1.25), int(H * S * 1.1)], fill=(14, 58, 68))
    img = ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(140 * S)))
    d = ImageDraw.Draw(img)

    def text(x, y, s, size, weight, fill, family=ui):
        lat = face(family, weight).load(size * S)
        cj = face(cjk, "Bold" if weight in ("Bold", "SemiBold") else "Regular").load(size * S)
        for ch in s:
            f = cj if is_wide(ch) else lat
            d.text((x, y), ch, font=f, fill=fill, anchor="lm")
            x += f.getlength(ch)
        return x

    # Logo: a tiny terminal tile.
    x0, yc = 72 * S, 214 * S
    tile = 84 * S
    d.rounded_rectangle([x0, yc - tile // 2, x0 + tile, yc + tile // 2], radius=20 * S, fill=ACC)
    text(x0 + 16 * S, yc + 2 * S, ">_", 38, "Bold", BG, family=mono)
    end = text(x0 + tile + 24 * S, yc, "tut", 92, "Bold", FG)
    text(end, yc, "shot", 92, "Bold", ACC)

    text(74 * S, 318 * S, "YAML command stories →", 27, "SemiBold", FG)
    text(74 * S, 356 * S, "tutorial screenshots for your README.", 27, "SemiBold", FG)
    text(74 * S, 410 * S, "把命令故事变成 README 教程截图。", 24, "Regular", DIM)

    def chip(x, y, label, color, family):
        f = face(family, "Regular").load(18 * S)
        cf = face(cjk, "Regular").load(18 * S)
        tw = sum((cf if is_wide(c) else f).getlength(c) for c in label)
        d.rounded_rectangle([x, y - 22 * S, x + tw + 28 * S, y + 22 * S], radius=8 * S, fill=CHIP, outline=CHIP_EDGE, width=S)
        cx = x + 14 * S
        for c in label:
            ff = cf if is_wide(c) else f
            d.text((cx, y), c, font=ff, fill=color, anchor="lm")
            cx += ff.getlength(c)
        return x + tw + 28 * S

    nx = chip(74 * S, 530 * S, "$ tutshot render", FG, mono)
    chip(nx + 12 * S, 530 * S, "no browser · CJK-ready · MIT", DIM, mono)

    # Terminal preview, rendered by tutshot at 2x on the right.
    renderer = Renderer(PREVIEW, get_theme("dusk"), scale=2)
    win = renderer.window_image(0)
    target_w = 560 * S
    win = win.resize((target_w, round(win.height * target_w / win.width)), Image.LANCZOS)
    wx, wy = 676 * S, (H * S - win.height) // 2 + 20 * S
    shadow = Image.new("L", img.size, 0)
    ImageDraw.Draw(shadow).rounded_rectangle([wx, wy + 16 * S, wx + win.width, wy + win.height + 16 * S], radius=24 * S, fill=170)
    shadow = shadow.filter(ImageFilter.GaussianBlur(28 * S))
    img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, shadow).convert("RGBA")
    img.alpha_composite(win, (wx, wy))

    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)} {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    main()
