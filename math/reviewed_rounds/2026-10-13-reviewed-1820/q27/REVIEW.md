# Q27 independent review: structural holonomy-gauge transfer obstruction

13 October 2026 UTC

## Verdict

**ACCEPT the precise structural and literal-certificate transport obstructions.** No repair is required for those bounded conclusions. This is not acceptance of a new exclusion or a classification of certificate routes.

The source label (stage 2; edges 8,9,11) remains accepted. The comparison label (stage 2; edges 8,9,12) remains unclassified. Accepted coordinate coverage stays **193/5,984**, leaving **5,791** unclassified labels. The full 34-phase fiber and the parent problem remain **OPEN**. Priority remains **50**.

A fresh independently written exact checker passed **1,520 checks**, including **18 controls**. It reconstructs the matrices and polynomials from the pinned chart, rather than running the candidate checker or accepting its receipts. Every one of the candidate's 63 nonzero transfer-residual coefficients agrees exactly, and the residual is independently nonzero at the stated regular unit point and a second regular unit point.

## 1. Input bindings, sources, and independence

The nominated candidate was supplied locally and is included verbatim as INPUT_CANDIDATE.zip. Its SHA-256 is:

7b7d129ca178d6fc15bbe18fb6a662bf3f9afb9f72c01835ab5c2e7eb55f430e

Its six-member manifest was verified with exact member-set equality, unique paths, safe paths, byte lengths, and SHA-256 values. The same checks were performed for the 12-member manifest of the nested accepted-193 archive and the 20-member manifest of its nested source author archive. The five candidate source-pin values were checked against the actual nested bytes.

The principal source bindings are:

- Accepted-193 ZIP: 1360f205268f3a58ddaeef0da9f4c76de8d76f3583b6f4e27dde64b65f95aea1
- Accepted source author ZIP: 225cb8cc9f77fdce7944e509b24bf50cc9360057dbf7e2570337c2d1efa6b157
- Original CHART.json: 5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98
- Source CERTIFICATE.json: 09635f366f111b6de8f95cc5b7f6be04963a343e8f8d6835ae100dcab8dc8558
- Accepted COVERAGE_193.json: 92627909ca69f209143e200143ee13efc4b84db6bbb6f93e00ce4425a0088a28

The three Phase40/41/42 inert source snapshots were read as definitions. They were not executed, imported, compiled, or evaluated. Phase40 and Phase41 specify target=cycle[j], source=cycle[j-1]; Phase41 uses an unweighted sum of the three original inverse matrices; Phase42 fixes seeds 42420 and 42520, the Gaussian-pair recipe, and the prescribed product S2*S1. Their hashes are retained in INDEPENDENT_RESULTS.json and are bound by the nested source manifest.

The candidate checker was read for audit only. No candidate, historical, or prior-review research program was executed or imported. The sole research program executed for this review is the freshly authored review_fresh.py. SymPy 1.14.0 provides exact Q(i) polynomial arithmetic and DomainMatrix exact determinant/inverse operations. Active Green numerators were rebuilt from ordinary matrix powers, independently of the candidate's directed-path construction. The fresh checker imports standard and SymPy libraries only.

The inherited historical limitation is preserved: the supplied snapshots bind the present source definitions but do not authenticate newly recovered canonical historical source blobs, an external repository, or a historical author. The inherited 192 exclusion proofs are not rerun by this review. The accepted source slice's literal polynomial certificate is freshly rechecked.

## 2. Original model and all six guards

N=8. Each stage retains its three original directed cycles and 24 gains. Fresh seeded generation matches all six cycle masks and all 34 Gaussian pairs. A separately written graph-reachability forest construction selects exactly edge indices 0 through 6 as the tree in each stage. All 48 gains have exact unit norm, with all 14 tree gains equal to one.

Only stage-2 branch-1 edges (8,9,11), or (8,9,12), receive x,y,z in that order. The other 31 free phases remain frozen. There is no branch weighting, interstage diagonal, changed witness, or stage-order substitution.

The model remains

G_sb=(I-W_sb)^(-1), S_s=G_s0+G_s1+G_s2, M=S2*S1.

Let L=S1, C=G20+G22, and h=h21. Fresh exact multiplication gives

h=(-4335586066535028372496+1298149621513208810103 i)/4525759492081695535625.

