import json, pathlib
root=pathlib.Path(__file__).resolve().parent
c=json.loads((root/'sources/CHART.json').read_text())
assert c['N']==8 and c['product_order']=='M=S2*S1' and c['sum_coefficients']==[1,1,1]
assert [s['seed'] for s in c['stages']]==[42420,42520]
assert c['free_phase_indices']==list(range(7,24))
cycles=[s['cycles'] for s in c['stages']]
pairs=[s['gaussian_pairs'] for s in c['stages']]
assert all(sorted(cy)==list(range(8)) for stage in cycles for cy in stage)
assert all(len(st)==17 for st in pairs)
def arr(x):return '{'+','.join(arr(a) if isinstance(a,list) else str(a) for a in x)+'}'
(root/'chart_generated.h').write_text('// Generated only from pinned CHART.json.\nstatic const int CYC[2][3][8]='+arr(cycles)+';\nstatic const int GAUSS[2][17][2]='+arr(pairs)+';\n')
