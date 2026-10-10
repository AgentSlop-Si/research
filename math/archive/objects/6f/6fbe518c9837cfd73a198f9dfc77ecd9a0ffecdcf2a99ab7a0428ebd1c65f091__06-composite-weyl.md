# Fixed-pair Weyl–Green branch bounds at every odd length

10 October 2026. New supported extension of F014 within its literal representation grammar. This proves no arithmetic-circuit lower bound and certifies no worldwide priority. The proof uses classical Weyl coordinates, Gauss sums and Hankel/Vandermonde rank. The new implication is the composite-length arithmetic combination, particularly the uniform half-length bound for odd prime powers.

## 1. Complete statement

Let N≥3 be odd. Let K be a field containing a primitive Nth root ω, with char(K) not dividing N. This includes C and suitable finite fields. All divisions in exponents are in Z/NZ. Define S e_j=e_(j+1), T e_j=ω^j e_j and F[i,j]=ω^(ij). Fix one ordered pair

U=S^uT^v, V=S^rT^s,

where D=us−vr is a unit modulo N. The same U,V are used in every branch. A permitted branch is

c (I−αU)^−1 (I−βV)^−1,

where c,α,β lie in K or a common extension field and α^N≠1, β^N≠1. Zero c,α,β are allowed. No additional branch-dependent Weyl monomial endpoints are allowed in this theorem. Let b be the number of branches in a sum equal to F.

Put A=u²+v², B=r²+s², h=ur+vs, δ=(D−h)/2, and m=(N+1)/2, all residue-dependent gcds interpreted with N. Then

b ≥ max{N/gcd(N,δ), min(m,N/gcd(N,A)), min(m,N/gcd(N,B))}.       (1)

Consequences:

1. For every odd N, b≥ceil(sqrt N).
2. For every odd prime power N, b≥(N+1)/2.
3. If δ is a unit modulo N, b≥N.
4. If δ=0 modulo N, b≥(N+1)/2 for every odd N, including mixed composites.

Equation (1) may be stronger than these summaries. Its minimum at N=15 can be 5, so it does not prove a half-length bound for all mixed composites. These are lower bounds only; no matching construction or optimality claim is made.

## 2. Weyl coefficient identity, including the phase conventions

The N² operators S^aT^b form a basis. Extract coefficients by

C_X[a,b]=(1/N) sum_t ω^(−bt) X[t+a,t].

Completing the square in C_F gives

C_F[a,b]=Γ ω^(−(a−b)²/4), Γ=(1/N) sum_t ω^(t²).

The change of variables (t,s)↦(t−s,t+s) is a bijection on (Z/NZ)², so character orthogonality proves

(sum_t ω^(t²))(sum_s ω^(−s²))=N.

Thus Γ is nonzero in every allowed characteristic; no complex positivity is used.

The actual ordered word phase is

U^iV^j = ω^[uv i(i−1)/2 + rs j(j−1)/2 + vr ij]
          S^(ui+rj) T^(vi+sj).

The coordinate map (i,j)↦(ui+rj,vi+sj) is bijective because D is a unit. Dividing the canonical coefficient by this word phase yields

C'_F[i,j]=Γ ω^[−A i²/4 + uv i/2 −B j²/4 + rs j/2 + δij].       (2)

For example, the mixed coefficient is

−(u−v)(r−s)/2−vr=(us−vr−ur−vs)/2=δ,

which fixes the sign and operator order. The i² coefficient is

−(u−v)²/4−uv/2=−(u²+v²)/4,

and similarly for j².

Odd N ensures U^N=V^N=I: the monomial phase contains N(N−1)/2, divisible by N. Each legal branch consequently has ordered coefficients

c α^i β^j / [(1−α^N)(1−β^N)], 0≤i,j<N.       (3)

Use 0^0=1 at zero parameters. Each coefficient matrix in (3) has rank at most one.