Both slices retain f=1-hxyz. All six source and candidate guard records were independently matched, including their stage, branch, holonomy, and entire guard polynomial. The other five original guards are separate, nonzero constants. Six frozen original Green matrices were directly inverted with two-sided checks and det(I-W)=1-h for every branch.

The unit point (1,1,conjugate(h)) is still a genuine excluded pole. The fresh active original matrix has determinant zero there, and its exact inverse raises the specific noninvertible-matrix exception; the five inactive guards remain nonzero.

## 3. Holonomy-gauge criterion and required hypotheses

For weighted transition matrices W_a,W_b on the same directed n-cycle, with every a_j,b_j nonzero, diagonal conjugation imposes

d_cycle[j]/d_cycle[j-1]=b_j/a_j.

Multiplying the n equations proves equal holonomy is necessary. Conversely, select one nonzero diagonal entry and propagate along the cycle. Equal holonomy makes the final recurrence consistent. The resulting D is invertible and unique up to scalar. Monomial ratios produce Laurent-monomial diagonal entries. This proves the candidate's first claim. Characteristic zero is adequate; no extra unmentioned positivity or unit-modulus assumption is needed for this algebraic lemma.

When the Green inverses exist, G_b=D G_a D^(-1). When L is invertible, define E=L^(-1)D^(-1)L. Direct expansion gives

M_b-D M_a E=(C-D C D^(-1))L.

Since L is invertible, this vanishes if and only if DC=CD. The invertibility of L is essential for this converse and for the stated definition of E. A fresh exact singular-L control demonstrates that a nonzero C-DCD^(-1) can annihilate a singular L; the unqualified converse is not accepted without the hypothesis.

For diagonal D,

(DC-CD)_rc=(d_r-d_c)C_rc.

Thus diagonal entries must agree along every edge of the undirected support graph formed by nonzero entries of C. Conversely, componentwise constant diagonal entries commute with C. Connected support forces D scalar. This argument is exact and does not enumerate coordinate triples. Controls include a disconnected background admitting a nonscalar commuting diagonal, a connected background rejecting it, and a two-cycle example where the complete canonical product identity succeeds for a commuting background and fails for a noncommuting background.

The claim concerning E is accepted in its direct-action sense: an invertible monomial E would allow the displayed equality itself to be interpreted as the prescribed external row/column monomial action. A dense E supplies no such direct action. This review does not infer from density alone that a matrix cannot accidentally lie in the same monomial orbit through some other transformation. No classification of all orbit coincidences or certificate transformations follows.

## 4. Frozen background and the neighboring triple

Every one of the 64 entries of C was freshly reconstructed, individually checked nonzero, and matched against the candidate. All 64 entries of L also matched and are nonzero. A fresh two-sided exact inverse proves L invertible, with determinant

4128500902846000013117604197/1284237393686217537633116
+ (112055293030001871276686265/67591441772958817770164) i.

Consequently, any genuinely nonscalar diagonal gauge fails the canonical full-product transport in this chart. A scalar specialization, such as z=1 in the specific comparison, is not claimed obstructed.

The active branch cycle is (3,4,2,6,7,5,0,1). For a=(8,9,11) and b=(8,9,12), the normalized gauge is

D=diag(1,1,1,1,1,1,z^(-1),1).

The fresh checker verifies W_b=D W_a D^(-1), and separately B_b=D B_a D^(-1) for B=I+W+...+W^7, on full Laurent support. Wrong gauge sign and identity-gauge controls fail as expected. The exact background witness is

C_6,0=-1451705013403/3813778015676-(126100838144/55931942249)i,

so

(C-DCD^(-1))_6,0=(1-z^(-1))C_6,0

is a nonzero Laurent polynomial. The complete 64-entry symbolic error identity was checked:

n_b-[D(B_a+fC)D^(-1)]L=f(C-DCD^(-1))L, with n=fM.

At (x,y,z)=(1,1,i), all six original guards are nonzero. In particular,

f=(5823909113594904345728+4335586066535028372496 i)/4525759492081695535625.

The background witness equals (1+i)C_6,0 and is nonzero. The exact induced E at this point has eight nonzero entries in each of its eight rows, so it is not monomial. Its complete Gaussian-rational entries are recorded in INDEPENDENT_RESULTS.json.

## 5. Literal original-defect certificate transplant

For each slice, powers of the original active W reconstruct B, with full identities

W^8=hxyz I, (I-W)B=B(I-W)=fI,

