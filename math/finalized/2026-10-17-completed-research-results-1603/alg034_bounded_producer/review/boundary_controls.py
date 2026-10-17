"""Independent maximum declared precision and precision-cap controls."""
import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'source'))
import producer as P
out=[]
for n,b,p,expected in [(4,3,4096,'success'),(64,64,None,'success'),(64,3,4096,'success'),(4,3,4097,'RESOURCE_LIMIT')]:
    raw={'F':0,'real':[1]+[0]*(n-1),'imag':[0]*n}; state=dict(N=n,B=b,a=n-1,beta=n-1)
    started=time.monotonic()
    try:
        r=P.execute(raw,state,p=p,include_trace=True)
        assert expected=='success'
        assert r.ledger['integer_operations']<=P.MAX_OPERATIONS
        assert r.ledger['max_working_integer_bits']<=P.MAX_WORKING_BITS
        assert r.ledger['max_stored_grid_bits']<=r.policy['p']+r.policy['plan']['I']
        assert r.ledger['max_product_accumulator_bits']<=2*(r.policy['p']+r.policy['plan']['I'])+3
        assert r.ledger['serialization_bytes_upper']>=len(r.trace_bytes)+len(r.input_context)+len(r.policy_bytes)+len(r.ledger_bytes)
        assert r.adapter.target_budget=='TARGET_BUDGET_PASS'
        entry=dict(n=n,b=b,p=r.policy['p'],status=r.status,integer_operations=r.ledger['integer_operations'],max_working_integer_bits=r.ledger['max_working_integer_bits'],serialized_trace_bytes=len(r.trace_bytes))
    except P.Failure as exc:
        assert expected=='RESOURCE_LIMIT' and 'RESOURCE_LIMIT' in str(exc)
        entry=dict(n=n,b=b,p=p,status='EXPECTED_RESOURCE_STOP',exception=str(exc))
    entry['pass']=True; entry['observed_seconds_diagnostic_only']=time.monotonic()-started; out.append(entry)
    print(json.dumps(entry),flush=True)
Path(__file__).with_name('BOUNDARY_CONTROLS.json').write_text(json.dumps({'status':'PASS','checks':out},indent=2)+'\n')
