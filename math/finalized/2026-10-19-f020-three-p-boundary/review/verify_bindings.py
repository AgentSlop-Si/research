from pathlib import Path
from hashlib import sha256
import json
import sys
if len(sys.argv)!=2: raise SystemExit('Usage: python verify_bindings.py ORIGINAL_SOURCE_ROOT')
root=Path(sys.argv[1]);out=Path(__file__).parent
candidate=root/'f020_three_p_boundary_20261019_1613'
expected_report='90385545114303539d4c29e9cc6cde2383480d6ad94cad83899ecc4f1cab0762'
expected_manifest='df02f0cc8bc18de23b120a2b5f6b08dda89492c08467641d78e34026aadb8354'
def h(p):return sha256(p.read_bytes()).hexdigest()
assert h(candidate/'REPORT.md')==expected_report
assert h(candidate/'MANIFEST.json')==expected_manifest
packs=[candidate,root/'f020_two_digit_hensel_20261019_0124',root/'f020_primepower_extension_review_20261019_0124',root/'f020_third_block_extension_20261019_1347',root/'f020_third_block_review_20261019_1354']
verified=[]
for pack in packs:
    manifest=json.loads((pack/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        f=pack/entry['path'];b=f.read_bytes()
        assert len(b)==entry['bytes'] and sha256(b).hexdigest()==entry['sha256'],str(f)
        verified.append({'path':str(f),'bytes':len(b),'sha256':entry['sha256']})
for binding in json.loads((candidate/'SOURCE_BINDINGS.json').read_text()):
    assert h(Path(binding['source']))==binding['sha256']==h(candidate/binding['copy'])
a=json.loads((packs[2]/'VERDICT.json').read_text())
assert a['verdict']=='ACCEPT' and a['author_report_sha256']==h(packs[1]/'REPORT.md') and a['author_manifest_sha256']==h(packs[1]/'MANIFEST.json')
b=json.loads((packs[4]/'VERDICT.json').read_text())
assert b['verdict']=='ACCEPT' and b['candidate_report_sha256']==h(packs[3]/'REPORT.md') and b['candidate_manifest_sha256']==h(packs[3]/'MANIFEST.json')
result={'status':'PASS','candidate_report_sha256':expected_report,'candidate_manifest_sha256':expected_manifest,'candidate_manifest_entries':26,'accepted_manifest_entries':44,'source_original_copy_bindings':10,'acceptance_bindings':2,'entries':verified,'executed_prior_code':False}
assert len(verified)==70
(out/'INPUT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: 26 candidate entries, 44 accepted dependency entries, 10 original/copy bindings, both acceptance bindings.')
