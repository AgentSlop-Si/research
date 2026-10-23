# Independent acceptance: fast-axis generator in the improved range

Date: 2026-10-23 UTC. Verdict: **ACCEPT this separate domain composition.** No frozen predecessor is altered or retrospectively assigned the larger domain.

## Binding and exact conclusion

Author packet: `signed_bank_fast_axis_new_range_20261023_v1`.

- ADDENDUM.md SHA-256: `1132fd344f8007a41a4d4a26197b66c08e97be62b365272c6aae747a70139032`.
- MANIFEST.json SHA-256: `75bb995a3491347728493afa0a8d79b3a677dca68fc641ff37da090246e5418b`.

For N odd, d>=4, N>=6d-2, and the original supplied coefficient-field/root interface, a represented list of 2N distinct scalars suffices for deterministic construction of a monic degree-m polynomial g in the SAME original U, m=N-d, satisfying g(0)!=0, gcd(g,g')=1, and full original-axis row rank. The complete coefficient-stage bounds are O(N^4) additions/multiplications, O(N^3) inversions, and O(N^2) live field elements. These bounds include failures, both coprime-combination loops and output.

This is the narrower old-domain fast-axis theorem composed explicitly with the already accepted new-range two-pencil theorem. It is not a new 5N/3 bank-count result, an improvement over the expected O(N^3) Las Vegas coefficient bound, an efficient splitting-field construction, a whole-owner closure, or an FFT/novelty claim.

## Dependency and degree audit

The accepted new-range pencil addendum, SHA-256 `da880d924870bc312dd8eff5ce57c5937104f1ffc7174dc191a4ddb458e190be`, supplies on N>=6d-2 the exact original-U gcds, endpoint independence, actual reciprocal witness f, and both coprime pencils. Its independent acceptance is `signed_bank_pencil_new_range_independent_20261023`, review SHA-256 `a1b08c5d1cd99340b4f632e434bfe0110e6d1c4ece186a1b97257d9c6edf173f`.

The accepted fast-axis theorem, SHA-256 `54a19739c708ea5d0e38e9fd18408ff7bf50ccfb5849f800ece67ac9829959dc`, with review `6e10976c19f56b2480b4dc278e4e2250db4caacb4c4d1fa299890acb595fd863`, was accepted only at N>=8d-10. I independently checked each of its uses of that domain against the larger range:

1. The exact original-axis congruence t rev_n(h)b=c b_(d-1)H_N modulo h uses only n+(d-1)=N-2 and g=(t-1)h. It does not use the old gate, squarefreeness, or c!=0. The normalized gcd test uses c!=0 explicitly and retains all reciprocal multiplicities.
2. The degree-N-1 cancellation still gives an (N-1)-by-2d affine coefficient matrix. Its row margin is N-2d-1>=4d-3>0.
3. At h0=t f, reciprocal coprimality forces f dividing b. Its degree margin is r-(d-1)=N-2d-1>=4d-3>0. Hence the same matrix has full column rank at zero and a nonzero 2d-row minor of degree at most 2d.
4. The normalized reciprocal-coprime residue margin n-(d-1)=N-2d>=4d-2>0 remains valid. The complete exceptional-gcd case split requires no stronger inequality.
5. Generic squarefreeness of the accepted second pencil and its nonzero linear constant coefficient are unchanged, including characteristic two. Thus the complete guard degree is still 2d+1+(2m-2)=2N-1.
6. Every consumer of the common scalar list fits: r+2=m for the first coprime loop, n+1=m for the second, and 2r+3=2m-1 for the reciprocal pencil are all below 2N. There is no hidden dependence on the former quadratic-size list.

The relevant dimension lower bound is the new dim U>=d+6, not the old 3d-2. No step of the fast-axis argument or its cost count requires the discarded bound. Only O(N) upper dimensions enter the loop counts.

## Paid cost and fields

Dense envelope preparation is O(N^3). Each of the two coprime-combination loops has O(N) basis directions, O(N) scalar attempts per direction, and O(N^2) polynomial-gcd work with O(N) inversions per attempt. Together they remain the dominant O(N^4)/O(N^3)-inversion stage. The reciprocal pencil and final 2N scalar tests each cost O(N^3) arithmetic and O(N^2) inversions. All polynomial operands remain degree O(N), and storage is O(N^2).

The finite field still satisfies Q>=N+1 and uses the same separately paid quadratic coefficient extension, with O(Q^3) preparation. Positive-characteristic infinite fields still require the effective distinct-element interface. No field-construction, representation, scalar-list write, or coefficient output cost is made free.

The accepted first-order bank ledger `abc2f7bedcd39c630069a3f2764bf81972690ca51c5fd086a1a151963bdb72bf` is otherwise unchanged: genuine splitting field, actual roots, amplitudes, weights, original branch inverses, all outputs and extension-coordinate costs remain charged. The literal warm application and accepted 5N/3+O(1) count are unchanged. The improvement is solely the guaranteed coefficient-selection bound over the whole improved parameter range.

## Independent controls and source bindings

Fresh composition controls reuse only this reviewer's accepted exact axis/arithmetic implementation and this reviewer's independently constructed new-range original-U pencil data. They do not execute or import author or historical scientific programs. All eight author manifest members and the selected source-pin records were hash-checked.

The controls compare the literal original dense X, the affine matrix M, and the complete fast gcd test at five scalars, including zero and the endpoint of the 2N-element list, in each of four fixtures strictly below the old gate: (N,d)=(29,5) over F233, (35,6) over F211, (51,8) over F256, and (63,10) over F4096. They check every original-U moment, actual guarded successful points, exact root orders, and the 64-element subfield containing q in the final quadratic-field fixture. A separate integer grid checks all displayed dimension and scalar-list margins. Normal and optimized outputs are byte-identical; detailed counts and fixture decisions are in CONTROL.json.

These are corroborating exact controls, not a substitute for the uniform domain audit. No roots or physical bank arrays were constructed, and no external state was modified by this review.
