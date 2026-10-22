# ALG-031: a shared quadratic seed still permits bounded diffuse-input concentration

21 October 2026 UTC. Candidate for independent verification, not accepted owner closure. No source program was executed and no external state was changed.

## Bounded result and unchanged owner boundary

For the exact original affine-chirp measurement and natural adjoint decoder, one nonzero quadratic coefficient a may be reused across all repetitions in the odd-prime regime. Fresh independent uniform affine pairs (b_j,d_j) are sufficient for a full-output coordinate-median guarantee on inputs satisfying the explicit diffuseness condition below. The proof is conditional on a; the repetitions need not be unconditionally independent when a is initially random and then reused.

The price of a uniform all-frequency guarantee proved here is a harmonic-squared factor. At the alias frequencies, that factor disappears and there is a sharper exact conditional variance identity. This is a bounded seed-reuse result, not a better overall FFT runtime, arbitrary-input theorem, dyadic theorem, stability theorem, bit-complexity result, or joint fast decoder. In particular, it does not close ALG-031. Independent review is pending.

## 1. Source-exact contract

The three original source bodies are retained verbatim in sources/. Their SHA256 values match the ALG-031 catalogue capture and the retained primary-source register:

- DECODER.md: 958a37ab8f0db835a83a62135b8b704533cce88f0f774667799da681b20d126a, 9,129 bytes. Result and sections 1-5 give the exact O(N log(2K)) natural-adjoint evaluator for all integer a,b,d when N=KM, K<=M; section 5 charges each repeated decoder unless another shared computation is proved.
- REPETITION.md: 0554f98e8eb0cdca57a5100d0a60e4f0a85c2613aaf723c0fbceec7d6b347638, 9,534 bytes. Sections 3 and 5 give the independently repeated variance/median argument, and sections 1-2 preserve spike obstructions. Its exact variance formula requires averaging a, not fixing it.
- AFFINE_RESONANCE.md: 504e7f01540b55df9a65692fe6d79e87fee014e7b08ab7f50f0bf499239aad55, 7,967 bytes. Decoder definition and sections 1 and 4 give the prime Gauss identities, flat alias obstruction, and precise covariance warning when a is fixed.

The underlying public repository locators are in SOURCE_BINDINGS.json. This candidate relies on the original mathematical bodies, not only their catalogue summaries. The accepted historical status is scoped exact decoder of the sketch, not exact DFT or a guarantee of sketch accuracy. The catalogue retains stability, bit complexity, stronger concentration, and shared multi-seed computation as unresolved. No native owner row was modified or independently reclassified here.

Let M be an odd prime, 1<=K<=M, N=KM, and x in C^N be fixed independently of the random seeds. Write x_{r,t}=x_{rM+t}, e_L(z)=exp(2 pi i z/L), and use the unitary DFT X. Choose any fixed a in F_M\{0}. It may instead be sampled once independently of x and then held fixed; every assertion below holds conditionally for every allowed value of a.

For each repetition j, draw b_j,d_j independently uniformly from F_M. The pairs are independent across j and independent of a and x. Set s_{j,r}=b_j+d_j r modulo M, and use exactly the original measurements and decoder:

Y_{r}(s)=sum_{t=0}^{M-1} x_{r,t} e_M(a t^2+s t),
H_s(m)=sum_{u=0}^{M-1} e_M(-a u^2-s u)e_N(-m u),
Xhat^{(j)}_m=N^(-1/2) sum_{r=0}^{K-1} e_K(-mr)Y_r(s_{j,r})H_{s_{j,r}}(m).

There is no changed sketch, input-dependent seed, head removal, alternative decoder, or raw-input side channel. For concentration, this is complex exact arithmetic. A broader pure field-operation contract alone does not provide the complex order comparisons required for coordinate medians.

## 2. Exact variance conditional on the shared a

Define the unnormalized local transform

F_r(m)=sum_t x_{r,t}e_N(-mt).

Then, conditional on a,

E[Xhat_m | a]=X_m,

Var(Xhat_m | a) = (1/N) sum_r [ (1/M) sum_{s in F_M} |Y_r(s)|^2 |H_s(m)|^2 - |F_r(m)|^2 ].                 (1)

Proof. A uniform s gives E_s[Y_r(s)H_s(m)]=F_r(m), since the s average kills precisely terms with t!=u. If r!=r', the map (b,d)->(b+dr,b+dr') is a bijection of F_M^2: r-r' is nonzero because K<=M. Thus the two slopes are independent uniform residues and the centered contributions of the two blocks have zero covariance. The block phases have modulus one, leaving exactly (1). This uses pairwise independence inside a repetition, not independence of all K blocks. It does not average a or cancel a nonexistent quadratic covariance condition.

The identity remains algebraically valid for a=0, but the following Gauss bound does not. For K>M the block covariance need not vanish; this candidate does not extend (1) to that range.

At every alias m=qK, the nonzero-a prime Gauss identity gives |H_s(qK)|^2=M for all s. Parseval for Y_r gives (1/M)sum_s|Y_r(s)|^2=sum_t|x_{r,t}|^2. Hence the exact sharper alias identity is

