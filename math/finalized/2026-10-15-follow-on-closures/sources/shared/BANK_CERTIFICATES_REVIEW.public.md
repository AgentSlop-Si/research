# Independent audit of the three remaining bounded bank certificates

Date: 2026-10-10 UTC. Verdict: **all three dependencies accepted within their stated bounded scopes**. No substantive algebraic correction is required. The orientation of the P-interface actions, the F4 splitting/distinct-root conditions, and the global Hamiltonian lifting caveat are explicit conditions of this acceptance.

## 1. Scope, provenance, and independence

The governing closure is `coverage_audit_20261010/LATEST_SOURCE_REVIEW_CLOSURE.json`, SHA-256 `1f372b3f09288fa17728b864ceb1f09ab695874653fbf65dccfdba7f15c941ba`.

Reviewed exactly:

1. `MONOMIAL_WEYL_BATCH_CLASSIFICATION.md`, §§7–8 only. §§1–6 remain accepted by the earlier audit and are not resealed here.
2. `FOURIER4_GREEN_KERNEL_AND_FOURIER8_CHART.md`, including its field, cost, and batch-lifting conditions.
3. `FOURIER8_NONCOMMUTING_ANCHOR_CERTIFICATE.md`, including its exact eight-chart quantifier and positive controls.

The source reports, companion JSON data, source programs, and manifests match every digest in the governing closure. Source programs were **not executed, imported, or read as algorithm text**. Their bytes were read only for hashing. Fresh programs in this directory independently construct the target matrices and necessary equations; source JSON is untrusted certificate data to be checked, not a verdict oracle. The projective gate's formulas and forest method were independently rederived; its full 2-SAT solver is neither assumed nor rerun.

All original reports, manifests, seals, accepted predecessors, and the original closure remain unchanged. The unrelated baseline transcription erratum is preserved unchanged. This audit does not verify the source literature/provenance paragraphs, reopen previous seals, claim FFT novelty, or infer an unrestricted Fourier-8 negative.

## 2. Claim-by-claim acceptance: monomial classification §§7–8

### M7.1. Whole-bank block routing — ACCEPTED

Let B be a direct sum of q copies of F_m, with a compatible primitive m-th root and characteristic not dividing m. If T and B T B^{-1} are monomial, a nonzero block T_bc is initially only partial monomial. Every row of F_m T_bc is nonzero: a used column receives exactly one nonzero contribution. Right multiplication by F_m^{-1} preserves the nonzeroness of each row. The symmetric argument through T_bc F_m^{-1} proves that every column of F_m T_bc F_m^{-1} is nonzero.

A block of a global monomial matrix has at most one entry per row and column. Thus the transformed nonzero block has exactly m entries and rank m. Rank preservation forces T_bc to have rank m, hence m entries. The global row/column uniqueness then routes entire banks by a permutation. This proof needs neither a prime modulus nor a Fourier-minor theorem.

### M7.2. Affine/character blocks for composite m — ACCEPTED

Write ζ=ω_N^{N/m}, U e_j=c_j e_{π(j)}, V e_k=d_k e_{τ(k)}, and F_m U=V F_m. At row τ(k), the entry equation is

    c_j ζ^{τ(k)π(j)} = d_k ζ^{kj}.

Its cross ratio with j=0 and k=0 gives

    kj = (τ(k)-τ(0))(π(j)-π(0)) mod m.

For m>1, k=j=1 makes the two differences multiplicative inverses in Z/mZ. Therefore π(j)=a j+b with a a unit, and

    c_j/c_0 = ζ^{-τ(0) a j}.

The m=1 case is separately trivial. No division by a nonunit residue is hidden. The audit also verifies every affine/character block over m=4,6,8: 32,72,256 positive controls respectively. These finite tests supplement, rather than replace, the field-general proof.

### M8.1. Explicit mixed-radix bank identity — ACCEPTED

Use compatible roots ω_d=ω_N^{N/d}, N=a m b, and the source's input/output digit routes. The exponent in P B Q is

    r_0(t_2+b t_1)+m b r_0 t_0+a b r_1 t_1+a r_1 t_2+a m r_2 t_2.

It equals `(t_2+b t_1+b m t_0)(r_0+a r_1+a m r_2)` modulo N. All other terms in the expansion are multiples of N. For each input/output pair, the sparse routes specify one relevant bank path; the coefficient is exactly ω_N^{kj}. Thus the identity holds algebraically over the supplied-root field, not merely in the tested examples. P and Q have row/column support a and b respectively and are monomial-equivalent to their stated Fourier batches.

### M8.2. Correctly oriented four monomial actions — ACCEPTED WITH EXPLICIT ORIENTATION

The actual actions are

    Q S Q^{-1}, Q D Q^{-1}, P^{-1} D P, P^{-1} S^{-1} P.

