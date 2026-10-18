"""Independent enclosure containment and sealed-evidence crosscheck; no runtime imports."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
source=Path(__file__).resolve().parent.parent / 'candidate'
author=json.loads((source/'TRUE_TARGET_INTERVALS.json').read_text())
review=json.loads((root/'TRUTH_257.json').read_text())
assert len(author['rows'])==len(review['rows'])==257
lift=1<<(review['bits']-author['bits'])
checks=0
for a,b in zip(author['rows'],review['rows']):
    assert a['row']==b['ell'] and a['terms']==b['count']
    for ka,kb in (('real_interval','real'),('imag_interval','imag')):
        assert a[ka][0]*lift<=b[kb][0]<=b[kb][1]<=a[ka][1]*lift,(a['row'],ka)
        checks+=1
manifest=source/'MANIFEST.json'
seal=json.loads((source/'SEAL.json').read_text())
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==seal['manifest_sha256']
assert len(json.loads(manifest.read_text())['files'])==seal['members']
result={'status':'PASS','contained_coordinate_intervals':checks,'row_count':257,'author_bits':author['bits'],'review_bits':review['bits'],'manifest_seal_verified':True}
(root/'ORACLE_CROSSCHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
