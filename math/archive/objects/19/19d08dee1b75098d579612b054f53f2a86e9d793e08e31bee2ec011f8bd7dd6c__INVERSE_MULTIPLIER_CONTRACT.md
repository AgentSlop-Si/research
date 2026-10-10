# Q30: inverse multipliers, exact preparation, and the finite-word boundary

10 October 2026. Fresh proof reconstruction. Supplied files were treated as inert text; no supplied program was executed, imported, compiled, or AST-parsed. The new exact arithmetic controls are independently authored in `fresh_backend_certificates.py`.

## Disposition

The conditional inverse-application theorem is closed below. Full nondegenerate quadratic chirps have an explicitly certified, asymptotically linear-time finite-word multiplier preparation. Hero17's general boundary annihilator is not such a chirp. A new first-order coefficient recurrence and second-order spectral recurrence give a fully charged O(N) **exact-field preparation**, but do not certify O(N) bounded-word preparation or the needed complex spectral lower bound. That finite-word transfer remains conditional. This is not a new unrestricted exact fast Fourier algorithm, nor a lower bound excluding a better preparation method.

## 1. Exact conditional error contract

Use the negative unitary Fourier transform U, and convolution C_h with unnormalized Fourier eigenvalues lambda_k=sum_j h_j exp(-2 pi i jk/N). Assume every lambda_k is nonzero. Write

D=diag(mu_k), mu_k=1/lambda_k, A=C_h^{-1}=U* D U,
M=max |mu_k|, m=min |mu_k|, kappa=M/m.

Suppose two potentially nonlinear transform routines satisfy, on every admissible input they receive,

||F(v)-Uv||_2 <= delta ||v||_2,
||G(v)-U*v||_2 <= delta ||v||_2.

Assume stored multipliers satisfy max_k |mu_tilde_k-mu_k|<=eta. The diagonal executor H must satisfy

||H(v)-diag(mu_tilde)v||_2 <= rho ||v||_2.

Then y=G(H(F(x))) satisfies the exact bound

||y-Ax||_2 <= [M(2 delta+delta^2)+(eta+rho)(1+delta)^2] ||x||_2.       (1)

Proof: put v=F(x), z=H(v). We have ||v||<=(1+delta)||x||, ||z||<=(M+eta+rho)(1+delta)||x||, and
||z-DUx|| <= [M delta+(eta+rho)(1+delta)]||x||.
Add the last-transform error delta||z|| and simplify. No linearity of F or G was used.

Since ||Ax||>=m||x||, the relative **output** error is bounded by the bracket in (1) divided by m. If eta+rho<=delta M and delta<=1/4, it is at most

kappa[(1+delta)^3-1] <=4 kappa delta.                         (2)

Thus delta=epsilon/(4 kappa), for epsilon<=1, is sufficient. Input-relative error instead has scale M; omitting that scale is incorrect. Exact unitary endpoint chirps in Q=L C_h R preserve this theorem for Q^{-1}=R^{-1} A L^{-1}. If these chirps are implemented approximately, charge their errors as two additional stages; they are not exact finite-word operations. With each relative stage/diagonal-coefficient budget <=delta, the same product calculation gives kappa[(1+delta)^5-1]<=9 kappa delta for delta<=1/4, so delta=epsilon/(10 kappa) suffices.

The finite-word compiler transfers only when all intermediate vectors and constants meet its representation/range contract, multiplier preparation is separately charged, and

log(1/epsilon)+log kappa=o(log N).

Use the compiler's stated finite-precision domain and charged fallback outside it. The asymptotic condition alone does not cover arbitrary finite exceptional precision. A convenient explicit range assumption is a certified power-of-two scaling making the multiplier magnitudes polynomially bounded above and below, with its exponent and rescaling cost charged. The normalized operator version of (1) is often preferable.

### Preparing reciprocals from eigenvalue approximations

Let sigma=min|lambda|>0 and L=max|lambda|. If max|lambda_tilde-lambda|<=xi<sigma, then every lambda_tilde is nonzero and

max|1/lambda_tilde-1/lambda| <= xi/[sigma(sigma-xi)].           (3)

An additional reciprocal rounding error eta_rec adds to the right side. In particular, xi=q sigma, q<1, contributes at most [q/(1-q)]M. Equation (3), followed by (1), is the complete conditional preparation-to-application contract. A certified positive lower bound for sigma may replace sigma conservatively. Merely observing a nonzero floating-point approximation is not such a certificate.

### Why a relative-l2 transform guarantee cannot substitute

Because lambda=sqrt(N) U h, a relative-l2 guarantee delta_h on transforming h only gives

max|lambda_tilde-lambda| <=sqrt(N) delta_h ||h||_2.             (4)

The guarantee permits the transform error delta_h||h||_2 e_k, attaining this sup bound. Therefore a black-box proof demanding xi<=q sigma must in general set delta_h<=q sigma/[sqrt(N)||h||_2]. Even a full flat-spectrum unit-modulus chirp has ||h||=sqrt(N), sigma=sqrt(N), requiring delta_h<=q/sqrt(N) by this route. This is an insufficiency of the contract, not a claim that the actual compiler attains that adversarial error.

