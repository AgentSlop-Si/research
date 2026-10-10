"""Exact cyclotomic proof: the entire 11x9 Fourier gate is one polynomial.

Computes and checks all 55 maximal minors, without numeric fitting,
in integral Z[z]/(z^4+1)[h0,h1,h2,h6].
"""
from __future__ import annotations
import sys,itertools,hashlib,json,math,random
from pathlib import Path
ROOT=Path(__file__).parent
from prior_loader import activate;activate()
import _bootstrap
from exact_polynomial_gate import build,det_sparse,p1,pzero,add,pmul,pscale,cpowroot
from inverse_quartic import cmul,cadd,ONE,ZERO,poly_constant,poly_eval
from dual_support import primitive_root
from universal_gate import gate,det
from triple_gate import modrank
from polynomial_resultant import lift_poly

def make_basis(obj):
    U,L=obj['Uhat'],obj['Lhat']
    Y={}
    for j in (1,2,4,5):
        Y[j]=[]
        for i in range(4 if j==4 else 5):
            A=pscale(p1,cpowroot(i*j))
            B=add(*[pscale(U[k],cpowroot(i*k)) for k in range(j)])
            C=add(*[pscale(L[k],cpowroot(i*k)) for k in range(j+1,8)])
            Y[j].append([A,B,C])
    TT=Y[4]
    cof=[pscale(det_sparse([TT[r] for r in range(4) if r!=i]),((-1)**i,0,0,0)) for i in range(4)]
    ell=[add(*[pmul(cof[i],Y[1][i][j]) for i in range(4)]) for j in range(3)]
    A,B,C=Y[1],Y[2],Y[5]
    K=[]
    for i in range(5):K.append([*A[i],*[pscale(x,(-1,0,0,0)) for x in B[i]],pzero,pzero,pzero])
    for i in range(5):K.append([*A[i],pzero,pzero,pzero,*[pscale(x,(-1,0,0,0)) for x in C[i]]])
    K.append(ell+[pzero]*6)
    return Y,K

def exact_test():
    obj=build();Y,K=make_basis(obj)
    v=lambda i,k: poly_constant(cpowroot(i*k))
    V=[[v(i,k) for k in range(3)] for i in range(5)]
    vanishing_four_by_four=0
    for j in (1,2):
        for idx in (0,1,2):
            for I in itertools.combinations(range(5),4):
                mat=[[V[i][k] for k in range(3)]+[Y[j][i][idx]] for i in I]
                P=det_sparse(mat)
                assert P=={},('not in common Fourier subspace',j,idx,I,P)
                vanishing_four_by_four+=1
    # All 3x3 minors of Y2 must be constant times base Vandermonde minor.
    rootbase=det_sparse(V[:3])
    dbase=det_sparse(Y[2][:3])
    assert dbase==obj['DB']
    plucker_checks=0;constants=[]
    for I in itertools.combinations(range(5),3):
        dV=det_sparse([V[i] for i in I]);dY=det_sparse([Y[2][i] for i in I])
        assert pmul(dY,rootbase)==pmul(dbase,dV)
        plucker_checks+=1
        constants.append([list(I), list(next(iter(dV.values()))),list(next(iter(rootbase.values())))])
    # Because top block has row rank <=3 and bottom block only 5 rows,
    # any 9x9 minor not containing ell and all five bottom rows vanishes.
    rankminors=0;zero_minors=0
    for I in itertools.combinations(range(11),9):
        detI=det_sparse([K[i] for i in I])
        good=I[-1]==10 and (5,6,7,8,9)==I[3:8] and all(j<5 for j in I[:3])
        if good:
            rankminors+=1
            dbi=det_sparse([Y[2][i] for i in I[:3]])
            assert detI==pscale(pmul(dbi,obj['DH']),(-1,0,0,0)), ('special minor fails',I)
        else:
            assert detI=={},('unexpected nonzero minor',I,len(detI))
            zero_minors+=1
    assert rankminors==10 and zero_minors==45
    print('EXACT FOURIER SUBSPACE AND 55-MINOR COLLAPSE PASSED:',
          vanishing_four_by_four,'4x4 identities,',plucker_checks,'Plucker identities,',
          rankminors,'nonzero minors,',zero_minors,'zero minors.',flush=True)
    return dict(subspace_determinant_identities=vanishing_four_by_four,plucker_identities=plucker_checks,
                maximal_minors=55,structurally_zero_minors=45,
                nonzero_minors_with_common_factor=10,
                full_gate_equivalent_polynomial='Dhat=-DB*DH=0',
                DB_terms=len(obj['DB']),DH_terms=len(obj['DH']),
                Dhat_terms=len(obj['Dhat']),vandermonde_constants=constants)

def quadric_irreducibility():
    # Absolute irreducibility: homogenized symmetric quadratic form rank >=3,
    # certified by a 4x4 determinant in the finite characteristic!=2 field.
    obj=build();DB=obj['DB'];p=12289;z=primitive_root(p,8);inv2=pow(2,-1,p)
    S=[[0]*5 for _ in range(5)]
    for mon,c in DB.items():
        val=sum(int(c[j])*pow(z,j,p) for j in range(4))%p
        if len(mon)==1:i,j=mon[0],4
        elif len(mon)==2:i,j=mon
        else:raise AssertionError('unexpected DB monomial')
        if i==j:S[i][i]=(S[i][i]+val)%p
        else:
            v=val*inv2%p;S[i][j]=(S[i][j]+v)%p;S[j][i]=(S[j][i]+v)%p
    minor=det([row[:4] for row in S[:4]],p)
    assert minor==11251 and minor!=0,(minor,S)
    print('IRREDUCIBILITY CERTIFICATE: homogenized DB rank >=4 at p',p,'z',z,'minor',minor,flush=True)
    return dict(prime=p,primitive_root=z,homogenization_variables=['h0','h1','h2','h6','q'],
                upper_left_4x4_det=minor,
                homogeneous_quadratic_form_matrix=S,
                inference='rank >=4 over C; a reducible degree-2 polynomial over C would homogenize to product of two linear forms, whose symmetric matrix has rank <=2. Thus DB is absolutely irreducible over C.')

if __name__=='__main__':
    out={'exact_gate_collapse':exact_test(),'DB_irreducibility':quadric_irreducibility()}
    (ROOT/'COLLAPSE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
