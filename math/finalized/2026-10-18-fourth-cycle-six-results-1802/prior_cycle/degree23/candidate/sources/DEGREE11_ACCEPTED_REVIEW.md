# Independent review: degree-eleven original Fourier-bank attainment

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**.

## Accepted results

Fix N=13, q=16, characteristic 53, the negative unnormalized target F[k,t]=16^(-kt), and the original signed-resolvent physical-bank grammar with exactly one independently free nonzero effective alpha node in each cross orientation. Let B(K) denote the minimum physical-bank count, allowing arbitrary legal beta and raw weights.

The explicit certificate proves

    B(F_(53^11))=16.

Its physical allocation is (7,1,1,7). Both seven-node same-sign supports are non-Frobenius-stable, both cross nodes are outside F53, all sixteen physical banks are nonzero, and every original branch inverse is legal. The upper bound is freshly verified directly from the original operators. The matching field-uniform lower bound is inherited from the accepted pinned source, with its exact scope checked below.

Scalar extension gives B(F_(53^d))=16 whenever 11 divides d. Together with the accepted attaining degrees 2,3,5,7, the known sufficient divisor list is now {2,3,5,7,11}. Apart from the solved base field d=1, the remaining unclassified degrees are restricted to d>1 with gcd(d,2310)=1. The smallest is **13**. This is not an iff classification and does not exclude attainment at any residual degree.

The separate prime-field-cross theorem is also accepted: when gcd(d,210)=1 and both cross nodes are required to lie in F53*, the exact minimum is **18**, even with initially arbitrary extension-valued same-sign supports. Thus any 16- or 17-bank witness in those degrees requires at least one nonbase cross node. It need not require both to be nonbase. The degree-eleven witness happens to use two nonbase cross nodes.

No broad parent closure, historical-priority determination, or FFT/runtime improvement follows.

## 1. Exact byte binding and independence

Acceptance attaches to this certificate SHA256:

    8b7264552dbc555fe1ee46359f3e19fd8c74a01a2be17c36f9aa2031eb09a25c

The accepted main REPORT.md SHA256 is:

    df8b4b763cdd6a1c5f87f9bcc56b32230689fb270e607afaf22db83ad88d617d

The accepted PRIME_CROSS_OBSTRUCTION.md SHA256 is:

    854dfac4f068dfbd5cf9d51db0620bf65ecc9bd7a23afd707e9156c43e303143

All 27 entries of the candidate manifest were checked against their complete local bytes; CANDIDATE_BINDING.json preserves those bindings. All five supplied source bodies were read, and their byte lengths, SHA256 values, and Git blob hashes match SOURCE_PINS.json. Read-only GitHub fetches at every exact repository path and commit independently returned the same blob hashes; REMOTE_SOURCE_RECEIPTS.json records those results.

Only review_check.py, freshly authored for this review, was executed. No candidate or historical program was run, imported, compiled, or evaluated. The supplied certificate and census were parsed only as inert JSON. The verifier reconstructs all arithmetic before comparing to the claimed matrix or census. It uses a third inverse construction, different from both the candidate's stated Gauss-Jordan and zero-diagonal backward-recurrence methods.

The independent computation passes again under Python isolated mode in a clean temporary directory containing only the new checker and frozen inert inputs. Mathematical receipts, the fresh 18-bank certificate, and the complete rebuilt cross census agree exactly across runs; runtime is excluded from the receipt comparison. COLD_REPLAY.json and COLD_RUN.log retain the evidence.

## 2. The field, supports, and original physical grammar

The field is K=F53[u]/(u^11+u+3), encoded in the ordered basis 1,u,...,u^10. Every input field array is checked for length eleven and canonical integer residues 0,...,52.

Before taking any extension-field inverse, generic prime-polynomial modular arithmetic establishes

    X^(53^11)=X mod (X^11+X+3),
    gcd(X^11+X+3, X^53-X)=1.

Because 11 is prime, the first equality restricts irreducible factor degrees to 1 or 11, and the gcd eliminates degree 1. The modulus is therefore irreducible and defines a field. All eleven successive Frobenius remainders are recorded in ARITHMETIC.json. Extension multiplication subsequently uses the explicit reduction u^11=-u-3, while inversion uses a separate polynomial extended-Euclidean algorithm and is checked by multiplication.

