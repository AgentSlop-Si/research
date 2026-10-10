# Phase24 Woodbury construction and fully charged coverage audit

9 October 2026. Scope: Section 5 and its implementation, together with the inherited Phase23 transform conventions. The separate combinatorial-rank audit is outside this report. No submitted program, test, or archive was executed or imported. All executable files in this audit directory are independently authored.

## Result

The nonsingular Woodbury identity is correct. Its small correction matrix is always invertible, and in fact has determinant **one**, not merely a generically nonzero determinant. The advertised dense evaluation bound is a valid arithmetic upper bound after its model and zero-defect corner case are stated properly.

There are two important source-level qualifications:

1. The uploaded zero-defect branch recomputes `pow(z,n,P)` separately for every output. Under ordinary modular powering this performs Θ(N log N) multiplication work even for identity ordering. Hoisting the scalar repairs the implementation; it does not invalidate the mathematical linear executor.
2. The uploaded routine excludes every `z^N=1`. Phase23's unpermuted-character shortcut cannot simply replace that branch for arbitrary permutations. A permuted character generally has many nonzero Fourier bins.

A bounded positive improvement is independently proved and implemented here: a supplied permuted geometric sequence with `s` changed successor edges can be transformed at **every z** in **O(N(s+1)) additions/multiplications plus one field inversion**, using O(N) field/index words. This includes the resonant bin, linear permutation validation, coefficient preparation, routing, and all outputs. It uses sparse twisted differences and avoids the dense Woodbury solve. It remains a restricted-input evaluator, with field/root selection and bit arithmetic explicitly charged separately. Neither this construction nor the uploaded package supplies the requested arbitrary-fresh-input exact all-output FFT below N log N.

## 1. The identity and all nonsingular cases

Let `Z e_j=e_(j+1 mod N)`, let `P^-1 e_t=e_(L[t])`, and put `W=P^-1 Z P`. Write `x=P^-1 g(z)`, where `g(z)_t=z^t`. Since W follows the order L,

    (I-zW)x = (1-z^N)e_(L[0]).

Conjugating by the orthogonal residual C gives the source's equation (5.1). Here orthogonality is algebraic: `C^-1=C^T`. It holds for the source's finite-field cosine/sine normalization because the necessary square roots and i exist and are invertible.

If J is the set of changed successor columns, then

    W-Z = Σ_(j∈J) (e_(W(j))-e_(j+1)) e_j^T.

Thus `R_W=R+UV^T` with the source's U and V, and the sign in the Woodbury formula is positive after substituting the update `-zUV^T` into `A_z=I-zR`. No independence of the s supplied columns is required. They may be redundant.

Both W and Z are N-cycle permutation matrices. Consequently,

    det(I-zW) = det(I-zZ) = 1-z^N.

For `z^N≠1`, the base and updated resolvents are invertible. The determinant lemma gives

    det(I_s-z V^T A_z^-1 U)
      = det(I-zR_W) / det(I-zR)
      = 1.

Therefore the uploaded small linear solver cannot encounter a truly singular correction under the stated valid-input and nonroot assumptions. Pivoting is still necessary because an individual diagonal pivot can vanish. The empty correction has determinant one by convention. The case z=0 is regular and returns `Ce_(L[0])`.

The block inverse signs are correct. On a rotation block `[[c,-s],[s,c]]`, the inverse numerator is `[[1-zc,-zs],[zs,1-zc]]` and determinant `1-2zc+z²`. With a primitive Nth root and characteristic not dividing N, these block denominators are nonzero precisely when the relevant eigenvalue is not resonant; `z^N≠1` excludes them all.

## 2. The inherited singular shortcut is insufficient

The identity before inversion remains valid when `z^N=1`, but it becomes a homogeneous equation and no longer determines the vector by inverse multiplication. The source explicitly raises an error in `phase24_ordering.py:159`.

Phase23 correctly evaluates `Cg(z)` as an ordinary Fourier character. The target here is `CP^-1g(z)`. A general P does not preserve that character. For a completely explicit check over F_97, take N=8, omega=47, i=22, sqrt(N)=28, sqrt(2)=14, z=64, and

    L = [0,4,2,3,1,5,6,7].

Then `z^8=1`, but the independently computed vectors are

    Cg(z)       = [0,0,2,0,0,44,0,0],
    CP^-1g(z)   = [0,67,33,81,1,59,16,15].

Thus the Section 5 reference to a separate Phase23 spectral branch should not be read as a supplied complete branch for this permuted problem. The source's nonsingular theorem is unaffected. The construction below repairs this restricted-family coverage without pretending the ordinary character shortcut applies.

## 3. Exact all-z O(N(s+1)) construction

