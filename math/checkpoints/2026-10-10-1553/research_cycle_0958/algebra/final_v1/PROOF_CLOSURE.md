# Algebra proof closure: arbitrary pencils and even-cycle banks

10 October 2026. Fresh derivation and proof audit. No supplied executable was run. These statements close mathematical proof gaps at their stated scope; they do not certify publication priority. The pre-existing source manuscripts remain unchanged.

## A. Universal arbitrary-matrix diagonal-pencil theorem (C03)

Let S be any commutative ring, m≥1, A,B∈S^{m×m}, D(w)=diag(1,w,…,w^{m−1}), and

P_0(a,w)=det(A−aDAD),  P_1(a,w)=det(B−awDBD).

Use the homogeneous degree-(m,m) Sylvester resultant R(w)=Res_a(P_0,P_1), even if specialized coefficients make actual a-degrees smaller. Set

T=m²(2m−1), v=m(m−1)(4m+1)/6, b=m(m−1)(2m−1)/6.

Then uniquely determined U,V∈S[w],S[x] satisfy

R(w)=w^v(w−1)^{m²}U(w),
w^T R(w^{-1})=(−1)^{m²}R(w),
w^{2b}U(w^{-1})=U(w),
U(w)=w^bV(w+w^{-1}), deg V≤b.

These are polynomial identities obtained by specialization from the universal integer coefficient ring. In rings with zero divisors, uniqueness still follows because the divided factors are monic, and the basis elements w^b(w+w^{-1})^j have distinguishable top degrees. The reciprocal identities are Laurent identities with the displayed grades; neither exact degree nor nonzero resultant is assumed after specialization.

### Complete proof

Work first in Z[A_ij,B_ij]. Entrywise 1−aw^{-e−i−j}=−aw^{-e−i−j}(1−a^{-1}w^{e+i+j}) gives

P_e(a,w^{-1})=(−a)^m w^{-m(e+m−1)}P_e(a^{-1},w).

Reversing two formal degree-m binary forms changes their resultant by (−1)^{m²}; homogeneity in both coefficient lists proves the grade-T reciprocity.

Put w=1+ε and a=1+εt. Every entry of either determinant is divisible by ε. Thus P_e(1+εt,1+ε)=ε^mQ_e(t,ε), with Q_e polynomial and formal t-degree at most m. The degree-(m,m) affine resultant identity gives

ε^{m²}R(1+ε)=ε^{2m²}Res_t(Q_0,Q_1).

Cancel in the universal integral domain. This proves (w−1)^{m²}|R without nonsingularity assumptions.

For the w-factor, pass to the rational function field K=Q(A_ij,B_ij). The coefficient of a^j in P_e is the mixed-minor sum

(−1)^j Σ_{|I|=|J|=j}(−1)^{ΣI+ΣJ}det(M[I,J])det(M[I^c,J^c])w^{ej+ΣI+ΣJ},

where M=A or B. Its unique lowest-weight term has I=J={0,…,j−1}. Its coefficient is a nonzero polynomial (specialize M=I to see this), so its w-valuation is j(j−1)+ej. The lower coefficient polygon therefore has successive slopes e,e+2,…,e+2(m−1). Its root valuations in a are −e−2i, 0≤i<m. Equivalently, for each i substitute a=w^{−e−2i}u: exactly the two consecutive terms i and i+1 have minimum weight, giving a simple nonzero leading u-root; the formal implicit-function theorem lifts it. This proves the stated valuations without a finite-residue-field hypothesis.

The two parity-separated slope sets cannot cancel in root differences. The root-product formula consequently yields

ord_w R=m²(2m−1)−Σ_{i,j}max(2i,2j+1)=Σ_{i,j}min(2i,2j+1)=v.

Therefore every coefficient below w^v vanishes in the universal integer polynomial ring. This is universal divisibility; specializations may raise the valuation or annihilate R. Since w and w−1 are comaximal, the two universal factors divide their product. Polynomial division by their monic product retains integral coefficients.

Removing the factors from reciprocity leaves grade T−2v−m²=2b. Because U is polynomial, this identity also forces deg U≤2b, including when the resultant degree drops. A reciprocal polynomial of grade 2b gives a Laurent polynomial w^{-b}U fixed by w↦w^{-1}. Every such invariant is uniquely an S-linear combination of 1 and w^k+w^{-k}, 1≤k≤b. The recurrence C_0=2, C_1=x, C_{k+1}=xC_k−C_{k−1} expresses w^k+w^{-k}=C_k(w+w^{-1}) without dividing by 2. This remains valid in characteristic 2 and over arbitrary S, proving V and its bound. ∎

### Sharpness and application boundary

