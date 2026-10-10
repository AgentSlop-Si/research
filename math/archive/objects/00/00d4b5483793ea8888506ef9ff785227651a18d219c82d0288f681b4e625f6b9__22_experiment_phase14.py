"""Reproducible v14 accuracy/cost PROXIES; not runtime benchmarks.

Fidelity and costs must be displayed together: these are not comparisons
of the same-accuracy guarantee across v13/v14 or against an FFT library.
"""
import json
import math
from pathlib import Path
import numpy as np
import phase_bank as b
import gram_union as u
import mixedradix as v13
import stationary_toeplitz as st


def experiment():
    rows=[]
    for g,m,M in [(128,3,8),(256,5,8),(512,3,16)]:
        n=g*m
        mask=tuple(((2*s+1)%M,) for s in range(m))
        chirp=b.constructed_bank_signal(g,m,M,mask,seed=88)
        rng=np.random.default_rng(90+n)
        noise=rng.normal(size=n)+1j*rng.normal(size=n)
        inputs={
            'known_one_bank':chirp,
            'known_one_bank_plus_small_noise':chirp+0.01*noise,
            'incompressible_position_impulses':None,
            'generic_gaussian':noise,
        }
        pulse=np.zeros((g,m),dtype=np.complex128)
        pulse[::M,:]=1
        inputs['incompressible_position_impulses']=pulse.reshape(n)
        for label,x in inputs.items():
            if label=='known_one_bank':
                r=b.known_banks(x,mask,M)
                target=0.
            else:
                target=0.05
                r=b.adaptive_banks(x,target,M)
            y=np.fft.fft(x)/math.sqrt(n)
            actual_relative=float(np.linalg.norm(y-r.output)/np.linalg.norm(x))
            rows.append({'n':n,'g':g,'m':m,'M':M,'type':label,'requested_rel_l2':target,
                         'selected_banks':r.selected_column_banks,
                         'available_banks':r.total_column_banks,
                         'actual_relative_l2_error':actual_relative,
                         'certified_exact_arithmetic_rel_l2_error':r.theoretical_relative_l2_error,
                         'charged_work_proxy':r.work_proxy['declared_work_proxy'],
                         'baseline_v13_one_row_proxy':v13.work_proxy(n,M)['work_proxy'],
                         'standard_fft_nlog2n_proxy':n*math.log2(n),
                         'note':'Different relative-error guarantees: proxies not same-accuracy speed claims'})
        fam=u.example_noncommuting_states(g,m,M)
        structured=u.constructed_union_signal(g,m,M,fam,seed=141)
        res=u.union_projection(structured,fam,M)
        actual=float(np.linalg.norm(res.output-np.fft.fft(structured)/math.sqrt(n))/np.linalg.norm(structured))
        rows.append({'n':n,'g':g,'m':m,'M':M,'type':'known_two_noncommuting_slopes',
                     'requested_rel_l2':0.,'selected_banks':res.state_count,
                     'available_banks':m*M,'actual_relative_l2_error':actual,
                     'certified_exact_arithmetic_rel_l2_error':res.relative_l2_error_certificate,
                     'charged_work_proxy':res.work_proxy['total_proxy'],
                     'baseline_v13_one_row_proxy':v13.work_proxy(n,M)['work_proxy'],
                     'standard_fft_nlog2n_proxy':n*math.log2(n),
                     'max_gram_condition':res.maximum_gram_condition,
                     'note':'Structured-input exactness; not arbitrary-input exact transform'})
        # The stationary q=M frame is fully exact on arbitrary dense x,
        # but its M simultaneous Green scans are explicitly costed.
        full=st.stationary_eval(noise,M,M)
        fullerr=float(np.linalg.norm(full.output-np.fft.fft(noise)/math.sqrt(n))/np.linalg.norm(noise))
        rows.append({'n':n,'g':g,'m':m,'M':M,'type':'stationary_full_rank_exact_generic',
                     'requested_rel_l2':0.,'selected_banks':m*M,
                     'available_banks':m*M,'actual_relative_l2_error':fullerr,
                     'certified_exact_arithmetic_rel_l2_error':0.,
                     'charged_work_proxy':full.operation_proxy['total_proxy'],
                     'baseline_v13_one_row_proxy':v13.work_proxy(n,M)['work_proxy'],
                     'standard_fft_nlog2n_proxy':n*math.log2(n),
                     'max_gram_condition':full.gram_condition,
                     'note':'EXACT arbitrary-input Fourier, but q=M scans cost Omega(NM), not sub-FFT'})
    path=Path(__file__).parent/'EXPERIMENT_RESULTS.json'
    path.write_text(json.dumps(rows,indent=2)+'\n')
    print(f'{len(rows)} reproducible v14 input/cost diagnostics:')
    for r in rows:
        print(f"N={r['n']:4d} {r['type']:40s} pass={r['selected_banks']:3d}/{r['available_banks']:<3d} "
              f"rel_error={r['actual_relative_l2_error']:.3g}, certificate={r['certified_exact_arithmetic_rel_l2_error']:.3g}, proxy={r['charged_work_proxy']:.1f}")

if __name__=='__main__':experiment()