Var(Xhat_{qK} | a) = [ M ||x||_2^2 - sum_r |sum_t x_{r,t}e_M(-qt)|^2 ] / N.                 (2)

It is not the unconditional source identity (M-1)||x||_2^2/N. For example, on flat input the conditional DC variance in (2) is zero; at a nonzero alias it is M||x||_2^2/N. A spike gives (M-1)/N, preserving the original spike obstruction.

## 3. All-frequency chirp interpolation bound

Write m=p+Kq, 0<=p<K, 0<=q<M, and tau=p/K. Define

G(v)=sum_u e_M(-a u^2-vu),
C_j(tau)=(1/M)sum_{u=0}^{M-1} e_M((j-tau)u),
Lambda_M(tau)=sum_{j=0}^{M-1}|C_j(tau)|.

Fourier inversion of e_M(-a u^2) gives the exact identity

H_s(p+Kq)=sum_{j=0}^{M-1} G(s+q+j) C_j(tau).                 (3)

All subscripts on G are modulo M. The identity |G(v)|^2=M follows by expanding its squared modulus and grouping u-w=h: the sum over w vanishes unless 2ah=0, hence h=0 in this prime/nonzero-a regime. Thus |G(v)|=sqrt(M), and

|H_s(p+Kq)| <= sqrt(M) Lambda_M(tau).                 (4)

For tau=0, Lambda_M(0)=1. For 0<tau<1, the geometric-sum formula gives

|C_j(tau)|=sin(pi tau)/(M |sin(pi(j-tau)/M)|).

Let d_j be the distance from j-tau to M Z, and order these distances increasingly as d_(1),...,d_(M). The nearest coefficient has modulus at most one, because it is an average of unit-modulus numbers. For k>=2, d_(k)>=(k-1)/2: k distinct grid points in a circular interval lifted to [-M/2,M/2] have extreme separation at least k-1. Also sin(pi d/M)>=2d/M for 0<=d<=M/2. Therefore the kth remaining coefficient is at most 1/(2d_(k))<=1/(k-1), proving

Lambda_M(tau) <= L_M := 1 + sum_{h=1}^{M-1} 1/h <= 2+log(M-1).                 (5)

This intentionally elementary bound is not claimed sharp. Define Lambda_* = max_{0<=p<K} Lambda_M(p/K); either Lambda_* or the computable upper bound L_M may be used below. Combining (1), (4), and Parseval yields

Var(Xhat_m | a) <= M Lambda_M(p/K)^2 ||x||_2^2 / N
                  <= M Lambda_*^2 ||x||_2^2 / N.                 (6)

The subtracted block-energy term in (1) can be retained for a sharper input-specific bound. No exact fixed-a equality without that term or the interpolation weights is asserted.

## 4. Shared-a full-output concentration

For x!=0 put rho=||x||_2^2/||x||_1^2. Fix epsilon>0 and 0<delta<1, and suppose

p_* := 2 M Lambda_*^2 rho / epsilon^2 < 1/4.                 (7)

The stronger, simpler sufficient condition 2 M L_M^2 rho/epsilon^2<1/4 avoids needing Lambda_* numerically. For odd R, aggregate by taking the ordinary real and imaginary coordinate medians of Xhat^{(1)}_m,...,Xhat^{(R)}_m separately, just as in REPETITION.md section 5.

For each fixed a,m, (6) and Markov give a one-repeat probability at most p_* of error greater than epsilon||x||_1/sqrt(2N). Conditional on a the repetitions are independent, because their (b_j,d_j) pairs are independent. If a strict majority are inside that disk, both component medians lie inside its coordinate bounds, so final complex error is at most epsilon||x||_1/sqrt(N).

A union bound over majority-bad subsets gives a failure probability at most 2^R p_*^((R+1)/2) <= (4p_*)^(R/2) at one bin. A union over all N frequencies, followed if needed by averaging over the shared a, proves

P( ||median_j Xhat^{(j)}-X||_infinity > epsilon||x||_1/sqrt(N) ) <= N (4p_*)^(R/2).                 (8)

Thus it suffices to take the least positive odd integer R at least

2 log(N/delta) / log(1/(4p_*)).                 (9)

For x=0 the output is identically zero. For an aliases-only guarantee, Lambda_*=1 and the union factor is M rather than N; (2) gives an optional still sharper variance. That aliases-only statement must not be substituted for (8).

For a flat input, rho=1/N, so the simple all-output sufficient hypothesis is K epsilon^2>8 L_M^2, and the denominator in (9) becomes log(K epsilon^2/(8L_M^2)). This is a genuine diffuse-input theorem with one reused quadratic seed. It is weaker than the source's independently refreshed-a variance guarantee by the harmonic-squared factor, not a claimed improvement in concentration rate. It does not give small-R accuracy on a spike or all arbitrary inputs.

## 5. Exact guard failures

