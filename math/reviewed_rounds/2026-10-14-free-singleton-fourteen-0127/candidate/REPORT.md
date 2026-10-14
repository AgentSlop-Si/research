# Removing the alpha=4 pins: exact fourteen-bank singleton minimum over F23

14 October 2026. **Candidate theorem and literal witness; independent review requested.**

## Result

At N=11 and q=13 over F23, removing the two alpha=4 pins while retaining exactly one effective alpha node in each cross-sign orientation changes the minimum number of original banks from the previously accepted sixteen to **fourteen**.

The new explicit witness has orientation allocation (6,1,1,6), in the order (++,-+,+-,--). Its two cross-sign nodes are both alpha=7, and each same-sign group uses the six distinct nonzero nodes

    {6,7,12,13,17,19}.

All fourteen banks have beta=1 and are nonzero. Fresh direct inversion of every original branch verifies all 121 entries of the literal Fourier target. A new all-22-singleton-node moment census proves a matching lower bound of fourteen. This lower bound agrees with the prior independently accepted all-F23 singleton theorem; it does not depend on the alpha=4 pinned obstruction.

The conclusion is about freely located cross-sign **singletons**. It does not claim an unrestricted-orientation minimum. If the singleton requirements themselves are also removed, this witness supplies an upper bound of fourteen, but this report's matching lower bound no longer applies. No characteristic-zero, extension-field, asymptotic, historical-novelty, or FFT-speed claim follows.

## 1. Exact domain and original-bank count

All alpha, beta, and raw weights below belong to F23. Define

    S e_t=e_(t+1 mod 11),  T e_t=13^t e_t,
    F[k,t]=13^(-kt),  0<=k,t<=10.

One counted summand is literally

    B_(epsilon,delta)(alpha,beta;w)
      =(1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j)T^delta)^(-1),
    Delta=1-alpha^11-beta^11 != 0.

The signs independently equal +1 or -1. Arbitrary legal beta values, including beta=0, are allowed in the lower bound. Equal-alpha banks within one orientation can be grouped by adding their sector-amplitude vectors. An effective node is one whose grouped vector is nonzero. Grouping is necessity bookkeeping, not a change to the count of physical summands.

Exactly one effective alpha node is required in (-,+), denoted y, and exactly one in (+,-), denoted z. They may differ. No node value is pinned, and no equal-support or beta=1 restriction is imposed on the minimization. Repeated banks, cancellations, and zero-alpha same-sign banks are allowed. No extra generator, transformed target, pre/post map, derivative atom, infinite node, trace-bank primitive, or singular limit is introduced.

Let b_single(F23) denote the minimum in this domain. The candidate statement proved here is b_single(F23)=14. The accepted predecessor b_4(F23)=16 has the additional conditions y=z=4. The domains are distinct, so the new witness does not contradict that theorem.

## 2. Deriving the alpha-dependent equations

Put U=S^epsilon, V=T^delta, omega=13^(epsilon delta). Then VU=omega UV. For r+ell<=10 define

    D_omega(r,ell)=product_(k=1)^r (1-omega^(ell+k))/(1-omega^k).

Every denominator is nonzero. The same coefficients obey

    D(r,ell)=omega^ell D(r-1,ell)+D(r,ell-1).

At total degree eleven all mixed coefficients vanish. Therefore, with X_j=alpha U+beta omega^j V,

    X_j^11=(alpha^11+beta^11)I,
    (I-X_j)^(-1)=(I+X_j+...+X_j^10)/Delta.

For 0<=a,b<11 set r=[epsilon a]_11, ell=[delta b]_11, and

    G_(epsilon,delta)(a,b)=D_omega(r,ell) if r+ell<=10, else 0.

Character extraction gives the Weyl coefficient of a matrix A as

    c_A(a,b)=(1/11)sum_t A[t+a,t]13^(-bt).

The coefficient of a bank is

    C H_b alpha^r G_(epsilon,delta)(a,b),
    H_b=beta^ell/(11 Delta C) sum_j w_j 13^(epsilon b j).

This formula divides by neither alpha nor beta; it includes zero values using the zeroth-power convention. The literal target has

    c_F(a,b)=C f(a,b),  C=18,
    f(a,b)=13^(3(a+b)^2).

The new code independently extracts and checks all 121 target coefficients and verifies the Gaussian product formula against the ordered-monomial recurrence.

### Forced singleton amplitudes and all five central windows

For b=1,...,5, the coordinate (a,b)=(11-b,b) has only (-,+) support. The target's normalized coefficient there is one. Thus y cannot be zero and the singleton's normalized amplitude is forced:

    T_b(y)=1/[y^b G_(-,+)(11-b,b)].

For b<=a<=10-b both negative-delta orientations vanish and G_(+,+)(a,b) is nonzero. Consequently every legal representation satisfies

    v_b(a;y)
      =[f(a,b)-T_b(y)y^(11-a)G_(-,+)(a,b)]/G_(+,+)(a,b)
      =sum_(x in X) A_(b,x)x^a,

