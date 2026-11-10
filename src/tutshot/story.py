"""Parse and validate a tutshot YAML story."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .themes import THEMES

ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
RESERVED_IDS = {"story"}  # story.png is the contact sheet

DEFAULT_TITLE = "bash"
DEFAULT_CWD = "~"
DEFAULT_WIDTH = 88
MIN_WIDTH, MAX_WIDTH = 40, 200

TOP_KEYS = {"title", "theme", "cwd", "prompt", "width", "caret", "steps"}
STEP_KEYS = {"id", "caption", "command", "output"}


class StoryError(ValueError):
    """Raised when a story file is missing, malformed or invalid."""


@dataclass(frozen=True)
class Step:
    id: str
    command: str
    output: str = ""
    caption: str | None = None


@dataclass(frozen=True)
class Story:
    steps: list[Step]
    title: str = DEFAULT_TITLE
    theme: str | None = None
    cwd: str = DEFAULT_CWD
    prompt: str | None = None
    width: int = DEFAULT_WIDTH
    caret: bool = True
    source: Path | None = field(default=None, compare=False)

    @property
    def window_title(self) -> str:
        where = f"{self.prompt}:{self.cwd}" if self.prompt else self.cwd
        return f"{self.title} — {where}" if where else self.title

    def all_text(self) -> str:
        parts = [self.title, self.cwd, self.prompt or ""]
        for s in self.steps:
            parts += [s.command, s.output, s.caption or ""]
        return "\n".join(parts)


def _unknown_keys(found: dict, allowed: set[str], where: str) -> None:
    for key in found:
        if key not in allowed:
            hint = difflib.get_close_matches(str(key), sorted(allowed), n=1)
            extra = f" (did you mean '{hint[0]}'?)" if hint else ""
            raise StoryError(f"{where}: unknown key '{key}'{extra}")


def _text(value: Any, where: str, *, required: bool = False, allow_multiline: bool = True) -> str | None:
    if value is None:
        if required:
            raise StoryError(f"{where} is required")
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise StoryError(f"{where} must be a string, got {type(value).__name__}")
    text = str(value)
    if not allow_multiline and "\n" in text.strip("\n"):
        raise StoryError(f"{where} must be a single line")
    return text


def parse_story(data: Any, source: Path | None = None) -> Story:
    """Validate already-loaded YAML data and return a :class:`Story`."""
    if not isinstance(data, dict):
        raise StoryError("story must be a YAML mapping with a 'steps' list")
    _unknown_keys(data, TOP_KEYS, "story")

    title = _text(data.get("title"), "title", allow_multiline=False) or DEFAULT_TITLE
    cwd = _text(data.get("cwd"), "cwd", allow_multiline=False)
    cwd = DEFAULT_CWD if cwd is None else cwd.strip()
    prompt = _text(data.get("prompt"), "prompt", allow_multiline=False)
    prompt = prompt.strip() or None if prompt is not None else None

    theme = data.get("theme")
    if theme is not None:
        theme = str(theme).strip().lower()
        if theme not in THEMES:
            raise StoryError(f"theme: unknown theme '{theme}' (choose one of: {', '.join(THEMES)})")

    width = data.get("width", DEFAULT_WIDTH)
    if isinstance(width, bool) or not isinstance(width, int):
        raise StoryError(f"width must be an integer number of columns, got {width!r}")
    if not MIN_WIDTH <= width <= MAX_WIDTH:
        raise StoryError(f"width must be between {MIN_WIDTH} and {MAX_WIDTH} columns, got {width}")

    caret = data.get("caret", True)
    if not isinstance(caret, bool):
        raise StoryError(f"caret must be true or false, got {caret!r}")

    raw_steps = data.get("steps")
    if raw_steps is None:
        raise StoryError("steps is required (a list of {id, command, output, caption})")
    if not isinstance(raw_steps, list) or not raw_steps:
        raise StoryError("steps must be a non-empty list")

    steps: list[Step] = []
    seen: set[str] = set()
    for i, raw in enumerate(raw_steps):
        where = f"steps[{i}]"
        if not isinstance(raw, dict):
            raise StoryError(f"{where} must be a mapping with at least 'id' and 'command'")
        _unknown_keys(raw, STEP_KEYS, where)
        sid = _text(raw.get("id"), f"{where}.id", required=True, allow_multiline=False).strip()
        where = f"steps[{i}] (id '{sid}')"
        if not ID_RE.match(sid):
            raise StoryError(f"{where}: id may only contain letters, digits, '-' and '_' (it becomes the file name)")
        if sid.lower() in RESERVED_IDS:
            raise StoryError(f"{where}: id '{sid}' is reserved for the contact sheet, pick another")
        if sid.lower() in seen:
            raise StoryError(f"{where}: duplicate id '{sid}'")
        seen.add(sid.lower())
        command = _text(raw.get("command"), f"{where}.command", required=True)
        command = command.strip("\n")
        if not command.strip():
            raise StoryError(f"{where}.command must not be empty")
        output = _text(raw.get("output"), f"{where}.output") or ""
        caption = _text(raw.get("caption"), f"{where}.caption", allow_multiline=False)
        caption = caption.strip() or None if caption is not None else None
        steps.append(Step(id=sid, command=command, output=output.rstrip("\n"), caption=caption))

    return Story(
        steps=steps,
        title=title.strip() or DEFAULT_TITLE,
        theme=theme,
        cwd=cwd,
        prompt=prompt,
        width=width,
        caret=caret,
        source=source,
    )


def load_story(path: str | Path) -> Story:
    """Read and validate a story file."""
    path = Path(path)
    if not path.is_file():
        raise StoryError(f"story file not found: {path} (create one with `tutshot init`)")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        loc = f" at line {mark.line + 1}, column {mark.column + 1}" if mark else ""
        problem = getattr(exc, "problem", None) or "invalid YAML"
        raise StoryError(f"{path}: {problem}{loc}") from None
    except UnicodeDecodeError:
        raise StoryError(f"{path}: file is not valid UTF-8") from None
    try:
        return parse_story(data, source=path)
    except StoryError as exc:
        raise StoryError(f"{path}: {exc}") from None


SAMPLE_STORY = """\
# tutshot story: each step becomes one screenshot, plus a combined story.png.
# Output is scripted, so keep paths tidy (~/project, ./docs) instead of real machine paths.
title: my-tool            # window title
theme: dusk               # dusk | paper | nord
cwd: ~/project            # shown in the title bar
width: 88                 # terminal columns (CJK characters count as 2)

steps:
  - id: install           # becomes install.png
    caption: Install the tool
    command: pip install my-tool
    output: |
      Successfully installed my-tool-1.0.0

  - id: hello
    caption: Run your first command
    command: my-tool hello --name world
    # Chinese / Japanese text works too, e.g.  command: my-tool hello "你好，世界"
    output: |
      Hello, world!
      Done in 0.02s

# Render with:  tutshot render tutshot.yml --out docs/images
"""
