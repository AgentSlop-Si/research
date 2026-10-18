"""Independent reviewer controls, written after inspecting candidate source.
Uses pi = 6 asin(1/2) with a positive rational series and geometric tail.
Imports only the frozen candidate backend, never either candidate checker/oracle.
"""
import sys, hashlib, json, random, time, types, importlib.util
from pathlib import Path
from fractions import Fraction as F
sys.dont_write_bytecode = True
CAND = (Path(__file__).resolve().parent.parent / 'candidate')
HERE = Path(__file__).resolve().parent
source_at_start=(CAND/'certified_fft.py').read_bytes()
backend=types.ModuleType('reviewed_candidate');sys.modules[backend.__name__]=backend
exec(compile(source_at_start,str(CAND/'certified_fft.py'),'exec'),backend.__dict__)
manifest_at_start=(CAND/'MANIFEST.json').read_bytes()
for item in json.loads(manifest_at_start)['files']:
    raw=(CAND/item['path']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']

def dec(z):
    if isinstance(z,dict) and set(z)=={'n','d'}: return F(int(z['n']),int(z['d']))
    if isinstance(z,dict):return {k:dec(v) for k,v in z.items()}
    if isinstance(z,list):return [dec(v) for v in z]
    return z

def enc(z):
    if isinstance(z,F):return {'n':str(z.numerator),'d':str(z.denominator)}
    if isinstance(z,dict):return {k:enc(v) for k,v in z.items()}
    if isinstance(z,(tuple,list)):return [enc(v) for v in z]
    return z

def independent_pi(q):
    # asin(1/2) = sum_n binom(2n,n)/(2^(4n+1)(2n+1)).
    # Consecutive ratios are (2n+1)^2/[8(n+1)(2n+3)] < 1/4.
    term=F(1,2);partial=F(0);n=0;goal=F(1,1<<(q+12))
    while True:
        partial += term
        following=term*F((2*n+1)**2,8*(n+1)*(2*n+3))
        tail=8*following # six times 4/3; upper bound for remaining pi series
        if tail <= goal:break
        term=following;n+=1
    lo=6*partial;hi=lo+tail
    return (lo+hi)/2,(hi-lo)/2

def independent_roots(N,q):
    pi,pe=independent_pi(q)
    goal=F(1,1<<(q+8));degree=0;remainder=F(4)
    while remainder>goal:
        degree+=1;remainder*=F(4,degree+1)
    roots=[]
    for r in range(N):
        c=r if 2*r<=N else r-N
        angle=F(2*c,N)*pi
        assert abs(angle)<4
        real=F(0);imag=F(0);power=F(1)
        for j in range(degree+1):
            if j:power*=angle/F(j)
            if j%2:imag += (-1)**((j-1)//2)*power
            else:real += (-1)**(j//2)*power
        roots.append((real,imag,pe+remainder))
    return roots

def enclosures(x,eps):
    S=sum(abs(F(v)) for z in x for v in z);q=0
    while (S+1)*F(1,1<<q)>eps/128:q+=1
    roots=independent_roots(len(x),q);boxes=[]
    for k in range(len(x)):
        re=F(0);im=F(0);err=F(0)
        for j,(a,b) in enumerate(x):
            c,s,e=roots[(j*k)%len(x)]
            re += a*c-b*s;im += a*s+b*c;err+=(abs(a)+abs(b))*e
        # Keep exact intervals without outward compression, independently of candidate.
        boxes.append(((re-err,re+err),(im-err,im+err)))
    return boxes

def passed(y,boxes,eps):
    return len(y)==len(boxes) and all(sum(max(abs(v-l),abs(v-u))**2 for v,(l,u) in zip(z,b)) <= eps*eps for z,b in zip(y,boxes))

def audit(x,eps,r,invoices):
    assert r['failed_work']==[backend.asdict(c) for c in invoices]
    assert r['failed_scalar_operations']==sum(c.scalar_operations for c in invoices)
    assert r['failed_bit_cost_sum']==[c.bit_cost_expression for c in invoices]
    N=len(x);b=max(F(v).denominator.bit_length()-1 for z in x for v in z)
    if N==1 or not any(v for z in x for v in z):
        assert r['absolute_error_bound']==0 and r['root_count']==0;return
    L=1<<(2*N-2).bit_length();ell=L.bit_length()-1
    S=sum(abs(v) for z in x for v in z)
    C=2*L*(2*ell+3);D=(S+1)*((L+1)*C+C*C)+1;K=4*D+4*(ell+1)*(S*L+1)+S+3
    p=max(b,ell)
    while K>eps*(1<<p):p+=1
    assert r['p']==p and r['L']==L and r['ell']==ell
    assert (r['S'],r['C'],r['D'],r['K'])==(S,C,D,K)
    assert r['absolute_error_bound']==K/(1<<p)<=eps
    assert 0<r['root_error_bound']<=F(1,1<<p)
    assert r['root_count']==N+L//2
    ct=r['meter']['counts'];assert ct['fft:transform']==3
    assert ct['fft:complex_multiply_round']==3*L*ell//2
    assert ct['fft:butterfly_add_subtract']==3*L*ell//2
    assert ct['pointwise:complex_multiply_round']==L
    assert ct['roots:radius_verification']==N+L//2
    assert ct['roots:taylor_term']==(N+L//2)*(r['root_taylor_degree']+1)
    assert ct['chirp_input:complex_multiply_round']==N
    assert ct['chirp_output:complex_multiply_round']==N
    assert ct['normalization:complex_divide_round']==N

start=time.perf_counter();results={'saved':[],'fresh':[],'negative_controls':[],'interface_controls':[]}
saved=dec(json.loads((CAND/'OUTPUT_VECTORS.json').read_text()))
for case in saved:
    boxes=enclosures(case['x'],case['epsilon'])
    assert passed(case['y'],boxes,case['epsilon']),case['name']
    charges=[backend.FailureCharge(**r) for r in case['receipt']['failed_work']]
    audit(case['x'],case['epsilon'],case['receipt'],charges)
    # Recompute outputs and receipts from inspected frozen backend source.
    y,r=backend.certified_dft(case['x'],case['epsilon'],charges,case['receipt']['cap'])
    assert y==[tuple(z) for z in case['y']]
    assert enc(r)==enc(case['receipt'])
    results['saved'].append({'name':case['name'],'bins':len(y),'independent_enclosure':True,'source_reproduction':True,'receipt':True})
    print('SAVED PASS',case['name'],flush=True)

rng=random.Random(992064)
fresh=[]
for N in (6,10,13,18,29,49,63,66,67,127,129):
    x=[(F(rng.randint(-40,40),1<<rng.randrange(11)),F(rng.randint(-40,40),1<<rng.randrange(11))) for _ in range(N)]
    fresh.append((f'unseen_length_{N}',x,F(1,1000000)))
fresh.extend([
 ('epsilon_long_near_one',[(F(1),F(0)),(F(-3,8),F(1,4)),(F(2),F(5))],F((1<<4096)-1,1<<4096)),
 ('epsilon_long_general',[(F(3),F(-1)),(F(1,32),F(7))],F((1<<2048)+3,3*(1<<2048)+7)),
 ('b_dominates',[(F(1,1<<650),F(-1,1<<650)),(F(0),F(0)),(F(1,1<<649),F(0))],F(1)),
 ('small_epsilon',[(F(1,4),F(3,8)),(F(-1,2),F(0)),(F(1,16),F(-2,3*0+8))],F(1,1<<500)),
 ('complex_large_cancel',[(F(1<<500),F(-(1<<490))),(F(-(1<<500)),F(1<<490)),(F(1,1<<300),F(1))],F(1,1<<150))])
for name,x,eps in fresh:
    y,r=backend.certified_dft(x,eps)
    audit(x,eps,r,[])
    assert passed(y,enclosures(x,eps),eps),name
    results['fresh'].append({'name':name,'N':len(x),'p':r['p'],'L':r['L'],'passed':True})
    print('FRESH PASS',name,flush=True)

# Independently authored rounding and root controls at extreme/small p.
for denominator in range(1,39):
    for numerator in range(-100,101):
        z=backend.round_ratio(numerator,denominator);err=abs(F(numerator,denominator)-z)
        assert err<=F(1,2)
        if err==F(1,2):assert z>F(numerator,denominator)
results['rounding_controls']=38*201
for p in (0,1,2,7,31,101):
    factory=backend.RootFactory(p,backend.Meter())
    for m in (1,2,3,5,8,17,33):
        target=independent_roots(m,p+12)
        for k in range(m):
            z=factory.root(k,m);zr=F(z[0],factory.scale);zi=F(z[1],factory.scale)
            cr,ci,e=target[k]
            assert abs(zr-cr)+abs(zi-ci)+2*e<=factory.h
    assert factory.max_radius<factory.h
results['root_controls']=6*sum((1,2,3,5,8,17,33))

# New source perturbations, not candidate-authored six mutation strings.
source=source_at_start.decode()
mutations=[
 ('chirp_residue_mod_N','chirps=[roots.root(j*j,2*N) for j in range(N)]','chirps=[roots.root(j*j,N) for j in range(N)]'),
 ('conjugate_only_mirrored_arm','if j: bb[L-j]=r','if j: bb[L-j]=(r[0],-r[1])'),
 ('wrong_final_chirp','val=cmul(conv,chirps[k],16*Q,meter,\'chirp_output\')','val=cmul(conv,(chirps[k][0],-chirps[k][1]),16*Q,meter,\'chirp_output\')'),
 ('off_by_16_normalization','conv=(round_ratio(inv[k][0],16*L),round_ratio(inv[k][1],16*L))','conv=(round_ratio(inv[k][0],L),round_ratio(inv[k][1],L))'),
 ('lost_grid_embedding','a=[(16*z[0],16*z[1]) for z in a]','a=[(z[0],z[1]) for z in a]')]
x=[(F(j*j-3*j+1,8),F(2*j-5,4)) for j in range(9)];eps=F(1,1000000);boxes=enclosures(x,eps)
for label,old,new in mutations:
    assert source.count(old)==1
    mutant=source.replace(old,new);module=types.ModuleType('review_mutant_'+label);sys.modules[module.__name__]=module
    exec(compile(mutant,module.__name__+'.py','exec'),module.__dict__)
    y,r=module.certified_dft(x,eps)
    assert not passed(y,boxes,eps),label
    results['negative_controls'].append({'name':label,'detected':True,'mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest()})

# Failure charges include zero, huge integer amounts, repeated labels, ordered terms.
charges=(backend.FailureCharge('same',0,0,'zero','done'),backend.FailureCharge('same',1<<4096,1<<1024,'explicit prior bit bound','late rejection'),backend.FailureCharge('last',17,123,'17*A(123)',''))
y,r=backend.certified_dft(x,eps,charges,cap=8);audit(x,eps,r,charges)
assert r['failed_scalar_operations']==(1<<4096)+17
results['invoice_order_and_large_encoding']=True

bad_calls=[([],F(1),None),([(True,0)],F(1),None),([(1,0)],True,None),([(F(1,3),0)],F(1),None),([(1,0)],F(1),True),([(1,0)],F(1),1),([(1,0)],F(1),-1)]
for xx,e,cap in bad_calls:
    try:backend.certified_dft(xx,e,cap=cap)
    except ValueError:results['interface_controls'].append('rejected')
    else:raise AssertionError('malformed input accepted')
invalid_charges=[backend.FailureCharge('',1,1,'A(1)'),backend.FailureCharge('a',True,1,'A(1)'),backend.FailureCharge('a',1,-1,'A(1)'),backend.FailureCharge('a',1,1,''),{'label':'not a record'}]
for c in invalid_charges:
    try:backend.certified_dft([(1,0)],F(1),[c])
    except ValueError:results['interface_controls'].append('rejected')
    else:raise AssertionError('bad invoice accepted')
# Final validation of the reviewer-requested detail correction.
for malformed in ([],{},None,17,True):
    c=backend.FailureCharge('bad detail',1,1,'A(1)',detail=malformed)
    try:backend.certified_dft([(1,0)],F(1),[c])
    except ValueError:results['interface_controls'].append('malformed_detail_rejected')
    else:raise AssertionError('non-string detail admitted')
results['detail_validation_corrected']=True
# Arbitrarily many invoice records are independent of N.
many=[backend.FailureCharge('prior',1<<2048,2050,'A(2050)','finished')]+[backend.FailureCharge('prior',1,1,'A(1)','') for _ in range(4096)]
y,r=backend.certified_dft([(1,0)],F(1),many)
audit([(1,0)],F(1),r,many)
assert r['failed_scalar_operations']==(1<<2048)+4096
results['many_invoice_records']={'N':1,'records':len(many),'largest_counter_bits':2049,'passed':True}
# Independently authored receipt falsification controls.
y,r=backend.certified_dft(x,eps,charges)
receipt_mutants=[('drop_invoice',{'failed_work':r['failed_work'][1:]}),('wrong_total',{'failed_scalar_operations':0}),('drop_bit_term',{'failed_bit_cost_sum':[]}),('free_roots',{'root_count':0}),('zero_error_claim',{'absolute_error_bound':F(0)}),('nonminimal_precision',{'p':r['p']+1}),('missing_transform',{'meter':{**r['meter'],'counts':{**r['meter']['counts'],'fft:transform':2}}}),('missing_root_work',{'meter':{**r['meter'],'counts':{**r['meter']['counts'],'roots:taylor_term':0}}})]
for label,delta in receipt_mutants:
    try:audit(x,eps,{**r,**delta},charges)
    except AssertionError:results['negative_controls'].append({'name':label,'receipt_mutation':True,'detected':True})
    else:raise AssertionError('receipt mutation undetected: '+label)
assert (CAND/'certified_fft.py').read_bytes()==source_at_start
assert (CAND/'MANIFEST.json').read_bytes()==manifest_at_start
for item in json.loads(manifest_at_start)['files']:
    raw=(CAND/item['path']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
results.update(saved_cases=len(saved),saved_bins=sum(len(c['y']) for c in saved),fresh_cases=len(fresh),fresh_bins=sum(len(x) for _,x,_ in fresh),elapsed_seconds=time.perf_counter()-start,independent_oracle='pi=6*asin(1/2), positive rational central-binomial series and geometric tail; direct DFT exact rational interval enclosure',candidate_backend_sha256=hashlib.sha256(source_at_start).hexdigest(),candidate_manifest_sha256=hashlib.sha256(manifest_at_start).hexdigest(),candidate_files_unchanged_during_checks=True)
(HERE/'REVIEW_CHECK_RESULTS.json').write_text(json.dumps(enc(results),indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ('saved','fresh')},indent=2))