At A=B=I, R=∏_{i,j}(w^{2j+1}−w^{2i}) under the usual Res(f,g)=lc(f)^deg(g)∏g(root f) convention. Each difference has unequal exponents, so its w-order is min(2i,2j+1), and its order at w=1 is one in characteristic zero. Hence v and m² are generically exact and deg V=b is attained. The illustrative sign agrees with the source.

Over a field, b+1 evaluations at nonzero w_i≠1 with pairwise distinct x_i=w_i+w_i^{-1} recover V, after division by the known factors. This requires enough admissible nodes in the base field or a paid extension. The map identifies w with w^{-1}; counting w-values instead of distinct quotient nodes is invalid. A zero homogeneous resultant alone never certifies a legal sparse recovery, especially when a leading degree drops.

The arbitrary-matrix extension is thus proved at the same generality as its printed statement. Its mechanism remains classical determinant/resultant/Newton-polygon algebra. No stronger recovery theorem follows automatically.

## B. Uniform even-cycle one-extra-pole theorem (ALG-EVEN-PRONY-EXTRA-POLE, F143)

Let N=2h≥4, q be a primitive Nth root in a characteristic-zero field, and c_j=q^{j(j−1)/2}, 0≤j<N. Over an algebraic closure, there are h≤Q≤h+1 distinct nonzero nodes α_ell, avoiding α_ell^N=−1, and nonzero weights β_ell such that

c_j=Σ_{ell=1}^Q β_ell α_ell^j for every 0≤j<N.

Consequently for a fixed cyclic Weyl shift T with T^N=−I, whose powers I,T,…,T^{N−1} are linearly independent,

Σ_{j=0}^{N−1}c_jT^j=Σ_{ell=1}^Q β_ell(1+α_ell^N)(I−α_ell T)^{-1}.

The lower bound concerns this fixed scalar common-T grammar, not arbitrary inverse matrices.

### Complete proof and finite selection rule

Define L(z^j)=c_j for all j≥0, R_n(z)=∏_{k=0}^{n−1}(z−q^k)=Σ_jr_{n,j}z^j, and

P_n(z)=Σ_j(c_n/c_j)r_{n,j}z^j.

Then P_n is monic, P_n(0)=(−1)^nq^{n(n−1)}≠0, and

L(z^sP_n)=c_sc_nR_n(q^s)=0 for 0≤s<n.

The Hankel determinant is

Δ_n=det[c_{i+j}]_{0≤i,j<n}=q^{n(n−1)(n−2)/2}∏_{d=1}^{n−1}(q^d−1)^{n−d}.

Indeed factor c_i and c_j from its rows and columns, then apply the Vandermonde formula to [q^{ij}]. Δ_n≠0 for n≤h+1, since all differences q^d−1 have 1≤d≤h<N. No positivity is used.

The bilinear orthogonal-polynomial recurrence gives P_{n+1}=(z−a_n)P_n−b_nP_{n−1} for 1≤n<h, with

b_n=Δ_{n+1}Δ_{n−1}/Δ_n²=q^{3n−3}(q^n−1)≠0.

To derive it, expand zP_n in the monic P-basis. Pairing with P_k for k≤n−2 kills those coefficients by L((zP_n)P_k)=L(P_n(zP_k))=0; the nonzero norms Δ_{k+1}/Δ_k permit cancellation. Pairing with P_{n−1} gives b_n. A common root of P_h,P_{h−1} would propagate through this recurrence to P_0=1. Therefore zP_h and P_{h−1} are coprime as well, since P_{h−1}(0)≠0.

Let F=zP_h, G=P_{h−1}, B_t=F+tG. It is monic of degree h+1, and L(z^sB_t)=0 for 0≤s≤h−2. For t≠0 its constant coefficient is nonzero. If B_t has a multiple root α, then G(α)≠0, t=−F(α)/G(α), and W(α)=0 where W=F'G−FG'. W has degree 2h−1 with leading coefficient 2, so at most 2h−1 distinct parameters are bad for squarefreeness. Each of the 2h roots of z^{2h}+1 forbids at most one further parameter; if G vanishes there, F does not, so it forbids none. At most 4h−1 parameters are bad. One integer t∈{1,…,4h} therefore gives squarefree B_t coprime to z^N+1.

For its h+1 roots, solve the nonsingular Vandermonde system matching c_0,…,c_h. Both sequences obey the monic B_t recurrence through index 2h−1: for the original sequence these are exactly the L(z^sB_t)=0 equations. Induction matches every required sample. Remove zero weights. Every representation with Q nodes has Hankel rank at most Q, while Δ_h≠0, proving Q≥h. Finally (I−αT)^{-1}=(1+α^N)^{-1}Σ_{j<N}α^jT^j proves the legal resolvent identity. ∎

This closes the proof of the at-most-h+1 construction. It does not prove that h always suffices, that t=1 always works, or that roots can be prepared or applied in subquadratic time. The field operations, algebraic extensions and root preparation remain charged. The N=2 case is outside the original claim, though it could be checked separately.
