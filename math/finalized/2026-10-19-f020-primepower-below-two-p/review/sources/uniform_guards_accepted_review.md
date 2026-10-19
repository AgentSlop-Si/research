# Independent review: F020 uniform odd-order node theorem

18 October 2026 UTC. Independent review of the frozen author candidate with manifest SHA-256 `291b57db309bfb44cf8f056f9c7677e5375e59026dcb1e14cfd1fc20e33bd1ca` and report SHA-256 `0635b3ce3d9cfffd13ef108cf4d1423ed0f3b007d29cbc5dce07cf8c3b53eebe`.

## Verdict

**ACCEPT, within the stated mathematical scope.** No blocking correction was found. This acceptance is independent of the author proof and author controls, and applies to the exact frozen bytes identified above.

For every odd integer d >= 3, every primitive dth root omega, and 0 <= b < d, the candidate proves:

1. gcd(U_b, 1+z^d) = 1, where U_b = H_b for even b and U_b = H_b/(z+1) for odd b.
2. For odd b, H_b'(-1;omega) != 0.
3. gcd(H_b, z^d-1) = 1; in particular H_b(1;omega) != 0.
4. As polynomials in q, D_b = Disc_z(H_b) and the accepted integral deflation V_b are monic, of degrees b(b^2-1)/3 and b(b-1)(2b-1)/6 respectively. The b=0,1 convention gives D_b=V_b=1.
5. Therefore V_b mod p is nonzero for every prime p and its (q-1)-adic order t_p(b) is finite.

The ordinary squarefreeness theorem for unrestricted b<p^s is **not established**. The candidate correctly identifies a precise equivalent nonisotropy lemma, and correctly shows that the proposed universal strict finite-t bound fails. This review does not close F020, change its priority, extend the all-A theorem automatically, revise a census, or settle a separate endpoint or paired-support obligation. No external write was performed.

The unlimited conclusions above rest on the algebraic proofs reviewed below, not on finite controls. Independent fresh controls passed 177 assertions; the inspected author checker also passed all 82 assertions when replayed unchanged in a separate directory.

## 1. Integer-lattice transformation and parity starts

The q-difference identity is correct. Direct coefficient comparison gives

    (1-q^k) [b choose k]_q = (1-q^(b-k+1)) [b choose k-1]_q.

At q=exp(i theta), theta=2 pi/d, substitution z=-q^j yields

    f_(j+1) = (1+q^j) f_j - q^(b+j) f_(j-1).

Write a(j)=bj/2+j^2/4 and y_j=exp(-i theta a(j))f_j. The two rotation exponents satisfy

    a(j)-a(j+1)+j/2 = -(2b+1)/4,
    b+j+a(j-1)-a(j+1) = 0.

Thus the claimed equation y_(j+1)=lambda c_j y_j-y_(j-1) follows exactly, with c_j=cos(pi j/d) and lambda=2 exp(-i pi(2b+1)/(2d)). Its phase lies strictly between -pi and 0 for every allowed b, including b=0 and b=d-1. Therefore lambda is never real. Fractional powers are defined by explicit exponentials, so the proof has no branch-choice ambiguity.

The parity starts are correct. For even b=2r, both H_b(-1) and H_b(-q) equal E_r=product_(a=1)^r(1-q^(2a-1)). For odd b=2r+1, H_b(-1)=0 and H_b(-q)=E_(r+1). All factors have exponent strictly between 0 and d and are nonzero.

For even b the normalized sequence starts M_0=1, M_1=X and has the first off-diagonal parameter 2/c_1. Later parameters are 1/(c_j c_(j-1)). The special first coefficient is necessary and is correctly retained in the candidate. For odd b one instead starts with y_0=0, y_1!=0 and normalizes the shifted sequence; its parameters are again positive reciprocal products of consecutive cosines. At the largest needed integer index j=h=(d-1)/2 all used cosines are positive. The smallest order d=3 needs no unavailable later coefficient.

Each normalized polynomial is the characteristic polynomial of a real symmetric tridiagonal Jacobi matrix with positive off-diagonal squares, hence all its zeros are real. Evaluation at nonreal lambda therefore cannot vanish. Reciprocity gives f_(-j)=(-1)^b q^(-bj)f_j; indices -h,...,h cover every residue modulo d. This proves separation from every negative dth-root node except the known odd root -1. The argument is genuinely uniform in d and b.