where X is the set of distinct nonzero effective ++ nodes. The same X is used across all five windows; sector amplitudes may differ. Zero-alpha groups contribute zero since a is positive. All legal beta choices have already been absorbed into the amplitudes, so changing beta cannot evade this necessary system.

This is explicitly polynomial in y:

    v_b(a;y)=u_(b,a)-d_(b,a)y^(11-a-b),
    u_(b,a)=f(a,b)/G_++(a,b),
    d_(b,a)=G_-+(a,b)/[G_-+(11-b,b)G_++(a,b)].

For complete numerical specificity, triples below mean (u,d,exponent); read each row in increasing a, beginning at a=b. Every number is modulo 23.

    b=1: (19,0,9), (19,17,8), (10,16,7), (12,22,6),
         (21,2,5), (4,8,4), (2,7,3), (9,1,2), (5,5,1)
    b=2: (21,0,7), (9,20,6), (3,1,5), (1,12,4),
         (19,8,3), (17,4,2), (6,14,1)
    b=3: (6,0,5), (19,8,4), (5,11,3), (9,20,2), (20,16,1)
    b=4: (13,0,3), (3,2,2), (8,4,1)
    b=5: (14,0,1).

In particular, the pinned y=4 numerical moments are just one specialization. Their fixed sextic obstruction cannot be assumed to persist for other y.

### Necessary shared-annihilator systems

Set s_(b,j)(y)=v_b(b+j;y), 0<=j<L_b, where L_b=11-2 b. If X has at most m nodes, with m<=22, pad it to an m-element subset of F23* and let h(t)=sum_(k=0)^m h_k t^k be the product of its distinct linear factors. Then h_m=1, its roots are distinct and nonzero, and

    sum_(k=0)^m h_k s_(b,j+k)(y)=0,
    1<=b<=5, 0<=j<L_b-m.

Padding is a necessary annihilator construction only; it adds no actual bank or amplitude. This covers smaller supports, repeated physical nodes, and cancellation.

For m=5 there are four rows from b=1 and two from b=2. For m=6 there are three rows from b=1 and one from b=2. The shorter windows impose no recurrence at these degrees. A positive recurrence gate is not sufficient for all bank sectors.

Reflection J e_t=e_(-t) satisfies JSJ=S^-1, JTJ=T^-1 and JFJ=F. It swaps ++ with -- and -+ with +-, preserving alpha, beta and original phase weights. Thus the identical necessary systems with parameter z govern the -- nodes. Reflection is a proof of representation symmetry, not an added legal primitive.

## 3. Genuine pin-independent singleton lower bound

The new exact code constructs the monic degree-five system for every y in F23*. The five lower-coefficient columns have rank five in all 22 cases. For 20 values, the augmented system is inconsistent. Only two values have a monic degree-five solution:

    y=4:  h(t)=t^5+8 t^4+t^3+18 t^2+4 t+6;
          nonzero F23 roots: none.
    y=15: h(t)=t^5+12 t^4+17 t^3+14 t^2+t+14;
          nonzero F23 roots: 3,21.

Neither polynomial splits into five distinct nonzero F23 roots. Therefore no y permits at most five distinct nonzero ++ nodes. The argument allows arbitrary other orientations and every legal beta. Reflection proves at least six distinct nonzero -- nodes for every z. Each required cross-sign effective group needs at least one actual bank. Hence

    actual bank count >=6+1+1+6=14.

This proof rederives the q=13 portion of the prior accepted all-220-pair/nine-survivor result, rather than assuming the stronger alpha=4 obstruction. The finite data behind the new proof are complete in MOMENT_CENSUS.json: every moment, matrix, augmented row-reduction, solution, and nonzero-root list is retained.

The lower bound is independent of the node pins. It remains dependent on the cross-sign singleton architecture. With two or more effective nodes in a cross orientation, the coordinate (11-b,b) forces only a weighted sum, not an individual T_b(y), so this proof cannot be reused unchanged.

## 4. What precisely breaks in the sixteen-bank proof

For every y the monic sextic common-annihilator system has rank four and two free F23 coefficients. The complete census therefore contains 22*23^2=11,638 polynomials. Exactly three have six distinct nonzero roots:

- y=7: support {6,7,12,13,17,19};
  h(t)=t^6+18 t^5+6 t^4+21 t^3+8 t^2+20 t+20.
- y=10: support {1,2,4,11,13,18};
  h(t)=t^6+20 t^5+9 t^4+4 t^3+5 t+7.
- y=12: support {3,12,14,15,16,19};
  h(t)=t^6+13 t^5+18 t^4+18 t^3+21 t^2+21 t+11.

At y=4 there is no split sextic, recovering the pinned seven-node necessity. At y=7 that obstruction disappears, and the corresponding full 14-bank system is solvable. Thus this is a literal counterexample to extending the sixteen-bank lower bound merely by deleting its two alpha=4 hypotheses.

The census also gives a necessary condition on any fourteen-bank singleton witness: y and z must each belong to {7,10,12}, with their corresponding same-sign supports exactly as displayed. There are only nine candidate ordered support pairs at that count. The declared search tested the first pair, (7,7), and stopped on success. The other eight pairs were not tested or classified. No sufficiency claim is made for the y=10 or y=12 moment gates.

