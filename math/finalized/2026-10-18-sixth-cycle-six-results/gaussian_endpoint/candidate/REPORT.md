# ALG-036: the critical Gaussian measurement endpoint

Date: 2026-10-18 UTC. Owner scope: ALG-036, priority 34. Status: theorem proved below; independent acceptance is a separate review step.

## 1. Result and exact scope

The critical exponent **alpha = 1/2 is impossible with a constant-fraction pathwise information deficit** in the actual measurement-only model. The estimate holds uniformly over independent seed laws, measurable transcript-only adaptive query policies, stopping rules, and measurable transcript-only decoders.

Let 0 < delta <= 1 and C > 0 be fixed. Let x have distribution CN(0,I_N), with E|x_j|^2 = 1. Let U_N be any fixed complex unitary N by N matrix. An algorithm draws coins R independent of x, chooses each complex-linear query a_t* x measurably from R and previous responses, and returns Xhat based only on R and its terminal transcript. Its terminal query matrix A has

    N - rank_C(A) >= delta N

almost surely, path by path. There is no raw-input read, uncharged nonlinear statistic, input-dependent coefficient information, or other side channel. Then, for every t > 1,

    Pr(||Xhat - U_N x||_infinity <= C N^(-1/2)||x||_2)
      <= exp[-(delta N/2) exp(-2 t^2 C^2/delta)]
         + exp[-N(t^2 - 1 - log(t^2))].                 (1)

The right side may of course be capped at one. Taking t = 2 gives the particularly simple estimate

    Pr(success) <= exp[-(delta/2) exp(-8 C^2/delta) N]
                   + exp[-(3 - log 4)N].               (2)

Thus success is exp(-Omega_(C,delta)(N)), hence o(1), for every fixed C and delta in the stated range. For delta > 1 there are no admissible schemes. The positive rate can be very small when C is large; its positivity is sufficient for the asymptotic result.

An almost-sure finite stopping time is permitted without a deterministic bound on the number of queries. Section 5 also covers a decoder of a countably infinite limiting transcript, if that broader interpretation of terminal transcript is desired. Independent decoder coins are included in R.

The key is a uniform translated cube estimate proved by successive coordinate conditioning. Independence of the output coordinates is not assumed. Neither a separated-coordinate maximum theorem nor an external Gaussian comparison inequality is needed.

## 2. A translated complex Gaussian disk

**Lemma 1.** If W ~ CN(mu,v) with v > 0, then for every center b in C and radius r >= 0,

    Pr(|W-b| <= r) <= 1 - exp(-r^2/v).                 (3)

**Proof.** After subtracting mu, the density is f(z) = (pi v)^(-1) exp(-|z|^2/v), radial and nonincreasing. Its positive superlevel sets are centered disks. For any centered disk D_s and translated radius-r disk B(b-mu,r),

    area(D_s intersect B(b-mu,r)) <= min(area(D_s), pi r^2)
                                 = area(D_s intersect B(0,r)).

Integrate this inequality over the density's level parameter, using the layer-cake identity and Tonelli's theorem. The translated disk has no more mass than B(0,r). Polar integration over B(0,r) gives 1-exp(-r^2/v). This also covers r=0. QED.

## 3. Uniform translated Gaussian-cube theorem

**Lemma 2.** Let P be any complex orthogonal projector on C^N, of rank d >= 1. Let Z ~ CN(0,P), allowing singular covariance. For every b in C^N and r >= 0,

    Pr(max_j |Z_j-b_j| <= r)
      <= product_(q=1)^d [1-exp(-N r^2/q)]             (4)
      <= [1-exp(-2N r^2/d)]^ceil(d/2)
      <= exp[-(d/2) exp(-2N r^2/d)].                  (5)

In particular, if d >= delta N,

    sup_(P,b) Pr(max_j |Z_j-b_j| <= r)
       <= exp[-(delta N/2) exp(-2r^2/delta)].          (6)

The supremum is over exactly the projector/translation class just stated; (6) is independent of orientation, center, and N except for its displayed rate.

