"""Phase18: Fourier's two sparse intertwining identities (exact prime-field checks)."""
import json
from harper_certificate import P,root_n
from weyl_gate import fourier_matrix,sum_two_green,mm
import random


def defects(M,omega):
    n=len(M)
    phases=[(pow(omega,j,P)+pow(omega,-j,P))%P for j in range(n)]
    defect_T=0;defect_V=0
    for i in range(n):
        for k in range(n):
            defect_T+=((M[i][(k+1)%n]+M[i][(k-1)%n]-phases[i]*M[i][k])%P!=0)
            defect_V+=((phases[k]*M[i][k]-M[(i+1)%n][k]-M[(i-1)%n][k])%P!=0)
    return defect_T,defect_V


def control(n):
    w=root_n(n);F=fourier_matrix(n,w)
    assert defects(F,w)==(0,0)
    JF=[[F[i][(-j)%n] for j in range(n)] for i in range(n)]
    assert defects(JF,w)==(0,0)
    M=[[(3*F[i][j]+5*JF[i][j])%P for j in range(n)] for i in range(n)]
    assert defects(M,w)==(0,0)
    assert [M[i][1] for i in range(n)] != [F[i][1] for i in range(n)]
    assert [F[i][1] for i in range(n)]==[pow(w,i,P)*F[0][1]%P for i in range(n)]
    return {'n':n,'Fourier_sparse_intertwiners':True,'inverse_Fourier_sparse_intertwiners':True,
            'arbitrary_linear_combination_intertwiners':True,
            'one_probe_column_separates_Fourier':True}


def negative(n):
    rng=random.Random(1804+n);w=root_n(n)
    A=sum_two_green(n,rng,w);B=sum_two_green(n,rng,w);M=mm(A,B)
    dt,dv=defects(M,w)
    assert dt>0 and dv>0
    return {'n':n,'green_sums_product_first_sparse_defect_nonzeros':dt,
            'green_sums_product_second_sparse_defect_nonzeros':dv}

if __name__=='__main__':
    print(json.dumps({'controls':[control(n) for n in (4,8,16,32,64,128)],
                      'product_samples':[negative(n) for n in (8,16,32,64)]},indent=2))
