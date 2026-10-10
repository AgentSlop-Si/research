# Signed magnetic fusion: support coverage and row-Hankel obstruction

10 October 2026. Newly derived continuation of accepted Phase18. This document does not modify its source or the frozen prior audits. All coefficients are exact. No historical-priority or running-time improvement is claimed.

## Model and coefficient formula

Let N >= 3 be odd. Work over a field k whose characteristic does not divide N and with a supplied primitive Nth root q. Write S e_i=e_(i+1), T e_i=q^i e_i, and W_(a,b)=S^a T^b, with indices modulo N represented in 0,...,N-1. For each orientation (epsilon,delta) in {+1,-1}^2, allow weighted averages of

Q_j=I-alpha S^epsilon-beta zeta^j T^delta,
zeta=q^(epsilon delta),  j=0,...,N-1,
Delta=1-alpha^N-beta^N != 0.

Phase18 applies with the signed pair: T^delta S^epsilon=zeta S^epsilon T^delta. An arbitrary branch-weight expansion into characters gives

R_(epsilon,delta)=sum_(ell=0)^(N-1) h_ell sum_(r=0)^(N-1-ell)
  alpha^r [r+ell choose ell]_zeta W_(epsilon r,delta ell),

where h_ell=gamma_ell beta^ell/Delta. These amplitudes need not be arbitrary when beta=0, but allowing arbitrary h_ell only enlarges the representation class. No argument below assumes that beta=0 permits nonzero high sectors. A finite sum within one orientation still obeys the same support restriction.

The negative Fourier matrix F[k,t]=q^(-kt) has coefficients

f(a,b)=C q^((a+b)^2/4),  C=G_-/N != 0,
G_-=sum_j q^(-j^2).

Fractions in exponents are inverses modulo the odd integer N, not division in k. The identity G_- G_+=N proves C != 0 in every allowed characteristic. The W_(a,b) form a basis. These accepted Phase18 facts can also be checked directly by trace and the invertible substitution (j,l) -> (l-j,l+j).

## S1. Exactly four signed orientations are necessary for support coverage

Define A_(epsilon,delta) by [epsilon a]_N+[delta b]_N <= N-1. Each orientation is confined to A_(epsilon,delta), regardless of legal parameters, weights, or the number of summands within that orientation.

For 1 <= a,b <= N-1 the four membership tests are:

- ++: a+b <= N-1
- +-: a < b
- -+: b < a
- --: a+b >= N+1

The union of ++,+-,-+ therefore misses exactly (a,b)=(t,t) with (N+1)/2 <= t <= N-1. The axes introduce no additional omissions. Reflecting either coordinate proves that every choice of three orientations misses a reflected diagonal segment of (N-1)/2 indices. Every collection of at most three orientations is contained in such a triple, so cannot represent Fourier even with arbitrarily many legal pairs per orientation.

All four cover the index square. On the axes, at least one triangle covers. In the interior with a != b a cross-sign triangle covers. If a=b, oddness implies either 2a <= N-1 or 2a >= N+1, so ++ or -- covers. This is coverage only. It does not imply coefficient realization. For even N the point (N/2,N/2) lies outside all four triangles, emphasizing the odd-length hypothesis.

A useful sharper description is that each orientation has exclusive points

(a,b)=(epsilon t,delta t),  1 <= t <= (N-1)/2.

Thus a one-pair-per-orientation representation of Fourier forces every alpha and beta to be nonzero and fixes each corresponding h_t from the Fourier coefficient. The origin and axes are not used to draw this conclusion.

## S2. A row has at most two exponentials per relevant parameter pair

Consider b=1 and 1 <= a <= N-1. A delta=-1 summand has ell=N-1 and r=0, so contributes only at a=0 and is absent from this row interval. A delta=+1, epsilon=+1 summand contributes

h_1 alpha^a (1-q^(a+1))/(1-q).

This expression remains valid at a=N-1, because its factor 1-q^N vanishes exactly where triangle support stops. It is a linear combination of alpha^a and (q alpha)^a. If alpha=0, it vanishes throughout the interval and is handled without inversion.

