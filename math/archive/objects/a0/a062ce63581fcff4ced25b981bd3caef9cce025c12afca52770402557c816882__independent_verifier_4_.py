from __future__ import annotations

import json
from pathlib import Path

from finite_field import inv, mat_identity, mat_mul, matrix_inverse, primitive_root, is_prime


def find_field(n: int, start: int = 2):
    k = start
    while True:
        p = k * n + 1
        if is_prime(p):
            g = primitive_root(p)
            w = pow(g, k, p)
            if w != 1 and pow(w, n, p) == 1:
                return p, w
        k += 1


def zero(n): return [[0] * n for _ in range(n)]


def weyl(n, p, w, h, r):
    a = zero(n)
    for j in range(n): a[(j+h)%n][j] = pow(w, r*j, p)
    return a


def green(n,p,w,alpha,h,r):
    W=weyl(n,p,w,h,r); A=mat_identity(n)
    for i in range(n):
        for j in range(n): A[i][j]=(A[i][j]-alpha*W[i][j])%p
    return matrix_inverse(A,p)


def rank(a,p):
    a=[r[:] for r in a]; R=len(a); C=len(a[0]); rr=0
    for c in range(C):
        q=next((i for i in range(rr,R) if a[i][c]%p),None)
        if q is None: continue
        a[rr],a[q]=a[q],a[rr]
        z=pow(a[rr][c],p-2,p);a[rr]=[x*z%p for x in a[rr]]
        for i in range(R):
            if i!=rr and a[i][c]%p:
                f=a[i][c]%p;a[i]=[(x-f*y)%p for x,y in zip(a[i],a[rr])]
        rr+=1
        if rr==R:break
    return rr


def verify_case(rec):
    n=rec['n'];p=rec['field_prime'];w=rec['omega'];alpha=rec['alpha']
    inv2=pow(2,-1,n)
    # Independently verify the chirp polynomial identity entrywise.
    for i in range(n):
        for j in range(n):
            target=pow(w,(i*j-i*i)%n,p)
            got=0
            for h in range(n):
                # U^h has one entry at i=j+h with phase -h*j-h(h-1)/2.
                if i==(j+h)%n:
                    coeff=pow(w,(-h*(h+1)*inv2)%n,p)
                    phase=pow(w,(-h*j-h*(h-1)*inv2)%n,p)
                    got=(got+coeff*phase)%p
            assert got==target
    # Independently check all reported B_x ranks.
    for x, expected in enumerate(rec['block_ranks']):
        B=[]
        for d in range(1,n):
            row=[]
            for h in range(1,n):
                ratio=d*pow(h,-1,n)%n
                phase=(-x*d*(d-h)*inv2)%n
                row.append(pow(alpha,ratio,p)*pow(w,phase,p)%p)
            B.append(row)
        assert rank(B,p)==expected==n-1
    # Selected character packet support <=2 per row and column follows from direct quadratic enumeration.
    for h,s in ((1,0),(1,1),(2%n,0),(2%n,3%n)):
        A=zero(n);den=pow((1-pow(alpha,n,p))%p,p-2,p)
        am=1
        for m in range(n):
            q0=h*m*(m-1)//2
            for j in range(n):
                if (m*j+q0-s)%n==0:
                    A[(j+m*h)%n][j]=(A[(j+m*h)%n][j]+den*am)%p
            am=am*alpha%p
        assert max(sum(v!=0 for v in row) for row in A)<=2
        assert max(sum(A[i][j]!=0 for i in range(n)) for j in range(n))<=2
    return True


def main():
    root=Path(__file__).resolve().parent
    data=json.loads((root/'results.json').read_text())
    passed=[]
    for rec in data['finite_field_cases']:
        verify_case(rec);passed.append(rec['n'])
    out={'independent_cases_passed':passed,'count':len(passed)}
    (root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
