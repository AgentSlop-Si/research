Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: ae5450d760e1b2922efe2d840b97dd3c0728e0db85a5e6f1d8c1594e505c5f6a

---

# Independent review: corrected Weil convention/API

Date: 2026-10-11 UTC. Verdict: **INDEPENDENT ACCEPT, bounded exact implementation-consistency gate**.

Accepted candidate: `Weil_Convention_API_Candidate_2026-10-11.zip`, SHA-256 `51f2ae033138859f5d7c30b3692e7c29d664dfdf5028b0ebe66226fa14fe59ae`.

## Result and scope

No blocking mathematical or implementation defect was found in the candidate's stated bounded API. The reviewer independently reconstructed all **795 positive operator certificates** and the **one expected wrong-sign rejection**, and matched their full certificate records. The author assertion ledger reconciles to 1,286. Separately authored reviewer controls pass **9,635 assertions**, including **850 independently audited operators**.

This accepts the fresh negative-chirp implementation and its frozen finite-field rejection interface. It does not accept the historical uploaded programs unchanged, certify their original exhaustive runs, certify a numerical production implementation, decide novelty, prove a faster FFT, or prove a lower bound for unrestricted arithmetic circuits or mixed Green/Weil architectures. The NF01 function returns only rejection or inconclusive, never an equivalence certificate.

## Independent method and provenance

Only the candidate's freshly authored `src/weil_exact.py` was imported, after static review. No uploaded original, original test driver, or inert text extract was executed, imported, or AST-parsed. The reviewer did not run the author's candidate driver; its cold record is identified explicitly as author evidence.

The separate reviewer implementation constructs full Fourier matrices and their algebraic inverses, diagonal chirps, coordinate permutation matrices, and explicit Heisenberg matrices. Upper shears are built by direct matrix products, independently of the candidate's difference-cached Gauss sums. Small ring inverses use determinant/adjugate formulas, independently of the candidate's unit-pivot elimination. Word products, covariance, rank, image cardinalities, row/column support, and the dense Bruhat expression are independently recomputed.

Integer-residue arithmetic is exact. NumPy 2.3.5 supplies integer matrix multiplication; a signed 64-bit overflow bound is checked before every such product, with reduction after every product. The finite test contexts keep other intermediate integer array expressions safely below the signed 64-bit bound. Modular inverses and powers use Python integer arithmetic. There are no floating coefficient comparisons.

Verified provenance:

- Candidate archive byte hash and all 20 candidate manifest entries.
- All three pinned sources: P11 and the v24/v25 original archives.
- All 38 listed archive member hashes and sizes.
- All five inert source extracts byte-for-byte against their pinned originals.
- The nested v24 archive inside v25 equals the separately pinned v24 archive byte-for-byte.
- The author's cold record, all four cold log hashes, and all 20 cold extracted manifest files. Cold gate and witness logs equal the candidate evidence bytes. This corroborates reproducibility but is not relabelled as independent reviewer execution.

See `evidence/provenance_checks.json` and `evidence/author_cold_record_verified.json`.

## Mathematical and API findings

1. **Convention.** For positive Fourier kernel, centered Heisenberg phases, and positive lower chirp, W inverse L(E) W equals U(-E). The coherent U(E) operator is F inverse C(-E) F. The API implements that rule. The q=3, coefficient field F7 witness independently yields diagonal/off-diagonal values 4/2 for the corrected operator and 3/6 for the historical sign. The historical sign fails U(1) covariance despite full support and passes the relabelled U(-1) covariance. A scalar cannot repair this label mismatch. Candidate sources: `src/weil_exact.py:148–195`; proof lines 9–24 and 67–75. The untouched historical v25 source retains its positive-chirp formula at inert source lines 122–141.

2. **Covariance and uniqueness.** The explicit centered Heisenberg matrices reproduce the candidate's intertwiner test. Checking the 2n translation/modulation generators suffices because they generate the full Heisenberg system with the same central cocycle under a symplectic map. Primitivity separates coordinate characters; hence commuting with all modulations forces diagonality and commuting with translations forces a scalar. Invertibility is independently verified, excluding a spurious zero intertwiner. Candidate sources: `src/weil_exact.py:213–246`; proof lines 30–39.

