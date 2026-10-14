# A literal thirteen-bank witness over F23 cubed

14 October 2026. Candidate attainment certificate, awaiting independent review.

## Result and scope

The first of exactly three declared configurations succeeds. Over E=F23[u]/(u³+13u²+13u+13), with N=11 and q=13, the literal Fourier matrix has a representation by thirteen nonzero original signed-resolvent banks. The orientation allocation is (5,1,1,6) in (++,-+,+-,--) order:

- ++ nodes: X={3,21,u,13+20u+14u²,20+2u+9u²}.
- -+ node:15.
- +- node:7.
- -- nodes:{6,7,12,13,17,19}.

Every beta is1. The last three elements of X are u,u^23,u^529. Each is a separate actual bank; no trace-bank primitive is introduced. All thirteen orientation/alpha pairs are distinct, and all thirteen literal bank matrices are nonzero. Thus each cross orientation has exactly one effective node.

The two other declared cases, with (+- node, -- support) equal to (10,{1,2,4,11,13,18}) or (12,{3,12,14,15,16,19}), fail exactly in coefficient sector3. They have exact null-functional certificates, also verified on every literal inverse branch.

This proves a candidate upper bound of13 in the stated extension-field singleton grammar. It does not establish a minimum. A separate all-parameter lower-bound audit and independent acceptance of this witness are required before combining them into an equality. Nothing here classifies other thirteen-bank supports or unrestricted orientation allocations.

## Original grammar and field

Let S e_t=e_(t+1 mod11), T e_t=13^t e_t, and F[k,t]=13^(-kt), for0<=k,t<=10. One counted bank is exactly

    B_(e,d)(alpha,beta;w)
      =(1/11) sum_(j=0)^10 w_j
          (I-alpha S^e-beta 13^(edj) T^d)^(-1),
    Delta=1-alpha^11-beta^11 !=0,
    e,d in {+1,-1}.

Nodes, beta values, and raw phase weights lie in E. The cubic has no F23 root, independently checked at all23 residues, so it is irreducible. An element is encoded as [a,b,c]=a+b u+c u² with all coefficients modulo23. No generator replacement, coordinate change, pre/post transformation, products of banks, derivative atoms, singular limit, or additional primitive is allowed.

All executed arithmetic code was newly authored for this bounded task. Historical programs were neither executed, imported, nor compiled. There were no external writes.

## Why these are the correct orientation pairings

With U=S^e, V=T^d and omega=13^(ed), VU=omega UV. Let D_omega(r,l) be the coefficient of U^r V^l in (U+V)^(r+l), and

    G_(e,d)(a,b)=D_omega([ea]_11,[db]_11)

when the two nonnegative exponents sum to at most10, and zero otherwise. Fresh code enumerates every binary word through length11 to derive these coefficients. Every mixed degree11 coefficient vanishes. The product formula for D is checked independently against word counting.

For a matrix M, write

    c_M(a,b)=(1/11) sum_t M[t+a,t]13^(-bt).

Direct extraction from the literal F gives c_F(a,b)=C f(a,b), C=18 and f(a,b)=13^(3(a+b)^2). Every target coordinate was checked, rather than assuming this formula.

The normalized bank coefficient is

    A_(i,b) alpha_i^[e_i a]_11 G_(e_i,d_i)(a,b).

For b=1,...,5, the sole-support coordinate a=11-b forces the -+ amplitude at node y. In the positive central window b<=a<=10-b, both negative-delta orientations vanish, so the shared ++ support is governed by that -+ node y. The cubic five-node support belongs to y=15. Reflection J e_t=e_(-t) swaps both signs and leaves F invariant, so the -- support is governed by the +- node z. Therefore the correct pairing is (++ X, -+15, +-z, --Y_z), not a swap of the two cross nodes. Reflection is used to derive the orientation relation, not as a new bank operation.

Only the three explicitly declared z values7,10,12 and their accepted six-node supports were tested. No wider support enumeration was performed.

## Complete coefficient solve and raw weights

For each b=0,...,10 the new program solves every one of the eleven equations

    sum_i A_(i,b) alpha_i^[e_i a]_11 G_(e_i,d_i)(a,b)=f(a,b),
    a=0,...,10.

