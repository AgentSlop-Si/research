# CROSS-TABLE review: STR-Q3 balanced non-Fourier tensors

Decision: ACCEPT, with the exact scope below. No mathematical repair is required for the pinned candidate.

Reviewed on 11 October 2026. Candidate Library file libfile_58ee12185a688191ae62e3da82c98b1e, version 0. Candidate ZIP SHA-256: bb54486fffa5e47d01ca29054c8a834fc1075196c570e77a87df5f97e4d2f83e. Candidate theorem SHA-256: 6b00ba850f5e3bf44a3e676b8dae3cc205a6e4d44f8bc7a2957cb902c1d3d1cf.

## Accepted scope

- The dense rational orthogonal family U_(2^d) = ([[3,-4],[4,3]]/5)^{tensor d} is not diagonally/permutation equivalent to a finite-abelian Fourier character matrix.
- Integer-only paid envelope construction yields Kappa=1, K=2, G=2, with at most four scaled numerical templates, including the residual and final rational scalar.
- In the declared finite-word RAM, for bounded-word complex dyadic input, t=O(d), and the exact sufficient table budget 2+m*2(p+2)<=d/2, the complete cold computation has the stated relative l2 error and word-work/storage bounds.
- Fixed t admits O(N log N/log log N) word work with explicit full-vector output. With no legal block parameter, the paid direct fallback is O(N log N).
- Polynomial accuracy t>=ad prohibits growing m only under this exact budget; it is not a transform or algorithm lower bound.

The claim ledger entries NF-T1, NF-T2, NF-T3, NF-T4, and NF-O1 are accepted only in this scope. The attached standalone proof includes explicit local and global nonlinear error estimates, integer rounding, range and bit-length implementation, routing, table enumeration, and parameter selection.

## Source and model audit

All 19 candidate-manifest members match their pinned byte lengths and SHA-256 hashes. The sealed ZIP has valid CRCs and the same member hashes. The six exact source copies match their original local source bytes, including the original H01 and P05 proofs and the acceptance ledger. A fresh materialization of the pinned candidate Library version matches the stated ZIP hash.

H01 T1 requires separate bounds on prefix norm and inverse norm, O(log N)-bit dyadic input descriptions, polynomial input dynamic range, polylogarithmic layer count, log(1/epsilon)=O(log N), charged certified coefficients, paid routing, nonlinear local stability, and full dyadic output. P05 S1 additionally requires paid scale certificates and counts distinct scaled numerical templates. Every one of these requirements is met; no condition-number-only or free-normalization substitution occurs.

No exact-field, ideal-real, or complex-scalar operation count is transferred into this word bound. The only exact rational operations used for tables have O(d)-bit operands and are charged constant-word arithmetic under the expressly assumed model. Large exponent gaps are handled by comparison before shifting. Output exponent magnitude may reach O(d^2), with O(log d)-bit encoding. This is a mantissa/exponent output contract, not an unmentioned fixed exponent-range promise.

The proof source snapshot pins H01 to 4afd27bacea1bd896d8b44e7e4c1eb51c1b24b3db997ceca9e554e69f81202bb and P05 to 02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787. R01 accepts the paid local-template compiler; R19 accepts paid balancing for 0<epsilon<=1. Their remaining production/eager-table obligations are preserved.

## Independent finite controls

All supplied research programs, including the author's fresh-controls program, were read only as inert text. The executed test program in this review was newly authored. It uses direct bit-product matrix coefficients and integer dot-product quotient rounding rather than importing the author's Fraction-valued table implementation. Exact reference arithmetic is used solely for falsification and regression; it is not a production word-RAM benchmark.

Reproduced exactly:

- 8,072 shape cases and 447,105 prefix/carry checks
- All 504 rounded output cases, including every recorded relative squared error and maximum local-budget fraction
- 168 unrounded macro/dense equality cases and 27,684 complex output coordinates
- All 52,182 local relative-error checks
- 1,280 high-precision legal-key checks
- All three advertised negative controls

New targeted controls passed:

- 240 rounded circuit cases and 42,912 local-error checks, with exact cancellation, pure imaginary data, extreme positive/negative dyadic exponents, residual blocks, and t up to 4d
- 2,049 signed half-integer tie checks
- 1,360 completely enumerated padded scalar-table keys at deliberately coarse diagnostic precisions
- 42 bounded-shift normalization checks, including exponent gaps of one billion without constructing such a shift
- 40 polynomial-accuracy parameter-grid checks

The four-template upper bound is attained at d=5,k=2. The first legal budget at epsilon=1 occurs at d=180: k=1,m=2,L=181,p=20,b=44,E=90. Thus even the first two-coordinate certificate has a 2^90 table-size upper budget. This is not evidence of practical speedup or even reduced work at that threshold. The reference tests evaluate requested entries on demand; they do not populate full theorem-precision tables at admissible astronomical N.

The three negative controls have the intended effects. Omitting final normalization at d=2 leaves relative error 9/16. Ignoring the full-block floor carry at d=4,k=1 doubles the final answer, giving relative error 1. Forcing k=1 at d=64,t=0 violates the table budget. None is silently treated as an admissible successful fast run.

## Boundaries retained

No claim is accepted about arbitrary dense input matrices, raw matrix recognition, arbitrary rotations or coefficient alphabets, scalar-arithmetic FFT improvements, practical speed, production constant-word validation, or full eager-table empirical validation. Classical tensor products and their separable factorization are not credited as new. No worldwide novelty or publication-priority conclusion follows from this instantiation.

The primary author-hosted Van Loan lecture was freshly opened and its stated Kronecker identities verified. The publisher page for the 2000 paper could not be opened in this review; the report relies on the accessible lecture only for classical background and on its own proof for the theorem.

No Sheet or GitHub changes were made. This report and its accompanying evidence are a separate review artifact; the candidate bytes remain unchanged.
