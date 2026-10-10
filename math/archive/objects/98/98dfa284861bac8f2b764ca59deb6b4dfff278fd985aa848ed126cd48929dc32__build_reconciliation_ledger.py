"""Assemble the authored, scoped review ledger; not a theorem checker."""
from pathlib import Path
import hashlib, json, collections

B = Path('external_inventory_text_review_0225')
O = B / 'sealed_reconciliation_0233'
if (O / 'SEALED_MANIFEST.json').exists():
    raise SystemExit('Refusing to alter sealed output')
rows = json.loads((O / 'ARCHIVE_MEMBER_VERIFICATION.json').read_text())

def family(indices, name, status, qualification, audits=()):
    for i in indices:
        rows[i].update(family=name, family_disposition=status,
                       retained_qualification=qualification,
                       prior_review_paths=list(audits))

def S(path):
    return '' + path

family(range(0, 2), 'Weyl expansion', 'Historical log/manifest only in this recovery',
       'No new theorem review or source rerun follows from these two files.')
family([2], 'Green Phase34', 'Manifest-only recovery',
       'Hash declarations are source metadata, not proof or execution evidence.')
family([3], 'Moving partition', 'Manifest-only recovery',
       'No theorem scope is enlarged by this manifest.')
family([4, 5], 'Hero0 Phase12', 'Historical logs only',
       'Recorded source test outcomes were read, not executed or newly certified.')
family(range(6, 11), 'Sparse defect', 'Previously accepted rank obstruction, with existing repairs retained',
       'Arbitrary-row-sparse scan escape needs the independent repair; source bandwidth proof alone is insufficient. Variable-r Woodbury preparation is O(N+Nr^2+r^3); application O(N+Nr+r^2). No-pivot source solver has stronger guards than the rank theorem.',
       [S('materials_1930_library/sparse_gate_audit/AUDIT_REPORT.md'),
        S('materials_1930_library/sparse_gate_audit/ARBITRARY_SPARSE_REPAIR.md')])
family(range(11, 19), 'Green Phase26', 'Previously accepted bounded-affine-step term-count obstruction',
       'Only affine interstage permutations and fixed step/exception budgets. Retain strict integer witness r*abs(t)<N, the finite large-bridge disjunction, and the inherited Phase25 inverse repair. No arbitrary non-affine circuit claim.',
       [S('materials_1930_library/phase26_audit/PHASE26_AUDIT.md')])
family(range(19, 28), 'Mixed radix v13', 'Previously accepted projector/covariance and conditional approximation analysis',
       'Randomized one-row estimator is not an exact full transform. Complete character bank is exact but inherited and collapses to ordinary Cooley-Tukey. Preserve one-row phase-sign correction, partial precision scope, and conditional-pairwise-independence extension.',
       [S('materials_1930_library/v13_audit/AUDIT_AND_EXTENSION.md')])
family([28, 29], 'Packet/separator v19', 'Historical prior-art and README claims reconciled to corrected prior audit',
       'Packet fusion and common-order rational gate retain costs and scope. Proposed sparse high-treewidth direct-inverse escape is refuted: a monomially Fourier inverse forces a dense denominator. No new v19 proof text occurs in these two recovered items.',
       [S('research_round_2344/review_green_phase33_packet_v19/INDEPENDENT_REVIEW.md')])
family([30], 'Interleaved scans', 'Manifest-only recovery',
       'No theorem review or successful execution is inferred from hash declarations.')
family([31], 'Two-stage cut', 'Manifest-only recovery',
       'No theorem review or successful execution is inferred from hash declarations.')
family([32, 33], 'Offset class v12', 'Historical claims reconciled to existing scoped audit',
       'Use half-up rounding and a linear structural class construction, not literal sorting. Retain prime-power/divisor and precision assumptions; alleged missing v11 core was already disproved by byte identity. No exact unrestricted FFT claim.',
       [S('materials_1910_offset/audit/OFFSET_V12_AUDIT.md')])
family([34], 'Unit-step chirp v9', 'README claims reconciled to existing scoped audit',
       'Prime-power/divisor and exact-index assumptions remain; M=1 projector is zero, mixed-prime covariance requires separate extension, source timing is historical, and precision claims use the corrected independent contract.',
       [S('materials_1628/supplement/THREE_ADDITIONS_AUDIT.md')])
family([35], 'Global bottleneck', 'Manifest-only recovery',
       'No theorem review or successful execution is inferred from hash declarations.')
family([36], 'Wide scan', 'Manifest-only recovery',
       'No theorem review or successful execution is inferred from hash declarations.')
family(range(37, 41), 'Three-stage bit reversal', 'Earlier N>=64 three-stage source improvement already accepted',
       'Uniform natural-endpoint N=32m>=64 cut has capacity 12m+1 versus Fourier rank 13m. Historical four-stage lead is superseded: later central-partition theorem excludes four rank-one repeated-bit-reversal stages at all dyadic N>=128; arbitrary mixing shuffles remain outside that all-length theorem.',
       [S('research_round_2156/three_stage/approved_bitrev64_source_milestone/AUDIT.md'),
        S('research_round_2156/review_repeated_bitrev_depth/REPEATED_BITREV_AUDIT.md')])
family([41], 'Bidirectional macro', 'Manifest-only recovery',
       'No theorem review or successful execution is inferred from hash declarations.')