## 2. Genuine quadratic chirps: a positive preparation theorem

Let N be odd, omega=exp(2 pi i/N), and

h_j=omega^(A j^2+B j+C), gcd(A,N)=1.

The parameters A,B,C are supplied as reduced residues modulo N with O(log N) bits; parsing or reducing longer descriptions is an additional input cost.

Let v=(4A)^{-1} mod N. Completing the square gives

lambda_k=G(A;N) omega^[C-v(B-k)^2],
G(A;N)=sum_j omega^(A j^2).

An elementary correlation calculation proves |G|^2=N: put j=l+d in the double sum for |G|^2; the inner geometric sum in l vanishes unless 2Ad=0 mod N, hence unless d=0. Thus min|lambda|=max|lambda|=sqrt(N), and kappa=1. The classical exact phase evaluation is

G(A;N)=epsilon_N (A/N) sqrt(N),
epsilon_N=1 if N=1 mod4, epsilon_N=i if N=3 mod4,

where (A/N) is the Jacobi symbol. It follows that sqrt(N) mu_k is an explicit unit-circle quadratic phase times a known fourth root of unity. The Jacobi symbol can be computed by Euclidean reciprocity and removing powers of two, without integer factorization; a polynomial(log N) charged bound suffices here.

### Fully charged finite-word construction

The model here is an address-capable word RAM with word width C n for a sufficiently large fixed C, and unit-cost integer addition, subtraction, multiplication, division, comparisons, shifts, Boolean operations, and random access on a fixed number of such words. Products of O(n)-bit integers are charged a fixed number of these allowed operations. Polynomial-bit interval preparation is separately paid in the displayed preparation term. This is an O(N) word-operation result, not an O(N) bit-operation result.

Let n=ceil(log2(N+1)) and target normalized multiplier error theta=2^{-t}, with t=o(n). Put p=t+10, G=2^p. Prepare a complete G-entry table of exp(2 pi i r/G), each enclosed to complex error at most theta/16. Certified Taylor/Machin rational interval evaluation takes poly(n,p) work per entry. Extended Euclid prepares v. For each k, compute the reciprocal phase exponent r_k=v(B-k)^2-C mod N exactly using O(1) O(n)-bit arithmetic operations, choose its nearest table phase by integer rounding of G r_k/N, multiply by the reciprocal Gauss factor conjugate(epsilon_N)(A/N), and store the result. Address rounding contributes at most pi/G. Total normalized sup error is less than theta/8.

Prepare one dyadic approximation to 1/sqrt(N) with relative error at most theta/8, using certified integer square-root bounds. Multiplying each phase and rounding to absolute error <=theta/(8 sqrt(N)) produces

max_k |mu_tilde_k-mu_k| <=theta/sqrt(N)=theta M.

All N writes and multiplications are paid. Preparation time is

O(N + 2^p poly(n,p)), space O(N+2^p poly(n,p)).                 (5)

For t=o(n), the second term is N^{o(1)}, so (5) is O(N) eventually. This is a genuine sup-norm preparation, not an l2 substitution. At unsupported finite parameters, use a charged slower interval fallback rather than asserting that its table fits. For an arbitrary supplied t outside O(n), a multiword implementation must pay its bit cost.

If d=gcd(A,N)>1, grouping j modulo N/d instead shows lambda_k=0 unless d divides B-k; the nonzero magnitudes are sqrt(Nd). Such a chirp is singular and cannot use an inverse multiplier on all coordinates. The gcd guard is essential.

This is classical Gauss-sum mathematics plus a finite-word phase-table implementation. It closes this subclass, not Hero17's entire source family. The source endpoint a=0, b=(N-1)/2 has annihilator (z^N-1)/(z-1), all coefficients1, and is indeed a full nondegenerate chirp. The other endpoint b=0 has h=delta_0 and lambda=1. Both are easy cases.

## 3. Hero17 boundary: new exact O(N) preparation, unresolved word stability

Take N=2(a+b)+1, m=2b, q=omega^{-1}, A0=a+1, and

g(z)=product_{r=0}^{m-1}(z-q^(A0+r))=sum_{r=0}^m c_r z^r,
h_s=c_{s+b} q^[s(s-1)/2] for -b<=s<=b; h_s=0 otherwise.

This is the source's Q=L C_h R kernel. Its coefficients obey

c_0=(-1)^m q^[A0 m+m(m-1)/2],
c_{r+1}/c_r=-q^[-(A0+m-r-1)] (1-q^(m-r))/(1-q^(r+1)).        (6)

All denominators are nonzero because 1<=r+1<=m<N. To prove (6), expand the geometric-root product by elementary symmetric functions, giving
c_r=(-1)^(m-r)q^[A0(m-r)+(m-r)(m-r-1)/2] [m choose r]_q,
and divide adjacent Gaussian binomials. This expansion can alternatively be established by multiplying one factor and induction. Roots and powers, all m ratios, and their divisions cost O(N) exact field operations when a primitive root and unit-cost field division are supplied. Bit complexity and root discovery are not included in that algebraic model.

The same recurrence yields

