# Independent audit of the odd cycle chirp classification

## Verdict

Accept the stated **partial uniform classification** in its precise scalar, common-cycle, characteristic-zero model. The uniform resonance gcd, prime-order squarefreeness proof, residue formulas, forced diagonal, and root-free field-operation costs are valid. Every one of the 250 saved modular certificates is correct, and their indices cover exactly N=5,9,...,1001. Together with the uniform odd-parity obstruction, this classifies all 500 odd sizes from 3 through 1001.

No mathematical error requiring withdrawal of a theorem was found. There is one minor reproducibility improvement: the supplied standalone certificate verifier does not assert completeness of the claimed index range. Its input file really does have the complete range, which this audit explicitly checks. This is a verifier-hardening issue, not a counterexample or a gap in the archived finite result.

The remaining general composite-order squarefreeness statement is not proved by this package. In particular, the finite certificates do not prove the entire family N=5r². No unrestricted Green-count minimum, subquadratic application algorithm, numerical-stability guarantee, or publication-priority claim follows.

## Scope and evidence

The primary document is `diagonal_chirp_classification_0246/CLASSIFICATION.md`. Its accompanying certificate data, result data, provenance records, and two programs were inspected. The two immediate predecessor reports were consulted to check the exact model and the m+1-branch fallback. Their programs were not executed.

All three package manifests were verified. The primary package manifest covers every file other than itself. The primary package's archived before/after snapshots agree on its 22 protected predecessor files and match their current bytes. This audit additionally hashes the whole primary package and those predecessor files before and after its own controls. The resulting snapshots are identical.

`independent_controls.py` is new audit code. It never imports or executes a supplied constructor or checker. It uses standard Python and the installed SymPy arithmetic library. Its finite certificate reconstruction uses the multiplicative Gaussian-binomial formula, different from both the source generator's Pascal recurrence and the source verifier's three-term recurrence. Small bank controls solve the shifted Hankel system directly and invert quotient elements by solving multiplication matrices.

The audit verifies mathematics and the archived evidence. Hash agreement establishes preservation during this audit; it does not independently prove the historical statement that no predecessor code was run before this audit began.

## Exact model and minimum

The result concerns

    N=2m+1 >= 3,  K=Q(q),  q a primitive Nth root,
    h=(N+1)/2,  f(k)=q^(h k²),
    C=sum_(k=0)^(N-1) f(k) P^k,
    C=delta I + sum_(s=1)^Q a_s (I-lambda_s P)^(-1).

Every branch has a scalar coefficient, the same natural N-cycle P, lambda_s nonzero, lambda_s^N unequal to 1, and a_s nonzero. Nodes and weights may lie in an algebraic closure of K. The root-free sum is implemented over K. The result does not establish that all individual nodes can be chosen in K.

An arbitrary added diagonal cannot enlarge this particular representation class. Both C and the branch sum are circulants, so their difference, if diagonal, is a scalar multiple of I. This argument ceases to apply if the individual branches themselves receive arbitrary nonconstant diagonal endpoints.

The resolvent identity is

    (I-lambda P)^(-1)
      = (sum_(k=0)^(N-1) lambda^k P^k)/(1-lambda^N).

Thus delta changes only moment k=0. The shifted m by m Hankel matrix factors as

    [f(i+j+1)]
      = f(1) diag(f(i)q^i) [q^(ij)] diag(f(j)q^j).

Its central matrix is Vandermonde on m distinct powers of primitive q. It is nonsingular, and any Q-node exponential representation has shifted Hankel rank at most Q. Therefore Q>=m. Repeated nodes can be combined; cancellations or repeated ordinary resolvents cannot evade the rank bound.

At Q=m the monic annihilator is uniquely fixed by the shifted moment equations. It is

    T_m(z;q)=sum_(j=0)^m (-1)^(m-j) [m choose j]_q z^j.

Its constant term is (-1)^m. Its roots give a legal m-branch representation exactly when they are distinct and avoid the Nth roots of unity. Conversely, an m-branch representation has m distinct nodes and forces this annihilator, so a failed guard cannot be repaired by selecting a different delta.

The predecessor's m+1 fallback is valid in characteristic zero. Briefly, the consecutive formal orthogonal polynomials are coprime, and the pencil of degrees m+1 and m excludes only finitely many parameters. The Wronskian bounds the repeated-root parameters by 2m; zero and the N cycle roots exclude at most N+1 more. Since 2m+N+1=2N, one of 2N+1 distinct integer parameters works. Residue matching then gives the N moments with delta=0. This confirms the required upper bound independently of the smaller-bank guard.

