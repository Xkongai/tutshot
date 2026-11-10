<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — YAML-Befehlsgeschichten als Tutorial-Screenshots für die README" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>Verwandelt eine kurze YAML-„Befehlsgeschichte“ in README-Screenshots im Tutorial-Stil.</b><br>
  Fensterrahmen, nummerierte Beschriftungen und erstklassiger chinesischer und japanischer Text — kein Browser, keine Aufnahme.
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português (Brasil)</a> | <a href="README.fr.md">Français</a> | <b>Deutsch</b> | <a href="README.ko.md">한국어</a> | <a href="README.ru.md">Русский</a>
</p>

```bash
pip install tutshot
tutshot init          # writes tutshot.yml
tutshot render        # writes docs/images/{step}.png + story.png
```

Jedes CLI-Projekt braucht in der README Screenshots nach dem Motto „so sieht es aus“. Von Hand entstehen
echte Maschinenpfade (`/Users/alice/dev/tmp3`), eine unordentliche Eingabeaufforderung, und bei jeder
geänderten Ausgabe fängt man von vorn an. **tutshot** lässt Sie das Tutorial *als Skript schreiben*: Befehl,
Ausgabe und Beschriftung jedes Schritts stehen in YAML, und Sie bekommen saubere, einheitliche PNGs, die
Sie jederzeit neu erzeugen können.

## Inhalt

