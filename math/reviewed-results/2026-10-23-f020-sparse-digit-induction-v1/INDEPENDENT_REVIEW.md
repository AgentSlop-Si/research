# Independent review: arbitrary sparse even-middle digit guard

23 October 2026 UTC. **ACCEPT the exact arbitrary-length theorem below.** This is not all-digit squarefreeness, historical novelty clearance, an FFT claim or whole-owner closure.

## 1. Frozen scope and incremental coverage

Author packet: `f020_sparse_digit_induction_20261023_frozen_v1`.

- REPORT.md SHA-256 `bda2193ca3b5e02479f20a61e21d803c965cf70d98dbb7f93400791cc36a014b`.
- MANIFEST.json SHA-256 `f2cc6aaa02a80a0e32b195341acf79ad6fabe7aea1185d6406985219143450c9`.

Let p be any odd prime, t>=0 any finite integer, r>k_1>...>k_t>j>=2 with every consecutive exponent gap at least two, every middle digit c_a even with 2<=c_a<p, and terminal digit d odd with 1<=d<p. For s>r and every characteristic-zero primitive p^s phase q, set

    n=2p^r+sum_(a=1)^t c_a p^(k_a)+d p^j.

Then both original P_n and H_n are squarefree, and the original ordinary algebraic-square CD kernel is nonzero at every original P_n root. No associated polynomial is substituted for the actual immediate neighbor.

There is no fixed upper bound on t. The proof uses one invariant at each scale, not a finite list of separately checked degree slices. The old t=0 and t=1 theorems retain all prior credit. Incremental coverage is only t>=2 after subtracting every inherited high-order, fixed and successful residual certificate. The exact C_u high-order subtraction in the report is unchanged. No adjacent scales, j=1, odd middle digits, even terminal digit, other leading digit or non-prime-power order is accepted. F020/F023 remain open as whole owners. Minimum new degree 14751 is consistent with the stated domain.

## 2. Source comparison and legality

I read the full new report and compared its uses of the accepted two-middle proof/review and enlarged deep-cap proof. The terminal-prefix cap in that accepted proof was explicitly established for arbitrary upper quotient, not only its original two-middle degree. The neighbor-derivative argument likewise depends only on its general block inequality. Those are legitimate reusable inputs. In contrast, the new arbitrary-suffix carry argument and repeated-scale gluing are not inherited automatically; they are verified below.

Source copies and their hashes are bound in BINDINGS.json. This is a selected mathematical-source comparison, not a recursive archive audit. No author or historical scientific program was executed or imported.

The geometric gap bound gives n<[2+1/(p+1)]p^r<p^(r+1)<=p^s. Thus all recurrence edges, finite-factorial factors and finite-connection denominators used in the proof are nonzero. Higher-scale disks are strictly inside their matching lower-scale disks. Both q orientations use the same X disks. Ordinary coordinate derivatives are units near X=0; the report explicitly pays each off-root prefactor. The proof does not assume that total weights lie below v(p).

## 3. The genuinely length-independent suffix invariant

For a remaining suffix m=sum even c_a p^(k_a)+d p^j, let L=p^j and u=(m-1)/2. Its digits are obtained without carry: below j they are (p-1)/2; at j they are (d-1)/2, strictly smaller than (p-1)/2; above j they are c_a/2 or zero, never exceeding (p-1)/2. Therefore

    W(m-1)=2W(u), W(m)=2W(u)+L,
    u mod p^b < (p^b-1)/2 for every b>j.

The last strict inequality is preserved no matter how many higher even digits are added. This is the needed new fact; one may not replace the entire lower suffix residue by the old one-digit residue.

For odd connection index ell=2x+1, if ord_p(ell)=b>j, then x mod p^a=(p^a-1)/2 exceeds u mod p^a at every j<a<=b. Adding x and u-x must carry across each of these levels. The W defect is at least p^b-L. For b<=j, superadditivity and V(ell)<=L suffice. Both cases yield

    W(u-x)+W(x)+V(ell)<=W(u)+L.

