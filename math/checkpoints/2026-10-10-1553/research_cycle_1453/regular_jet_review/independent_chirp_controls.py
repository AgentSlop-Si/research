#!/usr/bin/env python3
"""Independent review of the quadratic-chirp supplement.

Imports only our own review oracle, never candidate/source programs.
"""
import itertools
import json
from pathlib import Path
from independent_controls import (RNG, fourier, identity, inverse, multiply,
                                  root, transpose)

OUT=Path(__file__).resolve().parent


def chirp_matrix(n,w,p,h,ell,q):
    c=[pow(w,h*i*i+ell*i,p) for i in range(n)]
    W=[[0]*n for _ in range(n)]
    for j in range(n):
        W[(j+1)%n][j]=c[(j+1)%n]*pow(c[j],-1,p)%p
    power=identity(n)
    Q=[[0]*n for _ in range(n)]
    for coefficient in q:
        Q=[[(a+coefficient*b)%p for a,b in zip(ar,br)] for ar,br in zip(Q,power)]
        power=multiply(power,W,p)
    return Q


def laurent(q,j,w,p,h,ell):
    coefficients={}
    for a,qa in enumerate(q):
        for b,qb in enumerate(q):
            exponent=2*h*a+b
            v=qa*qb*pow(w,h*(a*a+b*b)+ell*(a+b)+a*b+j*(a+2*h*b),p)
            coefficients[exponent]=(coefficients.get(exponent,0)+v)%p
    return {e:v for e,v in coefficients.items() if v}


def small_controls():
    cases=0
    tested_columns=0
    zero_q0=0
    for n in (4,8,16,32):
        p=257
        w=root(p,n)
        for h,ell,kind in itertools.product(range(-4,5),(0,1,3),(0,1)):
            r=min(4,n-1)
            while True:
                q=[RNG.randrange(1,p) for _ in range(r+1)]
                if kind==0:
                    q[0]=0
                Q=chirp_matrix(n,w,p,h,ell,q)
                if inverse(Q,p) is not None:
                    break
            zero_q0+=q[0]==0
            A=multiply(multiply(transpose(Q),fourier(n,w,p),p),Q,p)
            width=(2*abs(h)+1)*r
            for j,col in enumerate(transpose(A)):
                coef=laurent(q,j,w,p,h,ell)
                assert coef
                assert max(coef)-min(coef)<=width
                predicted=[pow(w,i*j,p)*sum(v*pow(w,i*e,p) for e,v in coef.items())%p for i in range(n)]
                assert predicted==col
                assert sum(v!=0 for v in col)>=max(0,n-width)
                tested_columns+=1
            cases+=1
    return {'matrix_cases':cases,'columns':tested_columns,'q0_zero_cases':zero_q0,
            'curvatures':list(range(-4,5)),'linear_phases':[0,1,3]}


def large_controls():
    p=65537
    n=1024
    w=root(p,n)
    q=[1,3,5,7,9]
    # Reject/reselect if the test denominator accidentally hits a Fourier eigenvalue.
    while any(sum(v*pow(w,j*a,p) for a,v in enumerate(q))%p==0 for j in range(n)):
        q[-1]=(q[-1]+1)%p
    data=[]
    for h in (-3,-2,-1,0,1,2,3):
        ell=7
        c=[pow(w,h*i*i+ell*i,p) for i in range(n)]
        # Powers are obtained by products of actual wraparound edge weights.
        edge=[c[(j+1)%n]*pow(c[j],-1,p)%p for j in range(n)]
        powers=[]
        for j in range(n):
            row=[1]
            for a in range(1,len(q)):
                row.append(row[-1]*edge[(j+a-1)%n]%p)
            powers.append(row)
        for j in (0,17,n-1):
            direct=[sum(q[a]*q[b]*powers[i][a]*powers[j][b]*pow(w,((i+a)%n)*((j+b)%n),p)
                        for a in range(len(q)) for b in range(len(q)))%p for i in range(n)]
            coef=laurent(q,j,w,p,h,ell)
            predicted=[pow(w,i*j,p)*sum(v*pow(w,i*e,p) for e,v in coef.items())%p for i in range(n)]
            assert direct==predicted
            lower=n-(2*abs(h)+1)*(len(q)-1)
            support=sum(v!=0 for v in direct)
            assert support>=lower
            assert lower>64*(10+2)
            data.append({'h':h,'column':j,'support':support,'lower':lower,'carrier_upper':768})
    return {'N':n,'field':p,'q':q,'cases':data}


def cancellation_control():
    p=17;n=8;w=root(p,n);h=-1;ell=0
    for q in itertools.product(range(1,p),repeat=3):
        Q=chirp_matrix(n,w,p,h,ell,q)
        if inverse(Q,p) is None:
            continue
        for j in range(n):
            coef=laurent(q,j,w,p,h,ell)
            if 0 not in coef:
                assert coef
                return {'N':n,'field':p,'omega':w,'h':h,'ell':ell,
                        'q':q,'j':j,'Laurent_coefficients':coef,
                        'conclusion':'constant coefficient vanishes despite q0 != 0 and invertible Q'}
    raise AssertionError('No constant-term collision found')


def main():
    data={'status':'PASS','source_execution':False,'small':small_controls(),
          'large':large_controls(),'constant_term_cancellation':cancellation_control(),
          'scope':'Exact corroboration of independently rederived exponent formula and Laurent-width proof.'}
    (OUT/'CHIRP_REVIEW_RESULTS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':'PASS','small':data['small'],'large_column_cases':len(data['large']['cases']),
                      'cancellation_q':data['constant_term_cancellation']['q']}))


if __name__=='__main__':
    main()
