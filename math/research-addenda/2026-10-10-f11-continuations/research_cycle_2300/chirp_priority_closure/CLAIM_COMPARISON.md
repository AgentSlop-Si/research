# Common-chirp primary-source closure attempt

10 October 2026 UTC. Bounded comparison of the three sources left open by the reviewed manuscript. This report makes no manuscript changes or new mathematical claims.

## Decision

**None of the three original-body gaps is closed.** The pass found a new, specific acquisition lead for Lindsay, but it did not yield readable theorem pages. Derin remains abstract-only, Applebaum remains indexed-primary-passage evidence, and Lindsay Theorem 5B remains indirectly attributed through an inspected later primary paper. These are access/comparison gaps, not new proof gaps in the finite-field recognizer.

No new theorem-level evidence changes the existing disposition. The exact arbitrary-center eliminant and full-input finite-field decision composition remain candidates for further comparison, with historical priority unresolved. Missing matches and access failures are not originality evidence.

## 1. Frozen comparison target

The target is the contract in the cycle-2224 manuscript and concordance, supported by cycle-2020 proof and cycle-2033 local review, rather than an unspecified chirp-recovery claim.

For supplied certified prime p, supplied exact-order-N root omega in F_p, N dividing p−1, N≥3 and 1≤r≤floor(N/3), the input is every complete raw vector x in F_p^N. The algorithm decides whether

    x_j = omega^(a j²) sum_(ell=1)^s gamma_ell omega^(u_ell j), 0≤s≤r,

with distinct grid frequencies and nonzero listed coefficients. Neither phase nor frequencies are supplied. Zero is handled separately by the empty representation. For nonzero members an allowed interior center exists; if the center search fails, the algorithm rejects. For any chosen allowed center c with x_c nonzero, define

    E(z) = det[x_(c+i−j) z^((i−j)(i−j−1)/2)]_(0≤i,j≤r).

The key claims to match are not merely that a determinant can locate a nuisance parameter:

- E(0)=x_c^(r+1)≠0 for every such center, without a generic-position condition.
- Degree is at most D=binom(r+2,3); equality need not hold.
- Every true phase z=omega^(−2a) is a root.
- Each leading principal minor has nonzero constant term, yielding units for the truncated-polynomial-ring recurrence.
- The complete phase grid has L=N/gcd(2,N) elements; at most C=min(D,L) candidates survive. If E reduces to zero modulo z^L−1, every phase is retained, with the original E supplying the degree/root bound.
- All survivors receive frequency-grid, coefficient and complete-vector verification. Failed candidates are paid for. Acceptance includes the positive-sign unnormalized dense DFT; rejection supplies neither an arbitrary-input DFT nor a promised succinct negative witness. Budget abortion is UNKNOWN.

For dyadic N, the source ledger is

    T(r)+D+N log(min(D+1,L)+2)
      +C[N log(r+2)+r²]+Nr+N,
    T(r)=O(r²(D+1)^(log₂3)).

It implies O(Nr³ log(r+2)+r^(2+3log₂3)) additions/multiplications, with O(1+r⁴) separate scalar inversions and O(N+r⁴) field elements. The all-length decision envelope is separately O(Nr^(2+log₂3)+r^(2+3log₂3)). Optional certification, integer work and word/bit conversion remain separately charged. A literature cost must be matched to these variables, interfaces and failure semantics before it can be compared.

## 2. Source-by-source conclusion

### C7: Derin 1987

H. Derin, *Estimating Components of Univariate Gaussian Mixtures Using Prony's Method*, IEEE TPAMI 9(1), 142–148. [DOI](https://doi.org/10.1109/TPAMI.1987.4767880); [PubMed record](https://pubmed.ncbi.nlm.nih.gov/21869385/).

Inherited evidence establishes moment-based Gaussian-mixture estimation under equal-variance or equal-mean conditions using Prony's method. It does not identify whether the common variance is supplied, a specific variance eliminant, its degree, exceptional cases, or an every-input rejection theorem.

The new connected-index lookup returned the exact paper but no full-text URL. Exact-title/DOI and University of Massachusetts domain searches did not supply a readable original. Previously unsuccessful or denied IEEE routes were not pursued again.

**Still needed:** original pp.142–148, including the equal-variance setup and elimination/reconstruction equations. Until read, every comparison of uniform nonvanishing, determinant degree, candidate completeness or rejection cost is **unknown**, not negative.

### C8: Applebaum–Howard–Searle–Calderbank 2009