For even ell=2x, W(u-x)+W(x-1)+V(ell)=W(u-x)+W(x)<=W(u). Thus on a full upper disk, where the accepted strict deep cap applies to every index below pM, only odd connection indices can contribute at weight G=W(u). Their even-polynomial factors have constant initials. The entire constant sum is nonzero by the exact value g_m^0(0)=(-1)^u Q_u. The original g derivative bound is G-(p-1), not a formal derivative of a residual. This proves the deep g invariant without a fixed bound on the number of digits.

The deep ordinary f derivative has its unique minimum at h=0, delta=p^2. The bottom two half-digits allow the required carry-free subtraction, so its constant initial is nonzero at G+L-p. The P_m prefactor is higher, hence the statement holds off roots.

## 4. Full lower disks and actual shifts

At the largest remaining suffix scale M=p^k, every index is below pM. Half-W gives R_k(h)<=W(h)/2, with equality exactly at h=bM. Combined with superadditivity and the unique maximum of V(delta)-W(delta-1)/2, every ordinary H_m' score is at most G+p.

If m=cM+a0 begins with an even digit, the complete equality set is delta=p^2, h=bM for b=0,2,...,c, and a=(c-b)M/2+(a0-p^2)/2. The same balanced half-digits show that all these indices attain equality even when a0 has many digits. The block units depend only on c,b and the quotient blocks, while the lower suffix is retained in its exact scalar. Their full sum is M_c(Z). For the terminal suffix dL, the corresponding index is instead d-1, giving M_(d-1)(Z). Both indices are even and less than p, so the constant is nonzero. Thus the ordinary derivative is exact G+L-p on every strict lower interior, not on the entire boundary.

The off-root correction has weight at least j v(p)+G+L/2>G+L-p. Full-lower g is only bounded by G+L-M, with its ordinary Gauss derivative loss rho_k. A unit statement there is neither proved nor used.

For a prefix U, its terminal even digit makes V(U)=D, while every tail index has V<=M<D. The actual finite connections therefore give eta-1 of value at least D-M, f-correction weights at least G+L/2+D-M on lower disks and G+L+D-M on upper disks, and g-correction weights at least G+L+D-2M. The stated derivative losses are respectively rho_k or p. Since D>=p^2 M and L<=M, these errors are strictly above every retained derivative or unit initial. The conclusions apply to the genuine shifted continuants, not unshifted proxies. No constant deteriorates with the number of digits.

## 5. Arbitrary even prefixes require covers, not simplicity

For every prefix U_i, its terminal digit is even and nonzero. The accepted arbitrary-prefix terminal cap gives its complete uniform disk cover, core bound J, ordinary derivative bound J+D/2-p, and neighbor bound E=J-D/2. Its boundary residuals are M_e and M_(e-1), multiplied by a common nonzero Y factor there. They are coprime because e<p.

The report correctly repeats the general original-neighbor derivative proof. An H_(U_i-1)' term reduces to F(delta+1+2a)-W(a)-V(delta)>=D/2. The cases delta+1=lD+v use only the general block inequality: v=0 and v=1 are handled by the block contributions; 2<=v<D uses proper-block strictness and half-integrality. The only negative half-unit remainders are v-1=1 or p. At a multiple of D those exceptions force v+2w=2D and leave D+W(v/2-1)-V(v-1)>=D-p>=D/2. Hence B_i'>=E for every upper prefix, not merely the old two-middle core. The ordinary off-root H/P terms are bounded explicitly.

The outside ratio also needs no prefix simplicity. Its full monic cover, including multiplicities, gives equality between core and Newton-product valuations outside all disks. Nearest-center maximality handles tied distances; capped interval splitting gives the required ratio. The global digit bound W(x)/2-R(x)<=D/2-rho yields B/C>=-D/2+rho-tau. On the local radius-rho disk the core factors are analytic units, so differentiation is coefficientwise and gives C'/C>=-tau and B'/C>=-D/2-tau. The near-X=0 restriction and all field guards are retained. No unproved even-prefix squarefreeness theorem is an induction hypothesis.

