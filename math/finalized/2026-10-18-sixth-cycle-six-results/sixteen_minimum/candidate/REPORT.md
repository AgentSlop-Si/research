# Exact sixteen-point minimum: complete saturated residual, no improved minimum

Owner: M-MULTISCALE-CHIRP; related view Q24. Date: 18 October 2026.

## 1. Outcome and scope

**The requested exact minimum is not settled.** The accepted interval remains `8 <= r* <= 15`. This attempt treats every smaller candidate length 8 through 14 as a single finite minimization problem and records its exact characteristic-zero saturated systems. It does not substitute another length, another characteristic, or an isolated next-stage lower bound.

The useful completed work is an exact finite formulation, a proof that its saturation enforces precisely the original pole guards, a full symmetry/coverage index, fresh target checks, and a measured attempt on a mixed length-14 system. None of these is a nonexistence certificate for the remaining systems. No new minimum, attainment below 15, owner closure, arithmetic speedup, or efficient coefficient discovery is claimed. No external state was changed.

## 2. Fixed target and literal grammar

Let `a=zeta^-1`, where zeta is primitive of order 32, and work over `K=Q[a]/(a^16+1)` embedded in C. Let

`A=K[x]/(x^16-1)`,

`Q(x)=sum_(t=0)^15 a^(t^2) x^t`,

`C[i,j]=a^(-(i-j)^2)`.

The original operations are individually invertible `(I-alpha S^s)^-1`, with arbitrary integer strides, interspersed with nonzero scalar Weyl-monomial gauges. The exact factor guard is

`alpha^(16/gcd(16,s)) != 1`.

A zero-parameter factor is an identity. Stride-zero factors are removable scalars. Negative representatives are reversible with a scalar and monomial extraction. The already accepted gauge normalization, using

`x^r Q(x)=a^(r^2) Q(a^(-2r)x)`,

reduces every legal chain to `P=hQ` in A, with `h != 0`, where P is a product of binomials with strides in `{1,2,3,4,5,6,7,8}`. Conversely every such legal product gives the original resolvent chain. We preserve the scalar h rather than silently requiring the cyclic constant coefficient to equal 1.

The fresh verifier checks all 256 entries of `C Q(S)=16I` in the integral cyclotomic ring and all 256 instances of the shift identity. In particular Q is a unit, and it has ordinary degree fifteen and constant term one. The accepted bound of eight **odd** factors is used only to omit already excluded patterns.

## 3. The exact systems, including all coefficient degeneracies

For a count vector `n=(n1,...,n8)`, let `r=sum n_s` and introduce

`G_s(y)=1 + sum_(j=1)^n_s b_(s,j) y^j`,

`P_n(x)=product_(s=1)^8 G_s(x^s)=sum_(i=0)^15 c_i(b)x^i` in A.

The coefficient formula is completely explicit:

`c_i = sum product_(s:d_s>0) b_(s,d_s)`,

where the sum ranges over `0<=d_s<=n_s` with `sum s*d_s = i mod 16`. An empty product is one. The package generator emits the full sparse polynomial list for any indexed pattern; `BENCHMARK_SYSTEM.json` stores all coefficients for the measured mixed case.

Over the characteristic-zero field K, define

`I_n = < c_i-a^(i^2)c_0 : 1<=i<=15 >`,

`J_n = < c_i-a^(i^2)c_0 : 1<=i<=15, u*c_0-1 >`.

The unsolved system is `J_n=0` over an algebraic closure of K. Equivalently it is the saturation `I_n : c_0^infinity`.

**Exact equivalence.** J_n has a complex solution if and only if the original target admits a legal representation with at most n_s factors of each normalized stride s. Each G_s has constant term one, so over C it splits into at most n_s factors `(1-alpha y)`. Missing leading coefficients, internal zero coefficients, multiple roots, and degree-zero factors are all allowed. Padding by zero parameters yields the declared counts. The next section proves that every resulting binomial satisfies its exact guard. Conversely every legal chain gives these grouped coefficients and `u=h^-1`.

