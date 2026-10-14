# Independent acceptance: parameter gate and cubic twelve-bank exclusion

14 October 2026. Status: **INDEPENDENT ACCEPT, bounded scope**.

## Verdict

The degree-27 parameter theorem in `parameter_gate_candidate/REPORT.md` is accepted. Its exact determinant, all-extension coefficient-rank claim, irreducibility, unique separable nonzero-root quintics, and all 22 nonzero base-field specializations were reconstructed with fresh standard-library arithmetic.

The literal obstruction in `cubic_twelve_failure_candidate/REPORT.md` is accepted. All eleven full-sector systems were reconstructed, and all 132 original inverse branches were freshly inverted. The stated functional annihilates every branch but takes value 14 on the literal target.

**Combining these independently verified statements excludes every representation with at most twelve physical banks over F_(23^3), in the architecture with exactly one effective alpha node in each cross-sign orientation.** This conclusion allows arbitrary legal beta, arbitrarily chosen singleton nodes y and z before the proof, zero/repeated alpha nodes, and cancellations. It is not merely a rejection of one chosen coordinate list.

This review proves no unrestricted-architecture exclusion, no thirteen-bank exclusion or attainment, and no exact minimum of thirteen or fourteen. A matching upper bound, if supplied elsewhere, requires a separate accepted original-bank witness in exactly the same domain.

## 1. Exact domain

Let K=F_(23^3), N=11, q=13, and

    S e_t=e_(t+1 mod 11),  T e_t=13^t e_t,
    F[k,t]=13^(-kt).

A counted physical bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      =(1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j)T^delta)^(-1),
    Delta=1-alpha^11-beta^11 != 0.

All parameters and raw weights belong to K. The signs are independently +1 or -1. No new primitive, limiting node, derivative atom, pre/post map, transformed target, or product of banks is introduced.

Banks sharing an orientation and alpha can be grouped by their normalized sector-amplitude vectors. An effective node has a nonzero grouped vector. Exactly one effective alpha node is required in each cross orientation: y in (-,+), z in (+,-). They are not assumed equal. Ineffective groups contribute zero and do not improve a lower bound on physical summands.

The source's parameter theorem is verified more generally over every field extension K/F23 with the same grammar and q. Its application to all twelve-bank candidates below uses K=F_(23^3) specifically.

## 2. Independent derivation and symbolic verification

The verifier enumerates all binary words through length eleven in each commutation sign. It recovers every ordered coefficient G and the vanishing of all mixed coefficients at length eleven. It independently extracts all 121 Weyl coefficients of the literal target and confirms

    c_F(a,b)=18 f(a,b),  f(a,b)=13^(3(a+b)^2).

No candidate or historical program is imported or executed. The supplied JSON files are inert comparison evidence; moments and matrices are generated anew from the original grammar.

The bank coefficient is

    c_B(a,b)=18 A_b alpha^([epsilon a]_11) G_(epsilon,delta)(a,b),
    A_b=beta^([delta b]_11)/(11 Delta 18)
          * sum_j w_j 13^(epsilon b j).

This formula divides by neither alpha nor beta. Therefore replacing beta, including by zero when legal, cannot evade the necessary normalized sector systems.

At (a,b)=(11-b,b), b=1,...,5, only (-,+) can contribute. Its amplitude is forced, and y is nonzero. On the central positive-exponent windows b<=a<=10-b, both negative-delta orientations vanish. The regenerated triples (u,d,exponent) agree exactly with the parameter report. Thus the same-sign support must realize

    s_(b,j)(y)=u_(b,b+j)-d_(b,b+j)y^(11-2b-j).

All six degree-five recurrence rows were rebuilt. For E consisting of those rows and A=E[:,0:5], the independent computation gives

    det E = 15 H(y),
    H(y)=(y-4)(y-15)P7(y)P18(y),

with P7 and P18 exactly as stated in the source. `RESULTS.json` retains all coefficients and fresh certificates.

Verified without a factorization-library label:

