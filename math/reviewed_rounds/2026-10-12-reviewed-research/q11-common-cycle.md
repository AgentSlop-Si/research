Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 6242262e774762595139e6d11f57fc70c6dcff31e6de3f23e8534ee512ae8865

---

# Q11 common-cycle base-field obstruction: independent review

Date: 2026-10-11 UTC. Verdict: **ACCEPT SCOPED. No mathematical repair required.**

The accepted statement is: for every positive odd integer q with gcd(q,5)=1 and q ≡ 1 (mod 241), the specified five-coordinate block C_q has no representation over K=Q(eta) as two arbitrary diagonal-ended Hamiltonian-cycle Green terms sharing one structural cycle, plus an arbitrary diagonal matrix. All 24 directed cycle orders, arbitrary independent weights and endpoints, singular endpoint masks, and initially allowed zero edge weights are covered.

This closes that architecture over the base field. It does not close Q11's general base-field length-three question. Two different structural cycles plus a diagonal, three genuinely non-diagonal Green terms with arbitrary cycles, and growing full-B upper constructions remain open. The accepted quadratic-extension upper and previously accepted both-sign lower results are unchanged. No worldwide-priority or new-discovery-count conclusion is made.

## 1. Reviewed sources and integrity

The reviewed author archive is `Q11_Common_Cycle_Base_Field_Obstruction_CANDIDATE_2026-10-11.zip`, 55,202 bytes, SHA-256 `b2408282ce177cb939dccf5648fc5b4bca0662e023bab88ed6bf9d39cf269844`. Its `REPORT.md` is SHA-256 `07e2304fda5dca714aed4970119d47e35221b055a1f5020d6a7296afd1d49e44`.

The archive's 16 members match the supplied local files byte for byte. All 15 payload entries match the author's manifest; the manifest matches its seal. All seven source pins match. The original source paths were additionally checked against their recorded hashes and sizes in the review workspace; the six full-source copies are byte-identical, and the seventh extract's full parent source matches its separate parent-source pin.

Principal accepted dependencies:

- Exact C_q formula and allowed Green grammar: `SP11_ACCEPTED_PROOF.md`, sections 2, 2.1, 2.5; SHA-256 `4aed4e38953ac9266f8dbe8995dae1d61046f02972f11c5434c018681eac8df5`.
- Its independent acceptance: `SP11_INDEPENDENT_REVIEW.md`, SHA-256 `79f959f1b57550e031bf99e9d7ff8e5a26f76045bda4ddf56c60f366613940e8`.
- Frozen H01–H05 ledger: SHA-256 `b7480082c457ab4a906dbbca4ca52967e452157bba88f70c72a4d994381a335b`. H13 remains open in its general scope.
- Separate accepted negative-chirp review, preserved rather than replayed: SHA-256 `d89108b404074f6b3d995407b61b30acb57aa07069e736b29bf53025292d3c4b`.

The new proof uses the accepted entry formula, not the historical two-Green exclusion certificate. No author, uploaded, or historical program was executed, imported, compiled, or AST-parsed. Both executed programs in this review were authored independently from the displayed mathematical statements and use only the Python standard library. Candidate JSON is inert comparison data, read after independent reconstruction. No external write was made.

## 2. Independent necessity proof, including degenerate branches

Fix any directed cycle, relabelled in traversal order 0,1,2,3,4. Write each branch as L_s(I-W_s)^(-1)R_s, with (W_s x)_i=w_i^(s)x_(i+1), holonomy rho_s=product_i w_i^(s), and 1-rho_s nonzero. The target may also have any diagonal correction.

For a target T and each j modulo five, take A_j from rows j-2,j-1 and columns j,j+1. Take v_j from those same rows and column j+2. These are all off-diagonal positions, so the correction is irrelevant.

For one branch, its contribution to A_j is exactly

w_(j-1)/(1-rho) × [ell_(j-2)w_(j-2), ell_(j-1)]^T × [r_j, w_j r_(j+1)].

This follows either from the finite inverse identity (I-W)^(-1)=(I+W+...+W^4)/(1-rho), or by listing the four unique forward paths. It is rank at most one with no division by an edge or endpoint. If w_(j-1)=0, that branch contributes the zero window. The other branch has rank at most one. Thus an invertible target A_j forces w_(j-1) nonzero in both branches. Invertibility of all five target windows forces every edge in both branches nonzero and hence both holonomies nonzero. Entirely masked-out branches also cannot produce an invertible target window. These are consequences of the target, not omitted open guards.

