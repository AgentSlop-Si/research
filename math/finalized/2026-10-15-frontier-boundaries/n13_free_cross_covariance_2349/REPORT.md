# N13: exact rescaling covariance and the free-cross normalization obstruction

14 October 2026 UTC. Local bounded mathematical artifact; independent review pending. No historical program was executed. No external service was changed.

## Result first

**The natural simultaneous alpha rescaling does not give a target-preserving reduction to y=z=1.** Its coherent action is

    alpha_(+,delta) -> c alpha_(+,delta),
    alpha_(-,delta) -> c^(-1) alpha_(-,delta),
    (y,z) -> (c^(-1)y, cz).

Thus **yz is invariant**. Even if yz=1, the cyclic, common-row covariance has c^13=1 and changes the normalized Fourier target to c^a times that target, up to a sector scalar. Preserving the specified target forces c=1. A broader amplitude adjustment for arbitrary nonzero c has an explicit wrap correction; it still cannot preserve this target unless c=1.

More precisely, all invertible diagonal column-to-row covariance transports obtained by multiplicatively rescaling the alpha nodes are classified below. The only such transports that fix the Fourier target leave every alpha node unchanged. A reflection may exchange y and z, but cannot set either nonunit node to one.

This is an obstruction to a proposed normalization method, **not a nonexistence theorem for sixteen-bank certificates with arbitrary y,z**. Solving new full-sector systems after a rescaling can involve different weights, different supports, and cancellations; that is a new representation problem and is not justified by covariance. The degree-2/3/4 question in the freely varying cross model remains open.

## 1. Fixed model and normalized coefficients

Work over any field L of characteristic 53, with q=16 of order N=13. The fixed matrices are

    S e_t=e_(t+1), T e_t=q^t e_t, F[k,t]=q^(-kt).

One physical bank is the original signed-resolvent expression

    (1/13) sum_j w_j (I-alpha S^epsilon-beta q^(epsilon delta j)T^delta)^(-1),
    Delta=1-alpha^13-beta^13 != 0.

The accepted expansion, normalized by the nonzero Gauss factor gamma=7, has column

    C_(epsilon,delta;alpha)(a,b)
      =G_(epsilon,delta)(a,b) alpha^[epsilon a]_13,

and a freely chosen sector amplitude A_(epsilon,delta;alpha,b) at every nonzero alpha. The normalized target is

    f(a,b)=q^(10(a+b)^2),

which is nonzero at all 169 pairs. At a=0 or b=0, all four relevant G coefficients are 1. Arbitrary sector amplitudes can be implemented in the original grammar with beta=1 and Delta=-alpha^13, using the raw-weight formula in the source descent report. Thus the arguments below concern actual original-bank coefficients, rather than trace-valued or quotient replacement banks.

At sixteen banks the inherited lower theorem forces allocation (7,1,1,7), all alpha nodes nonzero, and one effective cross node y in (-,+) and z in (+,-).

## 2. Classification of diagonal rescaling covariance

