# ALG-016 and ALG-020: exact successor comparison gates

Prepared 16 October 2026 UTC. Candidate for independent review. No external writes and no supplied research programs were executed.

## Decision and scope

The named primary-source comparison gates can be completed for ALG-016 (Research overview row 189) and ALG-020 (row 192), subject to independent acceptance of this report. Both parent records remain **TO RESEARCH, priority 34**. No theorem, executable, production, priority, novelty or canonical-count promotion is proposed.

Fresh native reads include full Catalogue rows 127/131, novelity breakthough rows 120/123 and overview rows 189/192. All six owning views retain the comparison as unfinished. The earlier algorithm inventory explicitly marked each `NEW_COMPARATOR_OR_CHANGED_MODEL_SCOPE_NOT_SELECTED`. ALG-016's old single-port source already cited Sherman–Morrison generically, and the mathematical review already checked the update identity. This report does not count either as new proof. It supplies the missing exact published-formula, block-dimension, singular-coupling, source-interface and cost comparison. ALG-020 is a separate finite nilpotent-kernel Padé task; it does not repeat ALG-014's supplied-mode sparse-multiple evaluator comparison.

The recorded stop for each selected row is an exact primary-theorem hypothesis/formula/cost mapping or a qualified nonmatch, while preserving guards and proof status. The mappings below meet that comparison stop. The original outstanding constructions remain open.

Repository baseline: `0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4`. Workbook: https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit . Source index: `math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json`. Fresh owners, rather than the older locally saved index, control this proposal.

## 1. ALG-016: Schur closure, rank-one edits and paid reuse

### Source binding and preserved domain

The full canonical multiple-port README is 13,207 bytes, SHA-256 `322f0d1a5a76019fcd8102aaeab68f0302fe6effa83dc7fdc42339de552ec134`:
https://github.com/AgentSlop-Si/research/blob/0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4/math/archive/objects/32/322f0d1a5a76019fcd8102aaeab68f0302fe6effa83dc7fdc42339de552ec134__322f0d1a5a76019fcd8102aaeab68f0302fe6effa83dc7fdc42339de552ec134__README.md

Also read in full: its independent review `33247cdb1153f0205e9c15aeaa40e2d31183758e03322fb275a1509b5a00641b` (6,106 bytes); preceding coordinate-port README `65eaef1e9c9049a58fb028c891c0bd5e40e7e3ec693b71d9e28f17c5a500187c` (8,947 bytes); preceding review `ebaebdba4b83432857c81c741138ab32b14f3e806cc26d1cd53359024dfa6bba` (5,266 bytes); and the complete ALG-016/ALG-020 entries of the current REVIEW-16 outcome ledger, whole-file SHA-256 `46f76abe46263e0a4ef6a62eb4d017a33cc875b49f850fa073ee6ae0b5baf313`. Historical execution counts remain attributed evidence, not rerun acceptance.

Retain an exact field, invertible N, supplied q of exact order N, the boundary-corrected q-Weyl operators, and TK=JT. In the specified graph R>=1, h=R−1, U and V have N rows and d columns, Lambda is d by d, and V's columns are structured coordinate/Krylov observations. Columns need not be independent; Lambda need not be invertible. Transpose is algebraic transpose. The edit reuses identical sources and injection pattern and an already accumulated old solution. Sources and targets are disjoint; dirty background is preserved.

### Published formula and exact block substitution

Hager, *Updating the Inverse of a Matrix*, SIAM Review 31 (1989), printed pp.221–222, equations (1), (2), (5a) and (6a–b), gives the low-rank inverse and its block-Schur derivation. Section 2, p.224, separates solving the base system, preparing correction columns, solving the small system and forming outputs; it also warns about conditioning. This is the directly inspected published formula source, not a certification of earliest priority:
https://people.clas.ufl.edu/hager/files/update-1.pdf

Here is the exact substitution, derived from the owner's graph. Stack all R blocks. Define D by (Dz)_0=z_0 and (Dz)_r=z_r−Jz_(r−1). Let E_r inject one N-vector into block r, and let b stack the injected T x_s terms. Then

F_graph = D − E_0 U Lambda V^T E_h^T,
D^−1 E_0 U = stack_(r=0,...,h)(J^r U),
E_h^T D^−1 E_0 = J^h.

Set Hager's A=D, U_H=E_0 U Lambda and V_H=V^T E_h^T. Dimensions are RN by RN, RN by d, and d by RN. His capacitance matrix becomes exactly

S = I_d − V_H D^−1 U_H = I_d − G Lambda,
G=V^T J^h U.

With w=D^−1 b and g=V^T w_h, equation (1) gives every block

z_r = w_r + J^r U Lambda S^−1 g.

This placement of Lambda avoids any inverse of Lambda and therefore includes singular coupling and redundant ports. Hager's block determinant relations yield det(F_graph)=det(D)det(S)=det(S). Direct block elimination proves the same identity over the owner's field without importing numerical assumptions. Thus singular S means the full system is singular. It does not mean every forcing is inconsistent; some forcings can have multiple solutions. The contract correctly rejects rather than selecting a regularized answer.

