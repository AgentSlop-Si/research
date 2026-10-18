# M-NONLINEAR-COMPATIBILITY: actual full-rank profiles still do not determine coefficient compatibility

17 October 2026. Bounded proof and primary-source comparison candidate. No external writes were made by this worker.

## Result and recommended disposition

The named Koetter–Médard 2003 comparison is complete at the scope below. A fresh finite witness strengthens the previously recorded graph-capacity separation: **one explicit integer matrix in the fixed N=8 separated-generator family has every one of its 12,869 nonempty square minors nonzero, while the complex closure of that same matrix family has dimension exactly 60 in dimension 64.** Thus even the full collection of actual rectangular ranks does not characterize the family.

Recommend accepting this bounded theorem and comparison after independent review, but **retain M-NONLINEAR-COMPATIBILITY as TO RESEARCH at its existing priority**. The fixed Fourier target-fiber problem is not solved. Neither a Fourier factorization nor a Fourier-excluding polynomial is produced. The general principle that graph cuts need not guarantee compatible prescribed coefficients is classical; no worldwide-priority or runtime claim is made.

## 1. Exact scope and evidence

The pinned source is the 9 October independent audit linked by the current index at commit `e3f3fd2fde808e577989907f00740c16905dbeb1`. Its exact URL, Git blob SHA and the primary source locators are in `SOURCE_BINDING.json`.

Work over the complex numbers unless another field is stated. Index rows and columns by 0,...,7. Each scalar separated-generator stage is

    S[i,i] = d[i],
    S[i,j] = l[i] m[j] if i > j,
    S[i,j] = u[i] v[j] if i < j.

Each stage has 40 displayed parameters; four endpoint parameters are unobservable. The two-stage polynomial map is

    Phi(A,B) = B P A,
    p = [7,0,6,3,4,1,2,5],  P e_j = e_(p[j]).

This is the rank-one separated-generator chart, not a claim about every quasiseparable chart, Green-resolvent architecture, or an arbitrary linear circuit. The permutation convention is fixed explicitly by the entry formula Phi[i,j] = sum_k B[i,p[k]] A[k,j]. The older audit did not print that convention beside its permutation; the present certificate is a standalone certificate for the convention just displayed. Reversing the convention gives the transposed-family equivalent after swapping/transposing stages, so dimension and existence of a totally nonsingular member are unchanged, but the printed integer witness belongs to the displayed convention only.

The historical graph max-flow census, N=16 tangent witness, higher-rank claims and historical seed are not rerun or newly certified here. All present executable mathematics is freshly authored in `check.py`, using the Python standard library only. No historical program is imported or executed.

## 2. Fresh exact certificate

The 80 parameters are generated deterministically by a printed SHA-256 recipe and then stored explicitly in `RESULTS.json`. There is no random search. The result contains the full integer 8-by-8 product matrix and an explicit 60-by-60 Jacobian minor.

Running `python3 check.py` produces:

- Nonempty square minors by size: 64, 784, 3,136, 4,900, 3,136, 784, 64, 1.
- Total: 12,869. Vanishing minors: zero.
- Every minor is evaluated twice: exact integer Bareiss elimination and modular Gaussian elimination modulo the prime 1,000,000,007. The exact determinant reduced modulo the prime equals the independently computed residue in every case.
- Both stages are invertible: their determinant residues are 898,768,723 and 396,706,915.
- The 64-by-80 Jacobian has modular rank 60. Its listed 60-by-60 minor has determinant residue **696,549,753**.
- All 80 coordinate derivative checks pass exactly. Each parameter appears affinely in Phi, so a unit coordinate difference is the exact polynomial derivative; a separate two-unit difference verifies the affine dependence at the test point.

The checker also verifies primality by trial division. Ordered exact-determinant and modular-residue digests, parameter values, matrix entries and Jacobian row/column indices are recorded. This is an executable finite certificate, not a machine-formalized proof. The theoretical deductions from the exact checks follow next.

## 3. Proof of the claimed separation

### 3.1 Dimension upper bound

For the lower triangle, the observable factors are l[1],...,l[7] and m[0],...,m[6]. On the dense locus where these are nonzero, the products l[i]m[j] for i>j determine all 14 factors up to one common reciprocal scaling. Indeed, the bipartite incidence graph i>j is connected: l[7] meets every observable m[j], and m[0] meets every observable l[i]. The lower-triangle image therefore has dimension 13. The independent upper triangle has dimension 13, and the diagonal has dimension 8. The closure of the single-stage image is irreducible of dimension 34.

The invertible-stage locus is nonempty (it contains diagonal invertible stages) and is Zariski open, hence dense. For an invertible diagonal D, the transformation

    A -> D A,
    B -> B P D^(-1) P^(-1)

preserves the stage charts and B P A. This is a free 8-dimensional torus action when A is invertible. Thus every generic product fiber has dimension at least 8, and the image dimension is at most 2*34-8=60. The domain is irreducible, so the closure of the image of its dense invertible open locus is the full image closure. Singular/limiting choices do not increase this upper bound.

### 3.2 Dimension lower bound

The displayed Jacobian minor is an integer determinant nonzero modulo 1,000,000,007. It is therefore a nonzero integer. Over characteristic zero the polynomial map has differential rank at least 60 at this integer parameter point, so its image closure has dimension at least 60. Together with the upper bound, the dimension is exactly 60.

