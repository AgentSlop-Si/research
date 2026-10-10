"""Standalone exact/analytic certificate collector (not a discovery oracle)."""
import argparse
import json
from phase36_phase_rigidity import (
    exact_four_point_certificate, complex_gauge_audit,
    complex_single_cycle_phase_certificate, necessary_middle_phase_rank,
)
from phase36_two_mask import sandwich_phase_floor


def build():
    n_values=[4,8,16,32,64,128,256,512,1024,4096,65536]
    return dict(phase=36,
       exact_Qi_crossratio=exact_four_point_certificate(),
       complex_roots_of_unity=[complex_gauge_audit(n) for n in (4,8,16,32,64)],
       full_phase_rank_counterexample=[complex_single_cycle_phase_certificate(n) for n in (4,8,16,32)],
       all_size_spectral_floor=[dict(N=n,operator_error_floor=sandwich_phase_floor(n,.02,.02),
                              necessary_middle_phase_rank=necessary_middle_phase_rank(n,.02,.02)) for n in n_values])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='phase_certificate.json')
    args=ap.parse_args()
    result=build()
    with open(args.output,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    for x in result['all_size_spectral_floor']:
        print(x)
    print('wrote',args.output)
