#!/usr/bin/env python3
"""Fresh exact controls only. No historical module imports or executions.
These are arithmetic controls, not timing evidence or asymptotic proofs.
"""
import json, math, pathlib, hashlib
from functools import lru_cache
HERE=pathlib.Path(__file__).resolve().parent

def primes(r):
    return [p for p in range(2,r+1) if all(p%d for d in range(2,math.isqrt(p)+1))]

def native(r):
    ell=math.lcm(*range(1,r+1)); d=ell//r
    residue,modulus=0,1
    for p in primes(r):
        pp=1
        while ell%(pp*p)==0: pp*=p
        q=1
        while d%(q*p)==0: q*=p
        if q==1: continue
        target=(-pow(ell//pp,-1,q))%q
        residue+=modulus*((target-residue)*pow(modulus,-1,q)%q)
        modulus*=q
    assert modulus==d
    k=residue if d>1 else 1
    assert 1<=k<=max(1,d-1)
    P=1+k*ell; R=[1+(P-1)//j for j in range(1,r+1)]
    weights=[1]
    for z in R: weights.append(weights[-1]*z)
    assert weights[-1]%d==0
    beta=weights[-1]//d; s=beta.bit_length()-1
    assert beta>weights[-2]
    return {'r':r,'P':P,'d':d,'radices':R,'weights':weights[:-1], 'beta':beta,'s':s}

@lru_cache(maxsize=None)
def choose(x,j):
    if x>=0: return math.comb(x,j) if j<=x else 0
    return (-1 if j%2 else 1)*math.comb(-x+j-1,j)

@lru_cache(maxsize=None)
def row_norm(r,x): return sum(abs(choose(x,j)) for j in range(r))

def offset(r):
    return min(range(r),key=lambda a:(max(row_norm(r,-a),row_norm(r,2*r-2-a)),a))

def eval_coeff(c,x): return sum((-1 if j%2 else 1)*v*choose(x,j) for j,v in enumerate(c) if v)

def witness(p):
    r,P,R,W=p['r'],p['P'],p['radices'],p['weights']
    cs=[[0]*r]
    for j in range(r-1):
        c=[0]*r;c[j]=(R[j]-1)//2;cs.append(c)
    c=[0]*r;c[0]=P-1;cs.append(c)
    bs=[sum(c[j]*W[j] for j in range(r)) for c in cs]
    assert all(0<=b<1<<p['s'] for b in bs)
    return cs,bs

def slot(A,B,L): return 8*max(1,((2*L*A*B).bit_length()+7)//8)

def pack(c,w): return sum(z<<(i*w) for i,z in enumerate(c))

def extract(z,w,m,bound):
    Q=1<<w; out=[]
    for _ in range(m):
        q=z%Q
        if 2*q>=Q:q-=Q
        assert abs(q)<=bound
        out.append(q);z=(z-q)//Q
    assert z==0
    return out

def interp(values,target,start):
    diffs=list(values); ans=0
    for j in range(len(values)):
        ans+=diffs[0]*choose(target-start,j)
        diffs=[b-a for a,b in zip(diffs,diffs[1:])]
    return ans

def main():
    result={'scope':'Fresh independent exact arithmetic, no historical program execution.', 'shift_checks':[], 'complete_checks':[], 'asymptotic_cap_checks':[]}
    for r in range(2,65):
        products=[];maxima=[]
        for a in range(r):
            norms=[row_norm(r,x) for x in range(-a,2*r-1-a)]
            products.append(math.prod(norms));maxima.append(max(norms))
            if a+1<r:
                # Exact telescoping identity for total logarithmic height.
                nextprod=math.prod(row_norm(r,x) for x in range(-a-1,2*r-2-a))
                assert nextprod*row_norm(r,2*r-2-a)==products[-1]*row_norm(r,-a-1)
        crossing=next(a for a in range(r) if row_norm(r,-a)>=row_norm(r,2*r-2-a))
        candidates={max(0,crossing-1),crossing}
        sumarg={a for a,z in enumerate(products) if z==min(products)}
        maxarg={a for a,z in enumerate(maxima) if z==min(maxima)}
        assert sumarg<=candidates and maxarg<=candidates
        result['shift_checks'].append({'rank':r,'sum_minimizers':sorted(sumarg),'max_minimizers':sorted(maxarg),'crossing':crossing})
    for r in range(3,11):
        p=native(r);a=offset(r);cs,bs=witness(p);ds=[cs[0],*reversed(cs[1:-1]),cs[-1]];ts=[sum(c[j]*p['weights'][j] for j in range(r)) for c in ds]
        L=len(cs); nodes=list(range(-a,2*r-1-a)); raw=[];info=[]
        for x in nodes:
            ar=[eval_coeff(c,x) for c in cs];br=[eval_coeff(c,x) for c in ds]
            A=max(map(abs,ar));B=max(map(abs,br));norm=row_norm(r,x)
            # Exact safe polynomial saturation bound (P sufficiently large).
            assert 12*r*r*A >= (p['P']-1)*norm
            assert A<= (p['P']-1)*norm
            w=slot(A,B,L);u=pack(ar,w);v=pack(br,w);bound=L*A*B
            assert u>0 and v>0
            assert ((p['P']-2)<<(w*(L-1)))<=u<=(p['P']<<(w*(L-1)))
            conv=extract(u*v,w,2*L-1,bound)
            oracle=[sum(ar[j]*br[t-j] for j in range(L) if 0<=t-j<L) for t in range(2*L-1)]
            assert conv==oracle;raw.append(conv)
            info.append({'node':x,'slot_bits':w,'allocated_bits':L*w,'actual_left_bits':u.bit_length(),'actual_right_bits':v.bit_length()})
        assert len({tuple(eval_coeff(c,x) for c in cs) for x in nodes})==len(nodes)
        output=[interp([row[t] for row in raw],-p['P'],-a) for t in range(2*L-1)]
        oracle=[sum(bs[j]*ts[t-j] for j in range(L) if 0<=t-j<L) for t in range(2*L-1)]
        assert output==oracle
        X=pack(bs,p['s']);Y=pack(ts,p['s']);Z=pack(output,p['s']);assert Z==X*Y
        result['complete_checks'].append({'rank':r,'offset':a,'blocks':L,'input_bits':[X.bit_length(),Y.bit_length()],'nodes':info,'product_sha256':hashlib.sha256(str(Z).encode()).hexdigest()})
    alpha=.5482418475607564
    J=(((1+alpha)**2*math.log(1+alpha)-alpha*alpha*math.log(alpha)-alpha)/2/math.log(2)+(2-alpha)**2/2)
    result['analytic_constants']={'alpha':alpha,'J':J,'volume_lower':4+(2+2*J)/4,'volume_upper':4+(2+2*J)}
    for r in [16,24,32,48,64,96,128,192,256]:
        p=native(r);a=offset(r);cs,bs=witness(p);L=(3*(1<<(r-1)))//p['s'];assert L>=r+1
        N=(L-1)*p['s']+(p['P']-1).bit_length();assert N.bit_length()-1==r
        caps=[];actual=[];theorysum=0.0
        for x in range(-a,2*r-1-a):
            R=row_norm(r,x);A=max(abs(eval_coeff(c,x)) for c in cs)
            assert (p['P']-1)*R <=12*r*r*A
            caps.append(slot((p['P']-1)*R,(p['P']-1)*R,L));actual.append(slot(A,A,L))
            theorysum+=math.log2(R)
        kappa=math.log2(p['P'])/r
        result['asymptotic_cap_checks'].append({'rank':r,'offset':a,'point_bits':p['P'].bit_length(),'s':p['s'],'L':L,'N':N,'sum_row_log2_over_r2':theorysum/r**2,'J_limit':J,'kappa':kappa,'asymptotic_volume_formula':4+(2+2*J)/kappa,'padded_cap_volume':L*sum(caps)/N,'legal_witness_allocated_volume':L*sum(actual)/N,'legal_witness_actual_volume_lower':sum((L-1)*w+(p['P']-2).bit_length() for w in actual)/N,'largest_child_over_N':L*max(caps)/N})
    result['totals']={'exact_shift_ranks':len(result['shift_checks']),'complete_pipeline_products':len(result['complete_checks']),'node_convolutions':sum(len(z['nodes']) for z in result['complete_checks']),'large_metadata_ranks':len(result['asymptotic_cap_checks'])}
    (HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['totals'],indent=2));print(json.dumps(result['analytic_constants'],indent=2))
    for c in result['asymptotic_cap_checks']:
        print(c['rank'],round(c['legal_witness_actual_volume_lower'],6),round(c['padded_cap_volume'],6),round(c['asymptotic_volume_formula'],6),round(c['largest_child_over_N'],6))
if __name__=='__main__': main()
