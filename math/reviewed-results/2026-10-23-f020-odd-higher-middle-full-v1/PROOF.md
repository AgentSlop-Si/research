# Odd higher-middle completion: outside-cover rational control

23 October 2026 UTC. Author candidate for independent scientific review. No self-acceptance, publication, supplied-program replay, global F020 closure, or algorithmic speed claim.

## 1. Uniform theorem and actual new scope

Let p be any odd prime, c any odd integer with 1<=c<p, k>=2, r>=k+2, s>r, M=p^k, N=p^r, n=2N+cM. For every characteristic-zero primitive p^s-th root q, both original polynomials P_n and H_n are squarefree, and the original algebraic-square kernel is nonzero at every P_n root.

The original definitions remain

P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
H_n(z)=sum_j [n choose j]_q z^j,
w_j=product_(u=1)^j(1-q^u).

All derivatives are ordinary characteristic-zero derivatives, taken before reduction. The immediate neighbor is P_(n-1), not an associated-tail substitute.

This completes the odd-c part of the higher-middle shape n=2p^r+c p^k. Together with the accepted even-c theorem, it would complete this exact shape for every 1<=c<p. It does NOT complete arbitrary degrees, arbitrary digit patterns, odd-composite orders, independent all-A hypotheses, or whole F020/F023. It makes no historical novelty, FFT, bit-cost, or numerical-stability claim.

Inherited credit is retained for (c-1)M k-boundary roots, the exact zero, every successful first-residual/fixed certificate, and all high-order cases with phi(p^s)>C_((n-1)/2), where C_j is the explicitly defined accepted deflation degree bound in the pinned boundary report and frontier. New coverage credit is restricted to the genuinely unexcluded odd-middle residual family, not previously completed orders or the two already certified tail boundary roots in the n=513 example.

## 2. Notation and source inputs

Use an algebraic p-adic embedding, t=q-1, v(t)=1, e=v(p)=(p-1)p^(s-1), V(j)=p^ord_p(j), and W(j)=sum_(u=1)^j V(u). Set

c=2a+1, A=W(M), K=W(N), B_k=k(p-1)p^(k-1)/2,
m=cM, u=(m-1)/2, G=W(u)=aA+B_k,
C=P_(2N), B=P_(2N-1), b0=1-q^(2N), E=K-N/2.

Thus W(m)=2G+M and W(m-1)=2G. The original shifted tail continuants f=f_m^(2N), g=g_m^(2N) give exactly

P_n=fC-b0gB.

For a level ell, write beta_ell=p^floor(ell/2), L_ell=p^ell/beta_ell and rho_ell=beta_ell/2 for even ell, or (2p-1)p^(floor(ell/2)-1)/2 for odd ell. Put rho=rho_r and sigma=rho_k. The corresponding centers are x_b=i(q^(b/2)-q^(-b/2)). The original H disks centered at -q^b and P disks centered at x_b are analytic isometries under z=v0^2, X=v0+v0^-1, near v0=i.

The inherited higher-middle theorem exhausts all n roots by the k-disks, resolves the (c-1)M k-boundary roots, and places the other 2N+M roots in strict k-interiors. The latter are the only roots treated below.

The accepted leading-core proof gives, on all old r-disks,

C:>=K, C':>=K+N/2-p, B:>=E, B':>=E,
C_initial proportional to Z^2+1, B_initial proportional to Z,

where Z=gamma_b Y^L_r and gamma_b is nonzero. All C roots lie in the old r-disks. Outside their union, the leading Newton product N_(2N)(z) uniquely dominates the original H_(2N) expansion. This last stronger statement is explicitly proved in Section 3 of the accepted complete single-leading-digit source, not inferred merely from a root cover.

The same accepted single-leading-digit source, applied with degree m=cM, gives on each k-disk the coefficientwise ordinary H_m derivative initial proportional to M_(c-1)(gamma_b Y^L_k), at weight

D_f=G+M-p.

The off-root transfer to P_m' needs the ordinary chain rule, not just the source's derivative statement at roots. Exactly,

H_m'(v0^2)=v0^(m-2)[(m/2)P_m+(v0-v0^-1)P_m'/2].

The half-W bound proved in Section 3.1 gives weight(P_m)>=W(m)/2=G+M/2 on the full k-disks. Because v(m)=k e, the extra term has weight at least G+M/2+k e>D_f=G+M-p: here e>=(p-1)N and N>=p^2M. The other displayed coordinate factors have nonzero constant residues and are units. Thus the full coefficientwise H derivative initial transfers to the ordinary P derivative OFF its roots as well. Since c-1 is even and c<p, M_(c-1)(0) is nonzero. Consequently P_m' has EXACT value D_f throughout every strict k-interior, not only at P_m roots. The source's root-only P transfer is not silently broadened; the preceding chain-rule estimate is the added argument. These inputs and their exact original/public acceptance bindings are pinned with the recovered source bodies.

