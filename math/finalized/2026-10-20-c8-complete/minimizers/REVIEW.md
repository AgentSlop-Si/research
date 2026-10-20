# Independent adversarial review: complete C8 rank-zero minimizers

20 October 2026 UTC.

## Verdict and accepted scope

**ACCEPT the frozen candidate in ../classification/PROOF.md.** The proof gives necessary and sufficient conditions for every minimizing phase pair and every original complex-monomial/real-core representation, not merely a family containing a minimizer. No mathematical gap or counterexample was found.

The accepted conclusions are:

1. Every minimizing squared-phase pair A=P^2, B=Q^2 is four-periodic in the fixed Fourier ordering.
2. Exactly 32 squared-phase pairs remain after the continuous inverse scalar gauge is normalized by a0=1. The candidate's formulas are exhaustive and nonduplicating at this level.
3. The 32 pairs form one orbit under the stated Fourier-compatible translations and conjugation/reversal. Arbitrary permutations are not silently claimed as symmetries of the fixed Fourier matrix.
4. P and Q themselves need be periodic only up to independent real signs. All their square-root choices are allowed.
5. The canonical real core Re(PFQ) is not the only optimum. The candidate includes precisely all of the additional four-real-dimensional, two-by-two constrained core freedom.
6. Every original triple follows by arbitrary invertible real-monomial absorption, with the external operator norm unchanged.

The accepted exact rank-zero value is a premise. This report makes no positive correction-rank claim, no claim for another Fourier size, and no novelty claim.

The complete source paths, byte lengths, and SHA-256 bindings are recorded in SOURCE_BINDINGS_BEFORE.json and SOURCE_BINDINGS_AFTER.json. Frozen copies are included. The candidate is 16,836 bytes, with SHA-256 6d3af7582c56a7b03ab5967503642634a03a14af5f2234c9ab3118615d643c76. This review audits its mathematical text rather than relying on its checker or any historical program.

## 1. Equality in the scalar contraction inequality

Let m=(1-sqrt(sqrt(2)-1))/2 and n=1-m. Thus 0<m<1/2 and m+n=1.

For the first opposite-pair balancing step on R=[[a,b],[c,d]], norm(R)<1 makes equality impossible: increasing the positive b,c together to the first norm-one boundary strictly increases their arcsine sum. At the boundary the accepted scalar proof has q=bc <= (1-a)(1-d), and the cosine of the arcsine sum is strictly decreasing in q. Equality therefore forces q=(1-a)(1-d). The boundary identity then forces (b+c)^2=4bc, so b=c=sqrt((1-a)(1-d)).

Apply the same equality criterion to the column-swapped balanced matrix. It forces a=d=1-t, where t=b=c. The final function asin(t)+asin(1-t) is strictly convex for 0<t<1, not merely weakly convex. Since t lies in [m,n] and m<n, equality with the endpoint maximum occurs only at t=m or t=n.

Consequently the only possible equality trace grids are [[m,n],[n,m]] and [[n,m],[m,n]]. This is an exhaustive equality result. No unexamined zero or boundary entry exists: every grid entry is at least m>0 and below one.

## 2. Exact complex trace conditions and phase branches

For a periodic minimizing pair, every principal eigenphase belongs to [-theta,theta], where theta=acos(m)<pi/2. The accepted scalar lower bound and determinant-center upper bound have the same endpoint. Therefore equality holds at every step.

In a sector with normalized absolute trace m, its half-separation is theta, leaving midpoint zero. Its entire two-dimensional sector has Hermitian part mI. In a sector with normalized trace n, the half-separation is theta-pi/4 and its midpoint has absolute value pi/4. The determinant congruence forces the two high-trace midpoints to have the same sign. There is no independent sign choice for those two midpoints.

Thus the normalized complex traces are exactly

    (m, n eta, n eta, m), or (n eta, m, m, n eta),
    eta=exp(+i pi/4) or exp(-i pi/4).

These conditions are also sufficient. For a two-by-two unitary with nonzero trace 2p exp(i sigma), the phase of the trace squared is its determinant, regardless of the possible sign of a half-angle cosine in an arbitrary initial parametrization. Its two eigenvalues are therefore exp(i sigma)(p +/- i sqrt(1-p^2)). For the four traces above these phases lie in the desired arc and reach its endpoints.

The complete Hermitian spectrum is m with multiplicity six and s=sqrt(1-m^2)=sin(theta) with multiplicity two. This is stronger than merely knowing the minimum eigenvalue. It is needed for the complete real-core classification.

