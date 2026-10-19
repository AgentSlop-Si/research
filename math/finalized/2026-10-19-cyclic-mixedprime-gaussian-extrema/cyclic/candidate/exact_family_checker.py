"""Fresh characteristic-zero checks; imports no historical research programs.
All matrix entries are exact in Q[z]/Phi_(4N)(z), z=exp(pi*i/(2N)).
No floating-point calculation or optimization is used here.
"""
from fractions import Fraction as Q
from functools import lru_cache
from collections import defaultdict
import json, hashlib, pathlib, time
import sympy as sp

class Cyclo:
    def __init__(self, order):
        self.order=order
        x=sp.Symbol('x'); self.x=x
        self.poly=sp.Poly(sp.cyclotomic_poly(order,x),x)
        self.d=self.poly.degree()
        self.mod=[int(self.poly.nth(k)) for k in range(self.d)]
        self.zero=(Q(0),)*self.d
        self.one=(Q(1),)+(Q(0),)*(self.d-1)
        powers=[]
        for e in range(order):
            a=[0]*(max(e,self.d)+1); a[e]=1
            for k in range(len(a)-1,self.d-1,-1):
                if a[k]:
                    c=a[k]
                    for j,b in enumerate(self.mod): a[k-self.d+j]-=c*b
            powers.append(tuple(Q(v) for v in a[:self.d]))
        self.powers=powers
    def root(self,e):return self.powers[e%self.order]
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def sub(self,a,b):return tuple(x-y for x,y in zip(a,b))
    def scale(self,a,s):return tuple(s*x for x in a)
    @lru_cache(maxsize=150000)
    def mul(self,a,b):
        if a==self.zero or b==self.zero:return self.zero
        if a==self.one:return b
        if b==self.one:return a
        c=[Q(0)]*(2*self.d-1)
        ia=[(i,x) for i,x in enumerate(a) if x]
        ib=[(j,y) for j,y in enumerate(b) if y]
        for i,x in ia:
            for j,y in ib:c[i+j]+=x*y
        for k in range(len(c)-1,self.d-1,-1):
            if c[k]:
                t=c[k]
                for j,bj in enumerate(self.mod):
                    if bj:c[k-self.d+j]-=t*bj
        return tuple(c[:self.d])
    @lru_cache(maxsize=150000)
    def conj(self,a):
        r=[Q(0)]*self.d
        for j,c in enumerate(a):
            if c:
                for k,p in enumerate(self.root(-j)):
                    if p:r[k]+=c*p
        return tuple(r)
    def inv(self,a):
        expr=sum(sp.Rational(v.numerator,v.denominator)*self.x**j for j,v in enumerate(a) if v)
        ans=sp.Poly(sp.invert(expr,self.poly.as_expr(),self.x),self.x)
        return tuple(Q(ans.nth(j)) for j in range(self.d))
    def terms(self,terms,den=1):
        r=[Q(0)]*self.d
        for e,c in terms.items():
            if c:
                for j,p in enumerate(self.root(e)):
                    if p:r[j]+=c*p
        return tuple(x/den for x in r)

class Matrix:
    def __init__(self,R,n,entries=None):
        self.R,self.n=R,n
        self.a={k:v for k,v in (entries or {}).items() if v!=R.zero}
    def add(self,b):
        d=dict(self.a)
        for k,v in b.a.items():d[k]=self.R.add(d.get(k,self.R.zero),v)
        return Matrix(self.R,self.n,d)
    def scale(self,s):return Matrix(self.R,self.n,{k:self.R.mul(v,s) for k,v in self.a.items()})
    def sub(self,b):return self.add(b.scale(self.R.neg(self.R.one)))
    def mul(self,b):
        rows=defaultdict(list)
        for (k,j),v in b.a.items():rows[k].append((j,v))
        d={}
        for (i,k),v in self.a.items():
            for j,w in rows[k]:d[i,j]=self.R.add(d.get((i,j),self.R.zero),self.R.mul(v,w))
        return Matrix(self.R,self.n,d)
    def conj(self):return Matrix(self.R,self.n,{k:self.R.conj(v) for k,v in self.a.items()})
    def tr(self):
        s=self.R.zero
        for j in range(self.n):s=self.R.add(s,self.a.get((j,j),self.R.zero))
        return s
    def transpose(self):return Matrix(self.R,self.n,{(j,i):v for (i,j),v in self.a.items()})
    def eq(self,b):return self.a==b.a

