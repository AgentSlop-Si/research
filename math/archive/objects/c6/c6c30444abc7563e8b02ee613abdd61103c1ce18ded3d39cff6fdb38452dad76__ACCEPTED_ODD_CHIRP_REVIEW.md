# Independent odd-chirp cubic feedback review

Date: 2026-10-09 UTC. Verdict: the all-odd-length scalar-cubic relation, guards, exact degree claim, forced B formulas, and full-rank correction statement are correct. A is uniformly cheap; a cheap or paired-Green B remains unconstructed. This is a positive spectral identity, not a faster FFT.

## 1. Conventions and direct all-length proof

Let N>=3 be odd and work in a field of characteristic not dividing 2N with a specified primitive Nth root omega. Let h=(N+1)/2 modulo N, F[i,j]=omega^(ij), Fbar[i,j]=omega^(-ij), A[j,j]=omega^(h j^2), G=sum_j A[j,j], Gminus=sum_j A[j,j]^(-1), M=FA, and c=NG. Fbar denotes reversed exponent, not field conjugation in general.

The square completion h j^2+(i+k)j=h(j+i+k)^2-h(i+k)^2 modulo N gives

M^2=G A^(-1)Fbar,
M^3=NG I=cI.

These statements use only arithmetic in Z/NZ and a primitive root, so composite odd lengths are included. They do not require a prime-field Weil representation theorem.

The change of variables u=x-y,v=x+y is bijective because N is odd. It yields G Gminus=sum_(u,v) omega^(huv)=N. For nonzero u the inner geometric sum vanishes, even at composite N, because h is a unit and omega is primitive. Thus G and c are nonzero under the field guard.

For N>=5 the minimal polynomial of M is exactly cubic. A relation alpha M^2+beta M+gamma I=0 with alpha=0 is impossible unless all coefficients vanish, using nonzero off-diagonal Fourier entries. If alpha!=0, off-diagonal positions force beta!=0 and equal ratios (M^2)[0,j]/M[0,j]=G omega^(-h j^2) for j=1 and 2. This requires N to divide 3, impossible. The existing cubic gives the matching upper bound. At N=3 only an at-most-cubic statement is warranted; the independent nonresonant N=3 control has degree two.

## 2. Signs, generation, and normalization

Starting with a0=1 and r0=omega^h, the recurrences a_(j+1)=a_j r_j and r_(j+1)=omega r_j generate all chirp phases in O(N), since 2h=1 modulo N. Summing them gives G. Initial powering costs O(log N), absorbed by the linear budget. No Gauss-sum sign, square root, cube root, eigensolver, or target Fourier call is needed to generate A and c.

A is nonsingular diagonal, hence it can be represented by two half-scaled diagonal zero-mask Green plans under char!=2. This proves A's cheapness and admissibility, not B's.

The opposite chirp sign gives (F A^(-1))^3=NGminus R, where R reverses indices. It is generally not a scalar cube for N>2. For normalized U=F/sqrt(N), the correct positive-chirp cube is (UA)^3=(G/sqrt(N))I. The source correctly retains these phase and normalization distinctions.

