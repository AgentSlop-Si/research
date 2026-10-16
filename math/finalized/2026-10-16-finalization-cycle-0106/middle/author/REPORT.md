# ALG-018 and ALG-019: exact Prony and recurrence interface comparisons

Prepared 16 October 2026 UTC. Candidate for independent review. No external writes, historical program execution, installations or solver runs.

## Decision and source binding

The still-open named Prony/rational-series/sparse-interpolation comparison gates can be completed at the scope below, subject to independent acceptance. Both parent records remain **TO RESEARCH, priority 34**. The accepted restricted-tail identities and growing-filter recursion are preserved. This report does not complete their outstanding faster/full-operator constructions, numerical implementations or historical priority.

Baseline: AgentSlop-Si/research commit `73528f9e7495b0614106dfc4cc5b5c42907daaf5`. The current index has 70 closed and 257 open records. Fresh native reads cover the complete owning rows: ALG-018 in Catalogue 129, novelity breakthough 121, Research overview 190; ALG-019 in Catalogue 130, novelity breakthough 122, Research overview 191. All six views retain the named comparison as unfinished. The earlier algorithm inventory separately records `NEW_COMPARATOR_OR_CHANGED_MODEL_SCOPE_NOT_SELECTED` for both, and explicitly distinguishes their completed same-target/recursion comparisons from a yet-unselected precise primary-theorem mapping. The present report supplies that mapping; it does not count the older comparison again.

Workbook: https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit

All seven assigned mathematical bodies/reviews were read in full, along with the complete ALG-018/019 entries in the REVIEW-16 outcome ledger (whole-file SHA-256 `46f76abe46263e0a4ef6a62eb4d017a33cc875b49f850fa073ee6ae0b5baf313`) and the full owner histories. `SOURCE_BINDINGS.json` supplies exact immutable repository URLs, sizes and SHA-256 values. Core sources:

- ALG-018 fused-tail source: [e7c06a4… README](https://github.com/AgentSlop-Si/research/blob/73528f9e7495b0614106dfc4cc5b5c42907daaf5/math/archive/objects/e7/e7c06a4bc237a97c74aefc854ad6b7d22d44f7c7f858ec82789780935e857c35__e7c06a4bc237a97c__README.md), 5,623 bytes, SHA-256 `e7c06a4bc237a97c74aefc854ad6b7d22d44f7c7f858ec82789780935e857c35`.
- ALG-018 standalone block-tail source: [7bb840… README export](https://github.com/AgentSlop-Si/research/blob/73528f9e7495b0614106dfc4cc5b5c42907daaf5/math/archive/objects/7b/7bb8400c402dc65c0f741d0820bcc3ca3829261c853e8f2ac7a629fdd1463c60__7bb8400c402dc65c0f741d0820bcc3ca3829261c853e8f2ac7a629fdd1463c60__README.md). Original identity `7bb8400c402dc65c0f741d0820bcc3ca3829261c853e8f2ac7a629fdd1463c60`, 11,186 bytes, is distinct from the retrieved sanitized export, 11,154 bytes, SHA-256 `433f08d898ea3c403ff4da71e33e9e836f156584c64781dc3b81fca589f7eee1`. This is the already documented export difference, not newly recovered original bytes.
- ALG-019 grading source: [239adb… README](https://github.com/AgentSlop-Si/research/blob/73528f9e7495b0614106dfc4cc5b5c42907daaf5/math/archive/objects/23/239adb59c756af0317788283e19feb83d3293801546749b9b22447eccaee2b05__239adb59c756af0317788283e19feb83d3293801546749b9b22447eccaee2b05__README.md), 4,779 bytes, SHA-256 `239adb59c756af0317788283e19feb83d3293801546749b9b22447eccaee2b05`.
- ALG-019 complete decimation source: [e84fd2… README](https://github.com/AgentSlop-Si/research/blob/73528f9e7495b0614106dfc4cc5b5c42907daaf5/math/archive/objects/e8/e84fd241ddf5f362c09cb41cec13483b6f67c40703acfe6bec5f13e5e1ce6d46__e84fd241ddf5f362c09cb41cec13483b6f67c40703acfe6bec5f13e5e1ce6d46__README.md), 9,549 bytes, SHA-256 `e84fd241ddf5f362c09cb41cec13483b6f67c40703acfe6bec5f13e5e1ce6d46`.

The three accompanying review hashes are `8c14a657058b76788e5176acdc89b20d2dbb46dbe872a8d1f446cddf717a1916`, `8c3b40fa499aacd02699c93e7b07d4f6370b38593d716e8efc76ddd3da8ff047`, and `f9de1b8b0cb4009625285d2d6b1a81cf920deaede0b81f73eb963846f8ecff7c`. Their reported execution is historical attributed evidence, not a rerun here.

## Named primary sources and exact scope

Massey, *Shift-Register Synthesis and BCH Decoding* (1969), §II equation (2), §III Theorem 3/corollary and §IV Theorem 4/corollary, printed pp.122,124–126, distinguishes a recurrence fitted to a finite prefix from the infinite rational generating series. For a reduced rational series A(z)/B(z), B(0)=1, the minimal register length is max(deg B,1+deg A). It allows finite and infinite fields. These are scalar-sequence statements; application to a vector sequence below is proved directly through linear dependence, rather than attributed as Massey's vector theorem. [Primary paper](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf).

Van der Hoeven–Lecerf, *Sparse polynomial interpolation: Faster strategies over finite fields* (2024), §5 Algorithm 4 and equation (10), printed pp.13–14, takes an unknown black-box polynomial with degree/sparsity bounds. It selects an element of order at least max(D,2T), samples 2T geometric values, computes a Padé denominator, finds roots, recovers discrete logarithms and solves for coefficients. Steps 3 and 6 cost O(M_K(T) log T); black-box evaluation, root finding, discrete logarithms and any field extension are additional work. The stronger finite-field estimates require their stated hypotheses. [Primary paper](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf).

For the already credited convolution mechanism, van der Hoeven's *Newton's method and FFT trading*, §2.4, describes selected product coefficients through middle products and their transposed multiplication form; its introduction and §6 discuss shared transforms and smaller FFT blocks. The owner's existing block-tail comparison already credits this mechanism. This report does not claim it as a newly completed result. The paper's differential/Newton complexity assumptions are not imported as finite-field guarantees. [Primary author text](https://www.texmacs.org/joris/fnewton/fnewton_bis.html).

The FFTW authors' pruned-FFT note gives O(N log K) for selected outputs or sparse input, including the first-K-output construction for K dividing N. That is an arithmetic comparison, not an automatic native-speed claim. It does not identify an arbitrary q-kernel projection with selected Fourier coefficients. [Official source](https://fftw.org/pruned.html).

## 1. ALG-018: known sparse polynomial, arbitrary fresh vector

### Declared owner target

Select the existing standalone block-tail target L=C^(N-r)p(C), deg p<r, with dyadic N>=2, dyadic 1<=r<=N/2, supplied primitive Nth root q and N nonzero in the exact field. Keep the finite corner in C=TBT^-1, T=H_q(A). Since the upper-shift weights of B are all nonzero, its minimal polynomial, and therefore C's, is z^N.

This is distinct from the owner's other accepted map f(C)T, where f occupies the top r degrees. That map reads only r raw coordinates and costs O(Nr); the standalone map L generally reads the entire fresh vector in its projected inverse convolution. Neither statement supplies the full invertible H_q(C).

### Exact scalar interpolation map

Define the supplied polynomial f(z)=z^(N-r)p(z). Let S={k:0<=k<r,p_k!=0}, t=|S|. Its geometric samples are exactly

    a_j=f(q^j)=sum_(k in S) p_k (q^(N-r+k))^j.

All t nodes are distinct and nonzero because exponents lie in [0,N-1]. Thus

    sum_(j>=0) a_j u^j = sum_(k in S) p_k/(1-q^(N-r+k)u).

Distinct nodes and nonzero residues mean its reduced denominator is the product of these t linear factors, and its numerator has degree<t. Massey's scalar formulation therefore gives register length t (zero polynomial gives zero). Algorithm 4's order condition is met by omega=q, D=N, T=r since 2r<=N. This is an exact hypothesis/formula match for recovering this polynomial from scalar evaluations, if its coefficients were unknown.

In the actual owner API those coefficients and their high-degree positions are already supplied. Recovering them again does not apply f(C) to an arbitrary fresh vector. The N-root scalar evaluations are values of a polynomial at nonzero scalars, while C is nilpotent and is not diagonalized by those scalar nodes. Replacing f(C) with a diagonal scalar-sample action requires an additional proved and paid transform; none is supplied by sparse interpolation.

The mismatch can be checked without asymptotics. For r>1, f_1(z)=z^(N-r) and f_2(z)=z^(N-1) each have one nonzero monomial and one Prony mode in a_j, but rank(f_1(C))=r and rank(f_2(C))=1. Monomial count, scalar moment recurrence length and operator rank are distinct parameters. More generally, if p has valuation v, rank(L)=r-v; for p=0 it is zero. A small description is not an uncharged application circuit.

### All-coordinate certification and cost map

The retained exact operator factorization is

    L=T G^-1 (A^T)^(N-r) p(A^T) G T^-1.

It projects the last r coordinates of T^-1 x, applies the r-dimensional upper Toeplitz p action with the two G scalings, then decodes through the first r columns of T. The projection and all N outputs remain paid. For polynomials f,g of degree<N, f(C)=g(C) holds exactly when f=g, by minpoly(C)=z^N. Agreement on arbitrary short scalar samples without a valid sparsity/degree promise does not establish this identity, and agreement on a single vector is not an all-input operator certificate. The owner already supplies an all-coordinate algebraic identity and historical full-basis audits; this comparison is no new execution acceptance.

Let s=log2(2r), b=N/r, P=(2N+r)s and V=(2N+4r)s. Retained cold counts are 8N+log2(N)-5+P multiplications, log2(N)-s+P additions, 2N-2+P subtractions, N-1 negations and one constant inversion. Online counts are V+6N+8r multiplications, V+2N-2r additions and V subtractions. Length-2r roots come from q; all normalizations, padding, projection sums and N writes are charged. Storage is O(N); both cold and online field/index work are O(N log(r+1)). Root discovery, finite-bit costs, floating-point stability and measured native speed are separate.

The already completed same-target full-similarity comparator costs O(N log N) and requires its explicitly supplied primitive 2Nth root for length-2N convolution. Its presence is not a new result of this report. The r=N block endpoint remains excluded by the supplied-Nth-root contract. The original fused O(Nr) implementation can reach r=N quadratically; those two endpoints must not be merged. Nested same-input tails retain ell=r+s_tail-1 and nextpow2(ell)<=N/2; independent inputs cannot reuse that small state. Q07 recognition remains a separate interface.

**Disposition:** exact scalar-polynomial Prony/rational-series match, qualified nonmatch to the requested arbitrary-vector operator application. This completes the named comparison only. The low-degree remainder, shared complete-transform graph, numerical/production qualification and historical priority remain open.

## 2. ALG-019: sparse orbit transport is not sparse temporal spectrum

### Declared owner target and recurrence map

Use the owner's exact dyadic field/root contract, actual finite corner, H=H_q(C), and nonzero weighted cyclic permutation R with R^N=I. The accepted covariance is HR=DH, D=R(I-C). H is invertible because C is nilpotent and H_q has constant coefficient one. The declared reusable inputs are x_j=R^j x_0 after a fully paid y_0=Hx_0, with y_j=D^j y_0.

A direct linear-algebra comparison identifies the actual temporal recurrence order. For x_0=e_0, the N vectors e_0,R e_0,...,R^(N-1)e_0 are nonzero multiples of distinct coordinate vectors, hence form a basis. Since R^N=I, minpoly(R)=z^N-1. Applying invertible H proves that y_0,...,y_(N-1) are also a basis and minpoly(D)=z^N-1. Therefore no scalar-coefficient recurrence of order<N can generate this entire vector orbit from its beginning. The order-N recurrence y_(j+N)=y_j is exact. This assertion is about this recurrence interface, not a lower bound against other algorithms or a claim that every scalar projection has order N.

There is also an explicit scalar witness within the raw input interface:

    s_j=e_0^T R^j e_0 = 1 if N divides j, and 0 otherwise,
    sum_(j>=0) s_j u^j = 1/(1-u^N),
    s_j=(1/N) sum_(a=0)^(N-1) (q^a)^j.

Every state R^j e_0 is one-sparse in coordinates, but this scalar temporal sequence has all N distinct nonzero q-grid modes and minimal register length N. The rational fraction is reduced; the displayed orthogonality sum follows from q's exact order and invertible N. This maps precisely to Massey's scalar theorem. It also shows why coordinate-support preservation cannot be substituted for the sparse temporal-mode promise used by Prony.

For a more general x_0, special cancellations can shorten a projected or vector recurrence. The owner does not promise them. Applying Algorithm 4 with T=N to the witness would require order at least 2N, not provided by q of order N. A known-grid N-point Fourier inversion can of course represent this sequence without that extra root; the point is that the selected sparse-interpolation guarantee does not deliver an uncharged small-mode replacement. No impossibility of other algorithms follows.

### First action, full outputs and complete recursion

For a declared orbit of J query vectors, a streaming execution costs the paid first H action, O(N) grading preparation, and J-1 updates. Each input/output update has 3N-1 multiplications and N-1 additions, and writes N outputs. Storing all results requires O(JN) words; streaming needs O(N) live storage. Producing the samples or recovering scalar modes cannot erase these costs. A new independent vector is not automatically in the previously computed orbit, and nonunitary weights do not supply a rounding bound.

The accepted complete evaluator handles arbitrary fresh p(C)x through a different growing-filter recursion. At depth d, r=2^d, n=N/r and

    D_r=product_(a=0)^(r-1)(I+q^a J_n) diag(q^(-ri)).

The first linear-cost parity split is genuine, but D_2 has three nonzeros per row for N>=8 and is not the original two-sparse family under a monomial coordinate change. Generic even q-factorial coefficients do not become H_(q^2). All these exclusions were already completed and are preserved, not newly claimed.

The three recursive calls E(D)x, O(D)y and (E+O)(D)(x+y) produce both output blocks. All distinct inputs, coefficient sums, basis changes and D applications are charged. Node overhead is Theta(min(rn,n^2)); summing the retained construction gives

    Theta(sum_(d=0)^(log2(N)-2) 3^d min(N,N^2/4^d)+3^(log2(N)-1))
       = Theta(N^(1+0.5 log2(3))).

Shared depth plans cost O(N log N) preparation; live storage is O(N). The known full-operator O(N log N) comparator remains asymptotically better. Neither scalar sparse interpolation nor an orbit recurrence supplies a proved sharing rule for the independent recursive actions. This is the source-bound reason the comparison can finish while the faster complete graph remains genuinely open.

**Disposition:** exact rational-series/recurrence mapping with an explicit full-order witness, qualified nonmatch to small-mode recovery or an automatic faster complete evaluator. The named comparison is complete. Additional proved cross-action sharing, numerical/bit-model implementation and historical priority remain open.

## Minimal local cell proposal

`NATIVE_CELL_PREFIX_PROPOSAL.json` contains exactly 18 text-prefix changes: for each ID, Catalogue AE/AF; novelity breakthough O/P/Y/Z; Research overview F/P/Q. These are the current-action, comparison-evidence and pass/stop views. They preserve every old text byte under an explicit historical delimiter. No status, priority, proof, novelty, formula, canonical count, ID, title, old source link or original obligation is changed. In particular overview E190/E191 stay TO RESEARCH and L190/L191 stay 34.

The proposal is local and unapplied. Independent review and a fresh native preflight must precede any write. Apply only text values while preserving notes, formats, validation and rich links; abort on an unexpected preimage, ID, formula or metadata condition. No publication URL is guessed. A verified publication link may be attached separately after publication is confirmed.
