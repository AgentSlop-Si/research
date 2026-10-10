# Independent audit: FFT-horizon compressed retained Schur inverse

## Verdict

Accept the finite-horizon identity `K_(b+t)=C_t Q_r^t`, the table-driven constant-input evaluator, and the closed causal formal inverse for an arbitrary supplied polynomial right-hand side through degree n=log2 N. The retained inverse costs `O(r(n+1+d²)+n)` field/address work, where `r=N/2^b=2^d`, and `O(r(n+1)+r+n)` words. Choosing b=ceil(2 log2 n), when 1≤b≤n, makes this retained task O(N).

This is a real closure of the previously unresolved retained polynomial operation at this specific horizon. It does not close the full Fourier computation: constructing the right-hand side from arbitrary eliminated input and recovering the requested global outputs still need their own paid algorithms. The complete method currently verified remains O(N log N). No infinite rational closure, unrestricted FFT lower bound, bit-complexity improvement or historical novelty is asserted.

## 1. Source identity and review method

Constructor report: `iteration_13_compressed_schur/FFT_HORIZON_COMPRESSED_SCHUR_INVERSE.md`, SHA256 `c613761902541264b920a92ccadd68f75ab1f187cd570e336ea31cdb1957fdcb`. The full report and `verify_compressed_schur.py` were inspected as inert text. All four entries in `COMPRESSED_SCHUR_SHA256SUMS.txt` match; the report, checker, JSON controls, log and manifest are preserved unmodified in `constructor_snapshot/`. Supporting JSON/log entries were parsed as the constructor's evidence, not treated as independent runs.

Only newly authored `independent_compressed_checks.py` was executed. It imports no constructor or uploaded code. It reconstructs feedback matrices by full-space Q multiplication and eliminated-coordinate projection, then compares the compressed implementation to those matrices. `PROVENANCE.json` records all snapshot identities; `PORTABILITY_CHECK.json` records an actual relocated replay.

The construction uses the stationary Q source and the previously reviewed variable-block Schur definition. Earlier seals, including the scalar coupled-guard counterexample, remain unchanged. This audit is an additive post-checkpoint20 result.

## 2. Exact target and the finite-horizon distinction

Let N=2^n, 1≤b≤n, r=N/2^b=2^d. A supplied primitive Nth root ω is required over a field of characteristic not dividing N. Let

`Q_N e_s=e_(2s mod N)+ω^s e_(2s+1 mod N)`.

Retain `R={2^b j:0≤j<r}` and eliminate its complement E. The retained block is `Q_RR=A_r`, where `A_r e_j=e_(2j mod r)`. Exact formal elimination gives

`S_b(z)=I−zA_r−Σ_(L≥2) z^L K_L`,
`K_L=Q_RE Q_EE^(L−2) Q_ER`.

All inverses here are formal at z=0, with constant term identity. There is no numerical scalar-pivot guard in this formal problem. The input is an explicitly supplied array of r(n+1) coefficients f(z), and the output is `S_b^−1f mod z^(n+1)`. A supplied arbitrary polynomial marker h(z) is retained by the ordinary top-coefficient contraction; its r(n+1) reads/products/additions must be paid.

## 3. Independent proof of the compressed first-return identity

For a word k of t bits, define γ(0)=0, γ(2a)=γ(a), γ(2a+1)=γ(a)+a, and let rev_t reverse exactly t bits. Starting at j in the size-r Q graph with root η, following those t edges ends at `2^t j+k mod r` and has weight

`η^[j rev_t(k)+γ(k)]`.

Appending a zero doubles the state and adds no phase. Appending a one doubles the state, adds one, and multiplies by the current state's root power. This proves the formula inductively. Reducing the intermediate state modulo the graph size changes no root power. In particular trailing zeros change neither rev_t's contribution when interpreted with the original meaningful word nor γ's numerical value.

A first excursion from a retained state must begin with one. Its first return is completed by b zeros after the last one. Hence an excursion of length L=b+t≤n is exactly a t-bit word that starts and ends in one, contains no b-zero run, and is followed by b zeros. There is no return with 2≤L≤b. Call the admissible words B_(b,t).

