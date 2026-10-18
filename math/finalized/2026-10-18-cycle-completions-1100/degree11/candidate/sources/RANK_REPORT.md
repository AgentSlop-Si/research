# N13 free-cross degree-seven recurrences: uniform rank and the exact chart boundary

16 October 2026 UTC. New bounded mathematical result. Candidate scope: the degree-seven forced-window coefficient matrix in the original characteristic-53 signed-bank problem. Independent review is provided separately.

## Result

The six-by-seven coefficient matrix A(Y) has rank six at **every** Y in **every** field of characteristic 53. There is no intrinsic rank-drop locus in this necessary degree-seven recurrence gate.

The determinant D6(Y) of its first six columns is 48 times a monic irreducible polynomial of degree 37. Consequently the familiar chart that fixes the t^6 coefficient to lambda works for every cross node in F_(53^d) exactly when 37 does not divide d. In particular, there are no exceptional chart nodes in degrees 2, 3 or 4. If 37 divides d, precisely 37 cross nodes make this chart singular, but another certified six-column minor is nonzero there and the full coefficient matrix still has rank six.

A denominator-free polynomial particular solution and polynomial kernel vector give one affine line of monic degree-seven recurrence polynomials for every Y over every characteristic-53 field. This also treats the degree-37 chart exceptions without discarding them.

This closes the recorded rank-drop prerequisite. It does **not** give a sixteen-bank representation, exclude freely varying cross nodes in degrees 2–4, establish support splitting, or solve full-sector compatibility. The original parent records remain TO RESEARCH, priority 56.

## 1. Exact original model and inherited premises

