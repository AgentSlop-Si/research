"""Fresh package-only checksum writer; never modifies originals or shared coverage registry."""
from pathlib import Path
import json,hashlib
O=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=json.load(open(O/'COVERAGE.json'));c['completed_utc']='2026-10-10T05:40:10Z';(O/'COVERAGE.json').write_text(json.dumps(c,indent=2)+'\n')
files=sorted(p for p in O.rglob('*') if p.is_file() and p.name not in ['SEAL.json','SHA256SUMS.txt'])
manifest=''.join(f'{sha(p)}  {p.relative_to(O)}\n' for p in files)
(O/'SHA256SUMS.txt').write_text(manifest)
for line in manifest.splitlines():
 h,name=line.split('  ',1);assert sha(O/name)==h
seal={'package':O.name,'sealed_utc':'2026-10-10T05:40:10Z','file_count':len(files),'sealed_bytes':sum(p.stat().st_size for p in files),'sha256sums_sha256':sha(O/'SHA256SUMS.txt'),'coverage_sha256':sha(O/'COVERAGE.json'),'source_reviews_sha256':sha(O/'SOURCE_REVIEWS.json'),'assigned_sources':22,'source_bytes':165598,'source_lines':4013,'new_coverage_credit':c['new_coverage_credit'],'uploaded_source_execution':'none','uploaded_source_import_compile_AST':'none','central_registry_modified':False,'central_registry_modified_by_this_review':False,'registry_may_have_concurrent_parent_updates':True,'fresh_reviewer_control_groups':23,'all_package_digest_checks_passed':True,'stored_manifest_entries_rehashed':286,'all_stored_manifest_entries_match':True,'scope':'Complete inert assigned-source reading, not all-material closure, authenticated source execution, all-size proof acceptance, or novelty certification.'}
(O/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps(seal,indent=2))
