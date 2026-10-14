# Independent bounded review: recovered Q29 normalization

Verdict: **PASS at the stated bounded scope. No mathematical correction identified. Full Q29 ordinary-discriminant value and nonvanishing remain OPEN.**

Reviewed on 2026-10-14 UTC. The input packet is `Q29_Higher_Layer_Bounded_Normalization_and_Discriminant_Gap_2026-10-14.zip`, with expected SHA-256 `29f2fd3524b7d7d2548b3d0480fbcb605768987a34b428814c22343bd4a44ce4`. Exact input hashes are recorded in `SOURCE_HASHES.json`.

## What was independently executed

The reviewer wrote `recompute.cpp` from the direct relation

    H_n(-1-v) = -v H_(n-1)(-1-v) + (1+v)(1-q^(n-1)) H_(n-2)(-1-v).

It uses degree-18 field coordinates directly, with multiplication by eta implemented by reduction of eta^18 = -eta^9 - 1. Multiplication by `(1+x)^a` uses the base-5 factorization into powers of `1+x`, `1+x^5`, and `1+x^25`, with dense truncated x and v arrays. Thus it differs from the primary author's group-algebra calculation and from the reciprocal-polynomial implementation. It computes H1687 modulo `(x^100,v^101)` and returns `U1687(-1-v)=-H1687(-1-v)/v`. It also verifies that the constant-in-v remainder vanishes throughout x<100.

Only this new C++ executable and the newly written `check.py` were executed for this review. No author scientific executable, historical uploaded program, or imported author module was executed. The author source files were read as inert text. No external writes were made.

All 10,000 shared-center coefficient vectors match the recovered packet exactly, including zero vectors: 180,000 coordinates over F5, with 7,818 nonzero vectors. `check.py` separately computes the following checks from the reviewer's output, rather than using the author's derived results as input.

## Accepted arithmetic and precision

1. The instance is t=27, p=5, e=3, q=eta*zeta125 of order3375. H1687 is monic of degree1687; removal of the exact persistent factor z+1 gives U1687 of degree1686. The reciprocal polynomial R has degree843. The subscript1687 is an H-index, not the degree of U.
2. `ord_27(5)=18`, so Phi27 is irreducible over F5 and the specified degree-18 residue field is correct. Phi125(1+pi) is Eisenstein of degree100, giving v_pi(5)=100. Reduction modulo pi^100 is genuinely the characteristic-five truncated ring k[x]/x^100. Coefficient valuations strictly below100 transfer to the actual mixed-characteristic root. A missing coefficient at precision100 is not an exact zero.
3. The negative-slope Newton vertices are exactly `(0,75),(10,50),(50,10),(60,1),(62,0)`. Since all later coefficients are integral, unknown higher v-degrees cannot undercut these negative-slope segments. The root valuations and multiplicities are `(5/2,10),(1,40),(9/10,10),(1/2,2)`.
4. Every nonzero jet monomial has total degree at least60. The omitted error lies in `(pi^100,v^100)`; after v=pi Y and division by pi^60 it is coefficientwise divisible by pi^40. This proves integrality of the full F and certifies coefficients strictly below40. The residue is

       F mod pi = A(Y^10+3Y^30+Y^50) = A Y^10(Y^4-1)^10,
       A = (1,1,0,4,4,1,2,3,2,3,0,0,4,2,2,3,2,1).

   A is nonzero. The residue has degree50 while F still has degree1686. Every residual exponent is divisible by5, so the derivative residue is zero.
5. Fresh translation of the normalized jet gives precisely the reported five first faces. For c=0,1 the constant valuation is15, root radius relative to Y-c is3/2, and the divided face is `A(Z^10-1)`. For c=2,4 the constant valuation is10, radius1, and the face is `A(Z-1)^10`. For c=3 it is valuation10, radius1, and `A(Z-3)^10`. A fractional scaling uses an appropriate ramified extension. After face division the available absolute precision is strictly below25 or30, respectively. These faces remain inseparable.