family(range(42, 50), 'Green Phase25', 'Earlier structured-input and rank results accepted; inverse claim corrected',
       'Admissible individual resolvents do not imply invertible sum. Require det(A+B)!=0; use prior whole-matrix pivoted constant-frontier repair for all nonsingular cases. Original unpivoted band/Woodbury implementation has additional failure cases. Arithmetic complexity is not bit complexity or numerical stability.',
       [S('materials_1909/phase25_audit/PHASE25_AUDIT.md')])
family(range(50, 57), 'Green Phase33', 'Earlier finite-instance, chart/local, and additive statements accepted in scope',
       'Fixed Green-pair/coupling exclusions permit arbitrary invertible endpoint diagonals but do not exclude all choices. q^2 bound is a nonsingular chart/generic-target statement, tangent test is local, partial sixth-column match is not full Fourier, and additive q=Omega(log N) does not cover products.',
       [S('research_round_2344/review_green_phase33_packet_v19/INDEPENDENT_REVIEW.md')])
family([57], 'Hero17 Phase5', 'Manifest-only recovery',
       'No theorem review or successful execution is inferred from hash declarations.')
family([58], 'Three-updates audit', 'Manifest-only recovery',
       'An earlier audit manifest is not a new independent mathematical review.')
family(range(59, 65), 'Multistage bit-reversal geometry', 'Earlier restricted dimension results accepted',
       'All-size bound concerns the separated-generator chart (N>=3), not every quasiseparable boundary component. Exact saturation is established at N=8,16,32 and stated saved depths, extended there to greater depth by identity stages; no all-N saturation or Fourier-factorization conclusion.',
       [S('materials_1909/bitrev_audit/REPORT.md')])
family(range(65, 70), 'Endpoint minimax', 'Earlier characteristic-zero single-matrix minimax theorem accepted',
       'Independent endpoint minimax N/4+1 holds for dyadic N>=8. Keep characteristic-zero and single-matrix scope. Exact total-cut-rank minima are certified at N=8,16 only; no all-N finite-size total optimum, runtime theorem, or unrestricted multistage exclusion.',
       [S('materials_1848_endpoint/endpoint_audit/ENDPOINT_AUDIT.md')])

proofs = {6, 17, 26, 48, 54, 59, 65}
prior_art = {13, 28, 32, 44}
validation = {18, 49, 55}
runners = {15, 38, 46, 53, 61}
logs = {0, 4, 5, 8, 19, 20, 24, 25, 62, 69}
for row in rows:
    i = row['index']
    name = Path(row['source_member']).name
    if i in proofs:
        role = 'Standalone theorem/proof certificate'
        scope = 'Full text read; substantive claims compared with the identified prior scoped mathematical audit. No fresh proof-checker execution in this reconciliation.'
    elif i == 22:
        role = 'Supporting precision analysis'
        scope = 'Full text read; its conditional/partial precision contract compared with the prior v13 audit.'
    elif i in prior_art:
        role = 'Source prior-art narrative'
        scope = 'Full text read for claims and status; its bibliography and publication novelty were not independently re-established in this reconciliation.'
    elif i in validation:
        role = 'Source validation narrative'
        scope = 'Full text read and compared with prior review scope; described source runs remain historical records.'
    elif i in runners:
        role = 'Run instructions'
        scope = 'Full text read as documentation; commands were not executed.'
    elif i in logs:
        role = 'Historical source log'
        scope = 'Full text read; only byte identity is freshly verified. Recorded results are not current successful tests.'
    elif name == 'SHA256SUMS.txt':
        role = 'Source manifest'
        scope = 'Full text read as hash metadata; this recovered member is independently hashed, but its declared package-wide hash list is not a new proof or full package replay.'
    else:
        role = 'README/checkpoint/handoff narrative'
        scope = 'Full text read; mathematical scope and next-step status compared with identified prior reviews where available. Historical instructions are not new actions.'
    row.update(content_role=role, current_review_scope=scope, full_text_read=True,
               source_programs_executed_in_this_review=False,
               new_theorem_claim_from_recovery=False,
               newly_missing_original_claim=False)

audit_paths = sorted({p for row in rows for p in row['prior_review_paths']})
audits = []
for p in audit_paths:
    b = Path(p).read_bytes()
    audits.append({'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
                   'use': 'Prior scoped conclusions consulted as evidence of existing status; no source or prior checker executed by this reconciliation.'})
counts = dict(collections.Counter(row['content_role'] for row in rows))
(O / 'ITEM_RECONCILIATION.json').write_text(json.dumps(rows, indent=2) + '\n')
(O / 'PRIOR_REVIEW_EVIDENCE.json').write_text(json.dumps(audits, indent=2) + '\n')
(O / 'CONTENT_SCOPE_COUNTS.json').write_text(json.dumps(counts, indent=2) + '\n')
lines = ['# Item-level disposition index', '',
         'All indexes refer to the original 70-row recovery ledger. Full paths, hashes and qualifications are in ITEM_RECONCILIATION.json.', '',
         '| Index | Family | File | Content role | Existing disposition |',
         '|---:|---|---|---|---|']
for row in rows:
    lines.append(f"| {row['index']} | {row['family']} | {Path(row['source_member']).name} | {row['content_role']} | {row['family_disposition']} |")
(O / 'ITEM_INDEX.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'rows': len(rows), 'prior_review_documents': len(audits), 'content_roles': counts}, indent=2))
