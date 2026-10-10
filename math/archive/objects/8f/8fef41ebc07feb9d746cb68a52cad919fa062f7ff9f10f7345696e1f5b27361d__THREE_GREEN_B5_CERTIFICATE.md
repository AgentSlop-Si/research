# An exact three-Green factorization of the forced N5 chirp matrix

## Result

The forced five-coordinate chirp matrix admits THREE diagonal-ended Hamiltonian-cycle Green summands. Two summands use the same natural structural cycle with reciprocal algebraic closing weights; the third has zero weights on that structural cycle and supplies an explicit diagonal correction. Every endpoint diagonal in this particular construction is nonsingular, and all Green denominators are nonzero.

Let ζ be any primitive complex fifth root, F[i,j]=ζ^(ij), A=diag(ζ^(3j²)), g=1+2(ζ²+ζ³), and

    B=(F^(-1)+A)^(-1),
    B[i,j]=[ζ^(ij)−gζ^(−3(i+j)²)+5gζ^(−3i²)δ_ij]/(1+5g).

The construction is uniform across the four embeddings of Q(ζ); its coefficients lie in an explicitly specified quadratic extension of Q(ζ). Either of the two roots gives valid factors. No numerical fit, dimension-count existence inference, or unrestricted search is used.

Combined with the separately accepted all-order two-Green exclusion, this makes the minimum number of allowed summands at this particular target and size exactly THREE, once the present positive certificate passes its separate independent review. This is a finite-size positive control, not an all-length construction, an O(N) parameter family, a Fourier speedup, or a claim that fixed rational poles are impossible.

## 1. A finite synthesis lemma

The following algebraic reduction explains how the factors were found. Suppose a symmetric five-by-five target has nonzero off-diagonal data

    B01=B04=a,     B02=B03=b,
    B12=B34=c,     B13=B24=e,
    B14=f,        B23=h.

Its five diagonal entries may be arbitrary. Define four normalized constants

    α=c/(ab),     β=e/(ab),     γ=f/a²,     ε=h/b².

Choose a root d of the quadratic

    P(d)=(β²−γε)d²
       +(−2αβ+αγ+αε+βγ+βε−2γε)d
       +(β−γ)².                                      (1)

Define, in order,

    t=[γd+(α+β)d²]/[γ(d+2)−α−β],
    κ=(t+d²)/γ,
    x=(t−d)/κ,
    r1=x,  r2=(α−x)/d,  r3=(β−x)/d,  r4=(γ−x)/d,
    z=κ/(1+t),
    u0=1,          ui=B0i*ri                  (1≤i≤4),
    v0=z/t,        vi=B0i−z*ui                (1≤i≤4). (2)

Required guards are a,b,γ,d,β−γ,γ(d+2)−α−β,κ,t,1+t,1−t all nonzero. The certificate below checks every guard, at both roots and every primitive fifth-root embedding.

Then for every i<j,

    Bij=ui*vj+t*vi*uj.                                (3)

Here is a direct derivation. The four equations with i=0 follow from vj+t*v0*uj=B0j. For i,j≥1, the normalized right side of (3) is

    ri+t*rj−κ*ri*rj.

Since d=t−κx, the three equations with i=1 follow immediately from (2). Also κr4=1+d. Consequently the difference between the normalized (2,4) and (3,4) equations is β−α. The equation at (3,4) reduces to

    t[γ(d+2)−α−β]=γd+(α+β)d²,

which is the definition of t. Thus both (3,4) and (2,4) hold. Finally, the difference between the (2,3) and (2,4) expressions is

    (t−κr2)(β−γ)/d.

Setting it to ε−β and substituting t,κ reduces exactly to P(d)=0 after clearing the nonzero displayed denominators. This proves the remaining equation and hence all ten off-diagonal entries. This is a rational reconstruction from one quadratic, rather than a parameter count.

## 2. Explicit quadratic for the chirp target

Use the basis 1,ζ,ζ²,ζ³ for K=Q(ζ), with ζ⁴=−1−ζ−ζ²−ζ³. Direct reduction of the target entries gives

    α=(18−16ζ−26ζ²−110ζ³)/11,
    β=(34+16ζ−94ζ²−10ζ³)/11,
    γ=(254−848ζ−602ζ²+402ζ³)/121,
    ε=(1102+848ζ+1250ζ²+246ζ³)/121.

The leading coefficient in (1) is nonzero. After dividing by it, the equation is

    d²+p1*d+p0=0,                                    (4)

where

    p1=(−326−3932ζ−2918ζ²−714ζ³)/781,
    p0=(−7096+672ζ+5728ζ²+10576ζ³)/8591.

Its discriminant is the nonzero field element

    p1²−4p0=
    (−7841176−11247008ζ+1606788ζ²+6279476ζ³)/609961.

For an additional irreducibility check, at the prime ζ↦91 in characteristic241, equation (4) reduces to

    d²+30d+124,

whose discriminant is163 and 163^120=−1 modulo241. Thus it is irreducible over F241. The characteristic-zero quadratic is irreducible over K as well: its coefficients are regular at this prime; a root in K of this monic polynomial would be integral at the prime and reduce to a residue-field root. Equivalently, a square root in K of the unit discriminant would reduce to a square root of163. This uses the localization of the cyclotomic integer ring at the given prime, an integrally closed local ring. Hence E=K[d]/(d²+p1d+p0) is a degree-two number-field extension, of degree eight over Q.

