# Independent audit of the multiscale Weyl-support and dyadic chirp barrier

10 October 2026. Source: `fft_hero17_phase15_multiscale_weyl_chirp_2026-10-10/PROOF_CERTIFICATE.md`, inspected as inert mathematical text. No supplied program executed. Theorem-level verdict: accepted within the literal grammar; no arithmetic-runtime lower bound.

## 1. Fourier inverse Weyl support

Let N≥2, char(K)∤2N, ω primitive Nth root, S e_j=e_(j+1), T e_j=ω^j e_j. The words W_(a,b)=S^aT^b form a basis with twisted multiplication W_(a,b)W_(c,d)=ω^(bc)W_(a+c,b+d). For negative-exponent F_−, its inverse is F_+/N and its Weyl coefficients are G_N(a−b)/N², where

G_N(d)=sum_j ω^(j²+dj).

Direct multiplication with G_N^#(d)=sum_j ω^(−j²−dj), substituting h=j−k, gives

G_N(d)G_N^#(d)=N sum_(h:2h=0 modN) ω^(h²+dh).

For odd N this is N, so every coefficient is nonzero. For even N it is N[1+(−1)^(N/2+d)]. Translation j↦j+N/2 also shows G_N(d)=(−1)^(N/2+d)G_N(d). Since char(K)≠2, the odd-sign case is zero and the even-sign case has nonzero product2N. Thus

supp_W(F_−^−1)=N² for odd N, N²/2 for even N.

This works in the stated finite fields as well as C. Gauss parity and Weyl support are classical.

## 2. Literal sparse-inverse product count

For an invertible literal product M=W0 G1 W1 ... GL WL, suppose each Wj is a nonzero scalar times one Weyl monomial and each Gj^−1 has at most qj Weyl atoms. Inverting reverses the product; distribution generates at most product qj atoms, and cancellations only reduce support. Gauges translate the basis indices and multiply nonzero coefficients. Hence

product qj≥supp_W(M^−1).

For a Fourier target and qj≤3 this gives L≥ceil(log_3(N²)) at odd N or ceil(log_3(N²/2)) at even N. Changing to another invertible monomial Weyl coordinate frame permutes atoms, so support count is invariant under that restricted frame change. It is not invariant under arbitrary dense operator-basis changes.

## 3. Strict dyadic chirp refinement L≥m+1

Let N=2^m≥4, ζ a primitive2Nth root in K, char(K)∤2N, and ω=ζ². Define C[i,j]=ζ^((i−j)²). Even N ensures the chirp kernel is N-periodic. With D=diag(ζ^(j²)),

C=DF_−D,
C^−1=(1/N)D^−1F_+D^−1,
q_t=(C^−1)[t,0]=ζ^(−t²)/N.

All q_t are nonzero. Consider a literal product of L invertible pure-shift resolvents (I−α_j S^(s_j))^−1, with arbitrary strides and scalar weights, permitting nonzero scalar Weyl-monomial gauges between factors. Then L≥m+1.

First omit the gauges. C^−1 is a scalar multiple of a product of L shift binomials, so its support is≤2^L and L≥m. If L=m, every α_j must be nonzero and the2^m subset sums of the strides must be distinct moduloN, since any collision would leave fewer thanN possible shift coefficients.

For t=0,...,m−1, sum a complex character of order2^(t+1) over the complete subset-sum set Z/NZ. It is zero and factors as product_j(1+exp(2πi s_j/2^(t+1))). A factor must vanish, so one stride has2-adic valuation exactlyt. There arem strides andm distinct requirements; their valuations are precisely0,...,m−1. This character argument is combinatorial on integer strides and remains valid even when the representation coefficients lie in another field.

Select strides a,b with valuations0 and1. Unique subset sums mean the coefficients at0,a,b,a+b arise from exactly the empty, singleton, singleton and paired subsets. They must satisfy q0 q_(a+b)=q_a q_b. However the chirp gives

q0 q_(a+b)/(q_a q_b)=ζ^(−2ab)≠1,

because v2(ab)=1<m. This contradicts L=m.

To include interspersed Weyl gauges, use T^b S^s T^−b=ω^(bs) S^s. Move every gauge to the ends, changing only scalar resolvent parameters, to write M=κ S^aT^b R(S) for a circulant R. Since C is a nonzero-entry circulant, equality forces b=0 moduloN: compare entries after simultaneously shifting row and column by one, which multiplies the left monomial modulation byω^b while leaving a circulant unchanged. A net shift translates the inverse chirp coefficients. For a translated chirp q_(t+c), the ratio q_c q_(c+a+b)/(q_(c+a)q_(c+b)) is stillζ^(−2ab); the same contradiction applies. Arbitrary diagonal gauges do not normalize the circulant algebra and are excluded.

Strides0 and zero α need not be separately forbidden: they reduce possible support and so cannot occur in an L=m full-support extremizer. Invertibility is required factor by factor; for a non-generating stride its correct pole guard is based on the order of S^s, not an unexamined generic α^N guard. The theorem uses actual invertibility and remains valid.

There is no proof that m+1 factors suffice.

## 4. Binary reshape rank and positive fusion control

For1≤a<m, write t=u+2^a v. After nonzero row/column scaling, the rectangular array (q_(u+2^a v)) is [(ω^(−2^a v))^u]. Its2^(m−a) nodes are distinct. A leading Vandermonde square of size2^min(a,m−a) proves exactly that rank. Yet q itself can be generated in O(N) field work by updating its successive ratio geometrically. Tensor rank is not generation cost.

The identity

product_(j=0)^(m−1)(I+α^(2^j)S^(2^j))=(1−α^N)(I−αS)^−1

holds whenever α^N≠1, by the binary polynomial factorization. The right side has a linear-work cyclic recurrence even though the left displays m stages. This classical positive control prevents promoting the factor-count theorem to a runtime lower bound. Every setup, root, coefficient, memory/write and precision cost needs a separate computational contract.

## 5. Independent finite controls and novelty boundary

Fresh `multiscale_checks.py` verifies the Gauss-support theorem for N=2,...,25 in independently selected finite fields; direct chirp inverse products and all binary-cut ranks through N=32; all3150 stride multisets in the N=4,8,16 equality cases; and legal binomial fusion at several nonzero/zero scalar parameters. It uses only self-authored standard-library modular arithmetic, no source code or source result JSON.

The proof's strict one-extra-stage equality-case argument is a meaningful specialized refinement of a classical support count. A focused exact-grammar prior-art search is still required. Classical Bluestein, Weyl/Gauss, Vandermonde and binary geometric identities must be credited. No global priority or general exact FFT speedup is claimed.
