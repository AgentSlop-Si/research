# Common fiber splitting and its endpoint-mask gate

## Scope

This addendum concerns the deterministic nested four-sheet lift, not independently min-spliced orders at each size and not the certified N16 coefficient seed. Let the small grid have dimensions a,b, with a=b or a=2b, and assume a,b are even and b>=2. Write N=ab. The large grid has dimensions 2a,2b and size 4N. Sheets are literal high bits e=2 epsilon_x+epsilon_y in {0,1,2,3}.

The result strengthens the earlier common four-state Green representation: every lifted route has the same fixed Walsh 1+1+2 splitting. General physical endpoint masks mix these sectors. The only simple larger mask subalgebra that preserves a coarser 2+2 splitting cannot realize Fourier with the stated pulled-back bank, because it preserves a forbidden symmetry.

## 1. Identity monodromy before the merge

For any one of the eight labels let T_S be its unspliced small MGG cover and let P_S be the chosen small Hamiltonian cycle. Set eta=P_S T_S^(-1). The premerge large route is

    P0 = eta_hat T_L,

where eta_hat changes low coordinates according to eta and leaves both high sheet bits unchanged. It covers P_S. This calculation does not require any special ordering of P_S: its base traversal visits every small vertex once.

For a horizontal label (c,sign), a step on sheet bits is

    epsilon_y' = epsilon_y,
    epsilon_x' = epsilon_x + h(x,y) + (2b/a) epsilon_y mod 2,
    h(x,y) = floor((x+sign(2y+c))/a) mod 2.

The sign on the coefficient of epsilon_y is immaterial modulo 2. For a=b the coefficient vanishes; for a=2b it equals 1. The exact carry sum over one full base traversal is

    sum_(x,y) floor((x+sign(2y+c))/a)
      = sign b(b-1+c).

This is even because b is even. Also N is even, so the accumulated shear coefficient N(2b/a) vanishes modulo 2. The horizontal sheet monodromy of P0 is the identity.

For a vertical label,

    epsilon_x' = epsilon_x,
    epsilon_y' = epsilon_y + v(x,y) mod 2,
    v(x,y) = floor((y+sign(2x+c))/b) mod 2.

The possible epsilon_x coefficient 2a/b is even. The exact carry sum is

    sum_(x,y) floor((y+sign(2x+c))/b)
      = sign a(a-1+c),

again even. Thus vertical monodromy is also the identity.

The carry-sum identity uses the elementary formula sum_(x=0)^(a-1) floor((x+s)/a)=s for every integer s, including negative s.

Consequently P0 has exactly four cycles, each of length N, and each contains exactly one of the four tails over base vertex 0. Their increasing numeric order is e=0,1,2,3. The deterministic successor rotation used by the hierarchy therefore replaces the edge map phi_0 by phi_0 r, where

    r = (0 1 2 3),  or r(e)=e+1 mod 4.

All other sheet edge maps are unchanged. Since the premerge based monodromy is identity, the final based monodromy at 0 is exactly r for every label. The resulting route is Hamiltonian.

### Smallest bases are separate

The even-dimension assumptions are essential. With b=1,c=1, the horizontal carry sum b(b-1+c)=1 is odd. For example, on the formal a=2,b=1 horizontal c=1 lift, the premerge sheet monodromy is the high-x swap, not identity, and there are two cycles of length 2N rather than four N-cycles. The chosen hierarchy was initialized at b>=2 (and its expansion-certified bases are much larger). No claim here uses b=1 or extends the identity-monodromy statement to that case.

## 2. A common dihedral group and fixed Walsh splitting

Let D8 denote the order-eight subgroup of S4 preserving the unordered partition

    {{0,2},{1,3}}.

This is the dihedral group of a square. Both unmerged horizontal and vertical sheet maps preserve epsilon_y up to adding a constant, so they lie in D8. The merge rotation r also lies in D8. Hence every edge transport of every lifted label lies in this same D8, in the original literal high-bit sheet coordinates. This is an all-size containment theorem under section 1's hypotheses.

Use the fixed Walsh functions chi_c(e)=(-1)^(c dot e), where c,e are two-bit integers and bit 0 is the y bit. D8 fixes the trivial character chi_0, takes chi_1 to plus or minus itself, and permutes chi_2,chi_3 with signs. Therefore all eight route permutations, and all their Green resolvents, share the same channel splitting

    span(chi_0) + span(chi_1) + span(chi_2,chi_3).

No order-dependent fiber gauge is needed. The two one-dimensional channels are signed copies of the corresponding small base cycle. Their full-lap signs are +1 and -1. The remaining two-state sector is a signed 2N-cycle with full sign -1. Thus each Green still uses signed scans of lengths N,N,2N, with the same denominator product

    (1-tau^N)(1+tau^N)(1+tau^(2N)) = 1-tau^(4N).

This common splitting sharpens the basis description, not the operation count. It is also distinct from four scalar channels: the two-dimensional block cannot in general be simultaneously split across all orders.

## 3. Exact criterion for a common four-scalar gauge

