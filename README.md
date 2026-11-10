<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — YAML command stories to tutorial screenshots for your README" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>Turn a short YAML “command story” into tutorial-style README screenshots.</b><br>
  Window chrome, numbered captions and first-class Chinese / Japanese text — no browser, no recording.
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <b>English</b> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a>
</p>

```bash
pip install tutshot
tutshot init          # writes tutshot.yml
tutshot render        # writes docs/images/{step}.png + story.png
```

Every CLI project needs “here is what it looks like” screenshots in its README. Taking them by hand
means real machine paths (`/Users/alice/dev/tmp3`), a messy prompt, and redoing everything when the
output changes. **tutshot** lets you *script* the tutorial instead: write each step's command, output
and caption in YAML, and get clean, consistent PNGs you can regenerate any time.

## Contents

- [What it does](#what-it-does)
- [Demo](#demo)
- [Install](#install)
- [30-second quick start](#30-second-quick-start)
- [Story file reference](#story-file-reference)
- [Themes](#themes)
- [Fonts and CJK text](#fonts-and-cjk-text)
- [tutshot vs. freeze / vhs / termshot](#tutshot-vs-freeze--vhs--termshot)
- [Python API](#python-api)
- [Development](#development)
- [License](#license)

## What it does

- **Story in, screenshots out.** One YAML file describes a tutorial as numbered steps; tutshot
  writes one PNG per step (`install.png`, `init.png`, …) and a vertical storyboard, `story.png`.
- **Tutorial-clean by design.** Output is scripted, so your docs show `~/project` and `./docs`, not
  whatever directory you happened to be in.
- **Looks like a real terminal.** macOS-style window with traffic lights and a title bar, a green
  `$` prompt, bold commands, a block caret, a soft drop shadow, rounded corners.
- **Crisp text.** Everything is drawn at 2× and downsampled; `--scale 2` gives retina-sharp output.
- **CJK done right.** Characters are measured by East Asian width (中文 / 日本語 take two columns),
  so wrapping and alignment stay correct. If your story contains CJK and no CJK font is installed,
  tutshot stops with an install hint instead of writing boxes (tofu).
- **Small and offline.** Pure Python on top of Pillow, PyYAML and Typer. No Chrome, no Playwright,
  no asciinema, no network, no API keys.

## Demo

This is the storyboard tutshot generated from [`tutshot.yml`](tutshot.yml) in this repository
(`tutshot render`):

<p align="center">
  <img src="docs/images/story.png" alt="tutshot storyboard: install, init, edit the story, render" width="88%">
</p>

Each step is also saved on its own, ready to drop next to the matching README section:

<p align="center">
  <img src="docs/images/render.png" alt="tutshot render step" width="88%">
</p>

And the same thing with Chinese and Japanese text ([`examples/hello.yml`](examples/hello.yml), `nord` theme, custom prompt):

<p align="center">
  <img src="docs/images/hello/story.png" alt="tutshot rendering Chinese and Japanese commands" width="74%">
</p>

## Install

```bash
pip install tutshot
```

From a clone (for development or the latest code):

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Requires Python 3.11+. Check the version with `tutshot --version`.

## 30-second quick start

```bash
cd ~/project
tutshot init                 # 1. write a sample tutshot.yml
$EDITOR tutshot.yml          # 2. replace the sample steps with your own commands and output
tutshot render               # 3. PNGs land in docs/images/
```

Then reference them from your README:

```markdown
![Install](docs/images/install.png)
```

Useful options:

| Command | What it does |
| --- | --- |
| `tutshot init [path]` | Write a sample story (default `./tutshot.yml`; `--force` to overwrite) |
| `tutshot render [file]` | Render `file` (default `tutshot.yml`) to one PNG per step + `story.png` |
| `  --out DIR` / `-o` | Output directory (default `docs/images`) |
| `  --theme dusk\|paper\|nord` | Override the theme set in the story |
| `  --scale 2` | Retina output (2× pixels) |
| `  --no-sheet` | Skip `story.png` |
| `tutshot fonts` | Show which monospace / CJK / UI fonts were found |
| `tutshot --version` | Print the version |

Exit codes: `0` ok, `2` invalid story or options, `3` cannot render (for example a missing CJK font).

## Story file reference

```yaml
title: tutshot           # window title prefix (default: bash)
theme: dusk              # dusk | paper | nord (default: dusk; --theme overrides)
cwd: ~/project           # display-only path in the title bar (default: ~)
prompt: user@tutorial    # optional; shows "user@tutorial:~/project$ " instead of "$ "
width: 88                # terminal columns, 40–200 (default: 88 → ~1018 px wide images)
caret: true              # draw a final prompt with a block caret (default: true)
steps:
  - id: init             # required; file name → init.png (letters, digits, - and _)
    caption: Start a tutorial story   # optional; shown above the window with a step number
    command: tutshot init             # required; may span several lines
    output: |                         # optional; may be empty
      Wrote tutshot.yml
```

Rules tutshot checks for you, with a clear error message pointing at the step:

- `id` and `command` are required; ids must be unique (case-insensitive) and match `[A-Za-z0-9_-]+`.
- `story` is reserved for the storyboard file.
- Unknown keys are rejected with a suggestion (`ouput` → *did you mean 'output'?*).
- Long lines are wrapped by display width; long commands continue with a two-space indent.
- Tabs expand to 4 columns.

> **Tip:** keep the output honest. Paste real output from your tool and only tidy what a reader
> should not see — absolute machine paths, user names, timings that change every run.

## Themes

| `dusk` (default) | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="dusk theme"> | <img src="docs/images/themes/paper/preview.png" alt="paper theme"> | <img src="docs/images/themes/nord/preview.png" alt="nord theme"> |
| GitHub-dark inspired | Light, made for light READMEs | The Nord palette |

All images have transparent rounded corners, so they sit nicely on both GitHub light and dark mode.

## Fonts and CJK text

tutshot looks for fonts in the usual Linux, macOS and Windows font folders:

- **Terminal text:** JetBrains Mono, Cascadia Mono/Code, Menlo, Consolas, Noto Sans Mono,
  DejaVu Sans Mono, Liberation Mono, Ubuntu Mono, Source Code Pro, …
- **CJK:** Noto Sans (Mono) CJK, Source Han Sans, PingFang, Hiragino Sans GB, Microsoft YaHei,
  Yu Gothic, WenQuanYi Micro/Zen Hei, Droid Sans Fallback, Songti, SimSun, …
- **Title bar and captions:** Inter, Segoe UI, Helvetica, Noto Sans, DejaVu Sans, … (falls back to
  the monospace font).

Run `tutshot fonts` to see what was picked. To force a font, point an environment variable at the file:

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` works the same way, and `TUTSHOT_FONT_DIRS` adds extra folders to search.

Latin-only stories work with just DejaVu or Liberation fonts. Stories with Chinese, Japanese or
Korean text need a CJK font; without one tutshot exits with:

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

Emoji are not supported in v0.1 (there is no color-emoji rendering).

## tutshot vs. freeze / vhs / termshot

They solve different problems, and they work well together:

- Want a **pixel-perfect capture of a live terminal**, real colors and all? Use
  [freeze](https://github.com/charmbracelet/freeze) or [termshot](https://github.com/homeport/termshot).
- Want an **animated recording** of a session? Use [vhs](https://github.com/charmbracelet/vhs) or asciinema.
- Want to **storyboard a tutorial** — several numbered steps with captions, tidy paths, and output
  you control, regenerated from a text file in CI? That is what tutshot is for.

What tutshot does *not* do (yet): run your commands, keep ANSI colors from real output, or
syntax-highlight. You write the output; tutshot draws it.

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` validates already-loaded data, and `tutshot.render.Renderer` gives you the
individual window or card images as Pillow objects (the social preview in this repo is built
that way — see [`examples/social_preview.py`](examples/social_preview.py)).

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # regenerate every image in docs/images/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) © 2026 Xkongai