## Accepted discriminant accounting

The following assertions were independently derived; small exact symbolic computations additionally test the signs and scaling laws.

- For a degree-d polynomial, `Disc(c f(aY+b))=c^(2d-2) a^(d(d-1)) Disc(f)`. Here d=1686, c=pi^-60 and a=-pi. Consequently

      Disc_Y F = pi^2638710 Disc_z U1687.

  The full degree1686 is necessary; degree50 cannot be used in this identity. The leading coefficient of F is pi^1626.
- Removing H's persistent linear factor gives `Disc H=U(-1)^2 Disc U`. The freshly computed constant has valuation75, so that removal accounts for exactly150 in the valuation.
- For `U=z^m R((1+z)^2/z)`, writing R as a product over w_i writes U as a product of `z^2+(2-w_i)z+1`. Their discriminants are `w_i(w_i-4)`, and the pairwise resultants are `(w_i-w_j)^2`. Thus the classical exact identity, including its positive sign, is

      Disc U = (Disc R)^2 R(0)R(4).

  This is a standard reciprocal-polynomial identity, with no novelty claim. It remains valid as a polynomial identity when a discriminant vanishes.
- `U(-1)=-R843(0)` gives v_pi R843(0)=75. A fresh scalar H recurrence at z=1 gives a nonzero residue for U1687(1)=R843(4), independently confirming the other endpoint is a unit. Therefore

      v_pi Disc U1687 = 2 v_pi Disc R843 + 75

  with extended valuations if zero. A finite total would be odd; neither finiteness nor the value is established.
- A fresh finite-field computation of U13 verifies degree12, gcd(U13,U13')=1, and nonvanishing at every `-eta^j`, j=0,...,26. Together with the standard q-Lucas factorization this justifies unit cross-resultants and the simple remainder. This does not verify the higher jets at the other centers.
- For the 62 shared-center roots, direct summation of `2 min(v(alpha_i),v(alpha_j))` over all pairs gives3687. This agrees with the explicit annular scale contribution1867 and cross-resultant contribution1820. In the degree40 radius1 annulus, the four disjoint nonzero residue disks have ten roots each. Their extra within-disk radii are3/2,1,1,1, giving at least `90*(3/2+1+1+1)=405`. Hence the local bound is

      v_pi Disc W0 >=4092.

  This is a lower bound, including when the discriminant vanishes. The c=0 disk belongs to the inner annulus and must not be counted again. The full ordinary-discriminant valuation is not4092 by this argument. The outer degree2 edge has two nonzero coefficients, at degrees0 and2 after normalization, and therefore a squarefree quadratic residue in characteristic5; this does not resolve the other annular factors.

## Exact remaining gaps and guardrails

No correction to the sealed packet's bounded mathematical assertions is needed. Its explicit limitations are essential:

- The normalized local repeated branches still have inseparable residues.
- The value and nonvanishing of Disc R843 are not proved.
- Alternatively, all contributing repeated factors at all27 centers, or a proved valid symmetry reduction, remain necessary for a complete local resolution.
- This review independently recomputed only the shared-center jet. The author's single-method j=1 corroboration has not been promoted to an independent all-center result.
- Precision100, normalized precision40, and subsequent precision25/30 are exclusive ceilings. Passing a ceiling requires a certified higher mixed-characteristic lift that retains carry terms.
- No squarefree-residue, divided-derivative unit, full-Q29, all-layer e>=3, algorithmic-complexity, physical-speed, or novelty conclusion follows.

`CHECK_RESULT.json` contains the exact machine-readable bounded result. `AUDIT_RECEIPT.json` records UTC timing and all encountered errors, including repaired test-harness issues that did not alter the mathematics. `SOURCE_HASHES.json` binds the input bytes, and `MANIFEST.json` binds this review payload.
