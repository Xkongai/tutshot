#!/usr/bin/env bash
# Regenerate every image in docs/images/ with the installed tutshot CLI.
# Run from the repository root:  bash examples/build_docs.sh
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf docs/images
tutshot render tutshot.yml --out docs/images
tutshot render examples/hello.yml --out docs/images/hello
for theme in dusk paper nord; do
  tutshot render "examples/themes/${theme}.yml" --theme "$theme" --out "docs/images/themes/$theme" --no-sheet
done
python examples/social_preview.py
