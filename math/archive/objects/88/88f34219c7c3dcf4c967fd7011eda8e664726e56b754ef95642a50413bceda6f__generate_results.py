from __future__ import annotations
import json
from pathlib import Path
from two_line_weyl import *


def main():
    data={'rank_dichotomy':[],'factorizations':[],'line_classification':[]}
    for n in (5,7):
        p,w=field_for_length(n)
        independent=good=bad=0
        ranks={}
        for u in all_nonzero_vectors(n):
            for v in all_nonzero_vectors(n):
                if det2(u,v,n)==0:continue
                independent+=1
                k=compatibility_kappa(u,v,n)
                r=matrix_rank(dephased_fourier_tensor(n,p,w,u,v),p)
                ranks[str(r)]=ranks.get(str(r),0)+1
                if k==0:good+=1
                else:bad+=1
                assert r==(1 if k==0 else n)
        data['rank_dichotomy'].append({'N':n,'field':p,'independent_pairs':independent,'factorable_pairs':good,'nonfactorable_pairs':bad,'rank_histogram':ranks})
    cases=[(7,(1,0),1),(7,(1,2),2),(11,(2,3),1),(13,(2,2),1),(17,(0,1),1)]
    for n,u,t in cases:
        p,w=field_for_length(n);v,A,B=exact_two_line_factorization(n,p,w,u,t);F=fourier_matrix(n,p,w)
        data['factorizations'].append({'N':n,'field':p,'u':u,'v':v,'scale':t,'exact':mat_eq(mat_mul(A,B,p),F,p),'rank_A':matrix_rank(A,p),'rank_B':matrix_rank(B,p),'u_vertical':u[0]%n==0,'v_vertical':v[0]%n==0})
    for n in (5,7,11,13,17):
        p,w=field_for_length(n)
        full=rank1=vertical=nonvertical=0
        for u in all_nonzero_vectors(n):
            A=line_operator(n,p,w,u);r=matrix_rank(A,p)
            if qnorm(u,n)==0:
                rank1+=1;assert r==1
            else:
                full+=1;assert r==n
                if u[0]%n==0:vertical+=1
                else:nonvertical+=1
        data['line_classification'].append({'N':n,'field':p,'full_rank_anisotropic_lines':full,'rank_one_isotropic_lines':rank1,'vertical_full_rank_directions':vertical,'nonvertical_fourier_equivalent_directions':nonvertical})
    data['theorem_summary']={
        'pair_tensor_rank':'1 if kappa=0, otherwise N',
        'compatibility':'v=t*(a-b,a+b), with qnorm(u)!=0',
        'factors':'quadratic chirp line operators, unique up to one nonzero scalar',
        'hardness':'every nonvertical anisotropic line factor is diagonally/permutationally Fourier-equivalent',
        'bad_pair_sum_gate':'a sum of r fixed-pair products needs r>=N when kappa!=0',
        'rational_scan_gate':'if factor=q(C)^(-1)p(C), deg(q)>=floor((N-deg(p))/2) for a prime-length Fourier-equivalent factor'
    }
    path=Path(__file__).with_name('results.json');path.write_text(json.dumps(data,indent=2,sort_keys=True))
    print(json.dumps(data,indent=2,sort_keys=True))
if __name__=='__main__':main()
