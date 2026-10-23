# Independent review: the adjacent p^3/p^2 ordinary squarefreeness family

Date: 2026-10-23 UTC. Verdict: **ACCEPT the exact k=3 family.** No mathematical repair is required to the frozen report.

## 1. Exact scope and source binding

Author packet: `f020_adjacent_digit_guard_20261023`.

- REPORT.md SHA-256: `00f3c35c754f862906b6875689e6e710719660660d3082b3a4ac27259226e77a`.
- The author manifest and selected source hashes are bound in BINDINGS.json.

For every odd prime p, even 2<=c<p, odd 1<=d<p, r>=5, s>r, and every characteristic-zero primitive p^s-th root q, the ORIGINAL recurrence polynomial P_n and Rogers–Szego polynomial H_n are squarefree, and the ORIGINAL ordinary algebraic-square CD kernel is nonzero at every P_n root, where

    n=2p^r+c p^3+d p^2.

The minimum degree is 549. Incremental credit subtracts every previously successful high-order deflation, fixed-degree, and residual certificate. The exact inherited C_u formula is retained; it is not a Catalan bound. The theorem does not cover general adjacent k>=4, close F020/F023, or supply novelty, FFT, bit-cost or stability claims.

The selected accepted sparse-induction, two-middle and deep-cap proofs and independent reviews are copied and hash-bound. Their arbitrary-prefix core cover/B' lemma, deep-tail estimates, original ordinary off-root derivative transfers and outside-cover ratios are used only within the parameter obligations checked below. No author or historical scientific program was executed.

## 2. New adjacent cap and phase-sensitive initial

Put j=2, k=3, L=p^2, M=p^3, N=p^r, A=2N+cM, a0=dL, G0=W((a0-1)/2), sigma0=p/2, sigma=(2p-1)/2, and lambda=L/(2p)=p/2.

I independently checked the stronger auxiliary cap stated for general adjacent k=j+1>=3. Let S(h)=W(h)/2-R_k(h), digit-linear for h<p^k. All its digit-basis weights below k are positive. For a>=floor(k/2), S(p^a)=(k-a)(p-1)p^(a-1)/2; below that range R_k vanishes. The exact floor-sum bound W(h)-2W(floor(h/2))<=p^a, for highest digit a, gives

    R_k(h)-W(floor(h/2))<=p^a/2-S(h)<=p^(a-1)/2<=lambda.

Equality at lambda requires a=j, leading digit one, and all lower digits zero. Direct substitution verifies h=L; h=0,1 have defect zero. Thus the unique equality index is genuinely L, not an unverified collection whose units might cancel.

For the odd short tail, W(dL)=2G0+L. The Newton coefficient bound and superadditivity imply weight(P_(dL))>=G0+L-lambda, with the unique equality term h=L, a=(d-1)L/2. That final addition is carry-free. In a full k disk, N_L has initial a nonzero scalar times Y^(L/beta_k): all matching center differences have valuation at least beta_k>rho_k and all other factors have fixed nonzero initials. For k=3 the exponent is p. Hence at EVERY k boundary the tail initial is nonzero and the value is exactly G0+p^2-p/2, retaining the actual phase and center units.

This Y^p initial must not be differentiated after reduction. The report correctly obtains the ordinary derivative separately.

## 3. Ordinary derivative and the full-disk first-deleted-tail bound

A full k disk lies in the strict interior of its matching j disk even though the level gap is only one. The accepted terminal-j derivative initial is M_(d-1), with nonzero constant because d-1 is even and below p. Therefore the unshifted short-tail ordinary derivative has exact constant initial at G0+L-p on every full k disk. The off-root H/P chain term is bounded by j v(p)+G0+L/2, strictly higher; it is not discarded by an assumption that the tail itself vanishes.

