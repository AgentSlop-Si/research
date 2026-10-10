# Independent review of four character Fourier and Green channels

## Result

The constructor's four-character Fourier identity, active-bank identity, signed-route holonomy, endpoint-mask formula, and route-specific four-channel Green decomposition are correct under the conventions below. The homogeneous phase gauge is stated here as an explicit intertwining identity to remove any conjugation-direction ambiguity.

The Fourier identity uses four independent length-N input-residue vectors and four ordinary F_N applications, shared across all output characters. It gives the usual recurrence T(4N)=4T(N)+O(N). The Green identity gives either three signed scans of lengths N, N, 2N in the common Walsh basis, or four length-N scalar Green scans in an order-specific cyclic-character basis. These are exact operator representations, not faster Fourier recurrences or solved coefficient equations.

No earlier seal is modified. The constructor is credited for the supplied derivation; the reviewer independently proves the identities and writes the checks packaged here. This is not a publication-priority claim. No uploaded program or constructor program was executed.

## Conventions and guards

Let b=2^r, a=b or 2b, and N=ab. Small vertices have label bx+y, with 0<=x<a and 0<=y<b. Large vertices have label 2bX+Y, with 0<=X<2a and 0<=Y<2b. The fiber over (x,y) consists of

    (X,Y)=(x+a epsilon_x, y+b epsilon_y), epsilon_x,epsilon_y in {0,1}.

Write chi_(u,v)(epsilon)=(-1)^(u epsilon_x+v epsilon_y). Let Q_(u,v) sum a large vector on each fiber with those character signs. Stacking the four Q matrices gives an invertible 4N-by-4N matrix W with W W^T=4I and W^(-1)=W^T/4. The character group is V4, not C4.

Fourier matrices are unnormalized with positive exponent. Choose a primitive 4Nth root omega, and put zeta=omega^4, so F_N[k,t]=zeta^(kt). The field must have characteristic not dividing 4N and contain the stated roots. For dyadic N this excludes characteristic two. The negative-exponent version holds by replacing all roots consistently by their inverses. Roots at successive sizes must agree, not be chosen independently with incompatible orientations.

The permutation convention is P e_j=e_(P(j)). For Green identities, P_small is a single N-cycle, P_large is a single 4N-cycle, and the coordinate quotient satisfies pi P_large=P_small pi. For a supplied scalar tau, require 1-tau^(4N) != 0. Scalar zero is allowed by the algebra. Endpoint-mask invertibility, where required by the model, means every physical endpoint value is nonzero.

All complexity counts are field operations and word routing, with roots and field representation available. They are not bit-complexity claims. Index storage uses O(N) words of O(log N) bits; extension-field construction or arithmetic must be charged in its own cost model.

## 1 Fourier channel identity

For row bx+y and column j, summing the four physical Fourier rows gives exactly

    (Q_(u,v) F_(4N))[bx+y,j]
      = omega^((2bx+y)j)
        (1+(-1)^(u+j)) (1+(-1)^v omega^(bj)).

Indeed, increasing X by a adds 2N to the physical row label, contributing (-1)^j. Increasing Y by b contributes omega^(bj). The character signs give the other two factors.

For s=0,1,2,3 define

    D_s[bx+y,bx+y] = omega^((2bx+y)s),
    c_s = omega^(bs),
    (R0 f)[bx+y] = f[(2bx+y) mod N],
    (R1 f)[bx+y] = f[(2bx+y+b) mod N].

The N-by-N block on columns j=4t+s is zero unless s mod 2=u. When the parity agrees it is

    (Q_(u,v) F_(4N))[:,4t+s]
      = 2 D_s (R0+(-1)^v c_s R1) F_N.

The proof is substitution: omega^(4(2bx+y)t)=zeta^((2bx+y)t), while omega^(b(4t+s))=c_s zeta^(bt); the latter factor shifts the selected Fourier row by b. R0 and R1 are selectors, potentially with repetitions. Treating them as permutations would be an error. The formula includes b=1 and N=1.

