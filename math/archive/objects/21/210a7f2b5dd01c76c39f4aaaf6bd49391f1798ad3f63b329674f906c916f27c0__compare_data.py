import json, hashlib
from pathlib import Path
s=json.loads(Path('source/EXACT_THREE_GREEN_RESULTS.json').read_text());r=json.loads(Path('INDEPENDENT_RESULTS.json').read_text())
assert s['target']==r['target'] and s['discriminant']==r['discriminant']
convert=lambda x:[x['constant'],x['delta']]
assert list(map(convert,s['u']))==r['u'] and list(map(convert,s['v']))==r['v'] and list(map(convert,s['diagonal_correction']))==r['diagonal']
assert convert(s['pole_t'])==r['pole']
print('Source numerical field data agree with independent target, pole, endpoints, correction and discriminant.')
