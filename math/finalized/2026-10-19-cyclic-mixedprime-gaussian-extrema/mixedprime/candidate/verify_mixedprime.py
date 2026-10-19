#!/usr/bin/env python3
"""New exact controls for the 2q theorem. No historical imports or executions."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import gcd
import json

ROOT=Path(__file__).resolve().parent


def trim(a):
    a=list(a)
    while a and a[-1]==0: a.pop()
    return a


def divrem(a,b):
    a=trim(a); b=trim(b)
    assert b
    quotient=[F(0)]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        j=len(a)-len(b); t=F(a[-1])/b[-1]; quotient[j]=t
        for i,x in enumerate(b): a[i+j]-=t*x
        a=trim(a)
    return trim(quotient),a


CYCLO={1:[-1,1]}

def cyclo(n):
    if n not in CYCLO:
        a=[-1]+[0]*(n-1)+[1]
        for d in range(1,n):
            if n%d==0:
                a,r=divrem(a,cyclo(d)); assert not r
        assert all(F(x).denominator==1 for x in a)
        CYCLO[n]=[int(x) for x in a]
    return CYCLO[n]


def remainder(n,coeff):
    _,r=divrem(coeff,cyclo(n))
    return tuple(r+[F(0)]*(len(cyclo(n))-1-len(r)))


def zero_sum(n,terms):
    hist=[0]*n
    for exponent,coefficient in terms: hist[exponent%n]+=coefficient
    return not any(remainder(n,hist))


COUNTERS={'row_gram_entries':0,'column_gram_entries':0,'inverse_products':0,'error_grams':0}

def grams(n,R,d):
    assert len(R)==n and all(len(row)==n for row in R)
    assert all(v in (0,1) for row in R for v in row)
    failures=[]
    for r in range(n):
        for s in range(n):
            COUNTERS['row_gram_entries']+=1
            h=[0]*n
            for c in range(n): h[((r-s)*c)%n]+=R[r][c]*R[s][c]
            if r==s: h[0]-=d
            residual=remainder(n,h)
            if any(residual): failures.append({'gram':'row','i':r,'j':s,'residual':list(map(str,residual))})
    for c in range(n):
        for e in range(n):
            COUNTERS['column_gram_entries']+=1
            h=[0]*n
            for r in range(n): h[(r*(e-c))%n]+=R[r][c]*R[r][e]
            if c==e: h[0]-=d
            residual=remainder(n,h)
            if any(residual): failures.append({'gram':'column','i':c,'j':e,'residual':list(map(str,residual))})
    return failures


def divisor_mask(n,d):
    assert n%d==0
    return [[int(r//d==c%(n//d)) for c in range(n)] for r in range(n)]


CONNECTED=[[int(v) for v in s] for s in [
    '00110011','01010101','11001100','10101010',
    '00110011','10101010','11001100','01010101']]


def components(R):
    n=len(R); unseen=set(range(2*n)); out=[]
    while unseen:
        todo=[min(unseen)]; unseen.remove(todo[0]); found=[]
        while todo:
            v=todo.pop(); found.append(v)
            neighbors=([n+c for c in range(n) if R[v][c]] if v<n
                       else [r for r in range(n) if R[r][v-n]])
            for w in neighbors:
                if w in unseen: unseen.remove(w); todo.append(w)
        out.append(sorted(found))
    return out


class Field:
    def __init__(self,n):
        self.n=n; self.phi=cyclo(n); self.k=len(self.phi)-1
        self.zero=(F(0),)*self.k; self.one=(F(1),)+(F(0),)*(self.k-1)
        self.roots=[remainder(n,[0]*j+[1]) for j in range(n)]
    def plus(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def minus(self,a,b): return tuple(x-y for x,y in zip(a,b))
    def times_scalar(self,a,t): return tuple(x*t for x in a)
    def times(self,a,b):
        c=[F(0)]*(2*self.k-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y: c[i+j]+=x*y
        # Monic reduction is integral in the coefficient basis.
        for j in range(len(c)-1,self.k-1,-1):
            v=c[j]
            if v:
                for t in range(self.k): c[j-self.k+t]-=v*self.phi[t]
        return tuple(c[:self.k])
    def power(self,j): return self.roots[j%self.n]
    def bar(self,a):
        z=self.zero
        for j,x in enumerate(a):
            if x: z=self.plus(z,self.times_scalar(self.power(-j),x))
        return z
    def reciprocal(self,a):
        assert a!=self.zero
        # Solve the multiplication operator in the rational coefficient basis.
        cols=[self.times(a,self.power(j)) for j in range(self.k)]
        work=[[cols[j][i] for j in range(self.k)]+[F(i==0)] for i in range(self.k)]
        for j in range(self.k):
            pivot=next(i for i in range(j,self.k) if work[i][j])
            work[j],work[pivot]=work[pivot],work[j]
            t=work[j][j]; work[j]=[v/t for v in work[j]]
            for i in range(self.k):
                if i!=j and work[i][j]:
                    t=work[i][j]; work[i]=[x-t*y for x,y in zip(work[i],work[j])]
        out=tuple(work[i][-1] for i in range(self.k))
        assert self.times(a,out)==self.one
        return out
    def identity(self,n,scale=1):
        return [[self.times_scalar(self.one,F(scale)) if i==j else self.zero for j in range(n)] for i in range(n)]
    def adjoint(self,A): return [[self.bar(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
    def matmul(self,A,B):
        out=[]
        for row in A:
            rr=[]
            for j in range(len(B[0])):
                total=self.zero
                for t,x in enumerate(row):
                    if x!=self.zero and B[t][j]!=self.zero: total=self.plus(total,self.times(x,B[t][j]))
                rr.append(total)
            out.append(rr)
        return out
    def matrix_inverse(self,A):
        n=len(A); I=self.identity(n); work=[A[i][:]+I[i] for i in range(n)]
        for j in range(n):
            pivot=next(i for i in range(j,n) if work[i][j]!=self.zero)
            work[j],work[pivot]=work[pivot],work[j]
            t=self.reciprocal(work[j][j]); work[j]=[self.times(t,v) for v in work[j]]
            for i in range(n):
                if i!=j and work[i][j]!=self.zero:
                    t=work[i][j]; work[i]=[self.minus(x,self.times(t,y)) for x,y in zip(work[i],work[j])]
        assert [row[:n] for row in work]==I
        return [row[n:] for row in work]


def original_model(n,d,R,label):
    K=Field(n)
    H=[[K.power(r*c) for c in range(n)] for r in range(n)]
    A=[[K.zero if R[r][c] else H[r][c] for c in range(n)] for r in range(n)]
    B=[[K.times_scalar(x,F(1,n-d)) for x in row] for row in K.adjoint(A)]
    M=K.matrix_inverse(B)
    assert K.matmul(B,M)==K.matmul(M,B)==K.identity(n)
    COUNTERS['inverse_products']+=2
    row_counts=[sum(x!=K.zero for x in row) for row in B]
    col_counts=[sum(B[r][c]!=K.zero for r in range(n)) for c in range(n)]
    assert row_counts==col_counts==[n-d]*n
    E=[[K.minus(M[r][c],H[r][c]) for c in range(n)] for r in range(n)]
    assert K.matmul(K.adjoint(E),E)==K.matmul(E,K.adjoint(E))==K.identity(n,d)
    COUNTERS['error_grams']+=2
    dump=lambda T:[[[str(x) for x in el] for el in row] for row in T]
    return {'label':label,'N':n,'d':d,'field_modulus':K.phi,
            'normalization':'M=M_tilde/sqrt(N), M inverse=sqrt(N) B_tilde',
            'M_tilde':dump(M),'B_tilde':dump(B),'error_unnormalized':dump(E),
            'inverse_row_counts':row_counts,'inverse_column_counts':col_counts,
            'both_inverse_products':True,'both_error_grams':f'{d} I_{n}',
            'normalized_squared_spectral_error':str(F(d,n))}


def upper_candidate(q):
    n=2*q; R=[[0]*n for _ in range(n)]
    for a in range(q):
        for c in range(q): R[2*a][c]=1; R[2*a+1][c+q]=1
        R[2*a][a+q]=1; R[2*a+1][a]=1
    return R


def check_upper_candidate(q):
    n=2*q; R=upper_candidate(q)
    assert all(sum(row)==q+1 for row in R)
    assert all(sum(R[r][c] for r in range(n))==q+1 for c in range(n))
    same_parity=[]
    for parity in (0,1):
        for r in range(parity,n,2):
            for s in range(r+2,n,2):
                counts=[sum(R[r][c]*R[s][c] for c in (t,t+q)) for t in range(q)]
                assert counts==[1]*q
                assert zero_sum(n,(((r-s)*c,R[r][c]*R[s][c]) for c in range(n)))
                same_parity.append([r,s])
    fail=grams(n,R,q+1)
    primitive=next(x for x in fail if x['gram']=='row' and gcd(x['i']-x['j'],n)==1)
    r,s=primitive['i'],primitive['j']
    overlap=[c for c in range(n) if R[r][c]*R[s][c]]
    assert len(overlap)==2 and (overlap[0]-overlap[1])%q!=0
    return {'q':q,'N':n,'d':q+1,'R':R,'row_and_column_degrees':q+1,
            'same_parity_pairs_passed':len(same_parity),'primitive_failure':primitive,
            'failing_pair_overlap':overlap,'full_gram_failure_count':len(fail)}


def check_general_upper(p,q):
    n=p*q; d=(p-1)*q+1
    R=[[1]*n for _ in range(n)]
    for a in range(p):
        for b in range(q):
            r=a+p*b
            for t in range(q): R[r][t+q*a]=int(t==b)
    assert all(sum(row)==d for row in R)
    assert all(sum(row[c] for row in R)==d for c in range(n))
    same_pairs=0
    for a in range(p):
        for b in range(q):
            for e in range(b):
                r=a+p*b; s=a+p*e
                counts=[sum(R[r][t+q*k]*R[s][t+q*k] for k in range(p)) for t in range(q)]
                assert counts==[p-1]*q
                assert zero_sum(n,(((r-s)*c,R[r][c]*R[s][c]) for c in range(n)))
                same_pairs+=1
    fail=grams(n,R,d)
    primitive=next(x for x in fail if x['gram']=='row' and gcd(x['i']-x['j'],n)==1)
    r,s=primitive['i'],primitive['j']
    counts=[sum(R[r][t+q*k]*R[s][t+q*k] for k in range(p)) for t in range(q)]
    assert min(counts)==p-2 and max(counts)>p-2
    return {'p':p,'q':q,'N':n,'d':d,'R':R,'all_row_column_degrees':d,
            'same_group_pairs_passed':same_pairs,'primitive_failure':primitive,
            'primitive_overlap_fiber_counts':counts,'full_gram_failure_count':len(fail)}


def main():
    positives=[]
    for n in [6,10,14,22,26,34,15,21,35]:
        for d in range(1,n+1):
            if n%d==0:
                R=divisor_mask(n,d); assert not grams(n,R,d)
                positives.append({'label':'divisor','N':n,'d':d,'R':R,'both_grams':True})
    assert not grams(8,CONNECTED,4)
    comp=components(CONNECTED); assert len(comp)==1 and len(comp[0])==16
    positives.append({'label':'accepted_connected','N':8,'d':4,'R':CONNECTED,'both_grams':True,'components':comp})
    lift=[[CONNECTED[r%8][c%8] for c in range(24)] for r in range(24)]
    assert not grams(24,lift,12)
    lift_components=components(lift); assert len(lift_components)==1
    positives.append({'label':'accepted_connected_odd_CRT_lift','N':24,'d':12,'R':lift,'both_grams':True,'components':lift_components})
    upper=[check_upper_candidate(q) for q in [3,5,7,11,13]]
    general_upper=[check_general_upper(p,q) for p,q in [(3,5),(3,7),(5,7)]]
    # Exhaustively test only the elementary length-two vector lemma, not masks.
    vector_lemma_cases=0; vector_lemma_accepted=0
    for count in [3,4,5,6]:
        for codes in product(range(4),repeat=count):
            vector_lemma_cases+=1
            vv=[(c//2,c%2) for c in codes]
            if not all(sum(x*y for x,y in zip(vv[i],vv[j]))==1 for i in range(count) for j in range(i)):
                continue
            vector_lemma_accepted+=1
            baseline=[t for t in (0,1) if all(v[t] for v in vv)]
            assert len(baseline)==1
            assert sum(v[1-baseline[0]] for v in vv)<=1
    base=divisor_mask(6,2); switched=None
    for r in range(6):
        for s in range(r+1,6):
            for c in range(6):
                for e in range(c+1,6):
                    if [base[r][c],base[r][e],base[s][c],base[s][e]]==[1,0,0,1]:
                        corrupt=[row[:] for row in base]
                        for i,j in [(r,c),(r,e),(s,c),(s,e)]: corrupt[i][j]^=1
                        fail=grams(6,corrupt,2)
                        if fail:
                            switched={'N':6,'d':2,'R':corrupt,'switch':[r,s,c,e],'failure':fail[0]}
                            break
                if switched: break
            if switched: break
        if switched: break
    assert switched and all(sum(row)==2 for row in switched['R'])
    assert all(sum(row[c] for row in switched['R'])==2 for c in range(6))
    weighted_grid=[[1,2,2],[2,3,3]]
    hist=[0]*6
    for a in range(2):
        for b in range(3): hist[(3*a+2*b)%6]=weighted_grid[a][b]
    assert hist==[1,3,2,2,2,3] and not any(remainder(6,hist))
    assert all(weighted_grid[0][b]!=weighted_grid[1][b] for b in range(3))
    assert all(len(set(row))>1 for row in weighted_grid)
    original=[]
    for n in [6,10]:
        for d in [1,2,n//2]: original.append(original_model(n,d,divisor_mask(n,d),'mixed_prime_divisor'))
    original.append(original_model(8,4,CONNECTED,'accepted_connected'))
    negative={'q_plus_one_local_countercontrols':upper,'general_upper_countercontrols':general_upper,'degree_preserving_switch':switched,
              'weighted_coefficient_obstruction':{'N':6,'grid':weighted_grid,'coefficient_histogram':hist,
                'exact_residual':list(map(str,remainder(6,hist))),
                'warning':'A coefficient-level obstruction only; not an admissible square two-Gram mask.'}}
    result={'status':'proof candidate pending independent review','all_checks_passed':True,
            'main_theorem':'For every odd prime q, N=2q has equality-mask weights exactly 1,2,q,2q.',
            'supplement':'For primes p<q and N=pq, weights d<q are exactly 1,p; (p-1)q<d<pq is impossible.',
            'positive_mask_controls':len(positives),'original_model_controls':len(original),
            'upper_branch_countercontrols':len(upper),'general_upper_countercontrols':len(general_upper),'local_binary_vector_lemma_cases':vector_lemma_cases,
            'local_binary_vector_lemma_accepted':vector_lemma_accepted,'counters':COUNTERS,
            'historical_code_executed':False,'external_writes':False,
            'proof_is_not_a_census':True,'full_mixed_prime_gate_closed':False}
    for name,obj in [('RESULTS.json',result),('POSITIVE_MASKS.json',positives),('NEGATIVE_CONTROLS.json',negative),('ORIGINAL_MODEL_CONTROLS.json',original)]:
        (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
