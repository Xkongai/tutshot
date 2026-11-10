<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — YAML 명령 스토리를 README용 튜토리얼 스크린샷으로" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>짧은 YAML “명령 스토리”를 튜토리얼 스타일의 README 스크린샷으로 바꿉니다.</b><br>
  창 테두리, 번호가 매겨진 캡션, 일급으로 다루는 중국어·일본어 텍스트 — 브라우저도, 녹화도 필요 없습니다.
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português (Brasil)</a> | <a href="README.fr.md">Français</a> | <a href="README.de.md">Deutsch</a> | <b>한국어</b> | <a href="README.ru.md">Русский</a>
</p>

```bash
pip install tutshot
tutshot init          # writes tutshot.yml
tutshot render        # writes docs/images/{step}.png + story.png
```

모든 CLI 프로젝트의 README에는 “이렇게 생겼습니다”라는 스크린샷이 필요합니다. 직접 찍으면 실제 컴퓨터
경로(`/Users/alice/dev/tmp3`)와 지저분한 프롬프트가 들어가고, 출력이 바뀔 때마다 처음부터 다시 찍어야
합니다. **tutshot**은 튜토리얼을 *스크립트로 쓰게* 해 줍니다. 각 단계의 명령, 출력, 캡션을 YAML에 적으면
언제든 다시 만들 수 있는, 깨끗하고 일관된 PNG를 얻습니다.

## 목차

