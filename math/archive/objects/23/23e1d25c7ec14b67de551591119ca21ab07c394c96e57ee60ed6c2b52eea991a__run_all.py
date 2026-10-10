from __future__ import annotations
import json, unittest
from cyclotomic_packet import run_packet_checks, run_apply_checks
from rational_scan_gate import random_gate_cases
from separator_inverse_gate import separator_checks, treewidth_lower_bound


def make_results():
    packets=run_packet_checks()
    apply=run_apply_checks()
    rational=random_gate_cases()
    separator=separator_checks()
    return {
        'packet_matrix_cases':len(packets),
        'packet_apply_cases':len(apply),
        'rational_scan_cases':sum('denominator_degree' in r for r in rational),
        'fourier_block_cases':sum('fourier_n' in r for r in rational),
        'separator_cases':sum('inverse_cross_rank' in r for r in separator),
        'max_rational_rank_excess':max((r['rectangle_rank']-r['denominator_degree'] for r in rational if 'denominator_degree' in r),default=0),
        'max_separator_rank_excess':max((r['inverse_cross_rank']-r['separator'] for r in separator if 'inverse_cross_rank' in r),default=0),
        'treewidth_bounds':[{"n":n,"w_min":treewidth_lower_bound(n)} for n in (17,101,1009)],
        'packet_records':packets,
        'separator_records':separator,
    }

if __name__=='__main__':
    suite=unittest.defaultTestLoader.discover('.',pattern='test_checkpoint.py')
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): raise SystemExit(1)
    data=make_results()
    with open('results.json','w') as f: json.dump(data,f,indent=2,sort_keys=True)
    print(json.dumps(data,indent=2,sort_keys=True))