The P-side assertion should be read through H=P^T, as in the accepted §6, rather than replacing it by arbitrary conjugations P S P^{-1} and P D P^{-1}.

For Q, on output coordinates (r_0,t_2,r_1), Q S Q^{-1} reads the predecessor with r_0 decreased by one. At r_0=0 it instead reads (a-1,t_2,r_1-1 mod m), with nonzero multiplier ω_{mb}^{t_2}; otherwise the multiplier is 1. Q D Q^{-1} reads (r_0,t_2+1 mod b,r_1), with multiplier ω_N^{r_0}, and an additional factor ω_m^{r_1} exactly when t_2=b-1. These formulas include a=1, b=1, and the carry boundaries.

For P^T, exchange a and b in the Q construction, permute its output coordinates, and multiply output (r_0,t_2,t_1) by ω_N^{r_0 t_2}. This yields exactly P^T. Output monomials preserve monomial conjugates. Transposition gives the two displayed P-side actions. This supplies the missing explicit orientation detail without changing the source conclusion.

### M8.3. Four zero-mask layers and endpoint N=256 — ACCEPTED

For d=4, the audit constructs the standard factorization

    F_4 = H_{(0,2),(1,3)} diag(1,1,1,i)
          H_{(0,1),(2,3)} R_bit_reverse.

Each butterfly stage is a sum of two nonsingular monomials. F_2 requires one stage, and F_1 no stages; padding by I=(1/2)I+(1/2)I produces exactly two layers per exterior. Characteristic is odd in the dyadic setting, so the padding is legal. Input/output routes and twiddles are absorbed into the endpoints. Each zero mask may be placed on any Hamiltonian cycle and has guard 1.

Fresh controls verify all 45 combinations a,b in {1,2,4}, m in {1,2,4,8,16}, including every exterior factor and all eight nonsingular monomial summands. Six extra cases cover odd and mixed-composite digit sizes, for 51 exact bank identities total. The N=64, m=q=8, a=4,b=2 and N=256, m=q=16, a=b=4 controls pass with all four actual actions monomial.

The q≤16 statement applies to four **zero-mask** paired layers: each has row support at most 2, giving support at most 16m after the bank. Every Fourier entry is nonzero, so N≤16m. N=256 attains the square-bank endpoint. This is not a nonzero-Green lower bound.

### M8.4. Costs — ACCEPTED

Routes, compatible-root power tables, and twiddles require O(N) preparation and application once the root is supplied. Actual transform work remains

    (N/a)T(a)+(N/m)T(m)+(N/b)T(b)+O(N).

Fixed a,b≤4 provide ordinary fixed-radix recursion. The positive controls' primitive-root searches and dense comparison matrices are charged research verification, not part of the claimed O(N) preparation. This does not turn growing Fourier batches, arbitrary interface recovery, or coefficient discovery into free work.

## 3. Claim-by-claim acceptance: F4 and commuting F8

### F4.1. Field and distinct-root guards — ACCEPTED, NONVACUOUS

The field must contain primitive χ of order 8 and both distinct roots r,s of z²+h z+i, where i=χ² and h=χ+χ^{-1}; characteristic is not 2. Supplying χ alone does not guarantee splitting. With a=χ^{-1}, h²=2 and ha=1-i. The discriminant is 2-4i.

An additional independent singular-branch control is F25=F5[t]/(t²-2), χ=2t. Here χ has exact order 8, i=3, h=t, and the quadratic has the single repeated root r=s=2t. The Green guard itself is 1-r⁴=2, nonzero; it is the coefficient interpolation denominator r-s that fails. The stipulated distinct-root condition correctly rejects this case. The audit does not assert that no alternative F4 kernel exists in this field.

All four primitive eighth roots in each of 11 prime fields were checked: 20 split/distinct positives and 24 missing-split cases. Root extraction or extension construction remains separately chargeable.

### F4.2. One local paired-Green layer — ACCEPTED

The sequence `[1,a,-1,a]` satisfies c_{t+2}=-h c_{t+1}-i c_t for t=0,1. A+B=1 and Ar+Bs=a give c_t=A r^t+B s^t at all four indices. Geometric cyclic inversion gives

    (1-r⁴)(I-rS_4)^{-1}=Σ_{t=0}^3 r^t S_4^t.

The chirp sequence is 4-periodic. Multiplying its circulant on both sides by E=diag(χ^{j²}) produces entry χ^{u²+v²-(u-v)²}=i^{uv}. This is precisely the unnormalized positive F4, with the source's two branch coefficients.

### F4.3. Masks, endpoints, denominators — ACCEPTED

Since rs=i, both masks are nonzero. Since

    r⁴+s⁴=2-8i, r⁴s⁴=1,
    (1-r⁴)(1-s⁴)=8i,