This deduction uses a nonzero modular determinant to prove nonzero characteristic-zero determinant; it does not transfer finite-field point emptiness to complex emptiness.

### 3.3 Actual rank-profile insufficiency

Let V be the 60-dimensional complex image closure. Let U be the open subset of all 8-by-8 matrices whose nonempty square minors are all nonzero. The fresh integer matrix lies in V intersect U. Hence V intersect U is nonempty and has dimension 60, whereas U has dimension 64. In particular U minus V is nonempty and dense in U.

Every matrix in U has the same complete rectangular rank profile: a nonempty R-by-C submatrix has rank min(|R|,|C|). The certified member of the family and all matrices in U minus V share this profile. The latter matrices cannot be realized by the family. Consequently any test whose only information is the ranks of all coordinate submatrices cannot characterize coefficient realizability for this fixed family.

Equivalently, no individual coordinate minor vanishes identically on the family. Its unavoidable algebraic equations cannot be recovered merely by adding more coordinate-minor rank-zero tests. This does **not** say that arbitrary polynomial combinations of minors are powerless; such combinations can express additional compatibility equations.

This theorem is stronger than graph-capacity survival in its finite witness, but it does not decide the Fourier target: F_8 has some vanishing proper minors and need not share this full-rank profile. The witness establishes capacity attainment and the limitation of rank-only characterization, not F_8 membership or nonmembership.

## 4. Named primary-source comparison

Primary source: R. Koetter and M. Médard, *An Algebraic Approach to Network Coding*, IEEE/ACM Transactions on Networking 11(5), 782–795 (2003), DOI 10.1109/TNET.2003.818197, [author-hosted PDF](https://www.mit.edu/~medard/mpapers/networkcoding.pdf).

Theorem 3 (p.787) expresses acyclic linear-network transfer through polynomial path gains. Theorem 4 and its proof (p.788) obtain simultaneous multicast invertibility by a product of nonzero determinant polynomials, followed by sink decoding. Example 3 and Theorem 6 (p.789) distinguish cut feasibility from compatible interference constraints. Theorem 7 (p.790) characterizes solvability through a proper polynomial ideal.

Mapping: our acyclic scans also give a polynomial transfer map; the fresh minor product is nonzero. However, prescribing all entries of B P A equals F_8 is different from requesting decodable multicast. A free dense sink decoder would alter the allowed architecture and require its own computation. The paper does not establish this fixed permutation, dimension 60, chart-specific gauges, or Fourier membership. Its finite-field communication setting also does not automatically provide complex fixed-target coefficients or arithmetic/bit-cost bounds. Verdict: **classical mechanism overlap and a qualified nonmatch to the precise finite chart theorem**. Exact printed antecedence of this chart-specific result and worldwide priority remain unassessed.

The primary body was read via its author-hosted PDF text. Screenshot attempts for printed pp.789–790 returned cache errors, so whole-PDF visual verification is not claimed. No algorithmic-complexity hardness result from the paper is transferred to this fixed N=8 task.

## 5. Exact missing Fourier gate

This paragraph is a self-contained formulation for the chosen fixed chart. Set K=Q(zeta_8), with zeta_8 a primitive eighth root, and F[i,j]=zeta_8^(i*j), using the unnormalized Fourier convention. With theta the 80 displayed variables, define

    I_F = < Phi(theta)[i,j] - zeta_8^(i*j) : 0 <= i,j < 8 >
          in K[theta].

The exact fixed-chart complex feasibility question is whether I_F is a proper ideal. By the algebraically closed-field Nullstellensatz, properness is equivalent to an all-entry solution over the algebraic closure of K, and hence to one over C. It is not equivalent to finding a solution in K itself. Since F and P are invertible, any exact solution automatically has invertible A and B; no extra saturation by det(A)det(B) is needed for this chart. Any additional nonzero-parameter, unit-modulus, finite-field or pole restrictions would define a different guarded problem and must be imposed separately.

Two valid bounded outcomes would be:

1. Give explicit algebraic coefficients and check all 64 entry equations; or
2. Give a certificate 1 in I_F, or a polynomial h vanishing identically on the image with h(F) nonzero.

The second kind of h excludes even the image closure. Failure to find such an h does not prove actual image membership, because a polynomial image need not be closed. A Jacobian normal at one point also does not exclude all other target preimages.

If endpoint permutations or another middle permutation are permitted, each explicitly allowed branch needs its own target equations. Diagonal endpoint scalings absorb into this chart; arbitrary permutations produce a finite union and preserve the dimension upper bound, but do not eliminate the branchwise target obligation.

## 6. Boundary and next action

Close the named comparison and the fresh fixed-N full-rank-profile witness gate after independent acceptance. Keep the owner open. A genuine successor must select and settle an actual target-fiber branch, or identify a distinct primary theorem with an exact architecture mapping. Do not rerun the old graph-capacity census merely to strengthen a coefficient-existence claim.

There is no uniform construction, all-N theorem, lower bound on arithmetic work, numerical stability estimate, coefficient-bit bound, cheaper Fourier evaluation, implementation qualification or novelty promotion here. Computing a matrix in this fixed chart costs linear work per stage using prefix/suffix sums once coefficients are supplied; that fact does not synthesize Fourier coefficients or account for solving the target equations.
