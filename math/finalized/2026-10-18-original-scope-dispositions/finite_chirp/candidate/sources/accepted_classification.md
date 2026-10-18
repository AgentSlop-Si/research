# Odd-cycle chirps with one free diagonal: partial uniform classification

## Result in brief

Let N=2m+1>=3, let q be any primitive Nth root of unity in characteristic zero, put h=(N+1)/2, f(k)=q^(h k^2), and let P be the natural N-cycle. Work in exactly the scalar, common-P model

    C = sum_(k=0)^(N-1) f(k) P^k
      = delta I + sum_(s=1)^Q a_s (I-lambda_s P)^(-1),
    a_s != 0,  lambda_s != 0,  lambda_s^N != 1.

Allowing an arbitrary diagonal matrix instead of delta I does not enlarge this model: the difference of the two circulants is a diagonal circulant and must be scalar.

Nodes and branch coefficients may be algebraic over K=Q(q); the minimum is over an algebraic closure, equivalently over C. The root-free implementation of their sum uses K operations.

The earlier audit gives Q_min in {m,m+1}, with the smaller value precisely when the unique shifted moment polynomial passes three guards. This continuation proves:

1. The zero-node guard always passes.
2. The cycle-resonance guard is now completely classified for every odd N:

       gcd(T_m(z), z^N-1) = 1       if N == 1 mod 4,
                            z-1    if N == 3 mod 4.

   These are monic gcds over K. In the second case z=1 is a simple root of T_m.
3. For prime N, T_m is squarefree. Therefore every prime N==1 mod 4 has Q_min=(N-1)/2; every N==3 mod 4, prime or composite, has Q_min=(N+1)/2.
4. For composite N==1 mod 4, the only remaining uniform question is squarefreeness. Exact modular certificates settle every such N through 1001, with Q_min=(N-1)/2. Together with item 3 and the known odd-parity obstruction, this completely classifies every odd N from 3 through 1001.
5. Whenever Q_min=m, the free diagonal is forced and nonzero:

       delta = (-1)^m q^(-m(m+1)/2) product_(j=1)^m (1-q^j).

   Explicit algebraic branch coefficients and a root-free O(N^2)-setup, O(N^2)-application algorithm are given below.

There is no counterexample among the certified composite sizes. There is also no proof here that every composite N==1 mod 4 works. In particular, a theorem for every N=5r^2 is still missing. The report makes no FFT speedup, unrestricted Green lower bound, numerical stability, or publication-priority claim.

## 1. The exact scalar-bank criterion

The legal resolvent expansion is

    (I-lambda P)^(-1) = [sum_(k=0)^(N-1) lambda^k P^k]/(1-lambda^N).

Thus a free delta changes only the k=0 moment. The moments f(1),...,f(2m) must be a sum of Q exponentials. Their m by m shifted Hankel matrix is nonsingular, since

    f(i+j+1) = f(1) [f(i)q^i] [f(j)q^j] q^(ij)

and [q^(ij)] is a Vandermonde matrix on distinct nodes. Hence Q>=m.

Let T_m be the unique monic polynomial satisfying

    sum_(j=0)^m t_j f(k+j+1)=0,  0<=k<m.

The shifted Hankel system makes it unique. Direct coefficient expansion gives

    T_m(z;q) = sum_(j=0)^m (-1)^(m-j) [m choose j]_q z^j
             = (-1)^m H_m(-z;q),                         (1)

where H_m is the classical Rogers-Szego polynomial. Its Gaussian-binomial denominators are nonzero at primitive q because all their exponents are less than N. Equivalently, use the polynomial recurrence

    T_0=1, T_1=z-1,
    T_n=(z-1)T_(n-1)+(1-q^(n-1))z T_(n-2).              (2)

In particular T_m(0)=(-1)^m and z^m T_m(1/z)=(-1)^m T_m(z).

Every m-node exponential representation must have T_m as its annihilator. Conversely, distinct nonzero roots of T_m matching the resonance guard give the required m-node representation by the residue construction below. Its residues cannot vanish because the shifted Hankel rank is m. If a guard fails, the audited m+1-branch construction remains available, including with delta=0. This proves the exact criterion without adding endpoints, changing the cycle order, or allowing confluent/higher-order resolvents.

## 2. Uniform resonance theorem

We first use the principal complex embedding q=exp(2 pi i/N), and later use Galois invariance only for algebraic claims.

Define monic continuous-q-Hermite polynomials

    S_0=1, S_1=x,
    S_n=x S_(n-1)-(1-q^(n-1))S_(n-2).

For any nonzero z and either choice of sqrt(z), recurrence (2) gives

    T_n(z)=(i sqrt(z))^n S_n((z-1)/(i sqrt(z))).         (3)

If |z|=1, the argument of S_n in (3) is real.