each Green denominator is nonzero in odd characteristic. Further, a²+ha+i=1-i≠0, so a differs from both roots and A,B are nonzero. Both full left endpoints A(1-r⁴)E and B(1-s⁴)E and right endpoint E are nonsingular. The local identity has all eight edge masks nonzero. Repeated roots are not silently covered by taking a limit.

### F8C. Two commuting unshifted scalar-resolvent pairs after fixed chirps — ACCEPTED

Each permitted layer has numerator degree at most 1 and denominator degree at most 2. Their product forces C(z)D(z)=A(z) mod z⁸-1 with deg D≤4, D(0)=1, deg A≤2. Repeated poles, zero poles, and degenerate numerators still satisfy these bounds; denominator guards are needed to derive the identity.

For k=3,…,7 and j=0,…,4, the coefficient matrix is c_{k-j}=χ^{-k²}χ^{-j²}ω^{kj}. Removing nonzero row/column factors leaves a Vandermonde matrix on 1,ω,…,ω⁴. Its nodes are distinct over any allowed supplied-root field. Therefore the homogeneous constraints force D=0, contradicting D(0)=1. Six finite-field checks additionally verify the determinant including all chirp factors.

Only this exact fixed-chirp, common-cycle, scalar-endpoint, unshifted-numerator chart is empty. Independent endpoint diagonals, varying masks, numerator shifts, interstage twists, and different orders are outside the exclusion.

### LIFT. Local cyclic kernels do not automatically lift — ACCEPTED

A direct sum of the local F4 cyclic inverses has disjoint 4-cycles. It cannot simply be relabeled into a single Hamiltonian N-cycle. The source provides no stitching/cancellation certificate with the same branch budget and all masks, endpoints, guards, and application costs. Thus the local F4 kernel remains a finite positive control and does not replace a global batch evaluator. The same obligation survives any future local F8 kernel.

## 4. Claim-by-claim acceptance: noncommuting F8 anchors

### F8N.1. Full coefficient grammar and fraction-free system — ACCEPTED

For an eight-cycle π and nonsingular diagonal endpoints, inversion of a Green branch has exactly the support `diag(a)+diag(b)P_π`. Conversely, when every a_i≠0,

    Q^{-1}=(I-diag(-b_i/a_i)P_π)^{-1} diag(a_i^{-1}).

The determinant is δ=∏a_i-∏b_i for an even cycle. Its nonzero guard and all eight a_i≠0 are essential. Some b_i may be zero in this bounded chart; all-nonzero masks would be a smaller chart.

Four branches have 64 scalar coefficients. Introducing X1,X2 yields 192 variables and 192 equations as stated. Under branch guards, Q0 X Q1=Q0+Q1 uniquely gives X=Q0^{-1}+Q1^{-1}; X2 X1=F8 forces both X factors invertible. The eight-parameter interstage diagonal gauge preserves the grammar. None of these counts proves existence or nonexistence. Extra endpoint permutations need their own specified support tables.

### F8N.2. Linear scale completion — ACCEPTED, CONDITIONAL ON SUPPLIED DIRECTIONS

For Q0=D_ρ U and Q1=V D_τ, multiply Q0 B Q1=Q0+Q1 by D_ρ^{-1} and D_τ^{-1}. The result is

    U B V = U D_y + D_x V,
    (UBV)_{ij}=U_{ij}y_j+V_{ij}x_i.

This is linear in the 2N scales only after both direction families are known. It requires nonzero x,y, invertible U,V, nonzero base entries, all off-support equations, and a full guarded identity check. The row gate alone does not reconstruct shared column directions. O(N²) target-entry work and a conservative O(N³) scale solve are appropriate construction charges. Positive controls here verify the complete 64-entry scale equation, not just its supported positions.

### F8N.3. Legal anchors — ACCEPTED

Both specified pairings give K²=2I. The two global Hamiltonian visit orders retain only opposite matching edges, of weights 1/2 and -1/3. Their nilpotent parts square to zero, all connecting masks are zero, and guards are 1. The left endpoints 2I and diag(-1 on a,-3 on b) are nonsingular over Q(ζ8). Expanding each pair gives [[1,1],[1,-1]]. Thus X1=K legally forces X2=F8 K/2. No freely variable outer diagonal or first-layer coefficient is included in this anchor fixation.

### F8N.4. All eight exact bounded rejections — ACCEPTED

Arithmetic uses the exact field Q[z]/(z⁴+1); irreducibility follows from Eisenstein at 2 after replacing z by z+1. Every eligible triple, target block, transition, transition rank, forest path, tree transform, and recorded internal quadratic was rebuilt from F8 K. Using F8 K instead of F8 K/2 only rescales the homogeneous equations. The audit checks all **690 transitions** and **395 nonzero internal quadratics**, including rank-one and rank-zero cases. No singular transition is inverted. The adjugate reverse maps are used only on rank-two edges. All projective axes, including infinity, are retained.

