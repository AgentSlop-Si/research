# Independent final review: entrywise Fourier-mask stability and quantitative gaps

Date: 2026-10-18. Stable owner: **M-SPARSE-DEFECT**.

## Verdict

**ACCEPT the radical stability inequality, the strengthened general no-mask gap, and both stated polynomial small-codimension gaps. No mathematical correction is required.**

In the inherited domain N≥2, 1≤s≤N−1, d=N−s, and with the normalized complex Fourier matrix and spectral norm:

1. If no column-weight-d complementary Fourier mask is scaled unitary, then

   Delta(N,s)² ≥ d/N + 1/[10 N d^(phi(N)−1)].

2. For N≥4 with 3 not dividing N,

   Delta(N,N−3)² ≥ 3/N + 1/(30 N³).

3. For odd N≥3,

   Delta(N,N−2)² ≥ 2/N + 1/(5 N³).

4. More generally, if every bad column-weight-d mask has an off-diagonal Gram entry of modulus at least eta, where 0<eta≤1/N, then the explicit radical additive bound in the candidate's equation (S) is valid. Its simplification eta²/(10a²), a²=d/N, is valid under the no-mask premise.

These inequalities hold for **every admissible invertible matrix before taking an infimum**. The condition remains at most s nonzeros in **every row** of the inverse, with arbitrary complex entries and arbitrary supports. No condition-number bound, one-row relaxation, attained optimum, or new compactness premise has entered the proof.

Retain **TO RESEARCH**, priority **42**. Remaining composite classifications, exact nonsharp optima, and optimal asymptotic gap rates remain unresolved. No additional mathematical gate is needed for the results accepted here.

## Evidence binding

Candidate: `/workspace/shared/sparse_entrywise_gap_20261018_1508`.

- REPORT.md SHA-256: `d4db3e1e49035991dc70af6d846293d87c5d03fad903ed28eb50fc96c392eb8d`
- verify_exact.py SHA-256: `994d1cc08e49e45be6a2489f700fd90c860b16a52414301c7f17803a8f1eb61f`
- MANIFEST.json SHA-256: `23c8b1b9371d9fa9c6d74c94e1c976c68b27ea7d08d80b3b1e561116eaa66e36`

All 11 candidate manifest entries match their byte counts and SHA-256 hashes. The candidate seal matches its report, checker, and manifest. All three accepted-source copies match the original files, recorded lengths, and hashes. The ten-member manifest of the accepted codimension-three final review also verifies; its relevant seal bindings are verified in the integrity records.

The accepted input review is `/workspace/shared/sparse_codimension_three_final_review_20261018_1341/REVIEW.md`, SHA-256 `55ea2b87413865458f2691b5d7843f3cb8d694cd90f2661150e5d80d9f41e7c7`. Its accepted theorem domain explicitly supplies N≥2 and 1≤s≤N−1. The present candidate says it continues that accepted model and uses s≥1 throughout. Restating this domain in a standalone publication of the result would be useful editorially, but it is not a mathematical defect in the scoped packet.

Before/after integrity checks bind this review to unchanged candidate bytes. The candidate's checker was inspected but was neither imported nor executed. All finite calculations below come from `fresh_controls.py`, written for this review. No prior checker was imported or executed.

## 1. Simultaneous inverse-row supports and the easy branch

Let B=M⁻¹, E=M−F, rho=||E||, a²=d/N, q=s/N, and D=rho²−a². Every inverse row b_i is nonzero because B is invertible. For its actual support size t_i≤s,

   rho² ≥ ||e_iᵀ−b_i F||² / ||b_i||²
        ≥ 1 + ||b_i||⁻² − 2 sqrt(t_i/N) ||b_i||⁻¹
        ≥ 1−t_i/N.

The first inequality uses b_i E=e_iᵀ−b_i F; unitarity of F gives ||b_i F||=||b_i||. Cauchy–Schwarz on the actual support gives |(b_i F)_i|≤sqrt(t_i/N)||b_i||. Completing a scalar square proves the last inequality.

Thus D≥0. Moreover, if even one inverse row has t_i≤s−1, then D≥1/N. Consequently, in the near branch D<1/N, **all** inverse rows have exactly s nonzeros. The extracted matrix A[r,i]=F[r,i] 1_(r in S_i) therefore has s selected entries in every column, and C=F−A has d entries in every column. No common support pattern or row-regularity of C is assumed.