A delta=+1, epsilon=-1 summand with alpha != 0 contributes

h_1 alpha^(N-a) (1-q^(a-1))/(1-q^(-1)).

The factor at a=1 vanishes exactly where its triangle stops. This is a linear combination of (alpha^(-1))^a and (q alpha^(-1))^a. The alpha=0 case again vanishes on the entire interval, because N-a >= 1.

Consequently, if r_+ is the total number of parameter-pair summands with delta=+1, the coefficient sequence c(a,1), a=1,...,N-1, is a sum of at most 2 r_+ geometric sequences. Coincident roots or zero amplitudes can only reduce the rank. Applying the same calculation to b=-1 gives a sum of at most 2 r_- geometric sequences, with paired ratio q^(-1), where r_- counts delta=-1 pairs. Pairs of zero contribution may be counted; the resulting necessary bound is only weaker.

## S3. Fourier forces a growing number of parameter pairs

Put m=(N-1)/2 and H[i,j]=f(i+j+1,b), 0 <= i,j < m, for b=1 or b=-1. Every sampled a lies between 1 and N-2, hence in the preceding row interval. Expanding the square gives

H[i,j]=C q^((1+b)^2/4)
  q^(i^2/4+i(1+b)/2) q^(j^2/4+j(1+b)/2)
  (q^(i/2))^j.

All diagonal factors are nonzero. The last factor is a Vandermonde matrix on the distinct points q^(i/2), 0 <= i < m, so det H != 0 over every admissible field. Hence rank H=m.

For any geometric sequence z^a, its Hankel contribution has rank at most one. S2 therefore proves

r_+ >= ceil((N-1)/4),  r_- >= ceil((N-1)/4).

Combining this with S1 gives the total necessary bound

r_total >= max(4, 2 ceil((N-1)/4)).

Here the first term refers to four present orientations; the second counts individual parameter pairs, including repeated orientations. These are representation bounds. They do not imply that r_total independent N-cost applications are necessary: cost sharing is precisely what accepted Phase18 demonstrates can occur.

In particular, one pair per orientation has r_+=r_-=2 and cannot realize Fourier at any odd N >= 11. This conclusion uses an all-size proof, not a dimension count or extrapolation from controls.

## S4. Explicit coefficient-ratio constraints for one pair per orientation

Fix the delta=+1 pair parameters x=alpha_(++), y=alpha_(-+). Let 1 <= t <= m. At b=t, the central interval t <= a <= N-t receives only these two orientations. The exclusive endpoints a=t and a=N-t fix their amplitudes. For every interior t < a < N-t a Fourier representation must satisfy

q^(((a+t)^2)/4-t^2)
 = x^(a-t) [a+t choose t]_q / [2t choose t]_q
 + q^(-t^2) y^(N-a-t)
   [N-a+t choose t]_(q^(-1)) / [2t choose t]_(q^(-1)).

All displayed denominators are nonzero because 2t <= N-1. The Gaussian coefficient numerators have no vanishing factor for these interior points. Parameters x and y must be nonzero by S1. This is a necessary explicit two-parameter algebraic system; its reflected counterpart treats delta=-1. It is not asserted to be sufficient for the full matrix.

For t=1 it simplifies to the particularly convenient system, for 2 <= a <= N-2,

q^((a+1)^2/4)
 = q x^(a-1) (1-q^(a+1))/(1-q^2)
 + y^(N-a-1) (1-q^(a-1))/(1-q^(-2)).

These equations use only the interior row and unique endpoint coefficients, so arbitrary remaining phase-branch weights cannot repair a failure.

## S5. The remaining boundary length N=9 also fails, exactly

For one pair per orientation, S2 gives four row bases x,qx,z,qz, where x=alpha_(++), z=alpha_(-+)^(-1). Put A=x+z, B=xz. The monic recurrence polynomial is

