"""Small, exact all-basis implementation audit of the fused high-degree macro."""
import json
from pathlib import Path
from fused_tail import prepare,apply,prepare_rank_one,apply_rank_one,oracle_fused_tail


def main():
    rows=[]
    basis_vectors=0
    for prime in (65537,998244353):
        for n in (2,4,8,16,32,64):
            q=pow(3,(prime-1)//n,prime)
            assert pow(q,n,prime)==1 and pow(q,n//2,prime)!=1
            for r in sorted({1,min(2,n),min(4,n),n//2,n}):
                for mode in ('H_tail','integer_tail'):
                    coefficients=None if mode=='H_tail' else [(2,-3,5,1)[j%4]%prime for j in range(r)]
                    plan=prepare(prime,n,r,q,coefficients)
                    expected_prep={'mul':7*n-5+n.bit_length()-1+r*(r+1),
                                   'sub':2*n-2,'constant_inverse':1,'neg':n-1}
                    assert plan.preparation==expected_prep
                    if r==1:
                        extra=prepare_rank_one(plan)
                        assert extra=={'mul':n}
                        if mode=='H_tail':
                            assert plan.tail_matrix[0][0]==pow(q,-1,prime)
                            assert plan.rank_one_kernel==[pow(q,-1,prime)*t%prime for t in plan.kernel]
                    for j in range(n):
                        x=[int(i==j) for i in range(n)]
                        result,cost=apply(plan,x)
                        assert result==oracle_fused_tail(plan,x)
                        expected_action={'mul':r*(n+1)}
                        if r>1:
                            expected_action['add']=n*(r-1)
                        assert cost['field_operations']==expected_action
                        if r==1:
                            specialized,special_cost=apply_rank_one(plan,x)
                            assert specialized==result
                            assert special_cost['field_operations']=={'mul':n}
                        if j<n-r:
                            assert all(v==0 for v in result)
                        basis_vectors+=1
                    x=[(j*j+7*j+3)%prime for j in range(n)]
                    result,cost=apply(plan,x)
                    assert result==oracle_fused_tail(plan,x)
                    rows.append({'prime':prime,'n':n,'r':r,'coefficient_mode':mode,
                                 'basis_vectors':n,'preparation':plan.preparation,
                                 'action':cost,'all_equalities_passed':True})
    report={'status':'PASS','cases':len(rows),'basis_vectors':basis_vectors,
            'scope':'Exact high-degree tail macro; no full Fourier speedup.',
            'cases_detail':rows}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases_detail'},indent=2))


if __name__=='__main__':
    main()
