<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — historias de comandos en YAML como capturas de tutorial para tu README" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>Convierte una breve «historia de comandos» en YAML en capturas de README al estilo de un tutorial.</b><br>
  Marco de la ventana, leyendas numeradas y texto en chino y japonés de primera clase — sin navegador y sin grabación.
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <b>Español</b> | <a href="README.pt-BR.md">Português (Brasil)</a> | <a href="README.fr.md">Français</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ko.md">한국어</a> | <a href="README.ru.md">Русский</a>
</p>

```bash
pip install tutshot
tutshot init          # writes tutshot.yml
tutshot render        # writes docs/images/{step}.png + story.png
```

Todo proyecto de línea de comandos necesita en su README capturas de «así es como se ve». Hacerlas a
mano supone rutas reales de la máquina (`/Users/alice/dev/tmp3`), un prompt desordenado y rehacerlo
todo cuando cambia la salida. **tutshot** te permite *escribir el tutorial como un script*: anotas en
YAML el comando, la salida y la leyenda de cada paso, y obtienes PNG limpios y coherentes que puedes
regenerar cuando quieras.

## Contenido

- [Qué hace](#qué-hace)
- [Demostración](#demostración)
- [Instalación](#instalación)
- [Inicio rápido en 30 segundos](#inicio-rápido-en-30-segundos)
- [Referencia del archivo de historia](#referencia-del-archivo-de-historia)
- [Temas](#temas)
- [Fuentes y texto CJK](#fuentes-y-texto-cjk)
- [tutshot frente a freeze / vhs / termshot](#tutshot-frente-a-freeze--vhs--termshot)
- [Python API](#python-api)
- [Desarrollo](#desarrollo)
- [Licencia](#licencia)

## Qué hace

- **Historia dentro, capturas fuera.** Un archivo YAML describe un tutorial como pasos numerados; tutshot
  escribe un PNG por paso (`install.png`, `init.png`, …) y un storyboard vertical, `story.png`.
- **Limpio para tutoriales, por diseño.** La salida está escrita por ti, así que la documentación muestra
  `~/project` y `./docs`, no el directorio en el que casualmente estabas.
- **Parece una terminal de verdad.** Ventana al estilo de macOS, con los botones de semáforo y una barra
  de título, un prompt `$` verde, comandos en negrita, un cursor de bloque, una sombra suave y esquinas
  redondeadas.
- **Texto nítido.** Todo se dibuja a 2× y luego se reduce; `--scale 2` da una salida nítida para Retina.
- **CJK bien resuelto.** Los caracteres se miden por el ancho de Asia Oriental (中文 / 日本語 ocupan dos
  columnas), así que el ajuste de línea y la alineación siguen siendo correctos. Si la historia contiene
  CJK y no hay una fuente CJK instalada, tutshot se detiene con una pista de instalación en lugar de
  escribir recuadros (tofu).
- **Pequeño y sin conexión.** Python puro, sobre Pillow, PyYAML y Typer. Sin Chrome, sin Playwright,
  sin asciinema, sin red y sin claves de API.

## Demostración

Este es el storyboard que tutshot generó a partir de [`tutshot.yml`](tutshot.yml) en este repositorio
(`tutshot render`):

<p align="center">
  <img src="docs/images/story.png" alt="storyboard de tutshot: install, init, editar la historia, render" width="88%">
</p>

Cada paso también se guarda por separado, listo para colocarlo junto a la sección correspondiente del README:

<p align="center">
  <img src="docs/images/render.png" alt="paso render de tutshot" width="88%">
</p>

Y lo mismo con texto en chino y en japonés ([`examples/hello.yml`](examples/hello.yml), tema `nord`, prompt personalizado):

<p align="center">
  <img src="docs/images/hello/story.png" alt="tutshot dibujando comandos en chino y en japonés" width="74%">
</p>

## Instalación

```bash
pip install tutshot
```

Desde un clon (para desarrollar o usar el código más reciente):

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Requiere Python 3.11+. Comprueba la versión con `tutshot --version`.

## Inicio rápido en 30 segundos

```bash
cd ~/project
tutshot init                 # 1. write a sample tutshot.yml
$EDITOR tutshot.yml          # 2. replace the sample steps with your own commands and output
tutshot render               # 3. PNGs land in docs/images/
```

Luego referéncialas desde tu README:

```markdown
![Install](docs/images/install.png)
```

Opciones útiles:

| Comando | Qué hace |
| --- | --- |
| `tutshot init [path]` | Escribe una historia de ejemplo (por defecto `./tutshot.yml`; `--force` para sobrescribir) |
| `tutshot render [file]` | Renderiza `file` (por defecto `tutshot.yml`) a un PNG por paso y `story.png` |
| `  --out DIR` / `-o` | Directorio de salida (por defecto `docs/images`) |
| `  --theme dusk\|paper\|nord` | Sustituye el tema definido en la historia |
| `  --scale 2` | Salida Retina (píxeles a 2×) |
| `  --no-sheet` | Omite `story.png` |
| `tutshot fonts` | Muestra qué fuentes monoespaciadas / CJK / de interfaz se encontraron |
| `tutshot --version` | Imprime la versión |

Códigos de salida: `0` correcto, `2` historia u opciones no válidas, `3` no se puede renderizar (por ejemplo, falta una fuente CJK).

## Referencia del archivo de historia

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

Reglas que tutshot comprueba por ti, con un mensaje de error claro que señala el paso:

- `id` y `command` son obligatorios; los id deben ser únicos (sin distinguir mayúsculas de minúsculas) y coincidir con `[A-Za-z0-9_-]+`.
- `story` está reservado para el archivo del storyboard.
- Las claves desconocidas se rechazan con una sugerencia (`ouput` → *did you mean 'output'?*).
- Las líneas largas se ajustan según el ancho de visualización; los comandos largos continúan con una sangría de dos espacios.
- Los tabuladores se expanden a 4 columnas.

> **Consejo:** mantén la salida fiel. Pega la salida real de tu herramienta y retoca solo lo que un lector
> no debería ver: rutas absolutas de la máquina, nombres de usuario y tiempos que cambian en cada ejecución.

## Temas

| `dusk` (predeterminado) | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="tema dusk"> | <img src="docs/images/themes/paper/preview.png" alt="tema paper"> | <img src="docs/images/themes/nord/preview.png" alt="tema nord"> |
| Inspirado en GitHub Dark | Claro, pensado para README claros | La paleta Nord |

Todas las imágenes tienen esquinas redondeadas transparentes, así que quedan bien tanto en el modo claro como en el oscuro de GitHub.

## Fuentes y texto CJK

tutshot busca fuentes en las carpetas habituales de Linux, macOS y Windows:

- **Texto de la terminal:** JetBrains Mono, Cascadia Mono/Code, Menlo, Consolas, Noto Sans Mono,
  DejaVu Sans Mono, Liberation Mono, Ubuntu Mono, Source Code Pro, …
- **CJK:** Noto Sans (Mono) CJK, Source Han Sans, PingFang, Hiragino Sans GB, Microsoft YaHei,
  Yu Gothic, WenQuanYi Micro/Zen Hei, Droid Sans Fallback, Songti, SimSun, …
- **Barra de título y leyendas:** Inter, Segoe UI, Helvetica, Noto Sans, DejaVu Sans, … (si no hay,
  usa la fuente monoespaciada).

Ejecuta `tutshot fonts` para ver cuál se eligió. Para forzar una fuente, apunta una variable de entorno al archivo:

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` funciona igual, y `TUTSHOT_FONT_DIRS` añade carpetas extra a la búsqueda.

Las historias solo en alfabeto latino funcionan con las fuentes DejaVu o Liberation. Las historias con
texto en chino, japonés o coreano necesitan una fuente CJK; sin ella, tutshot termina con:

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

Los emoji no están admitidos en la v0.1 (no hay renderizado de emoji a color).

## tutshot frente a freeze / vhs / termshot

Resuelven problemas distintos y combinan bien:

- ¿Quieres una **captura al píxel de una terminal en vivo**, con los colores reales incluidos? Usa
  [freeze](https://github.com/charmbracelet/freeze) o [termshot](https://github.com/homeport/termshot).
- ¿Quieres una **grabación animada** de una sesión? Usa [vhs](https://github.com/charmbracelet/vhs) o asciinema.
- ¿Quieres **hacer el storyboard de un tutorial** — varios pasos numerados con leyendas, rutas ordenadas y una salida
  que tú controlas, regenerada desde un archivo de texto en CI? Para eso está tutshot.

Lo que tutshot *no* hace (todavía): ejecutar tus comandos, conservar los colores ANSI de una salida real ni
resaltar la sintaxis. Tú escribes la salida; tutshot la dibuja.

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` valida datos que ya están cargados, y `tutshot.render.Renderer` te da las
imágenes sueltas de la ventana o de la tarjeta como objetos de Pillow (la vista previa para redes de este
repositorio se construye así; consulta [`examples/social_preview.py`](examples/social_preview.py)).

## Desarrollo

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # regenerate every image in docs/images/
```

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y [CHANGELOG.md](CHANGELOG.md).

## Licencia

[MIT](LICENSE) © 2026 Xkongai