The pole simplifies to

    t=1+e*d,
    e=(−49+36ζ+65ζ²−87ζ³)/44.                         (5)

Its conjugate under d↦−p1−d is t^(-1). In particular Norm_(E/K)(t)=1. An equivalent explicit pole polynomial is

    t²+s*t+1=0,
    s=(13996+58170ζ−73235ζ²−211995ζ³)/17182.           (6)

Both roots give the following factorization; there is no arbitrary or approximate root selection.

## 3. The three actual Green plans

Let σ(i)=i+1 modulo5, with row action (Wx)i=wi*x_(σ(i)). Define three weighted Hamiltonian structural cycles:

    W0: weights (1,1,1,1,t),
    W1: weights (1,1,1,1,t^(-1)),
    W2: weights (0,0,0,0,0).

The structural cycle is σ even where weights vanish. For scalar q≠1, let H_q be the matrix with entries1 on/above the natural-order diagonal and q strictly below it. The cycle with weights(1,1,1,1,q) has

    (I−W_q)^(-1)=H_q/(1−q).                          (7)

This identity follows either from the five-step geometric series or by direct multiplication; all 25 entries for each nontrivial branch are checked in the certificate.

Let Du=diag(u), Dv=diag(v), and

    Δ=diag(Bii−(1+t)*ui*vi).

The explicit decomposition is

    B=(1−t)Du (I−W0)^(-1) Dv
      +(t−1)Dv (I−W1)^(-1) Du
      +Δ (I−W2)^(-1) I.                              (8)

By (7), its first two summands are Du H_t Dv and t Dv H_(1/t) Du. Above the diagonal their sum is (3); below the diagonal it is the transpose of (3), and B is symmetric. Their diagonal is (1+t)ui*vi, supplied to the target value by Δ. This proves every entry of (8).

The inverse guards are exactly 1−t≠0, 1−t^(-1)≠0, and1≠0. No matrix inverse of an unknown dense target occurs in factor reconstruction. At fixed N5, the formulas are a finite exact certificate; their existence supplies no asymptotic application claim.

## 4. Exact guards at both roots and all embeddings

In E, conjugation sends d to −p1−d. For y=a+bd,

    Norm_(E/K)(y)=a²−p1*a*b+p0*b².                    (9)

A nonzero norm guarantees that y is nonzero at both roots. A nonzero element of K remains nonzero under every primitive fifth-root embedding. Hence one exact basis calculation proves all requested guards simultaneously.

The recorded guard norms are nonzero, including:

    Norm(d)=p0,
    Norm(t)=1,
    Norm(t−1)=(48360+58170ζ−73235ζ²−211995ζ³)/17182,
    Norm(t+1)=(20368−58170ζ+73235ζ²+211995ζ³)/17182.

`EXACT_THREE_GREEN_RESULTS.json` gives the full four-coordinate rational basis representations of these norms and those of κ and the denominator γ(d+2)−α−β. The base-field divisions by a,b,γ,β−γ and the polynomial leading coefficient are also executed in the exact field. Their nonzero status is checked, and the quadratic constant p0=(β−γ)²/(β²−γε) certifies β−γ≠0.

All fifteen norms of ui,vi and Δii are nonzero as well, with their exact coefficients saved. Thus every endpoint diagonal in (8) is nonsingular, including the diagonal correction branch. The use of a zero-edge Green is permitted by the same grammar as the accepted two-summand exclusion; no unmatched endpoint permutation is introduced.

## 5. Certificate, verification and bounded search cost

The derivation uses a single prescribed natural cycle and the reciprocal-pole ansatz, then solves one quadratic. It performed no nonlinear numerical iteration or enumeration of orders. The exact verifier is newly authored, standard-library Python with rational arithmetic in K and its quadratic extension. It runs in well under one second in this environment; the actual mathematical complexity claim here is only that this fixed-size certificate is finite and explicit.

The verifier independently constructs the target from the given Fourier/chirp entry formula, derives the normalized constants and quadratic, reconstructs endpoints, checks:

- the cyclotomic relation, g²=5, and all50 left/right inverse entries proving that the explicit target is (F^(-1)+A)^(-1);
- all ten upper off-diagonal identities;
- all25 entries of (8);
- all50 entries of the two nontrivial Green inverse identities;
- the irreducible finite reduction, discriminant and every reconstruction/inverse guard;
- all15 endpoint nonzero norms.

The JSON contains the complete target, polynomial, pole, both endpoint vectors, diagonal correction and exact guard data in rational bases. It can be checked without following this derivation. No predecessor or uploaded program is imported or executed. Independent review is separate and must reconstruct these checks rather than treat this report as its own evidence.

## 6. Scope and open directions

This is a concrete escape from the all-order TWO-branch obstruction at N5, using exactly THREE branches. The certificate uses algebraic reciprocal poles, not fixed rational poles. It leaves open whether rational-pole or base-field-only three-branch factors exist, whether a comparable family exists at other lengths, and whether any such family can be generated and applied with an advantageous fully charged asymptotic cost. The infinite TWO-branch exclusion remains valid and is neither contradicted nor enlarged by this finite positive control.