After nonzero row and column scaling, (2) is [ω^(δij)]. It has exactly dδ=N/gcd(N,δ) distinct rows. Its first dδ-by-dδ block is a nonsingular Vandermonde matrix, so rank C'_F=dδ. Subadditivity gives b≥dδ.

## 3. Nonwrapping Hankel ranks at composite lengths

At j=0, equation (2) gives the chirp f_i=Γω^(−A i²/4+uv i/2). Form the m-by-m matrix H[a,b]=f_(a+b), 0≤a,b<m. Since 2m−2=N−1, no index is reduced modulo N.

Factoring the individual a and b phases leaves [ω^(−Aab/2)]. Its root order is dA=N/gcd(N,A). Repeated rows give rank≤dA; a leading square Vandermonde block of size min(m,dA) gives equality. Hence rank H=min(m,dA), in any allowed field.

Each permitted branch restricted to j=0 is a geometric sequence κ α^i, whose nonwrapping Hankel matrix is an outer product, even when α=0. Thus b≥min(m,dA). Reversing the two coefficient axes gives b≥min(m,dB). This proves (1).

The absence of extra Weyl endpoints matters here: a cyclically shifted geometric sequence need not have Hankel rank one. The separately established canonical-pair b≥N bound does allow Weyl monomial endpoints, because its full coefficient-rank argument does not use this Hankel premise. Those are different grammars.

## 4. Arithmetic combination

The elementary identity AB=h²+D² holds modulo N. If an odd prime ℓ divides both N and δ, then h≡D mod ℓ and AB≡2D² mod ℓ is nonzero. Therefore neither A nor B is divisible by ℓ. In particular

gcd(gcd(N,δ),gcd(N,A))=1.

Both gcds divide N, so their product is at most N. Consequently dδ dA≥N. Since m≥sqrt N for N≥3,

max(dδ,min(m,dA))≥sqrt N.

The integer count b is therefore at least ceil(sqrt N).

If N is a power of a single odd prime, the two coprime gcds cannot both exceed one. If gcd(N,δ)=1 then dδ=N. Otherwise gcd(N,A)=1, so min(m,dA)=m. This proves the prime-power bound.

When δ=0, every prime divisor of N divides δ, so gcd(N,A)=gcd(N,B)=1 and the same Hankel argument gives m.

## 5. Independent checks and limits

The freshly authored `fresh_checks.py` reconstructs 77 rotated bases by actual monomial actions at N=3,5,7,9,15,21,25,27,33,35,45. It checks all 45,661 coefficient entries against (2), computes the full coefficient rank, and computes both Hankel ranks over independently selected exact finite fields. It does not import or run any supplied research program.

A separate reviewer independently checked all 934,272 invertible direction tuples for odd N=3 through 25, verifying the gcd combination and the prime-power corollary. Finite controls supplement the above proof.

Changing generators between branches, reversing a branch order, adding arbitrary diagonal gauges, or allowing deeper paths is outside this theorem. A reverse-order two-Green path can have full canonical Weyl coefficient rank while applying in O(N) field work. Branch count is therefore not automatically evaluation complexity. Roots, coefficients, field extension construction, precision and shared evaluation remain separately charged algorithmic questions.

## 6. Primary comparison

- Gurevich–Hadani–Howe, *Quadratic reciprocity and the sign of the Gauss sum via the finite Weil representation*, https://arxiv.org/abs/0808.2447: the established Fourier/Weil/Gauss framework. Our all-odd residue calculation is supplied explicitly instead of asserting their precise prime-field theorem covers every composite.
- Plonka–Tasche, *Prony Methods for Recovery of Structured Functions*, https://num.math.uni-goettingen.de/plonka/pdfs/gamm-preprint.pdf, §2, especially the Hankel factorization around equations (7)–(8): geometric exponential sums have the classical Hankel/Vandermonde factorization. That mechanism is not new.
- The inherited F014 proof already supplies (2), mixed-coordinate rank, and the prime-length fixed-pair theorem. The new-to-project assertion is (1) with the gcd argument, prime-power consequence and field-explicit proof. A complete specialist prior-art search remains required before any publication priority claim.
