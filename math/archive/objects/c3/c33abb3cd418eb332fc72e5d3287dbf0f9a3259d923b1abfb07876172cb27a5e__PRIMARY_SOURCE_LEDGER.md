# Primary-source ledger

Retrieved 2026-10-10, approximately 05:48–05:53 UTC. Public external program/TeX files were read and saved as inert text only; none was executed, imported, compiled, or AST-parsed.

## External exact-transform preprint

Official author: OpenAI. Manuscript date: September 25, 2026. Directory latest commit returned by the public GitHub connector: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, Initial commit, 2026-10-06T21:58:50Z. This is a source version identifier, not peer-review or proof-verification evidence.

- `primary_sources/publication_readme.md.txt`: https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/README.md
- `primary_sources/paper_main.tex.txt`: https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/main.tex
- `primary_sources/model_and_theorem.tex.txt`: https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/introduction.tex
- `primary_sources/working_lengths.tex.txt`: https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/all-lengths.tex
- `primary_sources/paper_directory_commit.json.txt`: https://api.github.com/repos/openai/math/commits?path=preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026&per_page=1
- `primary_sources/formalization_scope.md.txt`: https://raw.githubusercontent.com/openai/math/main/lean/docs/130.md
- `primary_sources/formalization_main.lean.txt`: https://raw.githubusercontent.com/openai/math/main/lean/OAI/Computability/FourierTransform/Main.lean
- `primary_sources/comparator_statement.lean.txt`: https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/UniformFourier.lean
- `primary_sources/comparator_config.json.txt`: https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/UniformFourier.json

The all-length manuscript source was directly retrievable although the raw PDF URL returned an unsupported-content-type error in the web tool. Source-directory GitHub API responses supplied file paths and hashes. No search snippet is used as theorem evidence. The proof-body snapshot is current-main content, which need not have the same history as the manuscript directory. Its dependency proof and formal build were not checked.

## Classical ingredients and algorithmic context

- Alexeev, Cahill, Mixon, *Full Spark Frames*, JFAA 18 (2012), 1167–1194. Author-hosted primary PDF: https://borisalexeev.com/pdf/spark.pdf . Read Lemma 2 and the discussion after Theorem 4 on consecutive Fourier rows. This explicitly predates the interval full-spark ingredient used in the report.
- FFTW authors, *Pruned FFTs*: https://fftw.org/pruned.html . Read the standard selected-output construction and its scope. Supplied example code was not executed.
- Schechter, *On the inversion of certain matrices*, Math. Comp. 13 (1959), 73–77: https://doi.org/10.1090/S0025-5718-1959-0105798-2 . AMS PDF fetch returned HTTP 403; the historical attribution is stated, but this source's full text was not inspected. The report provides an independent elementary proof of the precise Cauchy nonsingularity fact it needs.
- Ying, *Sparse Fourier Transform via Butterfly Algorithm* (2008): https://arxiv.org/abs/0801.1524 . The abstract explicitly concerns approximate low rank for bounded space-frequency products. Used only to check the exact-versus-approximate scope distinction; no approximation theorem is imported.

## Local source text inspected

- `selected_convolution_construction_0421/SELECTED_CONVOLUTION_CONSTRUCTION.md`
- `normalized_frontier_independent_audit_0422/INDEPENDENT_NORMALIZED_FRONTIER_AUDIT.md`
- `normalized_packet_escape_0358/NORMALIZED_PACKET_ESCAPE.md`
- `fft_research_master_20261009/CURRENT_CHECKPOINT.md`

The first four are hashed in INPUTS.before.sha256 and INPUTS.after.sha256. Targeted text search in the master also confirmed that the external OpenAI preprint was already cited there. No central registry or master file was edited.
