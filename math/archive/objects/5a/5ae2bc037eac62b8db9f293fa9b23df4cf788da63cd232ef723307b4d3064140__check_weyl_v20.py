#!/usr/bin/env python3
"""Fresh packet, zero-minor, and Krylov checks; no uploaded modules imported."""
import itertools,json,random
from collections import deque
from pathlib import Path
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent

def field(n):
    k=2
    while not prime_by_trial_division(k*n+1):k+=1
    p=k*n+1
    for g in range(2,p):
        if len({pow(g,j,p) for j in range(1,p)})==p-1:return p,pow(g,k,p)
    raise AssertionError

def packet_controls():
    out=[];minors=[];zero=[];total=0
    for n in (3,5,7,11,13,17,19):
        p,w=field(n);f=Field(p);alpha=next(a for a in range(2,p) if pow(a,n,p)!=1);den=f.inv(1-pow(alpha,n,p))
        for h in (1,2):
            greens=[];weyls=[]
            for r in range(n):
                operator=[[0]*n for _ in range(n)]
                for j in range(n):operator[(j+h)%n][j]=pow(w,r*j,p)
                weyls.append(operator)
                a=[[(int(i==j)-alpha*operator[i][j])%p for j in range(n)] for i in range(n)]
                greens.append(f.inverse(a))
            left=f.mul(weyls[1],weyls[2]);right=f.mul(weyls[2],weyls[1]);phase=pow(w,-h,p)
            assert left==[[(phase*x)%p for x in row] for row in right]
            # The chirp similarity also establishes the same support-order guard.
            u=[t*(t-h)*pow(2*h,-1,n)%n for t in range(n)]
            for r,operator in enumerate(weyls):
                d=[pow(w,r*v,p) for v in u]
                assert all(operator[(j+h)%n][j]==d[(j+h)%n]*f.inv(d[j])%p for j in range(n))
            for s in range(n):
                literal=[[sum(pow(w,-r*s,p)*greens[r][i][j] for r in range(n))*f.inv(n)%p for j in range(n)] for i in range(n)]
                predicted=[[0]*n for _ in range(n)]
                if s==0:
                    for j in range(n):predicted[j][j]=den
                for m in range(1,n):
                    j=(s-h*m*(m-1)//2)*pow(m,-1,n)%n
                    predicted[(j+m*h)%n][j]=pow(alpha,m,p)*den%p
                assert literal==predicted
                nz=sum(bool(x) for row in literal for x in row);assert nz==(2*n-1 if s==0 else n-1)
                total+=1
            coeff=[(r*r+3*r+2)%p for r in range(n)]
            chat=[sum(c*pow(w,r*q,p) for r,c in enumerate(coeff))%p for q in range(n)]
            packet=[[sum(coeff[r]*greens[r][i][j] for r in range(n))%p for j in range(n)] for i in range(n)]
            expected=[[pow(alpha,((i-j)*pow(h,-1,n))%n,p)*den*chat[(u[i]-u[j])%n]%p for j in range(n)] for i in range(n)]
            assert packet==expected
            if n>=5:
                rr=[0,h];cc=[(2*h)%n,(-h)%n]
                det=f.det([[packet[i][j] for j in cc] for i in rr]);assert det==0
                # All prime Fourier 2-by-2 minors, not just the source's affine examples.
                count=0
                for r0,r1 in itertools.combinations(range(n),2):
                    for c0,c1 in itertools.combinations(range(n),2):
                        assert (pow(w,r0*c0+r1*c1,p)-pow(w,r0*c1+r1*c0,p))%p;count+=1
                rng=random.Random(20261020+n+h);rowperm=rng.sample(range(n),n);colperm=rng.sample(range(n),n)
                assert (pow(w,rowperm[rr[0]]*colperm[cc[0]]+rowperm[rr[1]]*colperm[cc[1]],p)-pow(w,rowperm[rr[0]]*colperm[cc[1]]+rowperm[rr[1]]*colperm[cc[0]],p))%p
                minors.append({'N':n,'h':h,'weighted_packet_minor':det,'all_Fourier_two_by_two_minors':count,'arbitrary_permutation_witness':'PASS'})
            # At alpha zero each resolvent is I: original exact counts require an extra nonzero guard.
            counts=[]
            for s in range(n):
                coefficient=sum(pow(w,-r*s,p) for r in range(n))*f.inv(n)%p
                assert coefficient==int(s==0);counts.append(n if coefficient else 0)
            zero.append({'N':n,'h':h,'alpha':0,'character_support_counts':counts,'orbit_span_dimension':1})
            out.append({'N':n,'field':p,'root':w,'alpha':alpha,'h':h,'character_cases':n,'weighted_entry_equalities':n*n})
    return {'packet_cases':out,'total_character_matrices':total,'fiber_minor_controls':minors,'alpha_zero_guard_controls':zero}

def krylov():
    source=json.loads((BASE/'sources/weyl_v20/results.json').read_text());p=1009;f=Field(p);out=[]
    for case in source['krylov_cases']:
        n=case['N'];a=f.eye(n)
        for shift,weight in zip(case['shifts'],case['weights']):
            for j in range(n):a[(j+shift)%n][j]=(a[(j+shift)%n][j]-weight)%p
        inv=f.inverse(a);assert all(x for row in inv for x in row)
        graph=[[i for i in range(n) if a[i][j]] for j in range(n)];delta=max(map(len,graph));diameter=0
        for origin in range(n):
            distance=[None]*n;distance[origin]=0;q=deque([origin])
            while q:
                v=q.popleft()
                for u in graph[v]:
                    if distance[u] is None:distance[u]=distance[v]+1;q.append(u)
            assert all(d is not None for d in distance);diameter=max(diameter,max(distance))
            vec=[int(i==origin) for i in range(n)]
            for step in range(n):
                assert all(not x or distance[i]<=step for i,x in enumerate(vec))
                vec=[sum(x*y for x,y in zip(row,vec))%p for row in a]
        power=f.eye(n);columns=[];target=[x for row in inv for x in row];degree=None
        for d in range(n):
            columns.append([x for row in power for x in row]);mat=list(map(list,zip(*columns)))
            if f.rank(mat)==f.rank([row+[t] for row,t in zip(mat,target)]):degree=d;break
            power=f.mul(power,a)
        bound=0
        while sum(delta**s for s in range(bound+1))<n:bound+=1
        assert diameter==case['directed_diameter'];assert degree==case['minimal_inverse_polynomial_degree'];assert delta==case['max_outdegree'];assert bound==case['size_lower_bound'];assert degree>=diameter>=bound
        out.append({'N':n,'field':p,'inverse_dense':True,'diameter':diameter,'maximum_outdegree':delta,'inverse_polynomial_degree':degree,'branching_bound':bound,'support_radius_controls':n*n})
    return out

if __name__=='__main__':
    result={'status':'PASS','weyl':packet_controls(),'krylov':krylov(),'timing_claims_replayed':False}
    (BASE/'WEYL_V20_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: 150 full character matrices, 14 weighted packets, 12 zero minors and all prime Fourier 2x2 minors, 14 alpha-zero guards, four saved Krylov cases')
