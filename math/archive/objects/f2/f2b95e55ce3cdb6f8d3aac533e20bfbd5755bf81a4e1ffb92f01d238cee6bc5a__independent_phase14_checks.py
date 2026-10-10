#!/usr/bin/env python3
"""Fresh independent controls; source programs are neither executed nor imported."""
import json,math,random,hashlib
from pathlib import Path

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def mv(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]
def add(A,B,p,k=1):return [[(x+k*y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(A,k,p):return [[k*x%p for x in row] for row in A]
def inv(A,p):
    n=len(A);R=[a[:]+b for a,b in zip(A,eye(n))]
    for j in range(n):
        k=next((k for k in range(j,n) if R[k][j]),None)
        if k is None:return None
        R[j],R[k]=R[k],R[j];t=pow(R[j][j],-1,p);R[j]=[x*t%p for x in R[j]]
        for k in range(n):
            if k!=j:
                t=R[k][j];R[k]=[(x-t*y)%p for x,y in zip(R[k],R[j])]
    return [row[n:] for row in R]
def det(A,p):
    R=[r[:] for r in A];v=1
    for j in range(len(R)):
        k=next((k for k in range(j,len(R)) if R[k][j]),None)
        if k is None:return 0
        if k!=j:R[j],R[k]=R[k],R[j];v=-v
        v=v*R[j][j]%p;t=pow(R[j][j],-1,p)
        for k in range(j+1,len(R)):
            z=R[k][j]*t%p;R[k]=[(x-z*y)%p for x,y in zip(R[k],R[j])]
    return v%p
def rank(A,p):
    basis={}
    for row in A:
        row=row[:]
        for k in sorted(basis):
            z=row[k]
            if z:row=[(a-z*b)%p for a,b in zip(row,basis[k])]
        j=next((j for j,x in enumerate(row) if x),None)
        if j is not None:
            z=pow(row[j],-1,p);basis[j]=[x*z%p for x in row]
    return len(basis)
def root(n,p):
    for a in range(2,p):
        w=pow(a,(p-1)//n,p)
        if pow(w,n,p)==1 and all(pow(w,j,p)!=1 for j in range(1,n)):return w
    raise AssertionError('root')
def denominator(n,p,w,a,b,stride=1,delta=1):
    A=eye(n)
    for j in range(n):A[j][j]=(A[j][j]-b*pow(w,delta*j,p))%p;A[(j+stride)%n][j]=(A[(j+stride)%n][j]-a)%p
    return A
def coeff(A,w,p):
    n=len(A);ni=pow(n,-1,p)
    return [[sum(A[(j+a)%n][j]*pow(w,-b*j,p) for j in range(n))*ni%p for b in range(n)] for a in range(n)]
def cuts(A,p,omitted_middle=False):
    n=len(A);m=n//2;L=list(range(m));R=list(range(n-m if omitted_middle else m,n))
    return [rank([[A[i][j] for j in L] for i in R],p),rank([[A[i][j] for j in R] for i in L],p)]
def batch(xs,p):
    pre=[1]
    for x in xs:
        if not x:raise ValueError('pole')
        pre.append(pre[-1]*x%p)
    z=pow(pre[-1],-1,p);out=[0]*len(xs)
    for i in range(len(xs)-1,-1,-1):out[i]=z*pre[i]%p;z=z*xs[i]%p
    return out
class Solver:
    def __init__(self,n,p,w,a,b,s=1,delta=1):
        self.n=n;self.p=p;self.a=a%p;self.cy=[];self.di=[];phase=1;q=w if delta==1 else pow(w,-1,p)
        for _ in range(n):self.di.append((1-b*phase)%p);phase=phase*q%p
        if not a%p:self.tab=batch(self.di,p);return
        self.tab=None;self.ai=pow(a,-1,p);seen=set();den=[]
        for j in range(n):
            if j in seen:continue
            ids=[];k=j
            while k not in seen:seen.add(k);ids.append(k);k=(k+s)%n
            assert k==j
            ratios=[self.di[i]*self.ai%p for i in ids];prod=1
            for rr in ratios[1:]:prod=prod*rr%p
            d=(self.di[j]*prod-a)%p
            if not d:raise ValueError('pole')
            self.cy.append((ids,ratios));den.append(d)
        self.closure=batch(den,p)
    def apply(self,x):
        n=self.n;p=self.p
        if self.tab is not None:return [a*b%p for a,b in zip(x,self.tab)]
        y=[0]*n
        for (ids,rr),din in zip(self.cy,self.closure):
            B=0
            for k in range(len(ids)-1,0,-1):B=(rr[k]*B-self.ai*x[ids[k]])%p
            y[ids[-1]]=(x[ids[0]]-self.di[ids[0]]*B)*din%p
            for k in range(len(ids)-1,0,-1):y[ids[k-1]]=(rr[k]*y[ids[k]]-self.ai*x[ids[k]])%p
        return y

def twirl(x,n,p,w,a,b,axis):
    D=(1-pow(a,n,p)-pow(b,n,p))%p;di=pow(D,-1,p)
    if axis=='T':
        bn=pow(b,n,p)
        if bn==1:
            phase=1;y=[0]*n
            for j in range(n):
                if b*phase%p==1:y[j]=n*di*x[j]%p
                phase=phase*w%p
            return y
        z=Solver(n,p,w,0,b).apply(x);return [(1-bn)*di*v%p for v in z]
    an=pow(a,n,p)
    if an==1:
        ai=pow(a,-1,p);t=1;total=0
        for v in x:total=(total+t*v)%p;t=t*ai%p
        t=1;y=[]
        for _ in x:y.append(t*total*di%p);t=t*a%p
        return y
    z=Solver(n,p,w,a,0).apply(x);return [(1-an)*di*v%p for v in z]

def main():
    rng=random.Random(14101026);out={'policy':'No uploaded code executed or imported','small':[],'span_checks':[],'mixed_depth':[],'strides':[]};basis=0;coefs=0;twirls=0;qpoly=0;guards=0
    cases=[(2,17),(3,31),(4,41),(5,101),(6,73),(7,113),(8,113),(9,109),(10,241),(12,157),(16,193)]
    signs=[(1,1),(1,-1),(-1,1),(-1,-1)]
    for n,p in cases:
        w=root(n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];FC=coeff(F,w,p);G=sum(pow(w,j*j,p) for j in range(n))%p;Gi=sum(pow(w,-j*j,p) for j in range(n))%p
        if n%2:assert G*Gi%p==n%p and all(all(row) for row in FC)
        elif n%4==0:assert G*Gi%p==2*n%p and FC[n//2][n//2]
        else:assert G==0 and FC[n//2][n//2]==0
        assert cuts(F,p)==[n//2]*2
        supports=[];matrices=[]
        for eps,delta in signs:
            support={((eps*a)%n,(delta*b)%n) for a in range(n) for b in range(n) if a+b<n};supports.append(support)
            for a,b in [(2,3),(2,1),(0,3),(1,0),(0,1),(0,0)]:
                A=denominator(n,p,w,a,b,eps,delta);D=(1-pow(a,n,p)-pow(b,n,p))%p;assert det(A,p)==D
                H=inv(A,p)
                if not D:
                    assert H is None
                    try:Solver(n,p,w,a,b,eps,delta);raise AssertionError('pole missed')
                    except ValueError:pass
                    guards+=1;continue
                op=Solver(n,p,w,a,b,eps,delta);C=coeff(H,w,p);nonzero={(i,j) for i in range(n) for j in range(n) if C[i][j]}
                assert nonzero<=support
                if a and b:assert nonzero==support
                assert max(cuts(H,p))<=1
                for j in range(n):
                    x=[int(k==j) for k in range(n)];assert op.apply(x)==[row[j] for row in H];basis+=1
                coefs+=n*n
                if n<=10:
                    W=add(eye(n),A,p,-1);P=eye(n);total=[[0]*n for _ in range(n)]
                    for _ in range(n):total=add(total,P,p);P=mm(W,P,p)
                    assert P==scale(eye(n),(pow(a,n,p)+pow(b,n,p))%p,p)
                    assert scale(total,pow(D,-1,p),p)==H;qpoly+=1
                if eps==delta==1:
                    x=[rng.randrange(p) for _ in range(n)]
                    for axis in ['S','T']:
                        target=[[0]*n for _ in range(n)];ni=pow(n,-1,p)
                        for i in range(n):
                            for j in range(n):
                                val=sum(H[(i-k)%n][(j-k)%n] if axis=='S' else pow(w,k*(i-j),p)*H[i][j] for k in range(n))
                                target[i][j]=val*ni%p
                        assert twirl(x,n,p,w,a,b,axis)==mv(target,x,p);twirls+=1
                matrices.append(H)
        union=set.union(*supports);missing={(i,j) for i in range(n) for j in range(n)}-union
        assert missing==({(n//2,n//2)} if n%2==0 else set())
        if n%2:
            for omitted in range(4):
                missing={(i,j) for i in range(n) for j in range(n)}-set.union(*[S for k,S in enumerate(supports) if k!=omitted]);assert any(FC[i][j] for i,j in missing)
        # Genuine partition tested for the product law; the old separated blocks are submatrices.
        for trial in range(12):
            total=[[0]*n for _ in range(n)];budget=0
            for _ in range(1+trial%3):
                M=eye(n);depth=1+rng.randrange(3);budget+=depth
                for _ in range(depth):
                    H=rng.choice(matrices);diag=[rng.randrange(p) for _ in range(n)];H=[[diag[i]*x%p for x in row] for i,row in enumerate(H)];M=mm(H,M,p)
                total=add(total,M,p)
            assert max(cuts(total,p))<=budget and max(cuts(total,p,True))<=budget
            out['mixed_depth'].append({'n':n,'field':p,'budget':budget,'true_cut_ranks':cuts(total,p)})
        # All physical strides, including stride zero and zero local diagonal pivots.
        for stride in range(n):
            for a,b in [(2,3),(2,1),(0,3)]:
                A=denominator(n,p,w,a,b,stride);H=inv(A,p)
                try:op=Solver(n,p,w,a,b,stride)
                except ValueError:assert H is None;guards+=1;continue
                assert H is not None;x=[rng.randrange(p) for _ in range(n)];assert op.apply(x)==mv(H,x,p)
                out['strides'].append({'n':n,'field':p,'stride':stride,'alpha':a,'beta':b})
        out['small'].append({'n':n,'field':p,'omega':w,'Gauss':G,'span_dimension_formula':n*n-int(n%2==0)})
    # Actual inverse-matrix sampled spans, independent of counting support masks.
    for n,p in cases[:9]:
        w=root(n,p);rows=[];expected=n*n-int(n%2==0)
        for eps,delta in signs:
            for a in range(n+2):
                for b in range(n+2):
                    H=inv(denominator(n,p,w,a,b,eps,delta),p)
                    if H is not None:rows.append([x for row in H for x in row])
        rr=rank(rows,p);assert rr==expected;out['span_checks'].append({'n':n,'field':p,'sampled_inverse_matrices':len(rows),'rank':rr})
    A=eye(3);B=eye(3);A[2][1]=1;B[1][0]=1;AB=mm(A,B,101)
    assert cuts(A,101,True)==cuts(B,101,True)==[0,0] and cuts(AB,101,True)==[1,0]
    assert max(cuts(AB,101))<=max(cuts(A,101))+max(cuts(B,101))
    out['odd_cut_counterexample']={'N':3,'field':101,'A':A,'B':B,'old_ranks':[cuts(M,101,True) for M in [A,B,AB]],'correct_partition_ranks':[cuts(M,101) for M in [A,B,AB]]}
    # Prior noncoprime-resonance false-rejection control must be accepted.
    n=8;p=97;w=64;a=64;s=2;x=[1,50,64,96,22,33,50,75];op=Solver(n,p,w,a,0,s);A=denominator(n,p,w,a,0,s);y=op.apply(x)
    assert pow(a,n,p)==1 and pow(a,n//math.gcd(n,s),p)!=1 and mv(A,y,p)==x
    out['noncoprime_no_pole_control']={'n':n,'field':p,'alpha':a,'stride':s,'alpha_to_N':1,'alpha_to_cycle_length':pow(a,4,p),'accepted':True}
    n=65536;p=998244353;w=pow(3,(p-1)//n,p);x=[rng.randrange(p) for _ in range(n)];a=17;b=23;op=Solver(n,p,w,a,b);y=op.apply(x);zp=Solver(n,p,w,2,1).apply(x);phase=1
    for i in range(n):
        assert ((1-b*phase)*y[i]-a*y[i-1])%p==x[i]
        assert ((1-phase)*zp[i]-2*zp[i-1])%p==x[i]
        phase=phase*w%p
    ys=twirl(x,n,p,w,a,b,'S');yt=twirl(x,n,p,w,a,b,'T');D=(1-pow(a,n,p)-pow(b,n,p))%p;rs=(1-pow(a,n,p))*pow(D,-1,p)%p;rt=(1-pow(b,n,p))*pow(D,-1,p)%p;phase=1
    for i in range(n):assert (ys[i]-a*ys[i-1])%p==rs*x[i]%p and (1-b*phase)*yt[i]%p==rt*x[i]%p;phase=phase*w%p
    long=Solver(n,p,w,2,0,n//2).apply(x);di=pow(-3,-1,p)
    assert all(long[i]==(x[i]+2*x[(i-n//2)%n])*di%p for i in range(n))
    mismatch=0
    for k in [0,1,7,123,n//2,n-1]:
        wk=pow(w,k,p);pw=1;val=0
        for xx in x:val=(val+pw*xx)%p;pw=pw*wk%p
        mismatch+=int(val!=y[k])
    assert mismatch==6
    P=lambda k:k.bit_length()-1+k.bit_count()
    prep_source=5*n+5+2*P(n)+P(n-1);prep_correct=prep_source+1;online=6*n-3
    assert prep_source==327750 and prep_correct+online==720964
    out['source_counter_correction']={'reason':'unmetered multiplication in normal Python assert den * pow_count(alpha,N-1)','reported_prep':prep_source,'corrected_prep':prep_correct,'online':online,'reported_total':prep_source+online,'corrected_total':prep_correct+online,'reported_S_twirl':786538,'corrected_S_twirl':786539,'T_twirl_unchanged':524364,'long_stride_unchanged':753666,'memory_counters':'partial vector-access instrumentation; table preparation and many coefficient reads not counted'}
    out['large']={'N':n,'field':p,'magnetic_equations':2*n,'twirl_equations':2*n,'long_stride_closed_form_outputs':n,'DFT_bins_distinct':mismatch,'output_sha256':hashlib.sha256(json.dumps(y).encode()).hexdigest()}
    out['summary']={'basis_inputs':basis,'full_matrix_coefficients':coefs,'q_polynomial_identities':qpoly,'twirl_matrix_checks':twirls,'singular_guard_checks':guards,'stride_cases':len(out['strides']),'mixed_depth_cases':len(out['mixed_depth'])};out['result']='PASS'
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']|{'result':'PASS'}))
if __name__=='__main__':main()