## 6. Every boundary, every adjacent annulus, and the deepest interior

At a boundary of any core scale, the deep tail bounds apply. If M_e vanishes, the original core neighbor and g are nonzero with exact values. The root equation gives delta+gamma=D/2, delta>=L. The exact f'C term has gaps 2delta-L, delta-L+1 and delta-L+p over the other three derivative terms. All are positive, including coincident residual classes. If M_e is nonzero, C is exact J and the direct gaps are D/2, D/2-L+1 and D/2-L+p. This branch includes f=B=0 without division by them.

At the deepest strict r interiors the leading-two core has constant nonzero residual, so the same direct comparison applies. No deeper core or extra root count is needed.

In each adjacent-scale annulus, a root is in a strict lower interior but outside the closed upper cover. Hence sigma<tau<rho. The full-lower weak g bound and exact f' value, together with the outside-core ratio, give the three gaps

    D/2-M+p+rho-2tau,
    D/2-M+p+rho-tau-sigma,
    D/2-M+p-tau.

They are positive because M+rho<D/2, uniformly for p>=3 and the gap at least two. Only C is divided out; g need not be a unit at arbitrary points.

The outermost terminal-j cap first counts all n roots with multiplicity and settles its (d-1)L boundary roots. Every remaining root lies in exactly one adjacent annulus, one core-scale boundary, or the deepest strict-r interior. Strict nesting makes these classes disjoint and exhaustive for every finite t. Adding a digit inserts one boundary and one annulus governed by the same invariant. This is a complete arbitrary-length proof, not an extrapolation of control data or an assertion that common residual zeros are characteristic-zero collisions.

Consecutive original continuants are coprime because every recurrence edge is nonzero. The ordinary CD identity proves the claimed algebraic-square kernel statement. Roots reduce to X=0 and are not +/-2; unit coordinate changes transfer multiplicity to H_n. Algebraic p-adic embedding/Galois conjugacy supplies every characteristic-zero primitive phase.

## 7. Fresh independent controls and their limits

The independently written `fresh_controls.py` passes **1,678,587** explicit checks, identically under normal Python and python -O. It imports no author/historical scientific code. It includes genuinely multi-digit suffixes m=1629 and 14751 at p=3 and m=32575 at p=5; exact half-digit deficits and all g connection endpoints; all equality terms and factorial units for multi-digit lower suffixes; new minimal full degree 14751 and its even-prefix original neighbor bounds; and growing-length margin/legality checks through thirty even middle digits.

Derivative maximizers are enumerated by fixing h and ord_p(delta). For each parity, the least positive delta of that order dominates all larger choices because W((m-h-delta)/2) strictly decreases as delta grows. Thus this is an exact maximizer enumeration, not random sampling. One complete unpruned enumeration independently checks that reduction. No finite parameter bound is substituted for the proof.

The actual out-of-scope negative m=819, p=3, ell=243 is independently reproduced: its g score 1824 exceeds G+L=1662 when two middle digits are odd. This rejects extending the carry lemma beyond its invariant, not squarefreeness of those out-of-scope polynomials. The accepted two-middle full-k g-unit counterexample remains inherited warning evidence, not relabeled fresh computation.

The author control count remains author evidence only. No cyclotomic root census, general-degree algorithm or bit-cost claim is inferred. Naive coefficient generation and root-field costs are not improved.

## 8. Verdict

Accept the bound arbitrary-length sparse even-middle theorem and its exact parity/gap/phase scope. No author repair was required after the full proof arrived. All prior source pins and credit exclusions survive. Whole F020/F023, historical priority and runtime claims remain unchanged. This mathematical verdict does not release any parent-level F020 external-operation hold; the reviewer performed no external writes.