This is the correct use of the global row constraint. The proof does not optimize a selected inverse row and then silently discard the others. Any matrix with an undersaturated inverse row is handled by the common easy branch.

## 2. Completing the square and the inverse-row norm bound

On the common support S_i, define b_(0i) as row i of B0=q⁻¹ A*. Then ||b_(0i)||²=1/q, and direct expansion gives

   q ||b_i−b_(0i)||² = ||b_i E||² − a² ||b_i||².

Indeed, both sides expand to 1+q||b_i||²−2 Re((b_i F)_i). This confirms the precise q factor and the conjugation convention.

Using ||b_i E||≤rho||b_i|| yields

   ||b_i−b_(0i)|| ≤ sqrt(D/q)||b_i||.

Since D<1/N≤q, the coefficient sqrt(D/q) is strictly below one even at s=1. The triangle inequality therefore gives

   ||b_i|| ≤ 1/(sqrt(q)−sqrt(D)).

For K=q(B−B0), k_i=||K[i,:]|| and u_i=sqrt(qD)||b_i||, this implies

   k_i≤u_i≤u=sqrt(D)/(1−sqrt(D/q)).

No global inverse norm, trace, or conditioning estimate is needed. The rowwise denominators remain valid at the smallest admissible budget.

## 3. The matching-diagonal PSD identity is correct

Set H=rho²I−EE*≥0, P=qBHB*+KK*≥0, and Z=C*C−a²I. The square-completion identity gives

   P_ii=qD||b_i||²=u_i².

For an independent derivation of the full identity, define

   G(X)=I−XF−F*X*+qXX*.

Because BE=I−BF and FF*=I,

   G(B)=B(EE*−a²I)B*=DBB*−BHB*.

Also qG(B0)=C*C−a²I=Z. Expanding qG at B0 with B=B0+K/q and qB0*=A gives

   qG(B)=Z−KC−C*K*+KK*.

Therefore

   Z=qD BB*−P+KC+C*K*.

The signs, q factors, matrix ordering, and adjoints are all correct. In particular, the two PSD matrices U=qDBB* and P have exactly the same diagonal u_i². For any PSD matrix T, its 2×2 principal minors give |T_ij|²≤T_ii T_jj. Hence

   |U_ij−P_ij|≤2u_i u_j.

Each column of C has norm a. Applying row/column Cauchy–Schwarz to KC and C*K* yields

   |Z_ij|≤2u_i u_j+a(k_i+k_j)≤2u²+2au.

The argument controls a single required entry; there is no hidden sum over N indices and no missing dimension factor. C need not have orthogonal columns, uniform row weights, or be invertible for these identities to hold.

## 4. Radical inversion, constant 10, and the infimum

Under the no-mask premise, the extracted C has some nonzero off-diagonal Gram entry. Its diagonal is exactly a², so the assumed separation gives eta≤2u²+2au. Solving this increasing quadratic on u≥0 gives

   u≥r=(sqrt(a²+2eta)−a)/2
       =eta/(sqrt(a²+2eta)+a).

Combining this with u≤sqrt(D)/(1−sqrt(D/q)) and using the strictly positive denominator gives

   sqrt(D)≥r/(1+r/sqrt(q))
           =eta/[a+sqrt(a²+2eta)+eta/sqrt(q)].

This is exactly equation (S), with no reversed inequality or extraneous root.

Let g be its additive term. Since its denominator is at least 2a and eta≤1/N,

   g≤eta²/(4a²)≤1/(4Nd)<1/N.

Thus every matrix in the other branch D≥1/N also obeys D≥g. The two branches cover the entire admissible set.

For the rounded denominator bound, a no-mask case has d≥2: at d=1 any permutation support supplies a scaled-unitary complementary mask. In the inherited domain, s≥1. Consequently

   eta/a²≤1/d≤1/2,
   eta/(a sqrt(q))≤1/sqrt(ds)≤1/sqrt(2).

Therefore

   [a+sqrt(a²+2eta)+eta/sqrt(q)]/a
      ≤1+sqrt(2)+1/sqrt(2)=1+3/sqrt(2).

Its square is 11/2+3sqrt(2)<10, since 18<81/4. The constant 10 is conservative and valid uniformly, including N=3,s=1.

