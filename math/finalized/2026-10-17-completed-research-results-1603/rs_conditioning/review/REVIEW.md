# Independent final-stage review: compact RS conditioning obstruction

17 October 2026. Verdict: **SCOPED ACCEPT. No mandatory mathematical repair.**

This review was started after the candidate was declared ready. It checks the exact frozen candidate, not an earlier draft, and does not infer completion of a broader research owner.

## 1. Frozen input and scope

Candidate directory in this publication: `../source/`.

- `PROOF.md` SHA-256: `33a1f1ac507f745d152a34ba6b1545d6bc4db867250c54d3dcda642d740d77d5`.
- `MANIFEST.json` SHA-256: `34091161d95a471ed1f2468211e3c59e9f80baa0f312470c92d6a2c62f31b4ad`.
- All eight manifest entries match both declared byte counts and SHA-256 values.
- The two copied source documents were read in full. Their local bytes match the source pins and manifest. Remote GitHub source contents were not re-fetched in this review.

The source alignment is correct: canonical positive embedding q=exp(2πi/N), N=2h≥4, c_j=q^[j(j−1)/2], coefficient convention P_n[j]=(c_n/c_j)R_n[j], pencil B_t=zP_h+tP_(h−1), degree m=h+1, and the unscaled square moment matrix V[j,i]=α_i^j for j=0,…,h. The compact acceptance source explicitly uses this same unscaled matrix and the 2N-point grid {k/(2N):1≤k≤2N}. The candidate does not silently change to a reduced-residue matrix, a normalized Vandermonde, or another primitive embedding.

## 2. Exact identity: accepted

The candidate's coefficient proof is valid for every even N≥4, including N=4:

- q^h=−1 and q²≠1 imply S_1=2/(1−q), S_2=0.
- R_h's top coefficients are 1, −S_1, S_1²/2.
- The multipliers at degrees h−1 and h−2 are −q^(−1) and q^(−3), respectively.
- The monic tP_(h−1) adds exactly t to the coefficient of z^(m−2), while leaving the coefficient of z^(m−1) unchanged.
- Thus the first two nonleading coefficients of B_t are a=2q^(−1)/(1−q) and b=2q^(−3)/(1−q)²+t. Newton's identity gives a²−2b=−4q^(−3)/(1−q)−2t.

Newton's identity counts roots with multiplicity and needs no squarefreeness. Both the phase q^(−3) and the parameter sign −2t are correct.

### Independent all-degree trace derivation

The inherited three-term recurrence has b_n=q^(3n−3)(q^n−1). Comparing the coefficient of z^(n−1) in the defining P_n gives p_n=−q^(n−1)(1−q^n)/(1−q). Consequently the diagonal coefficient is

a_n=p_n−p_(n+1)=q^(n−1)((1+q)q^n−1), including a_0=1.

Let J be the (h+1)-square tridiagonal matrix with diagonal a_0,…,a_(h−1),0, unit superdiagonal, and subdiagonal b_1,…,b_(h−1),−t. Its leading-principal determinant recurrence gives det(zI−J)=zP_h+tP_(h−1)=B_t. Hence, even if J is not diagonalizable,

Σ α_i²=tr(J²)=Σ_(n=0)^(h−1) a_n²+2Σ_(n=1)^(h−1)b_n−2t.

Set G_r=Σ_(n=0)^(h−1)q^(rn). The t-independent part is

q^(−3)[(q(1+q)²+2)G_4−2(q(1+q)+1)G_3+qG_2].

Here G_2=0 and G_3=2/(1−q³). For N>4, G_4=0. For N=4, its coefficient q(1+q)²+2=(q²+1)(q+2) is zero. Thus in all admitted cases the expression reduces to −4q^(−3)(1+q+q²)/(1−q³)=−4q^(−3)/(1−q). This independently confirms the all-N identity, including the small exceptional geometric-sum case.

## 3. Spectral inequality: accepted

The root-radius estimate uses only inequalities in the correct direction:

mρ² ≥ Σ|α_i|² ≥ |Σα_i²| ≥ 4/|1−q|−2|t|.

For the fixed canonical q, |1−q|=2sin(π/N). Therefore ρ²≥A_N(T) when |t|≤T and A_N(T)>0.

The matrix is m by m, with m=h+1 rows and columns. A column with node modulus ρ contains the last entry α_i^h, so σ_max(V)≥ρ^h. Separately, applying V* to the first coordinate unit vector gives the all-ones vector, hence σ_min(V)=σ_min(V*)≤sqrt(m). Dividing yields

