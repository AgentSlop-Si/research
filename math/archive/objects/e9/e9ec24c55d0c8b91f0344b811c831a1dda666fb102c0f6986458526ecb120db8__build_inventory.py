#!/usr/bin/env python3
"""Authored inventory builder: read/hash frozen research artifacts, execute none."""
from pathlib import Path
import hashlib,json
ROOT=Path('research_round_2156/joint_orbit')
OUT=ROOT/'checkpoint20_constructor_handoff'
V19=Path('master_v20_integration_20261010/fft_research_master_20261009/checkpoint_history/v19_SHA256SUMS.txt')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
v19={}
for line in V19.read_text().splitlines():
    h,p=line.split(None,1);v19.setdefault(h,[]).append(p.strip())
# Directory, original seal, title, result scope, remaining cost, independent review.
data=[
('iteration_9_bank_interface','SHA256SUMS.txt','True bank-interface transport',
 'Positive Weyl transport and exact Cooley-Tukey control; negative maximum-row or maximum-column degree obstruction for a proper mixed bank. O(N) total nonzeros are not excluded.',
 'The actual interface actions must satisfy the sparsity hypotheses. A larger sparse state lift does not suffice. The control exterior retains batched Fourier work.',
 'review_bank_interface_certificate','Accepted within the stated actual-action and mixed-bank hypotheses.'),
('iteration_9_bank_interface','EXTERIOR_UNIQUENESS_SHA256SUMS.txt','Fixed-interface exterior uniqueness',
 'Both fixed Cooley-Tukey intertwining equations leave exactly scalar multiples of the known exterior; one calibration fixes the scalar.',
 'Uniqueness of the operator does not rule out a cheaper factorization of that same operator. Matrix density is not an arithmetic lower bound.',
 'review_batched_interface_equivalence','Accepted together with the batched equivalence review.'),
('iteration_9_bank_interface','BATCHED_EQUIVALENCE_SHA256SUMS.txt','Batched Fourier equivalence',
 'Full-active exterior is cost-equivalent to m arbitrary length-q Fourier transforms with O(N) overhead. Active-support routing gives charged partial-bank reductions.',
 'Complement inverse transforms are paid. The original near-square extension in this report assumes m=rq; the opposite orientation is handled separately.',
 'review_batched_interface_equivalence','Accepted with active-support-cover and fixed-radix scope.'),
('iteration_9_bank_interface','ORIGINAL_ORIENTATION_SHA256SUMS.txt','Original bank orientation addendum',
 'For q=rm, packs the original q length-m bank transforms into one batch of m length-q transforms, then pays (N/r) inverse radix-r transforms and linear routing.',
 'Linear additional work requires fixed radix r. No bank swap and no cheap exterior construction are supplied.',
 'review_original_bank_orientation','Accepted as a separate additive theorem, including the original odd-exponent q=2m bank.'),
('iteration_9_bank_interface','CHANGED_INTERFACE_SHA256SUMS.txt','Changed interface constructions',
 'Exact interface gauge formulas, cheap constant-swap gauges, monomial-clock coset rigidity, and an admissible N=16 zero-mask butterfly construction.',
 'A cheap gauge must include its bank conjugate and inverse. The finite control relocates ordinary Fourier work and gives no scalable improvement.',
 'review_changed_interface','Accepted within the full-bank and explicitly stated finite-control scope.'),
('iteration_9_bank_interface','NONZERO_BUTTERFLY_SHA256SUMS.txt','Nonzero-mask butterfly control',
 'An explicit paired-Green expression for F2 with nonzero matching-edge masks; disjoint matchings can be stitched into Hamiltonian orders using zero connecting masks.',
 'This is the known butterfly operation in an admissible grammar. Masks are not nonzero on every ambient edge, and no general FFT improvement follows.',
 None,'Constructor-sealed; no separate completed independent acceptance located for this exact report.'),
('iteration_9_bank_interface','MONOMIAL_WEYL_CLASSIFICATION_SHA256SUMS.txt','Monomial Weyl batch classification',
 'Monomial conjugates of both primitive Weyl generators force monomial equivalence to equal-size Fourier blocks. Promised-input coefficient recovery is linear from sparse actions, a supplied root, and one genuine calibration entry. Support consequence m*dP*dQ>=N.',
 'Certifying the promise or obtaining actions/seed from a circuit is separately charged. Composite and dyadic cases allow intermediate block sizes. Sections 7-8 finite family claims remain outside the independent acceptance.',
 'review_weyl_monomial_batch','Independent acceptance covers sections 1-6 and 9 only; sections 7-8 explicitly not independently accepted. Classical related literature cited; novelty not established.'),
('iteration_9_bank_interface','FOURIER4_KERNEL_SHA256SUMS.txt','Fourier-4 positive kernel and Fourier-8 commuting chart',
 'Positive one-layer F4 paired-Green kernel with all cycle masks nonzero and explicit splitting/root/denominator guards. A narrow F8 commuting scalar-resolvent chart is excluded.',
 'Finite kernel only; batching short cycles does not automatically give a legal full ambient Hamiltonian layer. The F8 exclusion does not cover general noncommuting layers.',
 None,'Constructor-sealed; queued for independent review.'),
('iteration_9_bank_interface','FOURIER8_NONCOMMUTING_ANCHOR_SHA256SUMS.txt','Fourier-8 noncommuting anchor certificate',
 'Eight fully specified fixed-anchor/order charts are rejected by exact projective direction gates, with positive Green controls and a complete coefficient budget.',
 'No positive F8 two-layer kernel is found, and no unrestricted impossibility follows. The direction gate applies only after a target factor has been specified.',
 None,'Constructor-sealed; queued for independent review.'),
('iteration_10_marked_tree','ROOT_POLE_CANCELLATION_SHA256SUMS.txt','Root-pole cancellation and linear tree jet',
 'Exact pole-free bordered resolvent, an O(N) tree application and constant-input complete tree jet with 2N-2 coefficient slots, including the z=1 cancellation.',
 'The coupled retained border inverse is unresolved. Neither coefficient extraction nor a marked scalar determinant identity is counted as a free algorithm.',
 'review_marked_cycle_first_schur','Independently accepted; review excludes later elimination stages and a fast retained inverse.'),
('iteration_10_marked_tree','ONE_SCHUR_TWO_RUN_SHA256SUMS.txt','One Schur step and two-run jet',
 'One exact parity Schur step with a guarded tree pivot. A constant-input complete two-run numerator has at most 6N slots and an explicit O(N) shared quotient-state evaluator.',
 'The pivot guard can fail while the full operator is invertible. Polynomial unknowns, repeated Schur closure and retained inversion remain unresolved.',
 'review_marked_cycle_first_schur','Independently accepted, including the shared quotient-state implementation and an independent exceptional-chart countercontrol.'),
('iteration_10_marked_tree','NEXT_PIVOT_SUPPORT_SHA256SUMS.txt','Next-pivot tree and support reduction',
 'Exact next-pivot tree reference plus a growing-rank correction. Its explicit support permits a Woodbury reduction to N/32+1 marked coordinates; constant-input reduced-operator jets have an O(N) evaluator.',
 'Only one bounded stage is proved. Ambient maps and marks remain carried; no closed shrinking family or cheap inverse is established. Formal-series guards have constant term one.',
 None,'Constructor-sealed; queued for independent review.'),
('iteration_11_variable_block','VARIABLE_BLOCK_SHA256SUMS.txt','Variable-bit block elimination and work',
 'Exact b-bit Schur/packet identities and finite-horizon frontier count S(N,b)=N*sum[t=b..n-1] A_b(t)/2^t+(b+1)*A_b(n), N=2^n. The specified full-frontier evaluator costs Theta(N*min(n+1,2^b)).',
 'The matching lower bound belongs only to that evaluator. At b about log2(log2 N), its work remains Theta(N log N). The retained formal-series inverse and a closed smaller-state representation are unconstructed.',
 None,'Constructor-sealed; queued for independent review.'),
]
bundles=[]
for d,s,title,result,limit,rev,status in data:
    directory=ROOT/d;seal=directory/s
    entries=[]
    for line in seal.read_text().splitlines():
        h,name=line.split(None,1);name=name.strip().lstrip('*');p=directory/name
        assert sha(p)==h,(str(p),'seal mismatch')
        entries.append({'path':str(p),'relative_to_joint_orbit':str(p.relative_to(ROOT)),'sha256':h,'bytes':p.stat().st_size,'v19_paths_with_same_hash':v19.get(h,[])})
    reports=[e for e in entries if e['path'].endswith('.md')]
    assert len(reports)==1
    report=reports[0]
    sealentry={'path':str(seal),'relative_to_joint_orbit':str(seal.relative_to(ROOT)),'sha256':sha(seal),'bytes':seal.stat().st_size,'v19_paths_with_same_hash':v19.get(sha(seal),[])}
    review=None
    if rev:
        rd=ROOT.parent/rev;rm=rd/'SEALED_MANIFEST.json';rs=rd/'SEALED_MANIFEST.sha256'
        expected=rs.read_text().split()[0];assert sha(rm)==expected
        obj=json.loads(rm.read_text());files=obj['files']
        if isinstance(files,dict):
            for name,h in files.items():assert sha(rd/name)==h,(rev,name)
        elif isinstance(files,list):
            for f in files:assert sha(rd/f['path'])==f['sha256'],(rev,f['path'])
        else: raise AssertionError('Unexpected review seal format')
        review={'directory':str(rd),'manifest':str(rm),'manifest_sha256':sha(rm),'seal':str(rs),'seal_sha256':sha(rs),'seal_and_all_payload_hashes_verified':True}
    bundles.append({'id':len(bundles)+1,'title':title,'report':report['path'],'report_sha256':report['sha256'],'report_already_in_v19':bool(report['v19_paths_with_same_hash']),'result':result,'boundary_or_unresolved':limit,'independent_review_status':status,'independent_review':review,'files':entries+[sealentry],'original_seal':str(seal),'all_original_seal_payloads_verified':True})
