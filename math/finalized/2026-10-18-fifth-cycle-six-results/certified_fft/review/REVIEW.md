# ALG-064 certified all-length FFT fallback: independent review

Review date: 18 October 2026. **ACCEPTED at the explicitly bounded fallback scope, after two independently identified interface/ledger corrections.** All final candidate hashes were checked before and after independent execution and remained unchanged.

## Scope

This review concerns only the raw-complex-dyadic, rational-absolute-tolerance, positive-exponent, unnormalized, all-length numerical fallback. It does not accept a new discovery algorithm, noisy recurrence recognition, a production integration, optimal bit complexity or a whole-owner closure. ALG-064 remains TO RESEARCH, priority 42. The controlling source bytes hash to Git blob 456f54002032c99901e7e842651235c658052261. The reviewer inspected all candidate executable sources as text before local execution. No historical code or external packages were executed, and no external writes were made.

## All-size proof and implementation audit

1. Chirp identity and padding. With q_j=exp(pi i j^2/N), q_k q_j conjugate(q_{k-j})=exp(2 pi i jk/N). L is the least power of two at least 2N-1. The positive/negative arms at offsets 1,...,N-1 and L-(N-1),...,L-1 do not overlap. Every requested k-j lies in the supported interval. Both arms have the same conjugated chirp; a second conjugation on the mirrored arm would be wrong. Squared indices are reduced modulo 2N, preserving the parity information that modulo N loses.

2. FFT signs and normalization. Two unnormalized positive transforms, multiplication, then an unnormalized negative transform and division by L give circular convolution. The final positive chirp gives the requested positive DFT. Source bit reversal and span/stride indexing implement ordinary radix-2 decimation in time; conjugation provides the negative roots. All requested N outputs are emitted. N=1 and zero inputs take exact branches after validation.

3. Roots and rounding. Machin's identity is justified by exact tangent algebra and quadrant selection. Its series remainder and nearest-grid pi rounding give e_pi<=7h/16384. Centering makes angle sensitivity at most e_pi. Degree selection bounds the sine/cosine Taylor remainder by h/128 per component. Root-grid rounding adds at most h/16 in l1, so the total is at most 647h/8192. Outward rounding of the receipt by at most h/256 keeps it below h. The code computes its actual rational radius. Exact integer products, exact common-grid additions and the documented nearest rule provide the stated local error bound; negative ties do not introduce a sign asymmetry in its magnitude. Initial products really convert to h, the FFT arrays embed them by a factor 16, inverse normalization divides by 16L to return to h, and final products divide by 16Q. No grid factor is missing.

4. Radix-2 error lemma. Exact stage-s magnitudes are at most 2^s A. Approximate twiddle modulus is at most 1+h. Therefore e_(s+1)<=(2+h)e_s+h 2^s A+h. Dividing by 2^(s+1) and unrolling, with ell h<=1, gives the report's bound 2L[e_0+(ell+1)h(A+1)]. The proof holds for either sign, cancellation and zero values, and the finer h/16 arithmetic only reduces the local error.

5. End-to-end budget. Initial a errors are at most h(S+1), b errors at most h. The chosen C dominates both forward-transform errors. Exact A amplitudes are bounded by S (not LS), because the original l1 mass is S, and exact B amplitudes by 2N-1<=L. Thus the pointwise error is at most Dh. The inverse-transform error after normalization and rounding is at most E_c=2h[D+(ell+1)(SL+1)]+h. Exact requested convolution entries have modulus at most S. The final chirp introduces at most (1+h)E_c+Sh+h, bounded by Kh. All constants in the report match the source exactly. Kh<=epsilon proves the simultaneous Euclidean-complex absolute guarantee for every N, not just tested sizes.

6. Precision and termination. p starts at the largest dyadic input denominator exponent. Exact comparisons enforce both 2^p>=L and K/2^p<=epsilon and select the least admitted p. The displayed expression and asymptotic precision bound follow from K=O((S+1)L^2(ell+1)^2). Raw epsilon encoding can be long even when log(1/epsilon) is small; the separate T/E charge is essential and present. Arctangent tails decay geometrically and the Taylor remainder ratio eventually stays below 1/2. Every mathematical loop terminates for finite valid inputs under unbounded exact arithmetic and sufficient resources.

7. Numerical bit/setup/storage ledger. Taylor denominators divide q^t t!, with log q=O(p+log L), t=O(p+1). Both accumulated partial sums and temporary cross products therefore fit O(H) bits as stated. Arctangent partial sums fit the claimed smaller geometric-power/product-of-odd-indices bound. Fraction gcds and divisions are explicitly inside A(H). Integer kernel widths fit W because exact and approximate magnitudes remain polynomial in L, ell and S+1; even inverse intermediates are covered. Root setup is charged O((N+L)(p+1)A(H)); three FFTs have exactly 3(L/2)ell rounded products, and pointwise, normalization, input/output chirp, indexing and output work are separately covered. Constant-many arrays and one root's large rational temporaries yield the stated numerical storage. This is an O(N log N) transform-kernel claim, not an O(N log N) total-bit or practical-speed claim.

8. Failed-work accounting. The fallback preserves supplied invoice order, totals and symbolic terms; it does not independently prove that an upstream caller supplied every charge. The actual two adapter rejections retain all 170 performed real-operation/comparison charges, with the second rejection at tail index 16. The prior cap solve, if actually attempted, remains payable at its controlling bound. Production integration must supply its truthful full invoice. Peak pipeline storage is the maximum sequential-stage peak plus retained input/invoices, not a fictitious free failed phase.

