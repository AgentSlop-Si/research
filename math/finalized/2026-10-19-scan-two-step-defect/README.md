# Endpoint bit reversal: two-step defect and exact dual reductions

Owner: M-SCAN-DIMENSION. Status: TO RESEARCH. Priority: 34.

The original endpoint Jacobian rank lemma remains unresolved. This packet accepts only the structural results in [the report](candidate/REPORT.md) and [independent mathematical review](review/REVIEW.md).

For N=2^m, m>=3, the exact skew defect K=(TP)^2-((TP)^2)^T has 4m-4 supported coordinates. Its rank is 4m-6 for even m and 4m-8 for odd m, over every field. The separate determinant-one Woodbury correction and two-channel observability reformulation are accepted over Q; extension to another field requires actual invertibility of T. Symmetric/skew splitting additionally requires characteristic different from two. See [the domain ledger](DOMAIN_LEDGER.json).

The core determinant-one identity does not prove injectivity of the original H_N observations. No rational H_N annihilator is supplied. The accepted odd-sector pivot obstruction concerns a different pivot and remains intact. [OWNER_DISPOSITION.json](OWNER_DISPOSITION.json) preserves all original gates and the open/34 disposition. Classical determinant and Woodbury identities are credited; no historical novelty or performance conclusion is asserted.

## Integrity and portable checks

From this directory, run:

    python -B verify_package.py

This default command checks inventory, hashes, exact copy bindings, declared administrative projections, original manifests, domain/scope guards, and privacy boundaries. It does not run scientific code.

For the optional independent replay, with Python 3.12 and the versions in requirements.txt already available, run:

    python -B verify_package.py --replay

Replay copies the packet to a temporary directory and executes the five bundled check scripts there. It compares the exact parsed JSON results with the saved results and never overwrites the frozen packet. Those finite controls check transcription of the uniform proofs; they do not compute H_N ranks or prove the theorem by sampling. Review scripts use only bundled sibling imports, NumPy and SymPy; candidate checks use the standard library. No network or private file is needed.

## Preservation and privacy

Independent review, check programs, logs, results, and the endpoint source report are complete byte-for-byte copies. The candidate report and prior pivot source have only the explicitly listed provenance-locator tokens replaced; no mathematical word, formula, proof or conclusion is changed. Administrative candidate/SOURCE_BINDINGS.json is also projected. [COPY_BINDINGS.json](COPY_BINDINGS.json) and [PROJECTION_DISCLOSURE.json](PROJECTION_DISCLOSURE.json) bind originals and public bytes, with exact replacement text and original token offsets/hashes. Original files remain unchanged locally. The independent mathematical review applies to its recorded original candidate hash; the public report is bridged to that reviewed original by the locator-only ledger. The original candidate manifest is retained under provenance/ and is explicitly a pre-projection manifest.

Local research-workspace locators are removed from the public projection. Their historical source roles remain identified, and none is a runtime requirement. Private workbook identifiers, native rows, unrelated source material, and the proposed existing-record patch are excluded. [OMISSIONS.json](OMISSIONS.json) and [DEPENDENCIES.json](DEPENDENCIES.json) distinguish actual inputs from transitive historical references.

The prospective repository prefix is math/finalized/2026-10-19-scan-two-step-defect. This staged packet and its inert local patch do not claim publication or native/index synchronization. Only a separate verified release receipt can establish remote availability.
