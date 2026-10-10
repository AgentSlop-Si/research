# Complementary graph reconstruction and charged dispatcher fusion

These are independently justified project extensions. The supplied programs were not modified or executed. No external originality or priority claim is made.

## A. A stronger output-variation theorem without a second balance guard

Let two raw N=QM vectors pass the previously audited per-fiber recognizers with fixed mode bounds r_x,r_y and Q²<=C N. Supply the same prime field/root model as in AUDIT_REPORT.md. Their normalized character-amplitude arrays A,B have K_x<=r_x Q and K_y<=r_y Q nonzero entries.

The graph merge computes exact output amplitudes

    C[t,h] = M sum_{a+b=t+Qe} A[a,h] B[b,h] eta^{-he}.

All matching edges are charged:

    E = sum_h nnz(A[:,h]) nnz(B[:,h]) <= K_x K_y <= r_x r_y Q².

The dense N-cell accumulator, final cancellation scan, temporary zero/revival events and markers cost O(N+E). Counting support before cancellation would be unsound. The complete raw-input stage, before output reconstruction, costs

    O((r_x+r_y)N+(r_x²+r_y²)Q+E+N),

with O(Q(r_x+r_y)) scalar inversions from recognition. These are fixed-parameter O(N), under the supplied word/field contracts.

Let H be the number of surviving nonzero frequency columns. Every such label occurs in both inputs, so

    H <= min(K_x,K_y,M) <= min(r_x,r_y)Q.

This inherited sparsity remains useful even if the Q-by-M output matrix C itself is dense on its H columns.

Fix an integer output difference order d>=1. For Q>=d, define

    V_d = sum_{t=d}^{Q-1} nnz(nabla^d C[t,:]).

Scanning C and forming these differences costs O_d(N), with no new raw-signal recognition or hidden FFT. If V_d<=c_d Q for a fixed c_d, reconstruct all raw outputs as follows:

1. Evaluate each of the first d rows using its at most H active labels. Cost O(d M H), including phase lookup preparation. No dense M² transform is required.
2. Expand each sparse order-d difference into its M time-domain values, at total cost O(M V_d+N) when zero writes/scans are included.
3. Integrate the fixed-order recurrence forward in physical row order:

       z_t[u] = D_t[u] + sum_{j=1}^d (-1)^{j+1} binom(d,j) z_{t-j}[u].

   This is O_d(N), with d rolling history rows. Explicitly write every output.

Therefore reconstruction costs

    O_d(N+d M H+M V_d),

and is O_{d,r_x,r_y,c_d}(N). It requires **only Q²=O(N)** for the existing edge stage; **M²=O(N) is unnecessary**. All active columns and differences are derived from the charged merged array. If Q<d, either skip that candidate or directly expand all Q rows: Q M H<=d M H, again O_d(N) under the same bound.

The source first-difference gate instead counts

    D_source = nnz(C[0,:]) + V_1.

Its literal root evaluation is already O(M*nnz(C[0,:])), and all later work is O(N+M V_1). Thus it has an even sharper literal reconstruction ledger O(N+M D_source), although its documentation conservatively charges M². The source nevertheless hard-codes M²<=4N after the original state guard fails. Dropping that additional guard, and allowing the initial row to be paid from H, is a separately justified enhancement. Neither change is silently credited to the shipped function.

## B. Union with the prior rank fallback

The prior audit proves that rank(C)<=ell for fixed ell allows factorization C[t,h]=sum_j f_j[t]g_j[h] in O(ell Q H+N) work with at most ell inversions. Basis rows remain supported on those same H columns. Evaluate their character sums in O(ell M H), then explicitly write N outputs in O(ell N). This is also O(N) under the same input-mode and Q² assumptions.

A deterministic bounded dispatcher can therefore:

1. Try the original S=nnz(C)<=c_S Q expansion;
2. Try rank(C)<=ell;
3. Try V_d<=c_d Q for a fixed finite public list of orders d;
4. If all guards fail, decline this structured reconstruction.

The order of the successful alternatives can be rearranged. Crucially, every failed bounded-rank test and every difference scan is still charged O(N); failed routes do not execute an unguarded large expansion. A constant-size list preserves the linear bound. A constant total of at most ell new scalar inversions is added beyond input recognition.

The state condition is not logically essential when a sufficiently large first-variation budget is present: D_source<=2S. It can still be useful as a cheaper direct reconstruction. The rank and variation branches, by contrast, are genuinely distinct even on valid fixed-mode convolution inputs, as the next two constructions prove.

## C. Strict complementarity on actual sparse-input graphs

### C.1 Variation succeeds while every fixed-rank bound eventually fails

Set Q=M=s² with s>=2. Give x-row a the single label a mod s and y-row b the single label floor(b/s), all amplitudes 1. For label h=0,...,s-1, write a=h+s v and b=hs+w. Their sum is

    a+b = h(s+1)+s v+w.

The pair (v,w) runs once through every residue modulo Q. Thus E=S=sQ and every target row is occupied in each of s columns. The carry flips only at t=h(s+1):

    C[t,h] = M eta^{-h}, t<h(s+1),
             M,             t>=h(s+1).

For h=0 the column is constant. For h>=1 its jump is nonzero because eta has order M and 0<h<M. The distinct step positions make these s columns linearly independent: take temporal differences to isolate each nonconstant column, then retain the constant one. Hence rank(C)=s.

