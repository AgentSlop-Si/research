"""Fresh source-bound finite regression and numerical negative controls."""
import hashlib,json,random,time,types
from pathlib import Path
from fractions import Fraction as F
import certified_fft as backend
from independent_oracle import enclose_dft,certifies

HERE=Path(__file__).resolve().parent

def encode(value):
    if isinstance(value,F): return {'n':str(value.numerator),'d':str(value.denominator)}
    if isinstance(value,dict): return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [encode(v) for v in value]
    return value


def invoice_for_adapter_rejection(x,connection,label):
    """Only verify supplied span-one coefficient; no recurrence discovery."""
    operations=0;width=0
    for j in range(1,len(x)):
        a,b=x[j];c,d=x[j-1];u,v=connection
        terms=(u*c,v*d,u*d,v*c)
        defect=(a+terms[0]-terms[1],b+terms[2]+terms[3])
        # Four real products, four real additions/subtractions, two comparisons.
        operations+=10
        for z in (*terms,*defect):
            width=max(width,backend.bitwidth(z))
        if defect != (0,0):
            return backend.FailureCharge(label,operations,width,
                      f'{operations} * A({width})',f'rejected at tail index {j}'),j
    raise AssertionError('test adapter unexpectedly valid')


def audit(receipt,x,epsilon,invoices):
    assert receipt['failed_work']==[backend.asdict(i) for i in invoices]
    assert receipt['failed_scalar_operations']==sum(i.scalar_operations for i in invoices)
    assert receipt['failed_bit_cost_sum']==[i.bit_cost_expression for i in invoices]
    if receipt['branch']!='bluestein_radix2':
        assert receipt['absolute_error_bound']==0 and receipt['root_count']==0
        return
    N=len(x);L=1
    while L<2*N-1:L*=2
    ell=L.bit_length()-1;S=sum(abs(a)+abs(b) for a,b in x)
    C=2*L*(2*ell+3);D=(S+1)*((L+1)*C+C*C)+1
    K=4*D+4*(ell+1)*(S*L+1)+S+3
    assert receipt['L']==L and receipt['ell']==ell
    assert (receipt['C'],receipt['D'],receipt['K'])==(C,D,K)
    h=F(1,1 << receipt['p'])
    assert h<=F(1,L) and K*h<=epsilon
    assert receipt['absolute_error_bound']==K*h
    assert receipt['root_count']==N+L//2
    assert receipt['root_error_bound']<=h
    counts=receipt['meter']['counts']
    assert counts['fft:transform']==3
    assert counts['fft:complex_multiply_round']==3*(L//2)*ell
    assert counts['pointwise:complex_multiply_round']==L
    assert counts['chirp_input:complex_multiply_round']==N
    assert counts['chirp_output:complex_multiply_round']==N
    assert counts['normalization:complex_divide_round']==N
    assert counts['roots:radius_verification']==N+L//2


def mutated_backend(old,new):
    source=(HERE/'certified_fft.py').read_text()
    assert old in source
    changed=source.replace(old,new)
    module=types.ModuleType('fresh_mutant')
    # Dataclasses needs a registered namespace. Only this newly authored code runs.
    import sys
    sys.modules[module.__name__]=module
    exec(compile(changed,'fresh_mutant.py','exec'),module.__dict__)
    return module,hashlib.sha256(changed.encode()).hexdigest()


def main():
    start=time.perf_counter();rng=random.Random(64064)
    cases=[]
    def add(name,x,epsilon=F(1,10**12),invoices=()):
        cases.append((name,[(F(a),F(b)) for a,b in x],epsilon,invoices))
    add('N1_exact_extreme',[(F(2**200,1),F(-1,2**250))],F(1,2**80))
    for N in (2,3,4,5,7,8,9,11,12,15,16,17,19,23,25,27,31,32,33,37,45,64,65):
        x=[(F(rng.randint(-7,7),2**rng.randrange(0,9)),
            F(rng.randint(-7,7),2**rng.randrange(0,9))) for _ in range(N)]
        add(f'random_complex_N{N}',x)
    for N in (1,3,8,17):add(f'zero_N{N}',[(0,0)]*N)
    add('positive_sign_N4',[(0,0),(1,0),(0,0),(0,0)])
    add('unnormalized_constant_N7',[(1,0)]*7)
    add('alternating_N16',[(1 if j%2==0 else -1,0) for j in range(16)])
    add('dynamic_range_N7',[(2**120,F(1,2**150)),(-2**120,F(-1,2**150)),
                         (F(1,2**120),2**90),(1,-2**90),(0,0),(3,-2),(-7,5)],F(1,2**80))
    add('dynamic_range_N9',[(2**256,0),(F(1,2**280),-2**256)]+[(j,-j) for j in range(7)],F(1,2**100))
    late=[(F(1),F(0))]*16+[(F(2),F(0))]
    early,j0=invoice_for_adapter_rejection(late,(F(0),F(0)),'first rejected adapter')
    final,j1=invoice_for_adapter_rejection(late,(F(-1),F(0)),'late rejected adapter')
    assert j0==1 and j1==16
    add('late_rejection_all_prefix_charges_N17',late,F(1,10**15),(early,final))
    results=[];vectors=[];bins=0
    for name,x,epsilon,invoices in cases:
        y,receipt=backend.certified_dft(x,epsilon,failed_work=invoices,cap=0)
        audit(receipt,x,epsilon,invoices)
        assert all(v.denominator & (v.denominator-1)==0 for z in y for v in z)
        boxes,oracle=enclose_dft(x,epsilon)
        assert certifies(y,boxes,epsilon),name
        bins+=len(x)
        results.append({'name':name,'N':len(x),'L':receipt['L'],'p':receipt['p'],
                        'certified':True,'branch':receipt['branch']})
        vectors.append({'name':name,'x':x,'epsilon':epsilon,'y':y,'enclosures':boxes,
                        'oracle':oracle,'receipt':receipt})
        print('PASS',name,'N',len(x),'p',receipt['p'],flush=True)
    # Sign, normalization and exactly representable output sentinels.
    exact4=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
    y,_=backend.certified_dft([(0,0),(1,0),(0,0),(0,0)],F(1,10**12))
    assert y==exact4
    negatives=[]
    x=[(F(j+1),F((j*j)%5-2)) for j in range(7)];eps=F(1,10**9)
    boxes,_=enclose_dft(x,eps)
    mutations=[
      ('chirp_sign','roots.root(j*j,2*N)','roots.root(-j*j,2*N)'),
      ('chirp_square','roots.root(j*j,2*N)','roots.root(j,2*N)'),
      ('inverse_sign','inv=radix2(PP,twiddles,-1,p,meter)','inv=radix2(PP,twiddles,1,p,meter)'),
      ('inverse_normalization','round_ratio(inv[k][0],16*L),round_ratio(inv[k][1],16*L)',
                                'round_ratio(inv[k][0],16),round_ratio(inv[k][1],16)'),
      ('insufficient_padding','while L < 2*N-1: L <<= 1','while L < N: L <<= 1'),
      ('twiddle_stride','root = roots[j*stride]','root = roots[j]')]
    for label,old,new in mutations:
        mutant,sha=mutated_backend(old,new)
        y,r=mutant.certified_dft(x,eps)
        assert not certifies(y,boxes,eps),label
        negatives.append({'mutation':label,'source_sha256':sha,'detected_by':'independent exact enclosure'})
    # Ledger/precision mutations must also be detected independently.
    y,r=backend.certified_dft(late,F(1,10**15),failed_work=(early,final))
    for label,change in [
        ('drop_failed_prefix',{'failed_work':r['failed_work'][1:]}),
        ('free_root_preparation',{'root_count':0}),
        ('undercharge_fft',{'meter':{**r['meter'],'counts':{**r['meter']['counts'],'fft:complex_multiply_round':0}}}),
        ('false_precision',{'p':0}),
        ('false_error_bound',{'absolute_error_bound':F(0)})]:
        try:audit({**r,**change},late,F(1,10**15),(early,final))
        except AssertionError:pass
        else:raise AssertionError(label)
        negatives.append({'mutation':label,'detected_by':'independent receipt audit'})
    invalids=[([],F(1,10),None),([(F(1,3),0)],F(1,10),None),
              ([(1.0,0)],F(1,10),None), ([(1,0)],F(0),None),
              ([(1,0)],F(-1),None), ([(1,0)],F(2),None),
              ([(1,0)],0.1,None), ([(1,0)],F(1,10),1),
              ([(1,0)],F(1,10),-1), ([(1,0)],F(1,10),False)]
    for x,eps,cap in invalids:
        try:backend.certified_dft(x,eps,cap=cap)
        except ValueError:pass
        else:raise AssertionError('invalid domain admitted')
    # Regression for the independently found shape-validation defect: frozen
    # dataclasses alone do not prevent a mutable object in an unchecked field.
    malformed_details=[[],{},None,17]
    for detail in malformed_details:
        charge=backend.FailureCharge('malformed detail',1,1,'A(1)',detail)
        try:backend.certified_dft([(1,0)],F(1,10),failed_work=(charge,))
        except ValueError:pass
        else:raise AssertionError('non-string invoice detail admitted')
    # r is independent of N and encoded counters can have arbitrary width.
    # These are explicitly synthetic interface records, not claimed execution.
    wide_invoices=tuple(backend.FailureCharge(
        f'synthetic encoded invoice {j}',(1<<4096)+j,(1<<2048)+j,
        'symbolic prior work (encoding test only)',
        'synthetic interface control; not executed work') for j in range(129))
    _,wide_receipt=backend.certified_dft([(1,0)],F(1,10),failed_work=wide_invoices)
    audit(wide_receipt,[(F(1),F(0))],F(1,10),wide_invoices)
    assert wide_receipt['failed_scalar_operations']==129*(1<<4096)+128*129//2
    summary={'owner':'ALG-064','status':'author regression passed; independent review required',
             'case_count':len(cases),'certified_bins':bins,'cases':results,
             'negative_controls':negatives,'invalid_domain_controls':len(invalids),
             'malformed_invoice_detail_controls':len(malformed_details),
             'wide_invoice_control':{'N':1,'records':len(wide_invoices),
                 'max_counter_bits':4097,'max_width_field_bits':2049,
                 'meaning':'synthetic encoding preservation, not executed prior work'},
             'max_p':max(v['receipt']['p'] for v in vectors),
             'max_N':max(len(v['x']) for v in vectors),
             'runtime_seconds_observation_only':time.perf_counter()-start,
             'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in [HERE/'certified_fft.py',HERE/'independent_oracle.py',HERE/'checks.py']}}
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(encode(summary),indent=2)+'\n')
    (HERE/'OUTPUT_VECTORS.json').write_text(json.dumps(encode(vectors),indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
