# Independent review of the Phase 22 Jordan-jet construction

10 October 2026. Scope: the uploaded Phase 22 proof and research notes, read without executing or importing any uploaded program.

## Verdict

The displayed full and interval spectral recurrences are correct. The stated bounded-order, grid-frequency raw-input recognition and exact transform bound O(N R^2 + R^3) hold in the supplied-root field-arithmetic model under the stated characteristic and 2R <= N conditions. For fixed structural order this is linear work on the specified family. It supplies no universal exact linear-time DFT, numerical-stability guarantee, bit-complexity result, or verified historical priority.

The piecewise implementation claim is an accepted-input guarantee. The described greedy method may reject genuinely structured signals with short interior segments. Do not promote it to a complete recognizer for all piecewise inputs without an additional argument or algorithm.

## Proof checks

Put eta of order 2N, N odd, q=eta^8, and h_t=eta^(2t^2)/product_{j=1}^t(1-q^j). All denominators are nonzero. The coefficient ratio (1-q^t)h_t=eta^(4t-2)h_(t-1) directly gives the polynomial identity. Applying the Euler operator (z d/dz)^j uses the binomial expansion of (D+1)^j; the terminal monomial contributes N^j. Interval truncation adds the two displayed endpoint monomials with their exact signs.

The map k -> k+4 modulo 2N has two length-N cycles. On each cycle two direct seeds determine the remaining N-2 values by the second-order recurrence. Computing degrees in increasing order makes every lower-degree term available. Charging all seeds, binomial coefficients, root powers, coefficients and final output gives O(N(d+1)^2) field arithmetic and O(N(d+1)) memory. Selecting even output indices requires only parity orbits actually touched by mode shifts; it must not be compared with a 2N-output transform as if these were identical tasks.

The exponential-generating-function restatement divides by j!, so in positive characteristic it additionally requires d < char(K). This is automatic in the recognition regime d < R <= N/2, but is not an unconditional restatement for arbitrary jet degree. The binomial-coefficient recurrence itself does not divide by j!.

For normalized b_t=sum_i P_i(t)u_i^t, distinct nonzero grid roots and nonzero leading coefficients give a nonsingular leading R by R Hankel matrix. Indeed H=V M V^T, where V has columns t^j u_i^t, and each block of M is anti-triangular with nonzero antidiagonal binomial coefficients times the leading coefficient of P_i. The characteristic assumption protects these factors. Standard minimal-recurrence recovery from 2R samples therefore applies. A charged scan of all 2N grid roots identifies the factors and multiplicities; a confluent Vandermonde solve recovers amplitudes. Full input verification prevents prefix spoofing. Frequency shifts of the precomputed jets then supply every output.

For pieces, every accepted segment is verified and the segments partition the input. Endpoints and a bounded literal tail can be charged explicitly. A false structural guess cannot silently produce an accepted wrong transform when these checks are performed.

A concrete incomplete-recognition case is N=7 over F29, eta=4, Rmax=1, with normalized data b=(1,2,2,2,2,2,2). It has two constant pieces. The first two-sample order-one fit, however, requires ratio 2, which is outside the allowed 14th-root grid because 2^14=-1 modulo 29. The described greedy procedure therefore rejects before recovering that valid segmentation. This does not compromise correctness on accepted inputs.

## One representability qualification

The single-segment finite-field union bound min(1, binom(2N+R,R) p^(R-N)) is sound. The subsequent bare assertion that a finite union of subspaces of dimension below N is automatically proper needs qualification: that inference holds over an infinite field, but dimension alone is insufficient over a finite field.

A valid finite-field piecewise bound, with no optional tail, is

    min(1, sum_{j=1}^s binom(N-1,j-1) binom(2N+R,R)^j p^(j R-N)).

It counts partitions into j nonempty intervals, root-multiplicity choices per interval, and at most p^(jR) coefficient vectors. Degenerate descriptions only overcount. It establishes vanishing density for fixed s,R as N grows with p >= 2N+1. A literal tail of bounded length must have its length, placement and free coefficient count included separately. No complexity lower bound follows from this counting argument.

## Fresh exact controls

The accompanying independently written verify_jets.py uses only Python's standard library. It verifies 1,248 full-jet entries, 4,992 interval-jet entries, 1,512 reconstructed N-point bins, 120 confluent-Hankel rank cases, and ten dense-defect examples over ten different odd lengths and compatible prime fields. Endpoint cases include a singleton at either end. All checks pass. These controls corroborate the algebra, not the full submitted implementation or its operation counter.

## Benchmark and scope ledger

The source reports ordinary N-point counts 295,345 versus 181,578 at N=6,561; 2,657,323 versus 2,027,424 at N=59,049; and 7,971,747 versus 6,672,626 at N=177,147. Thus its ordinary N-point comparator wins in all three displayed cases. These values are source-reported; this review has not rerun the source executable or independently reproduced its operation ledger.

The reported crossover at N=59,049 is for the separate 2N-output zero-padded task. It cannot serve as an ordinary N-point speedup. Large nonsmooth lengths may use a quadratic demonstration fallback; no all-length fast fallback follows from the code description. Root discovery, finite-field certification, bit costs and floating-point conditioning are outside this theorem's model.

## Precedent and status

q-holonomic recurrences and generalized Prony/confluent-Hankel methods are established ingredients. Source-linked primary references include Garoufalidis and Koutschan, Twisting q-holonomic sequences by complex roots of unity (2012), https://arxiv.org/abs/1201.3353, and Bostan and Yurkevich, Fast Computation of the N-th Term of a q-Holonomic Sequence and Applications (2020), https://arxiv.org/abs/2012.08656. Their abstracts were checked; this bounded review does not claim a complete full-text priority comparison or equivalence to their algorithms.

Peter and Plonka, A Generalized Prony Method for Reconstruction of Sparse Sums of Eigenfunctions of Linear Operators (author manuscript dated 10 January 2013), explicitly treats generalized eigenfunctions and polynomial-times-exponential sums. The introduction and its stated Section 3 scope were inspected: https://num.math.uni-goettingen.de/plonka/pdfs/Operator_Prony_revised2.pdf. This is a direct predecessor for the recognition ingredient, not a claimed equivalent of the particular q-Gaussian Fourier jet evaluator.

The exact Fourier comparison must also remain current: the OpenAI Math 130 scope page, checked 10 October 2026, describes a uniform exact-complex unrestricted-coefficient O(n (log n)^(1-10^-13)) result with a supplied root, including scalar preparation. That external claim is a different model from finite-word approximate FFT tabulation and from this restricted-input theorem. This review does not independently audit that formalization. Source: https://github.com/openai/math/blob/main/lean/docs/130.md.

Status: mathematical scoped review complete and the [independent second review](05_jordan_second_review.md) passes with the stated qualifications. This public export is separately reviewed; its external export receipt does not enlarge the mathematical scope. The original source remains unmodified.
