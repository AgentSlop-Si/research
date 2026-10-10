# Growing-rank corollary for the exact common-chirp recognizer

9 October 2026. This is a direct, independently checked consequence of the approved explicit ledger in `additions/1906_chirp/eliminant_extension/ELIMINANT_EXTENSION.md`, Sections 4–6. It is separate from the sealed source/audit supplements. No publication-priority claim is made.

## Model and conclusion

Let r=r(N)>=1 and N>=3r. Work over a supplied prime field F_p with N dividing p-1 and a supplied certified primitive Nth root omega. Retain the exact input, equality-test, indexing, field-arithmetic and scalar-inversion contracts of the approved recognizer. The recognized family consists of at most r distinct linear characters sharing one quadratic chirp:

`x[j]=omega^(a*j^2) sum_(ell=1)^s c_ell omega^(b_ell*j)`, with 0<=s<=r.

The zero vector is the empty representation. Full-input verification remains mandatory; rejection means nonmembership in this family.

Using the polynomial Toeplitz eliminant and the ordinary Horner phase scan, recognition on every raw vector and the full-output transform on accepted vectors use

`O(N r^4 + r^(2+3 log2(3)))`

field additions/multiplications, plus the separately counted inversions described below, and

`O(N+r^4)`

field-element storage. In particular, for any integer rank schedule

`r=o((log N)^(1/4))`,

these arithmetic costs are `o(N log N)`, still only for recognition and accepted structured inputs. The family may now grow slowly with N; it does not cover arbitrary input vectors.

## Explicit derivation

Put D=binom(r+2,3)=O(r^3), L=N/gcd(2,N)<=N and C=min(D,L)<=D. The existing complete uniform ledger is

`O(T(r)+S(N,r)+C(Nr+r^3)+N)`.

The faster Toeplitz route gives

`T(r)=O(r^2(D+1)^log2(3))=O(r^(2+3 log2(3)))`.

Choose the already allowed Horner option rather than the optional convolution scan:

`S(N,r)<=O(L(D+1))=O(Nr^3)`.

Candidate dechirping, bounded recurrence, admissible-root scanning, amplitude recovery and exhaustive verification satisfy

`C(Nr+r^3)=O(Nr^4+r^6)`.

Because r>=1 and 2+3 log2(3)>6, the N, Nr^3 and r^6 terms are absorbed in `Nr^4+r^(2+3 log2(3))`. The approved Toeplitz storage is O(N+r(D+1))=O(N+r^4). Candidates are processed sequentially; no candidate-by-input table is assumed free.

If r=o((log N)^(1/4)), then r^4=o(log N), so Nr^4=o(N log N). The setup term is at most polylogarithmic, specifically `o((log N)^((2+3 log2(3))/4))`, and therefore also o(N log N). The requirement N>=3r holds eventually along such a schedule. This establishes the displayed asymptotic corollary without treating the fixed-r big-O constant as uniform by assumption.

## Inversions and remaining charges

The Toeplitz construction uses one cached scalar field inverse. Per candidate, bounded Berlekamp–Massey has at most r order-increasing updates and caches its baseline inverse; the amplitude solve needs at most r further pivots. Thus a conservative bound is O(1+Cr)=O(1+r^4) scalar field inversions, in addition to the stated integer modular inverse/gcd work in the accepted Gauss evaluation. This is not one inverse per input sample. All original field/root preparation assumptions, exact indices and output writes remain explicit.

If p=N^O(1) and an applicable word-arithmetic model charges O(log N) per scalar inverse, that extra bound is O(r^4 log N), also below N log N in this rank regime. Modular multiplication/reduction costs, integer bit costs, prime/root discovery and exact input encoding are still model obligations; no unconditional bit-complexity or numerical-stability theorem follows. In particular, the result does not convert exact equality-based recognition into a robust floating-point recognizer.

## What this does not establish

- Rejected vectors are not transformed by the recognizer. Combining it with an independently available exact O(N log N) backend in the same field/model yields an adaptive structured fast path whose arbitrary-input worst case remains that backend bound. Existence/setup of such a backend for the chosen field and lengths is not silently supplied by this corollary.
- The method does not establish an unrestricted exact sub-N-log-N transform or a new integer-multiplication bound.
- The proof is an arithmetic upper-bound consequence of the approved construction; it is not an optimized implementation benchmark, an input-coverage theorem, or a novelty verdict.

The delivered private theorem note is linked in `DELIVERED_THEOREM_NOTES.json`. This separately derived growing-rank corollary need not already appear on that previously delivered page.