**Proof.** We construct distinct coordinates j_1,...,j_d. Set P_0=P. At step ell, the current projector P_(ell-1) has rank d-ell+1. Since its diagonal entries are nonnegative and sum to that rank, choose a maximum-diagonal coordinate (with smallest-index tie breaking). Its conditional variance is

    v_ell = (P_(ell-1))_(j_ell,j_ell)
          >= (d-ell+1)/N > 0.                         (7)

For e=e_(j_ell), put

    P_ell = P_(ell-1)
            - P_(ell-1) e e* P_(ell-1)/v_ell.         (8)

If w=P_(ell-1)e/sqrt(v_ell), then w*w=1 and P_(ell-1)w=w. Therefore P_ell=P_(ell-1)-ww* is a Hermitian idempotent of rank d-ell. Its range is the old range intersected with {z:z_(j_ell)=0}. Previously observed coordinate variances are zero, so no coordinate is chosen twice. All choices depend only on P, not on Z or b.

Standard linear conditioning of a proper complex Gaussian, or its elementary orthogonal decomposition along w, shows that, conditional on Z_(j_1),...,Z_(j_(ell-1)), the coordinate Z_(j_ell) has distribution CN(mu_ell,v_ell). The conditional mean mu_ell may depend on all those observed values. Formula (8) is exactly its remaining covariance update; it is independent of the values. Singular ambient covariance causes no difficulty because the scalar variance v_ell is strictly positive.

Let E_ell be {|Z_(j_ell)-b_(j_ell)|<=r}. Lemma 1 applies to every conditional mean and gives

    Pr(E_ell | Z_(j_1),...,Z_(j_(ell-1)))
       <= 1-exp(-r^2/v_ell)
       <= 1-exp[-N r^2/(d-ell+1)].                   (9)

The event E_1 intersect ... intersect E_(ell-1) is measurable with respect to the variables being conditioned on. Successive use of the tower property therefore bounds the probability of their complete intersection by the product of the deterministic bounds in (9). The full cube event is contained in that intersection. This proves (4).

For the first k=ceil(d/2) choices, d-ell+1 >= d/2. Thus every corresponding factor is at most q=1-exp(-2N r^2/d). Discard the other factors, which are at most one. Then q^k <= exp[-k exp(-2N r^2/d)] <= exp[-(d/2)exp(-2N r^2/d)], proving (5). When d>=delta N, both d/2>=delta N/2 and exp(-2N r^2/d)>=exp(-2r^2/delta), proving (6). QED.

**Why conditioning on coordinates is legitimate here.** These artificial reveals are only a proof of a probability bound for the posterior Gaussian. They are not additional observations supplied to the original decoder. The chosen coordinates need not be independent, their means need not vanish after previous reveals, and the translation b can be arbitrary. The argument needs only a uniform scalar bound for every possible mean. This is precisely what Lemma 1 supplies.

## 4. The permitted adaptive measurement posterior

All random variables may be taken on standard Borel spaces, so regular conditional laws exist. Include all independent random choices in R at time zero. Write F_t = sigma(R,y_1,...,y_t), with rows a_t measurable with respect to F_(t-1). Inductively, conditional on F_t,

    x ~ CN(m_t,P_t),
    P_t = projector onto intersection_(s<=t) ker(a_s*). (10)

Initially m_0=0 and P_0=I_N. Given F_(t-1), the next row a=a_t is fixed. Put v=a*P_(t-1)a.

If v=0, the response y_t=a*m_(t-1) is already determined, and the posterior is unchanged. If v>0, decompose the Gaussian residual into its component along P_(t-1)a/sqrt(v) and its orthogonal complement. These proper complex Gaussian components are independent. Conditioning on y_t therefore gives

    m_t = m_(t-1) + P_(t-1)a (y_t-a*m_(t-1))/v,
    P_t = P_(t-1) - P_(t-1)aa*P_(t-1)/v.             (11)

As in (8), P_t is the projector onto the old kernel intersected with ker(a*). This proves (10) inductively, including arbitrary measurable branching of the query rows. Query rows and any internal states computed from the transcript add no information beyond F_t.

