Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, source identity and limitations are retained. Original source-report SHA-256: a20ef9c4b7b37f442fcd6259c5e49ebbeb161e9e833d38b2b467da761e12f90e.

# Independent acceptance: exact signed bank minimum eight over F8 at N=7

12 October 2026. Verdict: **ACCEPT, within the finite field and original signed additive grammar stated below.**

## Immutable object reviewed

The author candidate is `NEXT_MAGNETIC_SIGNED_N7_F8_Minimum_Eight_CANDIDATE_2026-10-12.zip`, 664,795 bytes, SHA-256:

`291a2124e49453714ebcf08a53bcde6f5afdff33762d039981df85389d285e1e`

Its root is `next_signed_f8_0214/`. All 43 manifest payloads and all source bindings were independently checked. No additional unlisted payload was present other than the manifest itself. The final mathematical run used a fresh extraction of these exact sealed bytes. Earlier examination of the mutable work directory is not the basis of acceptance.

`independent_verify.py` is a newly written reviewer control. It imports no author or predecessor program and executes none. The candidate's programs and sources are inert evidence. It uses a separate exponent-table implementation of F8 arithmetic, exhaustively checks the finite arithmetic, builds literal matrices and their finite geometric inverses, and verifies both inverse products. All certificate JSON is checked against these freshly computed matrices. `INDEPENDENT_CHECKS.json` and `INDEPENDENT_RUN.log` record the successful sealed-candidate run.

## Accepted theorem, exactly

Let K = F2[z]/(z^3+z+1). Fix N=7 and any of its six primitive seventh roots q, encoded 2,3,4,5,6,7 in the polynomial basis (1,z,z^2). With S e_t=e_(t+1), T e_t=q^t e_t and negative unnormalized Fourier target F[k,t]=q^(-kt), allow only additive sums of banks

B_(epsilon,delta)(alpha,beta;w) = (1/7) sum_(j=0)^6 w_j (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),

where epsilon,delta are integers +1 or -1; every alpha,beta,w_j lies in K; and Delta=1-alpha^7-beta^7 is nonzero for every bank. Then the exact minimum number of whole banks is eight for every such q.

This is a bank-count theorem over this one field. It is not an arbitrary-field or algebraic-closure theorem, a speedup, a new characteristic-zero minimum, a historical-priority result, or an enumeration of every phase-weight solution.

## Source grammar and prior knowledge

I read the pinned synthesis pages 1-5, particularly Definition 1.1, equations (1)-(5), and Theorem 1.2; the pinned common-node criterion; the N5 lower and upper notes; the prior N7 README; and the source scope guidance. The synthesis supplies exactly the grammar used above. Source paths and hashes are retained in the sealed candidate.

The counted object is the whole phase-weighted bank. Its seven inverse branches do not count as seven banks, and eight banks do not count as eight field operations or scans. No multiplication of banks, new Weyl generators, diagonal gauges, coordinate changes, permutations, or free transforms have been admitted. Arbitrary weights, vanishing weights, zero banks, coincident parameters, and equal nodes in different orientations are legal and explicitly accounted for.

The signs apply to integer powers of S and T. They are not scalar factors +1 or -1 inside K. The independent literal checks verify S != S^(-1), T != T^(-1), and both inverse identities for every root. Thus four distinct signed generator pairs remain present in characteristic two.

The original manuscript's domain is odd N>=3 with characteristic not dividing N. N1,N2,N4 are outside that domain. Preserve the already accepted N3 minimum four over its admissible fields and the N5 minimum five in characteristic zero. Most importantly, characteristic-zero N7 minimum eight was already accepted: the lower bound holds over characteristic-zero extensions containing q, with upper attainment in the specified cubic splitting field. This review does not reclassify that result as new or silently claim descent to Q(q). The new accepted increment is the complete bounded F8 case. N11 and the odd-N>=23 upper results remain unchanged.

## Complete legal-parameter reduction

For each orientation there are 64 pairs (alpha,beta). Since every nonzero element of F8 has seventh power one, exactly 50 pairs are legal: 49 with both parameters nonzero and the single pair (0,0). Exactly-one-zero pairs are forbidden. Across four orientations this is precisely 200 legal signed parameter slots, not merely a generic stratum.

At (0,0), all seven inverse matrices equal I, so the bank is an arbitrary scalar multiple of I. Its orientation has no effect. The four such slots collapse to a single scalar-identity subspace. There are no other legal zero-node or zero-beta degeneracies in F8.

For alpha,beta nonzero, Delta=1. Let D_l(alpha,beta) be the exact character projection of the seven literal inverse matrices in one orientation. The independent control checks, for every root, every orientation, every nonzero alpha,beta, and every l,

D_l(alpha,beta) = beta^l D_l(alpha,1).

It also checks the inverse character reconstruction of every literal branch. Since beta^l is invertible and the character matrix is invertible, the attainable seven independent sector amplitudes are exactly the same as at beta=1. This proves an exact normalization, not an enlargement of the legal class. Banks with the same (epsilon,delta,alpha) merge by adding these amplitudes. Merging cannot increase the bank count, including after cancellation or zero-weight removal.

The exact dictionary is therefore 28 nonidentity node-orientation atoms plus the optional identity. Repeated nodes do not require confluent atoms. Conversely every seven-sector amplitude choice on a nonidentity atom has legal raw weights over K. The control verifies the factor and reconstruction identities entry-by-entry, totaling 411,600 normalization scalar checks.

