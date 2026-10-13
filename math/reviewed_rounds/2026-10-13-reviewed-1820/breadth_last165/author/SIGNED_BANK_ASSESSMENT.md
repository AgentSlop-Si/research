# Signed-bank variable-singleton assessment: candidate only

## Useful result

In the original N=11 signed-bank grammar over F23, at the primitive root q=2, every nonzero F23 node for a single minus-plus bank forces at least six effective plus-plus nodes. Simultaneous reflection yields the same six-node lower bound for the minus-minus orientation when plus-minus is a singleton. Thus at least fourteen banks are required in the restricted architecture with one cross-sign singleton in each orientation and both singleton nodes in F23. Other bank nodes may lie in an extension. This is a fresh bounded candidate, pending independent review, and not an unrestricted fourteen-bank minimum.

The broader diagnostic enumerates all 10 primitive eleventh roots in F23 and all 22 nonzero singleton nodes: 211/220 necessary local recurrence matrices are nonsingular; nine are singular. A singular matrix is only a surviving necessary gate. It is not a Fourier representation. In particular no root-uniform or characteristic-zero conclusion follows from the q=2 result.

A separate exact check of all 529 parameter pairs in the source's mirrored, singleton-one sextic family finds no polynomial with six distinct nonzero F23 roots. This blocks direct base-field use of that exact two-parameter family. It does not rule out another fourteen-bank construction or a splitting-field realization.

## Why this is distinct from completed work

The early N11 construction leaves a full non-depressed quintic test open, but the later `WHOLE_LEFT_RANK_ENVELOPE.md` Section 7 and `BANK_QUINTIC_INDEPENDENT_REVIEW.md` already close it and establish the restricted fourteen-bank optimum when the cross-singleton nodes are 1 in characteristic zero. That accepted stage is preserved and was not redispatched. The present new bounded gate varies the singleton node over F23. N5 all-permitted-field minimum and N7 cases also remain closed.

## Source-bound reduction

Let f(a,b)=q^(3(a+b)^2) and retain the source Gaussian factors G_(epsilon,delta)(a,b), equal to the Gaussian coefficient for r=[epsilon a]_11, ell=[delta b]_11 when r+ell<=10 and zero otherwise. All Gaussian denominators used below are nonzero.

Suppose the minus-plus orientation has a single effective node y. The exclusive coordinate a=11-b forces its sector amplitude to

    T_b(y)=1 / (y^b G_-+(11-b,b)).

The case y=0 cannot match the nonzero exclusive Fourier coefficient. On the intervals a=1,...,9 for b=1 and a=2,...,8 for b=2, neither negative-delta orientation contributes. Therefore the plus-plus moments must equal

    v_b(a) = [f(a,b)-T_b(y)y^(11-a)G_-+(a,b)] / G_++(a,b).

A sum supported on at most five effective nodes has a nonzero degree-at-most-five common annihilator. Padding by powers of the variable, if necessary, produces a nonzero length-six coefficient vector annihilated by every six-term window. The four windows from b=1 and two from b=2 produce the reported 6x6 matrix. A nonzero determinant excludes that representation. Zero plus-plus nodes do not rescue the model: all tested exponents are positive, and the same annihilator argument remains necessary.

At q=2 and y=1 the determinant is 4 mod23, matching the later accepted source control. The determinants for y=1,...,22 are:

    4,11,9,19,11,16,7,9,12,8,21,3,13,7,19,15,6,7,16,1,6,14.

Every value is nonzero. Simultaneous reflection (a,b)→(-a,-b) preserves f and exchanges the two same-sign orientations and the two cross-sign orientations. It requires no extra gauge or coordinate transformation in the representation.

## Controls and cost

`SIGNED_BANK_F23_RESULT.json` records every one of the 220 matrices. The fresh first checker uses product Gaussian coefficients and elimination determinants. The alternate checker uses q-Pascal Gaussian coefficients and reduced row rank; all matrices and nonsingularity decisions agree. The singular q=3,y=4 control prevents an accidental universal pass. `SIGNED_BANK_SPLIT_SEARCH.json` records the separate 529-parameter split-node assessment. A separate enumeration of all74,613 six-node subsets of F23^* reconstructs their monic polynomials and checks the four source recurrence equations, also finding no compatible set. The source moment arrays are reconstructed from the fresh Gaussian checker rather than trusted as unverified constants. No supplied historical scientific program was run.

All arithmetic in these diagnostics is exact modular arithmetic. These finite case counts are checker workload, not bank-execution complexity. A counted bank still contains eleven inverse branches and eleven raw weights. No FFT, bit-cost, physical-speed, literature-priority or novelty conclusion is claimed.

## Exact next task and stop

Independently derive the variable-singleton moment reduction from the original branch formula, replay all 220 matrices and the 529 split tests, and check reflection, zero-node, field-extension and arbitrary-beta guards. Stop with a scoped acceptance, precise counterexample, or checker/source mismatch. Do not broaden this into a minimum for all orientation allocations or a characteristic-zero result. The signed-bank parent remains OPEN56, unchanged.
