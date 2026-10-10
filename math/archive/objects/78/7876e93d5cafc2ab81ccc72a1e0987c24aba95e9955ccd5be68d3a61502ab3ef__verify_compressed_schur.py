#!/usr/bin/env python3
"""Fresh, standard-library exact checks. Does not import earlier research code."""
import json
from pathlib import Path

P=65537

def root(n,p=P):
    # These are explicitly tested field fixtures, not a field/root construction algorithm.
    for a in range(2,p):
        w=pow(a,(p-1)//n,p)
        if pow(w,n,p)==1 and (n==1 or pow(w,n//2,p)!=1): return w
    raise AssertionError('root unavailable')

def qstep(x,w,p=P):
    N=len(x); out=[0]*N; phase=1
    for s,a in enumerate(x):
        out[2*s%N]=(out[2*s%N]+a)%p
        out[(2*s+1)%N]=(out[(2*s+1)%N]+phase*a)%p
        phase=phase*w%p
    return out

def gamma(k):
    g=0
    while k:
        if k&1: g+=k//2
        k//=2
    return g

def word_good(k,t,b):
    return k.bit_length()==t and k%2==1 and ('0'*b not in format(k,'b'))

def croute(v,t,b,w,N,p=P):
    r=len(v); mask=(1<<t)-1; eta=pow(w,1<<b,p)
    zeta=w*pow(eta,-1,p)%p
    out=[0]*r
    for a,x in enumerate(v):
        k=a&mask
        if word_good(k,t,b):
            y=((1<<b)*(a-k)+k)%r
            out[y]=(out[y]+pow(zeta,gamma(k),p)*x)%p
    return out

def compressed(v,N,b,w,H=None,p=P):
    n=N.bit_length()-1; H=n if H is None else H
    r=len(v); eta=pow(w,1<<b,p); out=[[0]*r for _ in range(H+1)]
    cur=v[:]
    for t in range(1,H-b+1):
        cur=qstep(cur,eta,p)
        out[b+t]=croute(cur,t,b,w,N,p)
    return out

def direct(v,N,b,w,H=None,p=P):
    n=N.bit_length()-1; H=n if H is None else H
    R=list(range(0,N,1<<b)); r=len(R); out=[[0]*r for _ in range(H+1)]
    x=[0]*N
    for j,s in enumerate(R): x[s]=v[j]
    x=qstep(x,w,p)
    for s in R: x[s]=0
    for L in range(2,H+1):
        x=qstep(x,w,p)
        out[L]=[x[s] for s in R]
        for s in R: x[s]=0
    return out

def add(a,b,p=P): return [(x+y)%p for x,y in zip(a,b)]
def tree(v,p=P):
    y=[0]*len(v)
    for j,x in enumerate(v): y[2*j%len(v)]=(y[2*j%len(v)]+x)%p
    return y

def polynomial_compressed(v,N,b,w,H,p=P):
    r=len(v[0]); eta=pow(w,1<<b,p)
    out=[v[j][:] for j in range(H+1)]
    for j in range(H):
        a=tree(v[j],p)
        out[j+1]=[(x-y)%p for x,y in zip(out[j+1],a)]
    cur=[row[:] for row in v]
    visits=0
    for t in range(1,H-b+1):
        cur=[qstep(cur[j],eta,p) for j in range(H-b-t+1)]
        for j,row in enumerate(cur):
            a=croute(row,t,b,w,N,p)
            out[j+b+t]=[(x-y)%p for x,y in zip(out[j+b+t],a)]
            visits+=r
    assert visits==r*max(H-b,0)*(max(H-b,0)+1)//2
    return out,visits

class Prepared:
    """Literal table-driven retained evaluator; all routes and updates are charged."""
    def __init__(self,N,b,w,p=P):
        self.N,self.b,self.p=N,b,p;self.n=N.bit_length()-1;self.r=N>>b;self.d=self.n-b
        r=self.r; eta=pow(w,1<<b,p);zeta=w*pow(eta,-1,p)%p
        self.qphase=[1]*r; powers=[1]*r
        for k in range(1,r):
            self.qphase[k]=self.qphase[k-1]*eta%p
            powers[k]=powers[k-1]*zeta%p
        self.fix=[1]*r;trail=[0]*r;run=[0]*r;self.good=[False]*r
        for k in range(1,r):
            j=k//2
            self.fix[k]=self.fix[j]*(powers[j] if k&1 else 1)%p
            trail[k]=0 if k&1 else trail[j]+1
            run[k]=max(run[j],trail[k]);self.good[k]=(k&1)==1 and run[k]<b
    def step(self,v):
        r=self.r;p=self.p;out=[0]*r
        for s,a in enumerate(v):
            out[2*s%r]=(out[2*s%r]+a)%p
            out[(2*s+1)%r]=(out[(2*s+1)%r]+self.qphase[s]*a)%p
        return out
    def route_into(self,v,t,out):
        r=self.r;b=self.b;p=self.p;mask=(1<<t)-1;lead=1<<(t-1)
        for a,x in enumerate(v):
            k=a&mask
            if k>=lead and self.good[k]:
                y=((1<<b)*(a-k)+k)%r
                out[y]=(out[y]+self.fix[k]*x)%p
    def solve(self,source,H=None):
        H=self.n if H is None else H
        assert H<=self.n
        r=self.r;p=self.p
        residual=[row[:] for row in source];out=[];visits=0
        for j in range(H+1):
            v=residual[j][:];out.append(v)
            if j<H:
                for a,x in enumerate(v):
                    residual[j+1][2*a%r]=(residual[j+1][2*a%r]+x)%p
            cur=v
            for t in range(1,H-j-self.b+1):
                cur=self.step(cur);self.route_into(cur,t,residual[j+self.b+t]);visits+=r
        d=max(H-self.b,0)
        assert visits==r*d*(d+1)//2
        return out,visits

def global_source(x,N,b,w,H,p=P):
    R=list(range(0,N,1<<b));state=x[:]
    for s in R:state[s]=0
    out=[[x[s] for s in R]]
    for _ in range(H):
        state=qstep(state,w,p);out.append([state[s] for s in R])
        for s in R: state[s]=0
    return out

def rank(a,p=P):
    a=[row[:] for row in a]
    if not a: return 0
    i=0
    for j in range(len(a[0])):
        z=next((k for k in range(i,len(a)) if a[k][j]%p),None)
        if z is None: continue
        a[i],a[z]=a[z],a[i]; q=pow(a[i][j],-1,p)
        a[i]=[x*q%p for x in a[i]]
        for k in range(i+1,len(a)):
            q=a[k][j]
            if q: a[k]=[(x-q*y)%p for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a): break
    return i

def source_columns(N,b,w,H,p=P):
    R=list(range(0,N,1<<b)); E=[s for s in range(N) if s%(1<<b)]
    columns=[]
    for s in E:
        x=[0]*N; x[s]=1; col=[]
        for _ in range(H):
            x=qstep(x,w,p); col += [x[t] for t in R]
            for t in R: x[t]=0
        columns.append(col)
    return [list(row) for row in zip(*columns)]

def main():
    result={'field':P,'basis_cases':[],'polynomial_cases':[],'support_cases':[], 'source_ranks':[], 'inverse_cases':[], 'recovery_cases':[]}
    for N in [2,4,8,16,32,64,128]:
        w=root(N); n=N.bit_length()-1
        for b in range(1,n+1):
            r=N>>b
            for j in range(r):
                v=[0]*r;v[j]=1
                assert compressed(v,N,b,w)==direct(v,N,b,w),(N,b,j)
            result['basis_cases'].append({'N':N,'b':b,'r':r,'basis_inputs':r})
            for t in range(1,n-b+1):
                good=[k for k in range(1<<t) if word_good(k,t,b)]
                support=set()
                for a in range(r):
                    k=a% (1<<t)
                    if word_good(k,t,b): support.add(((1<<b)*(a-k)+k)%r)
                expected=len(good)*max(r//(1<<(b+t)),1)
                assert len(support)==expected
                result['support_cases'].append({'N':N,'b':b,'t':t,'words':len(good),'slots':len(support)})
            v=[[((j+1)*(k+3)+j*j+7*k*k)%P for k in range(r)] for j in range(n+1)]
            got,visits=polynomial_compressed(v,N,b,w,n)
            want=[v[j][:] for j in range(n+1)]
            for j in range(n):
                a=tree(v[j]);want[j+1]=[(x-y)%P for x,y in zip(want[j+1],a)]
            for j in range(n+1):
                z=direct(v[j],N,b,w,n-j)
                for k in range(len(z)):
                    want[j+k]=[(x-y)%P for x,y in zip(want[j+k],z[k])]
            assert got==want,(N,b,'polynomial')
            result['polynomial_cases'].append({'N':N,'b':b,'r':r,'routed_state_visits':visits})
            prep=Prepared(N,b,w)
            solved,solve_visits=prep.solve(v)
            applied,_=polynomial_compressed(solved,N,b,w,n)
            assert applied==v,(N,b,'inverse')
            # Verify a supplied arbitrary polynomial marker's top coefficient.
            marker=[[((j+4)*(k+1)+11*j)%P for k in range(r)] for j in range(n+1)]
            mark=sum(marker[j][k]*solved[n-j][k] for j in range(n+1) for k in range(r))%P
            result['inverse_cases'].append({'N':N,'b':b,'visits':solve_visits,'marked_top_coefficient':mark})
            x=[(s*s+9*s+5)%P for s in range(N)]
            rhs=global_source(x,N,b,w,n)
            got,_=prep.solve(rhs)
            cur=x[:];R=list(range(0,N,1<<b));full=[]
            for j in range(n+1):
                full.append(cur[:]);assert got[j]==[cur[s] for s in R],(N,b,j,'global retained')
                cur=qstep(cur,w)
            # Reconstruct eliminated coefficients from the original block equation.
            previous=[0]*N;recovered=[]
            for j in range(n+1):
                rec=x[:] if j==0 else qstep(previous,w)
                for k,s in enumerate(R):rec[s]=got[j][k]
                assert rec==full[j],(N,b,j,'global recovery')
                recovered.append(rec);previous=rec
            h=[(3*s*s+7*s+2)%P for s in range(N)]
            assert sum(h[s]*recovered[n][s] for s in range(N))%P==sum(h[s]*full[n][s] for s in range(N))%P
            result['recovery_cases'].append({'N':N,'b':b,'all_coefficients_checked':n+1})
            if N<=64:
                A=source_columns(N,b,w,n)
                result['source_ranks'].append({'N':N,'b':b,'rank':rank(A),'rows':n*r,'cols':N-r})
    # A concrete failure of extending the finite-horizon route unchanged.
    N=16;b=2;w=root(N);v=[1,2,3,4];H=5
    got=compressed(v,N,b,w,H);want=direct(v,N,b,w,H)
    assert got[:5]==want[:5] and got[5]!=want[5]
    result['beyond_horizon_failure']={'N':N,'b':b,'omega':w,'input':v,'degree':5,'naive_value':got[5],'exact_value':want[5]}
    result['summary']={'basis_parameters':len(result['basis_cases']), 'basis_inputs':sum(a['basis_inputs'] for a in result['basis_cases']), 'polynomial_parameters':len(result['polynomial_cases']), 'support_parameters':len(result['support_cases']), 'inverse_parameters':len(result['inverse_cases']), 'full_recovery_parameters':len(result['recovery_cases'])}
    path=Path(__file__).with_name('COMPRESSED_SCHUR_CONTROLS.json');path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],sort_keys=True));print('ALL EXACT CHECKS PASSED')
if __name__=='__main__': main()