P(v)=(v-x)(v-qx)(v-z)(v-qz)=sum_(k=0)^4 p_k v^k,
p_3=-(1+q)A,
p_2=q A^2+(1+q^2)B,
p_1=-q(1+q)AB=qB p_3,
p_0=q^2 B^2.

The row recurrence sum_k p_k f(a+k,1)=0 holds for a=1,2,3,4. After division by the nonzero chirp factor, the polynomial sum_k p_k q^(k^2/4) v^k has roots q^((a+1)/2), a=1,...,4. They are four distinct roots and its leading coefficient is q^4. This uniquely determines P. Reduction modulo Phi_9(q)=q^6+q^3+1 gives

p_4=1,
p_3=-q^5+q^3-q^2-q+1,
p_2=-q^4+2q^2-1,
p_1=q^4-q^2+q+1=q p_3,
p_0=q^2.

Here p_3(q^2+1)=1 modulo Phi_9. Thus p_1=qB p_3 forces B=1. The p_2 equation and p_3=-(1+q)A would force

E=(1+q)^2(p_2-1-q^2)-q p_3^2
 =q^5-q^4+2q^2-2q-3=0.

But direct polynomial multiplication verifies

E(2q^5-q^4+3q^2-3q+2)=3 modulo Phi_9(q).

Since characteristic k does not divide 9, the right side is nonzero. This contradiction excludes N=9 over every admissible field, including characteristic 2. The proof does not rely on choosing complex embeddings or on numerical roots.

Together S3 and S5 exclude one parameter pair in each signed orientation for every odd N >= 9.

There is also a stronger finite-sum consequence at N=9: r_+ >= 3 and r_- >= 3, hence r_total >= 6. Indeed, S1 requires both epsilon orientations among the delta=+ pairs. If r_+=2, there is exactly one of each and the preceding proof still applies, regardless of how many delta=- pairs are present; they do not contribute on the tested interval. Simultaneously reflecting (a,b) to (-a,-b) preserves the Fourier coefficient and exchanges the two delta signs, proving the other bound.

## S6. N=3 has a four-bank construction over every admissible field

Set beta=1 in all four orientations and choose

alpha_(++)=1, alpha_(+-)=q, alpha_(-+)=q, alpha_(--)=1.

Since each alpha^3=1, every Delta=-1 is nonzero, even in characteristic 2. For b=0 the ell=0 sectors have coefficient sequences 1, q^a, q^(-a), 1. Let

c_k=(1/3) sum_(a=0)^2 f(a,0) q^(-ka),  k=0,+1,-1.

Assign h_(++,0)=c_0, h_(+-,0)=c_1, h_(-+,0)=c_(-1), and h_(--,0)=0. Orthogonality gives the entire target row b=0.

For each orientation put

h_(epsilon,delta,1)=f(epsilon,delta) /
  [alpha_(epsilon,delta)(1+q^(epsilon delta))].

All denominators are nonzero. These match the four exclusive nonaxis points. At each row b=d, d=+1,-1, the two ell=1 sectors have now matched both nonzero-a coefficients and contribute h_(+,d,1)+h_(-,d,1) at a=0. The ell=2 sector of orientation (+,-d) contributes only at (0,d). Set

h_(+,-d,2)=f(0,d)-h_(+,d,1)-h_(-,d,1),
h_(-,-d,2)=0.

This matches the two remaining coefficients and changes no earlier match. Finally beta=1 and Delta=-1 make every chosen amplitude legal: take gamma_(epsilon,delta,ell)=-h_(epsilon,delta,ell), and branch weights

w_j=sum_(ell=0)^2 gamma_ell (q^(epsilon delta))^(-j ell).

All nine Fourier coefficients are therefore matched by four legal magnetic banks. S1 proves that four is the exact minimum number of banks at N=3 in this grammar. Unlike the finite-field example below, this is a proof over every admissible field, including C.

## S7. Exact controls, with field and quantifier boundaries

All three executable controls here were freshly authored independently of supplied research programs. No supplied program was executed, imported, compiled, or AST-parsed.

