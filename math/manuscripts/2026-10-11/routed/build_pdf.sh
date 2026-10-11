#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
pandoc MANUSCRIPT.md --from markdown+tex_math_dollars+tex_math_single_backslash --to latex --standalone -o MANUSCRIPT.tex
# This environment has read-only TeX assets and no system-generated format/map.
# Build only the format/cache in a temporary directory, without installing software.
cache="${TMPDIR:-/tmp}/routed-manuscript-tex"
mkdir -p "$cache" qa
export TEXMF="{$cache,/usr/share/texmf,/usr/share/texlive/texmf-dist}"
export TEXMFDBS="$cache" TEXFORMATS="$cache" TEXFONTMAPS="$cache"
export TEXINPUTS=".:/usr/share/texlive/texmf-dist/tex//:/usr/share/texmf/tex//"
if [[ ! -f "$cache/pdflatex.fmt" ]]; then
  ( cd "$cache"; pdftex -ini -etex -interaction=nonstopmode -halt-on-error -jobname=pdflatex -progname=pdflatex pdflatex.ini > format.log )
fi
cat /usr/share/texmf/fonts/map/dvips/lm/lm.map /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/*.map > "$cache/pdftex.map"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=qa MANUSCRIPT.tex > qa/build.log
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=qa MANUSCRIPT.tex >> qa/build.log
cp qa/MANUSCRIPT.pdf MANUSCRIPT.pdf
