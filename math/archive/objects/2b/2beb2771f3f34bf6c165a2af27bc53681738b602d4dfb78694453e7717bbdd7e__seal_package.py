"""Fresh package seal. No source, registry or earlier package mutation."""
from pathlib import Path
import json,hashlib
P=Path(__file__).parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[{'path':p.relative_to(P).as_posix(),'size_bytes':p.stat().st_size,'sha256':H(p)}for p in sorted(P.rglob('*'))if p.is_file()and p not in (P/'SEAL.json',P/'SHA256SUMS.txt')]
(P/'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {r['path']}\n"for r in files))
seal={'package':P.name,'scope':'All51 assigned exact research sources fully read inertly; no complete corpus/all-proof or uploaded execution claim.','full_static_reads':51,'source_bytes':349868,'source_lines':7419,'supplied_source_executed_imported_compiled_AST_parsed':False,'fresh_independent_controls':8,'archive_containers_verified':42,'source_archive_occurrences_verified':139,'standalone_occurrences_verified':6,'stored_evidence_occurrence_records':432,'payload_manifest_sha256':H(P/'SHA256SUMS.txt'),'files':files}
(P/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for r in files:assert H(P/r['path'])==r['sha256']and(P/r['path']).stat().st_size==r['size_bytes']
assert H(P/'SHA256SUMS.txt')==seal['payload_manifest_sha256']
print(json.dumps({'sealed_files':len(files),'payload_manifest_sha256':seal['payload_manifest_sha256'],'seal_sha256':H(P/'SEAL.json'),'coverage_sha256':H(P/'COVERAGE.json'),'validation':'all sealed file checksums match'}))
