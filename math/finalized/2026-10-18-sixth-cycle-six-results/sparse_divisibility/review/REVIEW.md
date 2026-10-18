# Independent review: connected Fourier-mask obstruction

Date: 2026-10-18 (UTC).

## Verdict

**ACCEPT as an exact obstruction to the full-block structural premise only.**

The reviewed report is
`/workspace/shared/sparse_uniform_divisibility_20261018_2054/REPORT.md`,
SHA-256 `93be9a7c2c62b7a8c9ba6ff0cfce160b3c0469b03d0373f53fbcbad9e86f5cde`.

Its explicit binary mask at `(N,d)=(8,4)` retains the original Fourier phases,
has both unnormalized Grams equal to `4 I_8`, and has connected bipartite
support. Consequently it cannot be transformed by independent row and column
permutations into a direct sum of full `4 by 4` blocks. The same obstruction
holds at `(N,d)=(8m,4m)` for every odd positive integer `m`.

**The selected uniform necessity conjecture `d | N` remains unresolved.**
All accepted examples here satisfy divisibility. No nondivisor example, uniform
necessity proof, replacement classification, improved optimum, or quantitative
gap is accepted or implied. Retain owner **M-SPARSE-DEFECT**, status
**TO RESEARCH**, priority **42**. Do not close the selected uniform gate.

## 1. Independent mathematical assessment

### Base Gram and support obstruction

The four column supports printed in the report are correctly transcribed.
Repeated supports have two even and two odd row indices, which cancel for
column differences four. The four nonempty intersections between distinct
support classes contain exactly two rows. In each case their row difference
times the corresponding column difference is four modulo eight. Thus the two
retained roots are negatives, and every off-diagonal column Gram entry is zero.
The other two class pairs have disjoint supports. The diagonal entries are four.

The support-class intersection graph is the connected cycle
`0--1--3--2--0`. Every row appears, and every class contains two genuine column
vertices. Hence the whole bipartite graph has one component on 16 vertices.
A direct sum of full `4 by 4` blocks would have two components on eight vertices
each. Row and column permutations preserve these components. Equivalently,
columns zero and one have distinct overlapping supports, which cannot occur
in such a block sum.

### Infinite odd-parameter family

For odd `m>1`, put `u=m^(-1) mod 8` and `v=8^(-1) mod m`. CRT gives

`rc = m u (r mod 8)(c mod 8) + 8 v (r mod m)(c mod m) mod 8m`.

This follows directly by reducing each side modulo eight and modulo `m`.
With the report's literal mask

`R_N[r,c] = R_8[u(r mod 8) mod 8, c mod 8]`,

the retained Fourier matrix, indexed by CRT, has entries

`D_8[u a mod 8,e] H_m[v b mod m,f]`.

Both row multipliers are units. After these row permutations the matrix is
exactly `D_8 tensor H_m`; there is no arbitrary-phase substitution. Thus both
Grams are `(4 I_8) tensor (m I_m) = 4m I_(8m)`. Each row and column has `4m`
nonzeros. Its support replaces each base vertex by `m` twins with complete
bipartite connections for every base edge, so connectivity is preserved.
There are `16m` vertices and a full-block decomposition would require two
components. The case `m=1` is the base construction.

This proves the claim for every odd `m`. The finite direct checks below are
transcription and arithmetic controls, not the justification for the quantifier.

### Original optimization witness

For the literal unnormalized Fourier matrix `H` and retained matrix `D`, set
`A_0=H-D`, `B_tilde=A_0*/4`, and `M_tilde=B_tilde^(-1)`. Independent exact
arithmetic verifies both inverse products, exactly four nonzeros in every
row and column of `B_tilde`, and both error Grams

`(M_tilde-H)(M_tilde-H)* = (M_tilde-H)*(M_tilde-H) = 4 I_8`.

Since `M=M_tilde/sqrt(8)` and `F_8=H/sqrt(8)`, the original inverse is
`sqrt(8) B_tilde` and the squared spectral error is exactly `4/8=1/2`.
The simultaneous inverse-row budget is therefore satisfied. The construction
uses the accepted equality criterion correctly; it does not replace the actual
minimizer by the retained Fourier mask. The family conclusion follows from
the same criterion at `d/N=1/2`.

## 2. Execution and exact evidence

Only the new reviewed packet's checker and the new independent checker were
executed. No historical checker or search program was executed. No external
service, repository, spreadsheet, or index was modified. The source packet was
left unchanged; replay outputs were written in this separate review directory.

The complete 5,811-byte sibling checker was inspected before execution. It uses
only standard-library rational arithmetic and local output writes. A copy was
run from `replay/`, exited successfully, and produced `RESULTS.json` and
`GRAM_CERTIFICATE.json` byte-identical to the source files.

The independently written `independent_verify.py` imports no packet code. Its
base field is `Q(sqrt(2))[i]`, represented as four rational coordinates, rather
than the packet's quotient representation `Q[z]/(z^4+1)`. It builds the literal
mask from separate row strings and inverts `B_tilde` directly. It verifies:

- All 128 entries across both base Gram orders.
- Both inverse products and every inverse-row and inverse-column support count.
- Both full error Grams and the exact normalized error `1/2`.
- A different degree-preserving support-switch negative control, which fails
  the Gram condition despite retaining all support counts.
- All 65,408 entries across both Gram orders for `m=1,3,5,7,9,11,15`, directly
  from original-index Fourier exponent histograms reduced modulo independently
  constructed cyclotomic polynomials.
- All degrees and connected support for those seven family cases, plus every
  CRT pairing congruence for the nontrivial cases.
- Every size and SHA-256 in the 18-entry source manifest; all four copied source
  bindings; and those same hashes against the four original source files.

The checker finished with `PASS` and empty stderr. Its complete rational
minimizer, inverse, and error matrices are retained in `INDEPENDENT_WITNESS.json`.
Machine-readable results are in `INDEPENDENT_RESULTS.json`.

## 3. Nonblocking certificate convention

The sibling checker's auxiliary row-histogram loop uses exponent `k(j-i)`;
the direct `(DD*)[i,j]` exponent is `k(i-j)`. Thus this auxiliary row certificate
records the conjugates of the direct row-Gram entries. Since all required
entries are the real numbers zero or four, this verifies exactly the same
identity and is not a mathematical defect. The sibling's separate matrix
multiplication already checks `DD*` directly. The independent checker uses the
direct row-Gram exponent. No substantive report correction is required.

## 4. Search and publication boundary

The two retained `(12,5)` records both say that a time limit was reached, at
roughly 60 and 180 seconds. They do not establish existence or nonexistence.
The other solver-reported infeasibilities have no retained exact unsatisfiability
certificate and are not accepted as mathematical exclusion results. No MILP
search was rerun for this review.

The accepted weight-three classification is unaffected. What fails here is
the proposed extension of its full-square-block conclusion to all degrees.
No claim about worldwide novelty, complexity, an arbitrary-phase model, or
all possible structural reduction methods is added by this review.

## 5. Reproduction and seal

Run `python independent_verify.py` from this directory to redo the independent
checks. It requires the unchanged source packet and its bound original source
reports. The isolated replay artifacts are retained in `replay/`.

`VERDICT.json` gives the narrow acceptance disposition. `SOURCE_SNAPSHOT.json`
binds the reviewed source bytes, including its manifest. `MANIFEST.json` binds
all files in this review packet other than itself and the final seal. Source and review manifests
are rechecked after sealing; their hashes are recorded in `SEAL.sha256`.
