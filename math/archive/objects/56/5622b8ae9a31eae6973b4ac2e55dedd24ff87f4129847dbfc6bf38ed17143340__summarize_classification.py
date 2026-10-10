"""Check bounded universe coverage and write human-readable classification indices."""
from pathlib import Path
import json,csv,collections,math
p=Path(__file__).parent
row=json.loads((p/'ORDER_SCREEN_RESULTS.json').read_text());dom=json.loads((p/'SURVIVOR_DOMAINS.json').read_text());completion=json.loads((p/'COMPLETION_SCREEN_RESULTS.json').read_text());positive=json.loads((p/'MINOR_POSITIVE_CONTROLS.json').read_text())
assert len(row['cycles'])==24 and row['pairs']==576
assert len({tuple(z['cycle'])for z in row['cycles']})==24
assert {(z['first'],z['second'])for z in row['results']}=={(i,j)for i in range(24)for j in range(24)}
for z in row['cycles']:
 cyc=z['cycle'];pp=z['permutation'];assert cyc[0]==0 and sorted(cyc)==list(range(5))
 assert all(pp[cyc[i]]==cyc[(i+1)%5]for i in range(5))
assert all(241%d for d in range(2,math.isqrt(241)+1))
omega=91;assert pow(omega,5,241)==1 and omega!=1
roots=[pow(omega,j,241)for j in range(5)];G=sum(roots[3*j*j%5]for j in range(5))%241;c=5*G%241
assert(G,c,(1+c)%241)==(103,33,34)
B=[[(roots[i*j%5]-G*roots[-3*(i+j)**2%5]+(c*roots[-3*i*i%5]if i==j else 0))*pow(34,-1,241)%241 for j in range(5)]for i in range(5)]
assert B==row['B']
by_pair=collections.defaultdict(list)
for z in completion['branches']:
 key=z['first'],z['second'];by_pair[key].append(z)
 assert z['column_nullspace_ranks']==[1]*5
 assert(z['rank_scale'],z['rank_augmented'])==(10,11)
 cert=z['augmented_minor_certificate'];assert cert['determinant']!=[0,0]
 assert len(cert['positions'])==len({tuple(q)for q in cert['positions']})==11
 assert sum(cert['row_multidegrees'])==sum(cert['column_multidegrees'])==6
 assert all(t>=0 for t in cert['row_multidegrees']+cert['column_multidegrees'])
 assert cert['nonzero_gauge_check']
for z in dom:
 key=z['first'],z['second'];assert len(by_pair[key])==2**len(z['members'])
 assert sorted(q['branch']for q in by_pair[key])==list(range(2**len(z['members'])))
 assert all(not d['unrestricted']and d['nonempty']for d in z['domains'])
assert len(dom)==len(by_pair)==192 and len(completion['branches'])==624
with(p/'ORDER_PAIR_SUMMARY.csv').open('w',newline='')as f:
 writer=csv.writer(f);writer.writerow(['first_order','second_order','first_cycle_starting_0','second_cycle_starting_0','closed_certificate_stage','row_components','finite_row_branches','nonzero_augmented_minors'])
 for z in row['results']:
  a,b=z['first'],z['second'];branches=by_pair.get((a,b),[])
  if z['status']=='REJECT':stage='row_projective_empty';assert not branches
  else:stage='augmented_projective_empty';assert branches
  writer.writerow([a,b,' '.join(map(str,row['cycles'][a]['cycle'])),' '.join(map(str,row['cycles'][b]['cycle'])),stage,z['components'],len(branches),len(branches)])
with(p/'CYCLE_INDEX.csv').open('w',newline='')as f:
 writer=csv.writer(f);writer.writerow(['index','cycle_starting_0','row_permutation'])
 for k,z in enumerate(row['cycles']):writer.writerow([k,' '.join(map(str,z['cycle'])),' '.join(map(str,z['permutation']))])
summary=dict(status='PASS',target='B=(F5^-1+diag(zeta^(3j^2)))^-1',complex_conclusion='No two Hamiltonian Green terms with arbitrary diagonal endpoints, including singular masks and zero edges; fixed coordinates.',prime=241,omega=91,G=G,c=c,target_denominator=34,extension='theta^2=7 over F241',Hamiltonian_orders=24,ordered_pairs=576,row_projective_rejections=384,finite_row_survivor_pairs=192,one_component_survivors=sum(len(z['members'])==1 for z in dom),two_component_survivors=sum(len(z['members'])==2 for z in dom),finite_row_branches=624,column_rank_one_checks=624*5,nonzero_augmented_minors=624,gauge_homogeneity_checks=624,all_augmented_scale_ranks=[10,11],invalid_target_guard_discards=0,guard_only_rejections_used=0,continuous_row_or_column_strata_omitted=0,unmatched_endpoint_permutations_covered=False,positive_boundary_controls=positive)
(p/'CLASSIFICATION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k!='positive_boundary_controls'},indent=2))
