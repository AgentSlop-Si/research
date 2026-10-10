"""Independent exact modular nonexistence checks, no imported project modules.

For N=8, using a primitive eighth root r in F_p gives a specialization
of Z[zeta_8] -> F_p. A nonzero determinant after specialization proves
its original determinant is nonzero over the characteristic-zero field.

This certifies lower bounds, never suffices on its own for existence of a
characteristic-zero rational expression.
"""
import json

P=998244353
R=pow(3,(P-1)//8,P)
assert pow(R,8,P)==1 and pow(R,4,P)==P-1


def rank(A):
    if not A:return 0
    A=[list(map(lambda x: x%P,row)) for row in A]
    rows=len(A);cols=len(A[0]);i=0
    for j in range(cols):
        pivot=next((k for k in range(i,rows) if A[k][j]),None)
        if pivot is None:continue
        A[i],A[pivot]=A[pivot],A[i]
        inv=pow(A[i][j],-1,P)
        A[i]=[v*inv%P for v in A[i]]
        for k in range(i+1,rows):
            coeff=A[k][j]
            if coeff:A[k]=[(a-coeff*b)%P for a,b in zip(A[k],A[i])]
        i+=1
        if i==rows:break
    return i


def run():
    nodes=[]
    for mask in range(16):
        a=sum(pow(R,j,P) for j in range(4) if mask>>j&1)%P
        b=sum(pow(R,3*j,P) for j in range(4) if mask>>j&1)%P
        nodes.append((a,b))
    assert len({a for a,b in nodes})==16
    polydeg=10
    poly=[[(pow(a,j,P)) for j in range(polydeg+1)] for a,b in nodes]
    augmented=[r+[b] for r,(a,b) in zip(poly,nodes)]
    assert rank(poly)==11
    assert rank(augmented)==12
    ratdeg=7
    rat=[([pow(a,j,P) for j in range(ratdeg+1)]
          + [(-b*pow(a,j,P))%P for j in range(ratdeg+1)])
         for a,b in nodes]
    assert rank(rat)==16
    # Degree 8: 18 columns, 16 rows => nonzero kernel, but existence
    # requires checking Q != 0 at all nodes separately in char zero.
    deg8=[([pow(a,j,P) for j in range(9)]
          + [(-b*pow(a,j,P))%P for j in range(9)])
          for a,b in nodes]
    assert rank(deg8)==16
    return {'field_prime':P,'primitive_eighth_root':R,'unique_alpha_samples':16,
            'polynomial_degree_at_most_10_excluded':rank(poly)==11 and rank(augmented)==12,
            'rational_num_den_degree_at_most_7_excluded':rank(rat)==16,
            'rank_poly_deg10':rank(poly),'rank_poly_deg10_aug':rank(augmented),
            'rank_rational_deg7':rank(rat),'rank_rational_deg8':rank(deg8)}

if __name__=='__main__':
    r=run()
    with open('modular_certificate.json','w') as f:json.dump(r,f,indent=2)
    print(r)
