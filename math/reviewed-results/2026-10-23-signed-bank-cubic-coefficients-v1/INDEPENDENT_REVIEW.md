# Independent acceptance: cubic coefficient generator, improved range

23 October 2026 UTC. ACCEPT this separate symbolic domain composition. Author ADDENDUM.md SHA-256 `05721d475490cb5ea651454cc05cfa722bd20385fe28b27f6d9bc85f17c66964`; author manifest `ae03754d6275bdf3d860933bc32f45839aa19257b00dba779bb33d89bffaaac6`. No earlier packet is edited or retrospectively relabelled.

## Exact result

For odd N, d>=4 and N>=6d-2, with the supplied original coefficient-field/primitive-root interface and 2N distinct represented scalars, the complete deterministic coefficient stage constructs a monic degree-m polynomial g in the SAME original U, m=N-d, with nonzero constant, ordinary squarefreeness and full original axis rank. Cost: O(N^3) additions/multiplications, O(N^2) inversions, O(N^2) live field elements. This is not a bank-count improvement, an expected Las Vegas improvement, an efficient splitting/root algorithm, an end-to-end polynomial-time compiler, or an FFT/novelty claim. No N>=6d-5 transfer is accepted.

## Independent interface audit

The generic reverse-gcd lemma is now independently accepted in `signed_bank_reverse_gcd_independent_20261023`, manifest `da1d3bedd4afaf198c468f08c98ee280baf3c966bf05fbf597a6f07f172861f1`, review `00de7c45788a201c27e59af5166d697f2e8cc8b13de7610d8dd491537c85eaf2`. Its polynomial-space statement has no N,d threshold. Its original generator application remains separately bounded by N>=8d-10.

The already accepted new-range pencil and fast-axis compositions provide, at N>=6d-2, the exact V0=U0/[t(t-1)] and V1=U/(t-1), their gcd-one properties, endpoint independence, both pencil guards and full original-axis criterion. Their pinned reviews are respectively `a1b08c5d1cd99340b4f632e434bfe0110e6d1c4ece186a1b97257d9c6edf173f` and `aa2ee7f3300c290a05f969a836d1d94708d67e6394712df4273a1b4d34792514`.

First substitution: take a=f0 of degree r=m-2 with both endpoints one, W=V0, and phi(f)=coefficient_r(f)-f(0). Gcd(V0)=1 implies gcd(a,W)=1. Endpoint independence implies phi is nonzero. The generic lemma returns f1 in the SAME scalar span, coprime to f0, with nonzero phi. The reciprocal-pencil proof is unchanged.

Second substitution: after choosing monic reciprocal-coprime f, set h0=tf of degree n=m-1 and W=ker(coefficient_n) inside V1. Since V1=k h0+W, gcd(V1)=1 implies gcd(h0,W)=1, with multiplicities. Apply the generic lemma without a functional, taking degree bound L=n even though basis degrees are smaller. It returns the original required h1, with h1(0)!=0. Neither substitution invents a new coefficient space or uses polynomial multipliers in place of scalar combinations.

The generic lemma requires r+2=m scalars in the first instance and n+2=m+1 in the second. Both fit the supplied 2N list. The first reciprocal pencil uses 2r+3=2m-1<2N, and the unchanged complete final guard has degree at most 2d+1+(2m-2)=2N-1. Its affine matrix has N-1 rows and 2d columns, with witness margin N-2d-1>=4d-3>0; the reciprocal residue margin is N-2d>=4d-2. Thus every old-range consumer is checked at the new threshold, not transferred by terminology alone. The retained dimension lower bound is dim U>=d+6, while costs only require O(N) upper dimensions.

Both new combinations cost O(N^3) arithmetic and O(N^2) inversions because s,v,L=O(N). Dense original-space preparation, the reciprocal pencil and all final guarded scalar tests fit the same totals. The reverse chain and original bases use O(N^2) storage. Every failed trial, scalar filtering, endpoint repair and coefficient read/write is charged by the source lemma.

The separately paid finite quadratic coefficient-field construction, scalar representation and list creation remain explicit. Infinite positive-characteristic fields still need an effective list interface. Genuine splitting, actual distinct nonzero roots, amplitudes, weights, branch inverses, extension-coordinate expansion, factorial-degree overfield recipe, and literal warm application are unchanged. In particular, coefficient-only cubic work is not a bound for those additional stages.

## Fresh composition controls and binding

All author members and the four selected source bindings were checked. This review also binds the newly accepted reverse lemma review/verdict. The controls adapt only this reviewer's own accepted reverse-selection and exact field/original-axis code; no author or historical scientific code was executed.

Four fixtures are strictly outside the old gate: (N,d)=(29,5) over F233, (35,6) over F211, (51,8) over GF256, and (63,10) over GF4096. They rebuild the exact original U and both pencils, check all original moment equations, monicity, nonzero constant and squarefreeness, and compare with literal dense original-axis ranks N. The selected full coefficient vectors are retained. An integer parameter grid checks all displayed dimensions, list margins and final guard degrees. Normal and optimized runs are byte-identical: 16,839 checks. These new fixtures have no failed scalar trial; multiplicity and worst-case failed-trial coverage belongs to the separately bound generic-lemma review, not these fixtures.

These are corroborating controls, not a replacement for the uniform interface proof. No splitting extension, actual roots or physical bank arrays were instantiated. The author composition needs no mathematical repair within the stated scope.
