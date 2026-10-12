# Q11 exceptional block coloring independent review

12 October 2026 UTC. Verdict: **ACCEPT within the bounded scope below.**

The candidate gives a source-legal, fully paid **20q-7** additive Green upper for the frozen positive target, q=483^m, m>=1, N=5q^2, s=5q. This is eight branches fewer than the accepted 20q+1 upper. Its branches satisfy the same narrow Model R used by the separately accepted 20q-12 lower, so the fully paid restricted minimum lies in **[20q-12,20q-7]**, a five-branch gap. Exact optimality is not established.

The improvement has an important preparation tradeoff: O(N) field coefficient work is accompanied by **O(s^3) integer-word coloring work** and O(s^2) integer storage. The older construction's linear total compressed preparation claim does not transfer. Paid direct evaluation remains Theta(Nq), with O(N) compressed field and integer storage; expanded descriptors require Theta(Nq) writes/storage. The ordinary two-DFT O(N log N) evaluator remains asymptotically faster. Broader Q11 remains OPEN; no all-N, unrestricted-cycle lower, FFT improvement, stability, bit-speed, practical transform benchmark, or novelty claim is accepted.

## Sealed evidence and provenance

The reviewed candidate is Q11_Eight_Branch_Coloring_Improvement_CANDIDATE_2026-10-12.zip, 6,155,005 bytes, SHA-256 **5d0ecdfba10f682ac061415dc2f1ae89987a759106e6791629db8defb1abbf43**. Its 23 members, 22 manifest items, both accepted source pins, two nested review equalities, and all eight finite certificates were independently checked. The sealed report hash is d4721728e70de801b05446b92e979d1ef54b52e0da8aa31a45e9dcdca853389c.

The accepted upper source is pinned by 604a419f89bd0cb79e53448d39a37798bbef05e01bccc3d3421c98a2beec6a32. The accepted restricted lower source is pinned by 7bfdc4108aaccfb8ebf12bfa6812b632a82b07565fe73304fe2da7b26a351a74. Both original archives were independently rehashed and left unchanged.

The reviewer wrote check_independent.py, check_endpoint_formulas.py and check_bindings.py from scratch. No candidate Python checker or historical program was imported or executed. The newly authored C++ coloring source was read in full, compiled afresh, and executed at q=483. The final sealed source hash cb736ee16fdb694d5149dcbd4b0086eafe67be9760b8dc1a114498ffd0419be7 was rebuilt separately after its finite-input guard was tightened. Its complete certificate reproduced byte for byte. All external state remained unchanged.

## Target and exact exceptional factors

The inherited field is L=Q(omega), for a supplied primitive complex Nth root. With h=(N+1)/2, G=q(1+2eta^2+2eta^3), eta=omega^(q^4), c=NG and rho=(1+c)^(-1), the accepted identity is

B_ij = rho omega^(ij) - rho G omega^(-h(i+j)^2)
       + rho c omega^(-h i^2) delta_ij.

The guards G^2=N and rho=(1-c)/(1-125q^6) remain intact. Both kernels are symmetric. Partition S_a={a+su:0<=u<q}. Since s^2=5N, their restrictions have factors

u0(i)=rho omega^(ib),                 v0(j)=omega^(a(j-b)),
u1(i)=-rho G omega^(-h i^2-ib),      v1(j)=omega^(-h j^2-a(j-b)).

For a!=b, put {a,b} in E when q divides a+2b or b+2a. In the first case u1=gamma u0, gamma=-G omega^(-h a^2-2ab); thus the whole block factors as u0(v0+gamma v1)^T. Otherwise the second case gives v1=delta v0, delta=omega^(-h b^2), and the block factors as (u0+delta u1)v0^T. Direct expansion verifies the signs and scalars. When both congruences hold, the first recipe is valid. No division beyond the inherited scalar rho is added. Transposing these factors produces the correct reverse block because B is symmetric.

The rank-one collapse is exact, not a low-rank approximation. The upper needs only rank at most one. Characteristic-zero nonvanishing and exact rank classification used for the lower remain the independently accepted lower theorem; finite-field images here do not substitute for that theorem.

## Coloring algorithm and uniform cost

