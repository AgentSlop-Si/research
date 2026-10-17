# Independent acceptance: ALG-064 residual-aware numerical evaluator

17 October 2026. **ACCEPT the stated conditional finite-word evaluator contract.** Parent TO RESEARCH, priority 42, historical proof/novelty classifications and prior exact results remain unchanged.

## Mathematical review

The full coefficient identity C X=P+E+T^N B is correct for an arbitrary supplied sequence, with the defect measured over every index L through N-1. The declared recurrence span L is correctly retained when deg C=r<L. At Fourier nodes the numerator is A+E, where A=P+B; omitting E would invalidate numerical certification on perturbed data.

The small-denominator lemma is valid. Since C(0)=1, all factor roots alpha are nonzero. A product below (2N)^(-r) forces one factor |1-t/alpha|<1/(2N). Two distinct grid nodes in that same disk would have distance below 2/(2N-1), whereas their distance is at least 2 sin(pi/N)>=4/N. Thus at most r distinct nodes are genuinely small. Characteristic-root factorization is used only in the proof, not by the evaluator. Degree zero is separately covered by C=1.

With denominator evaluation error at most tau/4, the strict classifier |qhat|<3tau/4 selects only genuinely small nodes. Equality is regular; the regular denominator has modulus at least 3tau/4 and the true denominator at least tau/2. The exact squared-rational comparison removes any ambiguous numerical-zero test. The residual, numerator error and denominator error together contribute at most epsilon/2 after division, and the separately charged quotient rounding contributes at most epsilon/4. Certified direct Horner evaluation supplies every suspect output. This is an absolute-error result; it promises no relative error at tiny outputs.

The Horner bound 3D(U+2)rho follows by separating node displacement and operation rounding. The explicit p inequalities are sufficient, including exact coefficient representation at p>=2b. The displayed oversized p bound is conservative. The O(N(L+1)) arithmetic count includes all exact defects/boundaries, numerator/denominator evaluations, at most r direct N-term evaluations, division and output work. Multiplication and division bit costs and certified root-table construction remain explicitly charged. The one-inversion exact-field ledger is correctly not transferred to numerical arithmetic.

## Independent checks

Fresh exact rational and Q(sqrt(2),i) code evaluated grids N=2,4,8 with independently certified dyadic nodes and exact comparisons to algebraic target outputs. It passed:

- 367 admitted vectors and 1,990 exact all-output error checks;
- 1,990 exact defect identities and node certificates;
- 1,920 regular and 70 suspect outputs, always at most r suspects per vector;
- 175 admitted nonzero-residual cases and 175 deliberate residual-gate rejections;
- 35 untapped-register cases and 367 explicit precision-inequality checks;
- 576 exact single-root neighborhood controls.

The checks include resonant and near-resonant factors. The fixed-threshold counterexample is valid: C=1-T has an unbounded number of bins below any fixed positive threshold as N grows. These are finite controls of transcription, not a replacement for the universal proof. No author or historical research program was imported or executed.

## Accepted boundary

Close only the supplied-dyadic-coefficient, paid-certified-node, residual-aware fixed-grid evaluator subgate. Every exact dyadic recurrence with the supplied C passes the residual test. Failure for a supplied approximate C does not prove nonmembership. The report correctly makes no promise that numerical discovery finds suitable coefficients.

Stable raw-input coefficient discovery, root-table construction efficiency, arbitrary input encodings/heights, total certified fallback, normalization/real-residual conversion, historical source integration, production arithmetic and speed remain separate. Do not call this blanket numerical stability or an arbitrary-input DFT improvement. No external state was changed. Mathematical acceptance alone is not a native-write or publication receipt.