κ₂(V)≥ρ^h/sqrt(m)≥A_N(T)^(h/2)/sqrt(m).

This argument correctly bounds the smallest singular value from above. It does not confuse a determinant bound with a singular value. Adding the elementary lower bound 1 is legitimate.

If roots repeat, two columns coincide and V is singular. Under the stated convention κ₂(V)=∞ all inequalities remain true. Zero nodes or forbidden resonant nodes need not be excluded for this obstruction; the accepted legal bank subset is already covered. The proof does not remove roots whose bank residues happen to vanish.

## 4. Constants and asymptotics: accepted

The rational comparison is exact:

7N/11−2−(9/8)(N/2+1)=13N/176−25/8.

At N=44 this equals 1/8, and its slope is 13/176>0. Combining sin(π/N)≤π/N with π<22/7 gives A_N(1)>9/8 for every N≥44. Since h/2=N/4, the claimed bound follows with the correct exponent and denominator:

κ₂(V)≥max{1,(9/8)^(N/4)/sqrt(N/2+1)}.

The threshold is a convenient sufficient threshold, not a claimed optimum. The bound's nontrivial term can be below 1 near the threshold, which is explicitly acknowledged in the candidate.

Also A_N(1)→4/π. Taking logarithms, dividing by N, and using log(m)/N→0 gives liminf logκ₂(V_N)/N≥(1/4)log(4/π)>0. Singular lengths pose no difficulty with the extended value ∞. Replacing 1 by |t_N|=o(N) leaves the same limit. This is a genuine exponential-growth lower bound and rules out a uniform polynomial bound for any sequence of compact-grid selections.

## 5. Compact coverage and justified negative stopping scope

Every accepted parameter k/(2N), 1≤k≤2N, lies in (0,1]. The lower bound covers every complex parameter in the entire closed unit disk, so it covers every legal grid member regardless of how selected. No universal legality of the first grid point is needed. The proof therefore resolves the exact question of obtaining polynomial conditioning through compact-parameter selection alone in the fixed pencil and fixed unscaled coordinates. Additional search over that same parameter set cannot overturn the theorem.

The negative resolution does not establish any of the following, and the candidate correctly leaves all of them open:

- Conditioning in rescaled coordinates, a new polynomial basis, or another pencil.
- Polynomial-bit preparation, or impossibility of such preparation.
- Actual worst-case sensitivity for the one fixed chirp right-hand side.
- A production executor, practical FFT comparison, or general algorithmic lower bound.
- Exact h-pole optimality or the condition of a reduced-residue system.
- Other primitive embeddings or separate Q08 obligations.
- Whole-owner closure, discovery priority, or external novelty.

The candidate's distinction between exponential condition number and bit complexity is essential and correct: exponentially large κ can still cost only linearly many additional bits through logκ. Its worst-case right-hand-side sensitivity construction is also correct for freely chosen right-hand sides, and is expressly not applied to the fixed chirp right-hand side.

## 6. Fresh controls and evidence boundaries

`independent_controls.py` was written for this review. It imports installed general-purpose libraries only. No candidate, author, or historical executable was imported or run. The candidate script was inspected as inert text; its finite-case counts and described evidence scope are consistent with its result file.

Completed independent controls:

1. Verified the two requested frozen hashes and all eight manifest members.
2. Used exact integer-polynomial/cyclotomic arithmetic on the recurrence-trace formula for every even N=4,…,256: 127 cases. This is a different exact route from the author's direct product/coefficient construction.
3. Rejected a wrong q^(−2) phase and wrong +2t parameter sign at every checked N.
4. Verified the affine threshold comparison symbolically, including its exact margin at 44 and positive slope, rather than extrapolating a finite sweep.
5. Exercised the singular-value inequalities on five independently chosen real/complex node sets, including a zero node and an exact repeated-column singular case. The SVD values are sanity checks only; the repeated-column singularity is exact.

The all-degree proofs, not these finite controls, establish the theorem. No numerical root enclosure, production implementation, or practical performance certificate is claimed. No external write was made, and the candidate directory was not modified.

## 7. Final disposition

**Accept the compact-family polynomial-conditioning target as negatively resolved, at the exact model and scope above.** No mathematical correction is required before recording that bounded outcome. Preserve the broader unresolved obligations and do not mark FUS-06, NF-03, or Q20 wholly closed on this basis.