At each label a with 3a=0 modulo q, both exceptional neighbor residues coincide with a, leaving its four other lifts. There are fifteen such labels. Every other label has two distinct exceptional residues, neither its own, and therefore ten exceptional neighbors. Consequently E has 25q-45 edges, while H=K_s-E has maximum degree s-5 and minimum degree s-11.

The inspected fan algorithm constructs a proper coloring of H in k=s-4 colors. Its validity does not depend on an oracle or on the finite certificate. For an uncolored xy it maintains a fan rooted at x, starting with y, such that each later fan-edge color is absent at the preceding fan vertex. Taking a free color at the last vertex either reaches a free color at x or reaches a repeated fan neighbor. In the first case rotation finishes.

In the repeated-neighbor case, denote the repeated edge color by d, its position by j, and a free color at x by c. The c,d component beginning at x is a simple path, since c is absent at x. Swapping it makes d free at x. The predecessor of fan position j had d absent; hence if it lies on the path, it must be the other endpoint. When it is that endpoint, the changed fan edge now has c and the predecessor now misses c, preserving the entire fan. The last fan vertex still misses d because it is a different endpoint candidate and is outside the path. If the predecessor is outside the path, its d remains free, and the fan prefix ending there is unchanged in all relevant colors. Rotating the appropriate whole fan or prefix and inserting d extends the proper coloring by one edge.

Every vertex has a free color at every stage: its full degree is at most k-1. Edge/color lookup tables, linked free-color lists and a fan-position array provide constant-word-time updates. Fan, path and rotation lengths are O(s) per inserted edge, with O(s^2) edges, giving O(s^3) word work and O(s^2) words, including initialization and final verification. Address words have O(log N) bits because s^2=5N. The bundled fixed-width C++ control is explicitly restricted to odd q<=483; the all-m theorem is the scalable mathematical algorithm, not an assertion that this codec handles unbounded indices.

This is a classical fan recoloring application. Primary attribution was independently checked against Misra and Gries, “A constructive proof of Vizing's theorem,” Information Processing Letters 41 (1992), 131-133, https://doi.org/10.1016/0020-0190(92)90041-S, and the authors' manuscript https://www.cs.utexas.edu/~misra/psp.dir/vizing.pdf. No originality claim for the coloring method is made.

## Legal directed branches and same-class completion

Layer A uses both orientations of all s round-robin K_s matchings. On E it places the full collapsed block; elsewhere it places kernel 0. The unique singleton t in round t receives kernel 0's forward or reverse triangle. Layer B uses both orientations of the k color matchings of H, placing kernel 1 on their paired blocks. Each label chooses one color missing at that label. Only in that color is its singleton active for kernel 1. Proper coloring and this missing-color check prevent any class from being simultaneously paired and active as a singleton.

For each matching, concatenate paths S_a then S_b for its pairs, plus paths for every unmatched class, into one Hamiltonian structural cycle on the original N coordinates. All component boundary weights are zero; internal weights are one. Diagonal masks select one directed rank-one rectangle per paired component. Inactive singleton masks are zero. Reversing the entire cycle and its component paths, swapping the paired endpoint factors, and retaining the same singleton factors implements the reverse branch.

Each structural cycle is Hamiltonian; all holonomies are zero and all Green denominators equal one. The inverse is the finite weighted-walk sum. It is zero between distinct components and upper-triangular ones along each directed component. Thus the paired masks create exactly the desired rectangles without paired same-class leakage. Singleton masks create exactly the desired triangles. Endpoint permutations outside the prescribed diagonal Green term are absent.

Every off-class block is covered by its full collapsed block or its two kernels. Every class gets exactly one pair of opposite singleton triangles in each kernel, so the combined same-class block is complete. Each diagonal is duplicated once in each kernel. One fully counted branch, W=0 and diagonal endpoint

D_i = rho c omega^(-h i^2) - rho omega^(i^2)
      + rho G omega^(-4h i^2),

removes those duplicate diagonals and inserts the target's diagonal term. The total is 2s+2(s-4)+1=20q-7. This argument includes empty color classes and multiple active unmatched singletons. No omitted singleton, free diagonal, or incompatible orientation is hidden in the branch count.

Every branch is confined to a matching of the same fixed S_a classes. Per matched pair it has at most one nonzero off-class direction, with rank at most one. The calibration has no off-class entries. Therefore the entire construction belongs to the accepted lower's Model R. The five-branch fully paid comparison is justified. If an arbitrary block-diagonal correction were instead treated as genuinely free in the relaxed lower model, the uncalibrated 20q-8 branches would be a separate relaxed upper; that is not the fully paid source-legal claim.