The classical Fourier/Gauss-sum convention context is supported by the primary papers [Gurevich, Hadani and Howe](https://arxiv.org/html/0808.2447) and [Fernandez-Pousa](https://arxiv.org/html/1612.03487). The second uses a different Fourier-sign convention. The identities in this review are proved directly above rather than imported with an unverified scalar or sign. No novelty claim is made.

## 3. Feedback and the exact cubic inverse

Under the separate nonresonance guard 1+c!=0,

(I+M)^(-1)=(I-M+M^2)/(1+c),
B=(F^(-1)+A)^(-1)=(I+M)^(-1)F
 =[F-F A F+c A^(-1)]/(1+c).

The alternative Fbar expression follows from FAF=G A^(-1)Fbar A^(-1). All factors retain their required order.

Then K=BA=M(I+M)^(-1), I-K=(I+M)^(-1), and (I-K)^(-1)B=F. Covariance and the seed therefore hold algebraically. These formulas explicitly contain Fourier operators; they do not supply an O(N) implementation of B.

Clearing the rational relation M=K(I-K)^(-1) yields

mu(z)=z^3-c(1-z)^3
 =(1+c)z^3-3cz^2+3cz-c,
mu(K)=0, mu(1)=1.

The inverse is exactly

(I-K)^(-1)=(1+c)I+(1-2c)K+(1+c)K^2.

The signs and coefficient order are correct. At N>=5, a lower-degree annihilator of K would produce, after the invertible Mobius substitution and clearing at most a quadratic denominator, a nonzero lower-degree annihilator of M. Hence the loop degree is exactly three. This argument does not assume distinct cubic roots and remains algebraically valid in positive characteristic permitted by the guards.

If B were independently uniformly cheap, the Horner evaluator would use three B calls and two diagonal A calls plus vector work. Merely writing the displayed B formula does not establish that premise.

## 4. Resonance and complex norm claims

Over C, Gminus is the conjugate of G, so |G|=sqrt(N), and |c|=N^(3/2)>1. Thus c cannot equal -1 for unnormalized complex Fourier at N>=3. This is not a finite-field argument and does not transfer to the unitary-normalized scalar unchanged.

The explicit F_7, N=3, omega=2 control gives A=diag(1,4,4), G=2, c=6=-1. The cubic relation holds but I+M has rank one and cannot be inverted. The source correctly includes this forbidden pole.

Over C, A is unitary and M/sqrt(N) is unitary. Thus all singular values of I+M lie between sqrt(N)-1 and sqrt(N)+1. The exact identity

B-A^(-1)=-(I+M)^(-1)A^(-1)

proves full rank N of that specific correction and the norm envelope

1/(sqrt(N)+1)<=||B-A^(-1)||_2<=1/(sqrt(N)-1).

Dropping the correction sets BA=I and makes I-BA identically zero, so small norm does not permit exact omission. The shrinking feedback scale does not by itself mean a growing condition number; the condition bound (sqrt(N)+1)/(sqrt(N)-1) is valid. No floating-point stability or bit-complexity theorem follows.

Full rank here concerns the displayed difference from A^(-1). It is not a lower bound against every alternative sparse baseline, nor a proof of high arithmetic complexity.

## 5. Single-Green scope

The source correctly states that a single diagonal-ended Green B is impossible at odd N>2: B^(-1)=F^(-1)+A has every off-diagonal entry nonzero, whereas such a Green inverse has at most one off-diagonal nonzero per row.

With arbitrary independent monomial endpoints, only the total row-degree-two bound is automatic. It already excludes a one-Green realization for odd N>=5 because B^(-1) has at least N-1>2 nonzeros per row. It does not justify the same N=3 conclusion without an additional argument. Neither statement excludes a sum of two Green maps.

## 6. Independent exact checks

The reviewer authored a separate standard-library checker and executed no uploaded or constructor code. Ten nonresonant cases cover N=3,5,7,9,15,21,25,27,35,63 over explicitly checked prime fields. These include odd composites and independent choices of test fields.

The tests verify phase recurrence, G Gminus=N, both chirp-sign cube formulas, minimal degree of M and K where asserted, all B formulas, full-rank correction, the cubic annihilator, polynomial inverse, and every basis-vector output of the three-B Horner evaluator. All 210 basis inputs pass. A separate F_7,N3 resonance test verifies singularity and preserves the guard rather than dividing by zero.

The N=3 nonresonant control has degree two, consistent with the source's exception. Every tested N>=5 has degree three. The B implementations in these controls use dense Fourier matrices and are explicitly labeled oracle expressions; the tests do not establish cheap B.

An isolated copied replay reproduces all saved results with Python's standard library only. The source snapshot, independently authored verifier, results, and proof are sealed.

## 7. Remaining construction problem

The result gives an all-odd-length cheap A, an explicit scalar c, and a valid small-degree Fourier-compatible feedback specification. The unresolved step is a uniformly generated O(N) implementation or admissible two-Green realization of the forced B. Direct F, Fbar, or FAF applications cannot be hidden in that step. No all-length or odd-length faster FFT has been constructed.
