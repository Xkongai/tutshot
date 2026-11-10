<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — 把 YAML 命令故事变成 README 教程截图" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>把一小段 YAML“命令故事”变成教程风格的 README 截图。</b><br>
  窗口外框、带编号的步骤说明、原生支持中文 / 日文 —— 不需要浏览器，也不需要录屏。
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <b>简体中文</b> | <a href="README.ja.md">日本語</a>
</p>

```bash
pip install tutshot
tutshot init          # 生成 tutshot.yml
tutshot render        # 生成 docs/images/{步骤}.png 和 story.png
```

每个命令行项目的 README 都需要“用起来是这样的”截图。手动截图往往会带上真实的机器路径
（`/Users/alice/dev/tmp3`）、杂乱的提示符，而且输出一变就得全部重截。**tutshot** 让你把教程
*写成脚本*：在 YAML 里写好每一步的命令、输出和说明，就能得到干净、统一、随时可以重新生成的 PNG。

## 目录

- [功能](#功能)
- [效果展示](#效果展示)
- [安装](#安装)
- [30 秒上手](#30-秒上手)
- [故事文件格式](#故事文件格式)
- [主题](#主题)
- [字体与中日韩文字](#字体与中日韩文字)
- [与 freeze / vhs / termshot 的区别](#与-freeze--vhs--termshot-的区别)
- [Python API](#python-api)
- [开发](#开发)
- [许可证](#许可证)

## 功能

- **写故事，出截图。** 一个 YAML 文件按编号步骤描述一段教程；tutshot 为每一步生成一张 PNG
  （`install.png`、`init.png` …），再加一张竖向拼接的分镜图 `story.png`。
- **天生适合教程。** 输出由你编写，文档里显示的是 `~/project`、`./docs`，而不是你当时碰巧所在的目录。
- **像真的终端。** macOS 风格窗口（红黄绿三个按钮 + 标题栏）、绿色 `$` 提示符、加粗命令、方块光标、柔和阴影、圆角。
- **文字清晰。** 所有内容先按 2 倍绘制再缩小；`--scale 2` 可直接输出 Retina 清晰度。
- **认真处理中日韩文字。** 按东亚宽度计算字符宽度（中文 / 日文占两列），换行和对齐都不会错位。
  如果故事里有中日韩文字却没装对应字体，tutshot 会直接报错并给出安装提示，而不是输出一堆方框（豆腐块）。
- **小巧、离线。** 纯 Python，依赖只有 Pillow、PyYAML 和 Typer。不需要 Chrome、Playwright、asciinema，
  不联网，也不需要任何 API Key。

## 效果展示

下面是 tutshot 用本仓库的 [`tutshot.yml`](tutshot.yml) 生成的分镜图（`tutshot render`）：

<p align="center">
  <img src="docs/images/story.png" alt="tutshot 分镜图：安装、init、编辑故事、render" width="88%">
</p>

每一步也会单独保存一张，可以直接放到 README 对应的小节旁边：

<p align="center">
  <img src="docs/images/render.png" alt="tutshot render 这一步" width="88%">
</p>

中文和日文同样没问题（[`examples/hello.yml`](examples/hello.yml)，`nord` 主题，自定义提示符）：

<p align="center">
  <img src="docs/images/hello/story.png" alt="tutshot 渲染中文和日文命令" width="74%">
</p>

## 安装

```bash
pip install tutshot
```

从源码安装（开发或使用最新代码）：

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

需要 Python 3.11+。用 `tutshot --version` 查看版本。

## 30 秒上手

```bash
cd ~/project
tutshot init                 # 1. 生成示例 tutshot.yml
$EDITOR tutshot.yml          # 2. 把示例步骤换成你自己的命令和输出
tutshot render               # 3. PNG 会写到 docs/images/
```

然后在 README 里引用：

```markdown
![安装](docs/images/install.png)
```

常用命令与选项：

| 命令 | 作用 |
| --- | --- |
| `tutshot init [path]` | 生成示例故事（默认 `./tutshot.yml`；`--force` 覆盖已有文件） |
| `tutshot render [file]` | 渲染 `file`（默认 `tutshot.yml`），每步一张 PNG + `story.png` |
| `  --out DIR` / `-o` | 输出目录（默认 `docs/images`） |
| `  --theme dusk\|paper\|nord` | 覆盖故事里设置的主题 |
| `  --scale 2` | Retina 输出（2 倍像素） |
| `  --no-sheet` | 不生成 `story.png` |
| `tutshot fonts` | 显示找到的等宽 / 中日韩 / 界面字体 |
| `tutshot --version` | 显示版本 |

退出码：`0` 成功，`2` 故事文件或参数无效，`3` 无法渲染（例如缺少中日韩字体）。

## 故事文件格式

```yaml
title: tutshot           # 窗口标题前缀（默认 bash）
theme: dusk              # dusk | paper | nord（默认 dusk；--theme 可覆盖）
cwd: ~/project           # 只用于显示的路径，出现在标题栏（默认 ~）
prompt: user@tutorial    # 可选；提示符显示为 "user@tutorial:~/project$ " 而不是 "$ "
width: 88                # 终端列数，40–200（默认 88，图片约 1018 像素宽）
caret: true              # 末尾画一个带方块光标的提示符（默认 true）
steps:
  - id: init             # 必填；作为文件名 → init.png（字母、数字、- 和 _）
    caption: 开始写教程故事        # 可选；带步骤编号显示在窗口上方
    command: tutshot init         # 必填；可以多行
    output: |                     # 可选；可以为空
      Wrote tutshot.yml
```

tutshot 会帮你检查以下规则，并给出指向具体步骤的错误信息：

- `id` 和 `command` 必填；id 不能重复（不区分大小写），且只能匹配 `[A-Za-z0-9_-]+`。
- `story` 保留给分镜图文件使用。
- 未知字段会被拒绝并给出建议（`ouput` → *did you mean 'output'?*）。
- 过长的行按显示宽度换行；过长的命令换行后缩进两格。
- Tab 展开为 4 列。

> **建议：** 输出尽量保持真实。粘贴工具的真实输出，只整理读者不该看到的部分 ——
> 绝对路径、用户名、每次运行都会变化的耗时等。

## 主题

| `dusk`（默认） | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="dusk 主题"> | <img src="docs/images/themes/paper/preview.png" alt="paper 主题"> | <img src="docs/images/themes/nord/preview.png" alt="nord 主题"> |
| 参考 GitHub 深色 | 浅色，适合浅色 README | Nord 配色 |

所有图片都是透明圆角，在 GitHub 浅色和深色模式下都很协调。

## 字体与中日韩文字

tutshot 会在 Linux、macOS、Windows 的常见字体目录中查找：

- **终端文字：** JetBrains Mono、Cascadia Mono/Code、Menlo、Consolas、Noto Sans Mono、
  DejaVu Sans Mono、Liberation Mono、Ubuntu Mono、Source Code Pro …
- **中日韩：** Noto Sans (Mono) CJK、思源黑体 Source Han Sans、苹方 PingFang、冬青黑体 Hiragino Sans GB、
  微软雅黑、Yu Gothic、文泉驿微米黑 / 正黑、Droid Sans Fallback、宋体 …
- **标题栏和步骤说明：** Inter、Segoe UI、Helvetica、Noto Sans、DejaVu Sans …（找不到时使用等宽字体）。

运行 `tutshot fonts` 可查看实际选用的字体。要强制使用某个字体，用环境变量指向字体文件：

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` 用法相同，`TUTSHOT_FONT_DIRS` 可以追加额外的搜索目录。

只含英文的故事有 DejaVu 或 Liberation 字体就能渲染。含中文、日文或韩文的故事需要中日韩字体；
没有的话 tutshot 会退出并提示：

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

v0.1 暂不支持 Emoji（没有彩色 Emoji 渲染）。

## 与 freeze / vhs / termshot 的区别

它们解决的是不同的问题，也可以搭配使用：

- 想要**像素级还原真实终端**（包括真实颜色）？用 [freeze](https://github.com/charmbracelet/freeze)
  或 [termshot](https://github.com/homeport/termshot)。
- 想要**动态录屏**？用 [vhs](https://github.com/charmbracelet/vhs) 或 asciinema。
- 想要**给教程做分镜** —— 多个带编号和说明的步骤、整洁的路径、由你掌控的输出，并且能在 CI 里从文本文件重新生成？
  这正是 tutshot 的用途。

tutshot（目前）*不会*执行你的命令、不会保留真实输出里的 ANSI 颜色，也不做语法高亮。输出由你来写，tutshot 负责画出来。

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` 可以校验已经加载的数据；`tutshot.render.Renderer` 能以 Pillow 图像对象的形式返回单个窗口或卡片
（本仓库的社交预览图就是这样生成的，见 [`examples/social_preview.py`](examples/social_preview.py)）。

## 开发

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # 重新生成 docs/images/ 中的所有图片
```

参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

[MIT](LICENSE) © 2026 Xkongai
