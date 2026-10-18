#!/usr/bin/env python3
"""Independent small checker: built-ins, exact Fraction, no candidate imports."""
import fractions, hashlib, json, pathlib
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parent

def mul(A,B,p=None):
    C=[[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
    return [[x%p for x in row] for row in C] if p else C
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def rev(i,m):
    v=0
    for k in range(m):v=2*v+((i>>k)&1)
    return v
def data(n):
    th=[1,4];et=[1,3]
    for k in range(2,n+1):th.append(3*th[-1]-th[-2]);et.append(3*et[-1]-et[-2])
    a=[(-1)**i*et[n-1-i] for i in range(n)]
    b=[Fraction((-1)**i*th[i],th[n]) for i in range(n)]
    c=b.copy();e=a.copy();d=[Fraction(th[i]*et[n-1-i],th[n]) for i in range(n)]
    a[0]=0;b[-1]=0;c[-1]=0;e[0]=0
    return [a,b,c,e,d]
def chart(x,p=None):
    a,b,c,e,d=x;n=len(a)
    A=[[a[i]*b[j] if i>j else (c[i]*e[j] if i<j else d[i]) for j in range(n)] for i in range(n)]
    return [[z%p for z in row] for row in A] if p else A
def product(stages,P,p):
    M=stages[0]
    for S in stages[1:]:M=mul(mul(S,P,p),M,p)
    return M
def rank(A,p):
    # Independent column-basis algorithm, no row-echelon implementation shared.
    base={}
    for col in zip(*A):
        v=list(col)
        for pivot,w in base.items():
            scale=v[pivot]
            if scale:v=[(x-scale*y)%p for x,y in zip(v,w)]
        pivot=next((i for i,x in enumerate(v) if x),None)
        if pivot is not None:
            z=pow(v[pivot],-1,p);base[pivot]=[(x*z)%p for x in v]
    return len(base)

def run():
    checks=[]
    for n in (8,16):
        raw=data(n);S=chart(raw);T=[[4 if i==j==0 else (3 if i==j else int(abs(i-j)==1)) for j in range(n)] for i in range(n)]
        assert mul(T,S)==eye(n);assert mul(S,T)==eye(n)
        checks.append({'N':n,'exact_fraction_continuant_inverse':True,'maximum_parameter_numerator_bits':max(abs(Fraction(x).numerator).bit_length() for row in raw for x in row),'maximum_parameter_denominator_bits':max(Fraction(x).denominator.bit_length() for row in raw for x in row)})
    n=8;t=3;m=3;rv=[rev(i,m) for i in range(n)];P=[[int(i==rv[j]) for j in range(n)] for i in range(n)]
    for p in (12289,65537):
        raw=[[int(Fraction(x).numerator)*pow(int(Fraction(x).denominator),-1,p)%p for x in row] for row in data(n)]
        S=chart(raw,p);base=product([S]*t,P,p);cols=[]
        for stage in range(t):
            for typ in range(5):
                for q in range(n):
                    x=[row.copy() for row in raw];x[typ][q]=(x[typ][q]+1)%p
                    stages=[S]*t;stages[stage]=chart(x,p);M=product(stages,P,p)
                    cols.append([(M[i][j]-base[i][j])%p for i in range(n) for j in range(n)])
        rk=rank(list(map(list,zip(*cols))),p);assert rk==64
        checks.append({'N':8,'t':3,'p':p,'full_product_finite_difference_raw_rank':rk,'raw_columns':len(cols)})
    out={'all_passed':True,'method':'independent built-ins and Fraction; finite differences of the full original product; no candidate imports','checks':checks,'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
    (R/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
