# Independent review: exact eight-point chirp minimum seven

Date: 18 October 2026. Owner: M-MULTISCALE-CHIRP / Q24.

## Verdict

**ACCEPT the scoped theorem and concrete extension-field corollary.** No mathematical correction is required. The exact minimum is seven over C and over a finite splitting extension of Q(zeta16), in the stated literal grammar of individually invertible pure-shift resolvents with scalar Weyl-monomial gauges. The lower bound holds over every characteristic-zero coefficient field containing the chosen primitive sixteenth root. The displayed seven-stage F17^3 construction is also valid, and its minimum is seven for zeta=3.

This review does not close the broader owner, claim attainment over Q(zeta16) itself, establish novelty, or derive an arithmetic/runtime lower bound. No external files, catalogue rows, scores, statuses, or census totals were changed.

Frozen reviewed REPORT.md SHA-256:
0556d429c5b753f936f04b9872bdbc1d52704c9500b0faaee679b026c4c0e0b2

All 15 canonical entries in the candidate MANIFEST.json matched their recorded hashes and byte sizes. No candidate executable was imported or run by the independent verifier. Candidate mathematical text and certificate data were inspected directly.

## Independent exact checks

The separately authored independent_verify.py and its INDEPENDENT_RESULTS.json establish:

- All 64 entries of C Q(S)=8I in the integral cyclotomic ring Z[a]/(a^8+1), by direct matrix multiplication.
- All five stored polynomial ideal identities, using separately implemented SymPy polynomial reconstruction and arithmetic over F17.
- Every stored input-polynomial list equals the numerator of its necessary rational equations after exact cancellation. The equations were also independently derived from the original eight cyclic coefficient equations, as detailed below.
- An additional direct algebraic-closure check: all nine normalized length-five patterns with at least four odd strides have unit coefficient-equation ideals over F17 after adjoining h*z=1. The grouped polynomial coefficients are unrestricted; this is not a search of F17 points. Fewer-stage cases are included by zero-padding factors. Cases with fewer than four odd strides are excluded by the reviewed parity argument.
- The defining cubic for F17^3 and the second displayed cubic are irreducible over F17.
- Each of the seven displayed extension-field parameters has alpha^8 != 1, their binomial product equals Q, and literal multiplication of all seven cyclic resolvents gives C in all 64 matrix entries.

The extra direct Gröbner checks are corroboration. The candidate's reproducible core remains its five explicit, independently verified polynomial identities and elementary boundary arguments.

## Normalization and parity audit

Moving Weyl gauges through the resolvents only rescales parameters. The final modulation must be scalar because the candidate and inverse target are invertible circulants. Net shifts can be removed using q_(t-r)=a^(r^2-2rt)q_t. Negative strides introduce only an allowed scalar and monomial. The x -> x^3 symmetry, followed by x -> -x and the same monomial normalization, permits n1 >= n3. No arbitrary diagonal gauge is introduced.

The relation Q(-x)=x^4 Q(x) forces the odd-stride product O to satisfy the same relation: the even factor product is a unit and can be canceled. With zero through three odd factors, its paired coefficient conditions are incompatible with nonzero individual parameters. In particular, the 113/133 three-factor cases have a nonzero x^2/x^6 coefficient lacking its partner.

For four odd factors, 1111 forces the singular polynomial 1+x^4. In 1113, the coefficient conditions force the single stride-three parameter d^4=1, so that factor is singular. In 1133, the nondegenerate branch gives B=E=epsilon, D=-epsilon A and A^2=-2epsilon. The degenerate branch A=D=0 gives a multiple of x^2(1+x^4), also singular.

For the remaining branch, the candidate's U and V formulas are correct: they result from multiplying by (2-epsilon y)/3 modulo y^2-1 and by (1+epsilon y)/2 modulo y^2+1. The two-stride-four, mixed-stride and two-stride-two product exclusions follow exactly. In the last case, epsilon=-1 would imply a^2=2(-3+4b)/9 and then 177b=-28, contradicting b^2=-1 in characteristic zero. At a=6,b=4 modulo 17, the two sides of the first equation are 2 and 1.

