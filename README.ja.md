<p align="center">
  <img src="docs/images/social-preview.png" alt="tutshot — YAML のコマンドストーリーを README 用チュートリアル画像に" width="100%">
</p>

<h1 align="center">tutshot</h1>

<p align="center">
  <b>短い YAML の「コマンドストーリー」から、チュートリアル風の README スクリーンショットを作ります。</b><br>
  ウィンドウ枠、番号付きキャプション、日本語・中国語もきれいに表示 —— ブラウザも録画も不要です。
</p>

<p align="center">
  <a href="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml"><img src="https://github.com/Xkongai/tutshot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <b>日本語</b>
</p>

```bash
pip install tutshot
tutshot init          # tutshot.yml を作成
tutshot render        # docs/images/{ステップ}.png と story.png を作成
```

CLI ツールの README には「実際の画面はこうです」というスクリーンショットが欠かせません。手作業で撮ると
実際のマシンのパス（`/Users/alice/dev/tmp3`）や雑多なプロンプトが写り込み、出力が変わるたびに撮り直しです。
**tutshot** ではチュートリアルを *スクリプトとして書きます*。各ステップのコマンド・出力・キャプションを YAML に書けば、
いつでも再生成できる、きれいで統一感のある PNG が得られます。

## 目次

- [できること](#できること)
- [デモ](#デモ)
- [インストール](#インストール)
- [30 秒クイックスタート](#30-秒クイックスタート)
- [ストーリーファイルの書き方](#ストーリーファイルの書き方)
- [テーマ](#テーマ)
- [フォントと CJK テキスト](#フォントと-cjk-テキスト)
- [freeze / vhs / termshot との違い](#freeze--vhs--termshot-との違い)
- [Python API](#python-api)
- [開発](#開発)
- [ライセンス](#ライセンス)

## できること

- **ストーリーを書けば画像になる。** 1 つの YAML ファイルにチュートリアルを番号付きステップとして記述すると、
  ステップごとの PNG（`install.png`、`init.png` …）と縦に並べた絵コンテ `story.png` を出力します。
- **チュートリアル向けの見た目。** 出力は自分で書くので、ドキュメントには `~/project` や `./docs` が表示され、
  たまたま作業していたディレクトリは写りません。
- **本物の端末らしいデザイン。** macOS 風のウィンドウ（信号機ボタンとタイトルバー）、緑の `$` プロンプト、
  太字のコマンド、ブロックカーソル、やわらかい影、角丸。
- **くっきりした文字。** すべて 2 倍で描画してから縮小します。`--scale 2` で Retina 品質の画像を出力できます。
- **CJK を正しく扱う。** 文字幅は East Asian Width で計算（日本語・中国語は 2 桁）するので、折り返しや桁揃えが崩れません。
  ストーリーに CJK 文字があるのに CJK フォントがない場合は、豆腐（□）を出力せずにインストール方法を表示して終了します。
- **小さく、オフライン。** 依存は Pillow・PyYAML・Typer のみの純 Python。Chrome も Playwright も asciinema も不要、
  ネットワーク接続や API キーもいりません。

## デモ

このリポジトリの [`tutshot.yml`](tutshot.yml) から tutshot が生成した絵コンテです（`tutshot render`）：

<p align="center">
  <img src="docs/images/story.png" alt="tutshot の絵コンテ：install、init、ストーリー編集、render" width="88%">
</p>

各ステップは個別の画像としても保存されるので、README の該当セクションにそのまま貼れます：

<p align="center">
  <img src="docs/images/render.png" alt="tutshot render のステップ" width="88%">
</p>

日本語と中国語もこのとおりです（[`examples/hello.yml`](examples/hello.yml)、`nord` テーマ、カスタムプロンプト）：

<p align="center">
  <img src="docs/images/hello/story.png" alt="日本語と中国語のコマンドを描画した tutshot" width="74%">
</p>

## インストール

```bash
pip install tutshot
```

クローンしたソースから（開発用・最新版）：

```bash
git clone https://github.com/Xkongai/tutshot.git
cd tutshot
pip install -e .
```

Python 3.11 以上が必要です。バージョンは `tutshot --version` で確認できます。

## 30 秒クイックスタート

```bash
cd ~/project
tutshot init                 # 1. サンプルの tutshot.yml を作成
$EDITOR tutshot.yml          # 2. サンプルのステップを自分のコマンドと出力に書き換える
tutshot render               # 3. PNG が docs/images/ に出力される
```

あとは README から参照するだけです：

```markdown
![インストール](docs/images/install.png)
```

コマンドとオプション：

| コマンド | 説明 |
| --- | --- |
| `tutshot init [path]` | サンプルのストーリーを作成（既定 `./tutshot.yml`、`--force` で上書き） |
| `tutshot render [file]` | `file`（既定 `tutshot.yml`）をステップごとの PNG と `story.png` に描画 |
| `  --out DIR` / `-o` | 出力ディレクトリ（既定 `docs/images`） |
| `  --theme dusk\|paper\|nord` | ストーリーで指定したテーマを上書き |
| `  --scale 2` | Retina 出力（2 倍のピクセル数） |
| `  --no-sheet` | `story.png` を作らない |
| `tutshot fonts` | 見つかった等幅 / CJK / UI フォントを表示 |
| `tutshot --version` | バージョンを表示 |

終了コード：`0` 成功、`2` ストーリーまたはオプションが不正、`3` 描画できない（CJK フォントがないなど）。

## ストーリーファイルの書き方

```yaml
title: tutshot           # ウィンドウタイトルの先頭（既定 bash）
theme: dusk              # dusk | paper | nord（既定 dusk、--theme で上書き可）
cwd: ~/project           # タイトルバーに表示するだけのパス（既定 ~）
prompt: user@tutorial    # 省略可。"$ " の代わりに "user@tutorial:~/project$ " と表示
width: 88                # 端末の桁数 40–200（既定 88 → 画像幅 約 1018 px）
caret: true              # 最後にブロックカーソル付きのプロンプトを描く（既定 true）
steps:
  - id: init             # 必須。ファイル名になる → init.png（英数字、- と _）
    caption: ストーリーを書き始める   # 省略可。ステップ番号付きでウィンドウの上に表示
    command: tutshot init             # 必須。複数行も可
    output: |                         # 省略可。空でもよい
      Wrote tutshot.yml
```

tutshot は次のルールをチェックし、該当ステップを示す分かりやすいエラーを出します：

- `id` と `command` は必須。id は重複不可（大文字小文字を区別しない）で、`[A-Za-z0-9_-]+` に一致する必要があります。
- `story` は絵コンテ用のファイル名として予約されています。
- 未知のキーは候補付きで拒否されます（`ouput` → *did you mean 'output'?*）。
- 長い行は表示幅で折り返し、長いコマンドは 2 桁インデントして続けます。
- タブは 4 桁に展開されます。

> **ヒント：** 出力はできるだけ本物に。ツールの実際の出力を貼り、読者に見せる必要のない部分 ——
> 絶対パス、ユーザー名、毎回変わる実行時間など —— だけを整えましょう。

## テーマ

| `dusk`（既定） | `paper` | `nord` |
| --- | --- | --- |
| <img src="docs/images/themes/dusk/preview.png" alt="dusk テーマ"> | <img src="docs/images/themes/paper/preview.png" alt="paper テーマ"> | <img src="docs/images/themes/nord/preview.png" alt="nord テーマ"> |
| GitHub ダーク風 | 明るい README 向けのライト | Nord パレット |

どの画像も角が透明な角丸なので、GitHub のライトモードでもダークモードでもなじみます。

## フォントと CJK テキスト

tutshot は Linux・macOS・Windows の一般的なフォントフォルダを探します：

- **端末テキスト：** JetBrains Mono、Cascadia Mono/Code、Menlo、Consolas、Noto Sans Mono、
  DejaVu Sans Mono、Liberation Mono、Ubuntu Mono、Source Code Pro …
- **CJK：** Noto Sans (Mono) CJK、源ノ角ゴシック（Source Han Sans）、PingFang、Hiragino Sans GB、
  Microsoft YaHei、游ゴシック、WenQuanYi Micro/Zen Hei、Droid Sans Fallback、Songti、SimSun …
- **タイトルバーとキャプション：** Inter、Segoe UI、Helvetica、Noto Sans、DejaVu Sans …（なければ等幅フォント）。

実際に選ばれたフォントは `tutshot fonts` で確認できます。フォントを指定したい場合は環境変数でファイルを指定します：

```bash
TUTSHOT_MONO_FONT=~/fonts/JetBrainsMono-Regular.ttf \
TUTSHOT_CJK_FONT=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
tutshot render
```

`TUTSHOT_UI_FONT` も同様に使え、`TUTSHOT_FONT_DIRS` で検索フォルダを追加できます。

英語だけのストーリーなら DejaVu や Liberation フォントだけで描画できます。日本語・中国語・韓国語を含む
ストーリーには CJK フォントが必要で、ない場合は次のように表示して終了します：

```text
error: no CJK font found. Install Noto Sans CJK, e.g. `sudo apt install fonts-noto-cjk` ...
```

v0.1 では絵文字には対応していません（カラー絵文字の描画がありません）。

## freeze / vhs / termshot との違い

解決する問題が異なり、組み合わせて使うこともできます：

- **実際の端末をピクセル単位で再現**したい（色もそのまま）なら [freeze](https://github.com/charmbracelet/freeze)
  や [termshot](https://github.com/homeport/termshot)。
- **アニメーションで録画**したいなら [vhs](https://github.com/charmbracelet/vhs) や asciinema。
- **チュートリアルの絵コンテ**を作りたい —— 番号とキャプション付きの複数ステップ、整ったパス、自分で管理する出力を、
  テキストファイルから CI で再生成したい —— なら tutshot です。

tutshot は（今のところ）コマンドを実行せず、実際の出力の ANSI カラーも保持せず、シンタックスハイライトもしません。
出力はあなたが書き、tutshot はそれを描きます。

## Python API

```python
from tutshot import load_story, render_story

story = load_story("tutshot.yml")
paths = render_story(story, "docs/images", theme="paper", scale=2)
```

`parse_story(dict)` は読み込み済みのデータを検証します。`tutshot.render.Renderer` を使うと、ウィンドウ単体や
カードを Pillow の画像として取得できます（このリポジトリのソーシャルプレビュー画像はその方法で作っています。
[`examples/social_preview.py`](examples/social_preview.py) を参照）。

## 開発

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
bash examples/build_docs.sh    # docs/images/ の画像をすべて再生成
```

[CONTRIBUTING.md](CONTRIBUTING.md) と [CHANGELOG.md](CHANGELOG.md) も参照してください。

## ライセンス

[MIT](LICENSE) © 2026 Xkongai
