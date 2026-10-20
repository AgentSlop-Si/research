# ALG-036: separate original rank, norm, sampling and cost comparison

Date: 20 October 2026 UTC. This supplement is separate from the preserved optimizer comparison. Candidate for independent review, not a proof or worldwide-priority certificate.

## Disposition first

The recorded bounded task asks for a primary theorem with an exact hypothesis/formula/cost mapping, or a qualified nonmatch or specific access blocker. At that bounded stopping condition, this supplement supplies three additional source-specific comparisons, an explicit classical ingredient mapping, and a concrete unresolved Gaussian-information source-access lead. It therefore supports **completion of this bounded comparison pass**, conditional on independent acceptance. It does **not** support clearing historical priority, all model-matched novelty, or the whole ALG-036 owner. The original HIKP certificate comparison remains completed and is not reopened.

A newly identified, materially close historical lead is G. W. Wasilkowski's 1986 paper on optimal Gaussian algorithms. The author's institutional abstract establishes that Gaussian probabilistic error and adaptation are part of its subject. Primary full-text retrieval failed. A third-party transcription suggests direct overlap with the conditional-Gaussian and fixed-cardinality adaptive-decoding mechanism, but this is a lead to verify, not an established exact match or nonmatch. It is inappropriate to call that mechanism original pending this check.

## A. Exact retained claim and norm conversion

Let x~CN(0,I_N), U a fixed complex unitary, and let the algorithm observe complex-linear functionals chosen from previous answers and an independent seed only. The decoder and stopping rule are transcript-only. Write D=N-rank_C(A_T) for the terminal pathwise rank deficit. The accepted quantitative results require D≥d≥1 almost surely, not merely D>0 with positive probability or a lower bound on E D. No raw-input, uncharged norm, nonlinear statistic, or coefficient side channel is allowed.

The error event is

    ||Xhat-Ux||_infinity ≤ C N^(-alpha) ||x||_2,

with complex coordinate moduli. On this event, the elementary norm inequality gives

    ||Xhat-Ux||_2 / ||x||_2 ≤ C N^(1/2-alpha).

Thus alpha>1/2 forces vanishing relative l2 error; alpha=1/2 gives only the fixed bound C; alpha<1/2 gives a bound that grows with N. The last two are not automatically meaningful small relative-l2 guarantees. The converse conversion is much more demanding: a relative-l2 certificate ρ implies this l∞ event by norm comparison only when ρ≤C N^(-alpha).

The accepted sharp Gaussian projector bound and unconditional norm cutoff yield, by substitution, for 0<epsilon<1,

    Pr(error event) ≤ [1-exp{-C^2(1+epsilon)N^(2-2alpha)/d}]^d
                     + exp{-N[epsilon-log(1+epsilon)]}.

This is a success upper bound. At alpha=1/2 it is the accepted thin-deficit formula; at other alpha the displayed expression is the same fixed-radius bound with r²=C²(1+epsilon)N^(1-2alpha). There is no conditioning of the Gaussian posterior on a norm event. Earlier alpha>1/2, alpha<1/2 and random-one-coordinate-omission controls remain intact. A Gaussian-average upper bound can rule out a uniform every-input success guarantee in the same information model; a Gaussian-average positive construction cannot establish such a guarantee.

## B. Previously completed HIKP comparison, carried forward only

The accepted 16 October certificate maps HIKP v2 Theorems 4.9/6.1 to the sufficient condition

    (1+epsilon) sigma_k(Ux)_2/||x||_2 + delta ≤ C N^(-alpha).

Here sigma_k denotes best-k-term l2 error. The flat-spectrum control disproves that sufficient certificate for k<N, fixed alpha>1/2 and large N. It does not prove that every realization, adaptation, or actual error of a sparse Fourier algorithm fails the l∞ target. The completed source-specific norm/measurement/cost nonmatch is preserved rather than rerun.

Accepted certificate: https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-research-finalization-1722/comparisons/REPORT.md