Starting from global index 2^b j, the full weight is

`η^[j rev_t(k)] ω^γ(k)`, with `η=ω^(2^b)`;

the retained endpoint is `2^(b+t)j+k mod r`. For t≤d, the intermediate coordinate `a=2^t j+k mod r` uniquely identifies k by `k=a mod 2^t`. This uniqueness is the exact horizon restriction.

Define ζ=ω/η. Route intermediate coordinate a only when its identified word k is admissible; multiply by `ζ^γ(k)` and send it to

`y=2^b(a−k)+k mod r`.

The multiplication converts the compressed Q_r phase to the full phase, and the routing gives the full retained endpoint. When multiple a merge, their input fibers are precisely the disjoint fibers contributing to that endpoint, and ordinary addition handles the merge. Thus, for every input vector,

`K_(b+t)=C_t Q_r^t`, 1≤t≤d,

and

`S_b(z)=I−zA_r−Σ_(t=1)^d z^(b+t)C_tQ_r^t mod z^(n+1)`.

This proves an operator identity, not just a selected-input or scalar-marker equality. The case b=n has d=0 and no feedback term in the horizon; it is included.

## 4. Uniform table generation and exact structural support

η is obtained by b squarings of ω; ζ requires one inversion and one multiplication. Consecutive tables of η^a and ζ^a cost O(r), and

`c_(2a)=c_a`, `c_(2a+1)=c_a ζ^a`

generates all correction coefficients in O(r). No discrete logarithm, root extraction or per-edge exponentiation is used. Binary-parent recurrences compute trailing-zero and maximum-zero-run data in O(r) word operations. A word is eligible exactly when its leading bit lies at position t−1, it is odd, and its maximum zero run is less than b. The operations are on O(log N)-bit indices; this is a word/address model, not a unit-cost arbitrary-bit-integer assertion.

Our independent plan meters this setup: b+1+2(r−1)+floor(r/2) multiplications and one inversion, plus O(r+n) word/read/write work. It avoids multiplying by one in the even correction recurrence. The constructor's implementation may perform additional O(r) identity multiplications; this does not change its bound. Verifying the supplied root or discovering a field/root is a separate task; root discovery is not free.

For one constant vector, execute d sparse Q_r steps, each O(r), and d length-r routing scans. Initialization, recycled buffers, zero entries, phase updates, accepted merges and output writes are all charged. Total work including setup is O(r(d+1)+n).

For a fixed admissible k, the folded image has exactly `max(r/2^(b+t),1)` coordinates. Different words have different low-t-bit residues and therefore disjoint images. Each matrix row counted has a nonzero structural coefficient: within this horizon a fixed input/output pair cannot contain cancelling distinct words with the same k. Thus coefficient b+t has exactly

`|B_(b,t)| max(r/2^(b+t),1)`

structural output rows. Since `|B_(b,t)|≤2^(t−1)`, summing the early terms gives O(dr/2^b), and the remaining geometric tail gives O(r). These are emitted sparse coefficient slots. They do not remove the charged O(rd) dense trajectory work or the r(n+1) size of an arbitrary polynomial right-hand side.

## 5. Polynomial application and the causal inverse

For each input coefficient v_j, only trajectory lengths `1≤t≤d−j` can contribute below degree n+1. The exact number of Q_r state visits is

`r Σ_(j=0)^(d−1)(d−j)=r d(d+1)/2`.

Each Q_r step has r multiplications and 2r additions. Every associated routing scan visits r positions, and each accepted route costs one multiplication and one addition, including additions into existing coefficients. I−zA_r costs O(r(n+1)), and loading/storing the polynomial coefficients has the same bound. This proves the polynomial application bound without hiding a coefficient convolution in a scalar operation.

For inversion, initialize ρ_j=f_j. In increasing j:

1. Set v_j=ρ_j.
2. Add A_r v_j to ρ_(j+1), if that index is ≤n.
3. Starting with v_j, stream its Q_r trajectory through t≤d−j, and add C_tQ_r^t v_j to ρ_(j+b+t).

