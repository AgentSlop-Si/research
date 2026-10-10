"""Optional large-N exact-arithmetic-count / approximate-real calibration stress test."""
import json, numpy as np
from phase36_two_mask import make_green_triplet, sinkhorn_green, sandwich_phase_floor


def audit_sizes(sizes=(1024,4096,16384,65536)):
    out=[]
    for n in sizes:
        A,B,C=make_green_triplet(n)
        circuit,fit=sinkhorn_green(A,B,C)
        e0=np.zeros(n);e0[0]=1
        ec=max(np.max(np.abs(circuit.apply(e0)-1)),
               np.max(np.abs(circuit.transpose_apply(e0)-1)))
        e1=np.zeros(n);e1[1]=1
        second=circuit.apply(e1)
        expected=np.exp(-2j*np.pi*np.arange(n)/n)
        result=dict(N=n,iterations=fit['iterations'],
                    first_cross_max_error=float(ec),
                    second_column_max_error=float(np.max(np.abs(second-expected))),
                    phase_spectral_lower_bound=sandwich_phase_floor(n,.02,.02),
                    green_apply_arithmetic='O(N)',
                    sinkhorn_preprocessing='O(N log(1/tolerance)) field-arithmetic model')
        assert result['first_cross_max_error'] < 2e-10
        assert result['second_column_max_error'] >1.
        out.append(result)
        print('N={} iterations={} cross error {:.2e} next error {:.2f}'.format(
             n,fit['iterations'],result['first_cross_max_error'],result['second_column_max_error']))
    return out

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='large_audit.json')
    args=ap.parse_args()
    results=audit_sizes()
    with open(args.output,'w') as f:
        json.dump(results,f,indent=2)
        f.write('\n')