A complex solution may be taken algebraic over K by the weak Nullstellensatz, since all displayed equations are over K. This fact justifies the Galois symmetry below; it does not claim that parameters lie in K itself.

## 4. Why c_0 saturation is exactly the legality saturation

Put `d_s=gcd(16,s)` and `m_s=16/d_s`. Define the grouped determinant

`R_s = product_(mu^m_s=1) G_s(mu)`.

This is a polynomial over K in the grouped coefficients. It is a resultant, and it is nonzero exactly when G_s(x^s) is a unit of A. If G_s splits as a product of `(1-alpha_(s,j) y)`, then

`R_s = product_j (1-alpha_(s,j)^m_s)`.

Thus `R_s != 0` is exactly the conjunction of the original guards in that group. Put `D=product_s R_s` and `delta=det(M_Q)`, where M_Q is multiplication by Q on A. The full matrix identity proves `delta != 0`.

In the quotient by I_n, multiplicativity of determinants gives the exact identity

`delta*c_0^16 = product_s R_s^d_s`.

Consequently c_0 is a unit if and only if every R_s is a unit. This statement is valid even in the possibly nonreduced quotient ring. More explicitly, the right side is a multiple of D and divides D^8, since `1<=d_s<=8`. Localizing at c_0 or at D therefore gives the same quotient and

`I_n : c_0^infinity = I_n : D^infinity`.

So the single Rabinowitsch equation neither drops a pole condition nor excludes any legal coefficient-degenerate case.

This saturation is essential. For the measured pattern, choose `G_4(y)=1-y^2`, `G_8(y)=1+y`, and every other G_s=1. Then `P=(1-x^8)(1+x^8)=0` in A: all unsaturated equations hold, but all c_i are zero. The fresh verifier confirms this component and confirms that `u*c_0-1=-1` rejects it for every u. An unsaturated Gröbner computation or a forced normalization c_0=1 would not be a substitute for these systems.

## 5. Complete length and symmetry coverage

The accepted eight-odd-factor theorem reduces the candidate list to

`8<=r<=14`, `n_s>=0`, `sum n_s=r`, `n1+n3+n5+n7>=8`.

The exact counts before symmetry, followed by orbit counts, are:

- r=8: 165 patterns; 43 orbits.
- r=9: 880 patterns; 226 orbits.
- r=10: 2,816 patterns; 720 orbits.
- r=11: 7,008 patterns; 1,786 orbits.
- r=12: 14,946 patterns; 3,802 orbits.
- r=13: 28,680 patterns; 7,284 orbits.
- r=14: 50,940 patterns; 12,922 orbits.

There are 105,435 literal count patterns and 26,783 orbits across all seven layers. `ALL_LENGTHS_INDEX.json` explicitly lists every representative.

The symmetry is multiplication of strides by 3 modulo 16 followed by sign reversal to representatives 1 through 8. Its permutation is

`1->3->7->5->1`, `2<->6`, with 4 and 8 fixed.

This symmetry applies to the **full target**, not just its parity equation. Indeed `Q_a(x^3)=Q_(a^25)(x)` because 11 is the inverse of 3 modulo 16. Applying the field automorphism `a->a^9` then restores Q_a since `25*9=1 mod 32`. Extend that automorphism to algebraic parameters. Reverse negative strides and absorb their extracted monomial by the exact shift identity; the remaining variable rescaling is a sixteenth root of unity and preserves all pole guards. Zero factors can simply be reassigned as zero factors without inversion. The action has order four and preserves the odd-factor count.

The independent verifier uses a second stars-and-bars enumeration and an explicit stride permutation to reconstruct all orbits. It confirms that the lists have neither omissions nor duplicate orbit coverage.

There is also a smaller, complete test for existence at **any** length at most fourteen: pad every shorter pattern with zero stride-one parameters until its length is fourteen. `RESIDUAL_INDEX.json` lists every length-fourteen orbit and all its members. Thus excluding its 12,922 systems would prove r*=15, using the accepted upper witness. If any system survives, the seven-layer index still provides the exact minimization problem; mere survival of a numerical or incomplete algebraic computation is not an attainment witness.

