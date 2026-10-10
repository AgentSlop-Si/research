"""Separate reference calculations. Do not use phase13's rank/reconstruction formulas as oracle."""
import json,random,hashlib
from math import gcd
from phase13 import (omega_root,rotated,delta,find_dense_inverse_witness,sum_matrix,
                     prepare_gt_batch,sum_apply,Cost,coeff_F,rotated_rank)

OUT='AUDIT_RESULTS.json'

def row_rank(M,p):
    a=[list(row) for row in M]
    if not a:return 0
    nr=len(a);nc=len(a[0]);r=0
    for j in range(nc):
        chosen=-1
        for i in range(r,nr):
            if a[i][j]%p:chosen=i;break
        if chosen<0:continue
        a[r],a[chosen]=a[chosen],a[r]
        z=pow(a[r][j]%p,p-2,p)
        for k in range(j,nc):a[r][k]=a[r][k]*z%p
        for i in range(nr):
            if i!=r:
                t=a[i][j]
                if t:
                    for k in range(j,nc):a[i][k]=(a[i][k]-t*a[r][k])%p
        r+=1
        if r==nr:break
    return r

def matrix_inverse(A,p):
    n=len(A);v=[[a%p for a in A[i]]+[int(i==j) for j in range(n)] for i in range(n)]
    for k in range(n):
        row=next((i for i in range(k,n) if v[i][k]),None)
        if row is None:return None
        v[row],v[k]=v[k],v[row]
        z=pow(v[k][k],p-2,p)
        v[k]=[t*z%p for t in v[k]]
        for i in range(n):
            if i!=k and v[i][k]:
                z=v[i][k];v[i]=[(t-z*q)%p for t,q in zip(v[i],v[k])]
    return [r[n:] for r in v]

def direct_weyl_coeff(n,p,w):
    invn=pow(n,p-2,p)
    return [[sum(pow(w,(k*k+(a-b)*k)%n,p) for k in range(n))*invn%p
            for b in range(n)]for a in range(n)]