- `fresh_signed_controls.py`: checks the support gate for the 15 odd lengths 3 through 31; independently constructs and inverts the original branch matrices for 60 signed weighted averages at N=3,5,7,9,11, including alpha=0; checks the coefficient formula against all original matrix entries. It also searches exact small-field parameters after a complete necessary-row filter.
- N=3 over F_7 with q=2 has a positive four-bank realization, directly verified against F[k,t]=2^(-kt). Listed as (epsilon,delta; alpha,beta; w_0,w_1,w_2), the banks are (+,+;1,1;3,0,3), (-,+;1,1;5,3,6), (+,-;2,1;5,5,0), (-,-;2,1;0,4,6). Every Delta is 6. Each bank is (1/3) sum_j w_j Q_j^(-1). This is a finite-field existence example, not a complex existence claim.
- N=5 over F_11 with q=3 has exactly one row-compatible nonzero parameter pair on each delta side; the only combined quadruple fails the complete coefficient equations. This excludes that field only. N=7 over F_29 with q=7 has no compatible delta=+ or delta=- pair even on the tested row, again a field-specific control.
- `fresh_nine_certificate.py`: independently reconstructs the four forced recurrence coefficients from their roots and verifies all integer polynomial identities in S5. It verifies the full certificate E V - 3 = Phi_9(q)(2q^4-3q^3+q^2+5q-9), where V is the multiplier displayed in S5.
- `fresh_small_row_algebra.py`: exact SymPy Groebner reduction of the S4 t=1 equations over Q[q]/Phi_N(q), N=5,7. The reproduced polynomials, minimal polynomials, guards, and limitations are documented in `SMALL_CONTROL_SCOPE.md`. At N=7 the computed reduced basis is [1]. This is an exact symbolic control supporting characteristic-zero exclusion, separately labeled and not incorporated into the all-characteristic theorem. At N=5 the necessary row ideal is non-unit; that alone proves neither full realization nor failure.

Finite failures have not been extrapolated to other fields or lengths. The universal statements are S1-S6 and S9, proved directly.

## S8. Comparison with the inherited F014 and F018 grammars

The accepted F014 comparison is `../matrix/final_v1/NEW_COMPOSITE_WEYL_THEOREM.md`. Its counted object is a literal two-resolvent product c(I-alpha U)^(-1)(I-beta V)^(-1), with one fixed ordered generating pair U,V shared by every branch and separate guards alpha^N,beta^N != 1. Its canonical coefficient matrix has rank one and its one-coordinate sequence is geometric. The present counted object is a whole phase-weighted magnetic bank (1/N) sum_j w_j(I-alpha S^epsilon-beta zeta^j T^delta)^(-1), with guard 1-alpha^N-beta^N != 0. Each bank is expressed using N phase-indexed literal inverses, possibly with zero weights. Four different signed generator pairs are allowed across banks. The old fixed-pair two-resolvent product theorem therefore does not apply by simply renaming its branch count.

The Hankel/Vandermonde mechanism is classical and already appears in F014. The new-to-project scoped derivation is the signed-triangle coverage gate plus the isolation of b=+/-1, where a degree-one Gaussian coefficient makes an entire magnetic bank contribute at most two exponentials. That isolates the number of parameter-pair banks despite their many internal weighted inverse branches. It is a new grammar-specific consequence, not a new Hankel-rank theorem or a historical-priority claim.

F018 counts literal sparse inverse branches in its own endpoint grammar. It cannot be multiplied by a per-branch application cost to charge these averaged banks without an additional no-sharing proof. Accepted Phase18 is direct evidence that many noncommuting inverse branches can share work. The present bank-count bound likewise remains separate from evaluation complexity.

## S9. A coarse 4N-bank upper bound, with the naive work charged

Every matrix can be represented by at most 4N legal banks in this grammar. In particular, the order of the minimum Fourier bank count is Theta(N), although its evaluation complexity remains a different question.

Partition the Weyl index square by assigning each coefficient to one containing signed triangle, using S1. For each orientation let c_(r,ell) denote its assigned coefficient in local coordinates (epsilon r,delta ell), setting it to zero if that index was assigned elsewhere. For 0 <= r < N put