## Corrections identified and requested

The initial detail field admitted arbitrary objects, including a mutable list, despite a frozen dataclass and a shape-validation claim. The corrected source validates a string detail before either the exact or FFT branch. Separately, the first complexity formula omitted processing an arbitrary r-length invoice independent of N: repeated addition of wide counts is not covered merely by O(E_invoice) input reading. The corrected report now includes the explicit r A(T_invoice+log(r+1)) term, separately charged O(E_invoice+r(T_invoice+log(r+1))) retained/receipt storage and the r-inclusive O(r+N(p+log N+1)) whole-reference scalar-operation summary, plus encoding reads. All three revised statements were inspected and accepted. These are interface/ledger corrections; the numerical proof is unchanged.

## Independently authored numerical oracle

The reviewer checker uses a third pi identity: pi=6 asin(1/2). Its positive rational series has term t_n=binom(2n,n)/(2^(4n+1)(2n+1)) and ratio t_(n+1)/t_n=(2n+1)^2/[8(n+1)(2n+3)]<1/4. After a partial sum, the remaining pi tail is at most 8 times the first omitted asin term. The midpoint and half-width therefore give an exact rational pi enclosure without either candidate arctangent formula.

Centered roots are then enclosed by separately authored exact Taylor evaluation with a uniform Lagrange bound and the pi-radius contribution. The checker directly sums every N-transform output; it does not use chirp convolution or FFT in the oracle. Each real/imaginary interval encloses the target, and the squared farthest-corner distance certifies the Euclidean error. These finite controls detect transcription failures and bind implementation bytes; the preceding all-size proof supplies the universal guarantee.

## Final frozen binding and controls

Accepted candidate directory: /workspace/shared/alg064_certified_fft_20261018_1919

- Candidate MANIFEST.json SHA-256: bf879f9ca2b2716cacaf2079be3721c7d3d8f44474d99d9c04109ffd7619eefc
- Candidate REPORT.md SHA-256: bb11a15c3d48be8a78ff6a590f25555d2579b824fd5bfdad079a2a6bd4b1a04c
- Candidate certified_fft.py SHA-256: 72aa973e3626e3726b890e82a4f5712fa59dceceb2c4574e47bf4d681718fdd1
- Controlling exact source Git blob: 456f54002032c99901e7e842651235c658052261

FINAL_CANDIDATE_BINDINGS.json verifies every declared candidate file hash and byte length. The final reviewer execution compiled a captured backend byte string, based every numerical source mutation on that same byte string, and verified the whole candidate manifest and files both before and after the run. No candidate bytes were written by the reviewer. Initial binding/correction artifacts are retained only to explain the revision; they do not authorize acceptance of the superseded first candidate.

The corrected author suite was also rerun from inspected copies under author_reproduction/. Its summary matched exactly except for wall-clock time, and OUTPUT_VECTORS.json was byte-identical. This reproduces 34 cases/600 bins, six numerical source mutations, five receipt mutations, ten malformed-domain controls, four malformed-detail controls and the 129-record wide-invoice encoding test.

Independent reviewer controls passed:

- All 34 saved cases and 600 bins were certified with the third-formula oracle and regenerated exactly, including complete receipts.
- Sixteen additional cases and 591 bins cover unseen lengths 6, 10, 13, 18, 29, 49, 63, 66, 67, 127 and 129; a 4,096-bit near-one tolerance; another long rational encoding; b=650 tiny-amplitude data; epsilon=2^-500; and large complex cancellation. Maximum selected precision is 668 and maximum FFT length is 512.
- 7,638 signed rounding cases verify nearest distance and positive-infinity halfway ties.
- 414 root controls cover p=0,1,2,7,31,101 and denominators 1,2,3,5,8,17,33 against independent rational enclosures.
- Five newly authored source mutations are rejected by numerical enclosures: chirp residue modulo N, conjugating only the mirrored b arm, wrong final chirp, a missing factor 16 in normalization, and lost initial grid embedding.
- Eight independently authored receipt mutations are rejected: dropping an invoice, wrong total, missing bit-cost term, free roots, zero error claim, nonminimal precision, missing transform and missing root-term work.
- Seventeen malformed input/invoice controls reject, including list, dict, None, integer and boolean detail values.
- Ordered synthetic wide invoices preserve arbitrary integer counts and terms, including an N=1 case with 4,097 records. These large counts are explicitly interface/encoding controls, not claims that such discovery work was actually executed. The real two-attempt 170-operation rejection control remains separately reproduced.

REVIEW_CHECK_RESULTS.json and review_checks.py provide the complete independently authored finite check record and reproducible control implementation. Their 50 cases/1,191 bins support source binding and transcription only; universal validity follows from the all-size proof review above. Wall time is not performance evidence.

## Disposition

Accept and park the certified all-length fallback interface at this exact frozen scope. The result supplies all N complex dyadic outputs within the rational absolute tolerance, pays for root construction and finite precision, improves the numerical kernel from quadratic to O(N log N) arithmetic, and explicitly retains failed front-end costs plus invoice-processing cost. No remaining correction is required for this candidate's stated scope.

Keep ALG-064 TO RESEARCH at priority 42. Stable/noisy recurrence recognition and conditioning, non-dyadic inputs, production/historical integration, resource-limited certification, efficient root/bit-cost optimization and runtime benchmarking remain open. Caller honesty/completeness of predecessor invoices is an integration premise, not a fact the standalone fallback can certify. The classical Bluestein method is correctly attributed rather than asserted as a novel FFT construction.
