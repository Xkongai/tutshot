"""tutshot — turn a short YAML command story into tutorial-style README screenshots."""

from .story import Step, Story, StoryError, load_story, parse_story
from .render import RenderError, render_story

__version__ = "0.1.0"

__all__ = [
    "Step",
    "Story",
    "StoryError",
    "RenderError",
    "load_story",
    "parse_story",
    "render_story",
    "__version__",
]
