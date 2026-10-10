"""Fresh standard-library integer/cyclotomic verification of four-chain family."""
from pathlib import Path
import json

class PrimeRing:
    def __init__(self,p):
        self.p=p; self.d=p-1;self.zero=(0,)*self.d;self.one=(1,)+(0,)*(self.d-1)
        self.powers=[tuple(int(i==k) for i in range(self.d)) for k in range(self.d)]+[(-1,)*self.d]
    def z(self,k):return self.powers[k%self.p]
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def sub(self,a,b):return self.add(a,self.neg(b))
    def scalar(self,a,k):return tuple(x*k for x in a)
    def mul(self,a,b):
        c=[0]*(2*self.d-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:c[i+j]+=x*y
        for k in range(len(c)-1,self.d-1,-1):
            for j in range(self.d):c[k-self.d+j]-=c[k]
        return tuple(c[:self.d])
    def sum(self,xs):
        s=self.zero
        for x in xs:s=self.add(s,x)
        return s
    def conj(self,a):return self.sum(self.scalar(self.z(-k),v) for k,v in enumerate(a))

def verify(p):
    K=PrimeRing(p);z=K.z;mul=K.mul;add=K.add;sub=K.sub;Z=K.zero;O=K.one
    ell=K.sum((O,z(1),z(-1)))
    assert ell!=Z and ell!=O
    F=[[z(i*t) for t in range(p)] for i in range(p)]
    C=[[O if i==j else Z for j in range(p)] for i in range(p)]
    C[1][0]=O;C[2][1]=ell;C[p-1][2]=O
    R=[list(row) for row in F]
    for t in range(p):
        R[1][t]=sub(z(t),O)
        R[2][t]=sub(z(2*t),mul(ell,R[1][t]))
        R[p-1][t]=sub(z(-t),R[2][t])
    zeros=[[i,t] for i in range(p) for t in range(p) if R[i][t]==Z]
    assert zeros==[[1,0],[p-1,0],[p-1,1],[p-1,p-1]]
    for i in range(p):
        for t in range(p):assert K.sum(mul(C[i][v],R[v][t]) for v in range(p))==F[i][t]
    inv2=(p+1)//2
    Bs=[]
    for t in range(p):
        Bs.append([[mul(z(-inv2*t*t),R[v][t]) if u==t else Z for u in range(p)] for v in range(p)])
    raw=[[Z for j in range(p)] for i in range(p)]
    count=0
    for t in range(p):
        for i in range(p):
            left=K.sum(mul(C[i][v],Bs[t][v][t]) for v in range(p))
            for j in range(p):
                actual=mul(left,F[t][j]);target=z(-inv2*t*t+(i+j)*t)
                assert actual==target
                raw[i][j]=add(raw[i][j],actual);count+=1
    G=K.sum(z(-inv2*t*t) for t in range(p))
    assert mul(G,K.conj(G))==K.scalar(O,p)
    for i in range(p):
        for j in range(p):
            assert mul(z(-inv2*(i*i+j*j)),raw[i][j])==mul(G,F[i][j])
    for i in range(p):
        for j in range(p):assert F[i][(j+1)%p]==mul(z(i),F[i][j])
    nC=sum(x!=Z for row in C for x in row)
    middle=sum(x!=Z for B in Bs for row in B for x in row)
    assert nC==p+3 and middle==p*p-4
    return {'p':p,'C_nonzero':nC,'A_nonzero':p*p,'colored_middle_nonzero':middle,'total':p*p+nC+middle,'strict_baseline':2*p*p+p,'R_zero_positions':zeros,'fiber_entries_checked':count,'corrected_entries_checked':p*p,'gauss_norm_checked':p,'ell':ell}

results=[verify(p) for p in (5,7,11,13,17)]
out={'status':'passed_exact','source_programs_executed_or_imported':False,'arithmetic':'Integer arithmetic in Z[zeta_p] with Phi_p=sum_{k=0}^{p-1} x^k','cases':results,'fiber_entries_total':sum(x['fiber_entries_checked'] for x in results),'corrected_entries_total':sum(x['corrected_entries_checked'] for x in results)}
Path(__file__).with_name('INDEPENDENT_UNIFORM_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
