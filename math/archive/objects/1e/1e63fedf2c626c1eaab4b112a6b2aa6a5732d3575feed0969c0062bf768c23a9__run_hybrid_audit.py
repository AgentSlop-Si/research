"""Focused checks that discovery is paid on both fast and fallback paths."""
import json
import random
from pathlib import Path
from adaptive_recurrence import PrimeField
from hybrid import prepare_hybrid,apply_hybrid


def direct(field,roots,amplitudes,n):
    out=[]
    for j in range(n):
        value=field.zero
        for root,amplitude in zip(roots,amplitudes):
            value=field.add(value,field.mul(amplitude,field.power(root,j)))
        out.append(value)
    return out


def main():
    field=PrimeField(65537)
    rng=random.Random(20261011)
    cases=[]
    for n,label,indices in (
        (4096,'two partial fibers',[a+256*j for a in (1,3) for j in range(8)]),
        (1024,'unstructured fallback',rng.sample(range(1024),128))):
        root=field.root(n)
        roots=[field.power(root,j) for j in indices]
        k=len(roots);length=max(2,1<<(k-1).bit_length())
        eta=field.power(root,n//(2*length))
        plan=prepare_hybrid(field,n,roots,eta)
        amplitudes=[rng.randrange(65537) for _ in roots]
        y,counts=apply_hybrid(field,plan,amplitudes)
        assert y==direct(field,roots,amplitudes,n)
        assert (plan.method=='sparse_annihilator')==(label=='two partial fibers')
        assert sum(counts['field_operations'].values())<=min(
            plan.adaptive_online_total,plan.baseline_additional_total)
        cases.append(dict(n=n,k=k,label=label,method=plan.method,
                selected_stride=plan.adaptive.stride,taps=len(plan.adaptive.taps),
                discovery=plan.adaptive.preparation,preparation=plan.preparation,
                online=counts['field_operations'],
                adaptive_online_total=plan.adaptive_online_total,
                baseline_additional_total=plan.baseline_additional_total,
                cold_total=sum(plan.preparation.values())+sum(counts['field_operations'].values()),
                returned_output_count=len(y),status='PASS'))
    result=dict(status='PASS',cases=cases,
                scope='charged adaptive recurrence with ordinary FFT fallback; no universal little-o gain')
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
    (out/'hybrid_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