## Field and routing ledger

Five length-N tables P,U,V,T,D cost 5N-1 field multiplications and 2N additions, apart from the separately charged O(log N) scalar setup/optional supplied-root checks. Precomputing the changed endpoint in each exceptional pair costs q|E| additional additions and O(q|E|)=O(N) storage. Ordinary endpoint factors remain table lookups. The exact field preparation is therefore

M_prep=5N-1,
A_prep=2N+q(25q-45).

The number of directed paired rectangles is R=50q^2-60q+90. There are 4s active singleton triangles. Either component uses 2q multiplies and 2q-1 additions with accumulation. Initializing with D*x costs N multiplies. Hence

M_app=N+2q(R+4s)=100q^3-75q^2+180q,
A_app=(2q-1)(R+4s)=(2q-1)(50q^2-40q+90).

At m=1 these are 11,250,448,965 multiplications and 11,237,637,300 additions in 9,653 paid branches. Field operation counts were instrumented on the small actual schedules. At m=1 these counts are symbolic, not a full-transform run. Lookup, coordinate movement, loop work and structural-cycle enumeration are O(Ns) word work per application. Cold coloring has its separately stated O(s^3) word charge; since s^3=25Nq, this does not change the end-to-end direct upper's asymptotic order. The field degree grows with N, so none of this implies a bit-model speed advantage.

## Independent executable checks and limits

The independent verifier reconstructs each small branch's Hamiltonian successor, cut weights and diagonal masks, then sums actual W-walk entries. Its rank-one factors are independently recovered from direct kernel block values, separately from the explicit candidate factor formulas. It also checks the generic inverse recurrence and a separately counted dot/scan application.

Checks passed:

- 430,150 complete assembled entries at q=1,1,3,3,7,11, with two different primitive roots at q=1 and q=3;
- 8,200 entries of both defining inverse products at N<=45;
- 124 vector applications, including all basis vectors at N=5 and N=45, zero, constant, deterministic dense and random inputs;
- 872,800 original-coordinate Green recurrence checks;
- complete proper-color, exception-support, degree, missing-color and round-robin coverage checks at q=1,3,7,9,11,21,69,483;
- all 2,914,905 unordered m=1 pairs, comprising 12,030 exceptions and 2,902,875 colored H edges, with 2,411 colors and 2,415 checked singleton slots;
- fresh final-source C++ regeneration of the m=1 certificate, SHA-256 0c401dca819d64abf263db86cd3466b4123b56c7bb6926a2df9bd2f4f0629e3e, byte-identical to the sealed certificate;
- independent explicit-factor checks on all small off-class blocks, and at m=1 all 5,810,490 proportional endpoint coordinates over all 12,030 exceptional pairs, 60,150 selected combined-block entries, all 1,166,445 diagonal calibrations and a full length-N Gauss sum at independently verified p=18,663,121, omega=65,536;
- negative controls rejecting duplicate incident colors, occupied singleton slots, colored exceptional edges, truncated certificates, omitted paid calibration, omitted kernel-1 singleton triangles, omitted exceptional kernel terms, and a removed actual zero cut.

Small q controls are outside the frozen family and do not prove the infinite theorem. The m=1 algebra check verifies the listed coefficients and scalar identities, not the million-coordinate transform. No full m=1 field application or dense target was executed. Uniform correctness and cost follow from the proofs above. The sibling seal and cold receipt bind a fresh extraction replay of these exact reviewer programs and the final reviewed colorer.

## Scope and remaining work

This bounded eight-branch improvement retains the restricted 20q-12 lower, broader Q11 OPEN, ordinary-order rank obstruction, all-Q(eta) impossibility, retired five-coordinate minimum-three obligation, negative-family/all-N boundaries, and unresolved priority. The old linear-preparation statement does not transfer to the new coloring schedule without its additional integer-word cost.

Public derivative note: tracking instructions are replaced by public scope wording; the proof, counted model and preparation tradeoff are unchanged. Original report SHA-256: `bc50470f3e77b1ba28dacead57fa12a130620403d9430c9d650bc58ec3f329d2`.