*Chirp sensing codes: Deterministic compressed sensing measurements for fast recovery*, ACHA 26(2), 283–290. [DOI](https://doi.org/10.1016/j.acha.2008.08.002); [Duke publication record](https://scholars.duke.edu/publication/763127).

The inherited indexed journal passages describe complex chirps on a prime-length index grid, delay products, FFT peaks, dechirping and residual/iteration stopping. Theorem 1's sparse-minimizer uniqueness statement is distinct from correctness of the peak decoder on every input. Its O(MK log K) and all-shifts O(MK² log K) costs are not a matched F_p full-input decision ledger.

Fresh Duke and publisher routes did not expose the complete journal body. A verified AIM workshop link led to a Rice preprint endpoint that timed out. A CiteSeer preprint open returned a gateway error. No preprint was silently equated with the journal version.

**Still needed:** readable complete pp.283–290, especially §§3–6 and their assumptions. The inherited difference in input/field model is supported; complete-paper exclusion of the exact E/composition remains **unresolved**.

### C9: Lindsay 1989

B. G. Lindsay, *Moment Matrices: Applications in Mixtures*, Annals of Statistics 17(2), 722–740. [DOI](https://doi.org/10.1214/aos/1176347138); [original publisher location](https://projecteuclid.org/journals/annals-of-statistics/volume-17/issue-2/Moment-Matrices-Applications-in-Mixtures/10.1214/aos/1176347138.full).

The new connected-index lookup located an apparent 19-page original scan at a [SciSpace PDF endpoint](https://scispace.com/pdf/moment-matrices-applications-in-mixtures-2ri0trsa1h.pdf). The web extraction exposed only a digitization notice. Screenshots were unavailable, and direct retrieval returned HTTP 403; that route was stopped.

Theorem 5B was therefore not read. Its variance-root-selection attribution remains inherited from Agostini–Améndola–Ranestad §4.3, not newly verified in Lindsay. A generated SciSpace methods summary had no source context and was excluded from theorem evidence.

**Still needed:** the original Theorem 5B, all definitions and hypotheses on which it depends, and its surrounding argument. No theorem page number is invented.

## 3. Claim-level comparison matrix

“Unresolved” means the source does not currently support either a correspondence or an exclusion. It does not mean the paper lacks the result.

| Target feature | Derin C7 | Applebaum C8 | Original Lindsay C9 |
|---|---|---|---|
| Raw complete F_p vector; supplied prime/root; arbitrary valid-contract input | Inherited abstract uses moments of Gaussian mixtures; full interface unread | Inherited passages use complex-valued measurements; prime indexing is not F_p-valued arithmetic | Original setup unread; later primary discussion concerns moments |
| Unknown shared quadratic factor rather than supplied phase | Equal variance is stated; supplied versus unknown variance unresolved | Chirp parameters are estimated; exact common-phase restriction comparison incomplete | Shared-variance procedure attributed indirectly; original hypotheses unresolved |
| Determinant parameter search | No body-level determinant known | Inspected passages describe peak/dechirp search; complete-body determination pending | Later primary text gives a determinant; original theorem not inspected |
| Arbitrary nonzero-center E(0) guarantee and unit leading minors | Unresolved | Exact E contract not established by inspected passages | Unresolved |
| Degree D=binom(r+2,3), finite phase-grid completeness and zero-reduction handling | Unresolved | No matching contract established by inspected passages | Unresolved |
| All-input recognition with every failed candidate and rejection charged | Unresolved | Sparse uniqueness and decoder costs do not establish this contract | Unresolved |
| Separate inversions, storage, certification and dense DFT on acceptance | Unresolved | Different output/cost model in inherited passages; full inspection pending | Unresolved |

The existing positive antecedent evidence remains important: Agostini–Améndola–Ranestad and Wu–Yang explicitly give shared-variance determinant search followed by atomic recovery; Gutknecht–Hochbruck gives the classical nonsymmetric predictor mechanism. Those primary-body comparisons were already completed in cycle 2118 and are not discoveries of this pass. No claim to a new general nuisance-parameter elimination framework or Levinson algorithm is justified.

## 4. Enumerated legitimate routes and stopping point

The pass used the following bounded route families:

1. Read the frozen manuscript concordance, access receipt, cycle-2118 report/source log, and cycle-2218 readiness assessment.
2. Search exact paper titles, authors and DOIs through public search and the connected SciSpace index.
3. Search relevant author/institutional domains: UMass for Derin, Duke/Calderbank and arXiv for Applebaum, Penn State for Lindsay.
4. Open verified official or scholarly repository links: Duke; ScienceDirect; JSTOR; Project Euclid's indexed PDF route; AIM's actual Rice link; and the previously identified CiteSeer preprint.
5. For Lindsay's newly located scan, attempt standard web PDF extraction and page rendering, then one direct download after rendering failed technically. The download returned forbidden and was not retried.

Outcomes, exact URLs, and the distinction between earlier versus current failures are in SOURCE_ACCESS.json and ROUTE_LOG.md. Metadata, abstract repetitions, a page count, and generated summaries do not advance access depth.

Stop here. Further search repetition is not justified by an unresolved result alone. The next useful evidence is a legitimately readable original copy, such as an authorized user-supplied PDF or a functioning open author/publisher deposit. This report does not authorize outreach, account access, payment or uploading a paper.

## 5. Manuscript consequence

Retain the current qualifications. A stronger statement that these three sources have been fully compared would be unsupported. The manuscript can continue to present its locally proved exact recognizer with explicit unresolved historical priority. No ranking change, theorem extension, new fusion, or novelty certification follows from this pass.

The report and receipts are local. No manuscript, repository, Sheet, external message or submission was changed. The access log explicitly records the SciSpace results-table column operation rather than claiming that every research-tool operation was purely nonmutating.

