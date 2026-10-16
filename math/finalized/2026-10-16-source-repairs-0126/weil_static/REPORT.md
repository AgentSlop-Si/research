# ALG-WEIL-LOCAL: separately pinned v25 upper-shear repair

Prepared 16 October 2026 UTC. Static source repair independently accepted at the exact corrected-module hash below. This publication derivative incorporates the final static-only reviewer disposition; it does not assert historical or corrected code execution. Original archive retained unchanged. No supplied or modified historical research program was imported or executed. No installation, networked execution, or exhaustive SL2 enumeration was performed by this repair.

## Result and scope

The derivative consistently implements the labelled upper shear U(b) as F^-1 C_(-b) F, with positive-exponent F[x,y]=zeta^(xy) and C_b[x,x]=zeta^(b x²/2). The original positive-chirp implementation represented U(-b). Merely comparing support sizes or root orders could not detect that error.

The patch corrects all three primary numerical formulas, the separately supplied verifier's Gauss sum, exact signed-cross-ratio assertions, operator labels in the mathematical documentation, and regression tests. It adds negative-chirp and wrong-sign controls, every-scalar q=9 formula/normalization tests, and Weyl-displacement covariance tests that identify the group action. The derivative contains 13 test groups; they remain unrun in this static pass. All five Python files parse as Python syntax, which is not execution acceptance.

The complete original v25 archive remains the immutable history, SHA-256 `f8fbf4c58e95202665326bc7e66bc2da859502d38225a4d5ce3b42c043a00d15`. Its primary module hash is `dd0047554b2884c8ff1f62bb696c82d512825ac881dfd66d20828b746e5dd9d1`. The corrected module hash is `259b8047681ea555152e31c921f13653964cdcb09cc4a9ba9d40f4b2dc56266e`. The textual patch hash is `dd89f7681a5a8eca77d0951437d76dc7710df79149a723c9b1bb4f1759022c82`. Every original and derivative file is separately bound in SOURCE_BINDINGS.json.

## Owner and accepted-evidence boundary

The complete current owning rows were read: Catalogue 28, novelity breakthough 53, and Research overview 70 in the existing research workbook (private workbook link omitted from this publication derivative). They identify ALG-WEIL-LOCAL, priority 42, status TO RESEARCH, and explicitly separate the already accepted bounded fresh API from the untouched historical v25 implementation defect and the unrun original exhaustive suites.

The original RESEARCH.md, checkpoint, prior-art statement, primary module, test suite, separate verifier and driver were read fully as inert source. Their exact byte identities are retained. The original documentation hashes are `36a9e3ffe024621eaec00a746526a19e2d12fbbd289bf087c86810c4d3c0caa8`, `ba59028a517b2be5e776231867d00222694860e718ed1852c4beb5d224443fb4`, and `2c289af43194929a7308196a1f8ca4cd4a97e56b00e977ca5852a323fa34b8f9` respectively.

The prior accepted bounded API and review are recorded with archive hash `a206af8dc4aa68faf2ebdb6406c0be854b4ca692ac5805b8bdd0ccc3705f4f52`, review hash `ae5450d760e1b2922efe2d840b97dd3c0728e0db85a5e6f1d8c1594e505c5f6a`, and candidate hash `51f2ae033138859f5d7c30b3692e7c29d664dfdf5028b0ebe66226fa14fe59ae`. Those bytes were not recovered by the bounded lookup available to this repair. Their status remains recorded-unrecovered. No body reread, prior-certificate reconstruction, or prior execution replay is claimed. This repair is justified directly from the original formulas and fresh controls, and does not replace or silently revalidate that earlier API.

