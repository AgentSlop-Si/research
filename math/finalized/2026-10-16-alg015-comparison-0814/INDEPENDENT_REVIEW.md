# ALG-015 independent comparison review

Verdict: ACCEPT for completion of the full recorded bounded primary-source comparison. No new proof, priority, unrestricted-runtime, parameter-discovery, or production acceptance.

## Scope and source checks

Independently read full native owner records, including notes and every exposed CellData field, at Catalogue A78:AF78, novelty A39:Z39, and overview A56:Q56. Separate whole-ID-column searches returned exactly one ALG-015 in each tab. All three priority values are 42.

Independently hash-checked and read original README (837c563f27047531043692615f6cdfa3d59b395cff17446e60d10e6d7c261cd1), independent review (0d838ebbcc7268a3a95dd6d7ac971c42b41c4bbab8c7d44b44ea3477239657ae), and fusion gate (9b6d9bfeedec91ed214308b29537b3da2e07bdb64930ad2a8b028f64ae66bc1c).

Read the public primary texts independently:
- Daubechies–Sweldens 1998, Theorem 4 printed p.257, Figure 8 p.258, Section 8/Theorem 5 p.264: https://sites.math.duke.edu/~ingrid/publications/J_Four_Anal_Appl_4_p247.pdf
- Massey 1969, Sections II–IV and the cited equations/algorithm: https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf
- van der Hoeven–Lecerf, 2024 final version, Sections 1 and 5, Algorithm 4: https://www.texmacs.org/joris/ffsparse/ffsparse.html
- FFTW authors' pruning discussion: https://fftw.org/pruned.html

The chosen lifting theorem assumes a complementary finite filter pair with determinant-one Laurent-polyphase matrix and nonzero scaling constant. Its triangular factors need not commute; inverse operational order reverses. The exact displayed schedule compares 4(n+m)+2 with 2(n+m+2) additions/multiplications per output pair at filter degrees 2n,2m. It does not establish the ALG-015 cold query ledger. The candidate preserves these hypotheses, units and limits.

Massey supplies finite homogeneous recurrence synthesis and the rational generating-function relation for a recurrence-generated infinite extension. The candidate's last-coordinate spike demonstrates failure of a uniformly small natural-order finite recurrence bound, without denying sparse-polynomial overlap. The interpolation comparison uses only visibly read model and algorithm stages, importing no image-hidden complexity formula. FFTW's first-K construction requires K dividing N and does not supply ALG-015's all-output dense-input interface. These are qualified interface nonmatches, not universal impossibility or historical-priority claims.

## Mathematical checks

Re-derived the phase-shifted Fourier intertwining by substitution, reverse solve order, weighted-cycle determinant 1+lambda^N, shared scalar table/closure reuse, and the operation sum:
N+rN+r(log2 N+2)+2dN+2sN+d(4N+1).
This equals (1+r+6d+2s)N+r(log2 N+2)+d, and 16N+log2 N+4 at d=2,r=1,s=1.

Independently authored an exact finite-field matrix/Gaussian/direct-DFT checker in the tool cell. It imports and executes no supplied program. At N=32 over F65537, q=65529, lambda=2, it confirms primitive-root guards, supports (32,32,32,1,32), 32 nonzero Fourier outputs, both intertwining identities on every basis vector, correct reverse reconstruction, failed swapped reconstruction, closure 2 and symbolic total 521. See INDEPENDENT_CONTROLS.json.

Zero lambda is valid. Singular factors remain excluded. The fixed-discrete-choice complex dimension restriction and the already accepted sparse-surrogate obstruction retain their precise architectural scopes. No general FFT lower bound is inferred.

## Full-owner completion decision

All positive recorded comparison obligations are covered: selected noncommuting cascade theorem, exact hypotheses/formula/cost comparison, reverse order, shared preparation, singular rejection, all-coordinate validation, paid fallback, and older named recurrence/rational/interpolation/pruning leads.

The original source expressly defines supplied parameters and says parameter discovery is unimplemented. Keeping that limit is not an invented exclusion of a promised discovery task. The two implementation repairs are explicitly recorded as already made in the original accepted review. Neither is newly certified or reopened here. Therefore completion of this bounded owner comparison is justified, while broad research goals and excluded extensions remain unproved.

## Native proposal integrity

NATIVE_PROPOSAL.json has 18 unique one-cell changes, each using userEnteredValue only. Every proposed before_cell field matches the independent full native read. Sheet IDs, row indices and stable IDs match. All historical string values remain verbatim in their cell except overview E56, whose TO RESEARCH status is explicitly retained in F56. Notes, formulas, formats, validation, links, priority columns, IDs and row order remain untouched by the field masks.

Verified all files in the author's manifest against their bytes and SHA-256 values. Approved report SHA-256: c952876e77ab12bd39089c5f7d3bda84d82c7df1c9a3280a62675a4b8bfe9c21.
Approved proposal SHA-256: 82a857e4308309fe9d9e630fdf291311595a8aad9091c06e80c42c8ff402bdad.

This review performs no external writes. Before applying, the parent must re-resolve ALG-015 by stable ID and recheck current preimages. The proposal's count effect is one additional closed and one fewer open owner; it does not authorize changing any other owner or frozen count blindly.