The proof has now shown rho²≥a²+g for **every** admissible M. Taking square roots and then the infimum gives Delta≥sqrt(a²+g), equivalently Delta²≥a²+g. No minimizing sequence limit, attainment, continuity of inverse supports, or compactness result is required. The accepted equality-mask characterization is used to identify the no-mask families, not to supply a new quantitative-limit argument.

## 5. Paired embeddings and the general exponent

A nonzero off-diagonal entry of C*C is xi/N, where

   xi=sum_(r in T) omega^(r(j−i)),  |T|≤d.

This is an algebraic integer in Q(omega). The field has phi(N) embeddings, indexed by units modulo N. In a no-mask case N≥3, so the identity embedding and complex conjugation are distinct embeddings, even when their values happen to coincide because xi is real. Both factors must remain in the full field norm with their multiplicities.

The field norm is a nonzero integer. Every embedding is injective, so nonzero xi has no zero conjugate. Every conjugate is a sum of at most d unit-modulus terms and therefore has modulus at most d. Isolating the identity/conjugate pair gives

   1≤|Norm(xi)|≤|xi|² d^(phi(N)−2).

Thus

   |xi|≥d^(1−phi(N)/2),
   eta_cyc=1/[N d^(phi(N)/2−1)].

This argument does not require j−i to be coprime to N, distinct resulting exponents, full degree of xi, or a non-real xi. Repeated exponents merely give integer coefficients; a proper subfield or a real value creates repeated conjugate values with the appropriate field-norm multiplicity. N≥3 also ensures even phi(N)≥2, so eta_cyc≤1/N.

Substitution in eta²/(10a²) gives exactly

   1/[10 N d^(phi(N)−1)].

The ratio to the previously accepted additive lower bound is

   2^22 N^9 d^(phi(N)−1)/(10s^6).

It is greater than one uniformly: s<N implies N^9/s^6>N^3, while d≥2 and phi(N)≥2. The claimed strengthening is not contingent on finitely tested values.

## 6. Small-root geometry and polynomial normalization

### Two roots

After a rotation, a pair of N-th roots has modulus 2cos(pi k/N), where k is the circular exponent difference and 0≤k≤floor(N/2).

- For odd N, the smallest possible value is 2sin(pi/(2N))≥2/N.
- For even N, the zero at k=N/2 must be excluded. The smallest remaining value is 2sin(pi/N)≥4/N.

These follow from sin(x)≥2x/pi on [0,pi/2]. A singleton has modulus one, which is at least 2/N in the odd dimensions under consideration. Therefore every nonzero sum of at most two roots has modulus at least 2/N for odd N≥3. Dividing by N gives eta=2/N²≤1/N. With d=2,

   eta²/(10a²)=1/(5N³).

The accepted weight-two no-mask theorem supplies precisely the odd-dimensional hypothesis. No two-term zero was accidentally assigned a positive lower bound.

### Three roots

For any chosen pair among three roots, its sum has modulus 2cos(u), u=pi k/N in [0,pi/2]. The reverse triangle inequality gives

   |z1+z2+z3|≥|2cos(u)−1|.

On [0,pi/3], concavity places 2cos(u) above the chord joining (0,2) and (pi/3,1), so

   2cos(u)−1≥(3/pi)(pi/3−u).

On [pi/3,pi/2], integration of 2sin(t)≥sqrt(3)>3/pi gives

   1−2cos(u)≥(3/pi)(u−pi/3).

When 3 does not divide N, the integer 3k−N is nonzero. Combining the two estimates yields

   |z1+z2+z3|≥|3k−N|/N≥1/N.

The argument allows repeated roots, including k=0; antipodal pairs also cause no exception. At weight three a nonzero overlap may contain one, two, or three terms. Singletons and nonzero pairs satisfy the weaker 1/N bound as well, so eta=1/N² is justified for every bad mask. For d=3,

   eta²/(10a²)=1/(30N³).

The accepted codimension-three obstruction supplies the no-mask premise when N≥4 and 3 does not divide N. The excluded dimensions genuinely have three-term zero sums, so the arithmetic hypothesis is essential.

Taking the maximum of the general and applicable small-codimension lower bounds is valid. The candidate correctly avoids claiming that either always dominates at small N.

## 7. Fresh exact and rigorous controls

`fresh_controls.py` completed successfully with five matrix cases, 30,876 budget pairs, 208 cyclotomic patterns, 3,200 nonzero root-pair patterns, and 128,475 normalized root-triple patterns. Full records are in `FRESH_RESULTS.json`; the captured run prints PASS, with empty stderr.

