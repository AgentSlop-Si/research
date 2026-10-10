"""Independent exact controls, authored for this task. No project imports."""
import json
import random
from pathlib import Path
import sympy as s

w, a, x, t = s.symbols('w a x t')
HERE = Path(__file__).resolve().parent

def fixed_resultant(f, g, z, m):
    fc = [s.expand(f).coeff(z, k) for k in range(m, -1, -1)]
    gc = [s.expand(g).coeff(z, k) for k in range(m, -1, -1)]
    rows = []
    for co in (fc, gc):
        for k in range(m):
            rows.append([0]*k + co + [0]*(m-1-k))
    return s.expand(s.Matrix(rows).det(method='domain-ge'))

def minor_product(A, B):
    m = A.rows
    z = (-1)**(m*(m-1)//2)*A.det()*B.det()
    for M in (A, B):
        for j in range(1, m):
            z *= M[:j,:j].det()*M[j:,j:].det()
    return s.expand(z)

def parity_value(A, B):
    m = A.rows
    X = s.kronecker_product(A, B)
    groups = [[i*m+k for i in range(m) for k in range(m) if (i+k)%2 == e] for e in (0,1)]
    return s.prod(X.extract(G,G).det() for G in groups)

def tangent_value(A,B):
    m=A.rows; L=s.diag(*range(m))
    C=L*A+A*L; D=L*B+B*L+B
    K=s.kronecker_product(A,D)-s.kronecker_product(C,B)
    z=K.det()
    assert z==fixed_resultant((t*A+C).det(),(t*B+D).det(),t,m)
    return z

def trace_from_resultant(R,m):
    v=m*(m-1)*(4*m+1)//6; b=m*(m-1)*(2*m-1)//6
    U=s.cancel(R/(w**v*(w-1)**(m*m)))
    assert s.denom(U)==1
    U=s.Poly(U,w)
    C0,C1=s.Integer(2),x
    V=U.nth(b)
    for k in range(1,b+1):
        if k==1: C=C1
        else:
            C=s.expand(x*C1-C0); C0,C1=C1,C
        V += U.nth(b+k)*C
    V=s.Poly(s.expand(V),x)
    assert s.expand(w**b*V.as_expr().subs(x,w+1/w)-U.as_expr())==0
    return V

def order(poly,z,r,mod=None):
    P=s.Poly(poly,z,modulus=mod) if mod else s.Poly(poly,z)
    if P.is_zero: return None
    Q=s.Poly(z-r,z,modulus=mod) if mod else s.Poly(z-r,z)
    k=0
    while True:
        d,rem=s.div(P,Q)
        if not rem.is_zero: return k
        k+=1; P=d

def run_case(name,A,B):
    A=s.Matrix(A); B=s.Matrix(B); m=A.rows
    D=s.diag(*[w**i for i in range(m)])
    f=(A-a*D*A*D).det(); g=(B-a*w*D*B*D).det()
    R=fixed_resultant(f,g,a,m)
    V=trace_from_resultant(R,m)
    b=m*(m-1)*(2*m-1)//6
    assert V.nth(b)==minor_product(A,B)
    assert V.eval(2)==tangent_value(A,B)
    assert V.eval(-2)==parity_value(A,B)
    checks=[]
    for p in (None,2,3,5,7):
        VP=s.Poly(V.as_expr(),x,modulus=p) if p else V
        RP=s.Poly(R,w,modulus=p) if p else s.Poly(R,w)
        if RP.is_zero:
            assert VP.is_zero
            checks.append({'characteristic':p or 0,'zero_resultant':True})
            continue
        assert order(R,w,1,p)==m*m+2*order(V.as_expr(),x,2,p)
        if p!=2:
            assert order(R,w,-1,p)==2*order(V.as_expr(),x,-2,p)
        v=m*(m-1)*(4*m+1)//6
        assert order(R,w,0,p)==v+b-VP.degree()
        checks.append({'characteristic':p or 0,'zero_resultant':False,'degree_V':VP.degree()})
    # A direct independent determinant evaluation of the Laurent kernel.
    for z in (s.Rational(2),s.Rational(-2),s.Rational(3,2)):
        K=s.Matrix(m*m,m*m,lambda r,c: A[r//m,c//m]*B[r%m,c%m]*(z**(1+r%m-r//m+c%m-c//m)-1)/(z-1))
        assert s.cancel(K.det()-V.eval(z+1/z))==0
    return {'name':name,'m':m,'A':list(map(list,A.tolist())),'B':list(map(list,B.tolist())),
            'V':str(V.as_expr()),'top_coefficient':int(V.nth(b)),
            'value_plus_two':int(V.eval(2)),'value_minus_two':int(V.eval(-2)),
            'field_checks':checks}

def main():
    cases=[('scalar',[[2]],[[3]]),('scalar_zero',[[0]],[[3]]),
           ('identity_2',s.eye(2),s.eye(2)),
           ('degree_drop_nonzero',[[0,1],[1,0]],[[0,1],[1,0]]),
           ('singular_input_nonzero',[[1,1],[1,1]],s.eye(2)),
           ('extra_plus_one',[[4,3],[1,1]],s.eye(2)),
           ('extra_minus_one',[[1,1],[1,-1]],[[1,1],[1,-1]]),
           ('zero_resultant',s.zeros(2),s.eye(2)),
           ('identity_3',s.eye(3),s.eye(3)),
           ('dense_full_degree_3',[[3,1,1],[1,4,2],[1,2,5]],[[4,2,1],[2,5,1],[1,1,6]])]
    rng=random.Random(20261010)
    for m,count in ((2,8),(3,3)):
        for j in range(count):
            cases.append((f'random_{m}_{j}',s.Matrix(m,m,[rng.randint(-3,3) for _ in range(m*m)]),
                          s.Matrix(m,m,[rng.randint(-3,3) for _ in range(m*m)])))
    out=[]
    for args in cases:
        result=run_case(*args); out.append(result)
        print(result['name'],'PASS',result['V'],flush=True)
    report={'status':'PASS','source_program_execution':False,'source_program_imports':False,
            'external_writes':False,'fresh_program':Path(__file__).name,
            'case_count':len(out),'field_specializations':5*len(out),
            'independent_laurent_evaluations':3*len(out),'cases':out}
    (HERE/'FRESH_RESULTS.json').write_text(json.dumps(report,indent=2,default=int)+'\n')

if __name__=='__main__': main()
