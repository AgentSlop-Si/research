# Qtorus intake audit and three orientation boundary obstruction

Audit date: 12 October 2026 UTC. Original source filenames dated 13 October 2026 are retained unchanged.

## Result

The most actionable newly recovered source is the Qtorus phase-bridge archive. Its two-orientation impossibility theorem is sound in the stated prime-power grammar. A stronger restricted theorem follows from a different pair of frontier minors: **the same three additive orientations, even with independent arbitrary nonzero complex input/output diagonal gains on every branch, cannot be monomially equivalent to the Fourier matrix when m is any prime power at least 5 and N=m².**

Independent symbolic review accepted this restricted theorem on 12 October 2026. The reviewer separately derived the frontier argument and checked all translated support/exponent identities for m=5 through 40, totaling 44,220 minor checks. The acceptance is scoped to this mathematical argument; ordinary external peer review and historical priority remain separate. It is a restricted representation obstruction, not a general Fourier complexity lower bound or a completed fast-transform algorithm. External historical priority is unassessed.

The third orientation in the source genuinely repairs the source's original 2N witnesses. It does not repair the different 2N witnesses below. Those statements are compatible. In particular, the source's suggested continuation to N=64 and 256 with these same three orientations and higher-conductor diagonal gains is excluded. Its N=16 two-full-spark example lies outside the new m>=5 restriction and remains a valid finite structural control; 2-full-spark does not itself prove Fourier membership.

## Sources and bounded inspection

Three supplied archives were inspected. All 40 entries across their supplied manifests match their exact bytes. Uploaded code was read as inert text only, never imported, run, compiled, or deserialized. In particular, the PR622 pickle was not opened.

1. **Source ID QTORUS-CONNECTED-MINOR-20261013.** [FFT_Qtorus_Phase_Bridge_2026-10-13.zip](sources/FFT_Qtorus_Phase_Bridge_2026-10-13.zip). ZIP SHA-256 `0cc2147504a83677b16ee9f3f0cb57b62ebe20bb28120167a54b82444f59c690`. Main `RESEARCH.md` SHA-256 `17ac34b2c88530c51682f81a936992d36dd25cb1cf0f802f2f2e505068ccb24a`. Complete main text read, especially Sections 1–3 and the proposed next step. Original connected-minor and three-orientation checkers/results inspected statically. Thirteen manifest members verified.
2. **Source ID PR622-REPACKING-CANDIDATE-20261013.** [FFT_PR622_Repacking_Candidate_2026-10-13.zip](sources/FFT_PR622_Repacking_Candidate_2026-10-13.zip). ZIP SHA-256 `afb3280fda31e1a26e72d4dabf7870b9433ceef366114e66151be5e85ef4a05a`. `README.txt` SHA-256 `b571967e8d9c55d5729c0659d457986e38926ba4b288e6fdd1df80b6ace42bc0`. README and source inventory were triaged initially; the comparison JSON, profiles and two pinned primary-source EXPECTED files were then checked in the separate comparison supplement. Twenty-one original manifest members were verified. This source expressly withdraws algorithmic novelty, states that its native-complex saving is weaker than PR623's reported saving, and leaves full upstream admission and all-size FFT transfer uncompleted. Its references are to CrocSwap/integer-mult-bounds PR622/623/624, not AgentSlop-Si/research PR622. Owner-map legality remains unreviewed; the separate comparison supplement gives the exact moment evidence.
3. **Source ID Q2-DENSE-TORUS-20261013.** [FFT_Chain_Recovered_Phase_Q2_2026-10-13.zip](sources/FFT_Chain_Recovered_Phase_Q2_2026-10-13.zip). ZIP SHA-256 `dd8fa0bd6e7c6016922f1f5ab64ea81bcb80931b9f18df15a35dc9db88140e60`. `THEOREM.md` SHA-256 `ff6f36d2da31a41058eeec1fef664930b711ed31a39a338f9c514dcfc550d7f6`. README and full theorem read; six manifest members verified. The explicit dense well-conditioned transform is explicitly non-Fourier. Stationary-Q minimal-polynomial evidence is finite-size. Its complete solver and stationary-Q artifacts were not independently audited or replayed here.

