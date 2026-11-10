"""Color themes. Every color is an (R, G, B) tuple."""

from __future__ import annotations

from dataclasses import dataclass

RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Theme:
    name: str
    frame_top: RGB      # card background gradient (top-left)
    frame_bottom: RGB   # card background gradient (bottom-right)
    window: RGB         # terminal background
    bar: RGB            # title bar background
    border: RGB         # hairline around the window / under the bar
    fg: RGB             # output text
    command: RGB        # command text (drawn bold)
    dim: RGB            # title text, continuation markers
    prompt: RGB         # the "$" sign
    accent: RGB         # prompt user@host, step badges
    path: RGB           # cwd inside the prompt
    caret: RGB
    caption: RGB        # caption text on the frame
    badge_text: RGB
    shadow: int         # drop-shadow opacity 0-255
    lights: tuple[RGB, RGB, RGB] = ((255, 95, 86), (255, 189, 46), (39, 201, 63))


DUSK = Theme(
    name="dusk",
    frame_top=(33, 40, 52),
    frame_bottom=(18, 22, 30),
    window=(13, 17, 23),
    bar=(22, 27, 34),
    border=(48, 54, 61),
    fg=(201, 209, 217),
    command=(240, 246, 252),
    dim=(139, 148, 158),
    prompt=(63, 185, 80),
    accent=(57, 197, 207),
    path=(88, 166, 255),
    caret=(139, 148, 158),
    caption=(230, 237, 243),
    badge_text=(13, 17, 23),
    shadow=150,
)

PAPER = Theme(
    name="paper",
    frame_top=(243, 246, 250),
    frame_bottom=(226, 232, 240),
    window=(255, 255, 255),
    bar=(240, 243, 246),
    border=(208, 215, 222),
    fg=(36, 41, 47),
    command=(13, 17, 23),
    dim=(101, 109, 118),
    prompt=(26, 127, 55),
    accent=(9, 105, 218),
    path=(130, 80, 223),
    caret=(140, 149, 159),
    caption=(31, 35, 40),
    badge_text=(255, 255, 255),
    shadow=55,
)

NORD = Theme(
    name="nord",
    frame_top=(76, 86, 106),
    frame_bottom=(59, 66, 82),
    window=(46, 52, 64),
    bar=(59, 66, 82),
    border=(67, 76, 94),
    fg=(216, 222, 233),
    command=(236, 239, 244),
    dim=(143, 157, 180),
    prompt=(163, 190, 140),
    accent=(136, 192, 208),
    path=(129, 161, 193),
    caret=(143, 157, 180),
    caption=(236, 239, 244),
    badge_text=(46, 52, 64),
    shadow=120,
)

THEMES: dict[str, Theme] = {t.name: t for t in (DUSK, PAPER, NORD)}
DEFAULT_THEME = "dusk"


def get_theme(name: str | None) -> Theme:
    key = (name or DEFAULT_THEME).strip().lower()
    try:
        return THEMES[key]
    except KeyError:
        raise ValueError(f"unknown theme '{name}' (choose one of: {', '.join(THEMES)})") from None
