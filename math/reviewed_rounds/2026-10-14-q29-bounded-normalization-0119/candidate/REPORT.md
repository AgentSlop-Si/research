# Q29: recovered higher-layer normalization and exact discriminant accounting

14 October 2026 UTC. Status: **reproduced bounded result; full ordinary-discriminant gate remains open**.

## 1. Exact scope and result

Fix t=27, p=5, e=3. Let eta be a chosen primitive 27th root in the unramified degree-18 extension O of Z_5, let pi=zeta_125-1, and set q=eta(1+pi), an actual primitive 3375th root. Normalize v_pi(pi)=1, so v_pi(5)=100. The residue field is k=F_5[eta]/(eta^18+eta^9+1); ord_27(5)=18 proves this polynomial irreducible and fixes the primitive residue component.

H_n is the monic Rogers–Szegő polynomial of degree n. Throughout this report,

    n=1687,  U_1687(z;q)=H_1687(z;q)/(z+1),  deg_z U_1687=1686.

The subscript 1687 indexes the parent H polynomial. It is not U's degree. The persistent factor is removed by exact polynomial division. At the shared center z=-1-v, the convention is exactly U_1687(-1-v;q)=-H_1687(-1-v;q)/v.

Two different fresh recurrences reproduce all 10,000 shared-center coefficient vectors for x<100 and v<100, totaling 180,000 coordinates in F_5. The negative-slope Newton vertices at the actual higher root are

    (v degree, coefficient valuation): (0,75),(10,50),(50,10),(60,1),(62,0).

Consequently the 62 shared-center roots have pi-valuations 5/2 with multiplicity 10, 1 with multiplicity 40, 9/10 with multiplicity 10, and 1/2 with multiplicity 2. Here multiplicities count roots in the algebraic closure, including any unresolved repetitions; no simplicity assumption is made.

The integral normalization

    F(Y)=pi^(-60) U_1687(-1-pi Y;q)

has the nonzero residue

    F mod pi = A Y^10 (Y^4-1)^10,

where A is the following nonzero element of k, given in the basis 1,eta,...,eta^17:

    (1,1,0,4,4,1,2,3,2,3,0,0,4,2,2,3,2,1).

Thus the radius-1 annulus genuinely splits into four residue centers c=1,2,3,4, each of degree 10. The residue is still inseparable. In particular F' mod pi=0, so this normalization supplies no squarefree-residue or divided-derivative unit assertion.

The exact ordinary discriminant target is D=Disc_z U_1687(z;q), with degree 1686. A classical reciprocal-polynomial identity gives

    D = (Disc_w R_843)^2 R_843(0)R_843(4),

where U_1687(z;q)=z^843 R_843((1+z)^2/z;q) and R_843 is monic of degree 843. The instance-specific endpoint calculations give

    v_pi R_843(0)=75,  v_pi R_843(4)=0,
    v_pi D = 2 v_pi(Disc_w R_843)+75.

The last identity uses extended valuations if the discriminant is zero. Any finite claimed total must therefore be odd. The classical identity is not a novelty claim. Neither the value nor nonvanishing of Disc R_843 is established here.

## 2. Recovery and independent finite reconstruction

Previously saved local scientific files were recovered. No unsaved result was inferred. The saved primary C++ program uses

    H_n=(1+z)H_(n-1)-z(1-q^(n-1))H_(n-2)

at z=-eta^j(1+v), q=eta(1+x), in F_5[C_27][x,v]/(x^100,v^101). It then projects the eta group algebra to k. At j=0 it extracts -H/v, keeping v<100. The ordinary binomial exponent can be reduced modulo125 when x<100 in characteristic5; (1+x)^125=1 modulo x^100. Every recurrence operation preserves these truncation ideals.

The independent program instead uses

    R_m=(w-2+q^(2m)+q^(2m-1)) R_(m-1)
        -(1-q^(2m-1))(1-q^(2m-2)) R_(m-2),
    R_0=1, R_(-1)=0.

This follows by eliminating the even H terms from the preceding recurrence and dividing the identity H_(2m+1)=(1+z)z^m R_m(w), w=(1+z)^2/z. It keeps w<50 and x<100, and multiplies q powers using their base-5 Frobenius factorization. The substitution

    U_1687(-1-v;q)=sum_k (-1)^(843+k) r_(843,k)(q) v^(2k)(1+v)^(843-k)

shows why w<50 gives every coefficient with v<100: omitted k>=50 begin at v^100. The recurrence never decreases w-degree. The independent signed small checks m=0,...,6 pass before eta projection.

A clean replay compiled both saved fresh sources, reran both primary centers j=0 and j=1, and reran the independent shared-center construction. Both primary coefficient arrays equal their saved arrays after excluding nondeterministic elapsed-time fields. The independent U13 and U1687 output files are byte-identical to the saved files. There are 7,818 nonzero shared-center vectors. Exact comparisons and canonical hashes are in controls/RECOVERY_COMPARISON.json.

Only the shared center received the two-recurrence independence test. The reproduced j=1 output is preserved as a single-method corroboration, not an all-center symmetry proof or independent acceptance of the other 26 centers.