Independent acceptance: https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-research-finalization-1722/independent_review/INDEPENDENT_REVIEW.md

Access note for the two links above: both commit-pinned files were verified through the repository connector, but the repository is private. They are restricted provenance links, not publicly readable evidence. Their contents are not redistributed here. The inherited certificate status is reported by the accepted comparison and review; this public packet is not a self-contained archive of that earlier proof or review.

## C. New checked primary comparisons

### O01. Price–Woodruff, Lower Bounds for Adaptive Sparse Recovery

Primary full text: https://arxiv.org/pdf/1205.3518v2 (21 October 2012; published SODA 2013, pp. 652–663).

Introduction equation (1) requires, for every real input x, probability greater than 2/3 of ||xhat-x||_p≤(1+epsilon)sigma_k(x)_p. Section 3 studies p=2, k=1 using x=e_I+w with a random spike and isotropic real Gaussian noise of constant expected squared norm. Corollary 3.3, printed p. 6 / PDF page 7, gives m=Omega(R log^(1/R)n), hence Omega(log log n), for R rounds and m real scalar linear measurements. The proof allows rows to be orthogonalized.

This is a sampling lower bound for a best-k-term guarantee, not a bound for the pure isotropic proper-complex prior or the all-bin event in A. Its unknown spike plus noise must not be relabeled a centered Gaussian input. Measurement count and rounds are not arithmetic time or bit complexity. The target norms, hard input distribution, and quantitative scale differ. This is a qualified source-specific nonmatch, not a claim that its techniques cannot be adapted.

### O02. FFTW authors, Pruned FFTs

Primary author-maintained page: https://fftw.org/pruned.html (read 20 October 2026).

The page defines pruning as computing selected outputs and/or exploiting zero inputs. Its explicit first-K-output construction assumes K divides N, performs N/K transforms of size K, and combines them, giving O(N log K) arithmetic work. It uses the complete input. The page distinguishes operation-count savings from realized performance.

This is a positive arithmetic algorithm for a selected-output task, not an all-bin approximate recovery theorem or Gaussian rank barrier. Full input access can have rank N, even if only K outputs are wanted; K outputs are not K input measurements. Conversely, a charged arbitrary linear query may require many arithmetic operations to evaluate. Neither converting output count into rank nor converting rank into runtime is licensed. The exact computational scope is therefore a qualified nonmatch to A, while remaining relevant implementation background.

### O03. Traub–Wasilkowski–Woźniakowski, Average case optimality for linear problems (1984)

Primary institutional scan: https://iiif.library.cmu.edu/file/Traub_box00029_fld00003_bdl0001_doc0001/Traub_box00029_fld00003_bdl0001_doc0001.pdf

Theoretical Computer Science 29, 1–25. Section 3 uses radial/elliptical densities w(||Tf||) and weighted mean-square Hilbert error, equation (3.6); its weight permits relative weighting such as p(t)=1/t. Theorem 4.2, p. 15, expresses optimal error through tail eigenvalues. Theorem 5.1 and Corollary 5.2 use fixed-cardinality adaptive linear information; the setup on p. 17 assumes coefficient dependence continuously differentiable almost everywhere and an attained infimum. Section 7 prices each arbitrary linear functional at c and an entire output-vector addition or scalar multiplication at one.

This is substantial prior rank/information methodology, but its expected-square error is not a high-probability complex l∞ bound. Its specified adaptivity does not verify arbitrary measurable stopped-query hypotheses. Its cost convention is not coordinate-level Fourier arithmetic. These are exact model mismatches, not an assertion of historical originality for Gaussian rank methods.

**Direct scale illustration, not a new attribution claim.** Realify the proper-complex Gaussian as a real 2N-vector with covariance I/2. For fixed rank-m complex information and conditional-mean reconstruction, an elementary projection calculation gives E||error||₂²=N-m=d; divided by E||x||₂²=N, this is d/N. This explains the overlap with a tail-eigenvalue/MSE rank barrier, but does not convert an MSE lower bound into a vanishing success probability: rare large errors can carry the mean. The accepted theorem uses a uniform posterior small-ball bound instead.

