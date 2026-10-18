# Independent final review of the Fourier-window completion

Reviewed 17 October 2026 UTC. Verdict: the mathematical core passes, with an explicit representation/evaluation clarification required for the additional sequential-cost claim in §7.1. No unrestricted Fourier lower bound or faster Fourier algorithm is established.

## Reviewed source and method

Source directory: `../candidate`.
The exact reviewed PROOF.md has SHA-256 `475a32ecfadd70dabe8e815a793241a213138e620a177d3e8bc00a5d5914ff9c`.
The precise other reviewed hashes are in `independent_results.json`.

Read the submitted proof, README, source ledger, verifier, and result summaries. Read the original R30 PROOF.md and REPORT.md as data from the retained archive. Executed neither original R30 code nor the submitted verifier. Wrote and ran separate exact controls in this review directory. No external service was written to.

## Core findings

1. The declared positive-sign cyclic DFT identity `F_N = B_D ... B_1 P` is correct. The bit-reversed input permutation and every twiddle/sign match radix-two DIT. The proof is a complete transform factorization, not a binary-cube transform substituted for a cyclic DFT.
2. A stage-aligned component means a connected component over an entire nonempty interval of butterfly stages. Its active bits are precisely those stages, with spectators fixed. There are `N/2^k` components for each length-k interval and `D-k+1` such intervals. The stated total `N(D-1)+1` is correct. At N=256 it is 1,793, distinct from the 36 whole-vector intervals.
3. Every row and column of a k-stage component has exactly `2^k` nonzero coefficients. The unique-path argument is sound because each active address bit is visited only once and all edge coefficients are nonzero. Arbitrary nonzero internal diagonal scalings preserve this. Invertible monomial boundary changes preserve row and column support counts.
4. A one-stage butterfly has cross ratio −1. Row/column nonzero scaling preserves it, and row/column swaps invert it. R30 non-diagonal pair blocks have cross ratio `1/rho^2`, hence 1/9 or 9 for rho=±3. Those values cannot equal −1. Diagonal R30 cases fail support. Multi-stage components have at least four nonzeros per row, unlike any single R30 resolvent. The zero-eligible-window conclusion is proved for the declared family, including its allowed boundary changes.
5. Rho=±i is exactly the nonzero nonsingular parameter class that passes the pair cross-ratio test, and both signs are sufficient. The positive identity `B(t)=2 Z R_i diag(1,t)` is correct. Explicitly the negative-sign case can be written `B(t)=2 R_(-i) diag(1,-t)`. The full-transform identity in §5 then follows stage by stage, with scalar `2^D=N`. The positive class has exactly `ND/2` pair components and no longer component windows. It is explicitly outside implemented R30.
6. The specified radix-two counts are correct: ND complex additions and `T_D=ND/2−3N/2+2` general complex multiplications after excluding 1 and i twiddles. Under the stated ordinary complex-multiply implementation, this gives `2ND+2T_D` real additions and `4T_D` real multiplications. At N=256 the numbers 2,048, 642, 5,380, and 2,568 agree. Rho=±i changes none of that charged arithmetic once the reciprocal stage scalars are absorbed; rho=±3 offers zero replacements.
7. The two-sparse product depth inequality is correct: each factor can at most double row support, while the exact DFT is fully dense. It is a statement about a specified matrix-product representation. Cancellations can only reduce support and cannot evade the bound. The stronger statement of 4ND real additions is an evaluator-specific charge and must carry the clarification below.
8. The conjugated ordinary-phase result is also sound. Each selected one-bit factor has two nonzero coefficients because its phase has order at least four. Distinct subsets give distinct XOR routes, so each row has exactly `2^s` nonzeros. Any sum of monomial matrices therefore needs at least `2^s` terms. This does not prohibit faster evaluation in a different representation.

## Required clarification for §7.1

The existing wording is already narrower than a general lower bound, but publication should make the representation and arithmetic assumptions explicit. `ERRATUM.md` supplies an additive paragraph tied to the precise reviewed proof hash. The clarification should travel with the release or be incorporated into PROOF.md before claiming the sequential-cost statement without qualification.

In particular, no premise that all runtime input/intermediate values are numerically nonzero is needed for the support-depth proof. The nonzero conditions concern Fourier matrix entries and boundary scale coefficients. Literal per-factor operation counts concern an evaluator on arbitrary inputs with its prescribed operations charged; sparse/data-dependent shortcuts, alternate joint evaluation, packing, auxiliary dimensions, and representation conversion cannot silently inherit that count. The dyadic R30 implementation also does not acquire a supported exact Fourier-root representation merely from the formal identity.

## Fresh independent exact controls

`independent_controls.py` uses exact arithmetic in `Q[z]/(z^(N/2)+1)` to multiply stage matrices for N=2,4,8,16,32,64. This representation permits general polynomial addition and cancellation; it does not assume coefficients are single root powers when comparing matrices. It compares all 5,460 full-DFT coefficients, examines all 522 stage components and both row/column supports, and checks all 321 one-stage cross ratios. It also checks the R30 conjugacy, both coefficient classes, arbitrary nonzero row/column scalings and swaps, and both ±i butterfly identities using separately written Gaussian-rational arithmetic. All checks pass. These finite checks corroborate the all-D proofs; they do not replace them.

The submitted larger D≤10 counts are internally consistent on inspection, but this review does not claim to have re-executed those tests. The retained ZIP contains byte-identical copies of the corresponding release files. Manifest hashes and sizes were checked separately.

## Attribution and scope

The primary Cooley–Tukey paper link resolves, the author-hosted O'Donnell book presents the standard parity/Fourier basis in Chapter 1, and IBM's SXGate documentation gives exactly the C matrix used here. These are appropriate classical/authoritative attributions; the scoped classification and accounting reconciliation may be presented as this document's work without a historical-priority claim.

- Cooley and Tukey, 1965: https://web.stanford.edu/class/cme324/classics/cooley-tukey.pdf
- O'Donnell, Analysis of Boolean Functions: https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf
- IBM SXGate documentation: https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.circuit.library.SXGate

The overall conclusion remains: zero implemented R30 replacements in the explicitly enumerated radix-two stage-component family, and ordinary unchanged radix-two arithmetic in the ±i algebraic extension. No conclusion about all Fourier factorizations, arbitrary non-stage-aligned subgraphs, or general FFT complexity follows.
