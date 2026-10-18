"""Additional exact finite controls and independent complex coefficient checks."""
from dataclasses import asdict
from pathlib import Path
from fractions import Fraction as F
import json,time
from bounded_variation import (recognize,coefficient,Ledger,Rejected,pi_interval,reciprocal_root)
from run_example import direct_table,upper_squared,fjson
HERE=Path(__file__).resolve().parent

def main():
    started=time.monotonic();controls=[]
    def reject(name,obj,event=None,count=None):
        L=Ledger()
        try:recognize(obj,L)
        except Rejected as err:
            if event is not None:assert L.events.get(event)==count
            controls.append({'name':name,'rejected':True,'reason':str(err),'receipt':L.report()})
        else:raise AssertionError(name)
    base={'m':11,'F':0,'kind':'blocks','data':[[173,1,0],[384,2,0],[512,-1,0]]}
    reject('zero',dict(base,data=[[512,0,0]]))
    reject('noncanonical_grid',dict(base,data=[[512,2,0]]))
    reject('boolean',dict(base,data=[[512,True,0]]))
    reject('equal_adjacent_blocks',dict(base,data=[[123,1,0],[512,1,0]]))
    reject('unordered_endpoints',dict(base,data=[[123,1,0],[122,2,0],[512,1,0]]))
    reject('missing_tail',dict(base,data=[[511,1,0]]))
    reject('too_large_scale',dict(base,F=-1000))
    reject('oversized_exponent',dict(base,F=1<<200))
    ends=[(512*j)//9 for j in range(1,10)]
    reject('too_large_variation',dict(base,data=[[end,(-1)**j,0] for j,end in enumerate(ends)]))
    dense=[[1,0] for _ in range(512)];dense[-1]=[9999,0]
    reject('changed_last_exceeds_variation',dict(base,kind='dense',data=dense),'dense_coordinate_visits',512)
    reject('too_many_runs_after_full_scan',dict(base,kind='dense',data=[[(-1)**j,0] for j in range(512)]),'dense_coordinate_visits',512)
    # Same genuine original in both input representations has same mathematical source fields.
    dense2=[[1,0]]*173+[[2,0]]*211+[[-1,0]]*128
    L=Ledger();a=recognize(base,L);b=recognize(dict(base,kind='dense',data=dense2),L)
    da,db=asdict(a),asdict(b);da.pop('input_kind');db.pop('input_kind');assert da==db
    # Dense staircase is nonconstant on 8 blocks, not only a two-step template.
    staircase={'m':11,'F':0,'kind':'dense','data':[[1+j//64,0] for j in range(512)]}
    stair=recognize(staircase,Ledger());assert len(stair.blocks)==8 and stair.variation_factor==2
    # Eight alternating runs reach the allowed variation budget exactly.
    edge=recognize(dict(base,data=[[64*(j+1),(-1)**j,0] for j in range(8)]),Ledger())
    assert edge.variation_factor==8
    # Complex coefficients at positive, negative, and zero frequencies.
    obj={'m':11,'F':0,'kind':'blocks','data':[[73,1,1],[211,-2,1],[512,1,-2]]}
    L=Ledger();src=recognize(obj,L);P=16*src.m+16;Q=P+2*src.m+len(src.blocks).bit_length()+20
    pi=pi_interval(Q,L);root=reciprocal_root(4*src.N,Q,L)
    values=[[1,1]]*73+[[-2,1]]*138+[[1,-2]]*301
    oracle,_=direct_table(values,4*src.N,(src.N-1)//2,src.h)
    checks=[]
    for k in (0,1,4,17,-1,-4,-32):
        pair=coefficient(src,k,P,pi,root,Q,L)
        sq=upper_squared([F(v,1<<P) for v in pair],oracle[k%(4*src.N)])
        assert sq<=F(1,1<<(2*P))
        checks.append({'signed_frequency':k,'pair':pair,'squared_error_upper':fjson(sq)})
    report={'rejection_controls':controls,'same_original_dense_and_blocks':True,
        'nonconstant_staircase':asdict(stair),'variation_budget_boundary':asdict(edge),
        'complex_source':asdict(src),'complex_coefficient_checks':checks,'complex_front_prefix':L.report(),
        'observed_seconds':time.monotonic()-started,
        'scope':'Partial complex coefficient evaluations plus grammar/recognition controls; not a second full outer execution. Independent oracles are harness work.'}
    (HERE/'FRESH_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'controls':len(controls),'complex_checks':len(checks),'seconds':report['observed_seconds']}),flush=True)
if __name__=='__main__':main()
