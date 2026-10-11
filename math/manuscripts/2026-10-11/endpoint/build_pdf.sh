#!/usr/bin/env bash
# Rebuild the mathematical PDF from the editable LaTeX source.
set -euo pipefail
cd "$(dirname "$0")"
if [[ -d /usr/share/texlive/texmf-dist && -d /usr/share/texmf ]]; then
  export TEXMF='{/usr/share/texlive/texmf-dist,/usr/share/texmf}'
fi
cache=$(mktemp -d)
trap 'rm -rf "$cache"' EXIT
export TEXMFVAR="$cache" TEXMFCONFIG="$cache"
if ! kpsewhich pdflatex.fmt >/dev/null 2>&1; then
  (cd "$cache" && pdftex -ini -etex -jobname=pdflatex -progname=pdflatex \
    -interaction=nonstopmode -halt-on-error pdflatex.ini > format_build.log)
  export TEXFORMATS="$cache"
fi
pdflatex -interaction=nonstopmode -halt-on-error WORKING_MANUSCRIPT.tex
pdflatex -interaction=nonstopmode -halt-on-error WORKING_MANUSCRIPT.tex
