from pathlib import Path
import json
import sympy as s
P=Path(__file__).resolve().parent
D=json.loads((P/'ALL_MONOMIAL_MINORS.json').read_text())
C=json.loads(Path('research_cycle_1734/pole_escape/monomial_linear_consistency_certificate.json').read_text())
rows=[];rhs=[]
for c in D['certificates']:
 row=[0]*99
 for e in c['edges']:row[e]+=1
 rows.append(row);rhs.append(c['required_valuation'])
cols=C['pivot_columns'];assert len(cols)==26 and len(set(cols))==26
mat=s.Matrix([[row[i] for i in cols] for row in rows]);det=mat.det(method='domain-ge')
assert det==-1 and str(det)==C['square_submatrix_determinant']
w=[int(x) for x in C['explicit_solution']]
assert len(w)==99 and [i for i,v in enumerate(w) if v]==[17,31,32] and all(w[i]==1 for i in [17,31,32])
assert all(sum(a*b for a,b in zip(row,w))==v for row,v in zip(rows,rhs))
R=json.loads((P/'REVIEW_RECEIPT.json').read_text())
e=next(e for e in R['exact_tropical_entries'] if (e['output'],e['input'])==(0,4))
vals=[sum(w[i] for i in path) for path in e['paths']];assert min(vals)>0
out={'status':'PASS','determinant':int(det),'necessary_linear_equations_verified':26,'nonzero_weight_indices':[17,31,32],'all_nonzero_weights':1,'failed_entry':[0,4],'path_values_for_failed_entry':vals,'scope':'Only26 monomial valuation equations are satisfied; not entrywise tropical feasibility.'}
(P/'MONOMIAL_RANK_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