For all three cases the coefficient ranks are

    11,7,9,10,11,11,11,11,11,10,8.

For z=7 every system is consistent; free variables are set to zero in the deterministic row-reduced solve. With beta=1, Delta=-alpha^11 is nonzero. Raw phase weights are recovered as

    w_(i,j)=Delta_i C sum_b A_(i,b)13^(-e_i b j).

The forward transform is checked for all143 sector amplitudes. The complete143 raw weights are in RAW_CERTIFICATE.json and WITNESS.json, using explicit triples. RAW_CERTIFICATE.json also specifies the field, grammar and target, so it can be verified without invoking the coefficient solver. WITNESS.json additionally contains all sector equations, row reductions, chosen amplitudes, thirteen literal bank matrices and the aggregate.

## Literal verification

The implementation independently builds each original matrix

    I-alpha S^e-13^(edj)T^d

entry by entry and obtains its inverse by fresh Gauss-Jordan elimination. It does not use the geometric expansion to invert the matrices. The raw weights are applied with the original1/11 normalization.

For the successful z=7 witness:

-143 literal inverse matrices and286 left/right inverse-product identities pass.
-143 raw inverse/forward character-transform identities pass.
-1,573 bank Weyl coefficients extracted from literal matrices agree with the solved coefficients.
-All13 bank matrices are nonzero.
-All121 entries of their sum agree with the literal F, with zero mismatches.
-The thirteen orientation/alpha pairs are distinct, and exactly one nonzero bank occurs in each cross orientation.

A second polynomial-dictionary multiplication and monic long-division implementation checks multiplication by u and multiplicative inverses for180 distinct field elements occurring in the inverse data. This supplements the direct matrix checks; independent acceptance remains a separate task.

The two negative cases were checked equally literally:143 inverses each,286 inverse identities each, and143 zero functional evaluations each. The full run therefore records429 literal inversions and858 inverse-product identities across the three declared cases.

## Exact failures at z=10 and z=12

All vectors below are indexed by a=0,...,10 and lie in F23. For z=10, take

    lambda_10=(0,15,17,18,6,21,20,16,1,0,0).

For z=12, take

    lambda_12=(0,22,8,18,5,14,6,18,1,0,0).

For the corresponding full sector3 coefficient matrix M_3,

    lambda_10^T M_3=0, lambda_10^T f_3=8;
    lambda_12^T M_3=0, lambda_12^T f_3=18.

Thus the coefficient rank10 increases to augmented rank11 in each case. Define the literal functional

    L_z(M)=(1/11) sum_a lambda_(z,a) sum_t M[t+a,t]13^(-3t).

The program checks L_z directly on every143 inverse branches, obtaining zero. Direct target evaluation gives L_10(F)=6 and L_12(F)=2. Hence no raw weights can solve either tested configuration. These are exact obstructions, not failed numerical solves.

The full matrices, row reductions, null vectors and literal evaluations are retained in CASES.json. No stronger failure outside the tested supports is needed or claimed.

## Mutation controls and reproducibility

Twenty-seven deterministic rejection controls pass: perturb one raw weight, omit1/11, reverse the target exponent, delete each of13 banks separately, reverse all branch phase signs, corrupt an inverse entry, admit the singular alpha0/beta1 case, change the cubic constant, replace the support node3 by1, move a same-sign bank to a second cross node, swap cross nodes without reflecting supports, and perturb or zero either negative-case null vector.

A cold replay of the final source reproduces all deterministic outputs byte for byte. Exact input source hashes, output hashes, byte counts and archive hashes are retained. The contract was written before the first computation; its three-case boundary was respected.

Reproduce using only the new program:

    python3 -I fresh_thirteen_gate.py --out reproduced

The main arithmetic run and cold replay each took about1.8 seconds, including all three cases and controls. Exact timings are stored in the output folders. That is arithmetic wall time, not total research time; model-token usage is unavailable. There were no assertion failures or arithmetic exceptions, except the deliberately caught singular-matrix mutation.

The bounded construction task is complete. Candidate attainment13 and the two exact alternatives' failures are ready for independent review. Historical novelty, other characteristics, characteristic-zero lifting, asymptotic complexity and FFT speed are outside this result.