This section is an independent addition, not a claim about what the uploaded code already does. Work first with the unnormalized DFT

    X_k = Σ_(j=0)^(N-1) x_j omega^(kj).

Let `x_(L[t])=z^t`. Define the twisted difference `d=(I-zZ)x`. Substituting the covariance identity above gives

    d = (1-z^N)e_(L[0])
        + z Σ_(j∈J) x_j (e_(W(j))-e_(j+1)).

The support of d has size at most `2s+1`; cancellation can only reduce it. If `z^N=1`, the boundary term disappears, so the bound improves to `2s`. All coefficients are known after one O(N) pass that simultaneously constructs x and z^N. The successor and its defect set are obtained by an explicitly linear permutation validator and route construction.

Fourier covariance gives

    (1-z omega^k) X_k = D_k,
    D_k = Σ_(j∈supp d) d_j omega^(kj).

Prepare the N root powers once. For each nonzero d_j, its contribution across k is a geometric progression with step omega^j, so all numerators cost O(N(s+1)) field work. Batch inversion computes every regular denominator inverse using O(N) multiplications and **one** field inversion. Every regular output is then obtained by a multiplication.

Because omega has exact order N, at most one denominator vanishes. If it does, compute that one Fourier coefficient directly:

    X_k* = Σ_j x_j omega^(k*j).

A running power evaluates this N-term sum in O(N). No discrete logarithm, singular division, character-preservation assumption, or FFT oracle is needed. z=0 has no exceptional bin. If d vanishes identically, the directly evaluated resonant bin still supplies the missing homogeneous component.

After field/root selection, the complete arithmetic ledger is:

- validate the supplied permutation and form its successor: O(N) index operations;
- synthesize the supplied geometric input in that order, including z^N: O(N);
- identify changed edges and prepare sparse d: O(N);
- prepare root powers and denominators: O(N);
- numerator progressions: O(N(s+1));
- batch inversion: O(N) multiplications plus one inversion;
- exceptional bin, if any: O(N);
- materialize all N outputs: O(N);
- memory: O(N) field and index words.

The standalone `linear_twisted_dft.py` implements exactly this entry point:

    permuted_geometric_dft(order, z, p, omega)

It returns the unnormalized DFT and performs no dense C/R construction. It assumes p is a known odd prime and verifies the exact order of the supplied root for a dyadic N using two modular powers, costing O(log N) multiplications. If the normalized real residual is wanted, the source's O(N) parity conversion can follow, with its normalization constants separately prepared and charged.

The independence of the test harness is important: `AuditTransform` constructs dense Fourier/reference matrices and performs cubic orthogonality/covariance checks. **The test harness is not the linear executor.** The standalone entry point has no dependence on those matrices or on any submitted source.

## 4. Fully charged reading of the uploaded cost

The source's literal `O(Ns²+s³)` formula should include the empty-update baseline: `O(N(s+1)²+s³)` arithmetic and `O(N(s+1)+s²)` storage. Since s≤N, the latter is O(N(s+1)).

Coefficient generation is genuinely explicit, not a hidden full transform: one C column uses a single root exponentiation and N running powers, followed by O(N) real conversion. Constructing the seed and U/V costs O(N(s+1)), plus O((s+1)log N) powering absorbed in that bound. Forming the dense correction costs O(Ns²); elimination costs O(s³). Output formation costs O(Ns).

However, `phase24_ordering.py:166` is

    return [(1-pow(z,n,P))*q%P for q in base_seed]

so the scalar is recomputed N times when s=0. For dyadic N, ordinary binary powering takes Θ(log N) modular multiplications per call. A corrected implementation should compute the factor once before the comprehension. Positive-s output already does so at lines 180–182.

Also, `_invert_block_resolvent` uses N/2+1 separate modular inversions each time. There are s+1 such calls, plus s pivot inversions. Thus there are O(N(s+1)+s) inversions, not merely one. If division is a primitive field operation this is consistent with the arithmetic bound. If inversion is implemented by powering or Euclid, its p-dependent cost must be included. One can precompute and batch-invert common block determinants, but the submitted implementation does not do that.

Permutation validation calls `sorted(order)`. A generic comparison-sort charge is O(N log N), unlike an explicit linear validator. This alone is not proof of superlinear cost on constant-s valid inputs: those orders have at most s+2 increasing runs, and an adaptive sort can exploit that structure. The independent seen-array validator avoids relying on this subtlety and proves the linear route-preparation claim directly. The separate rank utility also sorts its permutation argument before its linear cycle scan.

The dense correction bound is an upper bound for one evaluation strategy, not a lower bound forced by rank. Indeed, the coordinate resolvent has the closed form

    (I-zZ)^-1[a,b] = z^((a-b) mod N)/(1-z^N).

