"""Supplementary independent complete-period sign/axis controls."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
source=(p/'independent_review.py').read_text().split('C=[S,S]')[0]
ns={'__file__':str(p/'independent_review.py')}
exec(compile(source,'oracle_prefix','exec'),ns)
S=ns['S'];count=0
for a in range(512):
    lo,hi=ns['sine'](a,256)
    if a%256==0: assert (lo,hi)==(0,0)
    elif a%256==128: assert (lo,hi)==((S,S) if a<256 else (-S,-S))
    else: assert lo>S//128 if a<256 else hi < -S//128
    count+=1
(p/'ORACLE_ROOT_CONTROL.json').write_text(json.dumps({'status':'PASS','full_rational_period_roots_checked':count,'nonzero_sign_intervals_separated_from_zero_by':'2^-7','purpose':'Verify independent oracle absolute-value branch and exact axes without candidate helpers'},indent=2)+'\n')
print('Independent root sign controls PASS',count)