Hence the exact alternatives really are m and m+1 in the stated model.

## Uniform resonance theorem

The proof is sound and does not assume positive orthogonality for complex q.

First use q=exp(2*pi*i/N). The recurrences imply

    T_n(z)=(i sqrt(z))^n S_n((z-1)/(i sqrt(z))),
    S_n(x)=x S_(n-1)(x)-(1-q^(n-1))S_(n-2)(x).

For z on the unit circle, write sqrt(z)=exp(i*phi/2); the transformed argument is the real number 2 sin(phi/2). Changing the square-root choice does not affect the polynomial identity.

The tridiagonal J has squared edge j equal to 1-q^j. The chosen phases give J=D R D with R real symmetric, zero diagonal, and positive off-diagonal entries. For 0<=j<m,

    theta_j=-pi/8+pi(2j+1)/(8N)

lies strictly between -pi/8 and 0. In particular, every entry of B=D^(-2) has positive real and imaginary parts.

If Jw=t w for a nonzero real t, putting v=Dw gives Rv=t Bv. The left quadratic form v*Rv is real. The imaginary part of the right side is t times the strictly positive number v*Im(B)v, a contradiction. This establishes the absence of nonzero real roots of S_m.

For even m, S_m(0) is a nonzero product of alternate nonzero squared edges. For odd m, the tridiagonal recurrence gives a one-dimensional kernel of R. On an orthonormal real basis adapted to that kernel, the coefficient of t in det(R-tB) is a nonzero real complementary determinant times a nonzero scalar proportional to v_0^T B v_0. Its real part is positive before multiplication by the real factor. Thus zero is a simple root. This checks algebraic simplicity, not merely geometric multiplicity.

The transformed argument has nonzero derivative at z=1. Consequently, in the principal embedding T_m has no unit-circle zero when m is even, and has only the simple zero z=1 when m is odd. The resulting monic gcd is

    gcd(T_m,z^N-1)=1       for N=1 mod 4,
                    z-1    for N=3 mod 4.

An automorphism q->q^a carries this algebraic gcd identity to any primitive embedding. It does not need to preserve arbitrary absolute values. The report correctly limits its stronger unit-circle statement to the principal embedding and its complex conjugate.

No additional hypothesis is missing from this argument at N=3: the matrix is 1 by 1, R=0, and its determinant has a simple zero exactly as required.

## Prime order squarefreeness

The ordinary discriminant factorization is correct:

    Disc_z T_n(z;q)=(q-1)^(n(n-1)/2) E_n(q),
    E_n in Z[q],
    E_n(1)=product_(j=1)^n j^j.

Here the discriminant uses the ordinary derivative in z, not a q-difference operator.

To justify the integrality step explicitly, substitute q=1+epsilon² and z=1+epsilon x. The recurrence shows that epsilon^(-n)T_n belongs to Z[epsilon,x], is monic in x, and specializes to the monic probabilists' Hermite polynomial. A discriminant scales by epsilon^(n(n-1)). Expanding the original integer polynomial Disc T_n at q=1 then forces its coefficients of (q-1)^k to vanish for k<n(n-1)/2. Division by the monic integer polynomial (q-1)^(n(n-1)/2) therefore leaves E_n in Z[q].

The Hermite constant also has the claimed sign. For monic He_n,

    He_n'=n He_(n-1),
    Res(He_n,He_(n-1))
      =(-1)^(n(n-1)/2) product_(j=1)^(n-1) j^j.

Multiplying by n^n and the discriminant sign leaves the positive product through n.

If q is primitive of prime order p and n<p, a zero E_n(q) would imply divisibility by Phi_p in Z[q]. Evaluation at 1 would make p divide a product of positive integers all less than p, impossible. Taking n=(p-1)/2 proves the report's prime-order result. The same reasoning works at primitive p^a-th roots when n<p, because Phi_(p^a)(1)=p.

The stated limitation is genuine for this argument: the target n=(p^a-1)/2 is not less than p when a>1, and Phi_N(1)=1 for orders with at least two distinct prime divisors. Nothing in this proof establishes the target squarefreeness for all composite orders.

Independent symbolic controls verify the ordinary-discriminant factorization and its integer quotient through n=8, and the Hermite discriminant formula through n=16. These are checks of the derivation, not replacements for its uniform proof.

## Residues and the forced diagonal