The seven supplied roots are distinct and nonzero. Their seven linear factors are multiplied out exactly and equal every coefficient of the supplied annihilator H. Their 53rd powers are computed; the resulting set differs from the original set. The supplied H has nonbase coefficients. Both orientations use precisely this root set. The cross records equal the supplied nonzero y and z, each with nonzero nonconstant coordinates. Thus the nonstability and nonbase-cross assertions concern actual elements and supports.

The operator tested is exactly

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
          (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1),

where S e_t=e_(t+1), T e_t=16^t e_t, with indices modulo thirteen. q=16 is independently checked to have exact order thirteen. Every guard is freshly recomputed as

    Delta=1-alpha^13-1=-alpha^13,

and matches the certificate while remaining nonzero. No trace, quotient-algebra bank, derivative, limiting singularity, or pre/post transform replaces this physical primitive.

## 3. Literal inverse and Fourier checks

For each of the 208 physical branches define the literal sparse matrix

    A=alpha S^epsilon+16^(epsilon*delta*j) T^delta.

The verifier forms I,A,...,A^12 by successive literal left matrix multiplication. It also forms A^13 and checks all 169 entries against (alpha^13+1)I. It constructs

    V=Delta^(-1)(I+A+...+A^12).

It then checks both (I-A)V=I and V(I-A)=I directly, entry by entry, using the two actual nonzero positions of each original row/column. Thus the geometric-series construction is not accepted merely on a formal q-binomial assertion. There are 208 inverses, 416 one-sided inverse identities, and 70,304 total scalar inverse-entry equalities, with zero failures.

Each inverse receives its supplied raw weight and the original factor 1/13. Each resulting physical-bank matrix is checked nonzero. All sixteen matrices are summed, and all 169 entries equal 16^(-kt). The claimed stored matrix is compared only after this reconstruction.

Additional independent checks establish:

- All 208 raw weights equal the forward character transform of the supplied sector amplitudes, and all 208 amplitudes are recovered by the inverse transform.
- Literal Fourier-to-Weyl extraction gives gamma=7 and all 169 normalized target coefficients 16^(10(a+b)^2).
- Literal Weyl extraction from every individual reconstructed bank matches all 2,704 predicted bank coefficients.
- All 169 actual-root sector equalities hold. Their independently computed ranks are 13,9,11,12,13,13,13,13,13,13,12,11,9.
- Omitting 1/13 gives 169 target mismatches; reversing the Fourier sign gives 144; adding one to the last raw weight gives 91.

These establish a literal original-bank identity, not merely a necessary recurrence condition or a support-splitting claim.

## 4. Lower bound and scalar extension

The pinned [accepted predecessor review](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md), section 1, explicitly binds a universal lower theorem: every characteristic-53 field and every legal beta require at least seven distinct nonzero effective nodes in each same-sign orientation, plus the two nonzero effective cross nodes. Repeated, ineffective, zero-alpha, or cancellation-only physical banks cannot reduce the physical count. Its section 2 supplies the arbitrary-beta amplitude bridge without division by beta.

That source's main theorem fixes y=z=1, but its separately stated inherited lower theorem is explicitly field-uniform and is not confined to the pinned-cross construction. It is this lower theorem, not the pinned-cross iff, that is used here. The large original lower-minor calculation is inherited and was not rerun. The new literal upper witness and this accepted lower theorem yield equality at degree eleven.

For 11|d, a finite-field embedding F_(53^11) into F_(53^d) preserves every raw parameter, nonzero guard, inverse, and matrix identity. The same lower bound applies after embedding, proving equality there. A matrix sum lying in F53 does not descend its individual raw parameters to F53. Conversely, failure of 11|d does not exclude a different witness over that field.

## 5. Prime-field cross nodes: fresh complete obstruction

This review independently reconstructs Gaussian factors from words in the two ordered operators. Right-appending S contributes the commutation factor omega^ell and right-appending T contributes one. This derives the additive coefficient recursion. All 676 reflection identities and the necessary isolated-row/support vanishings are checked.