## 3. Critical support and both normalization equality steps

This is the essential additional argument beyond the accepted value proof.

Let Z be unitary, T diagonal, 0<=T<=I, and Herm(ZT)>=mI. If Zx=lambda x with Re(lambda)=m and ||x||=1, normality gives

    m <= Re(lambda) x*Tx = m x*Tx <= m.

Hence (I-T)x=0. This implication uses m>0 and positivity of I-T, and does not assume Z commutes with T. If the critical eigenspace has nonzero support on each coordinate, the diagonal nature of T gives T=I.

Every periodic minimizer has this full support. Its two m-trace sectors are either even,+ together with odd,-, or even,- together with odd,+. The whole two-dimensional space of each is critical. The projector onto the sum of these two sectors has every diagonal entry exactly 1/2. In particular no coordinate can escape the equality argument, even if a particular eigenbasis vector has zero entries.

The order of applying this fact matters. The second normalization has a fully periodic output. Applying support rigidity there first proves T_A=I and hence the ORIGINAL A is periodic. Only then is the output of the first normalization fully periodic, so support rigidity applies to T_B and proves the ORIGINAL B is periodic. This avoids the circular mistake of assuming periodicity in the first step.

An averaged diagonal entry cannot vanish: the corresponding diagonal entry of Herm(C E) would be zero, contradicting its positive lower bound m. Alternatively, the support argument itself would rule out a zero diagonal entry of T. Equality |(a_j+a_{j+4})/2|=1 for two unit complex numbers forces their equality, not their equality up to sign. Thus actual squared-phase periodicity, not antiperiodicity, follows.

## 4. Exhaustive 32-family count, gauges, and a separate parametrization

I independently derived the magnitude equality using the top singular vectors (1,1)/sqrt(2) of the trace grid. Equality in the Cauchy-Schwarz proof of the Hadamard-factor contraction forces the two four-component nonnegative factor vectors to coincide. Thus the squared magnitudes of the four sum/difference factors alternate between m and n.

The candidate's phase ratios therefore have precisely the two possible real parts +/-sqrt(sqrt(2)-1) and the nonzero imaginary parts +/-sqrt(2-sqrt(2)). Every ratio has two choices, and all four ratios can be chosen independently. The determinant/trace identity determines the sign of eta from their product. The first three trace equations then determine B0,A1,B1 uniquely after a0=1. All denominators are nonzero; their moduli show each recovered phase has modulus one. The fourth trace follows from the exact ratio identity, including its factor -i.

An independent parametrization is useful as a cross-check. Let q be m or n, l=1-q, a=sqrt(q), b=sqrt(l). Choose signs epsilon,u,v,w independently. Set eta=exp(i epsilon pi/4), and choose

    (kappa,lambda)=(1,eta) if q=m,
    (kappa,lambda)=(eta,1) if q=n.

Put z=a+i u b and define

    A0=1, A2=z^2,
    A1=-i v (lambda/kappa) z (b+i w a),
    A3=-i v (lambda/kappa) z (b-i w a),

    E=a kappa/z, F=i v b kappa/z,
    G=i u b lambda/z, H=i v w a kappa^2/(lambda z),
    B0=E+F, B2=E-F, B1=G+H, B3=G-H.

These are all unit phases and have normalized traces

    (q kappa, l lambda, l lambda, q kappa).

The family has 2*2*2^3=32 members. Conversely, A2 fixes u; the ratio F/E fixes v; the ratio delta/gamma fixes w; the nonreal trace midpoint fixes epsilon; and q fixes the trace layout. Thus it has no duplication after a0=1 and recovers every equality pair. The independent exact checker verifies these identities for symbolic a,b subject only to a^2+b^2=1, across the complete discrete sign set. It is not a numerical sampling argument.

The continuous gauge (A,B)->(gA,g^{-1}B) remains arbitrary. Independent square-root signs in all sixteen entries of P,Q are real row/column gauges. They cannot be suppressed when claiming literal periodicity of P or Q, and the candidate correctly does not suppress them. The 32 count is a squared-phase scalar-gauge count, not a count of original L,C,R triples.

## 5. Fourier-compatible symmetry orbit and permutations

I directly rederived the transformations from the fixed Fourier convention omega=exp(-2pi i/8):

    S_a F=F D_{-a}, F S_b=D_b F, J conjugate(F)=F.

They give precisely the candidate's P,Q formulas under row translation, column translation, and conjugation/reversal. These are norm-preserving real permutations and/or conjugation of V, so they preserve ||Im_entry V||.