## 6. Exact elimination attempt and resource result

The mixed system tested has

`n=(2,2,2,2,2,1,2,1)`.

It contains eight odd and six even factors and uses every normalized stride class. Its coefficients contain 2,916 distinct grouped monomials. Its saturated system has fifteen variables (fourteen grouped coefficients and u), sixteen equations, 5,692 stored equation terms, and maximum total degree nine over the degree-sixteen number field K.

`attempt_elimination.py` is fresh, inspected code using the installed SymPy 1.14.0 exact algebraic-field engine, grevlex order, and the F5B method. The child is limited to 180 CPU seconds and 2 GiB address space; a separate wrapper imposes a 210-second wall limit and records actual wall time, CPU time, maximum RSS and exit status. No historical discovery or verification code was imported or run.

The final measured outcome is recorded in `RESOURCE_RESULT.json`, with input metadata in `ELIMINATION_STATUS.json` and stdout/stderr in `ELIMINATION.log`. A terminal interpretation is appended after the child finishes. A timeout, resource limit, missing basis, or non-unit intermediate state is not a mathematical answer.

The exact remaining work is to establish emptiness or extract certified algebraic solutions for the indexed J_n systems, in a manner sufficient to obtain the minimum and exclude every smaller layer. A unit ideal must be accompanied by checkable characteristic-zero ideal-membership certificates; a nonempty system must yield factors, individual guards, and all-entry verification. The generic grouped formulation is finite, but no total finishing-time or memory guarantee is known. Resource exhaustion on this one mixed system is evidence about the attempted engine and budget, not a lower bound on every possible algorithm.

## 7. Retained upper witness and stopping boundary

The accepted fifteen-stage algebraic witness remains valid: take the fifteen nonzero ordinary roots rho_j of Q, counted with multiplicity, and set `alpha_j=rho_j^-1`. Then

`Q(x)=product_(j=1)^15 (1-alpha_j x)`

and

`C=16 product_(j=1)^15 (I-alpha_j S)^-1`.

Q has no zero at any sixteenth root of unity by `C Q(S)=16I`; hence every `alpha_j^16 != 1`. The fresh all-entry identity checks the target behind this exact root specification, but this attempt supplies no shorter witness and no new exact minimum. The owner and related view remain open.

## 8. Reproduction and trust boundary

- `python build_residual.py` regenerates the complete indices and the measured exact system.
- `python verify_exact.py` independently checks finite coverage, all target entries, gauge/symmetry coefficient identities, grouped-versus-factor expansion, and the zero-product saturation control.
- `python run_bounded.py` repeats the resource-bounded exact attempt; its result is not part of a claimed minimum proof.

The generator and verifier are standard-library programs. The exploratory elimination additionally uses the installed SymPy package. Source bindings and a final manifest freeze the reports and artifacts. All verification claims are limited to the identities and coverage actually checked.

### Terminal resource interpretation

The child terminated by `SIGXCPU` (return code -24), without a Gröbner basis or ideal-membership certificate. The measured wall time was 183.432574 seconds, recorded child CPU time 185.414128 seconds, and peak RSS 104,476 KiB. The wall-time guard did not fire. These are the measurements reported by the operating system; the configured soft CPU budget was 180 seconds. The memory ceiling was not reached. A continuation of this exact F5B run requires a larger CPU budget; the required completion budget is unknown. No claim that more RAM alone would finish it is supported.

### Elementary complete-pattern controls

The index also marks the seven pure-odd-stride orbits (one in each length layer) as excluded by a direct characteristic-zero certificate. For a pure stride s in `{1,3,5,7}` with r<=14, `c_0=1` and `c_i=0` for `i=15s mod 16`. Thus `f_i=-a^(i^2)` and the exact certificate is `(-a^(-i^2))*f_i=1`. The verifier checks all 28 literal pure-odd cases. This is a control within the full finite problem, not an improved minimum. After these elementary controls, the explicitly unresolved index has 26,776 orbits across all layers, or 12,921 orbits for the padded length-fourteen existence test.
