import pytest

from tutshot import StoryError, load_story, parse_story
from tutshot.story import DEFAULT_WIDTH, SAMPLE_STORY

import yaml


def test_load_basic(fixtures):
    story = load_story(fixtures / "basic.yml")
    assert [s.id for s in story.steps] == ["one", "two"]
    assert story.steps[0].caption == "First step"
    assert story.steps[0].output == "ok"
    assert story.steps[1].output == ""
    assert story.steps[1].caption is None
    assert story.width == 60
    assert story.window_title == "demo — ~/project"


def test_defaults():
    story = parse_story({"steps": [{"id": "x", "command": "ls"}]})
    assert story.width == DEFAULT_WIDTH
    assert story.theme is None
    assert story.caret is True
    assert story.window_title == "bash — ~"


def test_prompt_in_title():
    story = parse_story({"prompt": "user@tutorial", "cwd": "~/p", "steps": [{"id": "x", "command": "ls"}]})
    assert story.window_title == "bash — user@tutorial:~/p"


def test_sample_story_is_valid():
    story = parse_story(yaml.safe_load(SAMPLE_STORY))
    assert len(story.steps) == 2


@pytest.mark.parametrize(
    "data, message",
    [
        ([], "mapping"),
        ({}, "steps is required"),
        ({"steps": []}, "non-empty"),
        ({"steps": [{"command": "ls"}]}, "id is required"),
        ({"steps": [{"id": "a"}]}, "command is required"),
        ({"steps": [{"id": "a", "command": "  "}]}, "must not be empty"),
        ({"steps": [{"id": "a b", "command": "ls"}]}, "may only contain"),
        ({"steps": [{"id": "../x", "command": "ls"}]}, "may only contain"),
        ({"steps": [{"id": "story", "command": "ls"}]}, "reserved"),
        ({"steps": [{"id": "a", "command": "ls"}, {"id": "A", "command": "ls"}]}, "duplicate"),
        ({"steps": [{"id": "a", "command": "ls", "ouput": "x"}]}, "did you mean 'output'"),
        ({"titel": "x", "steps": [{"id": "a", "command": "ls"}]}, "did you mean 'title'"),
        ({"theme": "neon", "steps": [{"id": "a", "command": "ls"}]}, "unknown theme"),
        ({"width": 10, "steps": [{"id": "a", "command": "ls"}]}, "between"),
        ({"width": "wide", "steps": [{"id": "a", "command": "ls"}]}, "integer"),
        ({"caret": "yes", "steps": [{"id": "a", "command": "ls"}]}, "true or false"),
        ({"steps": ["ls"]}, "mapping"),
        ({"steps": [{"id": "a", "command": ["ls"]}]}, "must be a string"),
    ],
)
def test_validation_errors(data, message):
    with pytest.raises(StoryError, match=message):
        parse_story(data)


def test_duplicate_file(fixtures):
    with pytest.raises(StoryError, match="duplicate id 'a'"):
        load_story(fixtures / "duplicate.yml")


def test_missing_file(tmp_path):
    with pytest.raises(StoryError, match="not found"):
        load_story(tmp_path / "nope.yml")


def test_bad_yaml(tmp_path):
    p = tmp_path / "bad.yml"
    p.write_text("steps: [\n  - id: a\n", encoding="utf-8")
    with pytest.raises(StoryError, match="line"):
        load_story(p)
