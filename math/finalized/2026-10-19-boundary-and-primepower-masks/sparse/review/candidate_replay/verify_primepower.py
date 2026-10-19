#!/usr/bin/env python3
"""Fresh exact checks for weighted prime-power Fourier-mask descent.
No imports of historical programs; standard library and local outputs only.
"""
from collections import defaultdict, deque
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def reduced(hist, p, a):
    """Coefficients in Q[X]/Phi_(p^a), in its usual monomial basis."""
    if a == 0:
        return (sum(hist),)
    L = p**a
    n = L//p
    assert len(hist) == L
    out = list(hist[:(p-1)*n])
    for u in range(n):
        b = hist[u+(p-1)*n]
        for q in range(p-1):
            out[u+q*n] -= b
    return tuple(out)


def vanish(terms, p, a):
    L = p**a
    h = [0]*L
    for exponent, coefficient in terms:
        h[exponent % L] += coefficient
    return not any(reduced(h, p, a))


def validate(B):
    p,a,d = B['p'],B['a'],B['d']
    x,y,k,R = B['x'],B['y'],B['k'],B['R']
    m = len(x)
    assert m > 0 and len(y) == len(k) == len(R) == m
    L = p**a
    assert all(0 <= z < L for z in x+y)
    assert all(isinstance(v,int) and v >= 0 for v in k)
    assert all(len(row)==m and all(v in (0,1) for v in row) for row in R)
    # Whole row Gram. Positive row factors may be omitted only off diagonal.
    for i in range(m):
        assert p**k[i]*sum(R[i]) == d, ('row diagonal',i)
        for l in range(m):
            if i != l:
                assert vanish((( (x[i]-x[l])*y[j], R[i][j]*R[l][j])
                               for j in range(m)),p,a), ('row off diagonal',i,l)
    # Whole column Gram, including all squared row weights.
    for j in range(m):
        assert sum(p**k[i]*R[i][j] for i in range(m)) == d, ('column diagonal',j)
        for l in range(m):
            if j != l:
                assert vanish(((x[i]*(y[l]-y[j]), p**k[i]*R[i][j]*R[i][l])
                               for i in range(m)),p,a), ('column off diagonal',j,l)
    return 2*m*m