For arbitrary input x, compute f_s=F_N(x[4t+s]) for four distinct residue vectors. All four output character vectors reuse these same four transforms; each character has two parity-compatible contributions. Recover the full original output with W^T/4. No sixteen independent transforms are needed, and no sharing of the four arbitrary residue inputs has been proved that eliminates their transforms. This count describes this exact implementation, not a universal arithmetic lower bound on every conceivable algorithm.

Geometric recurrences generate all four D_s arrays and constants in O(N) arithmetic; selectors and Walsh mixing cost O(N). Thus the displayed implementation has ordinary radix-four work 4T(N)+O(N), with the standard O(N log N) recurrence solution. It establishes neither a smaller active recursive mass nor a coefficient family realizing such a recurrence.

Normalization matters. If Fourier matrices alone are replaced by unitary-normalized ones while Q remains the unnormalized character sum, the displayed factor 2 becomes 1 relative to unitary F_N. If W itself is normalized to W/2, its factors must be adjusted too. These scalar adjustments do not change the number of independent residue inputs or transform applications.

## 2 Active-bank identity and accounting

Let active small block labels be J subset {0,...,a-1}, and pull them back to J union (J+a) at the large level. At an active label x, the large bank has F_(2b) on each of the two x-fiber copies. At an inactive label both are identities.

Choose rho primitive of order 2b and use rho^2 for F_b. Define D_v=diag(rho^(v y)), v=0,1, and selectors

    S_(v,w)[t,z] = (-1)^(w floor((2t+v)/b))
                   1_(z=(2t+v) mod b).