The numerator R is correctly formed as the polynomial part of the shifted Laurent moment series multiplied by T. For simple legal roots lambda_s, the partial fraction identity gives

    c_s=R(lambda_s)/T'(lambda_s),
    b_s=c_s/lambda_s,
    a_s=(1-lambda_s^N)b_s.

It matches the first m shifted moments by construction. The defining m orthogonality equations then extend that agreement through f(2m). At z=0,

    R(0)/T(0)=-sum_s b_s,

so delta=1+R(0)/T(0) restores f(0)=1 with the stated sign. A zero c_s would leave fewer than m shifted exponential terms, contradicting the nonsingular shifted Hankel matrix. The other two factors are nonzero by the guards.

The full (m+1) by (m+1) Hankel determinant is nonzero. Replacing only f(0) by 1-delta makes its determinant affine in delta. Its cofactor is the nonzero shifted-by-two m by m Hankel determinant. Therefore the unique possible delta is exactly the stated determinant ratio. Factoring its two Vandermonde determinants gives

    delta=q^(-m²) product_(i=0)^(m-1)(q^m-q^i)
         =(-1)^m q^(-m(m+1)/2) product_(j=1)^m(1-q^j).

All factors are nonzero because 1<=j<=m<N and q is primitive. This conclusion applies to a successful m-bank; in an illegal case it remains only the forced candidate diagonal.

The residue proof, determinant argument, and chirp phases agree. Fresh controls independently check the numerator, the product, the determinant ratio, every required moment, and the complete linear scan on the basis inputs specified below.

## Root free algorithm and costs

For a successful smaller bank, E=K[z]/(T) is a finite étale K-algebra of dimension m. It need not be a field. The guards imply that z, T', and 1-z^N are invertible in E. Its algebra trace becomes the sum of evaluations at all distinct roots after extending scalars. Hence

    b=z^(-1) R (T')^(-1),
    a=(1-z^N)b,
    ell(y)=Tr_(E/K)(a y)

implements exactly the scalar branch coefficients, and no unit-cost algebraic extension is being used.

The scan is consistent with P[i,i+1 mod N]=1. Its closure computes the first coordinate of (I-zP)^(-1)x, and y_i=x_i+z y_(i+1) computes the others backwards. The target chirp is even, but the proof does not need to rely on that symmetry to repair an orientation mismatch: the specified orientation already agrees.

The O(N²) successful-case setup bound is attainable with ordinary polynomial arithmetic. Constructing T and R, extended Euclidean inverses, and the squarefreeness gcd cost O(m²); generating z^N by repeated companion multiplication costs O(Nm). Newton sums produce the trace data in O(m²). To make the functional-cost statement explicit, compute traces of 1,z,...,z^(2m-2), then for a=sum_i a_i z^i store

    ell(z^j)=sum_i a_i Tr(z^(i+j)),  0<=j<m.

This costs O(m²) and stores only m functional coefficients. A naive construction of all full multiplication matrices is unnecessary. The audit deliberately uses those more expensive matrices as an independent control, not as the advertised production algorithm.

For application, multiplication by z modulo a monic degree-m T costs O(m), as does evaluating ell. Horner closure and the backwards scan cost O(Nm); one general quotient multiplication by the retained closure inverse costs O(m²). Therefore total application is O(Nm+m²)=O(N²), with O(N+m) workspace and O(N) retained base-field coefficients. Branch summation and cycle closure are fully charged.

The fallback's O(N³) setup follows from O(N) candidate tests at O(N²) each. Its application remains O(N²).

These are exact operations over K with q supplied. They do not bound bit complexity in rational coordinates, numerical conditioning, explicit algebraic root extraction, or the cost of constructing q. Nor do they give a width-one state: the state dimension is m, or m+1 in the fallback.

For the two-bank full inverse, N-1 nontrivial resolvent occurrences follow only when both smaller banks succeed. Combining the three resulting diagonal terms is legitimate if the grammar permits an arbitrary diagonal with possible zero entries. The report expressly retains this qualification. No full-inverse minimum follows from the per-bank rank bound.

## Finite certificates and fresh controls

For every listed N, the saved p is proven prime by trial division, p=1 mod N, and q_bar has exact multiplicative order N. The reconstructed Gaussian-binomial polynomial is identical to the saved T. The saved U and V satisfy the exact coefficient identity U T+V T'=1 over F_p. A separate Euclidean computation verifies both gcd(T,T')=1 and gcd(T,z^N-1)=1.

This proves a characteristic-zero fact. Exact order and p not dividing N give a homomorphism Z[zeta_N]->F_p sending zeta_N to q_bar. The discriminant is an algebraic integer. If it were zero in characteristic zero, its image would be zero under this homomorphism. The Bezout identity proves its image nonzero. One such exact certificate suffices; there is no probabilistic lifting claim.

