# ALG-031: accepted bounded shared-a concentration

Public, inert research package · 21 October 2026 UTC

## What is accepted

The original affine-chirp sketch and natural adjoint can reuse one fixed nonzero quadratic coefficient a, for odd-prime M, 1 <= K <= M, N=KM, and fixed input independent of the seeds. Each repetition still needs a fresh independent uniform pair (b,d) over all residues, including d=0. Aggregation is the original ordinary real/imaginary coordinate median with positive odd R.

For nonzero x, write rho=||x||_2^2/||x||_1^2 and Lambda_star=max_{0<=p<K} Lambda_M(p/K) <= 1+H_{M-1}. Under p_star=2 M Lambda_star^2 rho/epsilon^2 < 1/4, the probability of any output error exceeding epsilon||x||_1/sqrt(N) is at most N(4p_star)^(R/2). The harmonic envelope may replace Lambda_star as a sufficient bound. The zero input is exact. The sharper Lambda=1 and M-bin union apply only to alias bins, not all bins.

All R sketches and full decoders, repeat-dependent convolutions, table preparation, and outputs are charged: O(RN log(2K)) exact scalar work, plus O(RN) ordered-real comparisons for linear median selection and 2R independent uniform residue draws. Sorting medians instead costs O(NR log R) comparisons. Retaining all samples costs O(RN) storage plus decoder workspace and input/final output; p-batching uses O(RK+RM+M+K) auxiliary scalar storage, plus input and N final outputs if not streamed.

This is an exact-complex-root concentration theorem. Pure field operations do not supply the ordered-real comparisons needed by the medians. There is no finite-field attribution, bit-complexity, stability, joint multi-seed computation, sub-FFT total runtime, novelty, production-performance, or whole-ALG-031 closure claim. ALG-031 remains open.

## Read in this order

1. PUBLICATION_SCOPE.json gives the exact accepted scope, costs, guards, and exclusions.
2. proof/REPORT.md is the accepted v2 proof, retained byte-for-byte. Its original “candidate” and “review pending” language is frozen author chronology, not current status. The later review below records bounded acceptance.
3. review/INDEPENDENT_DERIVATION.md and review/ACCEPTANCE.json contain the current independent bounded acceptance. Only narrowly documented administrative locator substitutions were made for public packaging; no mathematical or acceptance language was rewritten.
4. proof/sources/ contains the three verbatim, already-public pinned mathematical source bodies. Their public URLs, original hashes, and sizes are in proof/SOURCE_BINDINGS.json. They establish the model and prior results, not completion of any broader or adjacent research item.
5. history/ preserves the superseded v1 proof, historical wording-only HOLD, and exact accepted sentence correction. These are explicitly historical, not competing current acceptance records.
6. lineage/ records original immutable hash pins and the exact administrative projection audit trail. The original workdir manifests are not included: they inventory private provenance, scripts, and diagnostics, whereas MANIFEST.json here binds only the public allowlist.

## Inert and sanitized

This package contains text and JSON only. It contains no scripts, executables, private scope-capture data or locators, user data, runtime logs, or standalone diagnostic results. Historical references to control programs, test artifacts, or workdir inventories in the frozen mathematical sources and proof are provenance statements, not a claim that those omitted artifacts are bundled. The packaged source bodies were not shortened or rewritten to remove their historical mathematical verification discussion.

Packaging checks rehashed the frozen originals, checked the single-sentence v1-to-v2 change, verified the exact allowed locator transformations, and checked ZIP membership and hashes. They did not execute supplied research programs or rerun the omitted finite controls. No external writes or uploads occurred during packaging.

Verify MANIFEST.sha256 against MANIFEST.json, then check every manifest member's bytes and SHA256. The two manifest files are excluded from the manifest's own member list to avoid self-reference. All other ZIP files are listed. ZIP entries are ordinary non-executable files with fixed timestamps; there are no symlinks, absolute paths, parent-directory entries, or executable payloads.