The reviewer computed all 8,400 legal phase inverses across the six roots, including the 336 branches in the displayed six witnesses. Every inverse was checked on both sides, totaling 823,200 scalar product equalities. As a separate degeneracy check, all 2,352 branches with forbidden exactly-one-zero parameter pairs were directly found singular. This does not authorize adding singular banks to the grammar.

## Exact lower bound

The reviewer obtains all sector columns from literal phase projection and Weyl coefficient extraction. It independently verifies the candidate's Gaussian-factor formula against every one of those literal columns, including the a=0 axes and b=0 row, and verifies cross-row zeros. The target is extracted from the literal negative Fourier matrix, not assumed from the supplied formula. It agrees with q^(2(a+b)^2). Here 1/7=1 and the source Gauss factor C is 1: all nonzero t and -t terms cancel in characteristic two.

At b=1, a=1,...,6, all delta=-1 atoms and the identity vanish. At b=6, the analogous delta=+1 atoms and the identity vanish. These vanishings were checked on the literal dictionary.

For each root and each delta sign, all 470 subsets of at most three of the 14 relevant atoms have an exact separating vector y with y dot target=1 and y dot column=0. The reviewer checks all 5,640 supplied separators, validates their domains, verifies exact combinatorial key coverage without duplicate or missing subsets, independently recomputes nonmembership and rank, and checks all reported ranks. One deliberate perturbation of each separator is detected.

It follows that every normalized representation needs at least four nonidentity atoms of each delta sign. Hence it needs at least eight banks. The normalization proof transfers this bound to every original presentation, including repeated parameters and the identity degeneracy. This covers all supports of at most seven among the 29 normalized slots (2,182,396 supports per root) by a mathematically complete edge reduction; it is not a claim that all global subsets were individually enumerated.

## Attainment and full minimum-support classification

The reviewer independently enumerates all C(14,4)=1001 four-atom subsets for each edge, then tests every eligible positive/negative edge pair on all seven coefficient rows. The eligible edge counts are 15 per sign at q=2,4,6 and nine per sign at q=3,5,7. Thus all 918 eligible pairs are classified, and the lists agree exactly with the sealed candidate. The accepted support counts in q=2,...,7 order are:

10, 2, 10, 2, 10, 2.

There are 36 accepted normalized supports across the six roots. Every eight-bank representation must have four nonidentity atoms of each delta sign and no identity bank, so this is exhaustive for normalized minimum supports. It does not enumerate the affine families of phase weights or claim uniqueness of a representation.

For each root, all eight displayed nodes, their orientations, beta=1, Delta=1, sector amplitudes and 56 raw phase weights pass the independent checks. The raw conversion is exactly

w_j = sum_l h_l q^(-epsilon delta j l).

There is no omitted 1/7, Gauss constant, guard factor, or Fourier-sign correction. All 49 original matrix entries agree per root, for 294 witness entries total. The reviewer additionally verifies reconstruction of every matrix unit from Weyl coefficients, exposing the full-output basis semantics directly.

The seven row ranks are (7,5,7,7,7,7,5), and the two deficient rows are explicitly checked compatible. Their ranks alone were not used as an existence argument. All banks are nonzero; deleting any displayed bank fails. Every nonzero perturbation of every witness raw weight fails (2,352 mutation tests), and replacing the negative Fourier target by the positive one fails for every root.

## Paid cost audit and open speed question

The supplied construction contains 56 inverse branches per root. In a deliberately unoptimized dense prepared application, store all 56 inverse matrices, apply each to the input, scale by its phase weight, and accumulate. Charging even zero weights gives 3,136 field multiplications and 2,744 field additions per vector, and 2,744 stored inverse entries plus 56 weights, parameters, root powers and working vectors.

The reviewer independently instrumented this evaluator on seven basis vectors, zero, all ones and a nonconstant vector for each root (60 applications). Each application exactly matches the Fourier output and exactly the stated charged operation counts. Because the full matrices agree and the evaluator is linear, correctness is for every vector, not just those test inputs.

The preparation audit confirms 392 multiplications and 336 additions for the 56 raw weights from sector constants. The declared conservative Gauss-Jordan bounds for 56 augmented 7-by-14 inverses are 38,416 multiplications, 32,928 additions and 392 scalar inversions. Checking both inverse products separately costs at most another 38,416 multiplications and 32,928 additions. The candidate explicitly leaves branch assembly, finite table preparation, guard checks, indexing, memory traffic and input/output as additional paid finite work. These figures are an arithmetic baseline, not a complete machine-runtime bound.

Search work is separately paid. The declared 17,652 edge-subset tests and at most 6,426 row-feasibility solves for 918 pairs are arithmetically consistent with the exhaustive coverage. Given the finite witness, an application does not require repeating the proof search, but preparation remains paid.

A direct dense 7-by-7 Fourier application is 49 multiplications and 42 additions under the same convention. This baseline is therefore no speed improvement. No all-size shared evaluator, asymptotic FFT result, numerical conditioning, bit-complexity improvement, or hardware performance conclusion is accepted.

## Scope and remaining work

Accept the bounded F8 exact minimum and full normalized minimum-support classification, retaining all source-model restrictions. The broader `NEXT-MAGNETIC-SIGNED::larger-minima` gate remains **progressed_open**: this one finite-field obligation is closed, while further sizes/fields and a genuinely improved paid shared evaluator remain open.

The already accepted characteristic-zero N7 theorem is preserved explicitly. This finite-field increment does not replace the N5 results or create new unrestricted field, size or performance conclusions.

No blocking mathematical or implementation defect was found in the sealed candidate. A minor editorial phrase in its last sentence says “both executed controls” even though it contains three author controls; that does not alter a theorem, certificate, count, or this acceptance.
