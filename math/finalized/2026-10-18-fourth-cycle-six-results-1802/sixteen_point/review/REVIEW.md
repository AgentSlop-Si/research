# Independent review: eight odd stages for the sixteen-point chirp

Date: 18 October 2026. Owner: M-MULTISCALE-CHIRP / Q24.

## Verdict

**ACCEPT the scoped lower bound and fifteen-stage constructions. No mathematical correction is required.**

Every legal sixteen-point representation in the original scalar Weyl-monomial / pure-shift-resolvent grammar contains at least eight odd-stride resolvents in characteristic zero and in characteristic 97. Consequently the characteristic-zero interval improves from seven through fifteen to **eight through fifteen** over C and the stated finite splitting extensions. For zeta=46, the interval is also eight through fifteen over F(97^12).

This is not an exact minimum. The bound eight is valid over every characteristic-zero or characteristic-97 coefficient field containing the required primitive 32nd root, but the fifteen-stage upper bound is only asserted in the stated splitting fields. The original cyclotomic coefficient field is not silently assumed to contain the factorization parameters. The broader owner remains open. No catalogue, owner, score, status, census, or external repository was changed in this review.

The earlier characteristic-17 result is preserved only in its already accepted setting: zeta^2=3 for the lower bound, with attainment over F(17^12). This review neither improves that result nor transfers the new characteristic-97 certificates to characteristic 17.

Frozen producer REPORT.md SHA-256:

`815f73e2b9ba34108cddd44fcf33cadc974ac76724280705a315dbe9c85de679`

Frozen producer MANIFEST.json SHA-256:

`7916943bf67c80f52b40b61c3c26614d60d0cb052f2f4b451ac28af11379c546`

## Independent verification and trust boundary

All 38 canonical producer files, both historical source bindings, and all 39 archive entries match their recorded bytes. The archive contains exactly the canonical files and manifest. The accepted historical report and review were read for their model and prior-result scope; no historical code was imported or executed.

The new `independent_verify.py` reads the frozen certificates and does not import any producer code. It builds grouped input equations by Cartesian selections from the four grouped factors, rather than the producer's iterative cyclic multiplication. It verifies each trace node by an exact polynomial zero-residual identity modulo 97, with only earlier nodes allowed. The trace-checking portion uses Python standard-library arithmetic. SymPy 1.14 is used separately for an independent finite-field factorization and irreducibility check. The producer's standalone verifier was also run separately after the independent checks and reproduced its PASS result.

Independent results:

- All 240 input polynomials are exactly the original eight parity equations in each of the thirty cases.
- All 4,568 derivation nodes and 81,904 stored polynomial terms check; the largest stored node degree is six.
- All 120 count vectors are covered by thirty rotation orbits, each of size four.
- Thirty corrupted-input, thirty corrupted-final-polynomial, and 29 invalid self-reference controls are rejected. The remaining trace terminates directly at an input equal to one and has no derived node to corrupt by self-reference.
- All 256 full matrix inverse entries, sixteen parity coefficients, and 256 coefficient shift-normalization instances check integrally in Z[a]/(a^16+1). An off-diagonal target corruption is rejected.
- There are 6,305 independent pole-criterion checks over all F97 parameters and strides -32 through 32, including zero and nongenerating strides.
- The negative-stride reversal identity checks on 12,288 parameter/root instances; the odd class action is exactly 1 -> 3 -> 7 -> 5 -> 1.
- All 75,264 nonzero F97 binomial-pair controls have at most one zero among the sixteen roots. The extension-field theorem relies on the root-permutation proof below, not on these finite controls alone.
- Independent factorization gives unit 19 and irreducible degrees 1,3,3,4,4. The factors are squarefree; Q has no common root with x^16-1; and x^(97^12)=x modulo each factor.
- All 1,296 independent in-place basis-vector applications satisfy the cyclic equations and the exact 31-multiplication/30-addition count.

Full machine-readable results and logs accompany this review.

## Original target, legal normalization, and odd count

