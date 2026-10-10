# A rank gate for fixed sparse defect decompositions

## Scope

This proposition is an elementary consequence of rank and nullity. It supplies a model-specific check for combining a linear interface factorization with a sparse-defect evaluator. It is not a general Fourier lower bound, and no historical novelty is claimed.

Let F be any field, let D:F^n→F^(n−1) have rank n−1, and write wt for the number of nonzero coordinates. Let C_j:F^d→F^n be fixed linear maps, j=1,…,p, with p≥1. Put M=Σ_j C_j and r=rank(M). The domain dimension d is arbitrary; the factors need not be square.

## Proposition

1. If wt(D C_j x)≤k_j for every x∈F^d, then
   rank(C_j)≤k_j+1.
   Consequently r≤Σ_j(k_j+1). With the same D on every piece, the stronger inequality is
   r≤1+Σ_j k_j.

2. Even without any uniform sparsity assumption, there is one common input x such that
   Σ_j wt(D C_j x)≥max(0,r−1).

3. Choose a linear functional ℓ:F^n→F that is nonzero on ker(D), and define E a=(ℓ(a),D a). Then E is invertible. There is one common input x such that
   Σ_j wt(E C_j x)≥r.
   This counts nonzero seed and defect coordinates together.

These statements hold over finite fields as well as infinite fields.

## Proof

A linear subspace W⊂F^m of dimension s contains a vector of weight at least s. To see this, choose a basis matrix for W and s rows forming an invertible square submatrix. Projection onto those s coordinates is onto F^s. In particular, some vector projects to (1,…,1). This argument uses no field-size assumption.

Apply this observation to im(D C_j). Uniform weight at most k_j implies rank(D C_j)≤k_j. Restricting D to im(C_j) loses at most its one-dimensional kernel, so rank(C_j)≤rank(D C_j)+1≤k_j+1. Rank subadditivity gives the first sum bound. Moreover,
r−1≤rank(D M)≤Σ_j rank(D C_j)≤Σ_j k_j,
which proves the stronger common-D bound.

Let A be the vertical stack of D C_1,…,D C_p. Summing its output blocks gives D M, so rank(A)≥rank(D M)≥r−1. The subspace observation applied to im(A) gives one input with at least max(0,r−1) nonzero stacked defect coordinates. This is a simultaneous-input statement, not a sum of separate worst cases.

Finally E has zero kernel: D a=0 implies a∈ker(D), and ℓ is nonzero on that one-dimensional space. Thus E is invertible. The stack of E C_j has the same rank as the stack of C_j. Summing the latter blocks gives M, so its rank is at least r. Applying the same observation proves part 3. ∎

## Exact connection to the q defect map

For the admitted Phase21 setting, n≥3 is odd, η is a supplied primitive 2n-th root in the actual field, and q=η^8 has order n. Define
(Da)_t=(1−q^t)a_t−η^(4t−2)a_(t−1), 1≤t<n.

All diagonal coefficients 1−q^t are nonzero. Therefore D has rank n−1, and ℓ(a)=a_0 makes E=(a_0,Da) invertible. The proposition applies in that field. The abstract proposition itself does not require roots of unity, primality, or total nonsingularity.

If a Schur factor C has rank s, some input has at least s−1 defects. A purported uniform k-defect treatment of this factor therefore requires s≤k+1. Applying this gate requires the actual factor and endpoint coordinates; a generic support graph or interface dimension alone does not specify them.

## When the cost inference is valid

Suppose every fixed piece has the same output length n and its independent evaluation, on the actual common input x, incurs at least
c n [1+wt(D C_j x)]
charged operations, where c>0 is uniform in n and j. Assume the costs of these evaluations add, with no cross-piece sharing. Then the worst-case total is at least
c n [p+max(0,r−1)]≥c n r.

Thus rank r=Ω(n) forces Ω(n²) work in this explicit model. For a separate target-size parameter N, a quadratic-in-N statement requires n=Θ(N) and r=Θ(N). Rectangular factors or low-rank targets instead give the stated Ω(nr) bound.

The accepted Phase21 forced sparse-path ledger is 20n−25+6n w per raw length-n piece with w defects and all 2n padded outputs. For n≥3 this is at least 6n(1+w), so independent use of that literal schedule meets the displayed hypothesis. This statement concerns that schedule and ledger. It does not turn its O(n(w+1)) upper bound into an intrinsic lower bound.

If an evaluator skips zero seeds or zero pieces, the fixed per-piece overhead hypothesis may fail. A separate, zero-aware version follows from part 3 only when the decoder charges at least c n per nonzero coordinate in the seed–defect expansion and costs add across all pieces. Then one common input still costs at least c n r. This coefficient-expansion model is distinct from the raw algorithm's four Horner seed evaluations.

## Boundaries and counterexamples

- An O(n(k+1)) upper bound alone implies no lower bound. Likewise, separately attained worst cases cannot simply be added: over F_2 the forms x_1, x_2, x_1+x_2 each attain weight one, but their summed weight never exceeds two. The proposition avoids this error by stacking.
- Uniform sparsity need not mean a single fixed support over a finite field. The plane spanned by (1,1,0) and (1,0,1) over F_2 has maximum weight two but uses all three coordinates. The rank proof remains valid.
- Shared cross-piece computation is outside the cost conclusion. The coordinate projections C_j=e_j e_j^T sum to the identity, which can be implemented by wires. Independently scanning/materializing every piece would impose an avoidable quadratic cost. In a transform application, aggregation before a shared transform likewise changes the model.
- Adaptive selection of factors, nonlinear decompositions, lookup or finite-word tabulation, shared recurrence updates, and cross-piece cancellation shortcuts are outside this fixed-linear, independent-evaluation conclusion. No lower bound for those broader models is asserted.
- FFT fallback does not satisfy the stated per-defect lower-cost contract on dense pieces. The Phase21 implementation's radix2/3 fallback must therefore be kept separate; its existence prevents extending this quadratic claim to the entire adaptive implementation.
- Different output lengths, defect maps of larger nullity, and unrestricted changes of coordinates require their own cost contracts. If each piece instead has its own rank-(n−1) map D_j, the individual rank bounds remain valid, but the common-D improvement need not. Stacking gives the weaker common-input defect bound max(0,r−p); fixed independent seed overhead still yields Ω(nr).

## Evidence and references

The proof is self-contained. It uses standard rank, nullspace, and coordinate-projection facts; see Gilbert Strang's [MIT lecture on the four fundamental subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-10-the-four-fundamental-subspaces/) for background.

The application uses the previously reviewed Schur v30/v31 archives and the Phase21 reciprocal q-factorial archive. Their identities and source links are recorded separately in SOURCE_PROVENANCE.json; no new Fourier-specific weight assignment or evaluator is supplied here.

Fresh exact controls exhaust the inputs of 144 small common-map cases and 27 distinct-map cases over F_2,F_3,F_5,F_7, verify the two finite-field counterexamples, and check admitted q-defect maps at (n,F)=(3,F_7),(5,F_11). These finite controls corroborate the proof and do not replace it. No submitted program was executed or imported.