3. **Exact support.** The annihilator and shift arguments prove every row has a nonempty coset of im(B transpose), every column has a nonempty coset of im(B), and both counts equal |im B|. This is valid over the stated odd local ring and the stated coefficient field. The API enumerates the image, rather than replacing it by rank modulo p. Independent row and column counts agree in every audited operator. The complex constant-modulus statement is separate from finite-field computation. Candidate proof lines 43–49.

4. **Dense Bruhat.** The block factorization L(DB inverse) G(-B) W L(B inverse A), and kernel cross term minus x transpose B inverse-transpose y, are correct. Three nonsymmetric-B controls specifically distinguish inverse-transpose placement. Every dense audited operator has one nonzero global scalar relating it to this kernel. Singular B is correctly rejected by the dense-kernel API. Candidate source lines 206–211; proof lines 53–63.

5. **Valuations and identity.** For nonzero b=p^v u, g=p^v, r=q/g, the support is x=y modulo g. Each residue block has scalar r inverse G(-u/2) times eta^((Y-X)^2/(2u)); its local primitive rectangle ratio is eta^(-u inverse), of order r. The product of opposite quadratic Gauss sums equals r in the coefficient field, which is nonzero, so the scalar cannot vanish there. The zero case is exactly identity, with no distinct-row/distinct-column nonzero rectangle. Tensor products and E=M D M transpose congruence are consistent. No general symmetric congruence diagonalizer is provided or certified. Candidate source lines 248–263; proof lines 79–91.

6. **Word closure and rank.** The listed application order agrees between operators and symplectic labels. The word API permits only L, U, G, W and partial W. The mod-p subadditive B-rank bound and coordinate-Fourier attainment are valid structural facts. They do not imply an unrestricted arithmetic lower bound. Candidate source lines 172–204; proof lines 95–97.

7. **NF01.** The API fixes a prime coefficient field, full square dimension N, primitive Nth target root, and invertible external row/column monomial equivalence. A zero entry excludes a dense cyclic Fourier target. Anchored ratios annihilated by a proper divisor e of N imply every rectangle ratio is annihilated by e, excluding the target's primitive Nth ratio. Row/column scaling and permutations preserve the complete ratio set. Every other result is inconclusive. The code also correctly validates root order and exponent divisibility. It does not implement the separate inverse-support or anchored-rank stages described as possible extensions in P11, and this bounded acceptance does not claim it does. No invariant propagation through arbitrary sums or products is supplied. Candidate source lines 284–319; proof lines 99–101.

8. **Domain controls.** The reviewed entry points are `ExactWeil` construction and its generator/word/verification/valuation/dense-cell methods, plus `fourier_rejection_gate`, on their documented typed inputs. The defaults cap dense operator dimension at 125; caller overrides, primality/root preparation, and bit complexity remain charged. This is an audit API, not a hardened arbitrary-input service or a performance claim. Odd prime-power coordinates and prime-field coefficients are distinct domains. Primitive qth roots are mandatory; finite-field conclusions are not silently transferred to complex absolute values or arbitrary coefficient extensions.

## Coverage

The independent reconstruction includes every one of the 795 source positive certificates and the expected negative, comprising the frozen controls, 77 scalar valuation cases, all 27 symmetric 2-by-2 shears over F3, six diagonal plus six mixed-congruence cases, 552 individual word generators, 122 complete words, and three nonsymmetric-B dense cases. Full displacement covariance is tested for the frozen cases and all 27 tensor shears, matching source scope.

Additional reviewer coverage includes:

- All 49 scalar shear parameters at q=49, rather than the source's eight selected q=49 cases.
- Three alternative coefficient-field/root contexts, and nontriangular invertible linear changes requiring a pivot permutation.
- 72 NF01 comparisons against a direct all-rectangle oracle after independent row/column permutations and nonzero scalings.
- All 1,296 nonzero 2-by-2 matrices over F7, each at both allowed exponent bounds: 2,592 NF01 checks.
- 26 invalid-input checks, coefficient mutation, zero intertwiner, wrong advertised label, nonzero projective scaling, and product-nonclosure controls.

See `evidence/reviewer_results.json` for exact counts and `src/reviewer_controls.py` for the independent program. Run from any working directory with Python and NumPy installed:

    python path/to/weil_convention_independent_review_2156/src/reviewer_controls.py

## Disposition for research records
