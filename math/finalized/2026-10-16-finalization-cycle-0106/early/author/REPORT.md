# M-SEED-BALANCE: fixed-seed versus two-sided unitary balancing

Date: 2026-10-16 UTC. Baseline: `AgentSlop-Si/research` main `73528f9e7495b0614106dfc4cc5b5c42907daaf5` (70 closed / 257 open). Workbook: `1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU`.

## Result and disposition

The selected **M-SEED-BALANCE** primary comparison is complete as a **qualified nonmatch with an exact bridge**. In the complex-unitary specialization the accepted fixed-seed condition is precisely a *one-sided* normal-form problem for (U=A^*f_N). Idel–Wolf's Theorem 2 guarantees a *two-sided* normal form for every unitary. Its second freely chosen endpoint is material, and an exact two-dimensional example separates the statements even inside the owner's weak-coupling neighborhood.

This discharges the owner's recorded comparison stop; the record is closure-eligible after independent acceptance, retaining priority 42 and all historical-priority qualifications. No excluded endpoint extension, production task or worldwide search is manufactured as a successor obligation. This report claims neither new acceptance of the existing seed theorem nor that its full formulation is printed in the selected primary source.

Only one of the permitted two records was selected. M-POSITIVE-PHASE was screened but is not modified or counted as completed. No completed F021/Q29/ALG034, sparse-defect, rectangle, centralizer or Weyl comparison was reopened.

## 1. Full owner and current history

Read live in their entirety:
- Research overview A95:Q95, stable ID in B95.
- Catalogue A57:AF57, stable ID in A57.
- novelity breakthough A78:Z78, stable ID in C78.

The saved full CellData snapshot includes formulas, notes, rich-link metadata and earlier history. Live stable IDs and rich links establish the current owner rows; older note text still contains an obsolete novelty-row number and is not substituted for the live binding.

Catalogue H57/I57/J57 and X57/Y57 contain the accepted one-internal-monomial seed equivalence, the weak-coupling obstruction and the two fixed N8/N16 common-coupling certificates. Z57 distinguishes their exclusions: an unrestricted sufficient B may contain Fourier, first-cross calibration is weaker than equality, and independent couplings/endpoints are not covered. None is phrased as a promised construction. AE57/AF57 select a primary theorem with hypothesis, formula and cost mapping, allowing a qualified nonmatch. Overview F95 specifically identifies historical attribution/comparison as the leading open work while preserving accepted correctness.

