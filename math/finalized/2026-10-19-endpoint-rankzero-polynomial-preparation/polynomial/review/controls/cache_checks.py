"""Independent exact cache/retry/error-budget control; no imported research code."""
from fractions import Fraction as F
import json
from pathlib import Path
sequences=[list(range(1,301)),list(range(300,0,-1)),[1,8,3,127,4,63,500,2,1000000,1,999999,4]]
rows=[]
for requests in sequences:
    cache=0;builds=[]
    for A in requests:
        if cache < A+2:
            cache=1<<(A+1).bit_length()
            builds.append(cache)
        assert cache>=A+2
        for m in [3,4,6,65]:
            f=A+(m).bit_length()+4
            total_cached_and_truncation=F(1,1<<(cache+1))+2*(m+1)*F(1,1<<f)
            assert total_cached_and_truncation<F(1,1<<A)
    assert max(builds)<2*(max(requests)+2)
    assert len(builds)<=(max(requests)+2).bit_length()
    assert F(sum(b**3 for b in builds),max(builds)**3)<=F(8,7)
    rows.append({'requests':len(requests),'maximum_request':max(requests),'constructed_precisions':builds,'last_precision_overrequest_bound':True,'geometric_cubic_cost_bound':True,'all_error_budgets_pass':True})
p=Path(__file__).resolve().parents[1]/'evidence'/'CACHE_RESULTS.json'
p.write_text(json.dumps({'status':'PASS','sequences':rows},indent=2)+'\n')
print(p.read_text())