The target remains the full matrix C[i,j]=zeta^((i-j)^2). Writing a=zeta^-1 and Q(x)=sum_(t=0)^15 a^(t^2)x^t gives C Q(S)=16 I. The independent check uses direct exponent summation for every matrix entry; it does not merely test selected outputs or assume the inverse polynomial.

Moving each permitted Weyl modulation through a shift resolvent only rescales its parameter. Because both the target and the resulting resolvent product are invertible circulants, a residual Weyl modulation must be scalar. A residual shift is absorbed using the exact identity x^r Q(x)=a^(r^2)Q(a^(-2r)x). This preserves stride parity and the number of nontrivial factors. No arbitrary diagonal gauge or additive branch enters.

For stride s the exact individual legality condition is alpha^(16/gcd(16,s)) != 1. It is equivalent to nonvanishing at every sixteenth root, including for even nongenerating strides. Identity parameters and legal stride-zero scalar factors can be removed. Negative strides introduce only a nonzero scalar and a monomial. Reversing a zero-parameter identity requires no reciprocal.

The identity Q(-x)=x^8Q(x), combined with the even/odd factorization P=OE, gives O(-x)=x^8O(x) because every original even factor is a unit. Therefore it is enough to exclude products with at most seven odd factors; an arbitrarily long even-factor portion cannot evade this obstruction. The conclusion is genuinely at least eight odd factors, not merely a statement about seven total factors.

## Exhaustive polynomial binding and certificate soundness

Every nonidentity odd stride reduces to one of the signed classes represented by 1,3,7,5. Extracting a monomial x^r changes the parity equation's sign by (-1)^r. If necessary, substitution x -> lambda x with lambda^16=1 and lambda^8=-1 restores the positive sign. Such a root exists over each relevant algebraic closure; lambda=8 works in F97.

Substitution x -> x^3 is an automorphism of the cyclic algebra, preserves x^8 because x^24=x^8, and cyclically rotates the four signed stride classes. Subsequent reversals and sign repair do not change their counts. Padding a shorter product with identity factors reaches exactly seven, whose 120 count vectors fall into the checked thirty orbits.

For each count vector, unrestricted grouped coefficients in 1+b_(s,1)x^s+...+b_(s,n)x^(ns) include every original product. Allowing extra grouped coefficients is safe for a nonexistence proof. The independently rebuilt cyclic coefficients c_i give precisely f_i=(-1)^i c_i-c_(i+8), 0<=i<8. The other eight coefficient conditions repeat these with signs, so none is omitted.

Every accepted trace begins with those eight reconstructed f_i. Subsequent nodes are either field multiples of an earlier node or checked polynomial combinations of earlier nodes. Acyclic reference checks, nonnegative exponent checks, and exact modular coefficient checks exclude circular or malformed derivations. The recorded terminal polynomial is literally one. Thus one belongs to the ideal of the original equations over F97 in each of the thirty cases. These are polynomial identities valid over the entire algebraic closure, not finite-point searches, numeric evidence, or trusted Groebner-basis labels.

No nonzero-parameter or factor-invertibility assumption is needed for the modular contradiction. Identity factors, singular affine factors, and arbitrary grouped coefficients are included.

## Characteristic-zero specialization: boundary and nonzero guards

The characteristic-zero conclusion does not follow from a modular unit ideal by itself. The supplied additional argument is valid:

1. Fix the finitely many odd strides of a hypothetical characteristic-zero parity solution. The affine factor equations have rational coefficients. If they have a solution over any characteristic-zero field, their ideal is proper over Qbar and the weak Nullstellensatz supplies a solution with algebraic-number coefficients. A number field can contain those coefficients and all required roots of unity.
2. At a valuation of that field above 97, write each factor as u_j+v_j x^(s_j), then scale its pair so both coefficients are integral and at least one is a unit. The parity relation is homogeneous in every pair, so this scaling preserves it. Every reduced pair is nonzero.
3. The sixteen roots of x^16-1 remain distinct in characteristic 97. For odd s, gcd(s,16)=1, so lambda -> lambda^s permutes those roots over any algebraically closed extension. A nonzero two-term factor has at most one zero on this root set. Nonzero constants and monomials have none. At most seven reduced factors therefore vanish on at most seven roots; their product is nonzero on at least nine roots and cannot disappear in the quotient algebra.
4. Remove reduced constants and extract reduced monomials. Normalize each remaining nonzero constant coefficient to one. The extracted monomial changes only the parity sign, repaired by the same root-of-unity substitution. Reverse signed classes, rotate to a covered count vector, and pad with identities. The number of remaining odd binomials never increases beyond seven.
5. This gives a solution to one of the thirty characteristic-97 systems already proved inconsistent, a contradiction.

The reduction does not assume individual invertibility survives. Poles, lost constant coefficients, reduced monomials, constants, lost degree, and zero parameters are explicitly handled. The pairwise normalization prevents zero individual factors; the root-count argument prevents a zero product. The result is therefore a legitimate characteristic-zero exclusion with the required projective boundary controls.

## Fifteen-stage upper bounds and field scope

In characteristic zero Q has degree fifteen, constant coefficient one, and no zero at a sixteenth root. In a splitting extension its fifteen nonzero roots rho_j, counted with multiplicity, give Q(x)=product_j(1-rho_j^-1 x). Each parameter alpha_j=rho_j^-1 satisfies alpha_j^16 != 1. The scalar 16 and fifteen legal shift-one resolvents reconstruct the full target. The splitting-extension degree bound 15! is valid; no splitting over Q(zeta) itself is asserted.

In characteristic 97, a=19 and zeta=46 are reciprocal and zeta^16=-1. Independent factorization reproduces the displayed linear, two cubic, and two quartic factors, including the leading unit 19. The factor degrees divide twelve, and the direct Frobenius modular checks also confirm every factor splits in F(97^12). The fifteen reciprocal root parameters are the stated linear parameter 46 and the Frobenius conjugates beta_k^(-97^j). Constant coefficient one fixes the factor-product normalization. The independently verified gcd(Q,x^16-1)=1 establishes every individual pole guard.

This is an exact algebraic specification of coefficients, not a coordinate-level root table or a coefficient-discovery algorithm. The lower-bound claim for other characteristic-97 primitive roots does not require this specific finite-field upper witness.

## Application, setup, and representation costs

With alpha and d=(1-alpha^16)^-1 already available, the sixteen-term Horner pass costs 15M_K+15A_K. Multiplying by d costs 1M_K. The recovery of the other fifteen coordinates costs 15M_K+15A_K. Thus one factor costs 31M_K+30A_K.

Fifteen factors and a scalar multiplication on all sixteen outputs cost 481M_K+450A_K per vector. Four squarings per parameter compute alpha^16, so precomputing all d values adds 60M_K+15A_K+15Inv_K. Setup plus one vector is therefore F_coeff+541M_K+465A_K+15Inv_K, with coefficient-field construction, factorization, root discovery, reciprocals, embeddings, and conversions retained in F_coeff.

The independent application test actually overwrites a sixteen-element buffer in place. The Horner pass reads all original coordinates before its first overwrite; subsequent recovery uses only the preceding recovered coordinate and the next still-original coordinate. At most two scalar working registers suffice, separately from the fifteen parameters and fifteen precomputed inverses.

The certificate generation is a research/proof expense, not coefficient setup or vector application. Extension-field operations are not base-field or bit operations. No FFT advantage, arithmetic-runtime lower bound, efficient setup, numerical stability, precision guarantee, or historical-priority claim is licensed.

## Remaining gate

Determine whether legal lengths eight through fourteen exist, or exclude them, while retaining individual invertibility, the full target, and the same operation grammar. Broader dyadic bounds, the original cyclotomic coefficient field, the characteristic-17 problem, efficient coefficient discovery, and numerical certification remain open.
