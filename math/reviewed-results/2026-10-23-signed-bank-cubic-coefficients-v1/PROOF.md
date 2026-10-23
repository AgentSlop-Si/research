# Candidate: reverse gcd descent in the improved support range

23 October 2026. Separate domain-composition candidate, pending independent review. The original reverse-descent packet is not altered. Its stated N>=8d-10 theorem is not retrospectively relabelled.

## Exact statement

Let N be odd, d>=4, N>=6d-2, m=N-d. Retain the exact original U, a supplied coefficient field containing a certified primitive Nth root q, characteristic not dividing N, and a represented list of 2N distinct coefficient-field scalars. Subject to acceptance of the source-bound reverse-descent selection lemma, the complete deterministic coefficient stage constructs an actual monic degree-m g in U with g(0) nonzero, ordinary squarefreeness and full ORIGINAL axis rank using O(N^3) additions/multiplications, O(N^2) inversions and O(N^2) live field elements.

This is a composition of a general polynomial selection lemma with the already separately accepted N>=6d-2 generator. It does not establish a further bank-count bound, expected-randomized improvement, full compiler/FFT speedup, or historical novelty.

## Complete source-interface substitution

The accepted improved-range pencil review supplies exactly V0={g/[t(t-1)]:g in U,g(0)=0}, r=m-2, and V1={g/(t-1):g in U}, n=m-1, with their gcd-one and independent endpoint properties. It explicitly audits that these properties follow from the original first-order support theorem at N>=6d-2, not from the discarded old dimension lower bound 3d-2. The retained lower bound is dim U>=d+6; all algorithmic storage/cost estimates use only the upper dimension O(N).

For the first combination, the accepted endpoint solve returns f0 in V0 with f0(0)=coefficient_r(f0)=1. The functional phi(f)=coefficient_r(f)-f(0) is nonzero on V0 by the same independent endpoints. Apply the source reverse-descent lemma to a=f0 and W=V0 with this phi. All its hypotheses are exact: a is nonzero monic degree r, gcd(a,W)=1 because gcd(V0)=1, basis degrees <=r, and phi is a coefficient functional. The output f1 is a scalar combination in V0, with gcd(f0,f1)=1 and phi(f1)!=0, exactly the unchanged first-pencil contract.

The accepted reciprocal pencil then returns a monic f with f(0)!=0 and gcd(f,rev_r f)=1. Set h0=t f and W={h in V1:coefficient_n(h)=0}. The accepted decomposition V1=k h0+W and gcd(V1)=1 give gcd(h0,W)=1, including multiplicities. Apply the same reverse-descent lemma to a=h0 and this W without an extra functional. Its output h1 lies in the original zero-leading slice and has gcd(h0,h1)=1, in particular h1(0)!=0. No polynomial multiples or changes of coefficient space enter either substitution.

The reverse-descent lemma depends on a scalar span, polynomial degrees, gcd one and the represented scalar list. It has no N,d or old support-threshold hypothesis, no squarefree/perfect-field assumption, and uses no numerical bank inequality. Both instances have s,L,v=O(N). Their lists require r+2=m and n+2=m+1 respectively; both are <=2N. The nonzero-scalar filtering and one endpoint-functional repair are already charged by the lemma.

## All remaining range and scalar guards

Neither reciprocal pencil is changed. The accepted improved-range fast-axis theorem supplies the original relation criterion including reciprocal-gcd cases, its affine (N-1)-by-2d matrix and nonzero 2d minor, squarefreeness, and degree <=2N-1 total final guard. The witness inequality is N-2d-1>=4d-3>0. The first reciprocal pencil needs 2r+3=2m-1<2N scalar values, and the final pencil needs 2N. No extra field-size or hidden list assumption is introduced.

The coefficient-field construction remains separately paid. In finite fields Q>=N+1 and the same represented quadratic coefficient field supplies enough values; its O(Q^3) base-field preparation is NOT absorbed into the coefficient-only bound. Infinite positive-characteristic fields still require an effective supplied list. Bit representation, counting/list setup and output coordinates remain charged at their existing interfaces.

## Complete ledger and limits

Original envelope/nullspace/endpoint preparation costs O(N^3) arithmetic and O(N^2) storage. Each reverse-descent application costs O((s+v)L^2)=O(N^3) arithmetic and O((s+v)L)=O(N^2) inversions, including scans, all failed trials, the optional functional repair, coefficient construction and output; chain storage is O(sL+v^2+L)=O(N^2). The first reciprocal pencil and 2N final guarded tests each remain O(N^3) arithmetic and O(N^2) inversions. Summing finitely many stages gives the stated deterministic totals.

The genuine splitting field, actual distinct nonzero roots, amplitudes, Vandermonde solves, raw bank weights, branch inverses, physical outputs, warm schedule and extension-coordinate expansion are unchanged. The possible m!-degree splitting overfield is not reduced. The result matches rather than improves the existing expected cubic Las Vegas coefficient bound. No transfer to the newly proposed N>=6d-5 bank threshold is made.

This packet is a symbolic dependency composition, not a new program or independently run scientific control. No historical or author scientific code was executed. Independent review must separately accept the generic reverse-descent lemma and verify this exact interface substitution before publication.
