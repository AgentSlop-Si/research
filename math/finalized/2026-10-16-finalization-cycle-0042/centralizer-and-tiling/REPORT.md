# Two source-bound finalization targets

Date: 2026-10-16 UTC. Baseline: `AgentSlop-Si/research` main `0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4` (69 closed / 258 open). Workbook: `1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU`.

## Findings ready for independent review

1. **ALG-MONOMIAL-CENTRALIZER:** the accepted complex monomial-commutant classification is an exact specialization of Tadej's complete unitary monomial stabilizer theorem, after a justified scalar normalization. The arbitrary splitting-field statement is retained as the accepted algebraic extension; it is not represented as an explicit theorem of this complex-unitary source. The full owner's current bounded comparison can close. Its listed exclusions are not silently converted into promised successor work.
2. **M-RECTANGLE-TILING:** the endpoint-incidence objective is exactly the wire-count objective of the corresponding depth-two factorization, but only on the much smaller disjoint-rectangle feasible class. The selected primary circuit theorems are qualified nonmatches for the exact cyclic divisor-dependent optimum. The remaining nonsquare-composite higher-rank optimum is an actual owner obligation, so this record stays TO RESEARCH at 42.

This report adds source comparison and a mathematical notation bridge. It adds no source-program execution, finite experiment, implementation acceptance, solver result, performance claim, theorem novelty or worldwide-priority claim. No external write occurred.

## 1. Full owner and prior-completion check

The complete rows were read live, including historical and current obligations, rather than selecting from an abbreviated index alone:

| Stable ID | Overview | Catalogue owner | Novelty owner |
|---|---|---|---|
| ALG-MONOMIAL-CENTRALIZER | 68 | 26 | 51 |
| M-RECTANGLE-TILING | 93 | 50 | 76 |

`OWNER_SNAPSHOT.json` preserves the bounded native read with exact CellData, including formulas and rich-link metadata. `SOURCE_INDEX.json` preserves both selected records from the pinned derivative index.

For the centralizer, Catalogue H26/I26/J26 and X26 give the accepted all-N classification, its monomial-only model and prior proof status. Z26 excludes the full dense commutant, uncharged unrelated gauges/routing and unrestricted runtime conclusions. AE26/AF26 ask for a primary theorem, an exact hypothesis/formula/cost mapping, or a qualified nonmatch. There is no outstanding production obligation in this record. Historical novelty is explicitly unverified.

For tiling, Catalogue X50/Y50 give the exact disjoint rank-one incidence theorem. Z50 expressly keeps the higher-rank optimum for nonsquare composites open. AE50 records the earlier Delvaux–Van Barel Lemma 11 rank-one-block comparison as **already complete**. This report does not award fresh completion credit for that construction, its subgroup proof, accepted finite census, shared Cooley–Tukey implementation, or any earlier review. The newly compared object is the independent endpoint-incidence objective and its feasible class.

## 2. ALG-MONOMIAL-CENTRALIZER

### Source and exact scope