If one singleton node lies outside {7,10,12}, the same necessary gate gives at least 15 total banks; if both do, it gives at least 16. These are lower bounds, with no new attainment claim for those individual pin pairs.

## 5. Full original-bank witness and literal verification

For (++,-+,+-,--) use the nodes (X,7,7,X), where X={6,7,12,13,17,19}. For each b=0,...,10 solve all eleven equations

    sum_(banks i) A_(i,b) alpha_i^([epsilon_i a]_11)
        G_(epsilon_i,delta_i)(a,b)=f(a,b),  0<=a<=10.

This is a complete original coefficient system, not a recurrence-only interpolation. Its ranks are

    11,8,10,11,11,11,11,11,11,10,8.

All eleven systems are compatible. With beta_i=1, legality is immediate from Delta_i=-alpha_i^11 !=0. Raw phase weights are recovered by

    w_(i,j)=Delta_i C sum_(b=0)^10 A_(i,b)13^(-epsilon_i b j).

The original 1/11 normalization is retained. The code checks the forward character transform for every recovered amplitude.

The full standalone witness WITNESS.json stores every bank's orientation, alpha, beta, Delta, eleven raw weights, normalized amplitudes, literal matrix, every sector system, the aggregate and the target. BRANCHES.json stores all 154 literal matrices and inverses. Fresh modular Gauss-Jordan inversion of the literal branch matrices is independent of the geometric expansion used to derive the coefficient equations.

Checked:

- 154 original 11-by-11 branch inversions;
- 308 left/right inverse-product identities;
- 154 inverse/forward character-transform identities;
- 1,694 bank Weyl-coefficient identities extracted from literal bank matrices;
- all 14 bank matrices nonzero;
- the fourteen orientation/alpha pairs distinct, so every listed group is effective;
- all 121 aggregate entries equal the literal F, with zero mismatches.

The theorem combines this 14-bank upper bound with the previous section's 14-bank lower bound in the exact same domain. The upper bound's beta=1 construction choice does not narrow the lower-bound domain.

## 6. Raw weights

Each row gives epsilon,delta,alpha,Delta and raw w_0,...,w_10. All beta values are 1; all residues are modulo 23.

    +,+, 6,22: 16,16,15,9,22,6,3,5,12,3,7
    +,+, 7, 1: 10,5,0,4,10,6,16,2,16,9,22
    +,+,12,22: 14,16,2,13,22,3,7,17,12,6,17
    +,+,13,22: 14,1,21,11,19,19,1,6,7,5,13
    +,+,17, 1: 7,15,5,11,20,22,19,18,1,18,14
    +,+,19, 1: 1,7,21,11,10,8,9,15,17,9,9
    -,+, 7, 1: 16,10,2,16,10,17,13,14,16,3,6
    +,-, 7, 1: 1,19,20,1,19,9,20,0,10,13,3
    -,-, 6,22: 22,6,16,0,15,0,12,22,8,18,18
    -,-, 7, 1: 13,4,14,11,12,9,15,1,18,19,22
    -,-,12,22: 19,22,13,2,14,18,20,20,2,22,0
    -,-,13,22: 22,17,2,15,8,13,17,2,11,22,11
    -,-,17, 1: 10,17,20,0,2,8,1,3,6,2,14
    -,-,19, 1: 4,19,15,8,12,15,5,13,18,16,13

## 7. Reproducibility, sources, and stop

CONTRACT.md was written before the new computation. The gate is finite and exact: all 22 nonzero y, every monic quintic/sextic in their affine systems, all 22 nonzero field evaluations per candidate, and a full-system pair search stopped at the first fully verified witness.

Run only the new self-contained standard-library source:

    python 3 -I fresh_gate.py --out replay

A cold replay produced byte-identical deterministic census, support list, pair log, witness, branch records, and result summary. REPLAY_VERIFICATION.json binds their hashes and byte lengths. Timing files are excluded from deterministic comparisons. TIMING_AND_ERRORS.json records the session interval and exact run timings; model token usage is unavailable.

Historical code was never executed, imported, or compiled. This task read the accepted base-field review, original moment/construction notes, pinned attainment report, pinned lower-bound review, and literature-scope comparison as inert research documents. Their exact source hashes are recorded in SOURCE_HASHES.txt, with snapshots in source_evidence/. No external service was written and no pre-existing research file was changed.

Independent review should reconstruct the 14 banks from raw weights alone, rederive the all-y necessary systems from the legal grammar, and check the two degree-five survivors and their root failures. The full sextic census and three-support classification are useful additional finite claims; the equality 14 itself needs only the all-y degree-five lower bound plus the literal witness.

The bounded gate is complete. The pin-dependent sixteen theorem does not extend unchanged. The free-singleton problem has a complete candidate equality 14. Unrestricted orientation allocations remain a different unresolved question. This report makes no historical novelty claim and does not upgrade itself to independently accepted status.