No historical uploaded scientific program executed. The only scientific programs executed are the newly authored local scientific programs and fresh audit. Historical reviews were read as inert documents.

## 3. Mixed-characteristic precision, carries and normalization

The Eisenstein polynomial Phi_125(1+pi) has degree100 and constant5. Hence (5)=(pi^100) in the local DVR up to a unit, and

    O[pi]/(pi^100) is k[x]/(x^100), x mapped to pi.

This is the actual-root mixed-characteristic quotient, not an assertion that 5 is zero at arbitrary precision. It proves that every displayed coefficient valuation strictly below100 is exact. All characteristic-zero carry terms first enter at the absolute pi-adic ceiling100. Unknown coefficients cannot be called zero at that ceiling.

Let J be the lifted shared jet. The exact error is in (pi^100,v^100). After v=pi Y and division by pi^60, the error is coefficientwise in pi^40. All computed coefficients have a+b>=60; omitted raw x-degrees contribute at least100, and omitted v-degrees at least100 after substitution. This proves F integral, with certified precision strictly below40. The only terms on a+b=60 are A v^10 pi^50, 3A v^30 pi^30, and A v^50 pi^10. They give A Y^10(Y^20-1)^2=A Y^10(Y^4-1)^10 in characteristic5.

For a further integral translation Y=c+pi^b Z, b>=0, the error stays at least40; dividing additionally by pi^h leaves only precision40-h. Ordinary differentiation in Y preserves the pi^40 error bound. Converting a derivative after a new variable scaling must explicitly account for the inverse scale. Neither differentiation nor residue cancellation licenses discarding these precision losses.

The recovered and independently rechecked next faces are:

- c=0: ten roots with v_pi(Y)=3/2; after division by pi^15 the face is A(Z^10-1), with precision strictly below25.
- c=1: ten roots with v_pi(Y-1)=3/2; the same divided face A(Z^10-1), with precision strictly below25.
- c=2,4: ten roots in each disk with v_pi(Y-c)=1; after division by pi^10 the face is A(Z-1)^10, with precision strictly below30.
- c=3: ten roots with v_pi(Y-3)=1; the divided face is A(Z-3)^10, with precision strictly below30.

All decisive coefficients are below40. Each face is again inseparable in characteristic5. The exact coefficients are in controls/NORMALIZATION_AUDIT.json. These faces are bounded root-location data, not terminal discriminant-unit proofs.

## 4. Negative controls

The same-residue lower root would be q_lower=eta(1+pi)^5, of order675. Modulo pi^100 this substitutes x^5 for x. At v-degree10 the correct actual-higher-root coefficient has valuation50 and leading coefficient A. The incorrect lower-root substitution has valuation at least100. Thus this substitution is arithmetically detected; it is not merely rejected by a schema check.

Replacing the shared-center convention -H/v by H/v sends A to -A, a distinct nonzero element in characteristic5. The signed independent small recurrences and this coefficient check detect the mistake.

No old order-675 scaling, its rejected unit witnesses, or the rejected unrestricted shared-U inequalities were used as a proof of the new normalization.

## 5. Ordinary discriminant accounting, including every scale

The convention for a monic degree-d polynomial is Disc(f)=product_(i<j)(alpha_i-alpha_j)^2. For nonmonic f the standard leading-coefficient factor is included.

### Persistent factor

Since H_1687=(z+1)U_1687,

    Disc_z H_1687 = U_1687(-1)^2 Disc_z U_1687.

The exact coefficient calculation gives v_pi U_1687(-1)=75. Removing this persistent linear factor therefore removes precisely150 from the discriminant valuation. It is not silently included in D.

### Full normalized polynomial

The full F is of degree1686, although its residue is of degree50; its leading coefficient is pi^1626. Translation does not change a discriminant, variable scaling by a contributes a^(d(d-1)), and scalar multiplication by c contributes c^(2d-2). Therefore

    Disc_Y F
      = pi^(1686*1685 - 60*(2*1686-2)) D
      = pi^2638710 D.

Using degree50 in this identity would be wrong. This formula does not evaluate Disc F or certify a unit after removing the displayed power.

### All residue centers and the simple remainder

The classical q-Lucas block identity at q=eta gives

    U_1687(z;eta)=(1+z^27)^62 U_13(z;eta).

