#!/usr/bin/env python3
from pathlib import Path
import random,json
import sympy as sp
HERE=Path(__file__).resolve().parent;rng=random.Random(102214)
def monomial(n):
    p=list(range(n));rng.shuffle(p);a=sp.zeros(n)
    for i,j in enumerate(p):a[i,j]=rng.choice([-3,-2,-1,1,2,3])
    return a

def grid_denominator(m):
    n=m*m;u=sp.eye(n)
    for i in range(n):
        if i//m:u[i,i-m]=-rng.randrange(4)
        if i%m:u[i,i-1]=-rng.randrange(4)
    return u

def count(a):
    return {'max_row':max(sum(v!=0 for v in a.row(i)) for i in range(a.rows)),
            'max_column':max(sum(v!=0 for v in a.col(i)) for i in range(a.cols))}
cases=[]
for m in [2,3]:
    n=m*m
    for mode in ['noncommuting','left_pure','right_pure','singular_zero_sum']:
        U1,U2,V1,V2=[monomial(n)*grid_denominator(m)*monomial(n) for _ in range(4)]
        C=monomial(n)
        alpha1,beta1,alpha2,beta2=2,3,-1,4
        if mode=='left_pure':alpha2,beta2=0,1
        if mode=='right_pure':alpha1,beta1=1,0
        if mode=='singular_zero_sum':V1=U1;alpha1,beta1=1,-1
        H1=alpha1*U1.inv()+beta1*V1.inv();H2=alpha2*U2.inv()+beta2*V2.inv()
        W1=alpha1*V1+beta1*U1;W2=alpha2*V2+beta2*U2
        K=U1*C.inv()*V2;F=H2*C*H1
        assert H1==U1.inv()*W1*V1.inv()
        assert H2==U2.inv()*W2*V2.inv()
        assert U2*F*V1==W2*K.inv()*W1
        block=K.row_join(W1).col_join(W2.row_join(U2*F*V1))
        assert block.rank()==n
        counts={label:count(A) for label,A in [('K',K),('W1',W1),('W2',W2)]}
        assert counts['K']['max_row']<=9 and counts['K']['max_column']<=9
        for label in ['W1','W2']:
            assert counts[label]['max_row']<=6 and counts[label]['max_column']<=6
        cases.append({'M':m,'mode':mode,'fraction_identity':True,'block_rank':n,'sparse_counts':counts,
                      'right_sum_singular':H1.det()==0,'left_sum_singular':H2.det()==0})
(HERE/'FRACTION_CONTROLS.json').write_text(json.dumps(cases,indent=2)+'\n')
print(json.dumps(cases,indent=2))