Primary: Wojciech Tadej, *Defect and equivalence of unitary matrices. The Fourier case*, [arXiv:1310.8119v2](https://arxiv.org/pdf/1310.8119v2). Relevant locators: Definition 3.1 (two-sided unitary monomial action); Corollary 4.8 and Lemma 4.9 (printed pp.44–45); Definition 4.11 (pp.46–47); Lemma 4.22 (pp.55–56); Theorem 4.23(c), equation (197) (pp.56–57). The version label is pinned; the PDF extraction displays both a 2014 arXiv version stamp and a 2022 internal title-page date, so no publication-date inference is made from that title page.

Tadej describes the full stabilizer of a complex finite-abelian Fourier matrix under paired permutation-and-phase operations. It factors into the permutation stabilizer and translations/modulations with a common unit scalar. In the cyclic case the two automorphisms are inverse to one another. This is a stronger two-sided symmetry description than the owner's one-matrix commutant, but it is stated in the complex unitary setting. The following specialization is our explicit bridge, not a claim that the printed theorem already uses the owner's variables or arbitrary field.

### Explicit normalization and bridge

Use the owner's positive-root convention `F[i,j]=omega^(ij)`, a primitive Nth root, and `Q e_j=a_j e_tau(j)`, with all `a_j` nonzero. Initially work over C and N>=2. Let `b=tau(0)`. Evaluating `FQ=QF` at row `tau(i)`, column 0 gives

`a_i = a_0 omega^(b tau(i))`.

Consequently all `|a_i|=|a_0|`. Thus `Q/a_0` is unitary monomial, and `(Q/a_0,Q/a_0)` belongs to the two-sided stabilizer: `S F T*=F` is equivalent to `SF=FT`. Dividing by a nonzero scalar neither changes commutation nor changes the permutation. This step is essential: arbitrary invertible monomials cannot simply be inserted into a unitary theorem.

Here is a basis-action translation of the cyclic stabilizer parameterization, derived by entry comparison to fix all signs. Let `u` be a unit modulo N and choose `b,c` modulo N. Every cyclic stabilizing pair has the form

`S e_i = theta omega^(u c i) e_(u i+b)`,

`T e_j = theta omega^(-u^(-1) b j-b c) e_(u^(-1) j+c)`,

with `|theta|=1`. Indeed the row `u i+b`, column j equality `SF=FT` reads

`theta omega^(u c i+ij) = theta omega^(-u^(-1)b j-bc+(u i+b)(u^(-1)j+c))`.

The exponents coincide. Completeness of these affine/character parameters follows from Tadej's complete stabilizer, Lemma 4.9's cyclic inverse pairing and its translation/modulation factors. This formula uses basis images, avoiding the inverse-permutation indexing convention of the printed `P_rho` matrices.

Impose `S=T`. Equality of permutation parts gives `u^2=1` and `c=b`. Equality of the weights gives

`omega^(u b j)=omega^(-u b j-b^2)` for every j.

The j=0 equation yields `b^2=0`; comparison with j=1 yields `2ub=0`, equivalent to `2b=0` because u is a unit. Returning the arbitrary common scalar, we recover exactly

`tau(j)=u j+b`, `u^2=1`, `2b=b^2=0`, `a_j=a_0 omega^(u b j)`.

Conversely the displayed stabilizing pair with c=b is diagonal under those congruences, so it commutes with F. This also follows from the entry equality directly. No new all-N proof acceptance is sought: the owner already has that theorem; this calculation binds it to the primary result.

For odd N, `2b=0` forces b=0. For even N the only candidates are 0 and N/2; the latter has `b^2=0 mod N` exactly when 4 divides N. N=1 is handled separately: F=[1], the sole permutation is identity, and every nonzero scalar Q commutes. No use of j=1 as a distinct coordinate or of an ambiguous unit convention in Z/1Z is needed.

### Field and cost boundaries

The owner's accepted proof also works over any field containing an element of exact order N. In positive characteristic that premise already forces characteristic not to divide N. The entry/congruence calculation above is algebraic and survives there, but the unit-modulus normalization and Tadej's stated unitary theorem do not. Therefore the external comparison is an exact complex specialization plus a qualified nonmatch in stated field scope; it is not external priority clearance for arbitrary splitting fields.

The source describes symmetries, not a charged Fourier evaluator. A selected monomial has N nonzero entries, but field/root acquisition, representation, gauge application, each repeated occurrence and routing costs are separate. The full dense commutant is not classified by this owner. No free unrelated gauge insertion, arbitrary interstage routing, finite-word stability, FFT speedup or unrestricted lower bound follows.

### Closure recommendation

The current primary-comparison stop is met. The guarded theorem record can be CLOSED after independent acceptance of this mapping and its exact proposal, without upgrading its numerical priority42 or worldwide-priority status. This does not close neighboring gauge, curvature or routing records. A specific later counterexample, requested extension or distinct named source can reopen work; an unspecified comparison is no longer a pending task.

## 3. M-RECTANGLE-TILING

### Source and exact cost model

Primary: Josh Alman, Yunfeng Guan and Ashwin Padaki, *Smaller Low-Depth Circuits for Kronecker Powers*, [arXiv:2211.05217v1](https://arxiv.org/pdf/2211.05217v1). Section 1, printed p.1 defines size as wires and synchronous size as summed factor nonzeros. Equation (1.1), p.4 expresses a depth-two transform as rank-one summands. Theorem 1.4, p.5 gives sub-N^(3/2) size for powers of a fixed q-by-q matrix over a field; Theorem 1.6, p.6 specializes to the Walsh–Hadamard matrix with size O(N^1.443).

These primary statements establish the comparison's actual objective and two theorem domains. They do not require the rank-one summands to have disjoint supports or to agree individually with the target on their support, and their fixed-base tensor-power assumption is material.

### Exact endpoint-count mapping, with feasibility preserved

Let the owner have a disjoint partition of all N^2 positions into nonempty rank-one rectangles `R_t x C_t`, with a_t=|R_t| and b_t=|C_t|. Factor the target restriction as a nonzero outer product, and extend both factors by zeros to N-vectors `u_t,v_t`. Then

`F = sum_t u_t v_t^T = U V^T`,

`nnz(U)+nnz(V) = sum_t(a_t+b_t)`.

This is an exact equality of the owner's endpoint objective and depth-two wire size for the constructed circuit, not merely an asymptotic analogy. It works over the owner's splitting field and does not use norms. A summand's support is exactly `R_t x C_t`, and because the rectangles are disjoint, exactly one summand contributes to every target entry. There is no overlap cancellation.

Conversely, a depth-two factorization whose nonzero outer-product supports form that disjoint partition automatically induces the owner's rank-one tiling, and its wire count is the same incidence sum. Thus the feasible classes coincide **only after** imposing the owner's disjoint-support constraint. General depth-two factorizations allow several gates to contribute to the same entry; neither individual summand nor its support need be a rank-one restriction of the target. The subgroup-envelope proof's premise is then unavailable. In particular, this comparison is not merely the old observation about shared deeper Cooley–Tukey computations: even at depth two, changing the summand support/cancellation rules changes the optimization problem.

The accepted divisor optimum

`C_tile(F_N)=N min_(d|N)(d+N/d)`

is therefore the minimum of the primary wire objective over a restricted feasible subset. One may infer `C_depth2(F_N)<=C_tile(F_N)`, not equality or a lower bound for the larger class.

### Theorem-domain nonmatch

For a fixed q>1 and n>1, `F_q^(tensor n)` is the character table of `(Z/qZ)^n`, whereas `F_(q^n)` is the character table of `Z/(q^n)Z`. The first group has exponent q and the second exponent q^n, so they are not isomorphic. Tadej Lemma 4.22/Corollary 4.5 additionally identify Fourier-matrix monomial equivalence with isomorphism of the indexing groups. Thus a same-size tensor-power circuit theorem cannot silently be substituted for the cyclic theorem. A concrete example is `F_2 tensor F_2` versus F_4. This observation is about the stated Fourier/monomial model, not arbitrary invertible basis changes.

Consequently AGP Theorem 1.4 does not supply the exact cyclic all-N divisor formula, its optimal constant, or the prime value N(N+1). Theorem 1.6 is an instructive compatible-field Walsh example of the larger circuit class; it is not a cyclic prime/composite theorem. The primary comparison is a qualified objective match and feasible-class/family nonmatch. It neither refutes the owner's exact optimum nor establishes that this optimum was historically new.

For the same reason, none of this settles the owner's higher-rank disjoint-tile objective `sum_t r_t(a_t+b_t)` for general nonsquare composite N. That explicit Z50 obligation remains OPEN. The already accepted complex stable-rank lower bound, square case and characteristic-zero prime full-minor case are not re-proved or counted anew.

### Paid-work and source-accounting limits

Wires are not a complete cold-execution invoice. Preserve supplied-root assumptions; prime/field discovery, root tables, integer indexing, allocation, storage, I/O and word/bit/numerical costs are not supplied by a wire-size theorem. The owner's saved qualification remains: direct first-term initialization realizes its scalar ledger; the literal old loop adds zero once per tile and executes N extra additions. No old program or MILP was run. Numerical MILP status is not a proof certificate. No implementation repair is proposed.

## 4. Primary access, identity and limited failed lead

The primary texts were read through the web PDF text extractor at the pinned version URLs. Visual PDF screenshots returned cache-miss errors. A single direct local fetch of the Tadej PDF returned HTTP403 and no bytes; it was not retried. Therefore no primary-PDF byte possession, PDF digest or visual-facsimile inspection is claimed. The mathematical formulas in the comparison were re-derived entrywise to avoid depending on stripped overbars or inverse permutation conventions in extraction.

A bounded auxiliary lead was checked but not used for a theorem claim: Pudlak's *A Note On the Use of Determinant...*, [ECCC TR98-042](https://eccc.weizmann.ac.il/eccc-reports/1998/TR98-042/index.html). Its linked six-page body and two-page comment were extractable only as garbled character codes, and screenshot recovery also failed. Secondary summaries were not substituted for the unreadable theorem. That unsuccessful lead is not the selected comparison's evidence or an attribution conclusion.

The repository audits were fetched at the baseline SHA. Their original source-archive hashes, historical member hashes and current sanitized-export bytes remain distinct. The rectangle audit's original historical member label `795e4df...` is not assumed to equal its sanitized-export digest `ed3a259...` recorded in the workbook. `SOURCE_IDENTITIES.json` records actual local UTF-8 snapshot digests separately. No original archive bytes were reconstructed or claimed.

## 5. Proposed state delta

`PROPOSAL.json` contains 23 exact single-cell before/after values with predecessor history retained. `LOCAL_VALIDATION.json` confirms all 23 preimages against the captured native snapshot, 22 verbatim history suffixes, one status change, no formula/priority changes and both repository Git blob identities. The proposal is eligible for separate independent review. No proposal cell may be applied without a fresh exact-before preflight. No numeric priority, historical assessment band, formula, row identity, old source locator or theorem body is to be changed. If centralizer closure is accepted, only that record changes status; the tiling parent remains open. Counts would become 70 closed / 257 open, subject to unrelated concurrent accepted changes and a fresh workbook rebuild.
