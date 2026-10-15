# ALG041: exact-source comparison with classical tools

Date: 2026-10-15. Scope: the named classical-volume, uncertainty, Schur, and selected-output comparison for the accepted actual-source exposed-packet result.

## Decision

**The named comparison is complete, subject to independent review.** The determinant step is an application of classical rectangular volume machinery. The packet identification, complete-bank Gram formula, and high-weight combinatorial certificate specify the matrix to which that machinery applies. Uncertainty explains the packets' simultaneous supports; it does not replace the weighted-volume argument. Schur elimination and selected-output transforms provide exact algebraic or algorithmic components but do not supply the missing faster causal construction under the accepted interface.

**The faster causal correction and complete sub-N log N transform remain OPEN.** No historical-priority finding, new unrestricted lower bound, production claim, or rank/status change is proposed. The previously accepted proof remains accepted only within its stated model. This comparison neither upgrades that acceptance nor changes global closure counts.

## 1. Exact object being compared

The complete project source `CONSTRAINED_JET_FUSION.md` (SHA-256 `f11dd814af83d7f8e3a40240cbd0ad0fc247ffb19776972f12666f8864d52112`) and complete `INDEPENDENT_CONSTRAINED_PACKET_AUDIT.md` (SHA-256 `bf520e2fe8c328bfc207b67b299074dc37cd1035172e6036d576f45a7f86124e`) were inspected. Source §§1–7 and audit acceptance/normalization sections control this comparison. No historical checker was executed.

There is one input x in C^N, N=2^n. Put d=n-b, r=2^d, L=2^(b-1), and Qe_s=e_(2s mod N)+omega^s e_(2s+1 mod N). Retained jets are u_h(a)=(Q^h x)_(2^b a). The young theorem requires b>=7 and L+2b<=n. K_t consists of length-t words starting and ending in 1 and avoiding 0^b; S_t={2^(b+t)q+k : k in K_t, 0<=q<2^(n-2b-t)}. These S_t are disjoint.

For h>=b, a=2^(h-b)q+c, f=rev_(h-b)(c), and M=2^(n-h), the actual packet is

    u_h(a)=omega^gamma(c) P_(h,q,f)(x),
    P_(h,q,f)(x)=sum_(s congruent q mod M) omega^(sf) x_s.

The factorization through the full unnormalized Fourier vector y is

    P_(h,q,f)(x)=(1/M) sum_(v=0)^(M-1) omega^(-qv2^h) y_(f+v2^h).

It is an identity, with no free transformation of the input. Fusion gives C_t Q_r^t u_j=1_(S_t)u_(j+b+t). Thus young feedback g_h is a coordinate mask of the same-time actual jet. Before the orbit is known, substituting this identity into the causal correction gives u_h(a)=u_h(a), not the value of that coordinate.

The lower-bound matrix H selects actual requested values with a in S_t and 2b+t<=h<=n. It has N columns and D<=r(n+1) rows. The stronger time restriction makes the q-bank complete and independent of the allowed f selection. Removing it invalidates the stated projector derivation. For each allowed h,f, the M rows have disjoint supports, squared norm 2^h, and span the Fourier coordinates ell congruent to f modulo 2^h. Consequently, with U the unitary Fourier matrix,

    H*H=U* diag(lambda_ell) U,
    lambda_ell=sum_(t=1)^L sum_(h=2b+t)^n 2^h 1_(E_(h,t)(ell)),

where the low h bits have pattern 0^b rev_t(k) 0^b [arbitrary lower bits]. U is used analytically, not provided as a free circuit gate. The original high-window, two-isolated-marker second-moment argument gives at least N/4096 eigenvalues >=2^(n-L). It does not assume independent overlapping occurrences.

## 2. Classical volume: an exact match after the source matrix is identified

