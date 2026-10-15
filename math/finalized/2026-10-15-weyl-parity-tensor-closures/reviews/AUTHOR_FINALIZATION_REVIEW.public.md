# Author finalization review: Weyl, parity depth, and tensor cuts

Publication derivative: mathematical reasoning, source comparisons and scientific boundaries are retained. Workbook bindings and application mechanics are omitted. Original and export hashes are recorded in PUBLIC_PROVENANCE.json.

Date: 2026-10-15 UTC. Status: local proposal; no external write performed.

## Recommendation

Close the three named theorem records at their already accepted, explicitly guarded scopes. Their full pinned proof/review bodies and accepted per-ID decisions have been read. The specific primary-source comparisons below replace the generic comparison queue with attributed overlap and qualified nonmatches. They do not establish worldwide priority or turn the results into unrestricted Fourier algorithms/lower bounds.


## 1. M-WEYL-RESIDUAL

### Exact theorem and independent reasoning

Let N>=2 and let omega be a primitive Nth root in the supplied field. Put Z e_k=e_(k+1), D e_k=omega^k e_k, and F[j,k]=omega^(jk), with a supplied normalization if desired. From MZ=DM, column k is D^k times column zero, so M[j,k]=b_j omega^(jk). The second equation MD=Z^-1 M forces b_(j+1)=b_j, including the cyclic boundary. Thus M=cF, with no invertibility premise on M. A deterministic scalar calibration fixes c=1.

For the complex metric use the unitary normalization of F and omega=exp(-2 pi i/N). Writing K=F* M turns the defects into [K,Z] and [K,D]. Expanding K in the orthonormal basis D^a Z^b/sqrt(N) gives defect-squared weights |1-omega^a|^2+|1-omega^b|^2. Only the scalar coefficient has zero weight. The minimum positive weight is 4 sin^2(pi/N), so the sharp residual-to-distance gap is 2 sin(pi/N). M=FD attains it. This is distance to the scalar Fourier family, not a replacement for calibration.

For a fixed linear map over F_q define A=MZ-DM, B=MD-Z^-1 M and rho=rank([A;B]). The accepted vectors for one common uniform probe are exactly ker([A;B]), of size q^(N-rho). Conditional on passing deterministic calibration, h independent uniform probes therefore pass with probability q^(-h rho). One calibration call plus the three calls M r, M(Zr), M(Dr) per probe yields 1+3h calls. A wrong scalar fails calibration even when rho=0.

### Primary attribution comparison

