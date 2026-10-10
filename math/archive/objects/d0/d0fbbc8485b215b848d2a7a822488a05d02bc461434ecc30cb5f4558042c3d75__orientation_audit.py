"""An independent orientation-stress audit using direct dense operators."""
import json,random
from phase13 import (omega_root,branch_matrix,reverse_matrix,triple_matrix,coeff_trace,rank,
    branch_apply,reverse_apply,triple_apply,matvec,fourier,gs_matrix,gt_diag)

CASES=[(3,307),(5,521),(7,701),(9,919),(11,1123),(15,1531),(17,1871)]

# Implement a fresh rank function to avoid treating the tested code's rank as oracle.
def audit_rank(A,p):
    M=[list(row) for row in A];m=len(M);n=len(M[0]);j=0
    for i in range(m):
        while j<n and not any(M[k][j] for k in range(i,m)):j+=1
        if j==n:return i
        k=next(k for k in range(i,m) if M[k][j]);M[i],M[k]=M[k],M[i]
        den=pow(M[i][j],p-2,p)
        for col in range(j,n):M[i][col]=M[i][col]*den%p
        for k in range(i+1,m):
            factor=M[k][j]
            if factor:
                for col in range(j,n):M[k][col]=(M[k][col]-factor*M[i][col])%p
        j+=1
    return m

def run():
    summary=[];basis_checks=0;random_checks=0
    for n,p in CASES:
        w=omega_root(n,p);a=2;b=3;g=4
        while pow(a,n,p)==1:a+=1
        while pow(b,n,p)==1:b+=1
        while pow(g,n,p)==1:g+=1
        A=branch_matrix(n,a,b,w,p);B=reverse_matrix(n,a,b,w,p)
        C=triple_matrix(n,a,b,g,w,p)
        F=fourier(n,w,p)
        assert audit_rank(coeff_trace(A,w,p),p)==1
        assert audit_rank(coeff_trace(B,w,p),p)==n
        assert audit_rank(coeff_trace(C,w,p),p)==n
        assert C!=F and B!=F and A!=F
        for j in range(n):
            x=[int(i==j) for i in range(n)]
            assert branch_apply(x,a,b,w,p)==[row[j] for row in A]
            assert reverse_apply(x,a,b,w,p)==[row[j] for row in B]
            assert triple_apply(x,a,b,g,w,p)==[row[j] for row in C]
            basis_checks+=3
        rng=random.Random(n*293+p)
        for _ in range(4):
            x=[rng.randrange(p) for _ in range(n)]
            assert reverse_apply(x,a,b,w,p)==matvec(B,x,p)
            assert triple_apply(x,a,b,g,w,p)==matvec(C,x,p)
            random_checks+=2
        summary.append({'N':n,'modulus':p,'forward_weyl_rank':1,'reverse_weyl_rank':n,
                        'triple_weyl_rank':n,'all_basis_vectors_checked':n})
    out={'cases':summary,'individual_basis_operator_checks':basis_checks,
         'independent_random_operator_checks':random_checks,
         'verdict':'rank N does not imply hard evaluation; reverse/triple Green paths remain O(N) and are not Fourier'}
    with open('ORIENTATION_AUDIT_RESULTS.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps({'basis':basis_checks,'random':random_checks,'cases':len(summary)},indent=2))

if __name__=='__main__':run()