and n=(B+fC)L. Fresh denominator clearing gives the same least positive integer for both slices:

S=47657433783260301946927308623286197903901526077573294125500000.

Let N=S n and Ntilde=xyz conjugate(N)(1/x,1/y,1/z). Every entry is verified Gaussian-integral and triaffine. All 49 original anchored defects are rebuilt in each slice:

P_rc=N_rc N_00 Ntilde_rc Ntilde_00-N_r0 N_0c Ntilde_r0 Ntilde_0c,

for 1<=r,c<=7. No anchor or matrix-entry division is introduced. All 98 polynomials divide exactly by f, with multiplication back checked on complete support. All source numerator coefficients and all 49 source defects agree with the sealed accepted independent reconstruction.

The source has 49 positive real rational contents c_j and quotient bridges P_j=f c_j q_j. Every bridge is rechecked. The 42 distinct in-range constant multipliers are nonzero Gaussian integers, and the common denominator d is positive with 3,803 decimal digits. H=4525759492081695535625 is independently reconstructed. Complete coefficient accumulation verifies both identities separately:

sum a_j q_j=dHf,

sum (a_j/c_j)P_j^(a)=dHf^2.

The fresh residual is computed directly from the full original-polynomial differences:

R=sum (a_j/c_j)(P_j^(b)-P_j^(a)).

It also equals sum (a_j/c_j)P_j^(b)-dHf^2. Its **63 nonzero coefficients** match the candidate coefficient-for-coefficient, not just by hash or at sample points. The exact complete residual is serialized in INDEPENDENT_RESULTS.json.

R(1,1,i) agrees with the candidate's entire Gaussian-rational value and is nonzero. A second independently selected regular unit point,

((3+4i)/5, (5+12i)/13, (8-15i)/17),

also gives nonzero R. Both entire exact values and all six guard values are serialized. At each point and for each slice, the six original matrices were inverted anew. This gives 24 regular original inversions, 256 exact product-numerator entry checks, and 196 exact original modulus-defect bridge checks. Independently accumulated weighted defects from these direct matrices agree with R at both points. These finite checks supplement the coefficient proof.

The z=1 specialization is a positive control: the two original models coincide at (1,1,1), and the residual vanishes there. This confirms that the nonzero residual is a polynomial obstruction, not a claim of pointwise failure at every possible specialization.

## 6. Controls and preserved scope

All 18 fresh controls pass: wrong gauge sign, identity gauge, omitted background error, same-slice transport, positive z=1 specialization, omitted actual source term, changed denominator, unsupported residual coefficient, wrong residual sign, dense E detection, disconnected/connected support behavior, the necessity of invertible L, equal/unequal holonomy closure, full transport with commuting/noncommuting backgrounds, and original pole rejection.

The inherited ledger was independently regenerated as 128 labels (s;7,a,b), 56 stage-1 branch-1 triples, eight cyclic-consecutive stage-2 branch-1 triples, and the accepted (2;8,9,11) label. It agrees exactly with all 193 stored labels. The comparison label is absent. These are coordinate-label counts; they do not claim disjoint geometric slices.

Acceptance means:

1. Equal active holonomy does not suffice for the specified canonical gauge to extend through the frozen background and product.
2. The accepted slice's particular literal same-anchor, same-scale multipliers do not form the same certificate on the comparison slice.

It does not mean that the comparison slice is feasible, Fourier-equivalent, excluded, or inaccessible to another certificate. It does not exclude all constant-multiplier, higher-degree, transformed, nonlinear, or other certificate routes. No conclusion is made for another witness, weighted stage sums, an interstage diagonal, larger N, nonunit internal phases, cross-stage movement, the full phase fiber, Fourier synthesis, computational speed, or historical novelty.

No external writes, GitHub changes, Sheet updates, sharing, or publication actions were performed.

## 7. Reproduction and sealing

Run `python review_fresh.py` from this packet directory. It reads the included hash-pinned candidate as inert input and writes INDEPENDENT_RESULTS.json. RUN.log records a successful run. The sealed packet includes the full nominated candidate, fresh checker, exact results, report, and README. MANIFEST.json covers every packet member except itself. The external SEAL.json records the final review ZIP hash and the clean-replay verification result.

A fresh extraction is run before handoff. Its regenerated exact-results bytes and successful log must agree with the sealed versions. Only the independent checker is executed in that replay.
