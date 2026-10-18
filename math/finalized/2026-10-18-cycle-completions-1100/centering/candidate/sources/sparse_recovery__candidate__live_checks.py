"""New recovery controls, including complete original-bound live schedules.
No author BUCKETS tests are rerun. Existing modules are pinned dependencies.
"""
from pathlib import Path
from hashlib import sha256
from math import gcd
import sys,json,time
from copy import deepcopy
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'vendor'))
import recovery

PINS={'nonconstant_buckets.py':'9b6accac4781c07a7e06acfa4239762b0cf21503bf619d7138971ce0c00d9993',
 'sparse_adapter.py':'cdbe745859a7f729c26e43f1476bacb5d8ee0f0ee656ab5bf2674e102332efa7',
 'vendor/sparse_supplier.py':'5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed'}
for path,pin in PINS.items():
    assert sha256((BASE/'vendor'/path).read_bytes()).hexdigest()==pin
from sparse_adapter import SparseAdapter

M=recovery.M; B=recovery.B; P=recovery.P

class LiveProvider:
    def __init__(self,raw,state):
        self.raw=deepcopy(raw);self.state=deepcopy(state)
        self.adapters=[];self.calls=0;self.schedule=[];self.bound_headers=[]
    def buckets(self,sigma,tau):
        if self.calls%6==0: self.adapters.append(SparseAdapter())
        run=self.adapters[-1].execute(self.raw,self.state,t=16,q=P,sigma=sigma,tau=tau)
        # Only the finite values cross the decoder interface.
        self.bound_headers.append(sha256(run.header_bytes).hexdigest())
        self.schedule.append([sigma,tau]);self.calls+=1
        return run.numerators
    def window(self,d):
        w=self.adapters[-1].engine.window(d)
        return w.lo,w.hi
    def receipt(self):
        receipts=[a.receipt() for a in self.adapters]
        # Reading/hash binding every header, retained raw/state copies, schedule
        # bookkeeping, receipt collection and the caller's output JSON writes.
        caller_work=1<<110;caller_storage=1<<60
        return {'groups':receipts,'preparations':len(receipts),'calls':self.calls,
          'full_bucket_coordinates':self.calls*B,'header_hashes':self.bound_headers,
          'caller_work_upper':caller_work,'caller_cumulative_storage_upper_bits':caller_storage,
          'total_bit_work_upper':sum(x['total_bit_work_upper'] for x in receipts)+caller_work,
          'cumulative_storage_upper_bits':sum(x['cumulative_storage_upper_bits'] for x in receipts)+caller_storage}

def check_output(raw,result):
    entries=raw['entries'];E=sum(re*re+im*im for _,re,im in entries)
    h=((E-1).bit_length()+1)//2
    original={(-n)%M:(re,im) for n,re,im in entries}
    returned={n:(re,im) for n,re,im in result['rows']}
    assert set(returned)<=set(original)
    common=max(h,P);total_error=0;max_component=0
    heavy=[]
    for n,(re,im) in original.items():
        # All |a|>=2 theta must occur; compare squared norms exactly.
        if (re*re+im*im)*(1<<(2*399)) >= (1<<(2*h)):
            heavy.append(n);assert n in returned
        qr,qi=returned.get(n,(0,0))
        er=(qr<<(common-P))-(re<<(common-h))
        ei=(qi<<(common-P))-(im<<(common-h))
        error=er*er+ei*ei;total_error+=error
        if n in returned:
            assert error <= 1<<(2*(common-462))
            max_component=max(max_component,error)
    assert total_error*(1<<800) <=81*(1<<(2*common))
    return {'h':h,'actual_support':len(entries),'recovered_support':len(returned),
        'heavy_indices':heavy,'omitted_indices':sorted(set(original)-set(returned)),
        'l2_error_squared_numerator':total_error,'error_common_grid_bits':common,
        'maximum_returned_component_error_squared_numerator':max_component}