The original ZIP archives are included under `sources/`. `intake_source_manifest_verification.json` records all checked member names and hashes.

## Audited source theorem

Let the grid be V=(Z/mZ)². For each branch t let q_t be a primitive complex m-th root and

- (Ax)[a,c] = x[a-1,c]
- (B_t x)[a,c] = q_t^a x[a,c-1]
- G_t = (I-alpha_t A-beta_t B_t)^(-1)
- alpha_t beta_t != 0 and 1-alpha_t^m-beta_t^m != 0.

The root-of-unity q-binomial identity gives the exact entry, for canonical differences u=(a-a') mod m, v=(c-c') mod m,

G_t[(a,c),(a',c')] = K_t alpha_t^u beta_t^v [u+v choose u]_(q_t) q_t^(a'v) if u+v<m, and zero otherwise,

where K_t=(1-alpha_t^m-beta_t^m)^(-1). All supported coefficients are nonzero.

Use the permutation convention (P_theta x)[theta(z)]=x[z], so (P_theta^(-1) G P_theta)[x,y]=G[theta(x),theta(y)]. Define phi(a,c)=(-c,a+c) mod m. The source's two-term sum is L_0G_0R_0 + L_1P_phi^(-1)G_1P_phi R_1 with independent invertible diagonal gains.

The source displays zero 2x2 minors whose row edges are (0,1) and (1,-1), at every grid translate, for m>=4. On each minor one branch is zero and the remaining branch has geometric rank one; the arbitrary branch gains preserve the zero determinant. Those edges generate V. For N=p^d, a Fourier zero 2x2 minor on distinct rows r,r' and distinct columns j,j' means N divides (r'-r)(j'-j), hence p divides r'-r. No permutation of all N Fourier row labels can assign one residue class modulo p to every vertex of a connected graph. This proves the source's stated two-orientation exclusion for prime-power m>=4, uniformly in all admitted parameters and branch gauges.

## New three orientation theorem

Define psi(a,c)=(a+c,a) mod m and

S = L_0 G_0 R_0 + L_1 P_phi^(-1) G_1 P_phi R_1 + L_2 P_psi^(-1) G_2 P_psi R_2,

with the preceding independent branch parameters and arbitrary invertible complex diagonal L_t,R_t.

**Theorem.** For every integer m>=5, the following two translated families are identically zero 2x2 minors of S. Consequently, for every prime-power m>=5, no outer invertible monomial matrices U,V can satisfy USV=F_(m²). The branch diagonals and alpha/beta parameters may contain higher-conductor phases; the obstruction is structural and does not require them to belong to Q(zeta_m).

### Frontier identity

For a primitive m-th root q and 0<=k<=m-1,

b_k = [m-1 choose k]_q = product_(j=1..k) (1-q^(m-j))/(1-q^j) = (-1)^k q^(-k(k+1)/2).

Therefore b_k²=q b_(k-1)b_(k+1) for 1<=k<=m-2. This identity is exact over C. The product denominators are nonzero because q is primitive.

### Horizontal witness

For every a,c mod m choose

R_H = ((a,c),(a,c+1)),
C_H = ((a+1,c+2),(a+1,c+3)).

Original-coordinate differences have u=m-1 and v values m-2,m-3,m-1,m-2. Therefore the identity branch is zero at all four entries.

After phi the (u,v) tables are

u_phi = ((2,3),(1,2)),
v_phi = ((m-3,m-4),(m-2,m-3)).

Their sums are all m-1, so every phi-branch entry is nonzero. After psi the differences have first coordinate v_original-1 and second coordinate m-1. Since v_original>=m-3>=2, their sums are at least m and the psi branch is zero at all four entries.

Thus only the phi branch contributes. Its Gaussian-binomial diagonal/off-diagonal product ratio is b_2²/(b_3 b_1)=q_1. Its phase ratio is q_1^(-1): integer representatives for the transformed input first coordinates are s_0=-(c+2), s_1=-(c+3), and the diagonal-minus-off-diagonal exponent is s_1-s_0=-1. The alpha and beta powers have the same total exponent in both products. K_1 and all independent diagonal gains cancel. The two determinant terms are equal and det S[R_H,C_H]=0.

### Diagonal witness

For every a,c mod m choose

R_D = ((a,c),(a+1,c-1)),
C_D = ((a+3,c-2),(a+4,c-3)).

Original-coordinate differences are

u_0 = ((m-3,m-4),(m-2,m-3)),
v_0 = ((2,3),(1,2)).

Every sum is m-1. Under phi the second difference coordinate is m-1 and the first is m-v_0>=1, so the phi branch is zero. Under psi the first difference coordinate is m-1 and the second is u_0>=1, so the psi branch is zero. Only the identity branch contributes.

Its Gaussian-binomial ratio is b_(m-3)²/(b_(m-4)b_(m-2))=q_0. Input first-coordinate representatives are t_0=a+3,t_1=a+4. The phase exponent difference is 2t_0+2t_1-3t_1-t_0=t_0-t_1=-1, giving q_0^(-1). All other factors cancel, so det S[R_D,C_D]=0.

### Wrap and Fourier equivalence

All displayed u,v lie in their canonical range for m>=5. Replacing a,c or an input first-coordinate representative by that value plus a multiple of m changes no root power. Thus the proof covers every wraparound translate, not only interior rectangles. Each row pair and each column pair consists of distinct coordinates.

The row directions remain (0,1) and (1,-1); they generate V. The source's connected-graph Fourier contradiction now applies unchanged for prime-power m. This completes the proof.

### Exact scope

- Covers precisely the three additive orientations identity, phi, psi with one canonical constant-coefficient two-direction q-torus resolvent per branch and independent nonzero left/right diagonal gains.
- Allows different primitive m-th roots for different branches, arbitrary nonzero complex alpha/beta values with invertibility denominators, arbitrary high-conductor branch gauges, and arbitrary outer monomial equivalence.
- Does not cover additional orientations, general weighted torus edges, non-diagonal interstage maps, products of sums, or arbitrary Fourier circuits.
- The structural zero witnesses exist for every m>=5. The Fourier contradiction asserted here needs m to be a prime power. For m with several distinct prime divisors, a Fourier zero-row graph can itself be connected.
- Does not exclude the m=4/N=16 three-orientation grammar. No finite N16 fitted point can yield an all-prime-power family using this unchanged grammar because m=8/N=64 is excluded.
- No practical runtime, bit complexity, stability of an implementation, lower bound on unrestricted arithmetic, all-size Fourier synthesis, or novelty conclusion follows.

## Fresh independent finite checks

`intake_qtorus_independent_check.py` was written during this audit. It imports only Python standard-library modules and imports/executes none of the supplied programs. It uses the Gaussian product formula, whereas the supplied connected-minor checker uses a Pascal recurrence. It directly checks the sparse residual (I-alpha A-beta B)G=I against the independently generated entries for all basis columns at m<=16. It uses distinct primitive branch roots and independent nonzero left/right gains.

Tested m values: 4,5,6,7,8,9,10,16,25,27,32. The prime fields and exact roots are explicitly checked and recorded per case. Results:

- 272,313 exact sparse-inverse residual entries
- 6,010 original two-orientation zero minors
- 5,978 new three-orientation zero minors
- 47,824 pure-zero excluded-branch entry checks
- 5,978 deliberate one-entry perturbations correctly destroy the zero determinant
- Connected row graph has all m² vertices in every case
- Nonprimitive q=1 rejected
- At m=4, the proposed new three-term witness has nonzero determinant 432780 in the recorded field, showing the m>=5 guard is substantive
- A separate N=36 Fourier zero-row graph generated by differences 2 and 3 is connected, illustrating why the prime-power gate cannot be silently removed.

Finite computations support the symbolic proof; they do not replace it. They are not a replay of the uploaded test harness, and do not establish every numerical claim in that source.

Checker SHA-256: `6cdf1d7e16b8010aa56afb8623641ad705d4116df1bdd118669f8ea41ea7f7f6`.

Results SHA-256: `b18583626b21dfe33e78860d11cd11360a99cb288b05f177b55970c278423660`.

Manifest receipt SHA-256: `c7c7c5172e4038e3dc11c69ce0d31e525bde567aa5bf77a4c653910a9e08d969`.

## Status and priority recommendations

**Research consequence: QTORUS-CONNECTED-MINOR-20261013.** The accepted `three-orientation-boundary` continuation closes the frozen three-orientation route negatively. Its same-family N64/256 target must be replaced by an explicit grammar-escape requirement. Other architectures remain open; no new canonical theorem registration, discovery recount, or general Fourier algorithm follows.

**Strongest next research check:** a candidate must change the three-orientation additive grammar before investing in Fourier phase fitting beyond N16. Require it to identify exactly which new branch or non-diagonal product fills the two frontier witness families above, then prove full Fourier covariance and normalization on all basis inputs. Filling these minors alone remains insufficient. No assertion is made that a fourth orientation or product will succeed.

**Q2 source boundary: Q2-DENSE-TORUS-20261013.** The solver-domain documentation correction is separately accepted in `q2_solver_guard_audit.md` and `q2_independent_review.md`; the broader executor and stationary-annihilator audit remain pending. The row-by-row solver displayed in Section 2 inverts I-beta q^a S, so that particular formula needs beta^m !=1 as well as 1-alpha^m-beta^m !=0; general invertibility of the full torus operator alone does not authorize that elimination order. The fixed alpha=beta=1/4 dense construction satisfies the extra guard, so this is a general solver-interface clarification, not a counterexample to its displayed schedule. The separate guard supplement proves the corrected statement and an exact counterexample to the wider elimination domain. Preserve exact-scalar and supplied-root assumptions, and do not treat bounded spectral condition as a bit-cost theorem.

**Repacking source boundary: PR622-REPACKING-CANDIDATE-20261013.** Lower priority for the novelty objective because the corrected source itself reports stronger comparable PR623 work. Its finite legal-placement assertions remain pending. The separate `pr622_comparison_audit.md` and `pr622_independent_review.md` accept the source-pinned threshold order PR623 > candidate > PR624. The fresh checker performs eight exact rational evaluations; the independent review checks the mathematical comparison and interval bounds, not a second numerical reconstruction. This narrower result does not certify map legality. The unchanged-provider full upstream admission, controller, routes, invoice and all-size transfer remain separate open gates. No claim that the source's finite inequalities are false is made.

These source identities do not represent three accepted canonical discoveries. Claims beyond the listed restricted obstruction, Q2 documentation correction and numerical-profile comparison remain outside independent acceptance here, including the Qtorus cost executor, Galois theorem, full experimental totals, Q2 stationary certificates and repacking owner maps.

## Independent review binding

The separate review is `qtorus_independent_review.md`, SHA-256 `fbba661c06619ec8fd9edc1eae182f6edbfca02bd0df7f815734247576ba921c`. Its independent control source is `review_qtorus_frontier.py`; its result `qtorus_independent_review_controls.json` has SHA-256 `3082c46fd25a9597d1f7276243d5cfa22331b2f6cc92cfe87e84902782ae836a`. The accepted scope is exactly the new three-orientation theorem above. The source's two-orientation theorem is directly subsumed for m>=5 and separately checked at m=4. No unrelated source experiment, Galois theorem, all-size implementation, or novelty statement is promoted by this review.

## Dated supplementary closures

The Q2 `solver-domain-documentation` obligation and PR622 `pinned-profile-ordering` obligation were independently accepted on 12 October 2026 at their exact bounded scopes. The Q2 solver program and stationary certificates, PR622 owner maps and all-size pipeline, and worldwide novelty remain unreviewed here. Original source archives remain unchanged.