allfiles=[f for b in bundles for f in b['files']]
assert len({f['path'] for f in allfiles})==52
inventory={'purpose':'Checkpoint20 preservation inventory for the bank-interface and marked-tree constructor. Original frozen bundles are unchanged; this index includes previously archived reports so their original controls and seals can also be preserved.','date_utc':'2026-10-10','author_task':'construct_bank_interface_certificate','scope':'All thirteen frozen deliverable bundles from iterations 9-11 of this constructor; no mutable scratch files. Earlier joint-orbit iterations belong to prior handoffs.','v19_comparison':{'manifest_path':str(V19),'manifest_sha256':sha(V19),'method':'Exact SHA256 membership, irrespective of renamed reviewer snapshot paths. Absence means absent from this verified v19 file manifest, not a chronology claim.'},'counts':{'frozen_bundles':len(bundles),'frozen_files_including_original_seals':len(allfiles),'report_hashes_already_in_v19':sum(b['report_already_in_v19'] for b in bundles),'report_hashes_absent_from_v19':sum(not b['report_already_in_v19'] for b in bundles),'all_file_hashes_already_in_v19':sum(bool(f['v19_paths_with_same_hash']) for f in allfiles),'all_file_hashes_absent_from_v19':sum(not f['v19_paths_with_same_hash'] for f in allfiles)},'source_provenance':{'marked_cycle_source':'Library-discovered source saved 2026-10-10 00:25 UTC; not a direct user upload.','library_file_id':'[private-id]','zip_path':'library_material_0031/FFT/fft_marked_cycle_theory_2026-10-10.zip','zip_sha256':'6f7e9f88d82f1242ffd58b7c84bb7a76ae39e4606eff52dc7838de99f93e438f','uploaded_code_executed':False},'global_boundary':'No general faster FFT, unrestricted paired-Green impossibility, or arithmetic lower bound has been established. Finite controls, narrow obstructions, and unresolved operator inverses retain their exact scope.','bundles':bundles}
(OUT/'CONSTRUCTOR_FROZEN_DELIVERABLES_FOR_CHECKPOINT20.json').write_text(json.dumps(inventory,indent=2)+'\n')
lines=['# Frozen constructor deliverables for checkpoint20','','All original bundles and seals are unchanged. This inventory is intended for preservation and later sorting, including positive controls, narrowly scoped negative results and unresolved operations. No uploaded code was executed.','','## Coverage','',f'- {len(bundles)} frozen bundles; {len(allfiles)} files including their original seals.',f'- {inventory["counts"]["report_hashes_absent_from_v19"]} report hashes are absent from the v19 manifest; {inventory["counts"]["report_hashes_already_in_v19"]} already appear as reviewer snapshots.',f'- Across all original files, {inventory["counts"]["all_file_hashes_absent_from_v19"]} hashes are absent from v19. Preserve full bundles even where a report snapshot already exists.','- Comparison uses exact content hashes, not filename or assumed creation time.','- Every original payload seal, plus all six linked review payload seals, was independently rehashed by this inventory builder.','- Detailed per-file hashes, sizes and v19 matching paths are in the companion JSON.','','## Reports absent from v19','']
for b in bundles:
    if not b['report_already_in_v19']:lines.append(f'{b["id"]}. {b["title"]}: `{b["report"]}`')