## 2. Forced odd root

Differentiation of the Rogers-Szego recurrence at z=-1 gives

    g_r=E_r+(1-q^(2r))g_(r-1), g_0=1.

The expanded formula in the candidate follows by division and iteration. Each factor (1-q^(2a))/(1-q^(2a-1)) is a positive real multiple of exp(i pi/d), because both sine arguments lie strictly between 0 and pi. All product terms in g_r/E_r therefore have argument in [0,r pi/d], a subset of [0,pi/2). Their real parts are positive; the sum cannot vanish. The empty-product case r=0 is included.

Consequently U_b(-1)=H_b'(-1)!=0 for odd b. Combining this with integer-lattice separation proves gcd(U_b,1+z^d)=1. The node polynomial itself is squarefree in characteristic zero, so the asserted gcd conclusion has no unresolved multiplicity issue.

## 3. Half-integer lattice and H_b(1)

The identity H_b(r;r^2)=product_(a=1)^b(1+r^a) follows directly from the three-term recurrence. Taking r=-exp(i pi/d) gives r^2=q and r^d=1, since d is odd. An odd-order root of unity cannot have a power equal to -1, so the product is nonzero. This supplies the nonzero start f_(1/2).

Rotated reciprocity gives y_(-1/2)=(-1)^b y_(1/2), with no residual phase. The shifted spectral polynomials consequently begin

    T_0=1, T_1=c_(1/2) X-(-1)^b.

After monic normalization the first diagonal is the real number (-1)^b/c_(1/2); subsequent diagonals are zero. The off-diagonal squares are 1/(c_(m+1/2)c_(m-1/2)), all positive within the range used. To reach y_(d/2), the largest cosine index actually needed is h-1/2, not d/2. Thus the vanishing of cos(pi/2) does not enter a denominator or recurrence step.

The real-Jacobi argument applies through m=h and proves nonvanishing on the positive half-lattice. Reciprocity supplies the negative half-lattice. The 2h+2 listed points cover all d roots of z^d=1, with the endpoint z=1 duplicated. Hence all these nodes are excluded, including H_b(1)!=0. This is a substantive proof of the extra endpoint claim, not an inference from integer-lattice separation.

## 4. All primitive embeddings

Only the principal embedding needs positivity. H_b and U_b have coefficients in Q(q); their relevant resultants with z^d+1 or z^d-1, and H_b'(-1), are algebraic elements in that field. A field automorphism q -> q^a for gcd(a,d)=1 preserves nonzero elements and takes these polynomials to the corresponding primitive embedding. Thus all conclusions transfer correctly. The candidate does not attempt to transfer real positivity to other embeddings.

One may use the resultant formulation to avoid any question about half-integer notation under field automorphisms. The nonzero resultant Res(H_b,z^d-1) has coefficients in Q(q) regardless of the exponential notation used to prove its nonvanishing.

## 5. Ordinary-discriminant monicity

The Newton/Hensel proof is valid. The coefficient of z^k is monic in q of degree k(b-k). With t=q^(-1) and z=t^(2j-b-1)w, the kth summand has valuation k(k-2j+1). The minimum -j(j-1) occurs at exactly k=j-1 and k=j. After scaling, the residual polynomial is w^(j-1)(1+w), whose root -1 has derivative (-1)^(j-1), a unit.

Hensel lifting therefore produces one Laurent-series root for each j, with leading term -q^(b+1-2j). Their valuations are distinct, giving all b roots. For i<j, the leading term of their difference is -q^(b+1-2i). Squaring each difference eliminates its sign, and the total exponent is

    2 sum_(i=1)^b (b-i)(b+1-2i) = b(b^2-1)/3.

The discriminant is a polynomial with integer coefficients, so this Laurent expansion proves both its degree and leading coefficient 1. Dividing by the accepted monic factor (q-1)^[b(b-1)/2] gives the stated V_b degree and monicity. In particular, no reduction V_b mod p can be the zero polynomial. The same residual derivative remains nonzero in characteristic two; this observation does not assert an unrelated positive-characteristic root-of-unity guard.

