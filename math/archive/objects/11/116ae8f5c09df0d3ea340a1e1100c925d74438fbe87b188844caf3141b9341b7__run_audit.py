from pathlib import Path
from fractions import Fraction
from random import Random
import hashlib,json,sys
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'fft_wordram_decoder_research'))
sys.path.insert(0,str(HERE.parent/'fft_wordram_integration'))
from guarded_decoder import GuardedDecoder
from sampling import sample_atoms,sample_count_integer
from control_variate import fit_periodic,fuse

def data(n,name):
    rng=Random(799+n); q=__import__('math').gcd(n,4)
    tile=[(10000,1000),(-12000,5000),(7000,-2000),(3000,15000)][:q]
    if name=='exact_periodic': return [tile[j%q] for j in range(n)]
    if name=='near_periodic':
        return [(tile[j%q][0]+rng.randrange(-4,5),tile[j%q][1]+rng.randrange(-4,5)) for j in range(n)]
    if name=='sparse_exceptions':
        x=[tile[j%q] for j in range(n)]
        for j in (1,n//3,n-1): x[j]=(x[j][0]+31,x[j][1]-17)
        return x
    if name=='noise': return [(rng.randrange(-99,100),rng.randrange(-99,100)) for _ in range(n)]
    if name=='spike': return [(n*1000,0) if j==0 else (0,0) for j in range(n)]
    if name=='zero': return [(0,0)]*n
    raise ValueError(name)

def main():
    records=[]; exact=0
    for n in (31,64,256):
        k=sample_count_integer(n,Fraction(1,4),Fraction(1,100))
        decoder=GuardedDecoder(n,k,block_size=4,phase_grid=64,slope_grid=256,
                               group_size=1,lane_step_bits=5,trig_bits=24,table_mode='eager')
        for index,name in enumerate(('exact_periodic','near_periodic','sparse_exceptions','noise','spike','zero')):
            x=data(n,name);answer=fuse(x,decoder,seed=801+index,cap_failure=Fraction(1,100))
            assert not answer['failed']
            fit=answer['fit']; scale=fit['scale'];lmass=fit['input_mass']
            r_mass=fit['residual_numerator_mass']/scale
            ref=np.fft.fft(np.array([complex(*p) for p in x]))
            actual=np.array([complex(a/answer['denominator'],b/answer['denominator']) for a,b in answer['integer_outputs']])
            err=float(max(abs(actual-ref)))
            # Exact rational input decomposition for every coordinate.
            for j,(a,b) in enumerate(x):
                rho=fit['residual'][j];s=fit['chosen_sums'][j%fit['period']]
                assert a*scale==s[0]+rho[0] and b*scale==s[1]+rho[1]
            assert len(actual)==n and answer['output_component_writes']==2*n+2*fit['period']
            assert r_mass<=lmass
            for key,pair in fit['exact_corner_spectrum'].items():
                assert answer['integer_outputs'][key]==tuple(v*answer['denominator'] for v in pair)
            assert err<=0.5*r_mass+1e-6
            exact+=answer['exact']
            plain_error=0.0
            if lmass:
                draw=sample_atoms(x,k,seed=801+index,cap_failure=Fraction(1,100));assert not draw['failed']
                baseline=decoder.decode(draw['samples'])
                plain_error=float(max(abs(np.array(baseline['values'])*lmass-ref)))
            records.append({'N':n,'workload':name,'exact':answer['exact'],
                            'input_mass':lmass,'residual_mass':r_mass,
                            'error_allowance_reduction':lmass/r_mass if r_mass else None,
                            'observed_fused_max_error':err,'observed_plain_max_error':plain_error,
                            'certified_high_probability_error_allowance':0.5*r_mass,
                            'exact_corner_outputs':fit['period'],'sample_count':k,
                            'cold_decoder_charged_operations':0 if answer['exact'] else sum(decoder.cold_counts.values()),
                            'note':'cold decoder setup charged in every nonzero-residual call; exact zero residual skips decoder',
                            'fit_counts':fit['counts']})
    result={'status':'PASS','cases':len(records),'exact_cases':exact,
            'all_output_comparisons':sum(v['N'] for v in records),
            'epsilon':0.5,'sampling_error_budget':0.25,'failure_bound_per_nonzero_residual_case':0.02,
            'records':records,'source_sha256':{
                'control_variate.py':hashlib.sha256((HERE/'control_variate.py').read_bytes()).hexdigest(),
                'run_audit.py':hashlib.sha256((HERE/'run_audit.py').read_bytes()).hexdigest(),
                '../fft_wordram_decoder_research/guarded_decoder.py':hashlib.sha256((HERE.parent/'fft_wordram_decoder_research/guarded_decoder.py').read_bytes()).hexdigest(),
                '../fft_wordram_integration/sampling.py':hashlib.sha256((HERE.parent/'fft_wordram_integration/sampling.py').read_bytes()).hexdigest()}}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','cases','exact_cases','all_output_comparisons')}))

if __name__=='__main__': main()