All updates go to later coefficients. At stage j, ρ_j is exactly the right-hand side of the coefficient-j Schur equation; induction proves the inverse. The same triangular state count applies. This is a complete causal program, not a recursive appeal to a smaller unresolved inverse.

Dense coefficient arrays occupy O(r(n+1)), with O(r) scratch and O(r+n) tables/counters. If b=ceil(log2(n²))≤n, then r≤N/n² and d≤n, so both `r(n+1)` and `rd²` are O(N). The finitely many small-n cases can be handled directly or by b=n; no invalid b=0 or b>n is required. With b near log2 n, the literal trajectory schedule has Θ(N log N) state visits for growing n. The improvement is specific to the larger retained spacing and supplied polynomial task.

The top polynomial-marker coefficient is `Σ_j h_j^T v_(n−j)`, taking O(r(n+1)) extra work. Exact arithmetic does not give floating-point stability or precision guarantees. Field inversion and multiplication require their ordinary costs in a bit model.

## 6. Boundary maps, rank obstruction and stopping point

For arbitrary full input x, the missing source task is

`f(z)=x_R+zQ_RE(I−zQ_EE)^−1x_E`.

Recovering eliminated outputs requires

`y_E=(I−zQ_EE)^−1(x_E+zQ_ERv)`.

The first-return identity starts at retained coordinates and therefore does not cover arbitrary x_E. Nor does it recover N global outputs from the retained coefficients without extra work.

For the first b source coefficients, the first hit of R at time L can use only zero edges. The input index must have exact two-adic valuation b−L; its retained destination is `s/2^(b−L) mod r`. For r≥2 this reaches each odd retained coordinate, and the source-coordinate subsets for distinct L and destinations are nonempty and disjoint. Stacking these maps gives rank exactly br/2. For r=1, the b valuation classes give rank b. Thus one fixed r-dimensional *linear summary* cannot represent all these early source coefficients when b≥3 (r≥2), or when b≥2 and r=1.

This is an input-summary dimensional obstruction, not an arithmetic lower bound. It does not rule out larger summaries, a polynomial summary or a direct O(N) source algorithm. It also does not imply that every source/output wrapper is expensive. Those are still separate research obligations.

The existing full reference source/recovery method uses the original sparse global system through n coefficients, costing O(Nn), and every coordinate and coefficient is checked. Therefore no end-to-end Fourier improvement follows yet. The old scalar coupled-guard example (N=4, F17, ω=13, b=2, z=8; branch determinants 3 and 14, coupled packet determinant 0, full determinant 7) remains valid in its prior seal. It does not obstruct the present formal-at-zero inverse; the distinction is essential.

## 7. Falsifying controls and exact independent results

The unchanged routing fails beyond the stated horizon because an intermediate coordinate no longer identifies the appended word. We reproduce the exact constructor counterexample: N=16, F65537, b=2, ω=64, input (1,2,3,4). At return degree 5, the unchanged compressed route gives zero, while direct eliminated-space propagation gives `(0,57313,0,510)`. The accepted identity stops at degree n=4.

Separate fresh controls at N=32, b=1 reject both omitting the b-bit fold and replacing Q_r^t by Q_r^(b+t). Phase multiplication alone cannot repair those changes.

Across F65537 and F257, every b for N=2,4,8,16,32,64,128,256 passes:

- 72 parameter cases and all 1,004 retained basis inputs, comparing every feedback coefficient to full-space matrix multiplication;
- 168 exact structural support counts;
- 160 word-phase groups, checking every word through t=5 from multiple wrapped initial states;
- 72 arbitrary polynomial inverses, independently applied and also compared to a dense coefficient recurrence;
- 72 supplied polynomial-marker checks and complete fresh-global-input recovery through every coefficient;
- 42 exact early-source stacked-rank tests through N=64, including r=1;
- exact state-visit, route-scan, tree-update and output-coefficient counts;
- count-only large-n checks through n=1024 without allocating those enormous vectors.

All pass. Our matrix oracles are deliberately not the claimed fast algorithm; the independently implemented retained plan is table driven and separately metered. The proofs establish the all-size result. Portable replay copies only this independent checker to a new directory; outputs are byte-identical. All hashes, results, code and source snapshots are in the sealed manifest.
