# Recovered Q2 solver domain correction

12 October 2026 UTC. Bounded mathematical and source-interface correction independently accepted at the scope below. The original archive and all original members are unchanged.

## Result

The two-pass row solver requires both beta^m != 1 and 1-alpha^m-beta^m != 0. The recovered `THEOREM.md` Section 2 presents that elimination after stating only the second condition. This omission is real, but the preserved earlier theorem and the supplied implementation already contain the missing guard. It is a documentation/interface correction, not evidence of an implementation error on admitted inputs.

The fixed alpha=beta=1/4 construction meets both guards at every m>=2. Its published exact-scalar O(N) solver claim is unaffected by this correction. The algebraic inverse identity and the triangular support formula need only the full inverse denominator (plus nonzero alpha/beta for exact support); they must not acquire an unnecessary beta^m!=1 restriction.

## Source binding

Archive: [FFT_Chain_Recovered_Phase_Q2_2026-10-13.zip](sources/FFT_Chain_Recovered_Phase_Q2_2026-10-13.zip), SHA-256 dd8fa0bd6e7c6016922f1f5ab64ea81bcb80931b9f18df15a35dc9db88140e60.

- `THEOREM.md` lines 34–54: algebraic inverse under 1-alpha^m-beta^m !=0 followed by the unqualified row-inverse solver description. SHA-256 ff6f36d2da31a41058eeec1fef664930b711ed31a39a338f9c514dcfc550d7f6.
- `PRIOR_QTGF.md` Section 4 explicitly assumes beta^m!=1 and product_a alpha_a !=1-beta^m for its O(N) row algorithm. Section 5 distinguishes the larger algebraic-inverse domain from the executor.
- `verify_recovery.py` function `qtorus_solve`, lines 58–62, computes both powers and explicitly asserts Bm!=1 and 1-Bm-Am!=0 before inverting 1-Bm. Its existing admitted fixtures therefore do not demonstrate the omitted domain.

All supplied programs were inspected as inert text; none was executed or imported.

## Corrected statement

Let m>=2, N=m², and let the exact field contain a primitive m-th root q. Let A and B act on coordinates (a,c) in (Z/mZ)² by (Ay)[a,c]=y[a-1,c] and (By)[a,c]=q^a y[a,c-1]. Given alpha,beta, assume

1. beta^m !=1;
2. delta=1-beta^m-alpha^m !=0.

Then, for every full input f, the stated two-pass cyclic row algorithm computes the unique y satisfying (I-alpha A-beta B)y=f using O(N) exact field operations and O(N) field storage, with supplied q and charged O(N) parameter/root-table preparation. This is an exact-scalar statement, not a finite-word stability or physical-time bound.

### Proof

For the m-cycle shift T, every row block D_a=I-beta q^a T has determinant 1-(beta q^a)^m=1-beta^m, so it is invertible exactly when guard 1 holds. A single row solution of z_c-gamma z_(c-1)=b_c is obtained by an affine recurrence around the cycle and one division by 1-gamma^m; it costs O(m).

All D_a are polynomials in the same T and commute. Their product is I-(beta T)^m=(1-beta^m)I. Therefore the product of their inverses is (1-beta^m)^(-1)I.

One forward row sweep from zero boundary gives a vector p at row m-1. Starting from a general boundary h changes that final vector by alpha^m/(1-beta^m) times h. Periodicity therefore gives

h = p + alpha^m/(1-beta^m) h,

h = (1-beta^m)/delta * p.

Guard 2 justifies the scalar boundary correction. A second row sweep with this boundary constructs the required cyclic solution. Two sweeps each contain m solves of length m; all input/output and root/parameter preparation are at most O(N). The preserved variable-alpha theorem replaces alpha^m with product_a alpha_a and is consistent with this specialization.

## Explicit counterexample outside the elimination domain

Take m=2, q=-1 and alpha=beta=1 over Q. Then delta=-1, so the full 4 by 4 operator is invertible. In the coordinate order (0,0),(0,1),(1,0),(1,1),

L = ((1,-1,-1,0),(-1,1,0,-1),(-1,0,1,1),(0,-1,1,1)).

Its determinant is 1. Since (A+B)²=2I,

L^(-1)=-(I+A+B).

For f=e_0 the exact solution is y=(-1,-1,-1,0).

However, beta^m=1, and the two row blocks are

D_0=((1,-1),(-1,1)),
D_1=((1,1),(1,1)),

both singular. The required row inverses and the code's division by 1-beta^m do not exist, even though the full inverse does. Thus full-operator invertibility does not suffice for this elimination order. No claim is made that another O(N) algorithm cannot cover this case.

## Fixed schedule and independent checks

For alpha=beta=1/4 and m>=2, 0<4^(-m)<=1/16 and delta=1-2*4^(-m)>=7/8. Both guards hold uniformly. This all-m inequality preserves the published dense-transform construction.

A new, self-authored `q2_guard_check.py` verifies the 4 by 4 example with exact Fraction arithmetic, both inverse products, det L=1, both singular row blocks, the displayed e_0 solution, and 63 exact-rational fixed-schedule controls m=2..64. It imports no supplied source. The counterexample and all-m guard proof are mathematical; the finite controls corroborate them.

- Checker SHA-256 e7724c2b335246ffd4bdbede02903b4d2bc80f698128331d7085023349ba4546.
- Result `q2_guard_results.json` SHA-256 7a6e8a897b9ffa0baafa8d4ebd221d7314e226f1785ac0a910e89d5ca45071d5.

## Remaining scope

The independent review closes only the solver-domain documentation obligation. The full Q2 numerical program, all saved full-output and stationary-Q minimal-polynomial certificates, broader solver domain, production bit/stability costs, general Fourier synthesis and historical priority remain outside this audit. Preserve the original archive bytes and attach this corrected statement as a dated supplement.

## Independent review

The separate `q2_independent_review.md` accepts the guarded statement and counterexample, while preserving the larger algebraic inverse domain and the fixed one-quarter construction. Broader Q2 claims remain outside its scope.
