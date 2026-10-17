"""Fresh independent verifier of the author's precise full-width cascade grammar.
No supplied/historical code is imported. Python integers are exactness oracles only.
"""
from pathlib import Path
import json,random
OUT=Path(__file__).resolve().parent

def cascade(x,m,d):
    assert x>=0 and m>=2 and d>=1
    B=1<<m;p=B-1
    n=max(1,x.bit_length());K=(n+m-1)//m
    states=[0]*d;q=0;prefix=0
    for k in range(K-1,-1,-1):
        a=(x>>(k*m))&(B-1)
        prefix=prefix*B+a
        for stage in range(d):
            old=states[stage]
            total=old+a
            correction=int(total>=p)
            a=old+correction
            states[stage]=total-correction*p
            assert 0<=a<B and 0<=states[stage]<p
        q=q*B+a
        residual=0
        for r in states[::-1]: residual=(residual<<m)-residual+r
        assert prefix==q*p**d+residual
    rem=0;assembly=0
    for r in states[::-1]:
        assembly+=max(1,rem.bit_length())+m
        rem=(rem<<m)-rem+r
    return q,rem,d*K*m,assembly

def convert(x,m,d):
    if x==0:return [0],0,0
    digits=[];volume=0;assembly=0
    while x:
        x,r,v,a=cascade(x,m,d)
        digits.append(r);volume+=v;assembly+=a
    return digits,volume,assembly

def recover(digits,m,d):
    x=0;work=0
    for r in reversed(digits):
        for _ in range(d):
            work+=max(1,x.bit_length())+m
            x=(x<<m)-x
        work+=max(1,x.bit_length(),r.bit_length())
        x+=r
    return x,work

def native(x,Q):
    if x==0:return [0]
    ds=[]
    while x:x,r=divmod(x,Q);ds.append(r)
    return ds

stats={'exact_cascade_checks':0,'exact_full_conversion_checks':0,
       'moderate_group_cost_cases':0,'seed':202610170014,'worst_case_cost_rows':[]}
for m in range(2,8):
    for d in range(1,9):
        Q=((1<<m)-1)**d
        for x in range(1024):
            q,r,_,_=cascade(x,m,d)
            assert (q,r)==divmod(x,Q)
            stats['exact_cascade_checks']+=1
rng=random.Random(stats['seed'])
for m in [2,3,4,5,7,8,13,31,64]:
    for d in [1,2,3,7,13,32]:
        p=(1<<m)-1;Q=p**d
        xs={0,1,Q-1,Q,Q+1,Q*Q-1,Q*Q,Q*Q+1}
        for bits in [1,7,32,127,256]:xs.add(rng.getrandbits(bits))
        for x in sorted(xs):
            q,r,_,_=cascade(x,m,d)
            assert (q,r)==divmod(x,Q)
            ds,volume,assembly=convert(x,m,d)
            assert ds==native(x,Q)
            assert recover(ds,m,d)[0]==x
            stats['exact_cascade_checks']+=1
            stats['exact_full_conversion_checks']+=1
ratios=[]
for N in [8,9,15,16,17,31,32,33,63,64,65,127,128,129,256,512,1024]:
    for m in sorted(set([2,3,4,7,max(2,N//16),max(2,N//8),max(2,N//4)])):
        for d in sorted(set([1,2,3,max(1,N//(8*m)),max(1,N//(4*m))])):
            if d*m>N/4:continue
            x=(1<<N)-1
            digits,volume,assembly=convert(x,m,d)
            y,reconstruction=recover(digits,m,d)
            assert y==x
            scale=N*N/m
            assert 0.125<=volume/scale<=8
            assert assembly<=16*scale and reconstruction<=16*scale
            ratios.append(volume/scale)
            stats['moderate_group_cost_cases']+=1
            stats['worst_case_cost_rows'].append({'N':N,'m':m,'d':d,'J':len(digits),
              'transition_volume':volume,'ratio_to_N2_over_m':volume/scale,
              'assembly_width_sum':assembly,'reconstruction_width_sum':reconstruction})
stats['min_moderate_volume_ratio']=min(ratios)
stats['max_moderate_volume_ratio']=max(ratios)
stats['result']='PASS'
(OUT/'CASCADE_RESULTS.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps({k:v for k,v in stats.items() if k!='worst_case_cost_rows'},indent=2))