h_{s+1}(1-q^(s+b+1))=-q^[2s-(a+b)]h_s+q^(s-a)h_s.            (7)

It is valid at the two support boundaries as well, because the vanishing factors make both sides zero. The zero-extended cyclic version is valid modulo N. Let H(z)=sum_{s modN}h_s z^s, evaluated at Nth roots only. Multiply (7) by z^s and sum to obtain

H(z)-(q^b+q^(-a)z)H(qz)+q^[-(a+b)]z H(q^2z)=0.

Consequently lambda_k=H(q^k) satisfies the cyclic second-order recurrence

lambda_k-(q^b+q^(k-a))lambda_{k+1}+q^[k-(a+b)]lambda_{k+2}=0. (8)

Compute lambda_0 and lambda_1 by two direct O(N) sums. Equation (8) generates the remaining N-2 values with O(1) field operations each and no zero denominators, since its last coefficient is a root of unity. Testing all values and forming their reciprocals takes another O(N) exact field operations if they are nonzero. Thus **exact coefficient, spectral, and inverse-multiplier preparation is O(N) in the supplied-root unit-cost exact-field model**, with O(N) storage. It does not itself apply C_h^{-1} to a fresh arbitrary input.

Why this does not close the finite-word claim: over C, the absolute-value recurrence only gives

|e_{k+2}|<=2|e_{k+1}|+|e_k|+local error,

allowing O(3^N) amplification in a crude certified bound. The q-binomial denominators also can be O(1/N), and the coefficients may be large. This does not prove actual exponential instability, but it does not supply a subpolynomial guard-precision bound. A precision O(N+log(1/epsilon)) implementation no longer meets the compiler's O(log N)-word regime. A sharper stable recurrence or other sup-norm preparation, and a useful complex lower-spectrum/condition bound, remain explicit tasks.

### Classical polynomial identification

There is a precise Stieltjes–Wigert description of this kernel. With E=A0 m+m(m-1)/2+b(b+1)/2,

H(z)=(-1)^m q^E z^(-b) (q;q)_m S_m(q^[-(A0+3b)]z;q).        (8a)

Indeed, substitute the Gaussian-binomial coefficient formula above; its combined q exponent is r^2-(A0+3b)r+E. Equation (8a) then follows term by term from the defining finite sum in NIST DLMF 18.27.18. This is a rational-polynomial identity; it remains valid at the present root of unity because m<N keeps (q;q)_m nonzero. The usual positive-measure orthogonality for real 0<q<1 does not give bounds at these complex roots of unity. Thus (8) fits classical q-polynomial difference theory, and is not evidence of a new family of special functions.

Primary definition checked: https://dlmf.nist.gov/18.27.E18

### Exact countercontrols against overbroad Gauss transfer

For N=5,a=b=1, let phi=(1+sqrt5)/2. Then

g(z)=1+phi z+z^2,
h_0=phi, h_1=1, h_4=omega^{-1}, h_2=h_3=0.

So lambda_k=phi+omega^{-k}+omega^{k-1}. The two larger magnitudes are sqrt(5+2sqrt5); the other three are sqrt((5-sqrt5)/2). Their ratio is phi^2=(3+sqrt5)/2. The exact quotient-ring control verifies the fourth-power relation between squared magnitudes. The spectrum is nonflat; the full-chirp min-spectrum formula cannot be substituted. This example does not refute existence of some other favorable uniform bound.

There are also exact singular finite-field instances. Fresh controls reconstructed the source's field-generator convention and obtained:

- N45, p181, omega16: zeros k11,35, rank43; omega3 instead gives rank45 in the same field.
- N49, p197, omega16: zeros k6,44, rank47.
- N53, p107, omega4: zeros k3,8,46,51, rank49; omega3 instead gives rank53 in the same field.
- The source comparison roots (N45,p271,omega44), (N49,p491,omega42), (N53,p743,omega212) all have full rank.

A field and N alone do not specify these finite-field certificates: the actual primitive root matters. The root-specific failures disprove universal invertibility over admissible root-rich fields. They say nothing by themselves about complex singularity at the canonical embedding.

## 4. Prior art and stopping condition

Casazza–Fickus, *Fourier Transforms of Finite Chirps* (2006), full PDF §4, Lemma1 and Proposition5, explicitly establishes quadratic-shift covariance and gcd-controlled Fourier magnitudes. Gurevich–Hadani–Howe (2008), §3.1 equation3.3 and §4, gives the Jacobi/Gauss phase context. These are primary-source checks, not a claim of historical novelty:

- https://link.springer.com/content/pdf/10.1155/ASP/2006/70204.pdf
- https://arxiv.org/html/0808.2447v3

The rational error estimates are direct norm/reciprocal perturbation arguments; the Gaussian-binomial ratio is classical. The exact spectral recurrence (8) is a project derivation in the classical Stieltjes–Wigert family identified in (8a); no historical novelty is claimed. Its proof and controls are sufficient to use it under the explicit algebraic model. It must not be promoted into a finite-word O(N) theorem without a new stability and conditioning argument. Q30's general finite-word transfer is therefore **partially closed, remaining dependency explicit**, not complete.