For Lambda_new=Lambda+a b^T, substitute A=S, u=Ga, v=b^T in Hager's equation (2). Set z=S^−1 Ga, v^T=b^T S^−1 and theta=1−b^T z. Then

S_new^−1 = S^−1 + z v^T/theta,
det(S_new)=det(S)theta.

Using only this identity and theta+b^Tz=1 gives

(Lambda+ab^T)S_new^−1 − Lambda S^−1
  = (a+Lambda z)v^T/theta.

Consequently Delta z_r=J^r U(a+Lambda z)v^T g/theta. This is a rank-at-most-one correction of the entire RN-output linear map. Zero edit factors may give rank zero. The update is legal exactly when theta is nonzero, assuming the old S is invertible. These formulas establish the algebraic match, including the full output and singular branches, not a new compiler replay.

### Cayley, spectral and Schur qualifications

Higham–Lin, *Matrix Functions: A Short Course* (2013), Definition 3.2 and §3.2, describes polynomial representation modulo the minimal polynomial over the complex numbers; §§6.3–6.7 discuss spectral/Schur computation. For f(t)=1/t and nonsingular F_graph this represents its inverse, but does not supply cheap preparation or application:
https://eprints.maths.manchester.ac.uk/2067/1/covered/MIMS_ep2013_73.pdf

Independently over any owner field, if the minimal polynomial is mu(t)=a_0+a_1t+...+t^k with a_0!=0, then F_graph^−1=−(a_1 I+...+F_graph^(k−1))/a_0. This is a Cayley-style representation, not a degree or runtime reduction. A diagonal spectral sum requires a split squarefree minimal polynomial; the owner's field and arbitrary ports do not guarantee that. Jordan/Hermite derivatives handle repeated complex eigenvalues, but complex numerical Schur methods cannot be transplanted as exact finite-field algorithms. No spectral-gap, convergence or stability hypothesis is needed for the exact Schur-complement algebra above.

### No hidden first-transform elimination

The graph forcing already contains one T x_s per injection. The accepted implementation charges its triangular ADD_T at 3N(N+1)/2 scalar instructions each. For M injections the retained total is

3MN(N+1)/2 + 2(R−1)(6N−3) + sum_active(6m_l+3k_l−4).

Initial preparation remains O(NL+Nd^2+d^3), plus dMN injection-functional additions, root-plan construction/checks, stored orbit rows, gate generation and reciprocal preparation. A coupling edit costs O(d^2+dMN+RN) preparation and O(QN+RN) online scalar work, with all RN outputs paid. The small inverse formula does not include these costs for free.

For structured ports, T^T e_j is an explicitly supplied row of the kernel, and the covariance transports that row by K^T. This genuinely avoids a new transform in that preparation. For arbitrary dense observation v, T^T v is not thereby cheap. The edit's zero new T calls depend on reusing the same old-source solution; independent new input banks cannot be substituted. The multiple-port helper's local removal of source-ID sorting is retained, while older helper construction still needs its sorting overhead. Hager's generic formula neither implements this dirty-state source interface nor clears its numerical or bit-cost obligations.

**Disposition:** exact Schur/low-rank update mechanism match, with explicit Cayley/spectral and complete-interface cost qualifications. The named comparison is complete. An economical complete fresh Fourier representation, production source replay, numerical/bit-model validation and historical priority remain unresolved.

## 2. ALG-020: finite Padé obstruction versus Prony recovery

### Source binding and domain

The full canonical README is 4,084 bytes, SHA-256 `added4a0f022537cb7c72a52e191a28a6eeb640575ba05af61d2e7eb6ef4f3f3`:
https://github.com/AgentSlop-Si/research/blob/0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4/math/archive/objects/ad/added4a0f022537cb7c72a52e191a28a6eeb640575ba05af61d2e7eb6ef4f3f3__added4a0f022537c__README.md

The owner's accepted statement has N=2^L>=2, primitive q and N invertible in the exact field. With t_j=1/product_(a=1,...,j)(1−q^a), H(z)=sum_(j=0,...,N−1)t_j z^j, and minpoly(C)=z^N, it states

H(C)=p(C)r(C)^−1, r(0)!=0 implies deg p+deg r>=N−1,

and the bound is attained. This report preserves the existing proof and all its guards.

### Exact recurrence map and a finite-prefix distinction

Massey, *Shift-Register Synthesis and BCH Decoding* (1969), §II equation (2), §III Theorem 3 and §IV Theorem 4/corollary, printed pp.122,124–126, relates finite-prefix recurrence constraints and rational series. The finite and infinite formulations are different; a finite-prefix fit does not certify the unseen tail:
https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf

The following comparison is derived from the owner. Normalize r(0)=1. The operator equality is exactly rH=p modulo z^N, because minpoly(C)=z^N. If deg p=m and deg r=d, this imposes

t_j + sum_(ell=1,...,d) r_ell t_(j−ell)=0 for m<j<N,

