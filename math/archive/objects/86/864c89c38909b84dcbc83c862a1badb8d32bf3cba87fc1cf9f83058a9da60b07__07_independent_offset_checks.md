# Full static source review: independent_offset_checks.py

- Source: additions/1910/audit/independent_offset_checks.py
- SHA-256: 8b5d011f6a270d7fc2666417e8f912ad2b570d3e49a5ab86d5e586b7d7660af4
- Bytes: 6504; lines: 159
- Read interval: 1–159 (complete)
- Supplied source execution/import/compile/parse: none
- New exact-hash full-read coverage: yes

## Full-source scope
Read lines 1–159: exact grid/classes, Fraction rank/Chebyshev/Ramanujan/covariance routines, dense complex operators, every main-loop check, result writing and CLI.

## Exact and numerical correctness
- grid uses integer floor(kq/n+1/2), fixing half ties upward, and returns numerator kq−nj. constructive_classes checks q>=n>=1 and uses period L=n/gcd(n,q); classes are r modulo L. Across all classes exactly n indices are generated, so this replacement needs no sorting-based uniqueness operation.
- exact_rank is ordinary rational elimination; chev correctly generates degrees 0 through R−1 for positive R. Distinct post-cut residuals give the corresponding nonsingular Chebyshev/Vandermonde matrix.
- unit_average evaluates the normalized Ramanujan sum mu(h)/phi(h), h=q/gcd(q,c), and detects square factors before returning zero. exact_covariance sums these rational values over equal within-block displacement sets. All saved covariance cases satisfy the stated legal prime-power/block regime m^2<=q.
- Fraction verification of C^2=(m/q)C plus trace gives exact rank because the rational matrix obeys a polynomial with distinct roots 0,m/q. int(trace/(m/q)) would truncate outside that invariant, but here the trace is exactly q−q/m times m/q. The saved ranks match q−q/m.
- projected_operator builds block outer(conj(s),s). Its unnormalized blocks have eigenvalue m and represent the randomized sketch; despite the informal word “projection,” it is m times an orthogonal rank-one projector, as required for mean identity. The unitary DFT sign, sqrt(q/n) lift and entrywise residual modulation are consistent with (j+num/n)/q=k/n.
- Numerical loops enumerate every unit a and beta for five small cases, not random sampled states. They verify the mean transform, row covariance largest eigenvalue and modulation identity. Conjugated row outer products correctly represent input quadratic-form covariance. These are floating complex checks with tolerances, not exact algebraic certificates.

## Guards and scope
Most helpers assume positive rectangular dimensions; grid does not validate n,q; chev(R=0) returns one entry and matrix_product expects a nonempty second matrix. projected_operator silently leaves a remainder block zero when m does not divide q, and it does not enforce m^2<=q or the prime-power regime. None of these invalid cases is used by main, so they do not invalidate its saved results. Assertions vanish under -O, potentially leading to unsupported PASS output. NumPy/FFT pipeline production precision, original all-length dispatcher edge cases and original code execution are outside this helper's checks. The field execution_scope string is a historical source declaration, not this review's execution statement.

## Costs
constructive_classes is O(n+L) exact index work with O(n+L) returned storage (integer bit costs separate). Exact covariance stores q^2 Fractions and builds roughly O(q^2*m) terms plus factorization; multiplying it is cubic q^3 rational work. Dense all-state numerical testing uses q*phi(q) states and dense q^3 products, n^3 covariance accumulation and eigensolves. It does not implement the proposed linear-work production estimator, and its runtime is not evidence of that complexity.

## Evidence and disposition
Saved results report 3,230 exact grid cases, eight rational projector identities, three corrected post-cut ranks (8,10,12) and five all-state numerical cases totaling 1,200 states. The source/result/log hashes match the 11-entry package seal, and result/log bytes are identical. The ties-to-even example n=6,q=9 genuinely has residual classes −1/2,0,+1/2; the half-up helper avoids it. No stored-result error was established. Accept scoped exact finite certificates and clearly labeled numerical evidence, preserving the report's broader original-prototype caveats rather than converting them into new defects in this checker.