### Matrices and PSD

- Two N=4 equality masks use different selected permutation/block supports from the candidate's witnesses. Their inverse matrices are perturbed by additive, differently phased, support-compatible coefficients rather than merely common row scalings. These exercise d=1 and d=2. Equality masks are legitimate tests of the unconditional algebraic identity even though the final no-mask theorem does not apply to d=1.
- A fresh N=3 monomial witness uses the permutation (0,2,1), with nonzero entries (sqrt(3)+i)/4, (−sqrt(3)+i)/4, (−sqrt(3)+i)/4. Its error Gram is exactly (3/4)I, giving D=1/12 in the nonsharp d=2 case. Every inverse row has one nonzero.
- A nonuniform complex perturbation of that witness retains the exact inverse-row budget and has a rigorously certified error upper bound 4/5.
- A budget-s=2 identity inverse at N=4 has undersaturated rows and exercises the easy branch explicitly.

All matrix arithmetic is exact. H≥0 and P≥0 are certified through **all principal minors**, not leading minors alone. The identities, matching diagonals, two PSD entry bounds, and final entrywise estimate are checked. A certified upper bound R for rho² suffices for these controls: the identities remain valid with H=RI−EE* and D=R−a². The universal proof itself uses the actual rho.

Negative controls reject a false error bound by an exact negative principal minor and reject the wrong cross-term signs. A matrix with one one-sparse inverse row but another two-sparse row is explicitly rejected as evidence for a budget-one global constraint.

### Cyclotomic norms

For N=3,...,28, the fresh code constructs multiplication by P in the integer quotient ring Z[x]/Phi_N and computes its determinant. This obtains the full field norm without using the candidate's resultant calculation. It independently multiplies all conjugate pairs in that quotient ring and verifies that the product is the same integer. The patterns include vanishing values, repeated exponents, real values, and lower-degree/subfield values. Nonzero norms are positive integers and the paired bound is checked through exact equalities or rigorous coordinate intervals.

The negative control 1+omega² at N=5 has certified modulus below one, rejecting an unjustified unit lower bound that would discard the other norm factors.

### Root geometry and scalar constants

Root coordinates are enclosed directly by sine and cosine rational Taylor polynomials with absolute Lagrange remainders. A decimal pi interval is itself certified by exact alternating arctangent bounds. Cartesian coordinates are summed and squared outward, independently of the candidate's pairwise-cosine Gram implementation. No floating-point threshold decides zero or a lower bound.

The dimensions are N=3,...,64 and 73, 89, 101, 127, 128, 181, 200, 257. Normalized triples (1,omega^a,omega^b), with a≤b, cover all triple sums up to common rotation and permutation. Exact cyclotomic reductions verify zero triples at selected dimensions divisible by three as negative controls.

For all budgets with d≥2 and N≤250, rational arithmetic checks separation normalization, the easy-branch comparison, the clean constant prerequisites, the old/new gap ratio, and both polynomial denominators. Symbolic identities check the radical inversion in a positive-variable parametrization.

These controls verify mechanisms and catch realistic sign, normalization, support, and arithmetic errors. They do not replace the infinite arguments above or re-prove the accepted support classifications by finite enumeration.

## 8. Scope and recommended record delta

Accept the following scoped record delta:

> Strengthened the general no-mask squared-gap bound to 1/[10 N d^(phi(N)−1)], d=N−s, using an entrywise matching-diagonal PSD identity and paired cyclotomic embeddings; the sharper explicit radical stability bound is also valid. Added polynomial squared gaps 1/(30N³) for the accepted codimension-three nonsharp family 3∤N and 1/(5N³) for the accepted odd codimension-two family. The estimates hold for every admissible matrix before taking the infimum and preserve simultaneous sparsity of all inverse rows. Remaining composite classifications and exact nonsharp optima remain open. Retain M-SPARSE-DEFECT, TO RESEARCH, priority 42.

There is no new weight-four or other composite classification, no exact optimum claim, no optimal-rate claim, and no new implementation-cost or worldwide-novelty claim. Earlier shared-frame, arithmetic, stability, and implementation caveats remain unchanged.

This review wrote only its new local review directory. It did not modify the candidate, accepted sources, GitHub, a spreadsheet, or any other external state.