- The factor product reconstructs det E exactly.
- Iterated Frobenius powers and exact extended-Euclidean identities certify that the degree-seven and degree-eighteen factors are irreducible.
- gcd(det E,(det E)')=1, and H(0) is nonzero.
- All six independently recomputed 5-by-5 coefficient minors equal the source values.
- gcd(M0,M1)=1, with an explicit fresh Bezout identity. Consequently rank A(y)=5 at every y in every extension, not only at sampled values.
- gcd(M0,det E)=1. The source's one-denominator Cramer formula works at every compatible parameter.
- All five fresh Cramer numerators equal the source values, and every recurrence residual is divisible by det E.
- gcd(N0,det E)=1, so each compatible quintic has nonzero constant term.
- In each of the four quotient fields for y-4, y-15, P7, and P18, the reconstructed quintic satisfies all six recurrences and has gcd(h,h')=1. Fresh polynomial Bezout certificates are retained. This covers all 27 parameter roots by their irreducible orbits.

Thus compatibility is exactly H(y)=0 and the monic quintic is unique and separable with nonzero constant term.

If any monic common annihilator of degree m<5 existed using all its available recurrence windows, multiplying it by t^(5-m) would produce a degree-five solution with constant term zero. This contradicts the verified unique solution. Hence no degree-at-most-four common annihilator exists for any parameter in any extension.

For actual support size m<=5, its distinct-node support polynomial annihilates all windows; padding as above establishes the necessity of a quintic. Conversely, at a compatible parameter whose quintic splits into five distinct nonzero nodes in K, Vandermonde interpolation fits the first five moments of the long windows and their recurrence forces all subsequent moments; the shorter windows have full-row-rank rectangular Vandermonde systems. This proves the stated window-only equivalence, without claiming full-bank sufficiency.

## 3. Complete base-field comparison

For every y=1,...,22, fresh moments, recurrence matrices, signed-right-hand-side reductions, coefficient rank, surviving quintic, and root list agree with both historical censuses independently. Formal y=0 is additionally checked and incompatible.

All coefficient ranks equal five. Exactly y=4 and y=15 survive:

    h4(t)=t^5+8t^4+t^3+18t^2+4t+6,
    h15(t)=t^5+12t^4+17t^3+14t^2+t+14
           =(t-3)(t-21)(t^3+13t^2+13t+13).

Fresh Frobenius and Bezout calculations certify h4 irreducible and the cubic factor of h15 irreducible. Their base-field root lists are respectively empty and {3,21}.

For direct cubic-field classification, the reviewer additionally computes the exact polynomial identities

    gcd(H(y), y^(23^3)-y)=(y-4)(y-15)=y^2+4y+14,
    gcd(h4(t), t^(23^3)-t)=1,
    h15(t) divides t^(23^3)-t.

These provide direct finite-field certificates in addition to the usual degree-divisibility argument. No huge extension enumeration is used.

## 4. Why this exhausts all twelve-bank candidates

1. Any representation with the stated singleton architecture has at least five distinct nonzero ++ nodes, because four or fewer would supply a prohibited degree-at-most-four window annihilator. Reflection gives at least five distinct nonzero -- nodes. The two effective cross groups require at least one physical bank apiece. Therefore every such representation needs at least twelve physical banks.
2. At most twelve consequently forces exactly twelve and allocation (5,1,1,5), with exactly five distinct nonzero nodes in each same-sign orientation. There is no room for extra physical duplicates, zero-alpha same-sign banks, or canceled groups to change the allocation; allowing them does not weaken this counting argument.
3. The ++ side supplies a split quintic. The cubic-field parameter gcd forces y to be 4 or 15. The y=4 quintic has no root in K and cannot be its support polynomial. Thus y=15, and uniqueness forces the ++ support to be exactly the five roots of h15.
4. Reflection J e_t=e_(-t) preserves F and swaps the two same-sign orientations and the two cross orientations, without changing alpha, beta, or physical count. The same argument forces z=15 and the -- support to be exactly the same root set. Equality of y and z and equality of supports are conclusions, not search assumptions.
5. The independently verified full-sector obstruction below excludes this sole remaining support pattern. Node ordering and choice of a cubic generator are irrelevant; the support is defined intrinsically as all roots of h15.

This proves that no representation with at most twelve physical banks exists in the exact declared domain. It does not decide thirteen-bank patterns such as (5,1,1,6), whose opposite singleton need not be 15.

## 5. Literal full-bank obstruction

Use K=F23[u]/(u^3+13u^2+13u+13). Fresh arithmetic confirms the five distinct nonzero roots

    X={3,21,u,13+20u+14u^2,20+2u+9u^2}.

The last three are u,u^23,u^529. Their product polynomial is exactly h15. All eleven sector systems were rebuilt from the grammar, with coefficient ranks

    (11,7,9,10,11,11,11,11,10,9,7).

Exactly b=3 and b=8 are inconsistent. At b=3, coefficient rank is 10 and augmented rank is 11. The displayed prime-field row vector

    lambda=(0,1,12,18,8,12,2,12,1,0,0)

annihilates all twelve coefficient columns and satisfies lambda*f_3=11.

Define the literal functional

    L(M)=(1/11) sum_a lambda_a sum_t M[(t+a) mod11,t]13^(-3t).

The reviewer directly evaluates L(F)=14. Separately, each of the 132 original branch matrices with beta=1 is reconstructed and freshly inverted. Every inverse equals the supplied literal inverse, all 264 left/right inverse identities pass, and L of every inverse is zero. Hence no raw weights on these branches can produce F.

The arbitrary-beta conclusion does not rest on the beta=1 examples. Independent polynomial contraction gives

    P_++(x)=h15(x)(9x+21x^2),
    P_-+(x)=4x^3+10x^4+19x^5+13x^6+21x^7,
    P_+-(x)=2x+6x^2=6x(x-15),
    P_--(x)=0.

The two cross contractions vanish at 15; the ++ contraction vanishes on X and at zero. For every legal bank, L(B)=18 A_3 P_(epsilon,delta)(alpha). Thus arbitrary beta, weights, and same-node grouping cannot repair the contradiction.

## 6. Stronger obstruction, carefully bounded

The b=3 functional annihilates every -- node, independently of its value or count. Therefore, with the two effective cross nodes fixed at 15 and the ++ support contained in X, adding arbitrarily many -- banks cannot help. Reflection gives the corresponding statement with the roles swapped.

The polynomial identities have prime-field coefficients, so this support-specific statement remains valid in every extension of F23, not only the chosen cubic realization. Combining it with the unique-quintic gate yields a further bounded corollary: **when both effective cross nodes are fixed at 15, any full representation over any extension of F23 requires at least six distinct nonzero nodes in each same-sign orientation, and hence at least fourteen physical banks.** This is only a lower bound in that pinned domain; no attainment is proved here.

It would be wrong to apply that fourteen-bank bound to freely chosen y,z. In particular, P_+-(z)=6z(z-15) is not identically zero. For z different from 0 and 15, the corresponding sector amplitude can contribute to L. The five-node ++ gate alone does not force z=15 when the -- side has six or more nodes. This certificate does not exclude all thirteen-bank free-singleton circuits.

## 7. Reproducibility and audit limits

Run only the newly authored checker:

    python -I parameter_cubic_lower_bound/independent_verify.py

For a separate output directory:

    python -I parameter_cubic_lower_bound/independent_verify.py --out parameter_cubic_lower_bound/cold_replay

The checker imports only Python's standard library. Candidate and historical source code was not executed, imported, or compiled. Only new files in this review directory were written; no external service was changed. `SOURCE_HASHES.json` binds the exact reviewed reports and data. `RESULTS.json` retains the independent symbolic and field certificates, complete base specialization records, sector ranks, and bounded verdict. The cold replay is checked against the deterministic outputs; timing is excluded from byte equality.

No assertion failed and no numerical approximation was used. Arithmetic execution was about one second; this is not total review or reasoning time. Model-token usage is unknown. This review has not verified any separately produced thirteen-bank witness, and makes no novelty, asymptotic speed, or characteristic-zero claim.