Now define p_0=1 and p_(i+1)=w_i p_i for every integer i, extending weights and endpoints periodically. Because the edges have just been forced nonzero, this two-sided definition is legal and p_(i+5)=rho p_i. Set x_i=ell_i/p_i and y_i=p_i r_i/(1-rho). For 0<j-i<5, the branch entry at the corresponding residue classes is x_i y_j. Therefore the two-branch target satisfies T_ij=x_i^(1)y_j^(1)+x_i^(2)y_j^(2) on each unwrapped off-diagonal interval.

Let X_j have rows (x_(j-2)^(1),x_(j-2)^(2)) and (x_(j-1)^(1),x_(j-1)^(2)). Let S_j have rows (y_j^(1),y_j^(2)) and (y_(j+1)^(1),y_(j+1)^(2)). Then A_j=X_j S_j^T. A_j invertible over K forces both square factors invertible, even if some individual endpoint entries vanish.

Define (a_j,b_j)^T=A_j^(-1)v_j. Cancelling X_j gives y_(j+2)^(s)=a_j y_j^(s)+b_j y_(j+1)^(s) for both branches. Consequently S_(j+1)=Q_j S_j, with Q_j=[[0,1],[a_j,b_j]]. In the order M=Q_4 Q_3 Q_2 Q_1 Q_0, this yields

M S_0 = S_5 = S_0 diag(rho_1,rho_2).

As S_0 is invertible, M is similar over K to that diagonal matrix. Its eigenvalues really are the two branch holonomies, with multiplicity. In particular, tr(M)=rho_1+rho_2, det(M)=rho_1 rho_2, and D=(tr M)^2-4det M=(rho_1-rho_2)^2. If the holonomies coincide, the stronger conclusion is M=rho_1 I; no repeated-eigenvalue or non-diagonalizable case is omitted.

The matrix M is computed from T alone. No proposed branch coordinates have to be recovered, inverted, or specialized after the invariant is established. The proof assumes neither reciprocal holonomies nor transpose relations nor common endpoint vectors. It asserts necessity only.

## 3. Independent residue reconstruction

The supplied omega, N=5q^2, eta=omega^(q^4), and K are exactly as in the accepted source. Eta has order five. The accepted entry formula is

C_q[i,j] = (eta^(ij) - qg eta^(-3(i+j)^2) + 5q^3g eta^(-3i^2) delta_ij)/(1+5q^3g),

g=1+2(eta^2+eta^3), g^2=5.

The q and q^3 factors are essential and were retained. The denominator's product with its g-conjugate is 1-125q^6, which is nonzero for the specified positive integral q.

The fresh checker independently verifies that 241 is prime and 91,87 are exact-order-five roots. It constructs both residue targets directly from the entry formula. At q=1 it also reconstructs each target by independent 5×5 Gauss–Jordan inversion of F_5^(-1)+A_5. The denominators are 34 at eta=91 and 209 at eta=87, and g is respectively 103 and 138. At eta=91 the target is

    161  20 102 102  20
     20 182  62  26  92
    102  62 236  28  26
    102  26  28 236  62
     20  92  26  62 182.

Every directed Hamiltonian cycle appears exactly once as (0, permutation of 1,2,3,4). Reversal is retained. For both anchors and every cycle, the reviewer independently forms all five windows, solves the recurrences by Gauss–Jordan inversion, and advances the two basis states in the required product order. All 240 window determinants are nonzero. All 48 monodromy determinants equal 1.

The entire author table matches, including every window, right-hand side, recurrence coefficient, transfer matrix, product, trace, determinant, discriminant, Euler symbol, and exhaustive square-root list. Sixteen orders are excluded at eta=91; the other eight are excluded at eta=87. At eta=87 alone, four orders remain unexcluded. Those single-prime limitations are retained explicitly.

For example, cycle 01234 at eta=91 yields M=[[199,160],[190,200]], trace 158, determinant 1, discriminant 137. Cycle 01324 at eta=87 yields trace 122 and discriminant 179. Each selected discriminant is nonzero, has Euler symbol 240, and has no square root among all 241 residues.

The review certificate contains all selected witnesses and both complete anchor tables. No author program was needed to obtain them.

## 4. Why the conclusion is characteristic-zero and uniform in q