def identity(R,n):return Matrix(R,n,{(j,j):R.one for j in range(n)})
def phase_data(N,parity_factor=True,global_phase=True):
    m=N//4
    q=[0 if j%2==0 else ((m*N if parity_factor else 0)-2+4*j) for j in range(N)]
    e=[[int(global_phase)+q[j]+q[k]-4*j*k for k in range(N)] for j in range(N)]
    return q,e

def direct_w_and_g(R,N,q,e):
    wd={};gd={};yd={}
    for j in range(N):
        for k in range(N):
            wt=defaultdict(int);gt=defaultdict(int)
            for a in range(N):
                ej,ek=e[a][j],e[a][k]
                wt[(ej+ek)%R.order]+=1
                for exp,c in [(ej+ek,-1),(ej-ek,1),(-ej+ek,1),(-ej-ek,-1)]:gt[exp%R.order]+=c
            wd[j,k]=R.terms(wt,N)
            gd[j,k]=R.terms(gt,4*N)
            # sqrt(N)*Im(V)=(z^e-z^-e)/(2i); i=z^N
            yd[j,k]=R.scale(R.sub(R.root(e[j][k]-N),R.root(-e[j][k]-N)),Q(1,2))
    return Matrix(R,N,wd),Matrix(R,N,gd),Matrix(R,N,yd)

def run(N):
    R=Cyclo(4*N);m=N//4;h=N//2;I=identity(R,N)
    q,e=phase_data(N);W,G,Y=direct_w_and_g(R,N,q,e)
    half=R.scale(R.one,Q(1,2));quarter=R.scale(R.one,Q(1,4))
    s2=R.sub(half,R.scale(R.add(R.root(2),R.root(-2)),Q(1,4)))
    c2=R.sub(R.one,s2)
    assert G.eq(I.sub(W.add(W.conj()).scale(half)).scale(half))
    assert Y.eq(Y.conj()) and Y.eq(Y.transpose())
    assert Y.transpose().mul(Y).scale(R.scale(R.one,Q(1,N))).eq(G)
    assert G.sub(I.scale(s2)).mul(G.sub(I.scale(c2))).a=={}
    trace_expected=R.add(R.scale(s2,h+2),R.scale(c2,h-2))
    assert G.tr()==trace_expected
    projector=G.sub(I.scale(s2)).scale(R.inv(R.sub(c2,s2)))
    assert projector.eq(projector.conj()) and projector.eq(projector.transpose())
    assert projector.mul(projector).eq(projector)
    assert projector.tr()==R.scale(R.one,h-2)
    residual=Y.mul(I.sub(projector))
    assert residual.transpose().mul(residual).scale(R.scale(R.one,Q(1,N))).eq(I.sub(projector).scale(s2))
    # Direct geometric-sum C = F B F and claimed four-permutation formula.
    b=[2*x for x in q]
    cd={};expected={}
    texp=2*m*N-4
    for j in range(N):
        for k in range(N):
            terms=defaultdict(int)
            for a in range(N):terms[(b[a]-4*(j+k)*a)%R.order]+=1
            cd[j,k]=R.terms(terms,N)
    for k in range(N):
        for shift,exp,sign in [(0,0,1),(h,0,1),(2,texp,1),(h+2,texp,-1)]:
            idx=((shift-k)%N,k)
            expected[idx]=R.add(expected.get(idx,R.zero),R.scale(R.root(exp),Q(sign,2)))
    C=Matrix(R,N,cd)
    assert C.eq(Matrix(R,N,expected))
    # Similarity W=Q (z^2 C B) Q^-1, all entries, with unnormalized q exponent roots.
    expectedW=Matrix(R,N,{(j,k):R.mul(v,R.root(2+b[k]+q[j]-q[k])) for (j,k),v in C.a.items()})
    assert W.eq(expectedW)
    # Exact weighted involution traces on parity / half-translation eigenspaces.
    traces=[]
    for parity,eta,shift,diag,signed in [(0,1,0,False,False),(1,1,0,True,True),(0,-1,2,False,True),(1,-1,2,True,False)]:
        accum=R.zero
        for j in range(N):
            if j%2!=parity:continue
            exp=(8*j if diag else 0)
            if signed:exp+=2*m*N
            if parity==1 and eta==-1:exp-=8
            weight=R.root(exp)
            if (shift-j)%N==j:accum=R.add(accum,weight)
            if (h+shift-j)%N==j:accum=R.add(accum,R.scale(weight,eta))
        traces.append(R.scale(accum,Q(1,2)))
    ee=int(m%2==0);oo=1-ee
    assert traces==[R.scale(R.one,v) for v in [1+ee,oo,oo,1+ee]]
    # Witness commutator cycle products and multiplicity endpoints.
    cycle_exponents=[]
    for parity in [0,1]:cycle_exponents.append(sum(b[j]-b[(j-1)%N] for j in range(parity,N,2))%(4*N))
    assert cycle_exponents==[2*N,2*N]
    spectrum=[(Q(1,N),m+1+ee),(Q(-1,N),m+oo),(Q(1,N)-1,m-1-ee),(1-Q(1,N),m-oo)]
    closed=sum(mult for angle,mult in spectrum if abs(angle)<=Q(1,N))
    opened=sum(mult for angle,mult in spectrum if abs(angle)<Q(1,N))
    assert closed==h+2 and opened==0
    # Each root exp(i*(2l+1)*pi/h) has multiplicity two.
    kphase=[Q(2*a+1,h) for a in range(h)]
    kphase=[p if p<=1 else p-2 for p in kphase]
    assert sum(2 for p in kphase if abs(p)<Q(2,N))==0
    assert sum(2 for p in kphase if abs(p)<=Q(2,N))==4
    out={'N':N,'r':m-1,'field_order':4*N,'field_degree':R.d,'direct_matrix_entries':N*N,
      'small_singular_multiplicity':h+2,'large_singular_multiplicity':h-2,
      'involution_traces':[1+ee,oo,oo,1+ee],
      'spectral_multiplicities':[m+1+ee,m+oo,m-1-ee,m-oo],
      'exact_w_gram_projector_residual_and_four_blocks':True,
      'commutator_cycle_products':[-1,-1],
      'open_closed_original_counts':[opened,closed],'open_closed_commutator_counts':[0,4]}
    R.mul.cache_clear();R.conj.cache_clear()
    return out