lines+=['','## Complete bundle inventory','']
for b in bundles:
    lines += [f'### {b["id"]}. {b["title"]}','',f'Report: `{b["report"]}`',f'Original seal: `{b["original_seal"]}`',f'Report SHA256: `{b["report_sha256"]}`',f'v19 report membership: {"already present as an identical snapshot" if b["report_already_in_v19"] else "absent"}.','',b['result'],'',f'Cost/scope boundary: {b["boundary_or_unresolved"]}','',f'Independent review: {b["independent_review_status"]}']
    if b['independent_review']:lines += [f'Review seal: `{b["independent_review"]["seal"]}`; manifest SHA256 `{b["independent_review"]["manifest_sha256"]}`.']
    lines+=['']
lines+=['## Preservation instructions and stopping boundary','','Copy the exact four files listed for each bundle, preserving their relative directory and original seal. Do not replace this with only the report: the authored verifier and frozen control output are part of the research record. The companion JSON lists all 52 source files. Reviewer bundles are separately linked and retain their independent acceptance boundaries.','','The two latest constructor milestones are support reduction and variable-bit elimination. Both were sent to the latest-source reviewer for queued audit. The bounded construction is complete; the retained inverse is still unresolved, and no speedup is claimed.','','The marked-cycle source was Library-discovered at 00:25 UTC, rather than part of a direct user upload. Its original ID and hash are recorded in JSON.','']
(OUT/'CONSTRUCTOR_FROZEN_DELIVERABLES_FOR_CHECKPOINT20.md').write_text('\n'.join(lines))
# List source payloads separately for convenient exact copying; destination is up to parent.
(OUT/'FROZEN_SOURCE_FILES.txt').write_text(''.join(f['path']+'\n' for f in allfiles))
sealed=['build_inventory.py','CONSTRUCTOR_FROZEN_DELIVERABLES_FOR_CHECKPOINT20.json','CONSTRUCTOR_FROZEN_DELIVERABLES_FOR_CHECKPOINT20.md','FROZEN_SOURCE_FILES.txt']
(OUT/'SHA256SUMS.txt').write_text(''.join(sha(OUT/name)+'  '+name+'\n' for name in sealed))
print(json.dumps(inventory['counts'],indent=2))
print('Inventory:',OUT)