## 6. Exact remaining gap and failed sufficient test

The transformation H_b(v^2)=v^b P_b(v+v^(-1)) is correct. The diagonal Christoffel-Darboux identity has ordinary squares P_k(X)^2 and denominator w_k, rather than absolute squares. Nonzero recurrence coefficients imply consecutive P_b and P_(b-1) have no common zero. At any zero xi of P_b, its kernel is therefore nonzero exactly when P_b'(xi)!=0.

The only ramification points of v -> v+v^(-1) are v=+/-1, corresponding to z=1 and X=+/-2. These are excluded by Section 3 above. Also H_b(0)=1, so v=0 never enters. Every other zero has its multiplicity preserved under the local coordinate changes. This proves the claimed equivalence between the missing kernel nonisotropy and ordinary H_b squarefreeness. The odd root at X=0 is already simple by the forced-root argument.

The positive Jacobi matrices used for lattice values are polynomials in the separate spectral parameter lambda; they are not the complex-coefficient P_b Jacobi matrices. The candidate explicitly respects this distinction. Its complex counterexample has u_1+u_2+u_3=2 and u_1 u_3=1, giving R_4=X^4-2X^2+1. All three coefficients have positive real part and increasing arguments, yet the zeros repeat. This properly defeats the proposed generic shortcut without pretending to be an actual-family counterexample.

The exact b=4 deflation and shifted reduction were independently reconstructed:

    V_4=(q+1)^2(q^2+q+1)(q^3+3q^2+3q+5)^2
        *(q^4+3q^3+4q^2+3q+5),
    V_4(1+t) mod 3=t^14-t^13-t^11-t^10+t^9+t^8.

Thus t_3(4)=8, exceeding phi(9)=6. A separate exact cyclotomic-field calculation confirms gcd(H_4,H_4')=1 at d=9, also at a nonprincipal embedding. Failure of the strict t-bound is therefore inconclusive for squarefreeness, precisely as the candidate states. No uniform ordinary-squarefreeness conclusion follows from monicity alone.

## 7. Independent controls and source integrity

The reviewer's `independent_controls.py` constructs H by its three-term recurrence, separately compares it to Gaussian product coefficients, and never imports the author's checker. Its 177 exact assertions cover the q-difference equation, reciprocity, parity starts, sector-sum derivative identity, half-lattice product, symbolic rotation exponents, all three monic Jacobi normalizations, Newton faces and degrees, direct discriminants, the failed finite-t criterion, q-Hermite/CD identities, bounded node controls at already covered orders 3,5,9 with nonprincipal embeddings, the complex-recurrence warning, and fresh source-byte verification. All passed on the first execution. These are transcription controls, not a new order census.

The author checker was inspected before execution. It imports standard installed SymPy and local standard libraries, performs bounded exact checks, and writes only CHECKS.json beside itself. Its identical bytes were copied to the separate review replay directory so the frozen author candidate was not changed. That replay passed 82 assertions; its output CHECKS.json is byte-identical to the frozen author's CHECKS.json. The reviewer's controls and replay remain separate evidence.

The candidate manifest hash and all eight declared file byte counts and SHA-256 hashes passed verification before and after review. Both controlling sources were freshly retrieved through the GitHub connector at their pinned commit paths. Exact content, SHA-256, byte counts, and Git blob IDs match the retained source copies. See `PROOF_SOURCES.md`, `SOURCE_VERIFICATION.json`, and `INPUT_VERIFICATION.json`.

The primary Spiridonov-Zhedanov paper was independently inspected: its first two pages distinguish real positive recurrence coefficients from complex ones and require a separate simplicity hypothesis in the latter case. It supports the limitation stated in the candidate. No broad novelty or priority determination was attempted, and no lower-degree simplicity theorem was inferred from top-degree root-of-unity orthogonality.

## Terminal boundary

The frozen author candidate is accepted for the uniform odd-order node theorem, positive-node exclusion, and discriminant monicity. Its declaration that ordinary squarefreeness remains unproved in the requested unrestricted prime-power range is accurate. Completion still needs lemma (L) or another genuine uniform nonvanishing mechanism. All existing exclusions and accepted prior ranges remain intact. This review is scientific acceptance only; it makes no canonical-record or repository change.
