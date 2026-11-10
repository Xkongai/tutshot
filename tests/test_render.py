import pytest
from PIL import Image

from tutshot import RenderError, load_story, parse_story, render_story
from tutshot import render as render_mod

from conftest import needs_cjk


def _sizes(paths):
    out = {}
    for p in paths:
        with Image.open(p) as im:
            out[p.name] = im.size
    return out


@pytest.mark.parametrize("theme", ["dusk", "paper", "nord"])
def test_render_writes_pngs(fixtures, tmp_path, theme):
    story = load_story(fixtures / "basic.yml")
    written = render_story(story, tmp_path / "out", theme=theme)
    assert [p.name for p in written] == ["one.png", "two.png", "story.png"]
    sizes = _sizes(written)
    for name, (w, h) in sizes.items():
        assert 500 < w < 1600, (name, w)
        assert 150 < h < 2000, (name, h)
    # same width for every image; the storyboard is taller than any single step
    assert len({w for w, _ in sizes.values()}) == 1
    assert sizes["story.png"][1] > sizes["one.png"][1] + sizes["two.png"][1] - 200


def test_render_has_content(fixtures, tmp_path):
    story = load_story(fixtures / "basic.yml")
    path = render_story(story, tmp_path, theme="paper", sheet=False)[0]
    with Image.open(path) as im:
        im = im.convert("RGBA")
        assert im.mode == "RGBA"
        assert im.getpixel((0, 0))[3] == 0  # rounded transparent corner
        colors = im.convert("RGB").getcolors(maxcolors=1_000_000)
        assert len(colors) > 50  # text + chrome, not a blank card


def test_width_controls_image_width(tmp_path):
    def width(cols):
        s = parse_story({"width": cols, "steps": [{"id": "a", "command": "ls"}]})
        with Image.open(render_story(s, tmp_path / str(cols), sheet=False)[0]) as im:
            return im.width

    assert width(100) > width(60)


def test_scale_2_doubles_size(fixtures, tmp_path):
    story = load_story(fixtures / "basic.yml")
    a = _sizes(render_story(story, tmp_path / "x1", sheet=False))
    b = _sizes(render_story(story, tmp_path / "x2", scale=2, sheet=False))
    assert abs(b["one.png"][0] - 2 * a["one.png"][0]) <= 2


def test_long_lines_wrap_instead_of_overflowing(tmp_path):
    long = "x" * 500
    s = parse_story({"width": 40, "steps": [{"id": "a", "command": "echo " + long, "output": long}]})
    r = render_mod.Renderer(s, render_mod.get_theme("dusk"))
    rows = r.step_rows(s.steps[0])
    assert len(rows) > 20


def test_unknown_theme(fixtures, tmp_path):
    with pytest.raises(RenderError, match="unknown theme"):
        render_story(load_story(fixtures / "basic.yml"), tmp_path, theme="neon")


@needs_cjk
def test_cjk_story_renders(fixtures, tmp_path):
    written = render_story(load_story(fixtures / "cjk.yml"), tmp_path)
    assert {p.name for p in written} == {"say.png", "story.png"}
    assert all(p.stat().st_size > 2000 for p in written)


def test_cjk_without_font_fails_clearly(fixtures, tmp_path, monkeypatch):
    monkeypatch.setattr(render_mod.fontlib, "find_cjk", lambda: None)
    with pytest.raises(RenderError, match="fonts-noto-cjk"):
        render_story(load_story(fixtures / "cjk.yml"), tmp_path)
    assert not list(tmp_path.iterdir())  # nothing half-written


def test_latin_story_needs_no_cjk_font(fixtures, tmp_path, monkeypatch):
    monkeypatch.setattr(render_mod.fontlib, "find_cjk", lambda: None)
    assert len(render_story(load_story(fixtures / "basic.yml"), tmp_path)) == 3
