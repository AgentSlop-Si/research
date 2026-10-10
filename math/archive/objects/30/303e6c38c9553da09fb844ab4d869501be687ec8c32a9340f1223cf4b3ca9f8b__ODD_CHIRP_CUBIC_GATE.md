# A uniform odd-length chirp spectral control, with the remaining B obligation

## Result

For every odd length N, a uniformly generated diagonal chirp A gives the exact scalar-cubic relation (F_N A)^3=N G I, where G is an explicitly computable quadratic Gauss sum. For unnormalized complex Fourier and N>1, this produces a mathematically Fourier-compatible feedback pair with an explicit cubic loop annihilator. A is genuinely O(N)-cheap. No O(N) application or paired-Green realization of the required B is supplied. Consequently this is a positive low-degree spectral control, not a fast Fourier construction.

## Primary-source convention check

The checked primary paper by Gurevich, Hadani and Howe defines the positive-exponent, unnormalized Fourier transform, distinguishes its unitary normalization, and gives F^2=N R and F^4=N^2I. Its DFT/Weil relation includes a nontrivial scalar. See Sections 2.1–2.2 in the arXiv version: https://arxiv.org/html/0808.2447 ; published version: https://doi.org/10.1093/imrn/rnp242 .

Fernández-Pousa's primary paper explicitly treats parity-correct modular inverses and quadratic-chirp/Gauss-sum Fourier pairs by completion of the square. Its displayed DFT uses the negative exponent, unlike the convention below, so its signs cannot be copied without conversion. See Theorem 1 and Proposition 4: https://arxiv.org/html/1612.03487 ; published version: https://doi.org/10.1364/JOSAA.34.000732 .

The precise cubic and feedback identities below are derived directly so that neither projective phase nor normalization is assumed. The Fourier/Gauss-sum mechanism is classical; no novelty claim is made.

## 1. Definitions and full scalar-cubic proof

Let N>=3 be odd. Work over a field E containing a primitive Nth root omega, with characteristic not dividing 2N. The main intended setting is exact complex arithmetic. Write h=(N+1)/2 as an integer residue modulo N, so 2h=1 modulo N. Define

    F[i,j]=omega^(ij),
    Fbar[i,j]=omega^(-ij),
    A[j,j]=omega^(h j^2),
    G=sum_(j=0)^(N-1) omega^(h j^2),
    Gminus=sum_(j=0)^(N-1) omega^(-h j^2),
    M=F A,
    c=N G.

Fbar denotes exponent reversal; over a general field it is not a conjugation operation. We have Fbar F=F Fbar=N I.

Completion of the square modulo N gives

    h j^2+(i+k)j = h(j+i+k)^2-h(i+k)^2.

Consequently

    (M^2)[i,k]
      =omega^(h k^2) sum_j omega^(h j^2+(i+k)j)
      =G omega^(-h i^2-i k),

and therefore

    M^2=G A^(-1) Fbar,
    M^3=G A^(-1) Fbar F A=N G I=cI.                  (1)

This proof works for every odd N, including composite N. No prime-length metaplectic representation is silently substituted for the cyclic-ring calculation.

G is nonzero. To see this without a Gauss-sum sign formula, change variables u=x-y, v=x+y, a bijection modulo odd N:

    G Gminus=sum_(x,y) omega^(h(x^2-y^2))
            =sum_(u,v) omega^(h u v)=N.                (2)

The inner sum vanishes for every nonzero u because h is a unit modulo N and omega is primitive. Since N is nonzero in E, both sums are nonzero.

For odd N>=5 the minimal polynomial of M has degree exactly three. Any nonzero relation alpha M^2+beta M+gamma I=0 with alpha=0 is ruled out by the nonzero off-diagonal entries of M and then by the diagonal. If alpha!=0, the same off-diagonal equations force beta!=0 and require the ratio (M^2)[0,j]/M[0,j]=G omega^(-h j^2) to be constant for j=1,2. This would imply omega^(3h)=1, hence N divides 3, a contradiction. Relation (1) supplies the matching upper bound. At N=3 only the degree-at-most-three statement is claimed.

## 2. Uniform generation and normalization cautions

The diagonal phases do not need a dense Fourier matrix. Starting with a0=1 and r0=omega^h, the recurrences

    a_(j+1)=a_j r_j,
    r_(j+1)=omega r_j

generate a_j=omega^(h j^2) in O(N) field operations. Sum the a_j to get G in O(N) additional additions. Compute omega^h by binary powering in O(log N) operations or a root stream; both fit the O(N) cold budget. A applies in N scalar multiplications; A^(-1) can be generated with the inverse phase recurrence. No new square root, cube root or Gauss-sum sign oracle is needed. A is also admitted by the paired-Green class as two zero-edge-weight identity Green plans with suitable nonsingular diagonal endpoints, for example two copies of A/2.

Equation (1) is scalar-cubic closure, not literal order three for the unnormalized operator. Over C, if U=F/sqrt(N), then

    (U A)^3=(G/sqrt(N)) I.

Making the cube exactly I would require an additional scalar normalization. Its cost and availability should be stated if used; this argument does not use it. In particular, substituting U for F changes the scalar and can change the nonresonance condition below.

The chirp sign is equally important. If Aminus=A^(-1), the corresponding calculation gives

    (F Aminus)^3=N Gminus R,

where R e_j=e_(-j modN). For N>2 this is generally not scalar; squaring gives a degree-six annihilator. The positive exponent in A above is essential to the displayed cubic.

## 3. The unique feedback B and the cubic loop annihilator

Assume the explicit nonresonance guard 1+c!=0. Since M^3=cI,

    (I+M)^(-1)=(I-M+M^2)/(1+c).

