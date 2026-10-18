"""Fresh support-blind, fixed-family finite BUCKETS recovery decoder.

The provider is trusted to meet the accepted numerical contract. Its private
raw source/descriptor is not passed into this module or inspected by recover.
An ordinary output is probabilistic, not a verified isolation certificate.
"""
from pathlib import Path
from hashlib import sha256
from importlib.util import spec_from_file_location, module_from_spec
import sys, json

BASE=Path(__file__).resolve().parent
M=1<<28; B=1<<17; T=2048; P=464; K=560; THETA_BITS=400
PIN='5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed'

def roots_module():
    path=BASE/'vendor/vendor/sparse_supplier.py'
    data=path.read_bytes()
    if sha256(data).hexdigest()!=PIN: raise ValueError('root primitive source pin')
    name='recovery_root_primitives_'+PIN[:12]
    if name not in sys.modules:
        spec=spec_from_file_location(name,path); module=module_from_spec(spec)
        sys.modules[name]=module; spec.loader.exec_module(module)
    return sys.modules[name],len(data)

def nearest(n,d):
    q,r=divmod(n,d)
    return q+int(2*r>d or (2*r==d and q&1))

def nearest_bin(n,sigma):
    v=(-sigma*n)%M
    j=nearest(v,T)%B
    q=(j*T+sigma*n)%M
    return j,min(q,M-q)

def recover(provider,sigma):
    """Use only provider.buckets(sigma,tau) and provider.window(d).

    buckets returns a tuple of B complex P-grid integer pairs. window returns
    (lower,upper) K-grid endpoints for the fixed original K(d), and is charged
    by provider. Neither API supplies support entries or active-bin metadata.
    """
    if type(sigma)is not int or not 0<sigma<M or not sigma&1:
        raise ValueError('odd multiplier in [1,M) required')
    sup,source_bytes=roots_module(); ledger=sup.Meter()
    roots,unused,D=sup.root_setup(28,256,ledger)
    stats={'coordinate_visits':0,'threshold_tests':0,'bit_decisions':0,
           'schedule_calls':0,'window_calls':0,'candidate_count':0,
           'source_bytes':source_bytes+len(Path(__file__).read_bytes()),
           'logical_retained_slots':0,'logical_output_writes':0}
    schedule=[]
    def get(tau):
        z=provider.buckets(sigma,tau)
        if type(z)is not tuple or len(z)!=B: raise ValueError('bucket shape')
        stats['schedule_calls']+=1; schedule.append([sigma,tau])
        for pair in z:
            stats['coordinate_visits']+=1
            if (type(pair)is not tuple or len(pair)!=2 or
                any(type(v)is not int or abs(v).bit_length()>480 for v in pair)):
                raise ValueError('finite bucket integer grammar/width')
        return z
    base=get(0); threshold_sq=1<<(2*(P-THETA_BITS)); candidates=[]
    for j,(a,b) in enumerate(base):
        stats['threshold_tests']+=1
        if a*a+b*b>=threshold_sq:
            candidates.append(j)
            if len(candidates)>64: raise ValueError('candidate cap; no recovery claim')
    stats['candidate_count']=len(candidates)
    stats['logical_retained_slots']=4*B+8*len(candidates)
    low={j:0 for j in candidates}
    margins=[]
    for bit in range(28):
        shifted=get(M>>(bit+1)); local_margin=None
        for j in candidates:
            br,bi=base[j]; pr,pi=shifted[j]
            # Exact cross product of two P-grid values.
            cr=pr*br+pi*bi; ci=pi*br-pr*bi
            root=sup.root_at(low[j],bit+1,roots,D,ledger)
            # root_at is negative sign; conjugate for positive phase correction.
            rr=root[0]; ri=(-root[1][1],-root[1][0])
            aa=(cr*rr[0],cr*rr[1]); bb=(ci*ri[0],ci*ri[1])
            lo=min(aa)-max(bb); hi=max(aa)-min(bb)
            if lo>0: margin=lo
            elif hi<0: low[j]|=1<<bit; margin=-hi
            else: raise ValueError('uncertain finite phase sign; no recovery claim')
            local_margin=margin if local_margin is None else min(local_margin,margin)
            stats['bit_decisions']+=1
        margins.append(local_margin)
    indices=sorted(set(low.values()))
    if len(indices)>16: raise ValueError('decoded support cap; no recovery claim')
    rows=[]; witnesses=[]; S=1<<K
    for n in indices:
        # Reject decoded collisions/forgeries inconsistent with every candidate.
        for j in candidates:
            if low[j]==n:
                q=(j*T+sigma*n)%M
                if min(q,M-q)>=2*T: raise ValueError('decoded bucket geometry')
        j,d=nearest_bin(n,sigma)
        if d>T//2: raise ValueError('nearest bin invariant')
        w=provider.window(d); stats['window_calls']+=1
        if (type(w)is not tuple or len(w)!=2 or
            any(type(v)is not int or abs(v).bit_length()>580 for v in w) or
            w[0]>w[1] or w[1]<S or w[1]-w[0]>(1<<82)):
            raise ValueError('window finite enclosure contract')
        lo=max(w[0],S); hi=w[1]; mid=(lo+hi)//2
        re,im=base[j]
        qr=nearest(re*S,mid); qi=nearest(im*S,mid)
        rows.append([(-n)%M,qr,qi]); witnesses.append([n,j,d])
        stats['logical_output_writes']+=1
    rows.sort()
    result={'schema':'ALG034_RESTRICTED_RECOVERY_V1',
        'status':'RANDOMIZED_RESTRICTED_RECOVERY_OUTPUT',
        'target':'R(x)/alpha for the bounded sparse-original singleton family',
        'sigma':sigma,'schedule':schedule,'value_bits':P,'rows':rows,
        'nearest_bin_witnesses':witnesses,'candidate_bins':candidates,
        'candidate_source_indices':[low[j] for j in candidates],
        'phase_sign_minimum_integer_margins':margins,
        'minimum_phase_margin_scale':-(2*P+256),
        'conditional_component_complex_error_power':-462,
        'conditional_l2_error_bound':{'coefficient':9,'power_two':-400},
        'success_probability_lower_bound':{'numerator':2033,'denominator':2048},
        'probability_condition':'uniform independent odd sigma; fixed admitted source; trusted bounded-error provider',
        'runtime_isolation_certificate':False,'exact_all_support_claim':False,
        'dense_or_outer_transfer_claim':False,'stats':stats}
    # A bounded canonical export plus all caller-visible result/control work.
    encoded=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    stats['serialized_result_bytes']=len(encoded)
    root_report=ledger.snapshot()
    E=(stats['coordinate_visits']+10*stats['threshold_tests']+
       4096*stats['bit_decisions']+4096*stats['window_calls']+
       stats['logical_retained_slots']+stats['logical_output_writes']+
       stats['source_bytes']+len(encoded)+root_report['operations']+65536)
    V=4096+E.bit_length()+64
    result['consumer_receipt']={'root_primitives':root_report,'charged_units':E,
        'width_envelope_bits':V,'total_bit_work_upper':root_report['total_bit_work_upper']+(1<<16)*E*V**3+(1<<100),
        'cumulative_storage_upper_bits':root_report['cumulative_storage_upper_bits']+4096*E*V+(1<<50),
        'provider_cost_included':False,'one_result_export_included':True,
        'model':'bounded schoolbook binary-work/cumulative-logical-storage envelope, not time or RSS'}
    return result