Every saved trial history was also recomputed. All 31 rejected trials are squarefree but have extra finite-field resonance. For example, the first is N=49, p=197, q_bar=16, with resonance gcd degree 2. These are bad reductions of the nonzero characteristic-zero resultant, not counterexamples to the resonance theorem.

The archive's claimed 918 moment identities and 4,892 scan-output entries agree with its saved per-case counts. This audit does not claim to have rerun that source checker. It supplies its own separately recorded controls:

- Exact cyclotomic fields for N=3,5,7,9,11,13, both chirp signs. These reconstruct the annihilator by a Hankel solve and check the exact resonance gcd. N=5,9,13 check every basis-vector output.
- Finite fields for N=17,21,25,45, both signs. Every basis-vector output is checked through N=25; N=45 uses two fully specified vectors for each sign.
- All successful bank controls use Gaussian elimination for quotient inverses and literal regular-representation matrix traces. They also compare the forced diagonal with an independently computed determinant ratio.
- Ordinary discriminants through degree 8 and Hermite discriminants through degree 16 are computed symbolically.

The exact counts, source-preservation checks, and machine-dependent elapsed time appear in `AUDIT_RESULTS.json`. All-basis testing proves the complete linear map for each such tested field and size. The two N=45 input vectors are explicitly limited spot checks of application code; they are not described as an all-input certificate. The uniform formulas supply the mathematical all-input proof.

## Literature and priority boundary

The identified Rogers-Szegö polynomial and its three-term recurrence are established formulas. Vinroot's Section 1 states the definition and recurrence; equation (2.3) gives the alternating evaluation used in the source report. [Vinroot, Multivariate Rogers-Szegö polynomials and flags in finite vector spaces](https://arxiv.org/html/1011.0984v1).

Cigler's Sections 5.1 and 5.2 give the relevant q-Hermite recurrence and its relation to Rogers-Szegö polynomials. These algebraic identities do not supply a positive real orthogonality measure at arbitrary complex q, and the report correctly supplies its own matrix-congruence proof. [Cigler, Continuous q-Hermite polynomials](https://homepage.univie.ac.at/johann.cigler/preprints/contqhermite.pdf).

The finite complex-moment, formal-orthogonal-polynomial, and minimal-partial-realization setting is established in the cited work of Pozza and Pranić. This supports attribution of the framework, not a claim that the exact root-of-unity specialization was previously proved there. [Pozza and Pranić](https://arxiv.org/abs/1903.11395).

A pertinent additional primary source is Ismail and Witte. Its introductory equations (1.7) and (1.8) distinguish ordinary and quantized discriminants, and Section 5 evaluates a q-difference discriminant for Rogers-Szegö polynomials. That formula must not be substituted for the ordinary discriminant in the present squarefreeness question. The report's warning on this point is justified. [Ismail and Witte, Discriminants and Functional Equations for Polynomials Orthogonal on the Unit Circle](https://arxiv.org/pdf/math/0012259).

This was a targeted literature check, not an exhaustive priority review. The mathematical audit supports the stated project-specific extension. It does not establish publication-level novelty or that the remaining composite question is open throughout the literature.

## Recommended wording and verifier improvement

No theorem statement needs correction. Preserve these qualifications in any shorter summary:

1. The minimum is for scalar resolvents sharing the natural cycle, with a single free diagonal, and nodes allowed in an algebraic closure.
2. The characteristic-zero resonance gcd holds in every primitive embedding. The stronger all-unit-circle-root claim is proved only for the principal embedding and its conjugate.
3. All listed sizes are certified exactly. Uniform squarefreeness for untested composite N=1 mod 4 is not established here.
4. The algorithm costs O(N²) base-field operations and uses a linearly growing algebra state. No FFT speedup is shown.
5. Publication priority is unverified.

For the original standalone certificate verifier, add an explicit assertion that the saved N list equals list(range(5,1002,4)), together with a check that each claimed minimum is (N-1)//2. This audit already performs both checks, so the recommendation does not weaken the present verdict. Keep sealed source files unchanged; apply such edits only in a separately versioned revision.

The audit is complete within its assigned scope. The exact outstanding mathematical target remains nonvanishing of Disc_z H_((N-1)/2)(z;zeta_N) for all composite N=1 mod 4, or a genuine counterexample. The present proof and finite evidence should not be promoted beyond that boundary.