with t_k=0 for negative k. It is a finite Padé condition. A length-s LFSR on the first N coefficients corresponds to such a congruence with deg r<=s and deg p<s. Conversely these degree inequalities give the finite recurrence from index s onward. For a general p/r candidate, the register length needed to generate its entire rational continuation is max(deg r,1+deg p) after cancellation, not deg r alone.

For N=2n the accepted determinant gives an especially precise interface comparison. The n by n Hankel matrix H_n=(t_(i+j))_(0<=i,j<n) is nonsingular: its largest index is N−2, within the source guard. If a register had length s<n, its associated degrees would sum to at most 2s−1<N−1, contradicting the accepted obstruction. A length-n register does exist: solve the n recurrence equations at j=n,...,2n−1 for r_1,...,r_n. Reversing columns turns their coefficient matrix into H_n. This solution is unique. Set p to the first n coefficients of rH. The degree theorem now forces deg p=n−1 and deg r=n. A common polynomial factor could be cancelled without changing the congruence (it is a unit at zero), violating the same bound; hence p and r are relatively prime.

Thus the finite N-term kernel has unique minimal register length N/2 and an extremal Padé pair of type (N/2−1,N/2). This is a direct comparison consequence of the retained Hankel certificate, not a newly executed reconstruction or a new historical-priority claim. It neither says that H as a full polynomial equals p/r nor supplies the next original q-factorial coefficient. Indeed t_N would divide by 1−q^N=0. If instead H is extended by zero coefficients, its rational function is H/1 and its minimal infinite-register length is N, because t_(N−1)!=0.

All-coordinate equality matters. A recurrence discovered from fewer coefficients can fail later, so certification of H(C) requires the whole mod-z^N congruence. Equality on one input vector is also insufficient in general: a vector annihilated by a lower polynomial probes only a quotient of the full operator. A supplied cyclic vector could certify the polynomial identity through an independently checked cyclic-basis argument; no such probe is silently assumed free.

### Prony and sparse interpolation: qualified interface nonmatch

Van der Hoeven–Lecerf, *Sparse polynomial interpolation: Faster strategies over finite fields* (2 May 2024), §5 Algorithm 4, printed pp.13–14, takes black-box polynomial evaluations and degree/term bounds. It constructs a Padé denominator, finds its roots, takes discrete logarithms and solves for coefficients; §1.1 distinguishes field and bit models, and the later faster strategies include additional hypotheses:
https://www.texmacs.org/joris/ffsparse/ffsparse.pdf

For f(x)=sum_(a=1,...,s)c_a x^(e_a), evaluation on a suitable geometric progression gives f(omega^j)=sum_a c_a lambda_a^j, lambda_a=omega^(e_a). Distinct active nonzero modes give a rational generating series with denominator product_a(1−lambda_a z) and numerator degree<s. Applying the owner's obstruction to any such representation of all N kernel coefficients yields 2s−1>=N−1, hence s>=N/2. Equivalently its size-n Hankel factorization V diag(c) V^T has rank at most s, while the owner has rank n. Repeated/cancelled modes must first be combined; zero weights do not count as active modes.

No matching upper bound on Prony mode count follows. The extremal Padé denominator need not split into simple base-field roots or into the permitted omega-grid. Repeated roots, extension fields and exponential-polynomial continuations have different interfaces. This is a qualified nonmatch between a universal nilpotent-operator representation barrier and black-box sparse polynomial recovery. It is not a statement that the source's entire q-root-of-unity theorem appears in Massey or the interpolation paper.

### Complete cost boundary

ALG-020 is an algebraic degree obstruction, not an evaluator or a time lower bound. Root preparation, t_j construction, finding p/r, denominator-unit verification, implementing p(C) and r(C)^−1, all N inputs/outputs and any failed attempts still belong to a proposed algorithm's ledger. Sparse interpolation's evaluations, root finding, discrete logs, extension arithmetic and complete verification are separate paid steps; its input oracle is not supplied by the obstruction. High degree may coexist with cheap sparse powers, fast convolution or shared subgraphs. A product of bounded-total-degree rational functions in this same C is covered after combining and cancellation, but sparse high-degree factors and different noncommuting operators are outside that restriction. Preserve the source's tail-fusion example and do not infer quadratic work, a general FFT lower bound or a runtime improvement.

**Disposition:** the finite Padé/LFSR mechanism and exact input/output mapping are complete, with a qualified Prony/sparse-interpolation nonmatch and explicit full-cost boundary. The full arbitrary-input fast-convolution question, production qualification and historical priority remain open.

## Review and application requirements

The accompanying local proposal contains exact before-text guards and prefix-only after-text for current-gate, pass/stop and comparison-evidence cells. It changes no statuses or priorities. Apply only after independent review, fresh native stable-ID/preimage checks and preservation of every earlier byte and all unrelated cell metadata. This report's source findings do not authorize an external write. No publication URL is guessed. No primary text was copied into the report beyond short identifiers; formulas and mappings above are independently written.

One Henderson–Searle Cornell PDF request returned HTTP429, and its legacy landing route did not supply the body. Neither result supports an internal theorem citation. The accessible Hager body supplies the matrix formula mapping; missing historical text is not evidence of novelty.
