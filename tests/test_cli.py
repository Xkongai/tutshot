import subprocess
import sys

from PIL import Image
from typer.testing import CliRunner

from tutshot import __version__
from tutshot.cli import app
from tutshot import render as render_mod

from conftest import needs_cjk

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for cmd in ("init", "render", "fonts"):
        assert cmd in result.output


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_init_writes_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "tutshot.yml").is_file()
    assert "Wrote tutshot.yml" in result.output
    # refuses to overwrite without --force
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 1
    assert "already exists" in result.output
    assert runner.invoke(app, ["init", "--force"]).exit_code == 0


def test_init_custom_path(tmp_path):
    target = tmp_path / "docs" / "story.yml"
    result = runner.invoke(app, ["init", str(target)])
    assert result.exit_code == 0, result.output
    assert target.is_file()


def test_init_then_render(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert runner.invoke(app, ["init"]).exit_code == 0
    result = runner.invoke(app, ["render", "--theme", "paper"])
    assert result.exit_code == 0, result.output
    out = tmp_path / "docs" / "images"
    names = sorted(p.name for p in out.glob("*.png"))
    assert names == ["hello.png", "install.png", "story.png"]
    assert "theme paper" in result.output
    with Image.open(out / "story.png") as im:
        assert im.width > 600 and im.height > 300


def test_render_out_option(fixtures, tmp_path):
    out = tmp_path / "shots"
    result = runner.invoke(app, ["render", str(fixtures / "basic.yml"), "--out", str(out), "--no-sheet"])
    assert result.exit_code == 0, result.output
    assert sorted(p.name for p in out.iterdir()) == ["one.png", "two.png"]


def test_render_missing_file(tmp_path):
    result = runner.invoke(app, ["render", str(tmp_path / "missing.yml")])
    assert result.exit_code == 2
    assert "not found" in result.output


def test_render_invalid_story(fixtures, tmp_path):
    result = runner.invoke(app, ["render", str(fixtures / "duplicate.yml"), "--out", str(tmp_path)])
    assert result.exit_code == 2
    assert "duplicate id" in result.output


def test_render_bad_theme(fixtures, tmp_path):
    result = runner.invoke(app, ["render", str(fixtures / "basic.yml"), "--theme", "neon", "--out", str(tmp_path)])
    assert result.exit_code == 2
    assert "unknown theme" in result.output


def test_render_cjk_without_font(fixtures, tmp_path, monkeypatch):
    monkeypatch.setattr(render_mod.fontlib, "find_cjk", lambda: None)
    result = runner.invoke(app, ["render", str(fixtures / "cjk.yml"), "--out", str(tmp_path)])
    assert result.exit_code == 3
    assert "fonts-noto-cjk" in result.output


@needs_cjk
def test_render_cjk(fixtures, tmp_path):
    result = runner.invoke(app, ["render", str(fixtures / "cjk.yml"), "--out", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "say.png").is_file()


def test_fonts_command():
    result = runner.invoke(app, ["fonts"])
    assert "mono" in result.output and "cjk" in result.output


def test_module_entrypoint():
    r = subprocess.run([sys.executable, "-m", "tutshot", "--version"], capture_output=True, text=True)
    assert r.returncode == 0
    assert __version__ in r.stdout