The legal degree n<[2+(p-1)/p^2]N<pN<=p^s keeps every factor and denominator below nonzero. Total polynomial weights are not assumed below e.

## 3. Global short-tail estimates on the k-disks

We require estimates on the larger k-disks, not an unauthorized transplant of old r-disk estimates.

### 3.1 Half-W cap and zero-coordinate values

On a k-disk set T_k(j)=sum_(v=1)^j min(V(v),sigma), R_k=W-T_k. For j<pM the accepted digit-linear cap is R_k(j)<=W(j)/2, with equality precisely at multiples of M. The original Newton formula and superadditivity imply, for q and q^-1,

weight(P_j)>=W(j)/2, j<pM.

Indeed each term has weight >=W(j)-R_k(ell)-W((j-ell)/2)>=W(j)/2. Equality requires the Newton index ell to be a multiple of M. Every positive such index has initial divisible by Y^L_k. Thus evaluation of the normalized initial at Y=0 comes only from ell=0: it is zero for odd j, and is the normalized exact P_j(0) for even j, with zero allowed if that constant has larger valuation. These conclusions hold in every disk; all coordinate factors have constant nonzero residue and the ell=0 term is independent of the disk center.

### 3.2 The actual first-deleted tail is a unit in strict k-interiors

For g_m^0 use the exact finite connection

g_m^0=w_m sum_(ell=1)^m (-1)^(ell-1)q^(ell(ell-1)/2) P_(m-ell)(q)P_(ell-1)(q^-1)/[w_(m-ell)w_(ell-1)(1-q^ell)].

Since m=cM with c<p, endpoint reflection gives

W(m-ell)+W(ell-1)=W(m-1)=2G.

Using the half-W bounds, every term has weight at least

W(m)-G-V(ell)=G+M-V(ell)>=G.

Equality requires ell=bM, 1<=b<=c. At Y=0 the even-b terms vanish because both polynomial indices are odd. The odd-b terms have even indices. Their constants attain their half-W weights: the first index is an even multiple of M and the second is bM-1 with b odd, both having carry-free halves.

Consequently the value at Y=0 of the weight-G initial is exactly the normalized value of the exact constant

g_m^0(0)=(-1)^u Q_u, Q_u=product_(j=1)^u(1-q^(2j)),