Work over a field K of characteristic 53, with N=13 and q=16 of order 13. The original target is F[k,t]=q^(-kt), with S e_t=e_(t+1) and T e_t=q^t e_t. A physical bank is

    (1/13) sum_(j=0)^12 w_j (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    1-alpha^13-beta^13 != 0.

All legal beta are allowed. Exactly one effective alpha node is permitted in each cross orientation (-,+) and (+,-), at independent nonzero nodes y and z. The accepted lower theorem implies that a sixteen-bank representation would have allocation (7,1,1,7), with seven distinct nonzero same-sign support nodes on each side. Their annihilators must be monic degree-seven polynomials with distinct nonzero roots in K. We inherit these conclusions from the source-bound accepted reviews; we do not claim a new replay of the degree-six lower-bound minors or bank inverses.

The source-bound expansion and normalized target are

    C_(epsilon,delta;alpha)(a,b)=G_(epsilon,delta)(a,b) alpha^[epsilon a]_13,
    f(a,b)=q^(10(a+b)^2).

The G factors are ordered Gaussian coefficients, with r=[epsilon a]_13, ell=[delta b]_13 and omega=q^(epsilon delta):

    G = product_(i=1)^ell (1-omega^(r+i))/(1-omega^i) if r+ell<13,
    G = 0 otherwise.

The accepted arbitrary-beta expansion has no division by beta. Thus the forced moments below apply to the original grammar, with no additional beta restriction and no trace-valued replacement bank.

## 2. Reconstructing the actual forced equations

For b=1,...,6 and b<=a<=12-b, the original isolated cross row forces

    v_b(a;Y) = [f(a,b)-Y^(13-a-b) G_-+(a,b)/G_-+(13-b,b)] / G_++(a,b).

Every denominator here is a nonzero element of F53. Each v is a polynomial in Y, with nonnegative exponent. At an actual nonzero cross node y, it equals the required positive-same-sign power moment.

Let H(t)=t^7+sum_(j=0)^6 h_j t^j. Its six available degree-seven consecutive recurrence windows are indexed, in this order, by

    (b,a)=(1,1),(1,2),(1,3),(1,4),(2,2),(2,3).

Define E(Y)[(b,a),j]=v_b(a+j;Y), for j=0,...,7. Set A=E[:,0:7] and bvec=-E[:,7]. Then every actual support annihilator satisfies

    A(y) h = bvec(y).

The result concerns this exact six-row system. It does not replace the remaining full-sector equations by recurrence necessity. The polynomial formulas also make sense at Y=0, and their rank theorem holds there, but a zero physical cross node is still illegal in a sixteen-bank representation.

## 3. Two maximal minors prove rank six over every extension

For j=0,...,6, let Dj be the determinant obtained by deleting column j from A, with all surviving columns in increasing order. Exact coefficientwise determinant expansion gives

    (deg D0,...,deg D6)=(32,33,34,35,36,37,37).

The certificate stores all coefficient arrays in ascending powers of Y, with residues 0,...,52. The following two arrays specify D0 and the monic polynomial f37=D6/48:

    D0 = [49,0,8,29,25,1,38,49,15,25,46,26,51,38,16,4,
          8,9,14,32,41,20,46,42,23,38,9,11,27,12,9,21,24]

    f37 = [35,0,0,17,49,13,18,6,21,47,41,6,37,8,18,3,
           51,33,26,11,50,50,16,3,24,25,25,9,32,7,44,49,
           45,2,40,14,41,1]

The following explicit arrays U,V certify U D6+V D0=1:

    U = [21,27,37,21,14,6,38,46,23,7,18,2,19,19,45,21,
         1,6,14,48,26,17,20,7,48,5,20,13,42,43,15,16]

    V = [35,51,28,11,27,13,45,51,3,20,21,50,19,47,37,22,
         11,24,11,4,49,5,18,4,6,7,45,52,36,38,1,26,
         27,27,47,11,21]

This identity is an equality in F53[Y], not agreement only at the 53 prime-field points. After evaluation in any characteristic-53 field, D6 and D0 cannot both vanish. Hence A always has a nonzero six-by-six minor and rank six. Since it has seven coefficient columns, the monic solution set is always a nonempty affine line.

## 4. Exact boundary of the h6=lambda coordinate chart

The certificate verifies by polynomial modular powering that

    Y^(53^37) = Y mod f37,
    gcd(f37, Y^53-Y)=1.

The degree 37 is prime. Every irreducible factor of a polynomial dividing Y^(53^37)-Y has degree dividing 37, so it has degree 1 or 37; the gcd test excludes degree 1. Therefore f37 is irreducible of degree 37. This argument also guarantees separability, since Y^(53^37)-Y has derivative -1.

Over F_(53^d), an irreducible degree-37 polynomial has a root if and only if 37 divides d; in that case all its 37 distinct roots occur. Its nonzero constant term excludes Y=0. Thus D6 is nonzero for every cross node when 37 does not divide d, including d=2,3,4. At degree-37 roots, D0 remains nonzero by the Bezout identity. The failure there belongs solely to the chosen coordinate chart; it is not a rank failure or a forbidden-bank conclusion.

Let c6 be the vector with component 6 equal to zero and the other components given by Cramer's determinants for the first six columns and right-hand side bvec. Let n_j=(-1)^j Dj. Then A c6=D6 bvec, A n=0, and n_6=D6. Wherever D6(y) is nonzero, every monic solution has the unique form

    h_j=(c6_j(y)+lambda n_j(y))/D6(y), j=0,...,6,

so h_6=lambda. At y=1 this recovers exactly the already accepted pinned formula

    H_lambda(t)=t^7+lambda t^6+(50+22lambda)t^5
      +(48+15lambda)t^4+(27+10lambda)t^3
      +(19+11lambda)t^2+(50+25lambda)t+(16+31lambda).

Recovering this formula is a source-interface regression, not a new proof of its full-sector or splitting properties.

## 5. One global affine family without denominators

Define c0 similarly using columns 1,...,6, with component 0 fixed to zero. Then A c0=D0 bvec. Set

    p=U c6+V c0,    n_j=(-1)^j Dj.

The stored arrays satisfy the coefficientwise identities

    A p=bvec,    A n=0.

Their component degrees are respectively (63,64,65,66,67,68,68) and (32,33,34,35,36,37,37). At every y, at least one component of n(y) is nonzero, because D0(y) and D6(y) cannot both vanish. The kernel of A(y) is one-dimensional, so every monic solution is uniquely

    H_(y,tau)(t)=t^7+sum_(j=0)^6 [p_j(y)+tau n_j(y)] t^j, tau in K.

This is a polynomial parameterization over F53 of the complete necessary affine line at every cross node, including the exceptional degree-37 chart points. Reflection gives the corresponding statement for the negative-same-sign support with the independently free cross node z.

The coefficients may lie in an extension field. This theorem does not force prime-Frobenius stability, factorization, squarefreeness, nonzero constant term, or splitting into seven K-valued nodes. Those are additional conditions on this family.

## 6. Checks, provenance, and honest stopping point

Only freshly authored code was run. The supplied historical proof/checker programs were not executed or imported. The safe checker uses only the Python standard library and reconstructs the actual G factors, all six rows, all seven maximal minors, both Bezout identities, Cramer's vectors, the global affine parameterization, and the irreducibility test. Its primary determinant construction is full polynomial Leibniz expansion, so it does not infer a polynomial from prime-field evaluations.

Additional controls verify 212 prime-field parameter regressions, recover the fourteen pinned affine coefficients, exhibit the degree-37 chart singularity with nonzero alternative minor, and reject corrupted particular-solution, kernel, and Bezout identities. No support search, extension-field census, raw inverse replay, historical scientific-code execution, or external write is part of this artifact. A separate independent reviewer reconstructs Gaussian coefficients via a different recurrence and maximal minors by scalar determinants plus justified degree-bounded interpolation.

This is a fixed-instance algebraic certificate; no Fourier runtime or bit-complexity improvement is claimed. Preparation, polynomial arithmetic, source reconstruction, and output are not being hidden inside a bank-count or FFT-speed claim.

The original open problem now has a simpler stated prerequisite: for independent nonzero y,z and affine parameters, enforce both support polynomials' distinct nonzero splitting over the chosen field and all original sector equations. In degrees 2–4 one may use the nonsingular h6=lambda chart without a missed exceptional-node branch. In general fields use the global polynomial family or both certified charts.

Stop here: the rank-drop subproblem is settled, while free-cross sixteen-bank existence/exclusion over degrees 2–4, possible seventeen-bank behavior, unrestricted cross allocations, other parameters, general field classification, historical priority, and FFT speed remain open.

## Sources

- Accepted original lower/forced-window review, local source SHA-256 896200e3b4b12d56dd13ac1d87b5e6ea64ef3283e77887898bb595d1bf304b6f, bound by the accepted pinned review below. Sections 3–6 provide the arbitrary-beta expansion, exact forced moments, and prior prime-field-only E7 rank check.
- [Accepted pinned field-criterion review](https://github.com/AgentSlop-Si/research/blob/3da81fafa69cc9caf3bbd16837dc5e29af18c840/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md). The y=z=1 result is prior work and is not reclassified as new here.
- [Accepted covariance-boundary review](https://github.com/AgentSlop-Si/research/blob/3da81fafa69cc9caf3bbd16837dc5e29af18c840/math/finalized/2026-10-15-frontier-boundaries/n13_free_cross_covariance_review_2355/INDEPENDENT_REVIEW.md). This artifact does not claim a target-preserving normalization of y,z.
- [Current frontier boundaries](https://github.com/AgentSlop-Si/research/blob/3da81fafa69cc9caf3bbd16837dc5e29af18c840/math/finalized/2026-10-15-frontier-boundaries/README.md). The current 87-closed/240-open index points here for these priority-56 records.

See SOURCE_LEDGER.json for exact local byte bindings. CERTIFICATE.json is the formal coefficient data; CHECK_RESULT.json is the fresh check receipt.