## D. Attributed geometric ingredients versus additional scope

The full primary sources S08–S09 in COMPARISON.md verify geometric Brascamp–Lieb and its equality structure. Their exact application is: factor the residual projector P=VV*, put p_j=P_jj and B_j=v_j/sqrt(p_j) for nonzero rows, realify to maps R^(2d)→R², and use

    B_j B_j*=I₂,       sum_j p_j B_j*B_j=I_(2d).

Disc-truncated Gaussian inputs then give the leverage product

    Pr(||Z-b||∞≤r) ≤ product_(p_j>0)(1-exp(-r²/p_j))^(p_j).

The coisometry and constant-one inequality are borrowed. BCCT explicitly credit Ball and Barthe for the geometric result; BCCT are a checked source/reproof, not its sole originators. Valdimarsson provides the equality theorem; its phase-block specialization and the subsequent scalar optimization are additional deductions. No checked geometric statement supplies adaptive transcript conditioning, the original norm cutoff, or a Fourier runtime model. The real-cube bound S03 shares the BL methodology but its event is not the complex disc event.

This is an explicit dependency attribution, not historical-priority clearance for the entire application. The direct concavity/Jensen calculation, Gaussian posterior recursion, and unconditional Chernoff event inclusion remain described as elementary derivations, without claiming first discovery.

## E. Material original-scope access lead

### OG01. Wasilkowski, Optimal algorithms for linear problems with Gaussian measures (1986)

Rocky Mountain Journal of Mathematics 16(4), 727–749, DOI https://doi.org/10.1216/RMJ-1986-16-4-727 . Author institutional abstract: https://scholars.uky.edu/en/publications/optimal-algorithms-for-linear-problems-with-gaussian-measures/ .

The DOI and Project Euclid full-text route returned retrieval errors. The Euclid PDF route returned a challenge/iframe page, not the article. The independent reviewer reproduced this gap. The readable institutional abstract concerns Gaussian average/probabilistic optimality and adaptation but cannot establish exact hypotheses.

A third-party transcription at https://paperzz.com/doc/7208297/optimal-algorithms-for-linear-problems-with suggests Theorem 3.1 on induced/conditional laws and Theorems 5.1–5.3 on translated spline decoding, fixed-cardinality adaptive comparison, and symmetric convex error. This was used only to identify precise next locations. Its formulas and hypotheses have not been certified against an authoritative full text. Treat OG01 as an unresolved primary-source mapping, not a cleared nonmatch. In particular, do not infer that the current posterior/adaptivity mechanism is novel.

Next check: obtain primary pp. 727–745 and compare real/complex convention, fixed versus stopped/pathwise rank, admissible coefficient measurability, deterministic versus input-dependent tolerance, and all-bin probability. Even a verified fixed-cardinality match would not by itself settle the exact weighted N=3 optimizer or all later stopping/sphere/runtime scopes.

## F. Stop condition and retained owner scope

1. The **bounded original-contract comparison pass** now has precise source-specific outcomes: inherited HIKP certificate nonmatch, O01 sampling nonmatch, O02 selected-output arithmetic nonmatch, O03 expected-error/adaptivity/cost nonmatch, verified BL/equality dependencies, and OG01 primary-access blocker. It can be recorded complete at this bounded stop after independent acceptance.
2. The **optimizer literature comparison** is independently bounded by S01–S10 and G01, with no verified all-radius subsumption and no global novelty claim.
3. **Historical priority and complete model-matched novelty remain unresolved**, especially OG01 and G01. These are not concealed by marking the bounded pass complete. Whole-owner status, priority, and unrelated mathematical/model scopes stay unchanged.

No external service mutation, author contact, purchase, sign-in, or repository operation was performed. The formulas above do not assert a production algorithm, unrestricted Fourier runtime lower bound, arbitrary sphere-prior theorem, or every-fixed-input positive guarantee.