The unique B that yields the exact target Fourier transfer with this A is

    B=(F^(-1)+A)^(-1)=(I+M)^(-1)F
     =[F-F A F+c A^(-1)]/(1+c).                       (3)

The last identity uses M^2 F=c A^(-1), which follows from (1). Equivalently,

    B=[F-G A^(-1)Fbar A^(-1)+c A^(-1)]/(1+c),

because F A F=G A^(-1)Fbar A^(-1). The order of all factors is retained.

Set K=BA=(I+M)^(-1)M. Then I-K=(I+M)^(-1), and

    (I-K)^(-1)B=(I+M)(I+M)^(-1)F=F.

Thus both the source's covariance and seed certificates hold as exact algebraic identities. This is not evidence of cheap B: equation (3) literally contains Fourier actions.

Since K and I-K are rational functions of M, they commute. From K(I-K)^(-1)=M and M^3=cI we get

    mu(K)=0,
    mu(z)=z^3-c(1-z)^3
         =(1+c)z^3-3cz^2+3cz-c,
    mu(1)=1.                                        (4)

Under 1+c!=0 this is a cubic annihilator with no annihilator resonance. For N>=5 its degree is minimal: a smaller polynomial in K would, after substituting K=M(I+M)^(-1) and clearing its at-most-quadratic denominator, give a nonzero polynomial of the same or smaller degree annihilating M. The inverse Möbius map ensures that substitution cannot make a nonzero scalar polynomial identically zero.

The finite closure inverse is explicitly

    (I-K)^(-1)=(1+c)I+(1-2c)K+(1+c)K^2.

Accordingly, if B were independently proved uniformly O(N)-cheap, the transfer would use three B calls and two diagonal A calls, plus O(N) vector arithmetic. Equation (3) alone does not supply that premise.

## 4. Complex nonresonance versus finite-field resonance

Over C, Gminus is the complex conjugate of G. Equation (2) gives |G|=sqrt(N), so |c|=N^(3/2)>1 at N>1. Hence c cannot equal -1: the unnormalized complex feedback is nonresonant at every odd N>=3.

This argument does not transfer to arbitrary finite fields. For example, over F7 with N=3, omega=2 and h=2, A=diag(1,4,4), G=2 and c=6=-1. Then I+M is singular. The cubic identity remains true, but the feedback B in (3) is unavailable. The exact verifier includes this forbidden-pole control rather than silently dropping the guard.

The normalized operator U=F/sqrt(N) has scalar G/sqrt(N) on cubing, so its analogue of the guard must be checked separately; the unnormalized magnitude argument no longer applies.

## 5. A small but indispensable full-rank correction

Over C, A is unitary and M/sqrt(N) is unitary. From B=(I+M)^(-1)M A^(-1),

    B-A^(-1)=-(I+M)^(-1)A^(-1).

Every singular value of I+M lies between sqrt(N)-1 and sqrt(N)+1. Therefore

    1/(sqrt(N)+1) <= ||B-A^(-1)||_2 <= 1/(sqrt(N)-1).

The correction has full rank N, since both factors on the right are invertible. Thus B approaches the diagonal inverse chirp in operator norm at rate Theta(N^(-1/2)); it is not a low-rank correction. Replacing B by A^(-1) makes BA=I, so I-BA=0 and the feedback solve ceases to exist. The exact correction is indispensable even though its norm is small.

The actual feedback gap is I-BA=(I+M)^(-1), with singular values also of order N^(-1/2). This is a scale statement, not by itself a claim of a large condition number: its condition number is bounded by (sqrt(N)+1)/(sqrt(N)-1). No stable floating-point algorithm is established by the exact-arithmetic closure.

## 6. What remains for the requested architecture

This construction solves a real part of the spectral problem: an explicit all-odd-length cheap A and its Gauss scalar give a uniform cubic closure with correct Fourier phases at the level of the forced feedback equations. It uses no unknown conjugator and does not discover coefficients by dense diagonalization.

The unresolved obligation is an O(N)-generated sum of two allowed independently ordered Green plans that equals the B in (3), or another admissible B application formula with a fully charged O(N) cost. Directly applying F, Fbar, or F A F inside (3) does not meet that obligation. The dense matrices used in verification are not a B generator.

A single diagonal-ended Green B is already impossible here for N>2: B^(-1)=F^(-1)+A has every off-diagonal entry nonzero, while the inverse of one such Green map has at most one off-diagonal nonzero per row. This elementary observation does not exclude a sum of two Green maps, whose inverse need not be sparse.

Thus the branch is a positive uniform cubic spectral control with a sharply isolated synthesis bottleneck. It is not an all-N or odd-N faster FFT, and no two-Green realization of B is claimed.

## 7. Exact controls and provenance

The newly authored check_odd_chirp.py verifies the phase recurrence, Gauss product, both chirp-sign cube formulas, cubic minimal degree where claimed, the three displayed B formulas, feedback output, covariance/seed, loop annihilator and its polynomial inverse over prime fields at odd prime and composite lengths. It checks all basis vectors for the Horner closure evaluator. A separate F7 case verifies the required resonance warning.

All source conventions and public links above were checked on 2026-10-09. The ACFF package motivating the feedback use has Library ID [private-id] and ZIP SHA-256 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9. No uploaded code is imported or run; the script uses only newly authored local matrix helpers. The completed checks pass 14 nonresonant cases through N=63, including odd composites; 278 basis vectors and 9,998 Fourier output entries; and one explicit resonant F7,N3 control. Actual per-case data are in ODD_CHIRP_RESULTS.json.