In the W basis, the active block from input character (u',w) to output character (u,v) is

    1_(u=u') D_v F_b S_(v,w).

The x-character is preserved because the two active x copies are identical. In the y coordinate, Q_v F_(2b)=2 D_v F_b E_v, where E_v selects even or odd input positions. Combining with Q_w^T/2 gives the stated signed selector. An inactive block is exactly 1_(u=u')1_(v=w)I_b.

For each active small block, form sum_w S_(v,w) z_(u,w), then apply F_b once for each pair (u,v). There are four b-point transforms per active small block, plus O(b) mixing and phases. Globally the cost is 4|J| T_F(b)+O(N) using this decomposition, matching the radix-two decomposition of the two F_(2b) copies per label. Identical transform matrices applied to four different data vectors count four times.

These are unnormalized bank matrices. With unitary Fourier blocks, the active formula acquires a factor 1/sqrt(2) relative to unitary F_b, while inactive blocks remain identities. Changes to bank normalization or active-label pullback require corresponding changes in the formula; they are not silent overall scalar factors.

## 3 Common Walsh basis and signed holonomy

Each small edge i->P_small(i) transports the four fiber labels by a permutation phi_i. Every permutation of four points is affine over GF(2)^2: the 4 translations and 6 invertible binary 2-by-2 matrices give 24 distinct affine permutations. Writing phi_i(epsilon)=A_i epsilon+t_i yields

    chi_c(phi_i(epsilon)) = (-1)^(c dot t_i) chi_(A_i^T c)(epsilon).

Thus W P_large W^(-1) is a signed permutation on the pairs (character,small vertex). The trivial character yields exactly P_small. The remaining three characters form an invariant signed-permutation sector of dimension 3N. This statement is about the route; nonconstant endpoint masks can couple the trivial and nontrivial sectors.

Transporting once around the base N-cycle gives a sheet holonomy M. The lifted permutation has one cycle for every orbit of M, with its length multiplied by N. Consequently, Hamiltonicity of P_large is equivalent to M being a four-cycle.

The affine linear part of a four-cycle is an order-two element of GL(2,2), since the identity would give a translation of order at most two and GL(2,2) has no element of order four. It fixes one of the three nonzero characters and swaps the other two. The signs on the fixed character and on the product around the exchanged pair are both -1. One proof diagonalizes a four-cycle: its eigenvalues are 1,i,-1,-i, and the trivial character already accounts for 1. Equivalently, check a canonical four-cycle and conjugate by an affine sheet permutation; the corresponding Walsh conjugation is again signed monomial. This latter argument does not require adjoining i.

It follows that the actual 3N-dimensional signed permutation has one signed N-cycle and one signed 2N-cycle, each with total sign -1. Together with the trivial sector, the common-basis Green term can be evaluated with three signed-cycle scans of lengths N, N, and 2N. Their denominators are

    1-tau^N, 1+tau^N, 1+tau^(2N),

whose product is 1-tau^(4N). No invertibility guard is discarded. This direct common-basis evaluator needs only characteristic different from two, not new fourth or 4Nth roots. It still visits a total of 4N vertices per Green term. Eight orders use 24 such scans per layer with total scan length 32N; three layers have 72 scans of mixed lengths and total length 96N, before the separately charged bank and endpoint work.

This is not three ordinary N-cycles, nor four copies of the original ordinary-wrap Green in the fixed Walsh basis. It is also not a lower bound against other channel representations.

## 4 Endpoint masks and the enlarged operator family

For a physical diagonal mask a(i,epsilon), define

    a_hat_c(i) = (1/4) sum_epsilon a(i,epsilon) chi_c(epsilon).

Its common-basis matrix is local on each small fiber, with

    M_a(i)[c,d] = a_hat_(c XOR d)(i).

This follows by multiplying character products chi_c chi_d=chi_(c XOR d). Thus a general endpoint becomes a local four-by-four XOR-convolution matrix; a pure character permutes the character channels. Its determinant is the product of the four original physical mask values. Nonzero original entries do not require nonzero Walsh coefficients, and nonzero Walsh coefficients do not imply an invertible original mask. Both distinctions are explicitly checked.

For a one-sided layer H_large=sum_j diag(a_j) (I-tau_j P_(j,large))^(-1), conjugation by W gives precisely

    sum_j M_(a_j) (I-tau_j S_j)^(-1),
    S_j = W P_(j,large) W^(-1).

This is an exact four-state representation with O(N) application for a fixed number of orders at one level. It enlarges the scalar endpoint/eight-order family. Applying the same coarsening repeatedly can multiply the state dimension by four at each level unless a separate reduction is proved. A constant dimension at one level cannot be assumed constant through the entire recursion.

The scalar-pole claims here do not silently cover arbitrary fiber-dependent edge weights. Such weights become additional local matrix masks in the common basis and can couple channels. Descending weights can be retained as shared base-edge weights, but the scalar tau formulas and their guards must then be replaced by their weighted versions. No arbitrary-weight scalar closure is asserted.

## 5 Route-specific cyclic-character Green decomposition

Traverse the base cycle i_0=0,i_1,...,i_(N-1). Let T_0 be the identity sheet labeling and T_(k+1)=phi_(i_k) T_k. In these transported labels, ordinary edges preserve a reference sheet label, and the wrap acts by M=T_N, a four-cycle. Choose q_c=M^c(0), c=0,1,2,3.

Set xi=omega_(4N)^N, the chosen primitive fourth root (the usual i over the complex numbers with the standard positive root), and use the positive four-point cyclic characters xi^(s c). Define R_s, a map from physical large vectors to base vectors, by putting coefficient xi^(s c) at the physical vertex (i_k,T_k(q_c)) in row i_k. Then

    R_s P_large = T_(eta_s) R_s, eta_s=xi^s,

where T_(eta_s) follows P_small with edge weight 1 on ordinary edges and eta_s on the wrap. The stacked R_s matrix is invertible: it is a sheet permutation followed by independent four-point Fourier transforms on each base fiber. This C4 eigenbasis differs from the fixed V4 Walsh basis and depends on the route through the transports T_k.

Consequently the large Green is conjugate to four scalar length-N Green operators with ordinary weights tau and wrap weight tau eta_s. Their denominators satisfy

    product_s (1-tau^N eta_s) = 1-tau^(4N).

For a homogeneous pole, choose beta_s^N=eta_s, for example beta_s=omega_(4N)^s. Let E_s[i_k,i_k]=beta_s^(-k). The precise conjugation is

    E_s^(-1) T_(eta_s) E_s = beta_s P_small.

Equivalently, setting A_s=E_s^(-1) R_s gives the directly useful identities

    A_s P_large = beta_s P_small A_s,
    A_s (I-tau P_large)^(-1)
      = (I-tau beta_s P_small)^(-1) A_s.

The inverse basis reconstruction is paid too. These are full operator identities on every input column, not selected-column fits. The checker verifies the intertwining entrywise and the resolvent on deterministic full vectors for tau=0,2,3, with all denominator products checked.

## 6 Costs of order-dependent gauges

A traversal obtains all sheet transports, inverse label maps, and phase exponents in O(N) word work and storage per order. Four-point basis conversions have constant size per base vertex. All beta_s^k sequences are generated in O(N) field operations. A route-specific evaluation therefore uses four N-point Green scans plus O(N) gauge work. Eight routes use 32 length-N scans per layer, and three layers use 96; their total scan length matches the common-basis representation above and the original 24 Green terms at size 4N.

The basis for order j is not automatically the basis for another order. Their relative basis change is a local four-by-four matrix on each base fiber, so it remains O(N) for a fixed number of orders, but it can mix channels. Fresh examples have nonzero off-diagonal changes. This demonstrates that these chosen gauges cannot simply be identified; it is not a theorem that every possible simultaneous basis is impossible.

The rational pole list 1/2,...,1/9 is not closed under the displayed homogeneous decomposition. One must allow the four wrap phases or the new poles tau_j omega_(4N)^s and the left/right order-index gauges. A general endpoint mask in such a basis is likewise a local matrix, not an unchanged scalar diagonal. Sharing one transformed endpoint family across all eight orders requires a separate proof.

The valid constructive outputs are the exact common-basis and order-specific identities. They do not supply the coupled coefficient solution, the recursive state/term reduction, the active-bank mass bound, or a bridge from the N16 fitting family to the separately selected large hierarchical bases. They neither invalidate the earlier common-cut capacity result nor promote it to Fourier synthesis, varying-stage separator control, or attained cross ranks.

## 7 Independent checks and replay

All checks are review-authored Python using the standard library. Exact arithmetic is in the prime field of order 998244353 with primitive generator 3 for the needed dyadic roots. The checker imports only the review-authored exact_utils.py. The general proofs above are not inferred merely from finite tests.

The recorded run passes:

- 16 Fourier layout/sign cases for b=1,2,4,8 and a=b,2b, covering N through 128, with 699040 entry equalities, full vector reconstruction, and both exponent orientations;
- all 24 sheet permutations, including all six four-cycle holonomies and their signed-character cycles;
- 32 hierarchical four-sheet routes from both square and rectangular small bases, all eight shear labels, and two consecutive lifts, with base N through 32;
- 384 exact channel-resolvent equalities and explicit full-rank channel-coordinate matrices;
- 14 comparisons of order-specific fiber bases, including nontrivial changes;
- 20 active/inactive bank cases for b through 16 and both exponent conventions, with 21824 entry equalities;
- four mask cases including the two contrasting invertibility guards.

The checked hierarchical routes are rebuilt by fresh review code: minimum-representative base splicing, base-preserving sheet lift, and fiber-zero merge. Constructor implementations remain inert. The previous independently reviewed hierarchy theorem justifies the all-size route assumptions; these bounded checks audit the new channel identities on explicit routes.

Run `python3 independent_checks.py` in the package directory. It regenerates VERIFIED_RESULTS.json deterministically. PORTABLE_REPLAY.json records replay in an isolated temporary directory containing only the two review-authored Python files; its result must be byte-identical. SEALED_MANIFEST.json and its SHA256 sidecar identify every sealed file. Source provenance records the exact constructor note inspected; frozen older reviews remain untouched.
