#!/usr/bin/env python3
"""Independent audit controls, standard library only; no constructor imports."""
import json,random
from pathlib import Path

def matzero(n,m=None):return [[0]*(n if m is None else m) for _ in range(n)]
def mm(A,B,p):
    C=matzero(len(A),len(B[0]))
    for i,row in enumerate(A):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(B[k]):
                    if y:C[i][j]=(C[i][j]+x*y)%p
    return C
def mv(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]
def rank(A,p):
    A=[row[:] for row in A];r=0
    for j in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None:continue
        A[k],A[r]=A[r],A[k];z=pow(A[r][j],-1,p);A[r]=[x*z%p for x in A[r]]
        for k in range(r+1,len(A)):
            z=A[k][j];A[k]=[(x-z*y)%p for x,y in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r
def plus(x,y,p,k=1):return [(a+k*b)%p for a,b in zip(x,y)]
def qmatrix(N,w,p):
    Q=matzero(N)
    for j in range(N):Q[2*j%N][j]=(Q[2*j%N][j]+1)%p;Q[(2*j+1)%N][j]=(Q[(2*j+1)%N][j]+pow(w,j,p))%p
    return Q
def oracle_feedback(N,b,w,p,H):
    r=N>>b;Q=qmatrix(N,w,p);inds=list(range(0,N,1<<b));E=[[int(i==s) for s in inds] for i in range(N)];state=mm(Q,E,p)
    A=[state[s][:] for s in inds]
    for s in inds:state[s]=[0]*r
    out=[matzero(r) for _ in range(H+1)]
    for L in range(2,H+1):
        state=mm(Q,state,p);out[L]=[state[s][:] for s in inds]
        for s in inds:state[s]=[0]*r
    return Q,A,out

class Plan:
    def __init__(self,N,b,w,p):
        self.N=N;self.n=N.bit_length()-1;self.b=b;self.r=N>>b;self.d=self.n-b;self.p=p
        eta=w;self.setup_mul=0
        for _ in range(b):eta=eta*eta%p;self.setup_mul+=1
        zeta=w*pow(eta,-1,p)%p;self.setup_mul+=1;self.setup_inv=1
        self.ph=[1]*self.r;zp=[1]*self.r
        for k in range(1,self.r):self.ph[k]=self.ph[k-1]*eta%p;zp[k]=zp[k-1]*zeta%p;self.setup_mul+=2
        self.fix=[1]*self.r;tail=[0]*self.r;run=[0]*self.r;self.valid=[False]*self.r
        for k in range(1,self.r):
            a=k>>1;self.fix[k]=self.fix[a]
            if k&1:self.fix[k]=self.fix[k]*zp[a]%p;self.setup_mul+=1
            else:tail[k]=tail[a]+1
            run[k]=max(run[a],tail[k]);self.valid[k]=bool(k&1) and run[k]<b
        assert self.setup_mul==b+1+2*(self.r-1)+self.r//2
        self.count={'state_visits':0,'route_checks':0,'route_updates':0,'mul':0,'add':0,'tree_updates':0,'output_scalars':0}
    def step(self,v):
        out=[0]*self.r;p=self.p
        for j,x in enumerate(v):out[2*j%self.r]=(out[2*j%self.r]+x)%p;out[(2*j+1)%self.r]=(out[(2*j+1)%self.r]+self.ph[j]*x)%p
        self.count['state_visits']+=self.r;self.count['mul']+=self.r;self.count['add']+=2*self.r
        return out
    def route(self,v,t,target):
        for a,x in enumerate(v):
            k=a% (1<<t);self.count['route_checks']+=1
            if k>=1<<(t-1) and self.valid[k]:
                y=((a-k)*(1<<self.b)+k)%self.r;target[y]=(target[y]+self.fix[k]*x)%self.p
                self.count['route_updates']+=1;self.count['mul']+=1;self.count['add']+=1
    def const_feedback(self,v,H):
        res=[[0]*self.r for _ in range(H+1)];cur=v[:]
        for t in range(1,max(H-self.b,0)+1):cur=self.step(cur);self.route(cur,t,res[self.b+t])
        return res
    def solve(self,f,H):
        assert H<=self.n and len(f)==H+1 and all(len(x)==self.r for x in f)
        rho=[x[:] for x in f];sol=[]
        for j in range(H+1):
            v=rho[j][:];sol.append(v);self.count['output_scalars']+=self.r
            if j<H:
                for a,x in enumerate(v):k=2*a%self.r;rho[j+1][k]=(rho[j+1][k]+x)%self.p
                self.count['tree_updates']+=self.r;self.count['add']+=self.r
            cur=v
            for t in range(1,max(H-j-self.b,0)+1):cur=self.step(cur);self.route(cur,t,rho[j+self.b+t])
        return sol

def source_jet(x,N,b,Q,p,H):
    inds=list(range(0,N,1<<b));state=x[:]
    for i in inds:state[i]=0
    out=[[x[i] for i in inds]]
    for L in range(1,H+1):
        state=mv(Q,state,p);out.append([state[i] for i in inds])
        for i in inds:state[i]=0
    return out

def apply_oracle(v,A,K,p,H):
    out=[x[:] for x in v]
    for j in range(H+1):
        if j<H:out[j+1]=plus(out[j+1],mv(A,v[j],p),p,-1)
        for L in range(2,H-j+1):out[j+L]=plus(out[j+L],mv(K[L],v[j],p),p,-1)
    return out

def main():
    rng=random.Random(13101026);out={'policy':'Only independent auditor code executed','cases':[],'source_rank_controls':[],'support_counts':[],'phase_controls':[],'large_cost_counts':[]}
    for p,base in [(65537,3),(257,3)]:
      for n in range(1,9):
        N=1<<n;w=pow(base,(p-1)//N,p);assert pow(w,N,p)==1 and pow(w,N//2,p)==p-1
        for b in range(1,n+1):
            r=N>>b;d=n-b;Q,A,K=oracle_feedback(N,b,w,p,n);plan=Plan(N,b,w,p)
            # Every retained basis coefficient, using full-space matrix multiplication as oracle.
            for j in range(r):
                v=[int(k==j) for k in range(r)];got=plan.const_feedback(v,n)
                for L in range(n+1):assert got[L]==[K[L][i][j] for i in range(r)]
            for t in range(1,d+1):
                words=[k for k in range(1<<(t-1),1<<t) if k&1 and '0'*b not in format(k,'b')]
                support=[i for i in range(r) if any(K[b+t][i])]
                assert len(support)==len(words)*max(r//(1<<(b+t)),1)
                out['support_counts'].append({'N':N,'field':p,'b':b,'t':t,'words':len(words),'rows':len(support)})
            # Word phase checked from actual edge traversal, with initial states near wrap.
            for t in range(1,min(d,5)+1):
                for k in range(1<<t):
                    s=0;gexp=0
                    for bit in format(k,'0%db'%t):
                        if bit=='1':gexp+=s
                        s=2*s+int(bit)
                    rev=int(format(k,'0%db'%t)[::-1],2)
                    for j in sorted(set([0,r//2,r-1])):
                        st=(1<<b)*j;weight=1
                        for bit in format(k,'0%db'%t)+'0'*b:
                            if bit=='1':weight=weight*pow(w,st,p)%p
                            st=(2*st+int(bit))%N
                        assert st//(1<<b)==((1<<(b+t))*j+k)%r
                        assert weight==pow(w,((1<<b)*j*rev+gexp),p)
                    assert plan.fix[k]==pow(w*(pow(pow(w,1<<b,p),-1,p))%p,gexp,p)
                out['phase_controls'].append({'N':N,'field':p,'b':b,'t':t,'all_words':1<<t})
            f=[[rng.randrange(p) for _ in range(r)] for j in range(n+1)];fresh=Plan(N,b,w,p);v=fresh.solve(f,n);assert apply_oracle(v,A,K,p,n)==f
            expected=r*d*(d+1)//2;assert fresh.count['state_visits']==fresh.count['route_checks']==expected and fresh.count['tree_updates']==n*r and fresh.count['output_scalars']==(n+1)*r
            # Independent coefficient recurrence using dense feedback matrices.
            ref=[]
            for j in range(n+1):
                z=f[j][:]
                if j:z=plus(z,mv(A,ref[j-1],p),p)
                for L in range(2,j+1):z=plus(z,mv(K[L],ref[j-L],p),p)
                ref.append(z)
            assert v==ref
            h=[[rng.randrange(p) for _ in range(r)] for j in range(n+1)]
            marked=sum(h[j][k]*v[n-j][k] for j in range(n+1) for k in range(r))%p
            assert marked==sum(h[j][k]*ref[n-j][k] for j in range(n+1) for k in range(r))%p
            # Global source and complete eliminated recovery remain explicitly full-space work.
            x=[rng.randrange(p) for _ in range(N)];src=source_jet(x,N,b,Q,p,n);ret=Plan(N,b,w,p).solve(src,n);cur=x[:];prev=None
            for j in range(n+1):
                rec=x[:] if j==0 else mv(Q,prev,p)
                for k in range(r):rec[k<<b]=ret[j][k]
                assert rec==cur;prev=rec;cur=mv(Q,cur,p)
            # All early source rows, including r=1, tested as a stacked linear map.
            if N<=64:
                cols=[]
                for s in range(N):
                    if not s%(1<<b):continue
                    xx=[int(j==s) for j in range(N)];sj=source_jet(xx,N,b,Q,p,b);cols.append([a for row in sj[1:] for a in row])
                    val=(s&-s).bit_length()-1;L=b-val;y=(s>>(b-L))%r
                    for q in range(1,b+1):assert sj[q]==[int(q==L and j==y) for j in range(r)]
                mat=[list(row) for row in zip(*cols)];rk=rank(mat,p);assert rk==(b*r//2 if r>=2 else b)
                out['source_rank_controls'].append({'N':N,'field':p,'b':b,'r':r,'early_rank':rk,'single_r_summary_excluded':rk>r})
            out['cases'].append({'N':N,'field':p,'b':b,'retained_basis_inputs':r,'arbitrary_polynomial_rhs':True,'global_coefficients_checked':N*(n+1),'marker':marked,'state_visits':expected,'setup_mul':fresh.setup_mul,'setup_inv':fresh.setup_inv,'online_counts':fresh.count})
    # Explicit horizon and wrong-fold/trajectory negative controls.
    N=16;b=2;p=65537;w=64;r=4;v=[1,2,3,4];Q,A,K=oracle_feedback(N,b,w,p,5);bad=Plan(N,b,w,p).const_feedback(v,5);right=mv(K[5],v,p)
    assert bad[5]==[0]*r and right==[0,57313,0,510]
    out['beyond_horizon']={'N':N,'b':b,'field':p,'omega':w,'degree':5,'naive':bad[5],'exact':right}
    # For (N,b)=(32,1), feedback t=1 cannot omit the fold or use t+b trajectory.
    N=32;b=1;p=65537;w=pow(3,(p-1)//N,p);r=N>>b;Q,A,K=oracle_feedback(N,b,w,p,5);v=list(range(1,r+1));pl=Plan(N,b,w,p);u=pl.step(v);correct=[0]*r;pl.route(u,1,correct)
    nofold=[0]*r
    for a,x in enumerate(u):
        k=a%2
        if k==1:nofold[a]=(nofold[a]+pl.fix[k]*x)%p
    extra=pl.step(u);wronglen=[0]*r;pl.route(extra,1,wronglen)
    assert correct==mv(K[2],v,p) and correct!=nofold and correct!=wronglen
    out['wrong_fold_and_length_controls']={'N':N,'b':b,'both_rejected':True}
    # Symbolic integer counts only; no enormous vector allocation.
    for n in [8,16,32,64,128,256,512,1024]:
        b=min(n,2*((n-1).bit_length()));r=(1<<n)>>b;d=n-b;visits=r*d*(d+1)//2;io=r*(n+1)
        assert visits<=1<<n and io<=1<<n
        out['large_cost_counts'].append({'n':n,'b':b,'state_visits_over_N':[visits,1<<n],'input_output_coefficients_over_N':[io,1<<n]})
    out['result']='PASS';Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'result':'PASS','parameters':len(out['cases']),'basis_inputs':sum(x['retained_basis_inputs'] for x in out['cases']),'support_cases':len(out['support_counts']),'source_rank_cases':len(out['source_rank_controls']),'phase_cases':len(out['phase_controls'])}))
if __name__=='__main__':main()