which has valuation G. This proves that initial is nonzero at Y=0, not that it is globally constant. Thus g_m^0 has exact value G on every strict k-interior, and coefficientwise weight>=G on the full k-disks. Ordinary Gauss differentiation gives weight((g_m^0)')>=G-sigma.

### 3.3 Shift error on the correct, larger disks

Let eta=product_(j=1)^m(1-q^(2N+j))/w_m, a scalar unit with v(eta-1)>=N-M. The finite f connection gives f=eta P_m+Delta_f. For d>0 its extra ratio (1-q^(2N))/(1-q^(2N+d)) has value N-V(d). The half-W bounds and W(m-d)+W(d)<=W(m) yield

weight(Delta_f)>=W(m)/2+N-M=G+N-M/2,
weight(Delta_f')>=G+N-M/2-sigma.

These are coefficientwise bounds on the full k-disks, so the derivative estimate is the legitimate ordinary Gauss inequality, not differentiation of a mere pointwise small error.

Similarly g=eta g_m^0+Delta_g. The reciprocal difference in its exact finite connection has value N-2V(ell), and endpoint reflection gives

weight(Delta_g)>=G+N-M,
weight(Delta_g')>=G+N-M-sigma.

Because N>=p^2M and sigma<M, the f derivative error is strictly above D_f=G+M-p. The g error has strictly positive relative weight. Hence on EVERY strict k-interior,

v(f')=D_f, v(g)=G,

and on every full k-disk weight(g')>=G-sigma. This includes c=1, p=3, both parities of k and r, and all outer shifts. No discarded internal M-block endpoint or unit cancellation is concealed.

## 4. Completion inside the old closed r-disks

For completeness, the new boundary and closed-disk arguments are restated, with their full derivations pinned as dependencies. On each old r-disk the stronger deep-cap tail bounds are

f>=G+M, f' exact D_f, g exact G, g'>=G-(p-1).

At a boundary root, B has exact E. The root identity implies f and C are nonzero. Put delta=v(f)-G>=M and gamma=v(C)-K>=0. Then delta+gamma=N/2. In

P_n'=f'C+fC'-b0g'B-b0gB',

the first term is exact K+D_f+gamma. The three other lower gaps are 2delta-M, delta-M+1, delta-M+p, all positive. A common short-tail/core residual root causes no exception: the actual amplitudes, rather than an inverse of a vanishing residual, determine these gaps.

In a strict old r-interior, C has exact K. Then f'C is exact K+D_f. The other three lower gaps are N/2, N/2-M+1, N/2-M+p, again positive. This direct argument includes f=B=0, without dividing by either. Every root in the old closed r-disks is therefore simple, with

v(P_n')=D_f+v(C).

## 5. A nearest-center ratio bound outside the old cover

Take a point in a strict k-interior but outside every old closed r-disk. In the H coordinate put

tau=max_(0<=b<2N) v(z+q^b).

It satisfies sigma<tau<rho. Using representatives modulo beta_r gives the same maximum: shifts by beta_r have valuation beta_r>rho. Ties for the closest center are permitted.

Fix a maximizing center a. Ultrametricity and maximality imply for all b in the range

v(z+q^b)=min(tau,V(b-a)),

with the a term interpreted as tau. If V(b-a)=tau, a larger value would contradict maximality, so there is no unaccounted cancellation at a tied level. For any consecutive string of 2h+1 indices, capped residue counting gives

sum_string v(z+q^b)<=tau+T_r(2h),

where T_r(j)=sum_(v=1)^j min(V(v),rho). Here is an explicit interval proof. Choose a member of this interval where v(z+q^b) is maximal, of value tau0<=tau. The distances for a left or right offset d are at most min(tau0,V(d)); equality at a tied level cannot increase beyond tau0 by the maximal choice. If the left and right lengths are h1,h2 with h1+h2=2h, their sums are bounded by T_r(h1)+T_r(h2)<=T_r(2h). The last inequality is superadditivity of the cap sum, immediate from its positive floor coefficients. Add tau0<=tau. This covers arbitrary endpoint alignments, multiple maximizing centers, and exact p-power tau values.

Outside this cover v(H_(2N))=v(N_(2N)). This also follows directly without a Newton noncancellation inference: H_(2N) is monic and has exactly 2L_r roots in each old H disk, whereas N_(2N) has exactly 2L_r center factors in each such disk. At an outside point, its distance to any root or center in a fixed old disk is its distance to that disk's representative. The monic products therefore have equal valuations. The accepted unique-leading-Newton statement is a compatible, stronger route, not an additional assumption. For the term j=2N-1-2h in the original H_(2N-1) Newton expansion, endpoint reflection gives W(2N-1)-W(j)=W(2h). Dividing that TERM by N_(2N), its value is at least

W(2h)-W(h)-tau-T_r(2h)=R_r(2h)-W(h)-tau.

Now the half-W cap and superadditivity show R_r(j)+W(h)<=E. Reflection for j+2h=2N-1 gives

R_r(j)+R_r(2h)=R_r(2N-1)=K-N+rho.

Subtracting yields W(h)-R_r(2h)<=N/2-rho. Therefore every term, and hence the original sum, satisfies

v(H_(2N-1)/H_(2N))>=-N/2+rho-tau.

The exact original coordinate formula gives B/C=v0 H_(2N-1)/H_(2N). On the branch v0 near i, v0 is an analytic unit and z(X) has unit ordinary derivative. Thus these coefficientwise valuations transfer to X disks without changing their bounds. All derivatives in Sections 6–8 are ordinary derivatives with respect to X, not z-derivatives silently relabeled and not q-derivatives. Hence finally

v(B/C)>=L0=-N/2+rho-tau.                         (5.1)

This is an actual-family inequality, not a finite residual test or an assumed noncancellation of B.

## 6. Ordinary derivative bounds for the outside ratio

Consider the radius-rho disk centered at the chosen OUTSIDE point X. Every point in this small disk has exactly the same distances to the old centers, because those distances have values <=tau<rho. It remains inside the same strict k-interior and outside the old cover.

Every C root lies in an old disk at distance value at least rho from its own center. Hence the distance from our point to each C root equals the distance to that center and has value <=tau. C is therefore an analytic unit on the radius-rho disk. Its monic factorization gives, coefficientwise there,

weight(C'/C)>=-tau.

The proof of (5.1) is coefficientwise on this entire disk: all factors z+q^b have constant normalized initials, and both monic core products have constant valuations by the disk root cover. The analytic isometry z=z(X), together with the unit v0 in B/C, preserves these Gauss lower bounds. Thus R=B/C is analytic with Gauss weight>=L0. Ordinary differentiation on this disk gives

weight(R')>=L0-rho=-N/2-tau.

The exact identity B'/C=R'+R C'/C then gives

weight(B'/C)>=-N/2-tau,                         (6.1)

because the other summand has bound -N/2+rho-2tau, which is strictly larger. There is no limiting-radius argument, no differentiation after reduction, and no assumption that B is nonzero.

## 7. The last outside roots have a uniquely least derivative term

At any P_n root in this outside region, the exact root identity f=b0g(B/C) and (5.1) give

v(f)>=G+N/2+rho-tau.

This remains true when f=B=0; no division by either occurs. Since C is a unit and f' has exact value D_f, f'C is nonzero with exact value v(C)+D_f.

Divide the competing derivative terms by C only, which is legal. Their lower gaps over D_f are

f C'/C: N/2-M+p+rho-2tau;
b0 g' B/C: N/2-M+p+rho-tau-sigma;
b0 g B'/C: N/2-M+p-tau.

All are strictly positive. Indeed tau<rho, sigma<rho, M<=N/p^2 and rho<N/p imply

M+rho < N(1/p^2+1/p) <=4N/9 <N/2.

Thus f'C is uniquely least and P_n' is nonzero. Its exact value is again

v(P_n')=D_f+v(C).

This settles every previously remaining outside root at once; no finer tail-root geometry, isolated numeric slice, or unproved root-separation radius is needed.

## 8. Exact original neighbor/kernel and root exhaustion

On every strict k-interior g has exact nonzero value G. The positively oriented exact determinant is

g_m^(2N)P_(n-1)-g_(m-1)^(2N)P_n
 = product_(j=1)^(m-1)(1-q^(2N+j)) C.

At a P_n root, C is nonzero. Outside the old cover it is an analytic unit; inside, C=0 would force B=0 through the transfer, contradicting consecutive coprimality. Since the scalar product has value 2G, the actual immediate neighbor has exact value

v(P_(n-1))=G+v(C).

With W(n-1)=2K+2G, the unchanged original CD identity yields, for every strict k-interior root,

v(kernel)=M-p+2(v(C)-K).

This quantity may be negative outside the old cover; it is finite, which is the needed nonvanishing assertion. No positivity claim is made.

The inherited (c-1)M k-boundary roots are already simple. Every other root lies in a strict k-interior, and the inside/outside old-cover partition is exhaustive. Sections 4 and 7 settle both parts, including zero. Counts sum to n without identifying any hidden leftover class.

Modulo the maximal ideal P_n reduces to X^n, so no root is +/-2. H_n(0)=1. The exact unit H/P coordinate identity transfers simplicity and ordinary root-derivative values; algebraic p-adic embedding and injectivity establish the result for every characteristic-zero primitive phase. No auxiliary finite-field phase is used for that logical transfer.

## 9. Evidence, exact costs, and scope limits

The proof uses original finite identities, digitwise inequalities and analytic Gauss norms. It does not require locating individual tail roots, factoring an unknown polynomial, evaluating a characteristic-zero gcd, or computing v(C) at a root in order to decide nonvanishing.

For finite transcription controls, V,W and interval sums through 2N can be computed by a sieve and prefix sums in O(N) arithmetic operations and O(N) storage; direct repeated divisions cost O(N log_p N). Enumerating all short-tail derivative minima by least eligible d costs O(m log_p m). Checking all core numerator indices at each selected center/radius costs O(N) per center/radius after prefix preparation. None of these arithmetic-operation counts includes the bit complexity of exact coefficient fields, high cyclotomic precision, algebraic root representation or gamma=v(C)-K. A naive recurrence construction of the original degree-n polynomial takes O(n^2) coefficient-field operations and O(n) live coefficients. No asymptotic improvement is claimed.

Fresh normal/-O controls are byte-identical and pass 3,314,302 explicit checks: 44 short-tail parameter fixtures, six full outside-core center/radius fixtures, and cap-splitting controls. They test exact bounds and score transcription; the separately pinned boundary controls cover the finite associated, transfer, derivative and original-neighbor identities. They are falsification/transcription controls; the all-parameter proof is Sections 3-8. No historical supplied scientific code is executed or imported. Source manifests preserve inherited acceptance rather than confusing recovered public bytes with original bytes. This packet is a scientific candidate, not authority to publish itself or update a table.