t_(r,ell)=c_(r,ell)/[r+ell choose ell]_zeta if r+ell <= N-1,
t_(r,ell)=0 otherwise.

Every Gaussian factor being divided by is nonzero: all numerator and denominator exponents are between 1 and N-1. Choose N parameter pairs in this orientation,

alpha_j=q^j, beta_j=1, 0 <= j < N.

Each has Delta_j=-1. Set

h_(j,ell)=(1/N) sum_(r=0)^(N-1) t_(r,ell) q^(-jr).

Root-of-unity orthogonality gives sum_j h_(j,ell) alpha_j^r=t_(r,ell). Thus the sum of these N banks matches the entire assigned triangle. Since beta=1 and Delta=-1, use gamma_(j,ell)=-h_(j,ell), followed by the ordinary branch-weight expansion

w_(j,k)=-sum_(ell=0)^(N-1) h_(j,ell) zeta^(-k ell).

Summing over four orientations proves the claim. This construction uses root-Vandermonde inversion as a mathematical formula, not as an assumed fast subroutine.

For an explicit conservative arithmetic upper bound, prepare all root powers and Gaussian factors using successive ratios, fill the four triangular arrays, and evaluate the two displayed finite transforms by direct nested loops. This takes O(N^3) field/address operations, including all coefficient divisions, and O(N^2) retained storage. It materializes 4N^2 branch-weight entries. If the input target is an ordinary matrix rather than Weyl coefficients, direct coefficient extraction costs another O(N^3), within this bound. For Fourier its explicit Weyl formula already supplies them.

There is also a direct fully charged O(N^3) application, which is not a speed improvement. There are 4N^2 literal branch instances. For each branch, beta=1 gives a known index i_0=-epsilon k with diagonal d_(i_0)=1-zeta^k q^(delta i_0)=0. Because alpha=q^j is nonzero, solve

d_i y_i-alpha y_(i-epsilon)=x_i

starting at y_(i_0-epsilon)=-x_(i_0)/alpha and stepping backward in epsilon using y_(i-epsilon)=(d_i y_i-x_i)/alpha. Exactly N equations determine all N outputs in O(N) work; the vanished diagonal creates the start, not an invalid division. Forming phases, multiplying by the supplied branch weight, and accumulating every output are also O(N) per branch. The factor 1/N is charged once or in the output scaling. The weights occupy O(N^2) storage and each branch uses only O(N) working storage.

The construction therefore proves a linear-order bank count with dense quadratic-size parameter data and a conservative cubic-work implementation. It proves no FFT improvement. In particular, arbitrary weights do not inherit the O(N) unweighted-bank evaluator, and coefficient preparation cannot be omitted from a runtime ledger.

## Scope, next obligation, and cost boundary

The four-orientation grammar escapes the old support barrier but still has an exact Fourier obstruction at one pair per orientation for all odd N >= 9, and every Fourier realization in the finite-sum grammar would need at least max(4,2 ceil((N-1)/4)) pairs.

The coarse growing-bank existence question is settled by S9. The next substantive algorithmic obligation is a compact description of the Fourier weights and a fully charged shared evaluator that genuinely improves the cost; dense interpolation does not supply either. A minimal concrete next test is N=9 with at least three pairs on each delta side, all four orientations present, and the full Fourier coefficient system plus all Delta guards enforced. It is not a sufficiency claim for six banks. The bounded small-length status is kept separate: N=3 is now constructively settled over every admissible field by S6, N=5 has field-specific failure and an undecided complex full-coefficient problem with one bank per orientation (four banks total), and N=7 has the stated exact characteristic-zero row control without an all-characteristic certificate. Count of pairs alone is not a runtime lower bound, and support coverage alone is not an algorithm. Parameter discovery, all weight preparation, legality, storage, input/output, and any across-pair cost sharing must be charged before any runtime claim. The mechanism uses classical root-of-unity filtering, Gaussian coefficients, Hankel rank, and Vandermonde algebra; global priority is unresolved.