- [Was es macht](#was-es-macht)
- [Demo](#demo)
- [Installation](#installation)
- [Schnellstart in 30 Sekunden](#schnellstart-in-30-sekunden)
- [Referenz der Story-Datei](#referenz-der-story-datei)
- [Themen](#themen)
- [Schriften und CJK-Text](#schriften-und-cjk-text)
- [tutshot im Vergleich zu freeze / vhs / termshot](#tutshot-im-vergleich-zu-freeze--vhs--termshot)
- [Python API](#python-api)
- [Entwicklung](#entwicklung)
- [Lizenz](#lizenz)

## Was es macht

- **Geschichte hinein, Screenshots heraus.** Eine YAML-Datei beschreibt ein Tutorial als nummerierte
  Schritte; tutshot schreibt ein PNG pro Schritt (`install.png`, `init.png`, …) und ein vertikales Storyboard, `story.png`.
- **Tutorial-sauber, von vornherein.** Die Ausgabe ist geschrieben, deshalb zeigen die Docs `~/project`
  und `./docs`, nicht das Verzeichnis, in dem Sie zufällig waren.
- **Sieht aus wie ein echtes Terminal.** Fenster im macOS-Stil mit Ampelknöpfen und Titelleiste, eine grüne
  `$`-Eingabeaufforderung, fette Befehle, ein Blockcursor, ein weicher Schlagschatten, abgerundete Ecken.
- **Scharfer Text.** Alles wird mit 2× gezeichnet und dann verkleinert; `--scale 2` liefert retina-scharfe Ausgabe.
- **CJK richtig gemacht.** Zeichen werden nach ostasiatischer Breite gemessen (中文 / 日本語 belegen zwei
  Spalten), deshalb bleiben Umbruch und Ausrichtung korrekt. Enthält die Story CJK und ist keine CJK-Schrift
  installiert, bricht tutshot mit einem Installationshinweis ab, statt Kästchen (Tofu) zu schreiben.
- **Klein und offline.** Reines Python auf Pillow, PyYAML und Typer. Kein Chrome, kein Playwright,
  kein asciinema, kein Netz, keine API-Schlüssel.

## Demo

Das ist das Storyboard, das tutshot aus [`tutshot.yml`](tutshot.yml) in diesem Repository erzeugt hat
(`tutshot render`):

<p align="center">
  <img src="docs/images/story.png" alt="tutshot-Storyboard: install, init, die Story bearbeiten, render" width="88%">
</p>

Jeder Schritt wird auch einzeln gespeichert, bereit zum Einfügen neben dem passenden README-Abschnitt:

<p align="center">
  <img src="docs/images/render.png" alt="tutshot-Schritt render" width="88%">
</p>

Und dasselbe mit chinesischem und japanischem Text ([`examples/hello.yml`](examples/hello.yml), Thema `nord`, eigene Eingabeaufforderung):

<p align="center">
  <img src="docs/images/hello/story.png" alt="tutshot zeichnet chinesische und japanische Befehle" width="74%">
</p>

## Installation

```bash
pip install tutshot
```

Aus einem Klon (für die Entwicklung oder den neuesten Code):

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Erfordert Python 3.11+. Die Version prüfen Sie mit `tutshot --version`.

## Schnellstart in 30 Sekunden

```bash
cd ~/project
tutshot init                 # 1. write a sample tutshot.yml
$EDITOR tutshot.yml          # 2. replace the sample steps with your own commands and output
tutshot render               # 3. PNGs land in docs/images/
```

Danach in der README darauf verweisen:

```markdown
![Install](docs/images/install.png)
```

Nützliche Optionen:

| Befehl | Wirkung |
| --- | --- |
| `tutshot init [path]` | Schreibt eine Beispiel-Story (Standard `./tutshot.yml`; `--force` zum Überschreiben) |
| `tutshot render [file]` | Rendert `file` (Standard `tutshot.yml`) zu einem PNG pro Schritt plus `story.png` |
| `  --out DIR` / `-o` | Ausgabeverzeichnis (Standard `docs/images`) |
| `  --theme dusk\|paper\|nord` | Überschreibt das in der Story gesetzte Thema |
| `  --scale 2` | Retina-Ausgabe (2× Pixel) |
| `  --no-sheet` | `story.png` weglassen |
| `tutshot fonts` | Zeigt, welche Mono- / CJK- / UI-Schriften gefunden wurden |
| `tutshot --version` | Gibt die Version aus |

Exit-Codes: `0` ok, `2` ungültige Story oder Optionen, `3` Rendern nicht möglich (zum Beispiel eine fehlende CJK-Schrift).

## Referenz der Story-Datei

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

Regeln, die tutshot für Sie prüft, mit einer klaren Fehlermeldung, die auf den Schritt zeigt:

- `id` und `command` sind erforderlich; ids müssen eindeutig sein (ohne Unterscheidung der Groß-/Kleinschreibung) und `[A-Za-z0-9_-]+` entsprechen.
- `story` ist für die Storyboard-Datei reserviert.
- Unbekannte Schlüssel werden mit einem Vorschlag abgelehnt (`ouput` → *did you mean 'output'?*).
- Lange Zeilen werden nach der Anzeigebreite umbrochen; lange Befehle gehen mit einem Einzug von zwei Leerzeichen weiter.
- Tabulatoren werden auf 4 Spalten erweitert.

> **Tipp:** Halten Sie die Ausgabe ehrlich. Fügen Sie die echte Ausgabe Ihres Werkzeugs ein und räumen
> Sie nur das weg, was eine lesende Person nicht sehen sollte — absolute Maschinenpfade, Benutzernamen
> und Laufzeiten, die sich bei jedem Aufruf ändern.

## Themen

| `dusk` (Standard) | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="Thema dusk"> | <img src="docs/images/themes/paper/preview.png" alt="Thema paper"> | <img src="docs/images/themes/nord/preview.png" alt="Thema nord"> |
| An GitHub Dark angelehnt | Hell, für helle READMEs gemacht | Die Nord-Palette |

Alle Bilder haben transparente abgerundete Ecken und sitzen deshalb sowohl im hellen als auch im dunklen GitHub-Modus gut.

## Schriften und CJK-Text

tutshot sucht Schriften in den üblichen Schriftordnern von Linux, macOS und Windows:

- **Terminaltext:** JetBrains Mono, Cascadia Mono/Code, Menlo, Consolas, Noto Sans Mono,
  DejaVu Sans Mono, Liberation Mono, Ubuntu Mono, Source Code Pro, …
- **CJK:** Noto Sans (Mono) CJK, Source Han Sans, PingFang, Hiragino Sans GB, Microsoft YaHei,
  Yu Gothic, WenQuanYi Micro/Zen Hei, Droid Sans Fallback, Songti, SimSun, …
- **Titelleiste und Beschriftungen:** Inter, Segoe UI, Helvetica, Noto Sans, DejaVu Sans, … (sonst
  die Monospace-Schrift).

`tutshot fonts` zeigt, welche gewählt wurde. Um eine Schrift zu erzwingen, lassen Sie eine Umgebungsvariable auf die Datei zeigen:

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` funktioniert genauso, und `TUTSHOT_FONT_DIRS` fügt weitere Suchordner hinzu.

Geschichten nur mit lateinischer Schrift kommen mit DejaVu- oder Liberation-Schriften aus. Geschichten mit
chinesischem, japanischem oder koreanischem Text brauchen eine CJK-Schrift; ohne sie beendet sich tutshot mit:

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

Emoji werden in v0.1 nicht unterstützt (es gibt kein Farb-Emoji-Rendering).

## tutshot im Vergleich zu freeze / vhs / termshot

Sie lösen verschiedene Aufgaben und ergänzen sich gut:

- Sie wollen eine **pixelgenaue Aufnahme eines laufenden Terminals**, inklusive der echten Farben? Nehmen Sie
  [freeze](https://github.com/charmbracelet/freeze) oder [termshot](https://github.com/homeport/termshot).
- Sie wollen eine **animierte Aufzeichnung** einer Sitzung? Nehmen Sie [vhs](https://github.com/charmbracelet/vhs) oder asciinema.
- Sie wollen ein **Tutorial als Storyboard** — mehrere nummerierte Schritte mit Beschriftungen, aufgeräumte Pfade
  und eine Ausgabe, die Sie bestimmen, aus einer Textdatei in der CI neu erzeugt? Dafür ist tutshot da.

Was tutshot (noch) *nicht* tut: Ihre Befehle ausführen, ANSI-Farben aus echter Ausgabe behalten oder Syntax
hervorheben. Sie schreiben die Ausgabe; tutshot zeichnet sie.

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` prüft bereits geladene Daten, und `tutshot.render.Renderer` liefert die einzelnen
Fenster- oder Kartenbilder als Pillow-Objekte (die Social-Vorschau in diesem Repository entsteht so —
siehe [`examples/social_preview.py`](examples/social_preview.py)).

## Entwicklung

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # regenerate every image in docs/images/
```

Siehe [CONTRIBUTING.md](CONTRIBUTING.md) und [CHANGELOG.md](CHANGELOG.md).

## Lizenz

[MIT](LICENSE) © 2026 Xkongai
