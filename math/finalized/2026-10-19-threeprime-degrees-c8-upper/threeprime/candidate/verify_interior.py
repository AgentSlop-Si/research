#!/usr/bin/env python3
"""Fresh exact controls for the order-3q interior proof; no historical imports."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json, time
ROOT=Path(__file__).resolve().parent

def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def divrem(a,b):
    a=list(a); b=trim(list(b)); out=[F(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        j=len(a)-len(b); c=a[-1]/b[-1]; out[j]=c
        for i,x in enumerate(b): a[i+j]-=c*x
        trim(a)
    return trim(out),trim(a)

def padd(a,b,sign=1):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=sign*x
    return trim(c)

def pmul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]+=x*y
    return trim(c)

PHI={}
def phi(n):
    if n not in PHI:
        p=[F(-1)]+[F(0)]*(n-1)+[F(1)]
        for d in range(1,n):
            if n%d==0:
                p,r=divrem(p,phi(d)); assert not any(r)
        PHI[n]=tuple(p)
    return PHI[n]

class Field:
    def __init__(self,n):
        self.n=n;self.p=phi(n);self.k=len(self.p)-1
        self.zero=(F(0),)*self.k;self.one=(F(1),)+(F(0),)*(self.k-1)
        self.roots=[self.reduce([F(0)]*j+[F(1)]) for j in range(n)]
    def reduce(self,x):
        x=list(x)
        for j in range(len(x)-1,self.k-1,-1):
            c=x[j]
            if c:
                for i in range(self.k):x[j-self.k+i]-=c*self.p[i]
        return tuple((x+[F(0)]*self.k)[:self.k])
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def sub(self,a,b):return tuple(x-y for x,y in zip(a,b))
    def scale(self,a,x):return tuple(y*x for y in a)
    def mul(self,a,b):
        if a==self.zero or b==self.zero:return self.zero
        if a==self.one:return b
        if b==self.one:return a
        return self.reduce(pmul(a,b))
    def inv(self,a):
        assert a!=self.zero
        r0,r1=list(self.p),trim(list(a));t0,t1=[F(0)],[F(1)]
        while any(r1):
            q,r=divrem(r0,r1);r0,r1=r1,r;t0,t1=t1,padd(t0,pmul(q,t1),-1)
        assert len(r0)==1
        return self.reduce([x/r0[0] for x in t0])
    def conj(self,a):
        out=self.zero
        for j,x in enumerate(a):
            if x:out=self.add(out,self.scale(self.roots[-j%self.n],x))
        return out

def divisor(n,d):
    return [[int(r//d==c%(n//d)) for c in range(n)] for r in range(n)]
CONNECTED=[[int(x) for x in s] for s in ['00110011','01010101','11001100','10101010','00110011','10101010','11001100','01010101']]

def gram(R,field,d):
    n=len(R); failures={'row':[],'column':[]}; zeros={'row':{},'column':{}}
    for which in failures:
        for r in range(n):
            for s in range(n):
                val=[F(0)]*field.k
                for c in range(n):
                    hit=R[r][c]*R[s][c] if which=='row' else R[c][r]*R[c][s]
                    if hit:
                        root=field.roots[(((r-s) if which=='row' else (s-r))*c)%n]
                        for j,x in enumerate(root):val[j]+=x
                target=field.scale(field.one,d) if r==s else field.zero
                if tuple(val)!=target:failures[which].append({'pair':[r,s],'value':[str(x) for x in val]})
                elif r!=s:
                    order=str(n//gcd(n,r-s));zeros[which][order]=zeros[which].get(order,0)+1
    return {'row_degrees':[sum(row) for row in R], 'column_degrees':[sum(R[r][c] for r in range(n)) for c in range(n)],'failures':failures,'offdiagonal_zeros_by_order':zeros}

def mask_record(label,R,d,positive):
    n=len(R);field=Field(n);audit=gram(R,field,d)
    assert all(x==d for x in audit['row_degrees']+audit['column_degrees'])
    if positive:assert not audit['failures']['row'] and not audit['failures']['column']
    else:assert audit['failures']['row'] and audit['failures']['column']
    return {'label':label,'n':n,'d':d,'R':R,'cyclotomic_polynomial':[str(x) for x in field.p],**audit}

def connected(R):
    n=len(R); seen={0};stack=[0]
    while stack:
        x=stack.pop();neigh=[n+c for c in range(n) if R[x][c]] if x<n else [r for r in range(n) if R[r][x-n]]
        for y in neigh:
            if y not in seen:seen.add(y);stack.append(y)
    return len(seen)==2*n

def matmul(A,B,K):
    nr,nk,nc=len(A),len(B),len(B[0]);out=[[K.zero for _ in range(nc)] for _ in range(nr)]
    for i in range(nr):
        for j in range(nk):
            if A[i][j]!=K.zero:
                for k in range(nc):
                    if B[j][k]!=K.zero:out[i][k]=K.add(out[i][k],K.mul(A[i][j],B[j][k]))
    return out

def adj(A,K):return [[K.conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def inverse(A,K):
    n=len(A); M=[list(A[i])+[K.one if i==j else K.zero for j in range(n)] for i in range(n)]
    for j in range(n):
        p=next(i for i in range(j,n) if M[i][j]!=K.zero);M[j],M[p]=M[p],M[j]
        c=K.inv(M[j][j]);M[j]=[K.mul(x,c) for x in M[j]]
        for i in range(n):
            if i!=j and M[i][j]!=K.zero:
                c=M[i][j];M[i]=[K.sub(x,K.mul(c,y)) for x,y in zip(M[i],M[j])]
    return [row[n:] for row in M]
def diagonal_check(A,K,val):
    n=len(A);assert all(A[i][j]==(K.scale(K.one,val) if i==j else K.zero) for i in range(n) for j in range(n))
def encode(A):return [[[str(x) for x in z] for z in row] for row in A]
def original_witness(R,d):
    n=len(R); K=Field(n);H=[[K.roots[(r*c)%n] for c in range(n)] for r in range(n)]
    A=[[K.zero if R[r][c] else H[r][c] for c in range(n)] for r in range(n)]
    B=[[K.scale(x,F(1,n-d)) for x in row] for row in adj(A,K)]
    M=inverse(B,K)
    diagonal_check(matmul(M,B,K),K,1);diagonal_check(matmul(B,M,K),K,1)
    assert all(sum(x!=K.zero for x in row)==n-d for row in B)
    assert all(sum(B[r][c]!=K.zero for r in range(n))==n-d for c in range(n))
    E=[[K.sub(M[r][c],H[r][c]) for c in range(n)] for r in range(n)]
    diagonal_check(matmul(E,adj(E,K),K),K,d);diagonal_check(matmul(adj(E,K),E,K),K,d)
    return {'n':n,'d':d,'R':R,'inverse_support_budget':n-d,'phi':[str(x) for x in K.p],'B_tilde':encode(B),'M_tilde':encode(M),'E':encode(E),'both_inverse_products':'identity','both_error_grams':f'{d} I','normalization':'M=M_tilde/sqrt(N); M^(-1)=sqrt(N) B_tilde; squared error=d/N'}

def local_checks():
    records={};families={};tested=0
    for n in range(1,12):
        good=[]
        for masks in combinations_with_replacement(range(8),n):
            tested+=1
            if all((masks[i]&masks[j]).bit_count()==1 for i in range(n) for j in range(i)):
                union=0;common=7
                for z in masks:union|=z;common&=z
                if n>=4:
                    assert common.bit_count()==1
                    assert sum(z.bit_count() for z in masks)==n+union.bit_count()-1
                good.append((masks,union,common))
        families[n]=good;records[str(n)]=len(good)
    split=0;singleton_nonbaseline=0
    for q in [5,7,11]:
        for n in range(1,q):
            m=q-n
            for A,u,ca in families[n]:
                for B,v,cb in families[m]:
                    if u&v:continue
                    split+=1;counts=[sum((z>>j)&1 for z in A+B) for j in range(3)]
                    assert sum(counts)<=q+1
                    if sum(counts)==q+1:
                        assert sorted(counts)==sorted([n,m,1])
                        if n==1 and A[0].bit_count()!=1:singleton_nonbaseline+=1
                        if m==1 and B[0].bit_count()!=1:singleton_nonbaseline+=1
    return {'multisets_tested':tested,'pairwise_one_families_by_size':records,'split_fiber_configurations':split,'saturated_singleton_nonbaseline_cases':singleton_nonbaseline}

def dump(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')

def main():
    start=time.time(); positives=[];negatives=[]
    for q in [5,7,11,13]:
        n=3*q
        for d in [1,3,q,n]:positives.append(mask_record(f'divisor {n},{d}',divisor(n,d),d,True))
    positives.append(mask_record('retained connected (8,4)',CONNECTED,4,True)); assert connected(CONNECTED)
    lift=[[CONNECTED[r%8][c%8] for c in range(24)] for r in range(24)]
    positives.append(mask_record('retained odd CRT lift (24,12)',lift,12,True));assert connected(lift)
    print('Positive controls passed:',len(positives),flush=True)
    for q in [5,7,11,13]:
        n=3*q;R=[]
        for r in range(n):
            a,b=r%3,r%q;baseline=a if b else (a+1)%3
            R.append([int(c%3==baseline or (c%3==(a+2)%3 and c%q==b)) for c in range(n)])
        rec=mask_record(f'all-split q+1 regular near-mask, q={q}',R,q+1,False)
        assert all((r['pair'][0]-r['pair'][1])%3!=0 for r in rec['failures']['row'])
        negatives.append(rec)
        R=[[int(r%3!=c%3) for c in range(n)] for r in range(n)]
        rec=mask_record(f'endpoint order-three obstruction, q={q}',R,2*q,False)
        assert len(rec['failures']['row'])==6*q and len(rec['failures']['column'])==6*q
        assert all(n//gcd(n,x['pair'][0]-x['pair'][1])==3 for x in rec['failures']['row']+rec['failures']['column'])
        negatives.append(rec)
    R=divisor(15,5)
    R[0][0],R[0][1],R[5][0],R[5][1]=0,1,1,0
    negatives.append(mask_record('degree-preserving switched divisor control',R,5,False))
    print('Negative controls passed:',len(negatives),flush=True)
    crt=0
    for q in [5,7,11,13,17]:
        n=3*q;e3=q*pow(q,-1,3);eq=3*pow(3,-1,q)
        for h in range(1,n):
            if gcd(h,n)>1:continue
            for r in range(n):
                for c in range(n):
                    assert (h*r*c-h*((r%3)*(c%3)*e3+(r%q)*(c%q)*eq))%n==0;crt+=1
    local=local_checks();print('Local incidence and CRT controls passed',flush=True)
    dump('POSITIVE_CONTROLS.json',positives);dump('NEGATIVE_CONTROLS.json',negatives);dump('LOCAL_CONTROLS.json',local)
    witnesses=[]
    for R,d in [(divisor(15,3),3),(divisor(15,5),5),(CONNECTED,4)]:
        witnesses.append(original_witness(R,d));print('Original inverse witness passed:',len(R),d,flush=True)
    dump('ORIGINAL_MODEL_CONTROLS.json',witnesses)
    all_masks=positives+negatives
    result={'all_passed':True,'positive_masks':len(positives),'negative_masks':len(negatives),'original_inverse_witnesses':len(witnesses),'row_gram_entries':sum(x['n']**2 for x in all_masks),'column_gram_entries':sum(x['n']**2 for x in all_masks),'inverse_product_entries':sum(2*x['n']**2 for x in witnesses),'error_gram_entries':sum(2*x['n']**2 for x in witnesses),'crt_congruences':crt,'local_controls':local,'elapsed_seconds':time.time()-start,'historical_code_imported_or_executed':False,'full_mask_census':False,'external_writes':False}
    dump('RESULTS.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