The five-odd cases with a stride-four factor or no even factor reduce to H Q_c with H,c nonzero. I verified their coefficient eliminations. For 11133, the x^6 equation simplifies to c^2=(1+b)/2; the remaining x^1 equation is inconsistent with b^2=-1 in characteristic zero and at b=4 modulo 17. The separately computed direct unit ideals corroborate all five-stage modular boundary cases without these elimination shortcuts.

## Necessary-equation and guard audit

Writing normalized grouped factors with constant coefficient one:

- 510: the x^4 and x^7 equations give aD^2-D+a=0. The x^3, x^5 and constant equations give bD^4+aD^3+D^2+aD+b=0. Here D and target scalar h are nonzero.
- 420: the x^5 and x^7 equations force D,E nonzero. The constant equation gives h=D/(D+aE), and x^2 gives E=b+aD+a/D. The remaining displayed equations are precisely x^6 and x^1 after these substitutions.
- 330: x^5 and x^7 force D,E nonzero. The constant, x^5, x^6, x^7 and x^2 equations give the displayed h,A,B,C,F. The three certificate inputs are the remaining x^1, x^3 and x^4 residuals.
- 411: parity gives B(1+D^4)=-2D^2, A=-BD and H=B/D+D. Individual legality gives D^8 != 1, so 1+D^4 != 0. The even coefficient equation gives e=(b-B)/(1-bB); the denominator cannot vanish because it would force b-B=2b != 0. The displayed residuals are the odd coefficient-ratio and odd/even amplitude conditions.
- 312: parity gives C=-D-AE, B=E-D^2-ADE, A(1-E^2-D^2E)=D^3, and 1+BE=AD. If D=0, parity forces E^2=-1 and A=C=0, producing a singular odd product. Hence D and R=1-E^2-D^2E are nonzero. The three affine forms in e are exactly the remaining necessary ratio and amplitude equations. Their pairwise determinants and the parity residual must vanish. The verified D^6 ideal identity excludes this guarded set.

Every rational denominator is accounted for by these guards or by a nonzero field constant. Exact rational cancellation followed by reduction modulo 17 does not introduce an identically zero denominator in any stored input. Clearing denominators only enlarges the necessary zero set. The E^2 and D^6 certificate targets therefore have the required nonzero values on hypothetical legal solutions.

## Characteristic-zero specialization audit

The specialization argument is valid and does not infer characteristic-zero emptiness from a finite-point count.

1. Polynomial equations and inverted nonvanishing guards defining a hypothetical solution have coefficients in Q(a). A nonempty such affine scheme has a point over a finite algebraic extension of Q(a), by the weak Nullstellensatz.
2. Choose a number-field prime above (17,a-6). Root-of-unity target coefficients are integral units there. Scale each binomial coefficient pair projectively to lie in the valuation ring with at least one unit. This is allowed even when the original parameter has a pole.
3. After scaling the factors, the target scalar is exactly the constant coefficient P0 of their reduced cyclic product, and is integral. Thus P_i=q_i P0 survives reduction; no assumption that the original scalar was a unit is needed.
4. Every remaining six-factor pattern has sum gcd(s_j,8) equal to six or seven, strictly below eight. A nonzero reduced projective binomial has at most gcd(s_j,8) zeros on the eight distinct eighth roots; monomial and constant limits have none. Therefore the product cannot become the zero element of the cyclic algebra.
5. The homogeneous equations now force reduced P0 != 0. Since reduced Q is invertible by C Q=8I, the reduced product is a unit and each factor is a unit.
6. A constant or monomial factor removes a stage. Its scalar/shift is absorbed by the already verified chirp normalization, contradicting the algebraic-closure lower bound for at most five stages. Otherwise every factor normalizes to the affine charts excluded by the five exact certificates.

This controls scalar collapse, parameter poles, vanishing parameters, monomial limits, loss of degree, and the all-zero product boundary. No unguarded specialization step remains.

## Attainment

Q has degree seven and nonzero constant coefficient. Factoring it over its splitting field produces seven normalized linear binomials. Because Q has no zero on the eighth roots, no individual factor can vanish there, so all seven resolvents are legal. The all-row inverse identity supplies the scalar gauge 8. This proves exact attainment over C and a finite algebraic extension, without making any unsupported coefficient-discovery or computational-cost claim.