Let J be the m by m complex symmetric tridiagonal matrix with zero diagonal and edge j, joining vertices j-1 and j, equal to

    c_j = sqrt(2 sin(pi j/N)) exp(i[-pi/4+pi j/(2N)]),
    1<=j<m.

Then c_j^2=1-q^j, so det(xI-J)=S_m(x). Set

    D_jj=exp(i theta_j),
    theta_j=-pi/8 + pi(2j+1)/(8N),  0<=j<m.

The sum theta_(j-1)+theta_j equals the phase of c_j. Consequently

    J=D R D,

where R is a real symmetric, zero-diagonal Jacobi matrix with strictly positive off-diagonal entries sqrt(2 sin(pi j/N)). Also every theta_j lies strictly between -pi/8 and 0. Therefore B=D^(-2) has strictly positive real and imaginary parts as Hermitian diagonal matrices.

If a real nonzero t were an eigenvalue of J, a nonzero vector v would satisfy

    Rv=t Bv.

Taking v* of both sides, the left side is real and the right side has imaginary part t v* Im(B) v !=0. This is impossible. Thus the only possible real root of S_m is zero.

For even m, the zero-diagonal tridiagonal determinant is a nonzero signed product of c_1^2,c_3^2,...,c_(m-1)^2. Hence S_m(0)!=0. Equation (3) proves that T_m has no unit-circle zero in this principal embedding.

For odd m, R has a one-dimensional kernel, as follows directly by solving its tridiagonal recurrence from its first coordinate. Choose its real nonzero kernel vector v_0. In an orthonormal real basis beginning with v_0/||v_0||, R has a zero block of size one and an invertible complementary block. The coefficient of t in det(R-tB) is a nonzero real factor times v_0^T B v_0. Its real and imaginary parts are positive, so this coefficient is nonzero. Thus zero is a simple root of S_m. The change of variable in (3) has nonzero derivative at z=1; T_m has exactly one unit-circle root, namely the simple root z=1.

This proves, in the principal embedding, the stated gcd with z^N-1. For another primitive q'=q^a, gcd computations are carried into each other by the field automorphism q->q^a. Hence the monic gcd is 1 for every primitive q' when m is even, and z-1 when m is odd.

Important distinction: the argument proves an absence of all unit-circle roots only in the principal embedding (and its complex conjugate). It proves nonresonance in every embedding by algebraic Galois invariance. A general automorphism need not preserve the absolute values of algebraic roots.

## 3. Prime-order squarefreeness from a Hermite degeneration

Here q is temporarily an indeterminate. Let

    D_n(q)=Disc_z T_n(z;q) in Z[q],
    M=n(n-1)/2.

The following integral factorization is useful:

    D_n(q)=(q-1)^M E_n(q),
    E_n(q) in Z[q],
    E_n(1)=product_(j=1)^n j^j.                        (4)

For a short proof put q=1+epsilon^2 and z=1+epsilon x. Define

    U_n(x,epsilon)=epsilon^(-n)T_n(1+epsilon x;1+epsilon^2).

Recurrence (2) becomes

    U_n=x U_(n-1)
        - [(1+epsilon^2)^(n-1)-1]/epsilon^2
          (1+epsilon x) U_(n-2).

The quotient in brackets is integral. Thus U_n is a monic polynomial in x over Z[epsilon], and at epsilon=0 it is the monic probabilists' Hermite polynomial He_n, satisfying

    He_n=x He_(n-1)-(n-1)He_(n-2).

Translation/scaling of discriminants gives

    D_n(1+epsilon^2)=epsilon^(n(n-1)) Disc_x U_n.

This proves divisibility in (4) and identifies E_n(1)=Disc He_n. For completeness, the standard Hermite discriminant formula follows algebraically from He_n'=n He_(n-1) and the three-term recurrence: the magnitude of Res(He_n,He_(n-1)) is product_(j=1)^(n-1) j^j, with the alternating resultant sign canceled by the discriminant sign. Hence Disc He_n=product_(j=1)^n j^j, as claimed.

Now let N=p be an odd prime, n=m=(p-1)/2. Suppose T_m at q=zeta_p were not squarefree. Since zeta_p!=1, (4) implies E_m(zeta_p)=0. The monic irreducible cyclotomic polynomial Phi_p divides E_m in Z[q]. Evaluating at q=1 would imply

    p = Phi_p(1) divides product_(j=1)^m j^j,

which is impossible because m<p. Therefore T_m is squarefree.

This argument actually proves squarefreeness at primitive p^a-th roots whenever n<p. For the present target n=(p^a-1)/2, this does not settle powers with a>1. For composite orders with more than one prime divisor, Phi_N(1)=1 gives no contradiction. Those limitations are why the proof is not presented as a uniform composite-order theorem.