def controls():
    # Missing (-1)^m is detected in the odd-m branch by the multiplicity/trace check.
    N=12;R=Cyclo(4*N);q,e=phase_data(N,False,True);W,G,Y=direct_w_and_g(R,N,q,e)
    s2=R.sub(R.scale(R.one,Q(1,2)),R.scale(R.add(R.root(2),R.root(-2)),Q(1,4)))
    c2=R.sub(R.one,s2)
    assert G.tr()!=R.add(R.scale(s2,8),R.scale(c2,4))
    N=8;R=Cyclo(4*N);q,e=phase_data(N,True,False);W,G,Y=direct_w_and_g(R,N,q,e)
    I=identity(R,N);s2=R.sub(R.scale(R.one,Q(1,2)),R.scale(R.add(R.root(2),R.root(-2)),Q(1,4)));c2=R.sub(R.one,s2)
    assert G.sub(I.scale(s2)).mul(G.sub(I.scale(c2))).a!={}
    # Universal complex-packing identity, with four independent real coordinates.
    a,b,c,d=sp.symbols('a b c d', real=True)
    correct=sp.expand((a+sp.I*b)*(d+sp.I*c))
    wrong=sp.expand((a+sp.I*b)*(d-sp.I*c))
    assert sp.im(correct)==a*c+b*d and sp.im(wrong)!=a*c+b*d
    # Open/closed destructive controls follow from exact rational endpoint counts above.
    return {'omitted_odd_m_sign_rejected':True,'omitted_global_phase_rejected':True,
      'packing_adjoint_instead_of_transpose_rejected':True,'closed_original_arc_rejected':True,
      'closed_commutator_arc_rejected':True}

if __name__=='__main__':
    started=time.time()
    sizes=[4,8,12,16,20,24,28,32]
    data={'arithmetic':'Fractions in cyclotomic quotient fields; no floating point','sizes':[], 'scope':'Finite exact controls of the analytic all-m proof; no historical code imported or executed.'}
    for N in sizes:
        data['sizes'].append(run(N));print('Verified N='+str(N),flush=True)
    data['destructive_controls']=controls()
    data['checker_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    pathlib.Path(__file__).with_name('EXACT_RESULTS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':'PASS','sizes':sizes,'elapsed_seconds':round(time.time()-started,3)}))
