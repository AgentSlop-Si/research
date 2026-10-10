#!/usr/bin/env python3
"""Self-authored exact chirp supplement controls; imports no research program."""
import json
from pathlib import Path
p=65537

def check(x,s):
    if not x:raise AssertionError(s)

def polymul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return c

def matmul(a,b):
    bt=list(zip(*b));return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]

def column(q,N,w,h,l,j):
    out=[]
    for i in range(N):
        value=0
        for a,qa in enumerate(q):
            for b,qb in enumerate(q):
                power=h*(a*a+b*b)+l*(a+b)+a*b+i*(2*h*a+b)+j*(a+2*h*b)
                value=(value+qa*qb*pow(w,power%N,p))%p
        out.append(pow(w,i*j,p)*value%p)
    return out

def main():
    gains=[3,27,243,2187];small=[]
    for N in [8,16,32,64]:
        w=pow(3,(p-1)//N,p)
        for r in [1,2,4]:
            q=[1]
            for a in gains[:r]:
                check(pow(a,N,p)!=1,'bad denominator');q=polymul(q,[1,-a%p])
            for h in [-2,-1,0,1,2]:
                l=3;C=[pow(w,(h*i*i+l*i)%N,p) for i in range(N)];Q=[[0]*N for _ in range(N)]
                for j in range(N):
                    for a,qa in enumerate(q):
                        i=(j+a)%N;Q[i][j]=(Q[i][j]+qa*C[i]*pow(C[j],-1,p))%p
                F=[[pow(w,i*j,p) for j in range(N)] for i in range(N)]
                direct=matmul(list(map(list,zip(*Q))),matmul(F,Q))
                maxzero=0
                for j in range(N):
                    c=column(q,N,w,h,l,j);check(c==[direct[i][j] for i in range(N)],'chirp formula')
                    check(any(c),'zero column');z=sum(v==0 for v in c);maxzero=max(maxzero,z)
                    check(z<=min(N,(2*abs(h)+1)*r),'Laurent zero bound')
                small.append({'N':N,'degree':r,'h':h,'ell':l,'columns':N,'max_zeros':maxzero,'width':(2*abs(h)+1)*r})
    q=[1]
    for a in gains:q=polymul(q,[1,-a%p])
    large=[]
    N=1024;w=pow(3,(p-1)//N,p)
    for h in [-2,-1,0,1,2]:
        width=(2*abs(h)+1)*4;cases=[]
        for j in [0,1,341,1023]:
            c=column(q,N,w,h,7,j);nnz=sum(v!=0 for v in c);check(nnz>=N-width,'large zero bound')
            cases.append({'j':j,'nnz':nnz})
        check(N-width>64*(10+2),'claimed exclusion does not apply')
        large.append({'h':h,'width':width,'lower':N-width,'carrier_upper':768,'columns':cases})
    result={'status':'PASS','field':p,'small_cases':small,'large_N':N,'large_cases':large,'scope':'Finite exact controls support algebra, not a general FFT lower bound.'}
    out=Path(__file__).with_name('CHIRP_FRESH_RESULTS_v1.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','small_cases':len(small),'small_columns':sum(c['columns'] for c in small),'large_columns':20}))
if __name__=='__main__':main()