For labels (tau;a,b,c,d), one row shift sends them to (1-tau;-b,a,-c,-d), and one column shift to (1-tau;-a,-b,d,-c). The formulas commute and have fourth power the identity. A combined action with odd total shift parity changes tau. A nonidentity action with both powers even flips a nonempty sign pair. When both powers are odd, a quarter rotation of a sign pair has no fixed point. Therefore the Z4 x Z4 action is free, with 16 labels in each orbit. It preserves epsilon, so each epsilon class is one orbit.

Conjugation with reversal sends the labels to (tau;-a,b,-c,-d), which flips epsilon. All 32 are therefore one orbit under the stated enlarged group. The accepted witness's labels are tau=m and (+1,-1,+1,+1), giving epsilon=-1, as claimed.

Plain conjugation is not silently treated as a symmetry of the fixed Fourier target. Nor is every exterior permutation. Arbitrary real permutations in the original model are instead absorbed into the unrestricted real core. These are different facts, and the candidate distinguishes them correctly.

## 6. Complete nearest-real-core freedom

Let V=X+iY be an optimal phase transform. Since the Hermitian spectrum above is m (six times) and s (twice), the singular values of the REAL matrix Y are

    d=sqrt((1-m)/2), six times;
    e=sqrt((1-s)/2), twice.

Here 0<e<d. Take a real SVD Y=O_L diag(dI6,eI2) O_R^T. For a real core C, put D=C-X. If ||-D+iY||<=d and v is any real top right singular vector of Y, then

    ||(-D+iY)v||^2=||Dv||^2+d^2,

so Dv=0. The adjoint argument for every real top left singular vector gives D^T u=0. Consequently D has only a two-by-two lower block K in these real SVD bases. This proves necessity on BOTH sides, not merely annihilation of a right subspace.

The residual is then block diagonal with i d I6 and -K+i e I2. Its norm is d if and only if ||K+i e I2||<=d, since conjugation and negation preserve norm. This proves both necessity and sufficiency of the candidate's core family.

The exact Hermitian LMI is

    (d^2-e^2)I2-K^T K-i e(K^T-K) >= 0.

For K=[[a,b],[c,f]], its two diagonal inequalities and determinant inequality are exactly those in the candidate. In particular the last term of the determinant is -e^2(b-c)^2; no sign or transpose has been lost. The checker derives this directly from the complex residual.

Nonzero cores really occur: K=tI2 is feasible for |t|<=sqrt(d^2-e^2). Thus C=Re(V) is only one member. The feasible K set has nonempty interior because ||i e I2||=e<d. Its description by a translated complex operator-norm constraint in four real coordinates is exact; it is not presumed to be an ordinary Euclidean ball.

## 7. Exhaustiveness for original monomial triples

Every invertible complex-monomial L,R admits L=P* M and R=N Q*, with P,Q diagonal unitary and M,N invertible real monomial. The external residual norm is exactly

    ||F-L C_orig R|| = ||P F Q-M C_orig N||.

No nonunitary residual transformation is performed. If the original triple attains the global value d, contractivity of the entrywise imaginary part gives phase error at most d; the accepted global lower bound forces equality. The phase pair must therefore belong to the exhaustive classification. The transformed real core must then belong to the exact two-by-two family above.

Conversely, every classified phase pair, every allowed square-root choice, every feasible two-by-two core, and arbitrary invertible real-monomial M,N produce an original optimum by C_orig=M^{-1} C N^{-1}. This includes all real magnitudes, signs, and exterior permutations. Redundancy of these gauges is harmless and explicitly acknowledged.

## 8. Exact controls, independence, and limits

The fresh program independent_exact_checks.py imports no source-packet code and executes no historical checker. It constructs the full normalized 8-by-8 Fourier matrix, all sector vectors, generic phase matrices, and the complete core LMI itself. Its controls include:

- the generic full eight-dimensional sector identity and determinant obstruction;
- both critical-sector projectors, their ranks, and diagonal entries 1/2;
- the entire separate 32-member family with symbolic circle parameters;
- the candidate's generic four-ratio trace identity;
- the exhaustive finite symmetry-label action and orbit size;
- the exact scalar endpoint and core determinant identities;
- the positive radical for s=sqrt(1-m^2).

All 100 controls pass. They support the stated identities; the universal equality, support, and exhaustion statements are established analytically in this report and the candidate, not inferred from the number of controls. No numerical optimizer, finite phase grid, or floating-point tolerance was used. No external state was modified.
