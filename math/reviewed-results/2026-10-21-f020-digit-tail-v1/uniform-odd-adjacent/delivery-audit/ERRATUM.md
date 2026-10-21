# Erratum to detached audit version 1

The version-1 detached audit REPORT.md incorrectly wrote L=p^(r-1). The accepted mathematical proof instead defines h=floor(r/2), beta=p^h and L=N/beta=p^(ceil(r/2)). The former expression agrees only for r=2,3 and is wrong for r>=4. This was an error in the auditor's summary, not in the accepted theorem, proof, controls or main public package.

Version 2 corrects that definition and makes the beta-disk count explicit: (beta-1)cL+(cL+1)=cN+1. It explicitly scopes the exceptional obstruction to r=2; the +2p discriminant correction applies precisely when r=2 and p divides R_c(-1), and is zero otherwise. The scaled odd-operator expression is also explicitly located in the proof's r=2 central coordinates.

Every other mathematical formula in the summary was checked against the hash-bound accepted proof. SUMMARY_FORMULA_CHECK.json records exact source excerpts and the partition identity; finite arithmetic fixtures include r>=4 and are not treated as proof of the family.

The original detached audit v1 is preserved unchanged as evidence and is superseded by this corrected version for the summary. The main public v2 ZIP and all accepted author/reviewer sources are unchanged. AUDIT_RESULTS.json and INVENTORY_QUALIFICATIONS.json are carried forward byte-for-byte as the earlier audit's recorded evidence. No fresh scientific replay is claimed for this editorial correction. CORRECTION_PROVENANCE.json binds the prior archive, erroneous report, unchanged main archive, accepted proof and exact replacements.

This correction does not expand scientific scope, assert global closure or historical novelty, or make a complexity claim. No external write or upload is part of it. Independent acceptance of the corrected detached audit is a separate review.
