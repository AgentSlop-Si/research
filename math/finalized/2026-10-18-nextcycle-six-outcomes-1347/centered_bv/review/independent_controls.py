"""Reexecute admitted/rejected source controls and independently audit complex values."""
from independent_review import *
sys.path.insert(0,str(HERE/'candidate'))
import bounded_variation as B

def main():
    kept=json.loads((SOURCE/'FRESH_CHECKS.json').read_text());base={'m':11,'F':0,'kind':'blocks','data':[[173,1,0],[384,2,0],[512,-1,0]]}
    cases=[('zero',dict(base,data=[[512,0,0]])),('noncanonical_grid',dict(base,data=[[512,2,0]])),
        ('boolean',dict(base,data=[[512,True,0]])),('equal_adjacent_blocks',dict(base,data=[[123,1,0],[512,1,0]])),
        ('unordered_endpoints',dict(base,data=[[123,1,0],[122,2,0],[512,1,0]])),('missing_tail',dict(base,data=[[511,1,0]])),
        ('too_large_scale',dict(base,F=-1000)),('oversized_exponent',dict(base,F=1<<200)),
        ('too_large_variation',dict(base,data=[[(512*j)//9,(-1)**(j-1),0] for j in range(1,10)])),
        ('changed_last_exceeds_variation',dict(base,kind='dense',data=[[1,0] for _ in range(511)]+[[9999,0]])),
        ('too_many_runs_after_full_scan',dict(base,kind='dense',data=[[(-1)**j,0] for j in range(512)]))]
    evidence=[]
    for (name,obj),stored in zip(cases,kept['rejection_controls']):
        ledger=B.Ledger()
        try:B.recognize(obj,ledger)
        except B.Rejected as error:
            assert name==stored['name'] and str(error)==stored['reason']
            assert ledger.report()==stored['receipt'],name
            evidence.append({'name':name,'paid_prefix_reproduces':True})
        else:raise AssertionError(name)
    dense=[[1,0]]*173+[[2,0]]*211+[[-1,0]]*128
    a=B.recognize(base,B.Ledger());b=B.recognize(dict(base,kind='dense',data=dense),B.Ledger())
    da,db=asdict(a),asdict(b);da.pop('input_kind');db.pop('input_kind');assert da==db
    staircase=B.recognize({'m':11,'F':0,'kind':'dense','data':[[1+j//64,0] for j in range(512)]},B.Ledger())
    assert asdict(staircase)=={**kept['nonconstant_staircase'],'blocks':tuple(tuple(v) for v in kept['nonconstant_staircase']['blocks'])}
    edge=B.recognize(dict(base,data=[[64*(j+1),(-1)**j,0] for j in range(8)]),B.Ledger());assert edge.variation_factor==8
    values=[[1,1]]*73+[[-2,1]]*138+[[1,-2]]*301;src=kept['complex_source']
    target=direct_targets(values,2048,255,src['h']);pairs=[]
    for record in kept['complex_coefficient_checks']:
        k=record['signed_frequency'];sq=squared_error(record['pair'],target[k%2048],192)
        assert sq<=Fraction(1,1<<384)
        pairs.append({'signed_frequency':k,'independent_squared_error_upper':fj(sq)})
    report={'all_eleven_rejection_prefixes_identical':True,'rejections':evidence,'dense_blocks_same_source':True,
        'staircase_and_budget_boundary_pass':True,'complex_coefficients_independently_checked':pairs,
        'scope':'Fresh recognizer calls; seven saved complex estimates checked with independent algebraic direct sums, without regenerating those seven estimates.'}
    dump('INDEPENDENT_CONTROLS.json',report)
    print(json.dumps({'rejection_prefixes_reproduced':len(evidence),'complex_coefficients_checked':len(pairs)}))
if __name__=='__main__':main()