There are V_1=s-1 transition states and nnz(C[0,:])=s, giving D_source=2s-1. Therefore the first-difference branch accepts in linear work, while every fixed-rank ell eventually rejects as s grows. The original S<=c_S Q branch also eventually rejects because S/Q=s.

The construction works equally with any M>=s and valid field/root, provided Q²=O(QM). The independently checked Q=9,M=81 case has N=729 and violates the source's M²<=4N guard, yet has S=27>2Q and D_source=5. The justified sparse-variation extension evaluates all 729 convolution outputs exactly. This is a concrete missed fast-path opportunity caused by the extra balance guard.

### C.2 Rank succeeds while every fixed state/first-variation bound eventually fails

Again set Q=M=s². For h=0,...,s-1 and v,w=0,...,s-1:

- At x-row a=h+s v, use label h with amplitude eta^{h floor((h+v)/s)}.
- At y-row b=(s-1)h+w, use label h with amplitude b_w=1+(w mod 2).

Every x row has one mode. The y intervals of length s are separated by s-1, so every y row has at most two modes. All amplitudes are nonzero since p>N.

Now a+b=s(h+v)+w. The carry is floor((h+v)/s), so the x amplitude cancels the graph carry factor exactly. As v,w vary, each output row appears once. Therefore

    C[t,h]=M b_{t mod s} for h<s, and C[t,h]=0 otherwise.

This is rank one, with S=sQ and H=s. For even s, the row factor changes at every adjacent row, so V_1=s(Q-1). For odd s, it changes at Q-s adjacent rows, so V_1=s(Q-s). In both cases D_source/Q grows on the order of s. Thus every fixed state or first-variation ratio eventually rejects, while the fixed rank-one branch accepts in linear work.

The checker verifies full direct convolution equality for s=3,4,5, not merely abstract coefficient matrices. This improves the earlier constant-row rank-one escape by showing that rank and temporal variation are not interchangeable assumptions on the actual input class.

These examples establish complementarity of fixed-rank and first-variation guards. They do not claim that the second family defeats every fixed higher-order variation test; that stronger assertion is not needed or established here.

## D. Full DFT dispatcher with separately budgeted Toeplitz

The graph reconstruction theorem concerns **cyclic convolution output**, whereas the Delta/Newton theorem concerns a **raw-input full DFT**. Keep these APIs and certificates distinct. Having a special convolution reconstruction route does not transform every raw input or imply an arbitrary-integer multiplication speedup.

For the raw-input DFT dispatcher, take a fixed finite public list of:

- balanced coprime CRT splits with tensor rank budget r_T;
- fiber splits satisfying Q²<=C N with per-fiber budget r_F;
- balanced Newton splits/orders, each fixed order d and total mode budget R_j;
- optionally fixed-anchor Delta alternatives with the repaired complete reset recognizer;
- the maximal support-coset/common-chirp branch with its separate budget r_C and the prior polynomial Toeplitz eliminant.

Charge every attempted recognizer; do not treat the first accepted branch as justification for free earlier scans. An unavailable factor/order is skipped explicitly. The old selected-divisor limitations remain unless the actual selected list is enlarged. A fixed finite list still does not cover all possible divisors.

For one of each inherited branch and a fixed finite Newton list, the arithmetic bound is

    O( N(1+r_T+r_F+r_C^4) + r_C^{2+3 log_2 3}
       + sum_j [d_j M_j² + (M_j+Q_j)R_j] ),

where constants depend on the fixed orders, balance ratios and list size. This uses the independently audited polynomial Toeplitz implementation for the chirp eliminant; the supplied factorial code must not be assigned this ledger. Fixed-B reset alternatives add their separately charged B M²+B N+(M+Q)R costs.

A conservative scalar-inversion count is

    O(r_T + Q_F r_F + 1 + r_C^4 + sum_j R_j),

with O(B M) extra possible failed-attempt inversions for each optional reset branch. Public factor scans, integer gcd/inverse operations, supplied-root checks, all input/output writes and preparation remain charged. For fixed orders and O(Q) event budgets, each Newton addition is O(N). The resulting result is a larger **selected structured union**, with no exact spectrum returned for a rejected arbitrary vector.

The same ledger allows a modest uniform event-budget schedule: for balanced Q_j,M_j and R_j=rho_j Q_j, each fixed-order Newton branch costs O_d((1+rho_j)N). Therefore r_T,r_F,rho_j=o(log N) and r_C=o((log N)^{1/4}) give o(N log N) arithmetic for all-input recognition and any accepted full DFT, after the separately budgeted polynomial chirp route is actually implemented. Inversion work remains absorbed under the polynomial-size word-field assumptions. This is a scoped growing-budget corollary, not a growing-order claim or an arbitrary-input transform theorem.

## E. Implementation and stopping boundary

This audit adds proofs, independently authored checkers and concrete counterexamples. It does not change the master or source programs, integrate a new dispatcher, execute supplied tests, or claim performance superiority. The implementable next steps are sharply bounded:

1. Replace the greedy optional-reset selection with the complete largest-cost rule if full B-anchor union coverage is intended.
2. Remove only the unnecessary graph-output M² guard after preserving the Q²/input-mode checks; budget reconstruction using active columns and variation.
3. Combine state, output rank and fixed-order variation alternatives with charged rejection.
4. Wire explicitly selected Newton branches into a separately budgeted DFT dispatcher, using the existing polynomial Toeplitz work only where actually integrated.

The unrestricted fresh arbitrary-input target remains open. No lower bound, quantum advantage, stable-complex theorem or publication-priority conclusion follows from this package.
