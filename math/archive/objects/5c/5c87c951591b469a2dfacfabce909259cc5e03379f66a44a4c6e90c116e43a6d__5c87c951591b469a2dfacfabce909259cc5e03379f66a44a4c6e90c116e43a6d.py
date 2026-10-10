#!/usr/bin/env python3
"""Exact rank obstruction for one-shot bit-partition separable Fourier operators.

For N=A^2, A a power of two, index input x=aA+b and output y=cA+d.
Let R[(a,c),(b,d)]=F_N[y,x] with exponent negative.
Then after swapping column index (b,d)->(d,b),
 R = (F_A tensor F_A) * diag(omega_N^(-bd)).
Thus rank(R)=A^2=N over any exact field containing a primitive Nth
root with char not dividing N. The operator-Schmidt rank of F_N across
this balanced register split is N, maximal.

No expression F_N=sum_{j=1}^s A_j tensor B_j can have s<N.
This is NOT a lower bound on unrestricted arithmetic circuits: products
of sparse or dense factors are not constrained by this one-shot sum rank.
"""
import json
import time
from phase10_rational import P,root_table,root_of_unity


def realignment_matrix(n):
    a=int(n**.5)
    if a*a!=n or a&(a-1):raise ValueError('N=A^2, A power of two')
    roots=root_table(n)
    rows=[]
    for left_input in range(a):
        for left_output in range(a):
            row=[]
            for right_input in range(a):
                for right_output in range(a):
                    x=left_input*a+right_input
                    y=left_output*a+right_output
                    row.append(roots[(-x*y)%n])
            rows.append(row)
    return rows


def rank_mod(rows):
    a=[row[:] for row in rows]
    if not a:return 0
    h=len(a);w=len(a[0]);rank=0
    for col in range(w):
        i=next((i for i in range(rank,h) if a[i][col]),None)
        if i is None:continue
        if i!=rank:a[rank],a[i]=a[i],a[rank]
        pivot=a[rank]
        inv=pow(pivot[col],P-2,P)
        # Pivot row need not be normalized to prove rank; eliminate with
        # factor v * pivot^-1, reduces multiplicative work.
        for j in range(rank+1,h):
            v=a[j][col]
            if not v:continue
            scale=v*inv%P
            row=a[j]
            for t in range(col+1,w):row[t]=(row[t]-scale*pivot[t])%P
            row[col]=0
        rank+=1
        if rank==h:break
    return rank


def check(n):
    a=int(n**.5)
    omega=root_of_unity(n)
    table=root_table(n)
    omega_a=pow(omega,a,P)
    r=realignment_matrix(n)
    checked=0
    for aa in range(a):
        for cc in range(a):
            for b in range(a):
                for d in range(a):
                    row=aa*a+cc;col=b*a+d
                    predicted=(pow(omega_a,-aa*d-cc*b,P)*
                               table[(-b*d)%n])%P
                    assert r[row][col]==predicted
                    checked+=1
    t=time.perf_counter()
    rank=rank_mod(r)
    dt=time.perf_counter()-t
    assert rank==n
    return {'n':n,'a':a,'exact_fourier_realignment_rank':rank,
            'max_possible_rank':n,'rank_upper_bound_of_s_terms':
            's; hence any F_N=sum_i A_i tensor B_i needs at least N terms',
            'matrix_entries_verified':checked,
            'runtime_sec':round(dt,4)}


def main():
    records=[]
    for n in (4,16,64,256):
        a=check(n)
        records.append(a)
        print('N=%d operator-Schmidt rank=%d/%d exact entries checked=%d runtime=%.3fs' %
             (n,a['exact_fourier_realignment_rank'],n,a['matrix_entries_verified'],
              a['runtime_sec']))
    result={
      'result':'FULL operator-Schmidt rank N for balanced bit partition N=A^2',
      'rigorous_identity':'R[(a,c),(b,d)]=omega_A^(-a*d-c*b)*omega_N^(-b*d)',
      'consequence':'N separable terms required in a one-shot sum of bit-partitioned operator products',
      'not_consequence':'Does not exclude O(N) unrestricted FFT circuits or products of many factors',
      'records':records}
    with open('SCHMIDT_AUDIT.json','w') as f:json.dump(result,f,indent=2)


if __name__=='__main__':main()