The first-deleted tail g_(dL)^0 has full-j weight at least G0. Its strict-j constant initial is nonzero: in the exact finite connection the equality endpoints are ell=bL; only odd b contribute constant terms, through the even P factors, and their complete sum is the actual recurrence value g_(dL)^0(0)=(-1)^((dL-1)/2)Q_((dL-1)/2). The coordinate units at these constant terms are the same retained limiting units on each disk, not arbitrary independently chosen phases. This is the accepted single-odd-tail mechanism and requires no two-level gap. It gives exact value G0 throughout every full k disk.

The new ordinary derivative bound is g'>=G0 on those full k disks. For the H-derivative part of a differentiated finite-connection term, its score is

    R_k(h)+R_k(t)+W(a)+W(b)+V(delta)+V(ell),
    h+delta+2a=dL-ell, t+2b=ell-1.

Using R_k=W/2-S and superadditivity gives at most

    G0-W(delta)/2-S(h)-S(t)+V(delta)+V(ell).

The elementary difference W(delta)/2-V(delta) is at least -1/2; negative cases occur only at delta=1,p. Those are odd, so h+t is odd and at least one index is positive. Since S has positive half-integral digit weights, S(h)+S(t)>=1/2, exactly supplying the missing half-unit. In all other cases no compensation is needed. Since V(ell)<=L, the score is at most G0+L. Subtracting from W(dL)=2G0+L proves the claimed bound termwise, in either orientation. Chain-rule P terms have nonnegative integer valuation and satisfy the undifferentiated product bound already at G0.

This is a coefficientwise full-disk argument. It does not extrapolate from the central disk and does not use the false stronger bound g'>=G0+L/2-p.

## 4. Actual shifts, legality, and the k=3 boundary proof

The exact associated continuants satisfy

    P_n=F C-b_A H B,
    C=P_A, B=P_(A-1), F=f_(dL)^A, H=g_(dL)^A,
    v(b_A)=V(A)=M.

All tail indices have valuation at most L<M. The exact finite connections give eta-1>=M-L and the stated full-j errors

    Delta_F>=G0+M-L/2,
    Delta_F'>=G0+M-L/2-sigma0,
    Delta_H>=G0+M-L,
    Delta_H'>=G0+M-L-sigma0.

Since M=pL and sigma0<L/2, these errors are strictly higher than all retained terms. Thus the actual shifted F,H, not an unshifted substitute, obey the same adjacent invariant. All indices are legal: n<2N+pM<3N<=pN<=p^s, with strictness also at p=3. Every recurrence edge and finite-connection denominator is nonzero. No total weight is required to lie below v(p) in the proof.

For the even core A, the accepted arbitrary-prefix terminal cap supplies C>=J, C'>=J+M/2-p, B>=E=J-M/2, and the ORIGINAL neighbor derivative B'>=E on every full k disk. Its residuals are Y^(2N/beta_k)M_c and Y^(2N/beta_k)M_(c-1); these Hermite factors are coprime since c<p. Prefix simplicity is not assumed.

At a P_n root on a core-zero boundary, B is exact E, F and H are nonzero, and the root equation gives delta+gamma=M/2 for delta=v(F)-G0=L-lambda and gamma=v(C)-J. The exact leading term F'C beats the other three ordinary derivative terms by at least

    L-2lambda, p-lambda, p-lambda.

At j=2 these are p^2-p, p/2, p/2, all strictly positive. This includes coincident residual classes and all noncentral disks. At a core-unit boundary C is exact J and the direct gaps are M/2-lambda, M/2-L+p, M/2-L+p, also positive. This branch does not divide by B and includes B=0.

Only the accepted full-disk B'>=E estimate is used. The separate experimental central estimate B'>=J-p is not assumed and is not valid globally.

## 5. Remaining root locations and exact original conclusion

For strict k interiors, take prefix 2N and suffix m=cM+dL. Its half-digits are all at most (p-1)/2, and the terminal deficit at j persists at every higher digit. The forced-carry argument used in the accepted sparse-suffix proof therefore still applies. The deep r cap remains within its proved range because r>=k+2 and m<pM; adjacency is only between j and k. On full r disks this gives the actual deep tail bounds f>=G+L, f' exact G+L-p, g exact G and g'>=G-(p-1).

