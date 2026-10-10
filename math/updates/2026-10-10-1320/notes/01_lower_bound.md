# Independent verdict: the N=7 two-row obstruction

10 October 2026

## Verdict and scope

**Accepted in characteristic zero: every representation of the negative Fourier matrix of length seven in the stated signed magnetic-resolvent bank grammar uses at least four banks with each delta sign, and hence at least eight banks in total.**

This is a lower bound only. This review supplies no eight-bank witness and does not determine the exact minimum. It makes no claim about runtime improvement, a general FFT lower bound, or historical priority. The previous mirrored six-bank result remains valid, but is subsumed as a mathematical consequence of this stronger, separate two-row obstruction.

The decisive independent certificate is an exact polynomial identity

    U(Y) R(Y) + V(Y) F(Y) = 1

in Q(q)[Y], where q is a primitive seventh root. The full rational coefficients of U and V are recorded in [EXACT_ROW_CERTIFICATE.json](../controls/lower/EXACT_ROW_CERTIFICATE.json), and the fresh control verifies the identity by exact multiplication. Thus no common root can exist in any characteristic-zero extension field. There is also a separately computed good-reduction certificate: at q=7 modulo 29, the resultant of the two unnormalized degree-nine polynomials is 24, which is nonzero. This is not a finite-field parameter-search argument.

## Reviewed frozen source

The reviewed author proof, “N=7: a two-row obstruction to three banks on either delta side,” has SHA-256 `a9490da5bba04ff093afc713f165cc18a403cd6ea1cb09da59e922e618c17866`. The source coefficient and quotient-certificate data are included under [lower-bound controls](../controls/lower/README.md). All exact moment and obstruction coefficients, both modular polynomials, the modular Bezout identity, every entry of the 9-by-9 multiplication matrix, and its inverse agree with the independent controls. [Source acceptance](../SOURCE_ACCEPTANCE.json) records the original source hashes and the public export transformations.

The author proof obtains the per-side lower bound by combining the new obstruction with the accepted earlier bound. This independent review additionally supplies a direct corner-support and legal zero-padding argument, making the strengthened lower bound self-contained in the bank grammar.

## The grammar, normalization, and literal checks

Let S e_i=e_(i+1), T e_i=q^i e_i, with indices modulo seven, and W_(a,b)=S^a T^b. A bank is

    (1/7) sum_(j=0)^6 w_j
      (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),

with epsilon,delta in {+1,-1} and Delta=1-alpha^7-beta^7 nonzero.

Its Weyl expansion has the form

    sum_(ell=0)^6 h_ell sum_(r=0)^(6-ell)
      alpha^r [r+ell choose ell]_(q^(epsilon delta))
      W_(epsilon r,delta ell).

For impossibility, the h_ell can be arbitrary independent scalars. This enlarges the legal class and therefore covers every beta and phase-weight choice in the original grammar. The fresh literal control verifies, coefficient by coefficient in symbolic alpha and beta, the Gaussian expansion of every power from zero through seven for all four orientations. In particular, the seventh power is (alpha^7+beta^7)I, so the finite geometric numerator gives the actual inverse whenever Delta is nonzero.

For F[k,t]=q^(-kt), a direct trace calculation gives

    c(a,b)=(1/7) sum_t q^(-bt-(t+a)t)
          = C q^(2(a+b)^2),
    C=(1/7) sum_t q^(-t^2) != 0.

The control checks all 49 coefficients exactly. Normalize amplitudes by C, and write f(a,b)=q^(2(a+b)^2).

A bank's row coefficient, apart from its row amplitude, is

    alpha^r [r+ell choose ell]_(q^(epsilon delta))

when r+ell<=6 and zero otherwise, where r=[epsilon a]_7 and ell=[delta b]_7. This support test is used without extrapolating generic-rank conclusions.

## The first isolated row

Suppose the positive-delta side consists of (++ with x), (++ with z), and (-+ with y). The number and parameters of negative-delta banks are unrestricted. At b=1 they have ell=6, and hence vanish at every a=1,...,6.

At a=6 the singleton is the only contributor. Define H=q/(1+q). The equation is h_y y=H, so y is nonzero. At a=1 only the duplicated orientation contributes, giving

    A+B=1, where A=h_x x/H and B=h_z z/H.

There has been no division by x or z. For a=2,...,5, write

    G_a=[a+1]_q,
    B_a=[8-a]_(q^-1),
    m_(a-1)=f(a,1)/(H G_a) - (B_a/G_a)y^(6-a).

All displayed scalar denominators are nonzero for a primitive seventh root. The four remaining equations are

    A x^j+B z^j=m_j(y), j=1,2,3,4.

Define m_0=1 and

    D=m2-m1^2,
    Sn=m3-m1*m2,
    Pn=m1*m3-m2^2,
    R=D*m4-Sn*m3+Pn*m2.

Every two-atom sequence has its 3-by-3 Hankel determinant zero, so R(y)=0. Moreover, directly from the node recurrence,

    Sn=(x+z)D,    Pn=xzD.

These are polynomial identities. They require no inverse of D, no distinctness of x and z, and no nonzero-node or nonzero-amplitude assumption. The independent control derives the moments from the literal row coefficients rather than trusting supplied coefficients.