## 4. Explicit minimal coefficients and the forced diagonal

Assume m is even and T=T_m is squarefree, as is proved for prime N and certified at the finite sizes below. Let lambda_1,...,lambda_m be its roots. The previous theorem already ensures nonzero, nonresonant nodes.

Define the shifted numerator

    R(z)=sum_(j=0)^(m-1)
           [sum_(l=0)^(m-1-j) t_(j+1+l) f(l+1)] z^j.

It is the polynomial part of T(z) times the formal shifted moment series sum_(k>=0)f(k+1)z^(-k-1). Set

    c_s=R(lambda_s)/T'(lambda_s),
    b_s=c_s/lambda_s,
    a_s=(1-lambda_s^N)b_s,
    delta=1+R(0)/T(0).                                (5)

Partial fractions give R(z)/T(z)=sum_s c_s/(z-lambda_s). The first m shifted moments agree by construction, and the T recurrence supplies the next m. Thus

    sum_s b_s lambda_s^k=f(k),  1<=k<=2m.

At z=0 the partial fractions give sum_s b_s=-R(0)/T(0), so delta restores f(0)=1. None of the c_s, b_s, a_s vanishes, by shifted Hankel rank and the legal-node guards. Formula (5) is therefore a completely specified exact minimal branch bank; it does not promise individually expanded roots in K.

### Closed product for delta

The full (m+1) by (m+1) moment matrix M=[f(i+j)] is nonsingular. For an m-node representation, replacing only f(0) by 1-delta must lower its determinant to zero. Expanding in that one entry forces

    delta=det[f(i+j)]_(0<=i,j<=m)
           /det[f(i+j+2)]_(0<=i,j<m).

Both determinants factor into chirp diagonals and a Vandermonde determinant. Their ratio is

    delta=q^(-m^2) product_(i=0)^(m-1)(q^m-q^i)
         =(-1)^m q^(-m(m+1)/2) product_(j=1)^m(1-q^j).

It is nonzero. This formula is also the forced candidate diagonal in the illegal m-node cases; it does not override a failed node guard.

At N=5, T=z^2-(1+q)z+1 and delta=1-q^3-q^4+q^2, agreeing with the independently audited special case. At N=9 the formulas give four legal branches and one diagonal, now within the certified composite range.

## 5. Root-free implementation and honest costs

Let E=K[z]/(T), a squarefree m-dimensional K-algebra. Define

    b=z^(-1) R(z) T'(z)^(-1) in E,
    a=(1-z^N)b,
    ell(y)=Tr_(E/K)(a y).

All inverses exist. The bank is

    C x = delta x + Tr_(E/K)[a (I-zP)^(-1)x].           (6)

The algebra trace equals the sum of evaluations at the distinct roots, so (6) is exactly (5). It is an m-dimensional state, not a unit-cost scalar extension or a width-one Green branch.

A sufficient elementary setup uses O(N^2) K operations:

- Generate f and the product for delta: O(N).
- Construct T by Gaussian-binomial coefficients or recurrence (2): O(m^2).
- For an unclassified composite N, test gcd(T,T') exactly: O(m^2). The resonance theorem removes the need for a separate resonance search, though a control gcd can be retained at O(N^2).
- Form R, invert z and T' modulo T, compute z^N by companion multiplication, and invert 1-z^N: O(m^2+Nm).
- Precompute the trace functional using Newton sums or multiplication-matrix traces, then ell: O(m^2).

The stored plan uses O(N) K coefficients. To apply it, compute

    y_0=[sum_(k=0)^(N-1) z^k x_k]/(1-z^N),
    y_i=x_i+z y_(i+1),  i=N-1,...,1,  y_N=y_0,
    output_i=delta x_i+ell(y_i).

Horner evaluation, companion multiplication by z, and evaluating ell each cost O(m) per step. One general quotient multiplication by the precomputed closure inverse costs O(m^2). Total application cost is O(Nm+m^2)=O(N^2), with O(N+m) work storage. All closure and branch-summing costs are charged.

For N==3 mod 4 the optimal count remains m+1. The audited guarded pencil supplies an O(N^3)-setup, O(N^2)-application algorithm. For a composite N==1 mod 4 whose T is not squarefree, the same fallback is optimal by the exact criterion. Thus every N is decidable and constructible; only a closed-form answer for all composite N==1 mod 4 is unresolved.

These are exact field-operation counts with q supplied. They exclude rational-coordinate bit growth, computation of q, explicit root extraction, conditioning and floating-point stability. The finite certification scripts deliberately favor independent checks over asymptotically optimal setup.

If the preceding full-inverse construction is used, two successful m-branch chirp banks give N-1 nontrivial resolvent occurrences. Their two diagonal corrections and the existing diagonal can be added as matrices. Calling that one legal diagonal occurrence requires a grammar allowing an arbitrary diagonal, possibly with zero entries; otherwise retaining the three separate nonzero scalar-chirp diagonal terms avoids silently assuming nonsingular combined endpoints. No minimum for the unrestricted full inverse is claimed.

## 6. Exact evidence and what it proves

`MODULAR_CERTIFICATES.json` contains one certificate for every N==1 mod 4 from 5 through 1001, inclusive: 250 sizes. Each includes a proven prime p==1 mod N, a primitive Nth root q_bar in F_p, T coefficients, and explicit polynomials U,V with

    U T + V T' = 1 in F_p[z].

These certify characteristic-zero squarefreeness, not merely behavior of an unrelated finite-field example. The evaluation homomorphism Z[zeta_N]->F_p exists because q_bar has exact order N and p does not divide N. A zero characteristic-zero discriminant would reduce to zero under every such homomorphism, contradicting this Bezout identity. Galois conjugacy makes each certificate cover every primitive complex q and both chirp signs.

`verify_certificates.py` does not import the generation/check script. It proves primality by trial division, verifies exact multiplicative order, reconstructs T with the three-term recurrence rather than the coefficientwise Pascal recurrence used by the generator, verifies the explicit Bezout identities, and directly evaluates T at every cycle root in the saved finite field. Every final certificate has both guards clear.

Some initial finite primes have extra resonance even though characteristic-zero resonance has been excluded. These are bad reductions, not characteristic-zero counterexamples. The saved trial history makes them visible; no zero finite-field resultant is treated as a liftable obstruction.

`check_classification.py` is fresh standard-library code. It independently checks shifted orthogonality, reciprocity, the product and rational-numerator formulas for delta, all N moments, and actual root-free scans. Finite bank controls use both signs at N=5,9,13,17,21,25,45,65,245; every basis vector is checked through N=25, and two fully specified input vectors are checked at each larger size. Characteristic-zero controls use independently implemented rational cyclotomic arithmetic at N=3,5,7,9: the odd-parity cases check the exact resonance gcd; N=5,9 check every basis-vector scan. Literal regular-representation traces, collected as coefficient traces of multiplication by monomials, are used instead of a prewritten trace routine. Direct integer Sylvester determinants also check the Hermite discriminant formula through degree 12. In total the bank controls check 918 moment identities and 4,892 scan output entries; four additional odd-parity characteristic-zero controls check their exact resonance gcd.

Finite certificates do not prove a uniform theorem for untested composite N. They do remove all doubt for their listed N, including N=45 and N=245 from the existing restricted-family examples.

## 7. Literature and attribution

The polynomial in (1), its three-term recurrence, and its alternating-value identity are established Rogers-Szego mathematics. C. Ryan Vinroot, *Multivariate Rogers-Szego polynomials and flags in finite vector spaces*, Section 1 and equation (2.3), explicitly gives those definitions and identities: https://arxiv.org/abs/1011.0984 . The alternating-value identity also proves T_(2k)(1)=product_(j=1)^k(1-q^(2j-1)) directly.

The continuous-q-Hermite change of variables and recurrence are standard; see Johann Cigler, *Continuous q-Hermite polynomials: An elementary approach*, Section 5.2: https://homepage.univie.ac.at/johann.cigler/preprints/contqhermite.pdf . The congruence argument in Section 2 is supplied in full here, so no positive-measure theorem is assumed for complex q.

The finite complex-moment, formal-orthogonality and minimal-realization framework is established; see Stefano Pozza and Miroslav S. Pranic, *The Gauss quadrature for general linear functionals, Lanczos algorithm, and minimal partial realization*: https://arxiv.org/abs/1903.11395 .

This is a project-specific branch-classification extension with elementary proofs, explicit coefficients and exact certificates. These sources are not an exhaustive priority search, and publication-level novelty of the specialization is unverified. No generalized q-discriminant formula is confused with the ordinary derivative discriminant needed here.

## 8. Exact unresolved bottleneck and stopping boundary

The remaining statement is narrowly formulated:

    For every composite N==1 mod 4, with m=(N-1)/2,
    is Disc_z H_m(z;zeta_N) nonzero?

Equivalently, does Phi_N(q) ever divide the integer polynomial E_m(q) from (4)? A proof of nondivisibility would finish the closed-form classification. A counterexample would force Q_min=m+1 at that N despite a free diagonal. The original zero and resonance guards no longer need to be solved. Neither the finite certificates nor the prime-order Hermite argument is a substitute for that missing composite-order proof.

Both input packages were read as data, their manifests verified, and all 22 source files hashed before and after. No uploaded or predecessor constructor/checker code was executed or imported; prior seals remain unchanged. The output manifest seals this report, executable fresh controls, the exact certificates and provenance records.