The complete accepted Phase35 review was fetched at the baseline SHA and read as inert text:
[accepted review](https://github.com/AgentSlop-Si/research/blob/73528f9e7495b0614106dfc4cc5b5c42907daaf5/math/archive/objects/b1/b1d13ce38ed662d9379e25ea0e87bed498174a56d161a84b7b20bbaaaee16de0__REVIEW.md).

The preceding positive-scaling/phase review was also screened to avoid attributing its already-recognized Sinkhorn ingredient as new work. Its scope is separate.

## 2. Primary statement and exact source scope

Martin Idel and Michael M. Wolf, *Sinkhorn normal form for unitary matrices*, [arXiv:1408.5728v3](https://arxiv.org/pdf/1408.5728v3), version stamp 4 September 2015. The publication is Linear Algebra and its Applications 471 (2015), 76–84, DOI [10.1016/j.laa.2014.12.031](https://doi.org/10.1016/j.laa.2014.12.031).

Theorem 2 (printed pp.1 and 3) gives, for every complex unitary U, diagonal unitaries L,R for which LUR has every row and column sum one. Lemma 1 (pp.2–3) connects this to a unimodular input vector whose image is also unimodular. Section 3, equation (2), p.4, identifies the line-sum-one unitary class by Fourier conjugation with (1\oplus\widetilde U). Its corollary allows general unitaries to be decomposed using several Fourier transforms and diagonal phases. The conclusion (p.6) explicitly calls the existence proof nonconstructive and leaves the cited iteration's universal convergence unproved.

These are the external claims used here. The following fixed-seed specialization, formulas and separating example are explicit deductions, not quotations or alleged printed theorems of that paper.

## 3. General invertible owner model

Let (u=(1,\ldots,1)^T), let (f=f_N) be the positive-root normalized Fourier matrix, so (fu=\sqrt N e_0) and (e_0^Tf=u^T/\sqrt N). Suppose A is invertible and its first-row entries (r_i=A_{0i}) are nonzero. The owner asks for

\[
f=A D B,\qquad Bu=b u,\quad u^TB=b u^T,
\]

where D is invertible diagonal and B is invertible bi-regular. Invertibility implies (b\ne0). A middle permutation can be absorbed into B because it fixes u on both sides; an arbitrary endpoint diagonal generally cannot.

Multiplying the first row by (B^{-1}) forces

\[
d_i=\frac{1}{b\sqrt N r_i}.
\]

Applying the factorization to u then gives the accepted equivalent conditions

\[
A(1/r)=N e_0,\qquad r_i(A^{-1})_{i0}=1/N\quad\hbox{for every }i.
\]

Here (1/r) is entrywise reciprocal. Conversely set
\[
D_0=\operatorname{diag}(1/(\sqrt N r_i)),\qquad
B_0=D_0^{-1}A^{-1}f.
\]
Then the displayed balance equation gives (B_0u=u) and (u^TB_0=u^T). Thus the seed condition is sufficient for this unrestricted B, with no cheap-B conclusion.

The normalized target only changes D by a common scalar; it leaves the leverage invariant and the original unnormalized Fourier theorem unchanged. For arbitrary invertible A these leverage values are the diagonal of the generally oblique rank-one projector (A^{-1}e_0e_0^TA). They need not be nonnegative real values. A complex-unitary theorem therefore cannot silently be applied to the entire invertible owner model.

## 4. Exact complex-unitary specialization

Now assume A is unitary, still with nonzero first row. The owner condition becomes

\[
|r_i|^2=1/N.
\]

If it holds, (D_0) above is unitary and (B_0) is unitary and bi-regular with sum one. Conversely the owner condition remains necessary even if B was initially permitted to be an arbitrary invertible bi-regular matrix. In any such factorization (D=D_0/b) and (B=bB_0), so normalization reduces the admissible right factor to a unitary one.

Define (U=A^*f). Then
\[
Uu=\sqrt N A^*e_0,\qquad |(Uu)_i|=\sqrt N|r_i|.
\]
Consequently
\[
\text{owner's fixed-unitary-seed condition}
\iff Uu\text{ is unimodular}
\iff U=D_0 B_0
\]
with diagonal unitary (D_0) and unitary line-sum-one (B_0).

The last equivalence is direct: if (Uu=z) has unit-modulus entries, set (D_0=\operatorname{diag}(z)) and (B_0=D_0^*U). Then (B_0u=u). Unitarity also gives (B_0^*u=u), hence (u^TB_0=u^T). Conversely (U=D_0B_0) makes (Uu=D_0u) unimodular.

The primary supplies `LUR=B`, while this fixed-seed problem needs (LU=B_0), with the right endpoint fixed to identity. Equivalently the source may choose any unimodular vector (Ru); the owner tests the prescribed vector u. A middle permutation does not cure the distinction because (Pu=u).

This is a substantive exact hypothesis/formula mapping. It explains why a universal two-sided scaling theorem neither implies nor contradicts the owner's conditional one-sided result.

## 5. Exact separator inside the weak-coupling neighborhood

Take (N=2) and
\[
A=\frac1{25}\begin{pmatrix}24&-7\\7&24\end{pmatrix},
\qquad
f_2=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
\]
A is real orthogonal and its first row is nonzero entrywise. Its owner leverage vector is
\[
(576/625,49/625)\ne(1/2,1/2).
\]
Moreover
\[
\|A-I\|_2=\sqrt{2}/5<1/2.
\]
This example therefore lies within the stated weak-coupling exclusion, not merely outside the nonzero-row domain.

Here
\[
U=A^*f_2=\frac1{25\sqrt2}
\begin{pmatrix}31&17\\17&-31\end{pmatrix}.
\]
The entries of (Uu=(48,-14)^T/(25\sqrt2)) have unequal magnitudes and are not both unit modulus. No one-sided normal form exists.

Nevertheless choose
\[
R=\operatorname{diag}(1,i),\quad
z=\frac{31+17i}{25\sqrt2},\quad
L=\operatorname{diag}(\overline z,i\overline z).
\]
Since (31^2+17^2=1250=(25\sqrt2)^2), both L and R are diagonal unitaries. Direct multiplication gives (URu=(z,-iz)^T), hence (LURu=u). The unitary (V=LUR) therefore has all row and column sums one.

Writing (U=L^{-1}VR^{-1}) cannot turn (VR^{-1}) into the owner's bi-regular right factor: if (VR^{-1}u=b u), multiply by (V^{-1}) and use (V^{-1}u=u) to obtain ((1,-i)^T=b(1,1)^T), which is impossible. The general nonexistence above also excludes a different choice of one-sided phases. These are exact algebraic identities; no numerical experiment, supplied program or solver was used.

## 6. Costs and retained boundaries

The source's existence of L,R has no certified finite arithmetic, bit, conditioning or convergence invoice. Once explicitly supplied, each diagonal application costs O(N) scalar multiplications, but this does not pay to discover its entries. Its Fourier-conjugation normal form already uses Fourier actions and therefore cannot provide a cheaper Fourier evaluator merely by being rewritten.

Similarly, the owner's (B_0=D_0^{-1}A^{-1}f) is an algebraic existence witness that explicitly contains f. It does not establish an O(N) implementation of B. A fixed number of the owner's legal Green scans, their signature formation and guarded entrywise divisions may be charged as in the accepted review; root/phase preparation, storage, routing and any bit/numerical costs remain distinct. Exact complex signature sorting/hashing requires the stated representation model.

The existing weak-coupling proof for (A=c(I+E)), \(\|E\|_2<1/2\), is not re-proved or recounted as new acceptance here. Positive scalar combinations of the permitted resolvents retain their coupling and positivity assumptions. The fixed common-coupling N8/N16 polynomial certificates remain fixed-pair statements; the selected source does not compare their printed priority or extend them. First-cross calibration still verifies only (2N-1) entries. No unrestricted endpoint masks, distinct independent-coupling construction, finite-word implementation, production claim or unrestricted lower bound follows.

The remaining *boundary* is historical priority of the owner's exact guarded synthesis, plus the expressly excluded models. The recorded stop allows a qualified nonmatch, so neither unspecified further literature nor excluded extensions are automatically pending work for this row.

## 7. Access, provenance and proposal controls

The v3 primary PDF's theorem text was read with the web PDF extractor. Two requested page screenshots returned cache-miss errors; an institutional journal-PDF open returned an internal error. No alternative access restriction was bypassed, no denied route was retried, and no primary-PDF byte possession or digest is claimed. The deductions were written with explicit conjugates to avoid stripped-overbar ambiguities in PDF extraction.

The repository review's historical member label starts b1d13ce..., while the sanitized text has the separate export SHA256 bd23457a... recorded in the workbook. These identities remain distinct. `SOURCE_IDENTITIES.json` records the fetched Git blob SHA and actual local UTF-8 digest, not a reconstruction of an original ZIP.

`PROPOSAL.json` is a local guarded 15-cell minimal proposal for this single ID, preserving every prior string as a verbatim historical suffix except the status enum. It changes no formulas, priorities, scientific theorem statements, source owners, ordering, original source URLs, or historical assessment bands. It is contingent on independent acceptance and a fresh exact-before preflight. If accepted and applied without unrelated concurrent changes, counts become 71 closed / 256 open. No external write occurred in this work.