This section states exactly what is classified. For each bank i, replace its node alpha_i by s_i alpha_i, with s_i nonzero. Allow its sector amplitude to be multiplied by any nonzero d_(i,b). A diagonal column-to-row covariance means that for some row multipliers R(a,b), independently of the amplitude values,

    C_b(alpha') diag_i(d_(i,b)) = diag_a(R(a,b)) C_b(alpha).

Here C_b contains the original bank columns and a common row multiplier is required because their sum is to transport a target. This permits separate node scalings and separate bank/sector scalars at the outset, not merely one assumed common c.

**Theorem.** Such a covariance exists if and only if there are c with c^13=1 and nonzero sector scalars kappa_b such that

    s_i=c       for every epsilon_i=+1,
    s_i=c^(-1)  for every epsilon_i=-1,
    d_(i,b)=kappa_b for every i,
    R(a,b)=kappa_b c^a.

This holds over every characteristic-53 extension; it is not inferred from a finite-field census.

Proof. At (a,b)=(0,0), each original and rescaled column is 1, so d_(i,0)=R(0,0)=kappa_0. At b=0, compare rows a=1 and a=2. The scale of every positive-epsilon column must be the same value p=R(1,0)/kappa_0, and R(2,0)/kappa_0=p^2. Each negative-epsilon scale m must satisfy

    m^12=p, m^11=p^2.

Dividing these nonzero equations gives m=p^(-1), and then p^13=1. Thus every negative scale is the same inverse and c=p. At a=0 in any sector, again every column is 1, so d_(i,b)=kappa_b is independent of i. Since c^13=1,

    c^(epsilon [epsilon a]_13)=c^a

for either sign, proving sufficiency and the formula for R wherever G is nonzero. Every row has a nonzero G in at least one orientation: choose signed residues in {0,...,6}, whose sum is at most 12. This also proves necessity of the displayed R on every row. No alpha or G equal to zero has been divided out on a row where it vanishes.

If the transported target is the same f, then R(a,b)f(a,b)=f(a,b), and f never vanishes. Row a=0 gives kappa_b=1 for every b; row a=1 gives c=1. Hence all s_i=1. This establishes the claimed target-preserving rigidity within the precise covariance class.

## 3. Parameter invariant and cyclic-generator covariance

Under the coherent action from section 2,

    y'=c^(-1)y, z'=cz, y'z'=yz.

Consequently setting both new cross nodes to 1 would require yz=1 and c=y=z^(-1). For cyclic covariance one also needs y^13=1. Neither condition makes the target invariant: the fixed-target equations still force c=1, hence y=z=1 already.

The individual values y^13 and z^13 are also invariants under cyclic rescaling. If reflection is allowed, yz and the unordered pair {y^13,z^13} remain invariant.

The same conclusion follows directly from the matrix algebra. An invertible scaling S -> cS, T -> dT preserves S^13=T^13=I only when c^13=d^13=1. Then

    B_(epsilon,delta)(alpha,beta;w)
      -> B_(epsilon,delta)(c^epsilon alpha,d^delta beta;w),
    f(a,b) -> c^a d^b f(a,b).

The commutation relation and each Delta are preserved. All thirteenth roots of unity already lie in F53 because q has order 13, so these are actual finite Weyl-character symmetries over every extension. For c=q^u and d=q^v the map is conjugation by S^(-v)T^u. The fixed Fourier target has no nontrivial symmetry in this scaling subgroup: its nonzero coefficients at (1,0) and (0,1) force c=d=1. Allowing arbitrary sector reweighting can absorb d^b but cannot remove the a-dependent factor c^a.

Simultaneous sign reflection is a separate valid target symmetry: J e_t=e_(-t) gives JFJ=F and sends (epsilon,delta) to (-epsilon,-delta), exchanging y and z. It does not normalize their values. A field automorphism fixing F53 likewise sends y,z to their images and can send either to 1 only if it was already 1.

## 4. Exact independent rescaling equations and the wrap defect

For a given certificate, let P_b(a) be the sum of its positive-epsilon contributions and N_b(a) the sum of its negative-epsilon contributions, so P_b(a)+N_b(a)=f(a,b). Uniformly scale the positive nodes by p and the negative nodes by m, and multiply their amplitudes in sector b by u_b and v_b. The exact transformed sum is

    f'(a,b)=u_b p^a P_b(a)+v_b m^(13-a) N_b(a),  1<=a<=12,
    f'(0,b)=u_b P_b(0)+v_b N_b(0).

There is no convention allowing replacement of the exponent at a=0 by 13. In particular, independent cross normalization uses p=z^(-1) and m=y^(-1). With the convenient choice u_b=kappa_b, v_b=kappa_b y^13, it would require

    kappa_b [z^(-a)P_b(a)+y^a N_b(a)]=f(a,b),  1<=a<=12,
    kappa_b [P_b(0)+y^13 N_b(0)]=f(0,b).

These are additional equations on the actual certificate, not identities. The two row factors coalesce only on yz=1. Separate changes in all individual amplitudes would require a new full-sector solve and are not provided by these equations.

Even drop the cyclic condition and take any c in L*. Put p=c, m=c^(-1), u_b=kappa_b and v_b=kappa_b c^13. All rescaled nonzero nodes are legal using beta=1. Then

    f'(a,b)=kappa_b c^a f(a,b),                   1<=a<=12,
    f'(0,b)=kappa_b f(0,b)
             +kappa_b(c^13-1)N_b(0).

The last term is the exact cyclic wrap defect. It cannot repair the Fourier target: at a=1 and a=2 in any sector, target preservation requires kappa_b c=1 and kappa_b c^2=1, which give c=1 and kappa_b=1. Thus permitting this more general sign-dependent amplitude adjustment does not restore a lossless normalization.

## 5. The same obstruction in the accepted forced windows

This gives a direct connection to the descent report. Set

    R_b(a)=G_-+(a,b)/G_-+(13-b,b),
    v_y(a,b)=[f(a,b)-y^(13-a-b)R_b(a)]/G_++(a,b).

The sole (-,+) amplitude is T_b=y^(-b)/G_-+(13-b,b), for b=1,...,6. Try the coherent rescaling c=y that sends its node to 1. Its amplitude must become 1/G_-+(13-b,b), forcing the common-row-adjusted factor kappa_b=y^(b-13). The positive-epsilon moments transported by this rule are

    kappa_b y^a v_y(a,b)
      =[y^(a+b-13)f(a,b)-R_b(a)]/G_++(a,b).

The required moments at y=1 are

    v_1(a,b)=[f(a,b)-R_b(a)]/G_++(a,b).

Their difference is exactly

    (y^(a+b-13)-1) f(a,b)/G_++(a,b).

Already the valid forced row b=1,a=11 has exponent -1, G_++=43 and f=46, hence f/G=6. The discrepancy is exactly 6(y^(-1)-1), which vanishes only if y=1 over every characteristic-53 field. For example, y=2 gives discrepancy 50 in F53. The reflected argument applies to the other cross node. This pinpoints the failure of inserting a rescaled free-cross certificate into the pinned y=z=1 equations; no division by a potentially zero G is used outside the accepted forced window.

## 6. Explicit legal covariance that fails to preserve F

Take c=q=16, d=1. Conjugation by T maps every original bank to an original bank with alpha replaced by q^epsilon alpha, preserving every branch denominator and all raw weights. Starting from any accepted pinned certificate, its cross nodes become

    (y',z')=(10,16),  y'z'=1 in F53.

But its sum becomes TFT^(-1), whose entries are

    (TFT^(-1))[k,t]=q^(k-t-kt).

The entry (k,t)=(1,0) changes from 1 to 16; exactly 156 of the 169 matrix entries change. Thus even the product-one locus and a legal thirteenth-root scaling do not preserve the fixed target. This example asserts the transformed representation of TFT^(-1); it does not assert a new original-target witness at cross nodes (10,16).

## 7. Fresh bounded verification and stopping condition

Only newly authored `check_fresh.py` was run. It independently rebuilt all G coefficients, checked their two axes, extracted all 169 Fourier Weyl coefficients and gamma=7, and verified the explicit transformed-target mismatch. It checked the full original branch inverses for one newly specified legal bank in each orientation and its q-scaled counterpart: 104 inverse matrices and 208 two-sided inverse product identities, plus 52 branch-conjugation identities and four weighted-bank identities.

For a finite sanity check, it tested the three b=0 covariance equations over all 52^2 base-field scaling pairs, finding precisely the 13 reciprocal root-of-unity pairs and only (1,1) among fixed-target pairs. This enumeration is not the proof over extensions; section 2 supplies that proof. It also checked 338 synthetic instances of the exact wrap-defect identity and rebuilt the section 5 forced-window discrepancy at all 52 nonzero base-field values of y. No support enumeration or extension-field search was performed, and no historical scientific code was imported, executed, or compiled.

`CHECK_RESULT.json` gives the complete small receipt. `SOURCE_BINDINGS.json` binds the source reports read as inert text. This task stops at the exact covariance classification and obstruction. It supplies neither a freely varying cross-node exclusion nor a new attainment certificate, minimum-degree claim, novelty claim, or arithmetic-speed claim.

## Source references

- `n13_descent_obstruction_2343/REPORT.md`, sections 1, 2, 5 and 7: sixteen-bank allocation, amplitude implementation, pinned obstruction and unresolved normalization gate.
- `n13_extension_quotient_gate_2045/sources/PRIOR_LOWER_REVIEW.md`, sections 1, 3 and 4: original bank grammar, Weyl expansion, fixed target, cross forced amplitudes and moments.
- `n13_extension_quotient_gate_2045/CONTRACT.md`: exact scope of the earlier bounded pinned census.
- `n13_publication_claims_audit_2341/THEOREM_AND_OPEN_OBLIGATIONS.md`: current accepted minima and the unresolved freely varying field classification.
