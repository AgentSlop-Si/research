"""Paid frontend rejection controls through the integrated adapter boundary."""
from pathlib import Path
import json
from integrated_centered import IntegratedCentered
import centered_source as front
HERE=Path(__file__).resolve().parent

def main():
    base={'m':11,'F':0,'kind':'constant','data':[-3,5]}
    controls=[]
    cases=[]
    x=dict(base);x['data']=[0,0];cases.append(('zero_outside_nonzero_family',x))
    x=dict(base);x['F']=100;cases.append(('scale_outside_outer_contract',x))
    x=dict(base);x['m']=10;cases.append(('too_small_for_provider',x))
    x=dict(base);x['data']=[True,5];cases.append(('boolean_component',x))
    x=dict(base);x['kind']='dense';x['data']=[[-3,5] for _ in range(512)];x['data'][-1]=[-1,5];cases.append(('changed_last_dense_coordinate',x))
    for label,x in cases:
        try:IntegratedCentered(x)
        except front.Rejected as error:
            controls.append({'name':label,'rejected':True,'reason':str(error),'front_paid_prefix':error.receipt})
        else:raise AssertionError(label)
    assert controls[-1]['front_paid_prefix']['events']['dense_coordinate_visits']==512
    (HERE/'BOUNDARY_CONTROLS.json').write_text(json.dumps({'controls':controls,
        'scope':'Five actual frontend rejections via integrated entry; no downstream numerical preparation is reached. Fixed adapter entry type/control overhead is O(1), in addition to these front receipts.'},indent=2)+'\n')
    print(json.dumps({'paid_rejections':len(controls),'changed_last_dense_coordinate_visits':512}))
if __name__=='__main__':main()
