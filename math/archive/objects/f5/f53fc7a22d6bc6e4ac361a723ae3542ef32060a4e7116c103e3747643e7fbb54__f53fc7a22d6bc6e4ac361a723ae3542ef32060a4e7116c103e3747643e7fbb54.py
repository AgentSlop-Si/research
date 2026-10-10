"""Auditable arithmetic proxies, not wall-clock or same-accuracy speedup claims.
Includes modular field multiplies/adds/inverses inside rational vs Bluestein;
preconditioner and Green solve are common O(N) tolls, itemized separately.
"""
import json,random,time
from pathlib import Path
from rational_forcing import (AllLengthGreen,forcing_from_sparse,bluestein_transform,
                              PolyStats,P0,G0)


def run():
    rng=random.Random(20261010)
    rows=[]
    for n,p,g in [(119,998244353,3),(256,P0,G0),(1024,P0,G0),(4096,P0,G0)]:
        eng=AllLengthGreen(n,p,g)
        # use r directly to compare FFT forcing strategies, same output length,
        # then separately account for P and L linear operations.
        full=PolyStats()
        generic=[rng.randrange(p) for _ in range(n)]
        fb,_=bluestein_transform(generic,n,eng.omega,p,g,full)
        blu_ops=full.total_field_ops()
        for k in sorted({1,2,3,4,8,16,32,min(n,64)}):
            if k>n:continue
            entries={j:rng.randrange(1,p) for j in rng.sample(range(n),k)}
            st=PolyStats()
            t0=time.perf_counter()
            y,_=forcing_from_sparse(entries,n,eng.omega,p,g,st)
            elapsed=time.perf_counter()-t0
            row={'N':n,'K':k,
                 'rational_field_op_proxy':st.total_field_ops(),
                 'full_bluestein_field_op_proxy':blu_ops,
                 'ratio_rational_to_full':round(st.total_field_ops()/blu_ops,5),
                 'short_ntt_calls':st.ntt_calls,
                 'max_short_ntt_length':st.max_ntt_length,
                 'full_bluestein_max_ntt_length':full.max_ntt_length,
                 'rational_blocks':st.rational_blocks,
                 'kernel_cache_builds':st.cached_kernel_transforms,
                 'kernel_cache_hits':st.cached_kernel_hits,
                 'short_twiddle_plans_built':st.twiddle_tables_built,
                 'short_twiddle_plan_hits':st.twiddle_table_hits,
                 'rational_elapsed_seconds':round(elapsed,5),
                 'green_common_P_and_L_field_toll_upper':8*n+1,
                 'primitive_root_discovery_included_in_both':False,
                 'prime':p}
            # Validate without N^2 reference using independent Bluestein.
            v=[entries.get(j,0) for j in range(n)]
            z,_=bluestein_transform(v,n,eng.omega,p,g)
            assert y==z,(n,k)
            rows.append(row)
    summary={'metric':'Scalar modular field addition/multiplication/inversion count in code; does not include P/L factor setup, memory, prime search, bit complexity, primitive root discovery or Python overhead',
             'rows':rows,'count':len(rows),'passed':True}
    out=Path(__file__).with_name('BENCH_RESULTS.json')
    out.write_text(json.dumps(summary,indent=2)+'\n')
    for d in rows:
        print('N=%4d K=%2d ratio=%6.3f short_max=%3d full_max=%5d'%(d['N'],d['K'],d['ratio_rational_to_full'],d['max_short_ntt_length'],d['full_bluestein_max_ntt_length']))
    return summary

if __name__=='__main__':run()