## The second isolated row

At b=2 every negative-delta bank has ell=5. It can contribute only at a=0,1,6 and therefore vanishes at a=2,3,4,5, regardless of how many such banks occur.

Let k_x,k_z,k_y be the b=2 amplitudes of the three positive-delta banks. At a=5, only the singleton contributes, so

    k_y=1/(y^2 [4 choose 2]_(q^-1)).

This division is legitimate because y was already forced nonzero. Set

    n2=q^4/[4 choose 2]_q,
    n3=(q-y^2 [6 choose 2]_(q^-1)/[4 choose 2]_(q^-1))
        /[5 choose 2]_q,
    n4=(q^2-y [5 choose 2]_(q^-1)/[4 choose 2]_(q^-1))
        /[6 choose 2]_q.

The a=2,3,4 equations are exactly

    k_x x^j+k_z z^j=n_j(y), j=2,3,4.

Therefore n4=(x+z)n3-xz n2. Multiplying by D and applying the two polynomial identities from the first row gives the necessary condition

    F(y)=D*n4-Sn*n3+Pn*n2=0.

There is still no division by D, x, z, x-z, any forward amplitude, or a discriminant. Cases with coincident nodes, zero forward nodes, vanishing forward amplitudes, or D=0 are all included. No rank condition is inferred from a zero determinant. The proof uses only necessary identities, followed by their certified incompatibility.

## Exact incompatibility and good reduction

The independent exact calculation obtains deg(R)=deg(F)=9. Its extended Euclidean identity U R+V F=1 in Q(q)[Y] is checked by multiplication and recorded with all coefficients. This identity alone proves that the necessary pair R(y)=F(y)=0 is impossible in every characteristic-zero extension field containing a primitive seventh root.

For an additional small certificate, specialize q to 7 modulo 29. The number 7 has order seven in F_29, and Phi_7(7)=0. Every scalar denominator in the derivation has nonzero image. The reduced polynomials, in increasing powers of Y, are

    Rbar=[23,26,9,23,13,0,11,16,10,8],
    Fbar=[28,5,17,4,2,15,24,10,28,3].

Both leading coefficients remain nonzero. An explicit modular Bezout identity is verified. The resultant is 24 modulo 29. A separately constructed 18-by-18 Sylvester matrix, with ascending coefficient rows and columns Y^j R followed by Y^j F for j=0,...,8, has determinant 5 modulo 29; its sign is opposite the conventional resultant in these odd degrees. Both are nonzero.

Equivalently, multiplication by F in the monic rank-nine quotient has determinant 19 modulo 29. This agrees with 24 divided by 8^9 modulo 29. This norm certificate is valid over the local coefficient ring at (29,q-7): all scalar denominators and the leading coefficient of R are units there, and the monic quotient is finite free with basis 1,Y,...,Y^8. Nonzero reduction of the multiplication determinant implies a nonzero characteristic-zero determinant and makes F a unit after passing to Q(q). No assumption that R is squarefree is needed, and no finite-field root enumeration is used.

## All orientation counts and both signs

The proof above excludes exactly three positive-delta banks in multiplicities (2,1) for the two epsilon signs. To cover all cases, the independent literal control checks the following symmetries on all 28 signed phase branches.

1. Transposition uses S^T=S^-1 and T^T=T. It maps (epsilon,delta) to (-epsilon,delta), reindexes j to -j, preserves alpha, beta, and Delta, and preserves F because F^T=F. Thus it also excludes positive-delta multiplicities (1,2).
2. Simultaneous row/column index reflection uses P e_i=e_(-i). Conjugation by P maps (epsilon,delta) to (-epsilon,-delta), preserves the phase-index convention and Delta, and preserves F. Consequently the same exclusion applies to three banks of negative delta.
3. At each of (a,b)=(3,3),(4,3),(3,4),(4,4), exactly one orientation has support, respectively (++),(-+),(+-),(--). The target coefficients are nonzero. Therefore all four orientations are required.
4. A side with only two banks must consequently contain one of each epsilon sign. It can be padded by a legal zero bank, for example alpha=beta=1 and all w_j=0, for which Delta=-1. This gives the already excluded three-bank class. Equivalently, the enlarged independent-amplitude argument directly permits a zero extra amplitude column. Sides with zero or one bank are already excluded by the four corners.

It follows that each delta side requires at least four banks. All six-bank multiplicities, all seven-bank splits, and their degenerate parameter strata are covered. The lower bound is at least eight; attainment remains open in this review.

## Independence and reproduction

The fresh controls are [verify_isolated_rows.py](../controls/lower/verify_isolated_rows.py) and [verify_literal_model.py](../controls/lower/verify_literal_model.py). They use SymPy for exact cyclotomic-field and univariate-polynomial arithmetic. No authored or predecessor research script was executed, imported, compiled, or parsed. Author JSON coefficient/certificate data are used only for comparison after independent derivation. [The scoped receipt](../receipts/lower_acceptance.json) identifies the exact frozen sources and hashes, the comparison result, and the independent output hashes.

Run each fresh control with Python 3 and SymPy. Each writes its own JSON results next to the script. This review performs no remote writes.
