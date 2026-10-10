#!/usr/bin/env python3
"""Positive encoding sanity check with a pinned known 16-operation circuit."""
from smt_search import smt,solve,bv
from pathlib import Path
import json,time
p=Path('results');cert=json.loads((p/'synthetic_staged_baseline_certificate.json').read_text())
src=smt(16,5000);asserts=[]
for g,gate in enumerate(cert['gates'],8):
    assert gate['op']=='add'
    (a,sa),(b,sb)=sorted(gate['terms'])
    asserts.extend(['(assert (= a_%d %s))'%(g,bv(a)), '(assert (= b_%d %s))'%(g,bv(b)), '(assert (= op_%d %s))'%(g,bv(0)), '(assert (= sa_%d %s))'%(g,str(sa==-1).lower()), '(assert (= sb_%d %s))'%(g,str(sb==-1).lower())])
src=src.replace('(check-sat)','\n'.join(asserts)+'\n(check-sat)');(p/'positive_control.smt2').write_text(src)
t=time.monotonic();out=solve(src);elapsed=time.monotonic()-t
assert out.splitlines()[0]=='sat',out
(p/'positive_control.log').write_text(out);(p/'positive_control.json').write_text(json.dumps({'status':'sat','gates':16,'pinned_baseline':True,'elapsed_seconds':elapsed},indent=2))
print('Pinned16-operation positive SMT control:SAT')