For each y in F53*, the six forced recurrence rows are reconstructed. RREF of the complete six-by-eight homogeneous matrix gives pivot columns 0,...,5 in all 52 cases. Consequently every monic degree-seven annihilator satisfying those rows, over any extension K, lies on the affine line

    H_lambda(t)=sum_(j=0)^7 (c_j+lambda n_j)t^j,
    c6=0, c7=1, n6=1, n7=0,

with all c_j,n_j in F53. Lambda is not assumed base-valued.

For each of the 2,704 ordered nonzero prime-field pairs (y,z), the two b=3 annihilator recurrences have E_s=C F_s, s=1,2. The necessary determinant Q=E1 F2-E2 F1 is reconstructed coefficientwise in F53[lambda], without division by any parameter expression. Every complete polynomial agrees with the inert census. The counts are:

    quadratic: 2,655; linear: 47; nonzero constant: 2; zero: 0.

The constant cases are (25,28), Q=27, and (46,4), Q=30. All 143,312 evaluations at the 53 prime-field lambda values are also checked against the direct determinant as a supplementary regression; the coefficientwise computation and degree bound, not those samples alone, justify the formal equations.

If gcd(d,210)=1, d is odd. A root lambda in F_(53^d) of a nonzero polynomial of degree at most two has Frobenius orbit length dividing d and at most two, hence length one. Therefore lambda, and then all annihilator coefficients, lie in F53. Each of the seven actual roots has orbit length dividing d and at most seven; the coprimality condition again forces it to lie in F53.

For an independent final contradiction, this review freshly enumerates all 52*53 affine polynomials and evaluates all 52 possible nonzero base roots. The counts for 0,...,6 roots are (1041,1006,521,150,32,5,1); no polynomial has seven roots. This verifies the needed one-sided base obstruction anew, rather than relying only on the cited stable-support theorem. Reflection applies the same proof to the other same-sign side.

The inherited count bound implies any representation with at most 17 physical banks has a seven-node same-sign side. Therefore no such representation exists with both cross nodes in F53* at gcd(d,210)=1. This argument leaves the other support, beta values, amplitudes, and weights initially arbitrary and discards no exceptional zero-amplitude case.

For attainment, this review also reconstructs a fresh 18-bank witness from the accepted support {1,2,6,7,12,21,22,26}, cross nodes 1, and beta=1. All thirteen complete sector systems are solved over F53; raw weights are reconstructed; all 234 original branch inverses are obtained by ordinary prime-field row reduction and checked on both sides. All eighteen bank matrices are nonzero and all 169 final entries equal the original Fourier target. FRESH_BASE18_CERTIFICATE.json contains the new full raw witness. Scalar extension proves the upper bound in every required degree. Thus the restricted minimum is exactly eighteen.

## 6. Boundary, operation accounting, and deliverables

The 16-bank result closes degree eleven and its scalar extensions in the free-cross-singleton grammar. The prime-cross exclusion closes its declared family for every gcd(d,210)=1. The remaining unrestricted finite-field classification starts at degree thirteen and is restricted to degrees coprime to 2310, using the previously accepted cases documented in the pinned degree-seven source. No global nonexistence claim follows from this residual list.

The four broad parent problems remain open. Other cross allocations, other lengths or characteristics, nonstable residual-degree constructions or exclusions, and historical priority remain outside this review. No literature/priority search was performed, so no novelty claim is made.

The operation ledger correctly keeps 16 banks separate from 208 inverse branches and charges field representation, preparation, weights, and matrix evaluation. Its unoptimized prepared-matrix evaluation totals, 37,869 extension multiplications and 35,139 additions, are arithmetically correct. They are neither lower bounds nor an FFT speedup.

Files: review_check.py is the standalone fresh checker; ARITHMETIC.json stores detailed receipts; FRESH_CROSS_CENSUS.json stores every rebuilt affine line and gate; FRESH_BASE18_CERTIFICATE.json stores the supplemental literal witness; inputs/ retains only inert supplied inputs and pinned text; CANDIDATE_BINDING.json, REMOTE_SOURCE_RECEIPTS.json, and COLD_REPLAY.json record provenance and replay. No external write, commit, research-register change, or supplied-code execution occurred.

Replay from this review directory:

    python -I review_check.py inputs
