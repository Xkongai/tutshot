"""Command-line interface: ``tutshot init | render | fonts``."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from PIL import Image

from . import __version__
from . import fonts as fontlib
from .render import RenderError, render_story
from .story import SAMPLE_STORY, StoryError, load_story
from .themes import THEMES

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode=None,
    help="Turn a short YAML command story into tutorial-style README screenshots.",
)


def _fail(message: str, code: int = 1) -> None:
    typer.secho(f"error: {message}", fg=typer.colors.RED, err=True)
    raise typer.Exit(code)


def _show(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def _version(value: bool) -> None:
    if value:
        typer.echo(f"tutshot {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-V", callback=_version, is_eager=True, help="Show the version and exit."
    ),
) -> None:
    """Turn a short YAML command story into tutorial-style README screenshots."""


@app.command()
def init(
    path: Path = typer.Argument(Path("tutshot.yml"), help="Where to write the sample story."),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite an existing file."),
) -> None:
    """Write a sample tutshot.yml story to edit."""
    if path.is_dir():
        path = path / "tutshot.yml"
    if path.exists() and not force:
        _fail(f"{_show(path)} already exists (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SAMPLE_STORY, encoding="utf-8")
    typer.echo(f"Wrote {_show(path)}")
    typer.echo(f"Next: edit the steps, then run  tutshot render {_show(path)}")


@app.command()
def render(
    file: Path = typer.Argument(Path("tutshot.yml"), help="Story file to render."),
    out: Path = typer.Option(Path("docs/images"), "--out", "-o", help="Output directory for PNGs."),
    theme: Optional[str] = typer.Option(
        None, "--theme", "-t", help=f"Override the story theme: {' | '.join(THEMES)}."
    ),
    scale: int = typer.Option(1, "--scale", min=1, max=3, help="Pixel density: 2 for retina-sharp images."),
    sheet: bool = typer.Option(True, "--sheet/--no-sheet", help="Also write story.png with every step."),
) -> None:
    """Render every step to {id}.png, plus a combined story.png."""
    if theme is not None and theme.lower() not in THEMES:
        _fail(f"unknown theme '{theme}' (choose one of: {', '.join(THEMES)})", 2)
    try:
        story = load_story(file)
        written = render_story(story, out, theme=theme.lower() if theme else None, scale=scale, sheet=sheet)
    except StoryError as exc:
        _fail(str(exc), 2)
    except RenderError as exc:
        _fail(str(exc), 3)
    used = (theme or story.theme or "dusk").lower()
    typer.echo(f"Rendered {len(story.steps)} step(s) from {_show(file)} with theme {used}:")
    for path in written:
        with Image.open(path) as im:
            w, h = im.size
        typer.echo(f"  {_show(path)}  {w}x{h}")


@app.command()
def fonts() -> None:
    """List the fonts tutshot found for terminal text, CJK and captions."""
    roles = [
        ("mono", fontlib.find_mono(), "terminal text", "fonts-dejavu-core or JetBrains Mono"),
        ("cjk", fontlib.find_cjk(), "Chinese / Japanese / Korean", "fonts-noto-cjk (Noto Sans CJK)"),
        ("ui", fontlib.find_ui(), "title bar and captions", "Inter (falls back to the mono font)"),
    ]
    missing = False
    for role, pair, what, hint in roles:
        if pair is None:
            missing = missing or role != "ui"
            typer.secho(f"{role:<5} not found  ({what}; install {hint})", fg=typer.colors.YELLOW)
            continue
        typer.echo(f"{role:<5} {pair.name}  ({what})")
        typer.echo(f"      regular: {pair.regular.path}" + (f" #{pair.regular.index}" if pair.regular.index else ""))
        bold = "synthetic (stroked regular)" if pair.bold.fake_bold else pair.bold.path
        if not pair.bold.fake_bold and pair.bold.variation:
            bold += f" ({pair.bold.variation})"
        if not pair.bold.fake_bold and pair.bold.index:
            bold += f" #{pair.bold.index}"
        typer.echo(f"      bold:    {bold}")
    typer.echo("Override with TUTSHOT_MONO_FONT, TUTSHOT_CJK_FONT or TUTSHOT_UI_FONT=/path/to/font")
    if missing:
        raise typer.Exit(1)


if __name__ == "__main__":  # pragma: no cover
    app()