The fresh independent finite-field computation proves that U13 has degree12, gcd(U13,U13')=1, and U13(-eta^j) is nonzero for every j=0,...,26. Thus Hensel factorization in the complete local DVR yields an exact monic factorization

    U_1687 = E product_(j=0)^26 W_j,
    deg E=12, deg W_j=62,
    E mod pi=U13, W_j mod pi=(z+eta^j)^62.

The ordinary product-discriminant identity is

    D = Disc(E) product_j Disc(W_j)
        product_j Res(E,W_j)^2 product_(i<j) Res(W_i,W_j)^2.

Every displayed cross-resultant and Disc(E) is a unit: their reductions are pairwise coprime, and E has squarefree reduction. Hence v_pi D=sum_j v_pi Disc(W_j). This proves that discarded cross-center terms have valuation zero; it does not determine the 27 local discriminants.

To compare the local v-coordinate z=alpha_j(1+v), alpha_j=-eta^j, define the monic degree62 polynomial L_j(v)=alpha_j^(-62) W_j(alpha_j(1+v)). Then Disc_z W_j=alpha_j^(62*61) Disc_v L_j. These powers are explicit units. At j=0, degree62 is even and L_0(v)=W_0(-1-v).

### Shared-center annular factors

Write L_0 as the four monic Newton-slope factors A_i of degrees (10,40,10,2). In an extension with rho^10=pi, let a=(25,10,9,5) and define

    Ahat_i(Y)=rho^(-a_i d_i) A_i(rho^(a_i)Y).

Each Ahat_i is integral and monic with unit constant term. Since the a_i decrease strictly, for i<j

    Res(A_i,A_j)=rho^(a_j d_i d_j) C_ij,
    C_ij=Res_Y(Ahat_i(Y), Ahat_j(rho^(a_i-a_j)Y)).

C_ij is a unit because its reduction is Ahat_j(0)^d_i. Thus the exact identity is

    Disc_v L_0 = rho^36870 (product_(i<j) C_ij^2)
                 product_i Disc_Y Ahat_i.

The within-factor scaling valuations are225,1560,81,1, totaling1867. The squared cross-resultant valuations are800,180,20,720,80,20, totaling1820. Consequently

    v_pi Disc L_0 = 3687 + sum_i v_pi Disc Ahat_i.

The outer degree2 factor has squarefree residual quadratic with nonzero constant term, so its normalized discriminant is a unit. The other terms have not been evaluated. Their repeated residue factors cannot be replaced by units.

Factor the normalized degree40 annular polynomial into the four monic degree10 Hensel disk factors B_c, c=1,2,3,4, with B_c mod pi=(Y-c)^10. They have pairwise unit resultants after the Y scaling. Their further certified intra-disk radii 3/2,1,1,1 contribute at least90*(3/2+1+1+1)=405 beyond the preceding baseline. Hence the bounded local consequence is

    v_pi Disc L_0 >=4092.

This is a local lower bound, valid also if the discriminant vanishes. It is neither the full ordinary-discriminant valuation nor an equality claim.

### Classical reciprocal identity and exact endpoint values

For any monic degree-m R and U=z^m R((1+z)^2/z), let w_i be the roots of R. Then U is the product of z^2+(2-w_i)z+1. Each quadratic has discriminant w_i(w_i-4); each pair has resultant (w_i-w_j)^2. The ordinary product formula proves

    Disc U=(Disc R)^2 Res(R,w(w-4))=(Disc R)^2 R(0)R(4).

The sign is positive; the two endpoint evaluation signs cancel. Being a polynomial identity, it holds even without separability. The independent finite-field check verifies it on U13 and R6, in addition to this algebraic derivation. This standard identity is included for correct accounting, with no historical or mathematical novelty claim.

For the present instance R has degree843. Since U(-1)=(-1)^843 R(0), the shared coefficient gives v_pi R(0)=75. A fresh direct scalar recurrence for H_n(1;eta), through n=1687, gives U_1687(1;eta) nonzero, proving R(4) is a unit at the actual root. Thus the endpoint contribution is exactly75 and v_pi D=2 v_pi Disc R_843+75.

## 6. Precise remaining gate

This audit supplies a source-bound integral normalization, exact first and second root-location faces below a justified mixed-characteristic ceiling, a global ordinary-discriminant identity with exact endpoint contribution, and explicit local/cross-resultant/scaling accounting. It does not supply the missing normalized local discriminants.

A complete ordinary-discriminant value or nonvanishing proof still requires either:

1. resolving Disc R843 with certified exact arithmetic and an all-degree argument; or
2. resolving every contributing repeated local branch in the 27 W_j factors, or proving a valid symmetry reduction, with sufficient precision for each derivative, discriminant and resultant.

In the shared factor alone, the degree10 or degree5 residual branches remain nonreduced. A continuation may use existing jets only while every decisive absolute valuation remains strictly below its transformed precision ceiling. If it reaches the ceiling, it must retain and certify the mixed-characteristic pi^100 carry terms in a higher lift. No claim is made that the current jet either suffices for or rules out such a continuation.

The second primary center j=1 does not establish the other25 polygons, and similar-looking first faces are not a symmetry proof. The global reciprocal identity does not close the unknown R843 discriminant. The all-layer e>=3 problem, general squarefreeness, algorithmic complexity, physical speed and historical novelty remain unchanged.

## 7. Preservation and limitations

The predecessor split review and small t=1,p=3,e=3 calibration were hash-bound and read as prior evidence. Their accepted scopes and rejected claims are preserved, not rerun or relabeled as new results. No table, score, external repository, uploaded source, or other external state was changed.

Run python3 replay.py for a clean finite reproduction and python3 verify_manifest.py for payload integrity. The archive is a locally sealed bounded research result, not a full Q29 acceptance. Audit timestamps, prior interruption, output truncations, one cancelled optional exploratory calculation, and unknown token usage are explicitly recorded in AUDIT_RECEIPT.json.