Primary comparator: Bürgisser–Lotz, *Lower Bounds on the Bounded Coefficient Complexity of Bilinear Maps*, arXiv:cs/0301016v1, Definitions 2.1–2.3 (pp. 3–4), §3 Eqs. (2), (4), (5) and Proposition 3.1 (pp. 7–8). [Primary paper](https://arxiv.org/pdf/cs/0301016)

Its linear-circuit model uses complex scalars of modulus at most 2 and counts instructions; outputs may occur anywhere in the result sequence. For an m-by-n matrix and 1<=rho<=min(m,n), Eq. (2) bounds complexity by log2 vol_rho; Eq. (4) compares maximal row volume with mean-square volume using sqrt(binomial(m,rho)); Eq. (5) expresses the latter by singular values. Proposition 3.1 replaces that binomial correction by the coarser m/2. The paper credits the square determinant method to Morgenstern and the rectangular r-volume formulation to Raz. These are classical components, not a new volume principle.

For our matrix set A_aug=[I_N;H], m=N+D, n=rho=N. The identity rows are the original inputs, already available. Direct substitution gives

    msv_N(A_aug)^2 = det(A_aug* A_aug) = det(I+H*H),
    max_(|J|=N) |det(A_aug)_J| >= sqrt(det(I+H*H)/binom(N+D,N)).

This is exactly the source's augmented Cauchy–Binet step, not an analogy based on independent jets. The binomial version comes from Eqs. (2),(4), before the coarsening in Proposition 3.1. Its finite correction must not be quoted as though Proposition 3.1 itself stated it.

In the project's coefficient-at-most-one model, track the maximum absolute determinant of N historical coefficient rows. Initially it is 1. A scalar gate cannot increase it; a binary sum or difference increases it by at most 2. Therefore the source's **addition-only** bound is

    A_add >= N/2 [(n-L)/4096 - log2(e(1+(n+1)/2^b))].

A negative right side says nothing. At b=floor(log2(n/(4 ln n))), L=o(n) and the correction is O(log log n), giving (1/8192-o(1))Nn. The BL model instead permits gain 2 and counts all gates. For a fixed scalar bound K, the same direct potential bounds total gates with a divisor log2(max(2,K)); it does not preserve the addition-only statement when amplifications are free. Unlimited gains require a separate growth budget.

No BL cyclic-convolution theorem is substituted for this proof: its bilinear two-input problem is not our one-N-vector constrained output map. The project-specific contribution evaluated here is the actual H, its complete-q decomposition, and its positive-density large eigenvalues. This attribution does not establish historical novelty of those components.

## 3. Uncertainty: exact support match, qualified nonmatches

Primary comparator: Tao, *An uncertainty principle for cyclic groups of prime order*, arXiv:math/0308286v6, §1 Eq. (1), pp. 1–2; Theorem 1.1 and Lemma 1.3. [Primary paper](https://arxiv.org/pdf/math/0308286)

The introduction proves the finite-abelian support product |supp a| |supp Fourier(a)|>=|G| by elementary inequalities and identifies subgroup indicators as equality examples. Its Fourier convention includes 1/|G|. The stronger support-sum theorem and nonvanishing-minor lemma require prime group order. These are different assertions.

Our packet coefficient vector is a character times the indicator of a coset of M Z/NZ. Its original-coordinate support has size 2^h; its Fourier support is an annihilator coset of size M=2^(n-h), so the product equals N. Signs of the labelled frequency coset depend on whether a coefficient row or its conjugate column is transformed; cardinalities and the source row-space formula agree. Neither normalization changes those support sets.

Thus classical uncertainty explains this packet geometry exactly. It supplies no count of the particular overlapping E_(h,t), no 2^h amplitude weights, and no circuit cost. Those remain the source's separate Gram/density/volume steps. The prime additive result cannot be invoked at N=2^n in the accepted regime. For example at N=4, (1,0,1,0) has support 2 and Fourier support 2, contradicting a hypothetical composite-order bound 2+2>=5. No full-spark conclusion is imported.

Donoho–Stark's original 1989 paper was also sought via the author-hosted and UCSD PDFs. Both had zero parsed text lines; the available screenshot route did not provide readable images. A Berkeley copy returned 403. An author-uploaded ResearchGate page exposed some text, but its full proof was not inspected. **No claim of a full Donoho–Stark proof read is made.** Tao's complete readable primary paper supplies the needed product statement. Morgenstern's original ACM PDF likewise was not obtained; the attribution above is explicitly the account in the fully inspected BL primary paper.

## 4. Information dimension and normalization are decisive

Rank H=#{ell:lambda_ell>0} is at most N, regardless of the number of exposed temporal values. The accepted rank N-a_b(n) belongs specifically to the complete stack u_b,...,u_n; it is not automatically the rank of H or a stack with earlier times. Repeated/overlapping temporal packets are already incorporated in lambda. The augmented identity rows restore full column rank without inventing independent data.

If each row at time h is multiplied by 2^(-h/2), then every normalized packet row has norm one, and the normalized eigenvalues become mu_ell=sum_(h,t)1_E. Their sum is D. Concavity gives

    log2 det(I+Hbar*Hbar) <= N log2(1+D/N)=O(N log log n)

at the accepted marker choice. More strongly, every N-row minor of [I;Hbar] has modulus at most 1 by Hadamard, so the particular maximal-minor lower bound is vacuous. The support-product statement and information dimension have not changed; the expensive unnormalized amplitudes have. This proves failure of this witness after normalization, not existence of a fast normalized algorithm or of a free renormalization back to the original outputs.

## 5. Schur/path sums: algebraic match, no causal cost certificate

Primary comparator: Giscard–Thwaite–Jaksch, *Evaluating Matrix Functions by Resummations on Graphs: The Method of Path-Sums*, arXiv:1112.1588v2, Theorem 3.2 and Remark 3.1/Eq. (3.3), p. 7; Appendix A.3, p. 20; §4.3, pp. 15–16. [Primary paper](https://arxiv.org/pdf/1112.1588)

The inverse theorem treats arbitrary partitions of an invertible complex matrix, subject to existence of the inverses appearing in its expressions. The two-block example recovers Schur inversion. Its tree cost analysis counts block inversions/products and depends on a tree partition and block size; the paper does not give a general small-boundary solver bound.

Here is our explicit algebraic mapping. Let T be the retained marker/avoidance set of the marker-cut construction and E its eliminated complement; the packet coordinates R are a subset of T. In formal power series set

    D_E(z)=I-zQ_EE,
    S_T(z)=I-zQ_TT-z^2 Q_TE D_E(z)^(-1) Q_ET,
    f_T(z)=x_T+zQ_TE D_E(z)^(-1)x_E.

Then

    u_T(z)=S_T(z)^(-1) f_T(z),
    u_E(z)=D_E(z)^(-1)(x_E+zQ_ET u_T(z)).

Constant terms of D_E and S_T are identity, so their formal inverses exist. Nilpotence of the eliminated block, when supplied by the marker-cut construction, makes D_E^(-1) a finite polynomial. This is our formal block-elimination application, not an unqualified substitution of a formal matrix into a complex-matrix theorem. Complex specializations need their actual inverse hypotheses checked.

Expansion identifies Q_TT as the length-one retained transition and Q_TE Q_EE^(ell-2)Q_ET as the length-ell first-return coefficient for ell>=2. This matches the retained recurrence's algebra. It does not compute its solution for free. A paid solver must form/apply the fresh term, compute the causal S_T inverse action through the required degree, and recover/output everything required. Fusion aliases leave precisely this work missing. No tree partition with the requisite block sizes, total output count, and coefficient-operation budget is supplied for applying the paper's special tree cost here. Schur/path-sum provenance is established; sub-Nn construction is not.

## 6. Selected-output algorithms: exact input/output tests

Primary comparator: van der Hoeven, *The Truncated Fourier Transform and Applications* (ISSAC 2004), §§3–4, Theorems 1–2, pp. 2–3. For corrections use *Notes on the Truncated Fourier Transform* (dated 2005; errata 2008 and 2025), §§5–6, Theorems 1–2 and Remark 3. [Original](https://www.texmacs.org/joris/issac04/issac04.pdf), [corrected account](https://www.texmacs.org/joris/tft/tft.pdf)

For length m=2^p and l<=m, the univariate TFT takes l coefficients, zeros the rest, and returns l specified bit-reversed evaluations. The stated forward count is at most lp+m additions and ceil((lp+m)/2) root multiplications; the inverse uses shifted additions with the same bounds. The corrected general inverse algorithm requires an initial segment in the bitwise partial order; arbitrary unions of intervals are not covered. Remark 3 exhibits algorithm failure at m=4,S={1,2}. The notes separately repair multivariate complexity claims.

Our input is an arbitrary dense N-vector; a small retained width r does not mean the other N-r input coordinates vanish. H also contains different-time coset packets, not simply the first r Fourier evaluations. Substituting l=r,N=m without an actual zero-input reduction and matching evaluation indices is invalid. The corrected notes do define asymmetric forward S-to-T pruning, but that definition alone supplies no low-cost bound for the full source-constrained bank. It does not justify an arbitrary selected-output inverse or solve the retained causal recurrence.

Additional primary implementation comparator: FFTW, *Pruned FFTs*, section “Computing only the first K outputs of a DFT with FFTW.” [Documentation](https://fftw.org/pruned.html)

For dense length-N data and K dividing N, its concrete procedure uses N/K length-K FFTs followed by twiddle-weighted sums for the first K outputs. The arithmetic order is O(N log K+N), rather than a cost depending only on K. It is implementation documentation, not an exact-complex lower-bound theorem; floating-point execution and planning are separate concerns.

In our application no identified K-output full-DFT subproblem equals all H rows for free. Even for K=r=N/2^b at the marker choice, log2 K=n-b=Theta(n); this advertised pruning order would still be O(Nn). This observation is a cost substitution for that algorithm, not a lower bound for every selection or every fused solver. If the spectral packet identity is used, computing full y first costs O(Nn), and independent packet inverse banks cost an additional sum_h O(D_h(n-h))+O(D), at most O(rn^2)+O(D). All such transforms, phase preparation, and writes must be charged.

## 7. Paid construction and remaining boundary

The accepted direct orbit has butterflies

    w_(2s)=v_s+v_(s+N/2),
    w_(2s+1)=omega^s(v_s-v_(s+N/2)), 0<=s<N/2.

Through n layers this costs Nn additions/subtractions and at most Nn/2 unit-modulus scalar multiplications. From a supplied exact primitive root, phase-table and membership preparation costs O(N+n) in the accepted field-operation and O(log N)-bit address model; root acquisition or order validation is not included. Input reading costs O(N), masked feedback writes O(r(n+1)), and final phase/reversal/writes O(N). Live orbit storage is O(N); saving all requested feedback adds O(r(n+1)) words. This genuinely pays for an order-matching construction. Its reuse occurs after, or during, a computed orbit, not before the unknown future states exist.

Fresh-source preparation alone, even with the accepted O(Nn/ln n) bill, is not an inverse-correction algorithm. A candidate improvement must either avoid literal exposure of these exact unnormalized complex values or specify a different model and pay for all needed conversions, correction, recovery, and output. Finite fields, nonlinear circuits, unlimited scalar gains, approximate outputs, and different exposure interfaces are not covered by the accepted obstruction.

## 8. Completion and evidence boundaries

- Completed: named comparison, exact rectangular-volume substitution, uncertainty support match and prime nonmatch, Schur algebra/cost distinction, corrected TFT interface test, dense-input pruning cost test, normalization and dimension accounting.
- Still open: faster causal correction/full transform under an admissible paid interface; historical priority; applicability of any different model.
- Preserved: accepted proof status and all guards, catalogue rank and broader solver gate, prior dated history. No claim that another result was newly proved or closed.
- Reading evidence: complete line-addressed primary-paper text was inspected for BL, Tao, Giscard et al., original TFT, and corrected TFT notes; full FFTW page was inspected. Mathematical extraction has occasional OCR glyph artifacts, so formulas above were checked against the surrounding statements and the accepted source. No downloaded-PDF byte hash is asserted when only a parsed text receipt was obtained.
- Publication: this authored comparison and the source-locator/hash manifest may be published. Full third-party texts, raw service responses, and spreadsheet snapshots are verification-only and excluded. All source-specific test counts in the old source remain historical; none were rerun for this comparison.

See `PRIMARY_SOURCE_LOCATORS.json` for versions, precise locators, receipt identities, and access qualifications.