Let T be an almost-sure finite stopping time for this filtration. The event {T=t} belongs to F_t. On that event, conditioning on the stopped transcript gives the same Gaussian conditional law CN(m_t,P_t). Formally, apply the defining conditional-expectation identity on each event {T=t} and sum over the countable t. Thus

    x | F_T ~ CN(m_T,P_T),
    rank(P_T) = N-rank(A_T).                           (12)

Stopping supplies no extra information not already in the transcript. The decoder output is F_T-measurable. In output coordinates,

    U_N x = U_N m_T + Z_T,
    Z_T | F_T ~ CN(0,Q_T),    Q_T=U_N P_T U_N*,         (13)

and Q_T is an orthogonal projector of the same terminal rank d_T. Given the transcript, b_T=Xhat-U_N m_T is an arbitrary fixed shift. Lemma 2 is uniform in both Q_T and b_T, so it applies directly even when the posterior subspace and decoder shift depend on the transcript.

## 5. Optional countably infinite terminal transcripts

The usual model stops almost surely in finite time, already handled above. If instead a terminal decoder is measurable with respect to F_infinity=sigma(union_t F_t), and the terminal row span has rank at most N-delta N, the same result holds.

Indeed m_t=E[x|F_t] converges in L2 and almost surely to m_infinity=E[x|F_infinity] by the square-integrable martingale convergence theorem. Each positive-variance query reduces the projector rank by one, so along any path there are at most N such reductions. Consequently P_t converges, and in fact is eventually constant pathwise, to the orthogonal projector P_infinity onto the intersection of all query kernels. For each deterministic h in C^N, (10) implies

    E[exp(i Re(h*x)) | F_t]
      = exp(i Re(h*m_t) - (1/4)h*P_t h).

Conditional-expectation martingale convergence and the limits of m_t,P_t identify the corresponding conditional characteristic function at F_infinity as that of CN(m_infinity,P_infinity). This identification can first be made simultaneously on a countable dense set of h and then extended by continuity. Thus the Gaussian posterior and Lemma 2 still apply. No finite-time bound is being silently imposed on a broader limiting-transcript model.

## 6. From the cube bound to the relative-norm endpoint

Fix t>1 and put G={||x||_2<=t sqrt(N)}. On success intersect G,

    ||Xhat-U_N x||_infinity <= Ct.

This is an event inclusion. We **do not condition the Gaussian posterior on G**. First apply (6), with r=Ct, conditional only on the terminal measurement transcript and R, and then average. The pathwise deficit hypothesis gives

    Pr(||Xhat-U_N x||_infinity <= Ct)
       <= exp[-(delta N/2) exp(-2t^2 C^2/delta)].       (14)

Since ||x||_2^2 is a sum of N independent mean-one exponential variables, its moment generating function is (1-lambda)^(-N) for lambda<1. Markov's inequality with lambda=1-t^(-2) gives

    Pr(G^c) <= exp[-N(t^2-1-log(t^2))].                (15)

Adding (15) to (14) proves (1). Both constants in the exponents are strictly positive for fixed C>0, delta>0, and t>1.

If the terminal deficit condition holds except on an event of probability eta_N, the same proof gives (1) plus eta_N. A deficit only in expectation does not suffice, as the source's full-information-on-half-the-seeds example shows.

## 7. Every-fixed-input quantifiers

For a fixed scheme define

    p_N(x)=Pr_R(success on the deterministic input x).

The theorem states E_x p_N(x)<=epsilon_N, where epsilon_N is the right side of (1), capped at one. Thus a purported guarantee p_N(x)>=1-rho_N for every fixed input would force

    1-rho_N <= epsilon_N.

In particular no every-fixed-input high-probability promise with rho_N tending to zero is possible. This does not select the bad input after seeing the seed. There exists a deterministic x_N, independent of the seed subsequently drawn, whose success probability is at most epsilon_N. More quantitatively, for every eta>0,

    Pr_x(p_N(x)>eta) <= epsilon_N/eta.

