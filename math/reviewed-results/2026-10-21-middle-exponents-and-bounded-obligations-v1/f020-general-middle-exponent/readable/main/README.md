# F020 uniform middle exponent proof package

This package presents the accepted statement for n=2p^r+cp, every odd prime p, integer r>=3, integer s>r, integer 1<=c<p, and every characteristic-zero primitive p^s-th phase. In the original normalization, P_n and Gaussian H_n are squarefree and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root.

The ENTIRE r=3 family, including all c, is inherited and receives no new credit here. Only r>=4 is added relative to the inspected accepted source chain. This bounded source comparison is not a global literature, originality or priority claim. Packaging adds no theorem.

The new author proof at author/REPORT.md and its accepting mathematical review at independent-review/INDEPENDENT_REVIEW.md are verbatim original bytes. The historical pending-review language in the author proof is preserved; the later acceptance is pinned separately in provenance/ACCEPTANCE_BINDING.json. Pre-freeze substantive mathematical exchange is disclosed, not represented as blind discovery.

The mathematical source is accepted, but this public archive is a frozen proposal for a SEPARATE independent package audit. Producer checks do not self-certify transformed bytes. A detached audit is relevant only when it binds this exact main ZIP SHA-256. The detached audit is not included in the main ZIP.

## Reading order

Read SCOPE.json for the complete root and derivative ledger, author/REPORT.md for the uniform proof, independent-review/INDEPENDENT_REVIEW.md for the mathematical review, then provenance/ACCEPTANCE_BINDING.json, LINEAGE.json and TRANSFORMATIONS.json for exact source authority and public transformations. The author/sources/ files are selected documentary snapshots, not complete reconstructed dependencies.

## Geometry and root ledger

Use v(q-1)=1, N=p^r, B=r(p-1)p^(r-1)/2, beta=p^floor(r/2), L=N/beta, K=N+2B, E=N/2+2B, D=N+E-p, m=(p-1)/2, F=c(p-1/2), alpha=1-1/(2p), eta=(p+1)/2 and sigma=p-1/2. The high radius is rho=beta/2 for even r and rho=p^(floor(r/2)-1)(2p-1)/2 for odd r. The short-tail radius sigma stays fixed; it is not replaced by growing rho.

- Even c: exactly 2L high boundary roots in each of beta old disks, totaling 2N, with derivative value D+F; cp outer roots, with derivative value 2N alpha+F-1/2; no exact zero, and constant value K+F.
- Odd c: put W=(c-1)(2p-1)/2. The 2N high roots have derivative W+N+E-1 over p-indivisible centers, but W+N+E+m-x over p-divisible centers, with x=p^ord_p(a) at nonzero centers and x=rho centrally. There is one separate exact simple zero, derivative K+W+p-1; p-1 separated inner roots, derivative 3N-N/p+W+p-1; and (c-1)p outer roots, derivative 2N alpha+F-1/2. At c=1 the outer sector is empty.

The beta/p-1 nonzero p-divisible centers appear once beta>p; they cannot be assigned the old r=3 noncentral derivative. The exact-zero count is separate from the central high boundary count. The disjoint totals are 2N+cp and 2N+1+(p-1)+(c-1)p, both n.

The all-r eta-neighbor lemma has coefficientwise lower bound 3N-N/p-p^2 and unique Newton lower-bound-score extremizer k*=2N-p^3. This is not an asserted analytic residual equality. For r=3 the extremizer becomes N, but it is not N when r>3. The first-deleted shifted-tail neighbor is retained; even-tail leading cancellations do not invalidate its lower bounds.

Outer coarse residuals have repeated p-fold roots, counted with multiplicity before simplicity is proved. Original characteristic-zero ordinary derivatives are taken before reduction, never replaced by the zero derivative of an inseparable residue polynomial. No general finer outer splitting radius is claimed. The original kernel uses algebraic squares, not absolute-value squares.

## Original bytes and explicit projections

All mathematical prose is unchanged except one administrative absolute locator token in the inherited even-review introduction. That inherited review is therefore a PROJECTION, not verbatim; its original and projected identities, original token hash/length/byte offset and literal replacement are recorded in provenance/TRANSFORMATIONS.json. JSON projections replace only absolute administrative locator strings and record every changed JSON pointer, original value hash/length and replacement; all scientific values, source hashes and acceptance language are preserved. Their public hashes intentionally differ from original hashes.

Every frozen-source/ token is a contextual source label, not a file promised inside this package, an executable instruction or a network locator. The current author/SOURCE_BINDINGS.json snapshot fields are active relative to author/. Historical nested binding fields retain their original-tree context and are NOT active relative to their new locations. provenance/LOCATOR_QUALIFICATIONS.json classifies every such field and supplies explicit current public correspondences, including projected identities or omitted status. A source hash in a projected binding still identifies the original bytes, not its projection.

Only the root MANIFEST.json and SEAL.json inventory this public package. The eight retained historical manifests and eight historical seals describe their original trees, not this selection. provenance/INVENTORY_QUALIFICATIONS.json accounts for every listed historical member; provenance/SOURCE_INVENTORY.json accounts for every file in the eight original source trees read and hashed. Historical script and diagnostic names or hashes do not mean those files are shipped. Do not run historical verifiers against this selected tree.

## Historical mismatch and evidence limits

The historical b=2p retained report has SHA-256 00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db; its review cites original report 6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da. The mismatch is real and unresolved. Historical original author bytes and their complete package are not claimed recovered or accepted. Needed short-block arguments are reconstructed directly, with inherited mathematical credit.

Supplied programs, private diagnostics, control-output files, run logs and redundant source guides are omitted. Omitted normal/optimized output identities and recorded totals are documented in provenance/RECORDED_CONTROL_QUALIFICATIONS.json. They are historical bounded evidence, not a fresh scientific replay, standalone reproducibility suite, uniform proof or universal good reduction. The inherited n=60 modulo-163 bad reduction is not a characteristic-zero theorem exception. All source verification for this package was read-only; no supplied program was executed.

No claim covers r<3, c>=p, arbitrary intermediate digits or degrees, p=2, s<=r, composite orders, global F020/F023 closure, historical novelty/priority, FFT or cost improvement, universal good finite reduction, or a general finer outer splitting radius. No external upload, repository/table mutation or permission change was performed.

## Archive integrity

This deterministic ZIP contains sorted, uncompressed regular Markdown and JSON files with fixed metadata, no containing-directory prefix, no directory entries, no executable permissions and no archive comment. Root MANIFEST.json binds every payload member by path, byte length and SHA-256, excluding itself and root SEAL.json; the seal binds the exact manifest and file count.

Without executing supplied code, compare the ZIP hash to the trusted detached record, reject duplicate, unsafe or unexpected members, compare every manifest byte length/hash and exact file set, and verify the seal. Hashes identify bytes, not mathematical truth, authorship, priority or digital signatures.
