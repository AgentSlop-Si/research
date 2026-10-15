# Independent Phase24 sorting rank audit

## Result and scope

The exact rank identity, random-binary rank distribution, and simultaneous all-stride probability bound in the uploaded Phase24 theorem are valid in their stated models. One boundary corollary needs correction: a mixed word with exactly one internal transition has no changed successor edges and no nontrivial defect cycle. The source rank formula itself already gives the correct zero rank.

These results concern stable sorting of iid fair binary words and correction ranks of a particular permutation-conjugated cyclic shift. They neither establish a new arbitrary-input Fourier algorithm nor prove an unrestricted Fourier lower bound. Rank is not a complete computational-cost measure.

The independently authored standard-library checker is `independent_rank_checks.py`; its exact results are in `CHECK_RESULTS.json`. No uploaded source program was run or imported.

## Conventions and universal identity

For N coordinates, Z e_j=e_(j+1 mod N). If L lists their new cyclic order, W e_(L[k])=e_(L[k+1 mod N]). For any stride a, multiplying W−Z^a on the left by Z^(−a) preserves rank and gives V−I, where V is a permutation. The equation Vv=v imposes one freely chosen constant per permutation cycle. Thus, over every field, including characteristic two and fields whose characteristic divides a cycle length,

rank(W−Z^a)=N−number_of_cycles(Z^(−a)W).

Let m_a be the number of matching columns W e_j=Z^a e_j. Those are exactly the one-cycles of V. Every other cycle has at least two coordinates, so rank(W−Z^a)≥(N−m_a)/2. A seen-array permutation validator followed by a cycle scan computes the rank in O(N) elementary field-free operations for one given stride. Computing every stride independently costs O(N²); the probability theorem below is not an O(N) all-stride screening algorithm.

## Stable binary sorting and corrected exceptional case

Let L list zero positions in their original order, followed by one positions in their original order. Let T be the number of transitions between neighboring bits in the noncyclic list. Then

r=rank(W−Z)=2 floor(T/2).

Here is the complete cycle description. If T=0 or T=1, W=Z and every cycle of Z^(−1)W has length one. If T≥2 is odd, the T transition positions form one nontrivial cycle. If T≥2 is even, the T transition positions together with N−1 form one nontrivial cycle. All other coordinates are fixed. Consequently, with s the number of changed successor edges,

- s=0 when T≤1;
- s=r+1 when T≥2.

For example, x=(0,1), L=(0,1), and W=Z. It is a mixed word, but r=s=0; it has no nontrivial defect cycle. Every mixed two-run word gives the same correction to the source's broad statement. The proof's odd-T argument produces a cycle of length T=1 in this case, which is a fixed point, not a nontrivial cycle.

This is a local correction to the support/nontrivial-cycle wording. It does not invalidate the principal rank formula, the distribution, or the random-input obstruction.

## Exact distribution and useful coverage consequence

For iid fair bits, the map from the word to its first bit and N−1 successive XOR differences is a bijection. Thus T is Binomial(N−1,1/2). For r=2k,

Pr(r=2k)=2^(1−N) [binom(N−1,2k)+binom(N−1,2k+1)]
         =2^(1−N) binom(N,2k+1).

Odd ranks have zero probability. For N≥3, E[r]=N/2−1 and Var(r)=N/4. To see the moment identities without relying on experiments, write r=T−I, where I indicates odd T. With m=N−1≥2, E[T]=m/2, Var(T)=m/4, E[I]=1/2, and E[T(−1)^T]=0, hence Cov(T,I)=0. Therefore E[r]=(m−1)/2 and Var(r)=(m+1)/4. At N=2 the rank is identically zero; the source properly states the variance formula only for N≥3.

The corrected zero-edge event has exactly 2N words, so

Pr(s=0)=N/2^(N−1).

For k≥1, Pr(s=2k+1)=2^(1−N) binom(N,2k+1). In particular E[s]=N/2−N/2^(N−1). These are independent corollaries of the validated distribution and corrected exceptional case.

More generally, for fixed k,

Pr(r≤2k)=2^(1−N) sum_(j=0)^k binom(N,2j+1).

Only O(N^(2k+1)) of the 2^N binary words have bounded rank at this reference shift. This quantifies the restricted coverage of constant-rank sorting repairs. It does not rule out exploiting some other fast structure in a high-rank correction.

## All-stride probability theorem

The source correctly treats a=1 separately and addresses all a=1,…,N−1, without requiring coprimality. Apart from at most two bridges joining the two color lists, a stable-sorted successor matching j↦j+a requires a nonwrapping binary substring with equal endpoints and all interior bits opposite. Let Q_a count such substrings. Then m_a≤Q_a+2 and E[Q_a]=(N−a)/2^a.

For a=1 the equality indicators are independent fair bits, and Hoeffding yields a failure bound exp(−N/32) for deviation N/8. For 2≤a≤A, split starting positions modulo a+1. Within a class the windows are disjoint and independent. If the total exceeds its mean by N/4, one class exceeds its mean by N/[4(a+1)]. There are a+1 classes, each of size at most 2N/(a+1). Hoeffding bounds the failure probability by (a+1) exp(−N/[16(a+1)]). For a>A, the first-moment union bound is at most N 2^(−A).

Take A=min(N−1,ceil(3 log2 N)). Outside the union of those events, m_a≤3N/4 for every a when N≥16, and hence rank(W−Z^a)≥N/8. Summing the short-stride bounds conservatively gives exactly the source guarantee:

Pr(all strides have rank at least N/8)
≥max(0,1−exp(−N/32)−A(A+1)exp(−N/[16(A+1)])−N 2^(−A)).

The bound tends to one and equals approximately 0.9956931798864608 at N=8192. It is zero after clipping at N=4096 and at several smaller tested sizes. Random tests at those sizes cannot be reported as positive values of this analytic guarantee.

This proves that, with high probability, no choice among the original cyclic powers gives a bounded-rank defect representation of the sorted shift. It does not exclude unrelated sparse reference graphs, independent coordinate orders, noncommuting products, nonlinear algorithms, or fast handling of a linearly growing rank.

## Independent evidence

- All 131,068 binary words for N=2,…,16: exact rank formula, corrected changed-edge formula, full cycle structure, probability counts, and rational moments.
- 16,388 exact word/stride cases for N≤10: matching-substring bound and universal rank/matching inequality.
- 2,154 exact Gaussian-elimination checks: every ordering for N=2,…,5, every stride including zero, and characteristics 2, 3, and 5.
- Six seeded iid-bit samples at each N=32,64,128,256,512: all strides checked. These finite samples are controls, not proofs of the high-probability theorem.
- All 240 mixed one-transition cases across N=2,…,16 confirm the boundary correction.

The source's experimental results remain source-reported. The counts above describe only the independently authored checker.