Tyson, Theorem 5, credits Weyl and gives the complex invertible Fourier characterization by conjugating shift and twist. Set R=Z and T=conjugate(D); conjugate the candidate to reconcile signs. This matches exact uniqueness on that subdomain. The noninvertible/splitting-field extension and quantitative certificate here have direct proofs above. [Tyson, section 2](https://arxiv.org/html/quant-ph/0306144#S2)

Freivalds, Theorem 3, tests a fixed matrix-product defect on independent signed Bernoulli (Rademacher) vectors. The common linear-defect testing mechanism matches. Its real/signed-Bernoulli theorem is not the exact F_q joint-kernel probability or the Weyl oracle-call ledger; those follow here by rank-nullity. [Freivalds 1979, pp. 59–60; PDF pp. 68–69](https://raganwald.com/assets/fractran/Mathematical-Foundations-of-Computer-Science-1979-Proceedings-8th-Symposium-Olomouc-Czechoslovakia-September-3-7-1979.pdf#page=68)

The inspected primary statements do not claim the complete sharp-gap/calibrated-verifier package. This is a qualified partial match, not evidence that the package is historically new. There is no unfilled internal lemma in the accepted scope.

### Retained boundaries

The norm statement is complex, and its gap decays with N. The oracle must be fixed, input-independent and linear; this is neither a linearity test nor protection against adaptive/stateful behavior. Randomness must be fresh, uniform and independent. Root/field and normalizer preparation, candidate preprocessing, memory movement and total evaluation work remain charged. Field operations do not by themselves give bit complexity. Modular rejection transfers only through a valid coefficient specialization with every required root/inverse and nonzero denominator. Finite passes are not a complex identity proof. No candidate transform or uniform coefficient synthesis is supplied. Q10's nonlinear finite-probe obstruction is a distinct theorem and is not subsumed by this closure.

## 2. M-PARITY-DEPTH

### Exact theorem and independent reasoning

Take complex F_N with N=2^k, k>=2, and nonzero binary parity masks with highest nonzero bits u,v. The column halfset has period h=2^(u+1); its h/2 representatives E contain exactly one representative of every residue modulo h/2. Therefore all smaller power-of-two residue counts agree, and the counts modulo h are zero or one. Osgood–Siripuram–Wu's imported characteristic-zero criterion makes E universal.

Write columns as e+h j and rows as rho+(N/h) ell. Fourier transformation along the repetition variable j splits the restriction by rho. If v<k-u-1, exactly half the blocks are present and each has column rank h/2, giving N/4. Otherwise every block is square on h/2 admitted rows and E, giving N/2. Both parity signs are covered.

For a stage of upper/lower quasiseparable order at most r_j, splitting a set and its complement into runs bounds the cross-rank by r_j d(A_j), one charged cut contribution per membership boundary. A product telescopes over transported sets and has cross-rank at most sum r_j d(A_j). Internal GF(2)-affine routing transports masks by invertible linear maps; translations only change signs. Low q_j mask bits set to zero give d(A_j)<=N 2^(-q_j)-1. If sum q_j<k, fewer than k homogeneous constraints leave a nonzero mask. For sum r_j>0 and sum r_j 2^(-q_j)<=1/4 its weighted capacity is strictly below N/4, a contradiction. If every r_j=0, stages are diagonal and their routed product has at most one nonzero entry per row and column, even when some diagonal entries vanish. This separately excludes the dense Fourier target.

The lower bound rank(F_N[R,C])>=N/4 for any balanced complex row/column sets follows from ||A||_F^2=N^2/4 and ||A||_2^2<=N in the unnormalized convention. Consequently arbitrary invertible monomial external endpoints are allowed for the coarse depth theorem, without broadening internal routing. Uniform r>=1 and q=ceil(log2(4rt)) give k<=t ceil(log2(4rt)).

### Primary attribution comparison

Osgood–Siripuram–Wu, Theorem 4, characterizes universal sampling sets for prime-power complex Fourier matrices by residue counts differing by at most one at every prime-power modulus. Substituting ambient h=2^(u+1), prime 2 and E above supplies exactly the imported nonsingularity step. Fourier symmetry permits its column-set use. The theorem does not itself state the moving-affine weighted-depth obstruction, which has the separate proof above. [Primary Theorem 4](https://arxiv.org/html/1204.0992v1#S4.SS2)

This is an explicit dependency/application attribution and a qualified nonmatch for the complete depth theorem. No worldwide-priority claim follows. The accepted review already states that no obligation remains for the qualified rank/depth theorem.

### Retained boundaries and correction

The parity-rank proof is characteristic-zero. Successful modular tests do not establish a universal finite-field sampling theorem; a universal-set determinant can vanish after specialization. Internal routing must remain GF(2)-affine. Orders are stage rank bounds, and the r_j weights must appear in any capacity ledger. In the saved r=2 regression, boundaries 31,31 have capacity 124, not 62; saved r=1 witnesses are unaffected. The defective historical helper is not certified as a corrected general-r implementation. No arbitrary nonlinear-routing exclusion, unrestricted arithmetic lower bound, or Fourier coefficient construction follows.

## 3. M-TENSOR-CUT

### Exact theorem and independent reasoning

For N=QM, use input j=t+Q u and output k=h+M s, with s,t in [0,Q), h,u in [0,M), primitive Nth root omega, xi=omega^M and eta=omega^Q. Expanding kj gives T[s,h,t,u]=omega^(-ht) xi^(-st) eta^(-hu) over the compatible splitting field.

The (s,h)|(t,u) flattening is the invertible Fourier matrix up to digit permutations, hence rank N. The (s,t)|(h,u) flattening becomes a repeated rectangular Vandermonde in omega^(-ht) after nonzero row/column scalings, hence rank min(Q,M). The (s,u)|(h,t) flattening is F_Q tensor F_M, up to a column scaling and permutations, hence rank N. CP rank is at least the first flattening rank N and at most N by fixing each (t,u) and taking its separate s,h factors and two coordinate vectors.

For separate invertible maps A on s and B on u, the transformed entries are C[a,t] omega^(-ht) E[h,b], where C=A F_Q and E=F_M B^T. Their support is exactly nnz(C)nnz(E). Invertibility gives nnz(C)>=Q and nnz(E)>=M. Equality QM occurs exactly when both are monomial. Thus the inverse-Fourier endpoint conversions, up to monomials, are forced by an N-entry center in this gauge class.

### Primary attribution comparison

Cooley–Tukey's mixed-radix substitution maps to the phase identity by r1=M, r2=Q, j0=h, j1=s, k0=t, k1=u, and conjugating the sign. Its two-axis transforms remain paid. [Original paper, pp. 297–298](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Cooley65.pdf)

Tyson, Definition 12 and Corollary 15, with M1=M, M2=Q, N1=Q, N2=M, matches the (s,u)|(h,t) rank N. It does not describe the differently paired min(Q,M) cut or the separate-endpoint support equality. [Tyson, section 5](https://arxiv.org/html/quant-ph/0306144#S5)

These are exact component mappings and a qualified nonmatch for the complete rank/support-rigidity package, not a claim of new priority.

### Retained boundaries and source identity

Keep these digits and labeled cuts: a different realignment can have a different rank. Separate invertible individual-leg changes preserve the cut ranks; joint two-leg changes are outside the local-gauge claim. Fixed-width exclusion requires min(Q,M) to grow; it does not grow with one radix fixed. The sparse center does not make inverse-Fourier endpoints free. General multi-stage arithmetic circuits and faster all-input evaluation remain outside scope. Unrelated mass-contraction and innovation results in the shared source review are not closed here.

The pinned local review export hashes to 0c56174e161f87436f39fd6a587945216ba386a3ba3d0e58c8118e13b2a5976b. The Catalogue explicitly preserves sanitized-export/original-byte identity qualifications, and novelty Q85 retains a different historical export-hash label. This finalization does not resolve or erase those historical identity distinctions. It binds the supplied pinned review plus its accepted per-ID decision and the independently checked mathematics.

## Evidence and review status

SOURCE_BINDINGS.json binds the three source reports and the accepted per-ID decisions by SHA256. The separate reviewer authored the fresh controls under checks/; the larger historical source totals are not reported as newly rerun. The completed independent scientific review and public payload-verdict derivative are included under reviews/. Public application evidence, if any, must be established separately by verified repository and workbook receipts.