For each cycle choose its certified eta residue z. Let R=Z[eta]_(241,eta-z), inside K. The fifth cyclotomic integer ring is Z[eta]; hence this localization is integrally closed. Equivalently, the selected prime is an unramified degree-one prime above 241, and its localization is a discrete valuation ring. The roots are simple: because 241 does not divide 5, X^5-1 is separable modulo 241.

For every integer q congruent to 1 modulo 241, q and q^3 have residues 1. Thus the target denominator is a unit of R and its target residue is exactly the independently rebuilt matrix. Every selected window determinant is also a unit. This simultaneously establishes characteristic-zero nonvanishing of the window determinants and legitimizes every inverse used in a_j,b_j and M. The resulting D lies in R and reduces to the selected nonzero nonsquare.

If a K-representation of the stipulated architecture existed, the necessity proof would give D=e^2 for e=rho_1-rho_2 in K. Since e satisfies the monic polynomial X^2-D over R, e is integral over R. Integrally closedness forces e into R. Reducing e^2=D would then exhibit a square root of the certified nonsquare in F_241, a contradiction. In valuation language, v(D)=0 forces 2v(e)=0, so e is a unit and its residue gives the same contradiction.

Crucially, the branch endpoints and weights themselves need not be regular at this prime. The proof never reduces them. Only the square root forced by the characteristic-zero invariant is shown regular. This rules out the entire K-architecture, not merely representations that survive a chosen open reduction guard.

This is an all-q argument, not an extrapolation from q=1. It also covers every primitive complex choice of eta: the formula defines the same algebraic problem in the abstract fifth cyclotomic field, and any primitive realization is a field isomorphism. The prime eta→z exists for each chosen realization.

## 5. Fresh positive, negative, and characteristic-zero controls

The controls are independent checks of indexing and boundaries, not substitutes for the uniform proof:

- 144 independently generated legal two-branch targets over F_241 and F_101, spanning all 24 structural orders. Green matrices are built by direct 5×5 inverse, independently of the path factorization.
- 48 of those targets have singular left and right endpoint masks in both branches. All five target windows are kept invertible. No zero endpoint is removed from these cases.
- 24 controls have equal branch holonomies. Their recovered M is exactly rho I, checking the repeated-eigenvalue case.
- Every control verifies the exact conjugacy equation M S_0=S_0 diag(rho_1,rho_2), trace, determinant, discriminant, and characteristic-polynomial evaluation at each holonomy.
- Ten controls place a zero edge in each branch and at each edge location. The predicted branch window is identically zero and the target minor vanishes.
- Two controls mask an entire branch. All five target window minors vanish.
- Arbitrary diagonal mutations preserve all 48 target invariants. Reversing multiplication order changes every one of the 48 product matrices. A changed off-diagonal target entry changes the checked product.
- Both residue targets agree at five explicitly eligible q-values. This is only a control of the congruence substitution.
- A separate fresh exact implementation of Q[X]/Phi_5(X) recomputes all 24 monodromies at q=1 and q=483. All 48 exact-field cases have determinant 1 and reproduce the selected residue minors, traces, and discriminants. These are characteristic-zero controls, not the all-q proof.

A cold reconstruction in a new local directory reproduces the finite certificate, exact-field certificate, and source-pin record byte for byte. The bundle contains both fresh programs and the candidate source data needed for a local reproduction. Reproducing the finite and exact-field controls needs only Python's standard library. If original workspace source paths are present, the checker also verifies them; otherwise the pinned copies and archive remain checked, while historical-path re-verification is unavailable.

## 6. Integration and scope boundaries

Accept `Q11-COMMON-CYCLE-BASE-FIELD-OBSTRUCTION` as a new, scoped obstruction strengthening the earlier construction-specific quadratic-field obstruction. Do not describe it as impossibility of every base-field length-three representation. Do not mark the whole Q11 upper gate closed.

Retain the explicit family qualifiers in every standalone annotation: q positive odd, gcd(q,5)=1, q ≡ 1 (mod 241). Keep the accepted quadratic-extension upper and H01–H05 unchanged. Preserve the separate M-CHIRP-LOWER both-sign results. Do not change discovery counts, novelty claims, rankings, historical blanks, or numerical/FFT performance claims.

The obstruction and all 24 cycle checks are fixed-dimensional. This is not a growing-N executor. Existing input construction and exact-coordinate preparation costs remain charged; no finite-field test count is a runtime speedup theorem.

`ROW_GUIDANCE.json` gives precise source-bound wording for the sole table writer. Fresh stable-ID and old-value checks remain required before any actual row write. This independent review itself makes no Sheet, GitHub, or Library mutation.