Therefore every entry of the small correction and right-hand side can be prepared in O(1) after an O(N) power table, rather than by an N-term dot product. The sparse construction in Section 3 goes further and removes the small solve altogether. A large correction rank does not establish an unrestricted arithmetic-circuit lower bound.

## 5. Field, bit, precision, and fresh-input limits

The uploaded implementation uses F_998244353, with `p-1=119·2^23`. Its root guard supports exactly dyadic N from 4 through 2^23. The powers-of-two normalization constants exist because 2 is a square in this field. The matrix identities can be considered more generally over suitable fields, but the real-residual implementation additionally needs the stated primitive root and invertible sqrt(N), sqrt(2), and i. The raw DFT extension does not need square roots.

A fixed finite field supports only finitely many lengths. A uniform unbounded-N claim must specify and pay for field selection, primality/generator information, root construction, normalization, and input encoding. With known p and a suitable generator, producing omega by powering has its own O(log p) multiplication charge. The source's square-root routine and nonresidue search have additional p-dependent work. None of this is established as a uniform linear-N setup theorem by the package or this extension.

Let B=ceil(log2 p). Field multiplication/reduction and inversion act on B-bit integers and are not constant-cost bit operations when p grows. Source dot products accumulate unreduced sums with up to roughly 2B+log N bits; arbitrary oversized Python inputs also require reading/reduction proportional to their actual size. The standalone evaluator reduces each update and keeps ordinary residues bounded, but still pays the cost of modular arithmetic. A faithful bound is the stated number of field operations times their implementation cost, plus inversion, field/root preparation, index/routing costs, and input/output representation costs.

For a prime-field family containing primitive Nth roots, p≥N+1. Writing N explicit fixed-width residues therefore already entails Ω(N log N) output bits when N is unbounded. An arithmetic-operation speedup and a below-N-log-N bit bound are different goals. Compact symbolic output would be another representation model and is not the materialized vector returned here.

Over the complex numbers the identities are exact algebraic identities. They do not supply exact algebraic-number bit bounds or a certified floating-point implementation. Near resonant roots, separately formed numerators and inverses can suffer cancellation or large intermediates. Orthogonality of the final C does not by itself bound intermediate conditioning in Woodbury elimination. No precision/error or stable numerical runtime theorem is proved.

Finally, the fast evaluator assumes that L and z are supplied. If a raw input vector is also given, verifying `x_(L[t])=z^t` costs O(N), but discovering a useful order or a small-defect description for arbitrary data is a separate problem. The new routine neither reads arbitrary vectors as its unconstrained input nor proves that every vector has such a representation. At s=Θ(N), its stated cost is O(N²), not sub-N-log-N. This upper bound is not a universal lower bound either. Combining rejection with an ordinary FFT preserves O(N log N) worst-case arithmetic rather than improving it.

## 6. Exact independent controls and reproduction

Run `python independent_checks.py` from this directory. Only the Python standard library and the independently authored `linear_twisted_dft.py` are used. The uploaded files are neither read nor imported by the checker.

The final test suite covers 13 field/length configurations: primes 17, 97, 193, and 998244353; dyadic lengths 4 through 64 as allowed by each field. All 24 orders are used at N=4; other sizes include identity, cyclic rotations, reversal, adjacent/distant swaps, two swaps, and seeded arbitrary permutations. At the small primes every field element z is tested; other configurations include every singular character and selected nonroots.

Observed passing controls:

- 13 exact dense orthogonality and covariance/sign checks;
- 6,144 nonsingular Woodbury outputs compared against direct Cx;
- 6,144 correction determinants equal to one, with every small-matrix/rhs entry also checked against the closed coordinate resolvent;
- 9,600 all-z sparse outputs compared against direct Cx;
- 9,600 standalone raw-DFT outputs compared directly against an independently constructed dense DFT, as well as through real conversion;
- 3,456 singular-root cases, including every nonzero field element for N=16 over F_17;
- seven malformed-permutation rejections;
- the explicit permuted-character counterexample above.

These are bounded exact controls, not execution of the uploaded implementation, independent verification of its performance counters, or a proof by finite testing. The algebraic proof establishes the full stated family. `CHECK_RESULTS.json` and `RUN.log` record the run; `SOURCE_INPUTS.json` records inspected source hashes; `SHA256SUMS.txt` seals the deliverables.

## Final conclusion

The source's nonsingular low-rank correction is mathematically sound. The literal zero-defect implementation needs a scalar-hoisting fix, and the inherited singular-character reference needs qualification. The independent sparse twisted-difference evaluator supplies a cleaner all-z restricted-family construction with fully explicit routing and coefficient work. The arbitrary-input exact all-output FFT goal, uniform field setup, and precision/bit-complexity target remain unmet.