For any connected base labeled graph with four-sheet permutation transports, choose paths from base 0 to every vertex, with transports T_v. Each edge v->w then gives the root holonomy

    g_edge = T_w^(-1) phi_edge T_v.

Generate the finite subgroup H of S4 from these elements. There exists a base-position-dependent complex fiber basis that makes every edge transport diagonal if and only if H is abelian.

Necessity: every closed-walk transport becomes diagonal in the basis at the root, and diagonal matrices commute. Sufficiency: commuting finite permutation matrices are commuting unitaries, so an orthonormal common eigenbasis exists; transport that root basis using T_v. Every remaining edge is diagonal in the resulting local bases. This criterion allows arbitrary complex invertible bases, not only sheet permutations or Walsh transforms.

In the present hierarchy H is contained in D8 and contains the four-cycle r, since the full first route is a based closed walk. Therefore H is either the cyclic group <r> of order four or D8 itself. An exact necessary and sufficient test for H=D8 is that at least one gauged edge holonomy lies outside <r>. Equivalently, a pair of generators fails to commute. We do not claim that this extra condition has been proved for every possible small-route choice or every hierarchy level.

The fresh controls find H=D8 in all 17 supplied instances: eight separately initialized one-level lifts at N=4,...,512, and three nested levels from each of seeds N=4,8,16. They record all eight group elements and explicit noncommuting edge-holonomy pairs. For example, at N=16 one pair is

    g=(1,2,3,0), h=(1,0,3,2),
    gh=(2,1,0,3), hg=(0,3,2,1).

Thus these finite instances have no common four-scalar gauge. A positive cyclic-group control confirms the commuting case. Group closure takes constant-size work per generator (at most 24 permutations), so obtaining all generators and testing the criterion costs O(N) for eight fixed labels.

## 4. Endpoint masks do not preserve the fine splitting

For a physical mask a(e) in one fiber, its Walsh representation is XOR convolution:

    M_a[c,d] = a_hat[c xor d],
    a_hat[c] = (1/4) sum_e a(e) chi_c(e).

A mask preserves the full 1+1+2 splitting term by term if and only if it is fiber-constant. Indeed, preservation of the trivial character line already requires diag(a)1 to be proportional to 1, so all four physical values coincide. Conversely, a fiber-constant mask is scalar on the fiber and preserves every sector.

The coarser partition {chi_0,chi_1} + {chi_2,chi_3} is preserved exactly when a_hat[2]=a_hat[3]=0. Equivalently,

    a(e) = alpha + beta chi_1(e),
    a(0)=a(2), a(1)=a(3).

Such a mask can be nonsingular, for example (1,2,1,2), but it generally exchanges the two one-dimensional sectors. A generic nonsingular physical mask, such as (1,2,3,4), mixes the coarser sectors as well. The usual physical nonzero guards are alpha+beta != 0 and alpha-beta != 0 for the two-value family; transformed coefficient nonvanishing is not the correct guard.

These statements describe the mask algebra and termwise closure. Special cancellations in a sum of terms are not excluded merely by a single mask's mixing.

## 5. The coarse closed mask family cannot give Fourier with the pulled-back bank

Let X swap the high-x bit while leaving the low coordinates and high-y bit unchanged. On global length-4N indices it is the shift by 2N. It is the central element r^2=(0 2)(1 3) of D8. Therefore every nested route permutation, and every scalar-pole Green resolvent, commutes with X.

Masks of the two-value form alpha+beta chi_1 are independent of the high-x bit, so they also commute with X. Hence any sum of these masked Green terms commutes with X.

The stated large bank has length-2b blocks with active labels pulled back from the small x coordinate: a block x is active exactly when x+a is active. Its active F_(2b) blocks and inactive identity blocks are identical on those pairs. It therefore commutes with X as well. Every product of these restricted layers and this bank consequently commutes with X.

The target F_(4N) does not commute with X. Commutation with this involution would imply simultaneous-shift invariance C[i+2N,j+2N]=C[i,j]. But

    F_(4N)[0,1]=1,
    F_(4N)[2N,2N+1]=-1.

Thus the two-value mask subalgebra cannot realize the Fourier matrix in this lifted geometry. Genuine high-x-dependent coefficients, a symmetry-breaking bank pattern, or another explicitly charged symmetry-breaking factor are necessary. This is an exact commutation obstruction, not an application-cost lower bound. It does not apply to the independently min-spliced N16 solution, whose routes were not assumed to be this nested family.

## 6. Controls and remaining obligation

`check_joint_holonomy.py` independently checks carry sums, exactly four premerge N-cycles, merge tails, literal based monodromy r, common D8 membership, group closure, noncommuting witnesses, and the mask-algebra conditions on all 16 binary masks. Its route helpers were authored in this research track; no uploaded source is executed.

The route containment and mask/symmetry theorems above are all-size under the explicit parity and bank hypotheses. Equality of the joint holonomy group with D8 is separately limited to the enumerated instances or the exact outside-C4 criterion. A future coefficient lift must break the high-x symmetry while retaining a paid operator representation and verifying every Fourier entry.