For the adjacent anchor, the verified nonzero commutator determinants, in basis (1,ζ,ζ²,ζ³), are:

- (natural, bit_reverse): (-1120,-1024,-320,576)
- (natural, gray): (48,32,32,32)
- (evens_odds, gray): (44,36,0,-36)
- (bit_reverse, gray): (44,36,0,-36)

The source return maps were independently reconstructed up to nonzero projective scale; their recorded determinants were then recomputed exactly. A common eigenline would be in the commutator kernel, so each nonzero determinant is a valid rejection over every extension of Q(ζ8).

For the half anchor:

- (natural, gray): source edges 2 and 13 force respectively (ζ-ζ³)y²=0 and -ζ²x²=0. No projective point survives.
- (evens_odds, gray) and (bit_reverse, gray): source edges 1 and 2 force (-1+ζ²)x²=0 and (-ζ+ζ³)y²=0. Each already contradicts projective nonzeroness within one forest component, irrespective of the other components.
- (natural, bit_reverse): edge 1 forces (-ζ-ζ³)xy=0. Both axes satisfy every internal quadratic. Axis (1,0) makes the base coefficient zero in rows 1,3,5,7; axis (0,1) makes it zero in rows 0,2,4,6. Thus this chart is rejected **only after the nonsingular diagonal-endpoint guard** is applied. It is not a direction-system contradiction and does not exclude that singular-endpoint boundary.

The first seven cases reject nonzero projective directions already. No free-first-layer, unlisted order-pair, endpoint-permutation, or unrestricted two-layer conclusion follows.

### F8N.5. Four positive controls — ACCEPTED

For each specified order pair, the independent audit forms the exact rational sum of `(I-2P_π)^{-1}` and `(I-3P_σ)^{-1}` by finite geometric series. It verifies both inverse identities, the full cleared matrix identity, the scale-completion identity, and all 345 eligible projective equations on the genuine row direction (1,-2). Guards are -255 and -6560. None is rejected. These positive controls exercise the gate without relying on numerical fitting or the constructor's output verdicts.

### F8N.6. Cost and quantifier boundary — ACCEPTED

Four supplied length-8 inverse branches can be applied by guarded cyclic recurrences in O(8) arithmetic. Finding/representing their coefficients is separate work. The eight negative charts do not settle the free 64-coefficient problem, and a local positive F8 still needs an explicit global Hamiltonian batch lift before use as a full-bank exterior.

## 5. Useful constructive implication, separately certified

The accepted mixed-radix family can be upgraded from zero masks to **nonzero matching masks** on all four actual butterfly layers when a=b=4. This is a small, exact corollary, not a lift of the all-nonzero F4 cyclic kernel.

For each ordered butterfly pair (u,v), choose α outside {0,1,-1}; a primitive fourth root works in every dyadic field. Put weight α^{-1} on v→u in the first Hamiltonian order and weight (-1-α)^{-1} on u→v in the second. Set every connecting edge to zero. Then

    H_pair = αI (I-α^{-1}E_uv)^{-1}
             + diag(1-α,-1-α)(I-(-1-α)^{-1}E_vu)^{-1}.

The two nilpotent masks square to zero. Ordering all pairs as v0,u0,v1,u1,… and u0,v0,u1,v1,… gives two genuine global Hamiltonian cycles, each with N/2 nonzero mask edges and guard 1. Twiddles, bit reversal, and the outer routes are absorbed in nonsingular monomial endpoints, preserving the two-layer budget per exterior.

`CONSTRUCTIVE_MATCHING_CONTROLS.json` supplies complete numeric Hamiltonian orders, every nonzero mask, all endpoint row/column/weight arrays, and full bank checks over F65537 for:

- N=128, m=8, q=16, a=b=4: all eight branches have 64 nonzero matching edges.
- N=256, m=q=16, a=b=4: all eight branches have 128 nonzero matching edges.

Every guard is 1 and both full Fourier identities pass. The formulas generate these arrays in O(N). This gives a useful broader positive control for future constructors, but no increased radix compression, no fully nonzero Hamiltonian masks, and no growing-size Fourier speedup. The all-nonzero local F4 kernel still has its separate lifting obligation.

## 6. Reproduction and closure

Run only the newly authored audit programs:

    python independent_audit.py
    python constructive_matching_extension.py

They require only the Python standard library and the sealed source JSON/paths; the second imports only this directory's first program. Both completed successfully. `INDEPENDENT_CONTROLS.json` and `CONSTRUCTIVE_MATCHING_CONTROLS.json` contain the exact outcomes. `CLAIM_VERDICTS.json` records machine-readable per-claim boundaries. `CLOSURE_ADDENDUM.json` closes precisely these three pending dependencies, without modifying the original closure. The directory manifest and detached seal bind these deliverables and all source fingerprints.