These cases show why the stated independence and arithmetic hypotheses cannot be silently dropped.

1. If a=0 is fixed, take flat x and m=0. For a uniform local slope s, Y_r(s)H_s(0)=M^2 times the indicator s=0, so Var(Xhat_0 | a=0)=K M^2(M-1)/N=M(M-1). Formula (2), wrongly applied at a=0, would give zero. Thus sampling a once from all of F_M and ignoring its zero event is not permitted. For uniform shared a including zero, one may only claim a separate failure allowance of at most 1/M in addition to the nonzero-a theorem; no such changed theorem is used here.
2. If d=0 is fixed rather than refreshed, take nonzero a and flat input at a nonzero alias. The shared-slope source identity gives normalized error magnitude one for every b. Its variance is N, whereas (2) for independent affine slopes gives M. The factor is K. Fresh b alone does not justify the block-decorrelated variance or the diffuse hypothesis (7).
3. Reusing b on a spike x=e_0 leaves the block-zero decoder unchanged under changes of d. Merely creating differently named d seeds does not provide independent spike estimates. This preserves, rather than evades, the source's repeated-arithmetic-mean and raw-median obstructions.

The second case is not a claim that fresh b averaging or medians can never work; it only rejects borrowing the independent-affine variance at fixed d. Similarly, neither example is an unconditional lower bound on all shared computations or all Fourier algorithms.

## 6. Whole cost and representation ledger

- Sketch formation is charged: R original sketches cost O(RN) exact arithmetic operations, with 2R independent uniform F_M draws and an optional one-time nonzero-a draw. Inputs are not assumed free to inspect.
- For a fixed shared a, the base table H_0(m) can be formed once in O(N) arithmetic by DECODER.md, and H_b(m)=H_0(m+Kb). This is only table reuse. Every repeat's seed-dependent sketch values and short-filter convolutions are still charged.
- The retained decoder gives O(RN log(2K)) arithmetic for all R full N-output decodes, including preparation, guarded inversions, nonunit/zero d cases, indexing in O(log N)-bit words, and the O(RN) sketch/input/output work. Reusing the base table does not remove the logarithmic convolution factor or the repetitions.
- Coordinate medians require an additional ordered-real operation model: deterministic linear selection on each real and imaginary coordinate uses O(RN) exact comparisons and data movements. This was already the aggregator in REPETITION.md, but is not supplied by a pure unordered field-operation count. If sorting is used instead, charge O(NR log R) comparisons. No finite-bit cost for these comparisons is proved.
- A straightforward implementation retains R decoded vectors, using O(RN) aggregate storage plus the original decoder workspace and input/output. Alternatively, retain RK sketch values, process one p residue at a time, and retain RM values for medians of that residue: O(RK+RM+M+K) auxiliary scalar storage, plus N output if not streamed. The shared-table shift by Kb preserves p, so this batching is valid. No O(M+K) total-memory claim for R exact medians is made.
- Suitable roots and exact scalar operations are the original assumptions. Root/field discovery, algebraic-number encoding, order-comparison bit cost, long-recurrence stability, near-zero geometric divisions, finite-precision robustness, and production speed remain unproved.

Substituting (9) gives the certified arithmetic budget

O( N log(2K) max{1, log(N/delta)/log(1/(4p_*))} ).

For flat input at fixed 0<epsilon<1 using L_M, the denominator is log(K epsilon^2/(8L_M^2)), smaller than log K wherever positive. The chosen sufficient repetition budget therefore does not certify sub-N log N work. This is a statement about this guarantee and implementation, not a universal arithmetic lower bound. A genuinely joint multiseed decoder that bypasses the per-repeat convolution charge remains open.

## 7. Verification status and owner conditions remaining

The analytic proof is all-size within the stated prime/nonzero-a, K<=M, fixed-input, independent fresh-(b,d) conditions. Independently authored narrow exact cyclotomic controls in controls.py check the mean, variance identity, alias simplification, interpolation, and two guard failures. They are controls, not a proof of numerical stability, a large-N benchmark, or an execution of supplied research programs. CONTROL_RESULTS.json records the exact coverage and outcomes.

This candidate closes only the proposed bounded question: can the original repeated-median method reuse a fixed nonzero quadratic coefficient, with an explicit full-output error bound and complete implementation charge? Pending independent verification, the answer is yes under (7), with the stated harmonic penalty.

ALG-031 stays open. This result does not settle:

- Stability and finite-precision evaluation of the accepted exact decoder, including long recurrences and near-zero geometric quotients.
- Bit complexity, root/field construction, and exact real comparison representation/cost.
- A stronger concentration result removing the harmonic penalty at all bins, an arbitrary-input small-repeat theorem, or a dyadic analogue.
- Shared b or d schemes outside the proved fresh-pair regime, unrestricted multiseed dependence, or an asymptotically faster joint decoder/aggregation method.
- Any separate native source-comparison obligation, historical priority, production implementation, or whole-owner completion determination.

No status, priority, novelty label, historical scope, adjacent owner, table entry, repository, or external file was changed.