def split(B):
    """Construct exactly the lower-level blocks in the written proof."""
    p,a,d = B['p'],B['a'],B['d']
    assert a > 0
    n = p**(a-1)
    x,y,k,R = B['x'],B['y'],B['k'],B['R']
    m = len(x)
    supports = [tuple(j for j in range(m) if R[i][j]) for i in range(m)]
    pure = []
    mixed = defaultdict(list)
    for i,S in enumerate(supports):
        residues = {y[j]%p for j in S}
        assert residues
        if len(residues)==1:
            pure.append((i,next(iter(residues))))
        else:
            mixed[(x[i]%n,S)].append(i)
    rows = [[] for _ in range(p)]
    for i,t in pure:
        assert all((x[i]*y[j]-x[i]*t-p*(x[i]%n)*((y[j]-t)//p))%(p**a)==0 for j in supports[i])
        rows[t].append((x[i]%n,k[i],supports[i],{'kind':'pure','input_rows':[i]}))
    for (u,S), inds in mixed.items():
        assert len(inds)==p
        assert {x[i]//n for i in inds} == set(range(p))
        assert len({k[i] for i in inds}) == 1
        assert all(supports[i]==S for i in inds)
        counts = [sum(y[j]%p==t for j in S) for t in range(p)]
        assert len(set(counts)) == 1 and counts[0]>0
        for t in range(p):
            # Direct exact p-point transform formula before row dephasing.
            for j in S:
                terms=[(x[i]*y[j]-n*t*(x[i]//n),1) for i in inds]
                if y[j]%p==t:
                    terms.append((u*y[j],-p))
                assert vanish(terms,p,a)
                if y[j]%p==t:
                    assert (u*y[j]-u*t-p*u*((y[j]-t)//p))%(p**a)==0
            rows[t].append((u,k[inds[0]]+1,tuple(j for j in S if y[j]%p==t),
                            {'kind':'mixed','input_rows':sorted(inds)}))
    assert sum(map(len,rows))==m
    children=[]
    events=[]
    for t in range(p):
        cols = [j for j in range(m) if y[j]%p==t]
        assert len(rows[t])==len(cols), ('square block count',t,len(rows[t]),len(cols))
        if not cols:
            continue
        child = {'p':p,'a':a-1,'d':d,
                 'x':[r[0] for r in rows[t]],
                 'y':[(y[j]-t)//p for j in cols],
                 'k':[r[1] for r in rows[t]],
                 'R':[[int(j in r[2]) for j in cols] for r in rows[t]]}
        children.append(child)
        events.append({'residue':t,'size':len(cols),'input_columns':cols,
                       'row_origins':[r[3] for r in rows[t]],
                       'new_weight_exponents':child['k']})
    return children,{'level':a,'size':m,'pure_rows':len(pure),
                     'matched_tuples':len(mixed),'children':events}


def descend(B, detailed=False):
    queue = deque([(B,'root')])
    entries=0
    records=[]
    terminals=[]
    while queue:
        cur,path=queue.popleft()
        entries += validate(cur)
        if cur['a']==0:
            assert all(sum(row)==1 for row in cur['R'])
            assert all(sum(row[j] for row in cur['R'])==1 for j in range(len(cur['y'])))
            assert all(cur['p']**z==cur['d'] for z in cur['k'])
            terminals += cur['k']
            record={'path':path,'level':0,'size':len(cur['x']),'terminal_weights':cur['k']}
        else:
            children,record=split(cur)
            record['path']=path
            for h,ch in enumerate(children):
                queue.append((ch,path+'/'+str(h)))
        if detailed:
            record['matrix_state']=cur
        records.append(record)
    assert len(terminals)==len(B['x'])
    assert len(set(terminals))==1
    return {'verified_gram_entries':entries,'terminal_exponent':terminals[0],
            'terminal_rows':len(terminals),'records':records}


def divisor_mask(p,a,b):
    N=p**a
    d=p**b
    m=N//d
    R=[[int(r//d==c%m) for c in range(N)] for r in range(N)]
    return {'p':p,'a':a,'d':d,'x':list(range(N)),'y':list(range(N)),
            'k':[0]*N,'R':R}


CONNECTED = [[int(c) for c in s] for s in
             ['00110011','01010101','11001100','10101010',
              '00110011','10101010','11001100','01010101']]


def connected_support(R):
    n=len(R)
    seen={0}
    todo=[0]
    while todo:
        v=todo.pop()
        neighbors=[n+j for j in range(n) if R[v][j]] if v<n else [i for i in range(n) if R[i][v-n]]
        for w in neighbors:
            if w not in seen:
                seen.add(w); todo.append(w)
    return len(seen)==2*n


def expect_rejection(B):
    try:
        validate(B)
    except AssertionError:
        return True
    raise AssertionError('corruption incorrectly accepted')


class Field:
    """Q[z]/(z^4+1), used only for the original connected inverse witness."""
    q=4
    zero=(Q(0),)*4
    one=(Q(1),Q(0),Q(0),Q(0))
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def neg(self,a): return tuple(-x for x in a)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def scale(self,a,t): return tuple(t*x for x in a)
    def mul(self,a,b):
        c=[Q(0)]*4
        for i in range(4):
            for j in range(4):
                e=i+j
                c[e%4] += a[i]*b[j]*(1 if e<4 else -1)
        return tuple(c)
    def power(self,e):
        e%=8
        out=[Q(0)]*4
        out[e%4]=Q(1 if e<4 else -1)
        return tuple(out)
    def conj(self,a):
        c=self.zero
        for i,v in enumerate(a): c=self.add(c,self.scale(self.power(-i),v))
        return c
    def inv(self,a):
        cols=[self.mul(a,self.power(j)) for j in range(4)]
        T=[[cols[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
        for j in range(4):
            i=next(i for i in range(j,4) if T[i][j])
            T[j],T[i]=T[i],T[j]
            t=T[j][j]; T[j]=[v/t for v in T[j]]
            for i in range(4):
                if i!=j:
                    t=T[i][j]
                    T[i]=[x-t*y for x,y in zip(T[i],T[j])]
        b=tuple(T[i][-1] for i in range(4))
        assert self.mul(a,b)==self.one
        return b


def inverse_witness():
    K=Field(); n=8
    def adj(A): return [[K.conj(A[j][i]) for j in range(n)] for i in range(n)]
    def mul(A,B):
        out=[]
        for i in range(n):
            row=[]
            for j in range(n):
                s=K.zero
                for t in range(n): s=K.add(s,K.mul(A[i][t],B[t][j]))
                row.append(s)
            out.append(row)
        return out
    def eye(scale=1): return [[K.scale(K.one,Q(scale)) if i==j else K.zero for j in range(n)] for i in range(n)]
    def inv(A):
        I=eye()
        T=[A[i][:]+I[i][:] for i in range(n)]
        for j in range(n):
            i=next(i for i in range(j,n) if T[i][j]!=K.zero)
            T[j],T[i]=T[i],T[j]
            z=K.inv(T[j][j]); T[j]=[K.mul(z,v) for v in T[j]]
            for i in range(n):
                if i!=j:
                    z=T[i][j]
                    T[i]=[K.sub(x,K.mul(z,y)) for x,y in zip(T[i],T[j])]
        return [row[n:] for row in T]
    H=[[K.power(i*j) for j in range(n)] for i in range(n)]
    A=[[K.zero if CONNECTED[i][j] else H[i][j] for j in range(n)] for i in range(n)]
    B=[[K.scale(v,Q(1,4)) for v in row] for row in adj(A)]
    M=inv(B)
    assert mul(M,B)==mul(B,M)==eye()
    assert all(sum(v!=K.zero for v in row)==4 for row in B)
    assert all(sum(B[i][j]!=K.zero for i in range(n))==4 for j in range(n))
    E=[[K.sub(M[i][j],H[i][j]) for j in range(n)] for i in range(n)]
    assert mul(E,adj(E))==mul(adj(E),E)==eye(4)
    def dump(A): return [[[str(v) for v in el] for el in row] for row in A]
    return {'field':'Q[z]/(z^4+1), primitive z of order 8',
            'normalization':'M = M_tilde/sqrt(8); M inverse = sqrt(8) B_tilde',
            'M_tilde':dump(M),'B_tilde':dump(B),'error_unnormalized':dump(E),
            'inverse_row_counts':[4]*8,'inverse_column_counts':[4]*8,
            'normalized_squared_spectral_error':'1/2',
            'both_inverse_products':True,'both_error_grams':'4 I_8'}


def main():
    baseline={'p':2,'a':3,'d':4,'x':list(range(8)),'y':list(range(8)),
              'k':[0]*8,'R':CONNECTED}
    assert connected_support(CONNECTED)
    assert len(set(tuple(r) for r in CONNECTED))==4
    control=descend(baseline,True)
    # Confirm unequal induced weights; a separate direct-sum control repeats labels.
    children,_=split(baseline)
    assert any(len(set(C['k']))>1 for C in children)
    repeated={'p':2,'a':3,'d':4,'x':list(range(8))*2,'y':list(range(8))*2,
              'k':[0]*16,'R':[[CONNECTED[i%8][j%8] if i//8==j//8 else 0
                              for j in range(16)] for i in range(16)]}
    repeated_result=descend(repeated,True)
    records=[]
    totals=control['verified_gram_entries']+repeated_result['verified_gram_entries']
    families=[(2,range(1,7)),(3,range(1,5)),(5,range(1,3)),(7,range(1,3)),(11,[1]),(13,[1])]
    for p,aa in families:
        for a in aa:
            for b in range(a+1):
                B=divisor_mask(p,a,b)
                out=descend(B)
                assert out['terminal_exponent']==b
                totals+=out['verified_gram_entries']
                records.append({'p':p,'a':a,'N':p**a,'d':p**b,
                                'verified_gram_entries':out['verified_gram_entries'],
                                'terminal_exponent':out['terminal_exponent'],
                                'descent':out['records']})
    corrupt=json.loads(json.dumps(baseline))
    # A 2x2 switch preserves both degree sequences but breaks orthogonality.
    switch=None
    for r in range(8):
        for s in range(r+1,8):
            for j in range(8):
                for l in range(j+1,8):
                    if [CONNECTED[r][j],CONNECTED[r][l],CONNECTED[s][j],CONNECTED[s][l]]==[1,0,0,1]:
                        switch=(r,s,j,l); break
                if switch: break
            if switch: break
        if switch: break
    r,s,j,l=switch
    for i,c in [(r,j),(r,l),(s,j),(s,l)]: corrupt['R'][i][c]^=1
    assert all(sum(row)==4 for row in corrupt['R'])
    assert all(sum(row[c] for row in corrupt['R'])==4 for c in range(8))
    assert expect_rejection(corrupt)
    badweight=json.loads(json.dumps(children[0])); badweight['k'][0]+=1
    assert expect_rejection(badweight)
    cyclo_checks=0
    for p,a in [(2,1),(2,4),(3,3),(5,2),(7,2)]:
        L=p**a; n=L//p
        beta=[(u*u+3*u+1)%11 for u in range(n)]
        hist=[beta[x%n] for x in range(L)]
        for h in range(1,L):
            if h%p:
                assert vanish(((h*x,hist[x]) for x in range(L)),p,a)
                cyclo_checks+=1
        bad=hist[:];bad[0]+=1
        assert any(reduced(bad,p,a))
    witness=inverse_witness()
    results={'status':'PASS','claim':'uniform proof candidate, pending independent review',
             'positive_divisor_cases':len(records),'connected_control':{'N':8,'d':4,'support_connected':True,
             'descent_exercises_unequal_weights':True,'descent_exercises_repeated_row_labels':False,
             'terminal_exponent':control['terminal_exponent']},
             'repeated_label_control':{'matrix_size':16,'character_order':8,'both_label_sets_repeated':True,
                                       'terminal_exponent':repeated_result['terminal_exponent']},
             'all_descent_gram_entries_verified':totals,'cyclotomic_vanishing_controls':cyclo_checks,
             'negative_controls':['degree-preserving support switch rejected','induced weight corruption rejected',
                                  'unbalanced coefficient fibers rejected'],
             'original_inverse_minimizer_verified':True,'historical_code_executed':False,
             'external_writes':False}
    (ROOT/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    (ROOT/'DESCENT_CERTIFICATES.json').write_text(json.dumps({'connected_control':control,'repeated_label_control':repeated_result,'divisor_controls':records},indent=2)+'\n')
    (ROOT/'CONNECTED_INVERSE_WITNESS.json').write_text(json.dumps(witness,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