- [하는 일](#하는-일)
- [데모](#데모)
- [설치](#설치)
- [30초 빠른 시작](#30초-빠른-시작)
- [스토리 파일 참조](#스토리-파일-참조)
- [테마](#테마)
- [글꼴과 CJK 텍스트](#글꼴과-cjk-텍스트)
- [tutshot 대 freeze / vhs / termshot](#tutshot-대-freeze--vhs--termshot)
- [Python API](#python-api)
- [개발](#개발)
- [라이선스](#라이선스)

## 하는 일

- **스토리를 넣으면 스크린샷이 나옵니다.** YAML 파일 하나가 튜토리얼을 번호 단계로 설명합니다. tutshot은
  단계마다 PNG 하나(`install.png`, `init.png`, …)와 세로 스토리보드 `story.png`를 씁니다.
- **처음부터 튜토리얼에 맞게 깨끗합니다.** 출력은 직접 적는 것이므로, 문서에는 그때 마침 있던 디렉터리가
  아니라 `~/project`와 `./docs`가 나옵니다.
- **진짜 터미널처럼 보입니다.** 신호등 버튼과 제목 표시줄이 있는 macOS 스타일 창, 초록색 `$` 프롬프트,
  굵은 명령, 블록 캐럿, 부드러운 그림자, 둥근 모서리.
- **선명한 글자.** 모든 것을 2배로 그린 뒤 축소합니다. `--scale 2`는 레티나급으로 선명한 출력입니다.
- **CJK를 제대로 처리합니다.** 문자는 동아시아 폭으로 잽니다(中文 / 日本語는 두 칸). 그래서 줄바꿈과
  정렬이 맞습니다. 스토리에 CJK가 있는데 CJK 글꼴이 없으면, tutshot은 네모 상자(tofu)를 그리지 않고
  설치 안내를 남기고 멈춥니다.
- **작고, 오프라인입니다.** Pillow, PyYAML, Typer 위의 순수 Python입니다. Chrome도, Playwright도,
  asciinema도 없고, 네트워크도, API 키도 필요 없습니다.

## 데모

이 저장소의 [`tutshot.yml`](tutshot.yml)로 tutshot이 만든 스토리보드입니다(`tutshot render`):

<p align="center">
  <img src="docs/images/story.png" alt="tutshot 스토리보드: install, init, 스토리 편집, render" width="88%">
</p>

각 단계도 따로 저장되므로, README의 해당 절 옆에 그대로 둘 수 있습니다.

<p align="center">
  <img src="docs/images/render.png" alt="tutshot render 단계" width="88%">
</p>

중국어와 일본어 텍스트도 마찬가지입니다([`examples/hello.yml`](examples/hello.yml), `nord` 테마, 사용자 지정 프롬프트):

<p align="center">
  <img src="docs/images/hello/story.png" alt="중국어와 일본어 명령을 그리는 tutshot" width="74%">
</p>

## 설치

```bash
pip install tutshot
```

클론에서 (개발하거나 최신 코드를 쓰려면):

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Python 3.11 이상이 필요합니다. 버전은 `tutshot --version`으로 확인합니다.

## 30초 빠른 시작

```bash
cd ~/project
tutshot init                 # 1. write a sample tutshot.yml
$EDITOR tutshot.yml          # 2. replace the sample steps with your own commands and output
tutshot render               # 3. PNGs land in docs/images/
```

그다음 README에서 참조합니다.

```markdown
![Install](docs/images/install.png)
```

유용한 옵션:

| 명령 | 하는 일 |
| --- | --- |
| `tutshot init [path]` | 예시 스토리를 씁니다(기본값 `./tutshot.yml`, `--force`로 덮어쓰기) |
| `tutshot render [file]` | `file`(기본값 `tutshot.yml`)을 단계별 PNG와 `story.png`로 렌더합니다 |
| `  --out DIR` / `-o` | 출력 디렉터리(기본값 `docs/images`) |
| `  --theme dusk\|paper\|nord` | 스토리에 설정된 테마를 덮어씁니다 |
| `  --scale 2` | 레티나 출력(2배 픽셀) |
| `  --no-sheet` | `story.png`를 만들지 않습니다 |
| `tutshot fonts` | 찾은 고정폭 / CJK / UI 글꼴을 보여 줍니다 |
| `tutshot --version` | 버전을 출력합니다 |

종료 코드: `0` 성공, `2` 스토리나 옵션이 잘못됨, `3` 렌더할 수 없음(예를 들어 CJK 글꼴이 없을 때).

## 스토리 파일 참조

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

tutshot이 대신 검사하는 규칙입니다. 해당 단계를 가리키는 분명한 오류 메시지를 냅니다.

- `id`와 `command`는 필수입니다. id는 고유해야 하고(대소문자 구분 없음) `[A-Za-z0-9_-]+`와 맞아야 합니다.
- `story`는 스토리보드 파일용으로 예약되어 있습니다.
- 알 수 없는 키는 제안과 함께 거부됩니다(`ouput` → *did you mean 'output'?*).
- 긴 줄은 표시 폭으로 줄바꿈되고, 긴 명령은 공백 두 칸을 들여 이어집니다.
- 탭은 4칸으로 펼쳐집니다.

> **팁:** 출력은 정직하게 두세요. 도구의 실제 출력을 붙이고, 독자가 보면 안 되는 것만 다듬으세요.
> 절대 경로, 사용자 이름, 실행할 때마다 바뀌는 소요 시간 같은 것입니다.

## 테마

| `dusk` (기본값) | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="dusk 테마"> | <img src="docs/images/themes/paper/preview.png" alt="paper 테마"> | <img src="docs/images/themes/nord/preview.png" alt="nord 테마"> |
| GitHub Dark에서 따옴 | 밝은 README를 위한 라이트 | Nord 팔레트 |

모든 이미지는 투명한 둥근 모서리를 가져, GitHub 라이트 모드와 다크 모드 모두에서 잘 앉습니다.

## 글꼴과 CJK 텍스트

tutshot은 Linux, macOS, Windows의 흔한 글꼴 폴더를 찾습니다.

- **터미널 텍스트:** JetBrains Mono, Cascadia Mono/Code, Menlo, Consolas, Noto Sans Mono,
  DejaVu Sans Mono, Liberation Mono, Ubuntu Mono, Source Code Pro, …
- **CJK:** Noto Sans (Mono) CJK, Source Han Sans, PingFang, Hiragino Sans GB, Microsoft YaHei,
  Yu Gothic, WenQuanYi Micro/Zen Hei, Droid Sans Fallback, Songti, SimSun, …
- **제목 표시줄과 캡션:** Inter, Segoe UI, Helvetica, Noto Sans, DejaVu Sans, … (없으면
  고정폭 글꼴을 씁니다).

`tutshot fonts`를 실행하면 어떤 글꼴이 골라졌는지 볼 수 있습니다. 글꼴을 고정하려면 환경 변수가 그 파일을 가리키게 하세요.

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT`도 같은 방식이고, `TUTSHOT_FONT_DIRS`는 검색할 폴더를 더합니다.

라틴 문자만 있는 스토리는 DejaVu나 Liberation 글꼴만으로 됩니다. 중국어, 일본어, 한국어가 있는
스토리에는 CJK 글꼴이 필요하고, 없으면 tutshot은 다음을 내고 끝납니다.

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

v0.1에서는 이모지를 지원하지 않습니다(컬러 이모지 렌더링이 없습니다).

## tutshot 대 freeze / vhs / termshot

푸는 문제가 다르고, 함께 쓰면 잘 맞습니다.

- **실행 중인 터미널을 픽셀 그대로 담고** 실제 색까지 원하면 [freeze](https://github.com/charmbracelet/freeze)나
  [termshot](https://github.com/homeport/termshot)을 쓰세요.
- 세션의 **애니메이션 녹화**가 필요하면 [vhs](https://github.com/charmbracelet/vhs)나 asciinema를 쓰세요.
- **튜토리얼의 스토리보드**가 필요하면 — 캡션이 있는 여러 번호 단계, 정돈된 경로, 직접 통제하는 출력을
  텍스트 파일에서 CI로 다시 만들고 싶다면 — tutshot이 그 도구입니다.

tutshot이 (아직은) *하지 않는* 일: 명령을 실행하지 않고, 실제 출력의 ANSI 색을 보존하지 않으며, 구문
강조도 하지 않습니다. 출력은 직접 쓰고, tutshot은 그것을 그립니다.

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)`는 이미 불러온 데이터를 검사하고, `tutshot.render.Renderer`는 창이나 카드 이미지를
Pillow 객체로 돌려줍니다(이 저장소의 소셜 미리보기는 그렇게 만들었습니다.
[`examples/social_preview.py`](examples/social_preview.py)를 보세요).

## 개발

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # regenerate every image in docs/images/
```

[CONTRIBUTING.md](CONTRIBUTING.md)와 [CHANGELOG.md](CHANGELOG.md)를 보세요.

## 라이선스

[MIT](LICENSE) © 2026 Xkongai
