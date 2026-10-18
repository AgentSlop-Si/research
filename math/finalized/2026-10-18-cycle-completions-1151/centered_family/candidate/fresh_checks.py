"""Fresh independent algebraic/direct-sum checks, plus whole-source production.
No historical program is imported. The oracle does not call production trig.
"""
import json
from dataclasses import asdict,replace
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import centered_source as p

HERE=Path(__file__).resolve().parent


def cyclo_sum(M,exponents):
    result=[0]*(M//2)
    for e in exponents:
        e%=M
        result[e%(M//2)] += 1 if e<M//2 else -1
    return tuple(result)


def exact_controls():
    rows=[];inverse_rows=0
    for m in range(3,10):
        M=1<<m;N=M//4;center=(N-1)//2
        spectra=[cyclo_sum(M,((j-center)*k for j in range(N))) for k in range(M)]
        support=[k for k,v in enumerate(spectra) if any(v)]
        assert support==[k for k in range(M) if k==0 or k%4]
        assert len(support)==M-N+1
        if m<=5:
            for ell in range(M):
                result=[0]*(M//2)
                for k,poly in enumerate(spectra):
                    for exponent,value in enumerate(poly):
                        e=(exponent-ell*k)%M
                        result[e%(M//2)]+=value*(1 if e<M//2 else -1)
                expected=[0]*(M//2)
                if ell in {(j-center)%M for j in range(N)}:expected[0]=M
                assert result==expected
                inverse_rows+=1
        rows.append({'m':m,'N':N,'exact_spectrum_support':len(support),'lower_bound_attained':True})
    return rows,inverse_rows


def plus(a,b):return a[0]+b[0],a[1]+b[1]
def times(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def scale(a,c):return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def grid(x,q):return F(x.numerator*(1<<q)//x.denominator,1<<q)


def oracle_pi(q):
    # pi/4=atan(1/2)+atan(1/3), independently of production Machin formula.
    def atan(d):
        n=q+8
        v=sum((F((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(n)),F(0))
        w=v+F((-1)**n,(2*n+1)*d**(2*n+1))
        return min(v,w),max(v,w)
    out=scale(plus(atan(2),atan(3)),4)
    return grid(out[0],q),-grid(-out[1],q)


def oracle_root(index,M,q,pi):
    r=index%M
    if r>M//2:r-=M
    lo,hi=scale(pi,F(2*r,M));x=(lo+hi)/2;angle=(hi-lo)/2
    terms=q//2+20;xx=x*x
    def horner(parity):
        value=F(0)
        for j in reversed(range(terms)):
            value=value*xx+F((-1)**j,factorial(2*j+parity))
        if parity:value*=x
        # Complete even/odd polynomial is covered by the full exponential tail.
        degree=2*terms-2
        error=F(4**(degree+1),factorial(degree+1))+angle
        return value-error,value+error
    return horner(0),scale(horner(1),-1)


def oracle_rsqrt(M,q):
    # Independent integer bisection, rather than production isqrt.
    lo,hi=0,1<<q
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid*mid*M<=1<<(2*q):lo=mid
        else:hi=mid
    return F(lo,1<<q),F(lo if lo*lo*M==1<<(2*q) else hi,1<<q)


def direct_oracle_controls():
    checked=0;details=[]
    for m in (3,4,5):
        M=1<<m;N=M//4;P=16*m+16;Q=P+2*m+16
        a,b=3,-1;E=N*(a*a+b*b);h=((E-1).bit_length()+1)//2
        src=p.Source(m,N,0,a,b,h,h,'constant')
        L=p.Ledger();pi=p.pi_interval(Q,L);root=p.reciprocal_root(M,Q,L)
        opi=oracle_pi(180);oroot=oracle_rsqrt(M,180)
        roots=[oracle_root(j,M,180,opi) for j in range(M)]
        for k in sorted(set((0,1,3,4,M-1,M-3,M//2))):
            signed=k if k<=M//2 else k-M
            val=p.coefficient(src,signed,P,pi,root,Q,L)
            real=(F(0),F(0));imag=(F(0),F(0))
            for j in range(N):
                rr,ii=roots[((j-(N-1)//2)*k)%M]
                real=plus(real,rr);imag=plus(imag,ii)
            # Multiply original c/2^h and unitary normalizer; direct finite sum.
            oracle_real=times(plus(scale(real,F(a,1<<h)),scale(imag,F(-b,1<<h))),oroot)
            oracle_imag=times(plus(scale(real,F(b,1<<h)),scale(imag,F(a,1<<h))),oroot)
            radii=[max(abs(F(z,1<<P)-lo),abs(F(z,1<<P)-hi)) for z,(lo,hi) in zip(val,(oracle_real,oracle_imag))]
            assert sum(x*x for x in radii)<=F(1,1<<(2*P))
            checked+=1
        details.append({'m':m,'direct_summation_coordinates':len(set((0,1,3,4,M-1,M-3,M//2)))})
    return checked,details


def structural_controls():
    plans=[]
    for m in (11,12,16,28,64,128,1024):
        M=1<<m;N=M//4;K=1<<((m+3)//4);S=1+2*(K-K//4);P=16*m+16
        assert K**4>=M and K<M//2 and 160*m+4<M
        # rho<=R M^-1/4 for every R>1/2, by fourth powers.
        assert (1<<(4*(P-1)))>=M
        assert S==1+3*K//2
        plans.append({'m':m,'support_count':str(S),'exact_support_count':str(3*N+1),'all_guards':True})
    return plans


def main():
    exact,inv=exact_controls()
    count,direct=direct_oracle_controls()
    inputs=[{'m':11,'F':0,'kind':'constant','data':(1,0)},
            {'m':12,'F':3,'kind':'constant','data':(3,-1)}]
    runs=[];answers=[]
    for obj in inputs:
        answer,receipt=p.produce(obj);answers.append(answer)
        assert len(answer.pairs)==1+3*answer.cutoff//2
        assert answer.exact_support_size==3*answer.source.N+1
        assert all(k==0 or k%4 for k,_ in answer.pairs)
        assert answer.pairs[0][0]==0 and any(answer.pairs[0][1])
        runs.append({'input':obj,'answer':asdict(answer),'receipt':receipt})
    # Full fresh replay, including recognition of every coordinate of a dense original.
    dense={'m':11,'F':0,'kind':'dense','data':[(1,0)]*512}
    dense_answer=replace(answers[0],source=replace(answers[0].source,input_kind='dense'))
    ok,replay_receipts=p.replay(dense,dense_answer)
    assert ok and replay_receipts['replay_production']['events']['dense_coordinate_visits']==512
    rejection_inputs=[{'m':11,'F':0,'kind':'dense','data':[(1,0)]*511+[(1,1)]},
        {'m':11,'F':0,'kind':'constant','data':(2,0)},
        {'m':11,'F':10000,'kind':'constant','data':(1,0)},
        {'m':10,'F':0,'kind':'constant','data':(1,0)},
        {'m':11,'F':0,'kind':'constant','data':(True,0)},
        {'m':11,'F':0,'kind':'constant','data':(0,0)},
        {'m':11,'F':0,'kind':'constant','data':(1<<2000,1)}]
    rejections=[]
    for obj in rejection_inputs:
        try:p.produce(obj)
        except p.Rejected as error:
            assert hasattr(error,'receipt')
            rejections.append({'reason':str(error),'receipt':error.receipt})
        else:raise AssertionError('rejection missing')
    # Recognition controls demonstrate original binding without pretending to replay coefficients.
    L=p.Ledger();src=p.recognize(inputs[0],L)
    changed=p.recognize({'m':11,'F':0,'kind':'constant','data':(1,1)},p.Ledger())
    assert src!=changed
    result={'status':'PASS','exact_cyclotomic_support':exact,'exact_inverse_coordinates':inv,
        'independent_direct_sum_coordinates':count,'direct_sum_controls':direct,
        'structural_plans':structural_controls(),'complete_production_runs':runs,
        'full_dense_source_replay':replay_receipts,'rejections':rejections,
        'full_frontend_runs_in_final_batch':3,'final_batch_frontend_coefficients':sum(len(a.pairs) for a in answers)+len(dense_answer.pairs),
        'historical_programs_executed':False,'full_outer_executed':False,'external_writes':False}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'EXAMPLE_MEDIAN_INPUT.json').write_text(json.dumps({'M':2048,'P':answers[0].bits,
        'candidates':[k for k,v in answers[0].pairs],
        'rows':[[v for k,v in answers[0].pairs]],'source':asdict(answers[0].source)},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','exact_inverse_coordinates','independent_direct_sum_coordinates','full_frontend_runs_in_final_batch','final_batch_frontend_coefficients','historical_programs_executed','full_outer_executed')},indent=2))


if __name__=='__main__':main()
