# Result: the cyclic lower bound is nonsharp at C8, rank zero

**Proved:** sin(3pi/16) < delta_(8,0) <= 1/sqrt(2), in the original external operator-norm model with arbitrary invertible complex monomial gauges, a real core, and complex correction rank zero.

This supplies a strict all-phase obstruction at the first smaller-rank case left open by the accepted N=4m, r=m-1 boundary family. It does not determine the exact C8 rank-zero optimum or give a quantitative positive gap.

The proof also establishes a uniform necessary equality theorem: at N=4m, attaining the existing rank-zero lower bound would force the squared row and column phases A,B to have period N/2. Their commutator endpoint vectors have complementary Fourier parity supports.

For C8, this produces four invariant two-dimensional sectors. Each has a flat endpoint eigenvector, so unitarity forces equal diagonal entries. The two even sectors then require both b0=b2 and b0=-b2, contradicting invertibility. This is the final obstruction; no sparse anti-diagonal shortcut is used.

Files:
- PROOF.md: self-contained model reduction, uniform equality rigidity, C8 contradiction, and legal upper witness
- exact_controls.py: newly written exact symbolic controls
- EXACT_RESULTS.json / exact_stdout.txt: PASS, 519 exact assertions
- PROVENANCE.json / MANIFEST.json: scope and integrity

Still open: the exact value of delta_(8,0), explicit numerical gap, rank-zero attainment/strictness at N=4m with m>=3, and the remaining smaller positive correction ranks. No novelty or general FFT speedup claim is made.

Exploratory numerical code under exploratory/ is excluded from the certificate manifest and is not evidence for any theorem. No historical code was executed and no external state was changed.
