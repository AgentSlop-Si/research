# A two-parameter family of fourteen-bank order-eleven realizations

10 October 2026. Author addendum to the frozen N11_FOURTEEN_BANK_CONSTRUCTION.md. This does not change its node polynomial, witness, or proof. It extracts a genuine parametric extension from the same four moment constraints. Independent review is pending for this addendum.

## Statement

Keep q, K=Q(q), H, T, the nine moments s_i, the seven moments u_i, and the invertible 4×4 matrix A exactly as defined in Sections 2–4 of the main construction. For two parameters λ,μ set c_4=λ, c_5=μ, c_6=1 and define

(c_0,c_1,c_2,c_3)^t
 = A^−1 (−s_6−λs_4−μs_5,
          −s_7−λs_5−μs_6,
          −s_8−λs_6−μs_7,
          −u_6−λu_4−μu_5)^t.

Thus every c_0,...,c_3 is an explicitly defined affine polynomial in λ,μ with coefficients in K. Let

g_(λ,μ)(t)=t^6+μt^5+λt^4+c_3t^3+c_2t²+c_1t+c_0.

Construct the remainders p_r, matrices M_b, and the same selected 11×11 minors D_b for b=0,3,4,5 exactly as in Section 5 of the main note, now using this sextic. Define the explicit exceptional polynomial

P(λ,μ)=c_0 Res_t(g_(λ,μ),∂g_(λ,μ)/∂t) D_0 D_3 D_4 D_5 ∈ K[λ,μ].

This definition is finite and explicit: the resultant is the determinant of the usual 11×11 Sylvester matrix, and each D_b is the determinant of the stated eleven-column submatrix. The entries p_r are polynomial in the c_i because reduction is by a monic polynomial; hence P has no parameter-dependent denominator.

For every characteristic-zero extension E of K and every (λ,μ)∈E² with P(λ,μ)≠0, the main construction gives a fourteen-bank representation of F_11 over the splitting field L of g_(λ,μ) over E. Its orientation multiplicities remain (6,1,1,6), all beta values remain 1, its two singleton alpha values remain 1, and its six roots are used in each same-sign orientation. One has [L:E]≤720.

The permitted parameter set is nonempty: at (λ,μ)=(0,0) it is precisely the already-certified main construction. In the good reduction at (23,q−2),

P(0,0)=12·6·5·3·18·8=17≠0 modulo 23.

Therefore P is not the zero polynomial. This supplies a nonempty Zariski-open two-parameter family. In particular it supplies infinitely many choices (λ,μ)∈K², since K is infinite. These are infinitely many realizations at the fixed order eleven, not an infinite family of transform orders.

## Proof

The four defining affine equations give the same recurrences

s_(r+6)+sum_(k=0)^5 c_k s_(r+k)=0, r=0,1,2,
u_6+sum_(k=0)^5 c_k u_k=0

identically in λ,μ. The edge formulas in Sections 6 and 8 of the main note were already written with sums over all six coefficients; their proofs use these recurrences and c_0≠0, not c_4=c_5=0. Therefore the b=1 and b=2 rows remain exactly compatible.

If P≠0 then g has six distinct nonzero roots, its four selected row minors are invertible, and all Lagrange amplitude formulas are legal. All other denominators are the unchanged nonzero Gaussian factors and constants in K. The four nonsingular rows, the five reflection assignments, and the raw-weight formula therefore apply verbatim. The exact original-resolvent identity and phase orthogonality prove equality to F_11 in the original grammar. This proves the claim for every permitted parameter pair.

## Scope and counts

There are two independent free coefficient parameters, λ and μ, before excluding the explicit proper algebraic exceptional set P=0. The four other lower sextic coefficients are determined by the fixed 4×4 solve. The selected-row zero-coordinate conventions are fixed as before, not extra free parameters in this stated family. Root ordering merely relabels banks.

For each parameter pair the result has at most 14 whole banks and 154 raw weights, with the same preparation inventory as the main construction. The rational coefficient field becomes E and the root splitting field is a distinct, explicit additional requirement. This does not establish minimality, an all-size formula, any evaluation-cost advantage, or novelty relative to literature.