Subsequent bounded source recovery found and fully read a verified sanitized publication derivative of that earlier review, [at immutable repository commit 877bd407](https://github.com/AgentSlop-Si/research/blob/877bd407be43845d453286e4d1406a7b15844631/math/reviewed_rounds/2026-10-12-reviewed-research/weil-convention-api.md). It is 9,893 bytes, published SHA-256 `72f630c55bdec7a02f833a0af12662a7b0cceb07f266833b0787f8e99f67c611`, Git blob `50ba2bc9ae04020fe65bf4fbd70e39a688e86f02`. Its canonical publication manifest marks derivative=true and one private-reference edit. The bounded prior acceptance and limitations are therefore readable as a publication derivative. The three exact original bodies above remain unrecovered; this is not byte-identical original recovery or execution replay.

## Uniform static justification

Let p be an odd prime, q=p^k, k>=1, and let the coefficient field have characteristic different from p and contain a primitive q-th root zeta. All inverse integers in the formulas below are interpreted in their stated ring or coefficient field. No assertion is made for p=2, a nonprimitive root, or a noninvertible q.

With W=[[0,-1],[1,0]] and L(c)=[[1,0],[c,1]], direct 2-by-2 multiplication gives W^-1 L(-b) W=[[1,b],[0,1]]=U(b). Therefore, with the retained F and C conventions, the negative chirp is required. The corrected matrix entry is

    U_b[x,y] = q^-1 sum_(z mod q) zeta^(-b z²/2 + (y-x)z).

For b nonzero modulo q, set g=gcd(b,q)=p^v, m=q/g, u=b/g modulo m, and eta=zeta^g. Shifting z by m multiplies the summand by zeta^((y-x)m); averaging the g shifts proves the sum vanishes unless g divides y-x. If x=r+gX and y=r+gY, reduction to m terms and completing the square give

    U_b[x,y] = kappa_(-u,m) eta^((Y-X)²/(2u)),
    kappa_(-u,m) = m^-1 sum_(z mod m) eta^(-u z²/2).

Both signs change relative to the original positive-chirp formula: the reduced Gauss parameter becomes -u, and the completed-square phase becomes positive. The code's X=x//g, Y=y//g is valid on its retained support test because x and y then have the same residue r.

Nonvanishing needs no floating-point or complex-absolute-value argument: writing G(a)=sum_z eta^(a z²/2), the invertible change of variables r=x-y, s=x+y gives G(a)G(-a)=sum_(r,s) eta^(a r s/2)=m. Since m is nonzero in the coefficient field, G(a) is nonzero. Every supported entry is therefore nonzero.

Expanding the square gives positive row/column chirps around the kernel eta^(-XY/u). The latter is the cyclic F_m after the unit coordinate change Y -> -u^-1 Y. The four-entry ratio at block indices 0,1 is eta^(-u^-1), of exact order m. Thus the support/block/core-order conclusions survive, while the signed exponent is now correct. For b=0 the orthogonality sum gives identity, handled separately in the closed formula.

The group label is also tested independently using D(a,c)f(x)=zeta^(c(x-a/2))f(x-a). Under this convention, C_b acts on (a,c) by L(b), F by W, and the corrected U_b satisfies U_b D(a,c)=D(a+bc,c) U_b. Positive chirp would give a-bc and fails the sign regression. This does not claim a new global normalization of every Weil group element or a complete representation audit.

## Fresh bounded mathematical controls

The newly authored checker check_negative_chirp_math.py imports no original or corrected research module. It uses only standard-library exact integer/finite-field arithmetic, has no network/subprocess/install behavior, and does not enumerate SL2. It checks every scalar b at q=3,9,25,27,49, covering 113 cases including five identities. Its exact fields and roots are recorded in BOUNDED_MATH_CHECKS.json.

Result: PASS, 934,875 assertions, 311,723 matrix-entry equalities including Fourier-inverse and group-label controls, 461,139 Weyl-covariance entry comparisons, and 108 expected rejections of the positive-chirp model. Every nonzero b has the predicted support locus, row/column counts, nonzero reduced Gauss factor, exact signed block ratio and primitive residual order. Matrix-product, direct Gauss and completed-square entries agree. These are formula checks, not a run or import of the derivative.

The checker source SHA-256 is `2347a5db79ffba15f8c697a1b80a75563db92d34d239cd376b3ab68e0f448213`. Static syntax and source-manifest checks pass. The patch applies cleanly to the exact original text in a dry run. Packaging and source-file hashes are separately verified; no successful historical log is used to infer a repaired-source pass.

## Historical preservation and replay instructions

The corrected package moves verbatim original results.json, independent_results.json, RESULT_SUMMARY.json, run_all.log and MANIFEST.sha256 under historical_outputs/. Their bytes are unchanged. The original RESEARCH/checkpoint text remains recoverable in the original archive; the derivative identifies its historical execution claims explicitly. The derivative's new manifest binds static inputs and historical files, and excludes mutable future run outputs. The build_results.py test-group count is updated to 13. The driver success label names the derivative.

UPPER_SHEAR_SOURCE.patch is the source-text patch. Applying it alone updates the eight modified source/document files; the corrected ZIP additionally includes the documented historical-output relocation and a regenerated manifest. The complete corrected ZIP is the preferred reproducible derivative. The original source ZIP is included separately in the repair packet and is not overwritten.

## Remaining gates and proposed owner disposition

1. Final static source repair and controls are independently accepted. Reviewer report SHA-256 `37e52c3a66f85aa6b6bb67fb404789d88a36444938f6becf0d0f6a57dc8d6e92` confirms the corrected module, original fourteen-entry and derivative sixteen-entry manifests, and the unrun-source boundary. This completes only the static-repair sub-obligation.
2. Execute the corrected implementation tests, after the required action-time authorization, to obtain implementation-level acceptance. No such run is included here.
3. Execute the original exhaustive SL2/subgroup suites if that original owner obligation is to be discharged. It remains distinct from both the fresh bounded mathematics and any corrected-derivative run.
4. Recover the exact prior accepted bounded API/review bytes before claiming a full reread or replay of that earlier acceptance.
5. General symmetric congruence diagonalization, numerical production qualification, preparation and bit costs, and model-matched historical novelty remain uncertified. Existing restricted theorem, support/cost scope and all rejected extensions are retained.

With independent static acceptance now verified, the narrow source-defect item may say: "A separately pinned v25 derivative now corrects the upper-shear convention consistently across primary formulas, verifier, labels and tests. Original archive and historical results are preserved. Fresh independent bounded mathematics and static syntax checks pass; the derivative and original exhaustive suites remain unrun. Earlier bounded API/review bodies remain recorded-unrecovered."

The parent record remains TO RESEARCH at priority 42. This repair is not a general arithmetic lower bound, full double-coset classification, p=2 extension, faster FFT, production qualification, or historical-priority claim. Native owner histories have not been edited by this task.
