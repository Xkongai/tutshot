<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — histórias de comandos em YAML como capturas de tutorial para o README" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>Transforme uma breve “história de comandos” em YAML em capturas de README no estilo de um tutorial.</b><br>
  Moldura da janela, legendas numeradas e texto em chinês e japonês de primeira classe — sem navegador e sem gravação.
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <b>Português (Brasil)</b> | <a href="README.fr.md">Français</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ko.md">한국어</a> | <a href="README.ru.md">Русский</a>
</p>

```bash
pip install tutshot
tutshot init          # writes tutshot.yml
tutshot render        # writes docs/images/{step}.png + story.png
```

Todo projeto de linha de comando precisa de capturas de “é assim que fica” no README. Fazê-las à mão
significa caminhos reais da máquina (`/Users/alice/dev/tmp3`), um prompt bagunçado e refazer tudo quando
a saída muda. O **tutshot** deixa você *escrever o tutorial como um script*: anote no YAML o comando, a
saída e a legenda de cada passo e obtenha PNGs limpos e consistentes, que você pode gerar de novo quando quiser.

## Conteúdo

- [O que faz](#o-que-faz)
- [Demonstração](#demonstração)
- [Instalação](#instalação)
- [Início rápido em 30 segundos](#início-rápido-em-30-segundos)
- [Referência do arquivo de história](#referência-do-arquivo-de-história)
- [Temas](#temas)
- [Fontes e texto CJK](#fontes-e-texto-cjk)
- [tutshot versus freeze / vhs / termshot](#tutshot-versus-freeze--vhs--termshot)
- [Python API](#python-api)
- [Desenvolvimento](#desenvolvimento)
- [Licença](#licença)

## O que faz

- **História entra, capturas saem.** Um arquivo YAML descreve um tutorial como passos numerados; o tutshot
  grava um PNG por passo (`install.png`, `init.png`, …) e um storyboard vertical, `story.png`.
- **Limpo para tutorial, por construção.** A saída é escrita por você, então a documentação mostra
  `~/project` e `./docs`, não o diretório em que você por acaso estava.
- **Parece um terminal de verdade.** Janela no estilo do macOS, com os botões de semáforo e uma barra de
  título, um prompt `$` verde, comandos em negrito, um cursor de bloco, uma sombra suave e cantos arredondados.
- **Texto nítido.** Tudo é desenhado em 2× e depois reduzido; `--scale 2` produz uma saída nítida para Retina.
- **CJK feito direito.** Os caracteres são medidos pela largura do Leste Asiático (中文 / 日本語 ocupam duas
  colunas), então a quebra de linha e o alinhamento continuam corretos. Se a história contém CJK e não há
  uma fonte CJK instalada, o tutshot para com uma dica de instalação em vez de desenhar quadradinhos (tofu).
- **Pequeno e offline.** Python puro, em cima de Pillow, PyYAML e Typer. Sem Chrome, sem Playwright,
  sem asciinema, sem rede e sem chaves de API.

## Demonstração

Este é o storyboard que o tutshot gerou a partir de [`tutshot.yml`](tutshot.yml) neste repositório
(`tutshot render`):

<p align="center">
  <img src="docs/images/story.png" alt="storyboard do tutshot: install, init, editar a história, render" width="88%">
</p>

Cada passo também é salvo à parte, pronto para ficar ao lado da seção correspondente do README:

<p align="center">
  <img src="docs/images/render.png" alt="passo render do tutshot" width="88%">
</p>

E a mesma coisa com texto em chinês e japonês ([`examples/hello.yml`](examples/hello.yml), tema `nord`, prompt personalizado):

<p align="center">
  <img src="docs/images/hello/story.png" alt="tutshot desenhando comandos em chinês e japonês" width="74%">
</p>

## Instalação

```bash
pip install tutshot
```

A partir de um clone (para desenvolver ou usar o código mais recente):

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Requer Python 3.11+. Confira a versão com `tutshot --version`.

## Início rápido em 30 segundos

```bash
cd ~/project
tutshot init                 # 1. write a sample tutshot.yml
$EDITOR tutshot.yml          # 2. replace the sample steps with your own commands and output
tutshot render               # 3. PNGs land in docs/images/
```

Depois, referencie as imagens no seu README:

```markdown
![Install](docs/images/install.png)
```

Opções úteis:

| Comando | O que faz |
| --- | --- |
| `tutshot init [path]` | Grava uma história de exemplo (padrão `./tutshot.yml`; `--force` para sobrescrever) |
| `tutshot render [file]` | Renderiza `file` (padrão `tutshot.yml`) em um PNG por passo e `story.png` |
| `  --out DIR` / `-o` | Diretório de saída (padrão `docs/images`) |
| `  --theme dusk\|paper\|nord` | Substitui o tema definido na história |
| `  --scale 2` | Saída Retina (pixels em 2×) |
| `  --no-sheet` | Não gera `story.png` |
| `tutshot fonts` | Mostra quais fontes monoespaçadas / CJK / de interface foram encontradas |
| `tutshot --version` | Imprime a versão |

Códigos de saída: `0` ok, `2` história ou opções inválidas, `3` não é possível renderizar (por exemplo, falta uma fonte CJK).

## Referência do arquivo de história

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

Regras que o tutshot confere para você, com uma mensagem de erro clara apontando para o passo:

- `id` e `command` são obrigatórios; os ids devem ser únicos (sem diferenciar maiúsculas de minúsculas) e corresponder a `[A-Za-z0-9_-]+`.
- `story` é reservado para o arquivo do storyboard.
- Chaves desconhecidas são rejeitadas com uma sugestão (`ouput` → *did you mean 'output'?*).
- Linhas longas são quebradas pela largura de exibição; comandos longos continuam com um recuo de dois espaços.
- Tabulações se expandem para 4 colunas.

> **Dica:** mantenha a saída honesta. Cole a saída real da sua ferramenta e arrume só o que o leitor
> não deveria ver — caminhos absolutos da máquina, nomes de usuário e tempos que mudam a cada execução.

## Temas

| `dusk` (padrão) | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="tema dusk"> | <img src="docs/images/themes/paper/preview.png" alt="tema paper"> | <img src="docs/images/themes/nord/preview.png" alt="tema nord"> |
| Inspirado no GitHub Dark | Claro, feito para READMEs claros | A paleta Nord |

Todas as imagens têm cantos arredondados transparentes, então ficam bem tanto no modo claro quanto no escuro do GitHub.

## Fontes e texto CJK

O tutshot procura fontes nas pastas habituais do Linux, do macOS e do Windows:

- **Texto do terminal:** JetBrains Mono, Cascadia Mono/Code, Menlo, Consolas, Noto Sans Mono,
  DejaVu Sans Mono, Liberation Mono, Ubuntu Mono, Source Code Pro, …
- **CJK:** Noto Sans (Mono) CJK, Source Han Sans, PingFang, Hiragino Sans GB, Microsoft YaHei,
  Yu Gothic, WenQuanYi Micro/Zen Hei, Droid Sans Fallback, Songti, SimSun, …
- **Barra de título e legendas:** Inter, Segoe UI, Helvetica, Noto Sans, DejaVu Sans, … (se não houver,
  usa a fonte monoespaçada).

Execute `tutshot fonts` para ver qual foi escolhida. Para forçar uma fonte, aponte uma variável de ambiente para o arquivo:

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` funciona do mesmo jeito, e `TUTSHOT_FONT_DIRS` acrescenta pastas extras à busca.

Para histórias só em alfabeto latino, as fontes DejaVu ou Liberation bastam. Histórias com texto
em chinês, japonês ou coreano precisam de uma fonte CJK; sem ela, o tutshot sai com:

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

Emoji não é suportado na v0.1 (não há renderização de emoji colorido).

## tutshot versus freeze / vhs / termshot

Eles resolvem problemas diferentes e funcionam bem juntos:

- Quer uma **captura pixel a pixel de um terminal ao vivo**, com as cores reais e tudo? Use
  [freeze](https://github.com/charmbracelet/freeze) ou [termshot](https://github.com/homeport/termshot).
- Quer uma **gravação animada** de uma sessão? Use [vhs](https://github.com/charmbracelet/vhs) ou o asciinema.
- Quer **montar o storyboard de um tutorial** — vários passos numerados com legendas, caminhos arrumados e uma saída
  que você controla, regenerada a partir de um arquivo de texto na CI? É para isso que o tutshot existe.

O que o tutshot *não* faz (ainda): executar os seus comandos, preservar as cores ANSI de uma saída real ou
destacar a sintaxe. Você escreve a saída; o tutshot desenha.

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` valida dados que já foram carregados, e `tutshot.render.Renderer` entrega as
imagens avulsas da janela ou do cartão como objetos do Pillow (a prévia para redes deste repositório é
construída assim — veja [`examples/social_preview.py`](examples/social_preview.py)).

## Desenvolvimento

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # regenerate every image in docs/images/
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md) e [CHANGELOG.md](CHANGELOG.md).

## Licença

[MIT](LICENSE) © 2026 Xkongai