def main():
    started=time.monotonic();named=[]
    # Exact exhaustive small-modulus controls for the actual 2-adic counting
    # identity used in the proof. This is not a theorem-scale N scan.
    pair_count=0
    for m in range(5,10):
        N=1<<m
        for d_exp in range(2,m-1):
            D=1<<d_exp
            for difference in range(1,N):
                actual=sum(min((a*difference)%N,(-a*difference)%N)<D for a in range(1,N,2))
                v=(difference&-difference).bit_length()-1
                expected=0 if v>=d_exp else D
                assert actual==expected; pair_count+=1
    named.append({'name':'exact_odd_multiplier_pair_count','instances':pair_count})
    # Fixed local demonstration tape; no claim that this deterministic value
    # itself implements random sampling or empirically proves probability.
    indices=[1,3,19031,982731,1234567,2880011,9081723,12345679,
             20000003,31415927,55555559,90000001,123456789,188888881,M-3,M-1]
    entries=[]
    for j,n in enumerate(indices):
        if j<12: re=(1<<1022)+(2*j+1);im=(-1 if j&1 else 1)*(1<<(1018+j%3))
        elif j==12:re=1<<626;im=0
        elif j==13:re=1<<620;im=0
        elif j==14:re=1;im=0
        else:re=-(1<<1022);im=1
        entries.append([n,re,im])
    raw={'schema':'ALG034_SPARSE_DYADIC_V1','N':M,'F':0,'entries':entries}
    state={'N':M,'B':M,'a':7,'beta':19}
    sigma=10007
    separations=[min((sigma*(x-y))%M,(sigma*(y-x))%M) for i,x in enumerate(indices) for y in indices[:i]]
    assert min(separations)>=4*recovery.T
    (BASE/'ORIGINAL_INPUT.json').write_text(json.dumps({'raw':raw,'state':state,'sigma':sigma},indent=2)+'\n')
    provider=LiveProvider(raw,state)
    result=recovery.recover(provider,sigma)
    accuracy=check_output(raw,result)
    assert result['stats']['coordinate_visits']==29*B
    assert result['stats']['schedule_calls']==29
    assert provider.calls==29
    assert len(result['rows'])>1
    # The newly exposed recovery gap is exercised by a permitted tiny mode.
    assert (-indices[14])%M in accuracy['omitted_indices']
    result['original_binding']={'raw_and_state_path':'ORIGINAL_INPUT.json',
       'raw_and_state_sha256':sha256((BASE/'ORIGINAL_INPUT.json').read_bytes()).hexdigest(),
       'independently_retained_original_required':True,'external_authentication':False}
    receipt=provider.receipt()
    result['provider_receipt']=receipt
    result['combined_receipt']={'total_bit_work_upper':receipt['total_bit_work_upper']+result['consumer_receipt']['total_bit_work_upper'],
       'cumulative_storage_upper_bits':receipt['cumulative_storage_upper_bits']+result['consumer_receipt']['cumulative_storage_upper_bits'],
       'production_runs':1,'replay_runs':0,'random_bits_if_uniform_sampling':27,
       'normalized_sparse_output_rows':len(result['rows']),'all_N_output_materialized':False}
    (BASE/'RECOVERY_RUN.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    named.append({'name':'complete_29_call_original_bound_recovery','minimum_hashed_pair_separation':min(separations),**accuracy})
    # Exact counterexample inequalities, independent of the live execution.
    c=(1<<1023)+1;e0=c*c;e1=e0+1
    assert ((e0-1).bit_length()+1)//2==1024
    assert ((e1-1).bit_length()+1)//2==1024
    assert 3073*(1<<464)<(1<<1022) # perturbation <rho/4, much smaller in fact
    assert 3073<(1<<12)
    named.append({'name':'exact_support_oracle_indistinguishability','normalizer_h':1024,'difference_power_two':-1024,
      'uniform_bucket_difference_upper':{'coefficient':3073,'power_two':-1024}})
    # Strict value-only API boundary and visible finite failure outcomes.
    class Malformed:
        def buckets(self,sigma,tau):return ((0,0),)*(B-1)+((0.0,0),)
    try:recovery.recover(Malformed(),1)
    except ValueError as e:assert 'grammar' in str(e)
    else:raise AssertionError('float intake accepted')
    named.append({'name':'reject_float_bucket_value'})
    class Ambiguous:
        def buckets(self,sigma,tau):
            return ((1<<(P-400),0),)+((0,0),)*(B-1) if tau==0 else ((0,0),)*B
    try:recovery.recover(Ambiguous(),1)
    except ValueError as e:assert 'uncertain finite phase' in str(e)
    else:raise AssertionError('uncertain phase accepted')
    named.append({'name':'reject_uncertain_phase_sign'})
    out={'status':'PASS_NEW_RESTRICTED_RECOVERY_CONTROLS','named_checks':named,
       'elapsed_seconds':time.monotonic()-started,'dependency_pins':PINS,
       'independent_final_review':False,'prior_accepted_tests_rerun':False,
       'external_writes':False}
    (BASE/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'seconds':out['elapsed_seconds'],'rows':len(result['rows']),
       'candidates':result['stats']['candidate_count'],'full_bucket_coordinates':29*B}))

if __name__=='__main__':main()