On full k disks, the derivative equality set delta=p^2 and h=bM with even b remains exact; its residual M_c has nonzero constant on strict interiors. Only the weak g bound G+L-M is used there, never a false full-k g unit. Outer shifts are dominated since N>=p^2 M. The leading-two r-boundary, deepest-interior and k/r-annulus comparisons remain strictly positive because M+rho_r<N/2. No gap between j and k enters those inequalities.

In the j/k annulus, the complete monic core cover and the accepted ratio lemma give C'/C>=-tau, B/C>=-M/2+sigma-tau and B'/C>=-M/2-tau, including tied nearest centers. Only C is divided out, where it is a unit. The three derivative gaps are bounded below strictly by

    M/2-L+p-sigma=p^2(p-2)/2+1/2>0.

The terminal-j cap applied directly to n provides a complete root cover counted with multiplicity and (d-1)L simple boundary roots. Its arbitrary-upper-prefix proof does not require the j/k gap. All other roots lie in exactly one of the j/k annulus, a k boundary, or a strict k interior. The latter has the accepted r-cover/outside partition. The preceding comparisons therefore exhaust the roots without an unjustified allocation among repeated residual classes.

Consecutive original P_n and P_(n-1) are coprime by their nonzero recurrence edges. The unchanged ordinary CD identity consequently makes the original algebraic-square kernel nonzero at every root. The H/P coordinate map has unit derivative near all relevant roots, which reduce to X=0 and not +/-2; H_n(0)=1 excludes a missing zero endpoint. Thus squarefreeness transfers to H_n. The algebraic p-adic embedding/Galois argument covers every characteristic-zero primitive phase, not only the embedding used to describe valuations.

## 6. Independent exact controls and explicit negative scope

Fresh reviewer code, not imported author code, checks the adjacent cap and unique equality at every h in selected full ranges; it computes complete Newton and differentiated-score maxima rather than sampling individual terms. It tests the ordinary g derivative in both factor orientations, parity compensation, actual shift margins and every k=3 boundary/annulus margin. It also confirms the negative general-k margin p-lambda in sample k=4,5 cases, without interpreting it as a multiple root.

A separate direct reconstruction uses the ORIGINAL shifted f/g recurrences and their ordinary derivative recurrences at all 20 level-3 centers in the fixtures (p,d,c)=(3,1,2),(5,1,2),(5,3,4),(7,1,2), with legal r=5,s=6. It substitutes the actual X centers i(q^(a/2)-q^(-a/2)) and the full disk variable, retaining every coefficient in a truncated T=q-1 square-root coordinate below 2v(p). Exact prime-field or quadratic-residue arithmetic and Lucas binomial coefficients certify these low-weight initials. Ordinary differentiation is performed in the recurrence BEFORE reduction; the controls never differentiate Y^p formally.

All 20 fixtures have the required nonzero Y^p initial of F, nonzero constant initial of F', exact constant unit H, and H'>=G0. At every noncentral tested center, H' actually attains G0. This independently rejects a stronger global derivative bound inferred from central behavior. Central derivatives can have larger value, and a zero truncated output is recorded only as a lower bound at the cutoff, not an exact zero polynomial.

Normal and optimized outputs are byte-identical, with 17,383 explicit checks. These are low-weight coefficient and transcription controls, not a characteristic-zero root census or an independent proof by finite enumeration. Source pins and author-file hashes are verified separately.

The report's general-k sufficient combined-derivative condition is correctly scoped as UNPROVED. Its strict valuation threshold really is needed to prevent later cancellation with FC'. Neither separate nonvanishing nor residual coincidence settles that condition. Only the k=3 family is accepted here.

No external repository, native table, or other external state was modified by this review. Existing publication holds, if any, are not released by mathematical acceptance alone.
