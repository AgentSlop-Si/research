# Mixed prime power Fourier masks below the larger prime

For distinct primes p<q, including p=2, every exponent a>=2, and N=p^a q, the accepted theorem classifies all possible mask degrees strictly below q. It concerns arbitrary entrywise binary supports with the literal Fourier phases, not selected rectangular submatrices or only block constructions.

## Accepted theorem

Let zeta be any primitive Nth complex root, R an arbitrary binary N-by-N matrix, and D[r,c]=R[r,c] zeta^(rc). For integer 0<=d<q, there exists such a mask with either D*D=dI or DD*=dI exactly when

    d=0, or d=p^j with 0<=j<=a and p^j<q.

At a=2 this is {0,1,p} if p<q<p^2 and {0,1,p,p^2} if q>p^2. The boundary d=q has the inherited divisor witness, not an extension of the short-overlap argument. No degree above q is classified.

The new reduction erases the q-character after grouping a zero column Gram by q-label. Over Q(zeta_(p^a)), the q-root has minimal polynomial 1+X+...+X^(q-1), forcing all grouped coefficients equal. Since a column intersection has fewer than q rows, one label is missing and every coefficient must be zero. The erased matrix remains square of size p^a q, with the same support and both Grams dI.

Its repeated labels are essential. The inherited weighted theorem covers arbitrary square size, repeated row and column labels, and row weights p^(k_i/2); it bounds the exponent by K+a. Here all k_i=0, hence j<=a. The actual weighted proof, independent review, programs, full descent certificates, weighted stress cases and observed original-model evidence are bundled, not just their locators.

## Original inverse row consequence and limits

Let F be the normalized complex Fourier target and Delta(N,s) the infimum of ||M-F||_2 over invertible complex M with at most s nonzeros in every row of M^(-1). The norm is the spectral operator norm; supports, coefficients, phases and conditioning are unrestricted. For 0<d<q and s=N-d, the accepted complementary-mask criterion and compactness argument give Delta(N,N-d)=sqrt(d/N) exactly at the allowed p-powers. Every other integer degree in this sector has a strict infimum gap, not merely nonattainment.

Prime-power descent, the a=1 low-degree semiprime result, divisor witnesses, inverse-row equality and compactness, earlier exact values, and earlier quantitative gap bounds are inherited. The older weighted candidate's overbroad statement that all quantitative gaps remain open is explicitly corrected by its unchanged independent review. No new gap rate, excluded optimum, full mixed-order classification, support geometry, computational advantage, historical novelty, or owner closure is claimed. The broader owner remains TO RESEARCH at priority 42.

## Evidence and how to read it

Start with [the proof](PROOF.md), [the independent review](INDEPENDENT_REVIEW.md), [the weighted prime-power proof](WEIGHTED_PRIMEPOWER_PROOF.md), [its review](WEIGHTED_PRIMEPOWER_REVIEW.md), and [the inverse-row criterion review](INVERSE_ROW_CRITERION_REVIEW.md). Historical candidate-stage labels remain unchanged; the later independent reviews and this exact scope summary govern acceptance.

The new author evidence records 25 positive controls, four degree-q erasure failures and six regular negative near-masks. The new independent evidence records 20 positive square controls, including six nontrivial cross-q constructions, five degree-q erasure failures, two negative near-masks and 1,499,570 active checks. These finite controls corroborate the proof and its strict guard; they are not an exhaustive mask classification.

The weighted source additionally retains the 2,474,236-byte author descent certificate and 1,048,911-byte independent certificate, including the independent square weighted/repeated-label stress cases of dimensions 30, 26 and 12 at character orders 8, 9 and 5. This preparation read and checked their stored data and hashes, but ran no scientific program.

The evidence ZIP, [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json), [source closure](SOURCE_CLOSURE.md) and [reproduction limits](REPRODUCE.md) distinguish original inventories, actual public bytes and two explicit documentary locator projections. The data-only command python verify_package.py checks integrity and provenance, not the theorem or a fresh scientific run. No turnkey scientific replay is certified.
