<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — истории команд в YAML как учебные скриншоты для README" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>Превращает короткую YAML-«историю команд» в скриншоты README в стиле учебника.</b><br>
  Рамка окна, нумерованные подписи и полноценный китайский и японский текст — без браузера и без записи.
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português (Brasil)</a> | <a href="README.fr.md">Français</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ko.md">한국어</a> | <b>Русский</b>
</p>

```bash
pip install tutshot
tutshot init          # writes tutshot.yml
tutshot render        # writes docs/images/{step}.png + story.png
```

Каждому проекту для командной строки нужны в README скриншоты «вот как это выглядит». Снятые вручную,
они тащат настоящие пути машины (`/Users/alice/dev/tmp3`), беспорядочное приглашение, и всё приходится
переснимать, когда вывод меняется. **tutshot** позволяет *написать учебник как сценарий*: команду, вывод
и подпись каждого шага вы задаёте в YAML и получаете чистые, одинаковые PNG, которые можно заново
собрать в любой момент.

## Содержание

- [Что он делает](#что-он-делает)
- [Демонстрация](#демонстрация)
- [Установка](#установка)
- [Быстрый старт за 30 секунд](#быстрый-старт-за-30-секунд)
- [Справка по файлу истории](#справка-по-файлу-истории)
- [Темы](#темы)
- [Шрифты и текст CJK](#шрифты-и-текст-cjk)
- [tutshot в сравнении с freeze / vhs / termshot](#tutshot-в-сравнении-с-freeze--vhs--termshot)
- [Python API](#python-api)
- [Разработка](#разработка)
- [Лицензия](#лицензия)

## Что он делает

- **История на входе, скриншоты на выходе.** Один файл YAML описывает учебник нумерованными шагами;
  tutshot пишет PNG на каждый шаг (`install.png`, `init.png`, …) и вертикальную раскадровку, `story.png`.
- **Чистый вид для учебника заложен в основу.** Вывод написан вами, поэтому в документации видны
  `~/project` и `./docs`, а не каталог, в котором вы случайно оказались.
- **Похоже на настоящий терминал.** Окно в стиле macOS со светофорными кнопками и заголовком, зелёное
  приглашение `$`, жирные команды, блочный курсор, мягкая тень, скруглённые углы.
- **Чёткий текст.** Всё рисуется в 2× и затем уменьшается; `--scale 2` даёт резкий вывод уровня Retina.
- **CJK сделан правильно.** Ширина символов считается по восточноазиатской ширине (中文 / 日本語 занимают
  два столбца), поэтому перенос и выравнивание остаются верными. Если в истории есть CJK, а шрифта CJK
  нет, tutshot останавливается с подсказкой по установке, а не рисует квадратики (тофу).
- **Маленький и офлайн.** Чистый Python поверх Pillow, PyYAML и Typer. Без Chrome, без Playwright,
  без asciinema, без сети и без ключей API.

## Демонстрация

Это раскадровка, которую tutshot собрал из [`tutshot.yml`](tutshot.yml) в этом репозитории
(`tutshot render`):

<p align="center">
  <img src="docs/images/story.png" alt="раскадровка tutshot: install, init, правка истории, render" width="88%">
</p>

Каждый шаг сохраняется и отдельно — его можно поставить рядом с соответствующим разделом README:

<p align="center">
  <img src="docs/images/render.png" alt="шаг render в tutshot" width="88%">
</p>

И то же самое с китайским и японским текстом ([`examples/hello.yml`](examples/hello.yml), тема `nord`, своё приглашение):

<p align="center">
  <img src="docs/images/hello/story.png" alt="tutshot рисует команды на китайском и японском" width="74%">
</p>

## Установка

```bash
pip install tutshot
```

Из клона (для разработки или самого свежего кода):

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Нужен Python 3.11+. Версию смотрите через `tutshot --version`.

## Быстрый старт за 30 секунд

```bash
cd ~/project
tutshot init                 # 1. write a sample tutshot.yml
$EDITOR tutshot.yml          # 2. replace the sample steps with your own commands and output
tutshot render               # 3. PNGs land in docs/images/
```

Затем сошлитесь на них из README:

```markdown
![Install](docs/images/install.png)
```

Полезные параметры:

| Команда | Что делает |
| --- | --- |
| `tutshot init [path]` | Пишет пример истории (по умолчанию `./tutshot.yml`; `--force`, чтобы перезаписать) |
| `tutshot render [file]` | Рендерит `file` (по умолчанию `tutshot.yml`) в PNG на каждый шаг и `story.png` |
| `  --out DIR` / `-o` | Каталог вывода (по умолчанию `docs/images`) |
| `  --theme dusk\|paper\|nord` | Переопределяет тему, заданную в истории |
| `  --scale 2` | Вывод Retina (пиксели 2×) |
| `  --no-sheet` | Не создавать `story.png` |
| `tutshot fonts` | Показывает найденные моноширинные шрифты, шрифты CJK и шрифты интерфейса |
| `tutshot --version` | Печатает версию |

Коды выхода: `0` успешно, `2` неверная история или параметры, `3` отрисовать нельзя (например, нет шрифта CJK).

## Справка по файлу истории

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

Правила, которые tutshot проверяет за вас, с ясным сообщением об ошибке, указывающим на шаг:

- `id` и `command` обязательны; идентификаторы должны быть уникальны (без учёта регистра) и соответствовать `[A-Za-z0-9_-]+`.
- `story` зарезервирован для файла раскадровки.
- Неизвестные ключи отклоняются с подсказкой (`ouput` → *did you mean 'output'?*).
- Длинные строки переносятся по ширине отображения; длинные команды продолжаются с отступом в два пробела.
- Табуляции разворачиваются в 4 столбца.

> **Совет:** пусть вывод будет честным. Вставляйте настоящий вывод инструмента и прибирайте только то,
> чего читатель видеть не должен — абсолютные пути машины, имена пользователей и длительности, которые меняются при каждом запуске.

## Темы

| `dusk` (по умолчанию) | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="тема dusk"> | <img src="docs/images/themes/paper/preview.png" alt="тема paper"> | <img src="docs/images/themes/nord/preview.png" alt="тема nord"> |
| По мотивам GitHub Dark | Светлая, для светлых README | Палитра Nord |

У всех изображений прозрачные скруглённые углы, поэтому они хорошо смотрятся и в светлом, и в тёмном режиме GitHub.

## Шрифты и текст CJK

tutshot ищет шрифты в обычных папках шрифтов Linux, macOS и Windows:

- **Текст терминала:** JetBrains Mono, Cascadia Mono/Code, Menlo, Consolas, Noto Sans Mono,
  DejaVu Sans Mono, Liberation Mono, Ubuntu Mono, Source Code Pro, …
- **CJK:** Noto Sans (Mono) CJK, Source Han Sans, PingFang, Hiragino Sans GB, Microsoft YaHei,
  Yu Gothic, WenQuanYi Micro/Zen Hei, Droid Sans Fallback, Songti, SimSun, …
- **Заголовок окна и подписи:** Inter, Segoe UI, Helvetica, Noto Sans, DejaVu Sans, … (если их нет,
  берётся моноширинный шрифт).

Запустите `tutshot fonts`, чтобы увидеть, что выбрано. Чтобы принудить шрифт, укажите переменной окружения путь к файлу:

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` работает так же, а `TUTSHOT_FONT_DIRS` добавляет дополнительные папки для поиска.

Для историй только на латинице хватает шрифтов DejaVu или Liberation. Истории с китайским,
японским или корейским текстом требуют шрифт CJK; без него tutshot завершается так:

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

Эмодзи в v0.1 не поддерживаются (цветного рендеринга эмодзи нет).

## tutshot в сравнении с freeze / vhs / termshot

Они решают разные задачи и хорошо работают вместе:

- Нужен **снимок живого терминала с точностью до пикселя**, с настоящими цветами? Возьмите
  [freeze](https://github.com/charmbracelet/freeze) или [termshot](https://github.com/homeport/termshot).
- Нужна **анимированная запись** сеанса? Возьмите [vhs](https://github.com/charmbracelet/vhs) или asciinema.
- Нужно **раскадровать учебник** — несколько нумерованных шагов с подписями, аккуратные пути и вывод,
  которым вы управляете, заново собранный из текстового файла в CI? Для этого и есть tutshot.

Чего tutshot *не* делает (пока): не запускает ваши команды, не сохраняет цвета ANSI из настоящего вывода
и не подсвечивает синтаксис. Вывод пишете вы; tutshot его рисует.

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` проверяет уже загруженные данные, а `tutshot.render.Renderer` отдаёт отдельные
изображения окна или карточки как объекты Pillow (социальное превью в этом репозитории собрано именно
так — см. [`examples/social_preview.py`](examples/social_preview.py)).

## Разработка

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # regenerate every image in docs/images/
```

См. [CONTRIBUTING.md](CONTRIBUTING.md) и [CHANGELOG.md](CHANGELOG.md).

## Лицензия

[MIT](LICENSE) © 2026 Xkongai
