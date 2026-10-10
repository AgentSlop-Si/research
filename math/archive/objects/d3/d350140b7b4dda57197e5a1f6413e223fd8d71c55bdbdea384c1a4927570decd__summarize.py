"""Stratify approximate timing results by actual information retained."""
import json
from pathlib import Path


def group_summary(rows):
    if not rows:return {'cases':0}
    return {'cases':len(rows),
            'native_median_wins':sum(x['ratio_to_faster_native_baseline']<1 for x in rows),
            'numpy_median_wins':sum(x['ratio_to_numpy']<1 for x in rows),
            'native_nonoverlapping_middle_half_wins':sum(x['native_iqr_separated_win'] for x in rows),
            'numpy_nonoverlapping_middle_half_wins':sum(x['numpy_iqr_separated_win'] for x in rows),
            'native_ratio_range':[min(x['ratio_to_faster_native_baseline'] for x in rows),
                                  max(x['ratio_to_faster_native_baseline'] for x in rows)],
            'numpy_ratio_range':[min(x['ratio_to_numpy'] for x in rows),
                                 max(x['ratio_to_numpy'] for x in rows)],
            'relative_l2_error_range':[min(x['relative_l2_error'] for x in rows),
                                       max(x['relative_l2_error'] for x in rows)]}


def main():
    root=Path(__file__).resolve().parent
    report=json.loads((root/'results.json').read_text())
    rows=report['results']
    for row in rows:
        same=[x for x in rows if x['n']==row['n'] and x['family']==row['family']]
        native=min((x for x in same if x['method'] in ('native_dit','native_dif')),
                   key=lambda x:x['median_seconds'])
        numpy=next(x for x in same if x['method']=='numpy')
        row['native_iqr_separated_win']=row['q75_seconds']<native['q25_seconds']
        row['numpy_iqr_separated_win']=row['q75_seconds']<numpy['q25_seconds']
    approx=[r for r in rows if r['method'].startswith('epsilon_')]
    retained=[r for r in approx if not r['all_zero_output']]
    accurate=[r for r in retained if r['relative_l2_error']<=1e-10]
    zero=[r for r in approx if r['all_zero_output']]
    zero_only=[r for r in rows if r['method']=='zero_pruned']
    result={'all_approximate':group_summary(approx),
            'nonzero_outputs':group_summary(retained),
            'nonzero_and_relative_l2_error_at_most_1e_minus_10':group_summary(accurate),
            'all_zero_outputs':group_summary(zero),
            'zero_only_mode':group_summary(zero_only),
            'coherent_high_fidelity_cases':accurate,
            'notes':['Wins count median timings, not confidence statements.',
                     'All-zero responses can satisfy the global maximum-error condition while losing all energy.']}
    (root/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='coherent_high_fidelity_cases'},indent=2))


if __name__=='__main__':main()