def direct_reconstruct_rotated(n,p,w,C,u,v,r,s):
    A=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            uvphase=(u*v*i*(i-1)//2+r*s*j*(j-1)//2+v*r*i*j)%n
            for k in range(n):
                to=(k+u*i+r*j)%n
                phase=(uvphase+(v*i+s*j)*k)%n
                A[to][k]=(A[to][k]+C[i][j]*pow(w,phase,p))%p
    return A

def audit_small():
    cases=[(3,307),(5,521),(7,701),(9,919),(11,1123),(15,1531),(17,1871)]
    summaries=[];n_all_entries=0;num_basis=0;minhank=0;dense_inverse_cases=[]
    for n,p in cases:
        w=omega_root(n,p)
        C=direct_weyl_coeff(n,p,w)
        assert C==coeff_F(n,w,p)
        assert row_rank(C,p)==n
        candidates=[(1,0,0,1),(1,0,1,1),(0,1,1,1),(1,1,0,1),(1,2,1,3),(1,0,1,7),(1,0,1,11)]
        selected=[b for b in candidates if gcd(b[0]*b[3]-b[1]*b[2],n)==1]
        for b in selected:
            Cprime=rotated(n,w,p,*b)
            calc=direct_reconstruct_rotated(n,p,w,Cprime,*b)
            ref=[[pow(w,i*j%n,p) for j in range(n)]for i in range(n)]
            assert calc==ref,(n,b)
            n_all_entries+=n*n;num_basis+=1
            assert row_rank(Cprime,p)==rotated_rank(n,*b)
            D,z=delta(n,*b)
            if z==0:
                h=(n+1)//2
                H=[[Cprime[i+j][0] for j in range(h)]for i in range(h)]
                assert row_rank(H,p)==h
                minhank+=1
        witness=find_dense_inverse_witness(n,w,p)
        assert witness is not None
        a,b=witness;H=sum_matrix(n,a,b,w,p)
        Hi=matrix_inverse(H,p)
        assert Hi is not None and all(z!=0 for row in Hi for z in row)
        assert all(sum(H[i][k]*Hi[k][j] for k in range(n))%p == (i==j) for i in range(n) for j in range(n))
        dense_inverse_cases.append({'n':n,'p':p,'alpha':a,'beta':b,'nonzero_inverse_entries':n*n})
        summaries.append({'n':n,'prime_field':p,'weyl_coeff_rank':n,'rotated_basis_checks':len(selected),
                          'gauss_nonzero':True,'full_spectrum_reference':True})
    return {'cases':summaries,'basis_checks':num_basis,'basis_reconstruction_entries_checked':n_all_entries,
            'favorable_hankel_certificates':minhank,'full_inverse_witnesses':dense_inverse_cases}

def audit_prime_GL2():
    details=[]
    for n in [3,5,7,11]:
        total=0;rank_one=0;full=0
        for u in range(n):
            for v in range(n):
                for r in range(n):
                    for s in range(n):
                        D,z=delta(n,u,v,r,s)
                        if not D:continue
                        total+=1
                        # Two independent routes to the same obstruction:
                        if z==0:
                            rank_one+=1
                            a2=(u*u+v*v)%n;b2=(r*r+s*s)%n
                            assert a2*b2%n==2*D*D%n and a2!=0 and b2!=0
                        else:full+=1
        assert total==(n*n-1)*(n*n-n)
        details.append({'n':n,'all_generating_direction_pairs':total,'rank_one_gauges':rank_one,
                        'full_rank_gauges':full,'uniform_branch_lower_bound':(n+1)//2})
    return details

def audit_large():
    p=998244353;n=65536;w=omega_root(n,p)
    rng=random.Random(20261010)
    x=[rng.randrange(p) for _ in range(n)]
    prep=Cost();diag=prepare_gt_batch(n,3,w,p,prep)
    online=Cost();out=sum_apply(x,2,3,w,p,online,diag)
    gs=[(y-xx*dd)%p for y,xx,dd in zip(out,x,diag)]
    assert len(out)==n
    assert all((gs[k]-2*gs[k-1])%p==x[k] for k in range(n))
    iden=pow(1-pow(2,n,p),-1,p)
    positions=[0,1,2,3,n//13,n//7,n//3,n//2,n-1]
    kernel_checks=0
    for i in positions:
        direct=(sum(pow(2,(i-j)%n,p)*x[j] for j in range(n))*iden+x[i]*pow((1-3*pow(w,i,p))%p,-1,p))%p
        assert direct==out[i]
        kernel_checks+=1
    # Reject an accidental FFT interpretation on raw, unrelated random data.
    Fourier_spot_mismatches=0;Fourier_checks=0
    for k in [0,1,2,3,n//7,n//5,n//3,n//2,n-1]:
        coeff=sum(x[j]*pow(w,(k*j)%n,p) for j in range(n))%p
        Fourier_checks+=1
        Fourier_spot_mismatches+=(coeff!=out[k])
    assert Fourier_spot_mismatches==Fourier_checks
    assert prep.inv==1 and online.inv==1
    assert (prep.total+online.total)<14*n
    return {'n':n,'modulus':p,'arbitrary_input':'independently seeded uniform random field samples',
            'all_cyclic_Green_equations_checked':n,'direct_kernel_rows_verified':kernel_checks,
            'independent_Fourier_bins_checked':Fourier_checks,'nonmatching_Fourier_bins':Fourier_spot_mismatches,
            'preparation_field_cost':prep.json(),'online_field_cost':online.json(),
            'total_field_operations':prep.total+online.total}

def main():
    r={'phase':13,'model':'exact finite prime fields (theorems over complex odd N)',
       'small':audit_small(),'prime_direction_enumeration':audit_prime_GL2(),
       'large_arbitrary_input_non_fourier_witness':audit_large(),
       'verdict':'Valid scoped algebraic and Green-branching results; NOT a new full-DFT algorithm.'}
    with open(OUT,'w') as f:json.dump(r,f,indent=2)
    print(json.dumps({'small_basis_checks':r['small']['basis_checks'],
         'all_GL2_bases':sum(x['all_generating_direction_pairs'] for x in r['prime_direction_enumeration']),
         'largest_n':r['large_arbitrary_input_non_fourier_witness']['n'],
         'work':r['large_arbitrary_input_non_fourier_witness']['total_field_operations']},indent=2))

if __name__=='__main__':main()
