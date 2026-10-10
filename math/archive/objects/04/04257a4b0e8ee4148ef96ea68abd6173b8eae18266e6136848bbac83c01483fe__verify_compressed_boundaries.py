#!/usr/bin/env python3
"""Fresh standard-library checks; no imported research/constructor programs."""
import json
from pathlib import Path
P=65537

def root(N):
    for a in range(2,P):
        w=pow(a,(P-1)//N,P)
        if pow(w,N,P)==1 and pow(w,N//2,P)!=1:return w
    raise AssertionError()

def qstep(x,w):
    N=len(x);out=[0]*N;phase=1
    for s,a in enumerate(x):
        out[2*s%N]=(out[2*s%N]+a)%P
        out[(2*s+1)%N]=(out[(2*s+1)%N]+phase*a)%P
        phase=phase*w%P
    return out

def qtstep(x,w):
    N=len(x);out=[0]*N;phase=1
    for s in range(N):
        out[s]=(x[2*s%N]+phase*x[(2*s+1)%N])%P
        phase=phase*w%P
    return out

def gamma(k):
    ans=0
    while k:
        ans+=(k//2)*(k&1);k//=2
    return ans

def rev(k,d):
    ans=0
    for _ in range(d):ans=2*ans+(k&1);k//=2
    return ans

def good(k,L,b):
    return k>0 and k.bit_length()==L and '0'*b not in format(k,'b')

def fold_inputs(x,b):
    N=len(x);r=N>>b;us=[]
    for c in range(b):
        a=b-c;u=[0]*r
        for j in range(N>>a):u[j%r]=(u[j%r]+x[j<<a])%P
        us.append(u)
    return us

def schur_coefficient(cur,t,b,w,N):
    r=len(cur);eta=pow(w,1<<b,P);out=[0]*r
    for a,v in enumerate(cur):
        k=a% (1<<t)
        if good(k,t,b) and k%2:
            y=((1<<b)*(a-k)+k)%r
            out[y]=(out[y]+pow(w*pow(eta,-1,P)%P,gamma(k),P)*v)%P
    return out

def compressed_source(x,b,w):
    N=len(x);n=N.bit_length()-1;d=n-b;r=1<<d
    out=[[0]*r for _ in range(n+1)];out[0]=x[::1<<b]
    for s in range(1,N):
        a=(s&-s).bit_length()-1
        if a<b:
            L=b-a;y=(s>>a)%r;out[L][y]=(out[L][y]+x[s])%P
    cur=x[:]
    for t in range(1,d+1):
        cur=qstep(cur,w)
        for a,v in enumerate(cur):
            k=a% (1<<t);c=t-k.bit_length()
            if k%2 and c<b and '0'*b not in format(k,'b'):
                out[b+t][a%r]=(out[b+t][a%r]+v)%P
    eta=pow(w,1<<b,P);us=fold_inputs(x,b)
    for c in range(min(b,d)):
        cur=us[c]
        for t in range(1,d-c+1):
            cur=qstep(cur,eta);v=schur_coefficient(cur,t,b,w,N)
            out[b+c+t]=[(a-z)%P for a,z in zip(out[b+c+t],v)]
    return out

def direct_source(x,b,w):
    N=len(x);n=N.bit_length()-1;R=list(range(0,N,1<<b));cur=x[:]
    for s in R:cur[s]=0
    out=[[x[s] for s in R]]
    for L in range(1,n+1):
        cur=qstep(cur,w);out.append([cur[s] for s in R])
        for s in R:cur[s]=0
    return out

def forced_constant(v,N,b,w,H=None):
    n=N.bit_length()-1;H=n if H is None else H;d=n-b;r=1<<d;eta=pow(w,1<<b,P)
    out=[[0]*N for _ in range(H+1)];cur=v[:]
    for L in range(1,min(d,H)+1):
        cur=qstep(cur,eta)
        for a,u in enumerate(cur):
            k=a%(1<<L)
            if good(k,L,b):
                y=((1<<b)*(a-k)+k)%N
                out[L][y]=(out[L][y]+pow(w*pow(eta,-1,P)%P,gamma(k),P)*u)%P
    if H>d:
        assert len(cur)==r
        for L in range(d+1,H+1):
            for word in range(1<<(L-1),1<<L):
                if good(word,L,b):
                    a=word>>(L-d)
                    phase=pow(w,gamma(word),P)*pow(pow(eta,gamma(a),P),-1,P)%P
                    out[L][word]=phase*cur[a]%P
    return out

def direct_forced(v,N,b,w,H=None):
    n=N.bit_length()-1;H=n if H is None else H;R=list(range(0,N,1<<b))
    cur=[0]*N
    for j,s in enumerate(R):cur[s]=v[j]
    out=[[0]*N]
    for L in range(1,H+1):
        cur=qstep(cur,w)
        for s in R:cur[s]=0
        out.append(cur[:])
    return out

def compressed_free(x,b,w):
    N=len(x);n=N.bit_length()-1;d=n-b;r=1<<d;eta=pow(w,1<<b,P)
    full=x[:]
    for _ in range(n):full=qstep(full,w)
    us=fold_inputs(x,b);trans=[]
    for u in us:
        cur=u[:]
        for _ in range(d):cur=qstep(cur,eta)
        trans.append(cur)
    out=[0]*N;correction=[0]*N;mask=[]
    for word in range(1,N):
        binary=format(word,'0%db'%n)
        if '0'*b in binary:continue
        c=n-word.bit_length();freq=rev(word,n);a=rev((freq>>c)%r,d)
        assert a==word>>(b-c)
        phase=pow(w,gamma(word),P)*pow(pow(eta,gamma(a),P),-1,P)%P
        correction[word]=phase*trans[c][a]%P
        out[word]=(full[word]-correction[word])%P;mask.append(word)
    return out,full,correction,mask

def direct_free(x,b,w):
    N=len(x);n=N.bit_length()-1;R=list(range(0,N,1<<b));cur=x[:]
    for s in R:cur[s]=0
    for _ in range(n):
        cur=qstep(cur,w)
        for s in R:cur[s]=0
    return cur

def vapply(x,w):
    N=len(x);n=N.bit_length()-1;out=[0]*N
    for s,a in enumerate(x):out[rev(s,n)]=pow(pow(w,gamma(s),P),-1,P)*a%P
    return out

def main():
    result={'field':P,'cases':[], 'polynomial_force_cases':[], 'transpose_cases':[], 'count_cases':[], 'transpose_boundary_cases':[]}
    for N in [2,4,8,16,32,64,128]:
        w=root(N);n=N.bit_length()-1
        x=[(s*s+5*s+7)%P for s in range(N)]
        assert vapply(qstep(x,w),w)==qtstep(vapply(x,w),w)
        result['transpose_cases'].append({'N':N})
        for b in range(1,n+1):
            r=N>>b;d=n-b
            for s in range(N):
                x=[0]*N;x[s]=1
                assert compressed_source(x,b,w)==direct_source(x,b,w),(N,b,s,'source')
                got,full,correction,mask=compressed_free(x,b,w)
                assert got==direct_free(x,b,w),(N,b,s,'free')
                assert N-len(mask)<= (n-b+1)*r
            for j in range(r):
                v=[0]*r;v[j]=1
                assert forced_constant(v,N,b,w)==direct_forced(v,N,b,w),(N,b,j,'forced')
            # Endpoint-weighted transpose turns a suffix-zero source into prefix-zero forced recovery.
            xx=[(s*s+7*s+2)%P if s%(1<<b) else 0 for s in range(N)]
            hh=[(j*j+11*j+3)%P for j in range(r)]
            source=direct_source(xx,b,w)
            hglobal=[0]*N
            for j in range(r):hglobal[j<<b]=hh[j]
            vinvh=[pow(w,gamma(s),P)*hglobal[rev(s,n)]%P for s in range(N)]
            assert all(vinvh[s]==0 for s in range(r,N))
            state=vinvh
            for L in range(1,n+1):
                state=qstep(state,w)
                for s in range(r):state[s]=0
                mapped=vapply(state,w)
                assert sum(hh[j]*source[L][j] for j in range(r))%P==sum(xx[s]*mapped[s] for s in range(N))%P
            result['transpose_boundary_cases'].append({'N':N,'b':b,'all_coefficients':n})
            result['cases'].append({'N':N,'b':b,'global_basis_inputs':N,'retained_basis_inputs':r,'free_allowed_rows':len(mask),'rank_difference_upper':(n+1)*r})
            v=[[((j+3)*(k+5)+j*j+k*k)%P for k in range(r)] for j in range(n+1)]
            got=[[0]*N for _ in range(n+1)];want=[[0]*N for _ in range(n+1)]
            for j in range(n+1):
                a=forced_constant(v[j],N,b,w,n-j);z=direct_forced(v[j],N,b,w,n-j)
                for L in range(len(a)):
                    got[j+L]=[(u+t)%P for u,t in zip(got[j+L],a[L])]
                    want[j+L]=[(u+t)%P for u,t in zip(want[j+L],z[L])]
            assert got==want,(N,b,'polynomial forced')
            stages=sum(min(d,n-j) for j in range(n+1))
            assert stages==d*(n+1)-d*(d+1)//2
            late=sum((n-L+1)*(1<<(L-1)) for L in range(d+1,n+1))
            assert late<2*N
            result['polynomial_force_cases'].append({'N':N,'b':b,'small_state_visits':r*stages,'late_word_visits':late})
    for n in range(1,129):
        N=1<<n
        for b in range(1,n+1):
            # Counts only, not exponentially large transforms.
            state=[0]*b;state[0]=1
            for _ in range(n):state=[sum(state)]+state[:-1]
            allowed=sum(state);r=N>>b
            assert N-allowed<=(n-b+1)*r
            if b>=min(n,2*(n.bit_length()-1)+2):
                result['count_cases'].append({'n':n,'b':b,'missing_rows':N-allowed,'difference_rank_bound':(n+1)*r})
    result['summary']={'parameters':len(result['cases']),'global_basis_inputs':sum(a['global_basis_inputs'] for a in result['cases']),'retained_basis_inputs':sum(a['retained_basis_inputs'] for a in result['cases']),'polynomial_force_parameters':len(result['polynomial_force_cases']),'transpose_parameters':len(result['transpose_cases']),'transpose_boundary_parameters':len(result['transpose_boundary_cases']),'integer_count_parameters':sum(range(1,129))}
    Path(__file__).with_name('COMPRESSED_BOUNDARY_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],sort_keys=True));print('ALL EXACT CHECKS PASSED')
if __name__=='__main__':main()
