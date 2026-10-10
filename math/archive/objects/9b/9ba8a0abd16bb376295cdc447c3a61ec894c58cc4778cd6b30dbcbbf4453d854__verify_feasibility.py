"""Exact small-field verification: full stacked-pencil feasibility via rank augmentation.
Works over GF(17) for N=4, with a primitive fourth root omega=4.
"""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=17
N=4
W=4

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%P for j in range(len(B[0]))] for i in range(len(A))]

def inv_scalar(a):
    return pow(a%P,-1,P)

def matrank(rows):
    if not rows:return 0
    M=[[int(v)%P for v in row] for row in rows]
    nr,nc=len(M),len(M[0]);r=0
    for col in range(nc):
        pivot=next((i for i in range(r,nr) if M[i][col]),None)
        if pivot is None:continue
        M[r],M[pivot]=M[pivot],M[r]
        mult=inv_scalar(M[r][col])
        M[r]=[(v*mult)%P for v in M[r]]
        for i in range(nr):
            if i!=r and M[i][col]:
                q=M[i][col]
                M[i]=[(x-q*y)%P for x,y in zip(M[i],M[r])]
        r+=1
        if r==nr:break
    return r

def E(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def Fourier(n=N,omega=W):return [[pow(omega,i*j,P) for j in range(n)] for i in range(n)]

def shifted_columns(B,j):
    return [B[i][j] for i in range(len(B))]

def build_pencils(A,B):
    n=len(A);phase=[pow(W,i,P) for i in range(n)]
    K=[]
    for j in range(n):
        K.extend([[(A[i][t]*(B[t][(j+1)%n]-phase[i]*B[t][j]))%P for t in range(n)] for i in range(n)])
    K0=K[:n]
    H=[[A[i][t]*B[t][0]%P for t in range(n)] for i in range(n)]
    return K,K0,H

def exact_condition(M,H):
    n=len(H);r=matrank(M)
    if r==n:return {'valid':False,'rank':r,'bad_coordinates':list(range(n)),'bad_seed_rows':list(range(n))}
    bad_coords=[i for i in range(n) if matrank(M+[E(n)[i]])==r]
    bad_seed=[i for i in range(n) if matrank(M+[H[i]])==r]
    return {'valid':not bad_coords and not bad_seed,'rank':r,'bad_coordinates':bad_coords,'bad_seed_rows':bad_seed}

def first_two_validity(A,B):
    K,K0,H=build_pencils(A,B)
    return exact_condition(K0,H),exact_condition(K,H)

def test_exact_solution(A,B):
    K,K0,H=build_pencils(A,B)
    found=None
    for t in range(P):
        # enumerate only for N=4
        pass
    for d0 in range(1,P):
        for d1 in range(1,P):
            for d2 in range(1,P):
                for d3 in range(1,P):
                    d=[d0,d1,d2,d3]
                    if any(sum(row[k]*d[k] for k in range(N))%P for row in K):continue
                    c=[sum(H[i][k]*d[k] for k in range(N))%P for i in range(N)]
                    if all(c):
                        found=d
                        D=[[d[i]*int(i==j) for j in range(N)] for i in range(N)]
                        M=matmul(matmul(A,D),B)
                        L=[[int(i==j)*inv_scalar(c[i]) for j in range(N)] for i in range(N)]
                        assert matmul(L,M)==Fourier()
                        return found
    return found


def main():
    F=Fourier();I=E(N)
    # Positive full Fourier instance
    pfirst,pfull=first_two_validity(F,I)
    assert pfirst['valid'] and pfull['valid']
    assert test_exact_solution(F,I) is not None
    # Singular phase pencil, but kernel forces zero middle gauge entries.
    badfirst,badfull=first_two_validity(I,I)
    assert not badfirst['valid'] and badfirst['rank']<N
    assert len(badfirst['bad_coordinates'])>0
    assert test_exact_solution(I,I) is None
    # First two Fourier columns can match with d all nonzero,
    # but the seed vector A D b0 has an unavoidable zero row.
    Bseed=[ [1,0,0,0], [1,1,0,0], [0,1,1,0], [0,0,0,1] ]
    assert matrank(Bseed)==N
    seedfirst,seedfull=first_two_validity(F,Bseed)
    assert seedfirst['rank']<N
    assert not seedfirst['bad_coordinates']
    assert len(seedfirst['bad_seed_rows'])>0
    assert not seedfirst['valid']
    assert test_exact_solution(F,Bseed) is None
    # First two columns can match including nonzero first column,
    # but a corrupted THIRD B column ruins global covariance.
    Bthird=[ [1,0,1,0], [0,1,0,0], [0,0,1,0], [0,0,0,1] ]
    assert matrank(Bthird)==N
    thirdfirst,thirdfull=first_two_validity(F,Bthird)
    assert thirdfirst['valid']
    assert not thirdfull['valid']
    assert test_exact_solution(F,Bthird) is None
    result={'field':f'GF({P})','N':N,'primitive_root':W,
            'true_fourier':{'two_columns':pfirst,'all_columns':pfull},
            'singular_pencil_but_zero_gauge':{'two_columns':badfirst,'all_columns':badfull},
            'unavoidable_seed_zero':{'two_columns':seedfirst,'all_columns':seedfull},
            'third_column_corrupted':{'two_columns':thirdfirst,'all_columns':thirdfull}}
    (HERE/'FEASIBILITY_RESULTS.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