The theorem is uniform over schemes, so these consequences hold for arbitrary admissible sequences of independently seeded adaptive schemes and decoders.

## 8. Application to the original block-local architecture

Retain the accepted original embedding and block-local information accounting. At least B>=floor(N/M)-2 completely occupied length-M blocks each contribute at least M-s unseen complex dimensions if at most s query rows are supported on each such fixed block. Arbitrary transcript-only choices of those rows do not change this pathwise rank count:

    d >= B(M-s).

For N>=6M, B>=N/(2M). If s/M<=1-gamma for a fixed gamma>0, then

    d >= (gamma/2)N.

Insert delta=gamma/2 in (1) or (2). In particular with t=2,

    Pr(success at alpha=1/2)
       <= exp[-(gamma/4)exp(-16C^2/gamma)N]
          + exp[-(3-log4)N].                          (16)

For M=Theta(log N) and fixed s, eventually s/M<=1/2 and N>=6M. Taking gamma=1/2 gives the explicit valid choice delta=1/4. More sharply, d/N>=(1-3M/N)(1-s/M) tends to one, so any fixed delta<1 is eventually allowed. This settles the original fixed-s high-deficit regime at its actual critical exponent.

The larger family s<M with M-s as small as one need only have d on the order of N/log N. No endpoint conclusion for that thin-deficit regime is asserted here.

## 9. Boundaries and retained results

- The source's conditional alpha<1/2 positive approximation theorem is unchanged. At that exponent the norm-scaled coordinate tolerance grows with N under Gaussian input; the fixed-radius endpoint argument does not contradict it.
- The accepted random-one-coordinate-omission control is unchanged. Its rank deficit is one, so it does not meet any fixed delta>0 hypothesis. At alpha=1/2 its deterministic-input failure bound is at most 1/(C^2 N), which illustrates exactly why a quantitative deficit is indispensable.
- No claim is made for d asymptotic to N/log N, arbitrary nonzero rank deficiency, or input-dependent coefficients chosen after uncharged input reads.
- This is an information-retention impossibility theorem, not an arithmetic lower bound for Fourier computation, a faster implementation, or a novelty/priority claim.
- No source package was imported, executed, or dynamically loaded. All computations described below are fresh self-authored controls. No external write, publication, or table edit was performed.

## 10. Evidence, reproducibility, and review

`controls/fresh_controls.py` is a newly authored standalone checker. It verifies exact rational/complex projector pivot identities and rank/variance inequalities, independently computes corresponding Gaussian Schur-complement covariances, checks all branches of a small transcript-only adaptive/stopping example, and runs numerical scalar disk sanity checks using the noncentral chi-square formula. It also checks exact coordinate-projector probabilities against the displayed bounds.

Recorded result: PASS. The checker covers 247 coordinate projectors, 29 dense complex projectors, 919 exact projector pivots, 150 exact Schur-complement comparisons, all seven adaptive test paths (including both query branches, early stopping, and four redundant queries), 180 scalar-disk checks, and 102 coordinate-probability bound chains. The largest floating bound-order discrepancy is 4.45e-16, within the explicit 2e-14 diagnostic tolerance.

The exact identities support transcription and edge-case checking; numerical disk calculations are diagnostics. Neither finite controls nor their software libraries replace the all-N mathematical proof in Sections 2–8. The program's JSON output records versions, seeds, test counts, and residuals. It is safe to rerun this newly authored checker; it does not execute any historical research program and makes no network requests.

`SOURCE_MANIFEST.json` identifies the exact source copies, their original local paths, verified SHA-256 hashes, controlling sections, and the pinned public Git blob where supplied. `MANIFEST.sha256` covers the complete deliverable payload except itself.

**Terminal candidate:** the requested constant-fraction critical endpoint is proved, with an explicit exponential rate, in the exact stated information model. There is no unresolved small-ball lemma for this scope. Independent review should focus on the successive-coordinate conditioning argument, posterior validity under stopping, and the unconditioned norm-event inclusion. Acceptance does not close broader ALG-036 questions outside this exact gate.
