"""Exact rational verifier for additional candidate JSON, independently
expanding determinant monomials and checking every entry and 2x2 minor.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import json,collections,sys,hashlib
P=Path(__file__).resolve().parent
T=json.loads(Path('research_cycle_1635/v34_independent_audit/source/extracted/fft_cyclotomic_zero_forcing_v34/topology_11.json').read_text());L=T['layers']
adj=[]
for layer in L:
 a={i:[] for i in range(11)}
 for k,(v,u) in enumerate(layer):a[u].append((v,k))
 adj.append(a)
paths={}
for j in range(11):
 for u,a in adj[0][j]:
  for v,b in adj[1][u]:
   for i,c in adj[2][v]:paths.setdefault((i,j),[]).append((a,33+b,66+c))
minors=[]
for i,j in combinations(range(11),2):
 for k,l in combinations(range(11),2):
  poly=collections.defaultdict(int)
  for sign,pair1,pair2 in [(1,(i,k),(j,l)),(-1,(i,l),(j,k))]:
   for a in paths[pair1]:
    for b in paths[pair2]:poly[tuple(sorted(a+b))]+=sign
  minors.append({'rows':[i,j],'cols':[k,l],'terms':{a:c for a,c in poly.items() if c}})
for name in sys.argv[1:]:
 src=Path(name);data=json.loads(src.read_text())
 if 'weights' not in data:
  print(src.name+': no candidate; no mathematical exclusion certified.');continue
 w=[F(*a) if isinstance(a,list) else F(a) for a in data['weights']];assert len(w)==99
 badentries=[];neg=[]
 for pair,ps in sorted(paths.items()):
  vals=[sum(w[e] for e in path) for path in ps];m=min([F(0)]+vals)
  if ([F(0)]+vals).count(m)<2:badentries.append(pair)
  if m<0:neg.append(pair)
 badminors=[]
 for z,mr in enumerate(minors):
  vals=[sum(w[e] for e in mon) for mon in mr['terms']];m=min([F(1)]+vals)
  if ([F(1)]+vals).count(m)<2:
   badminors.append({'index':z,'rows':mr['rows'],'cols':mr['cols'],'minimum':str(m),'terms':[{'edges':mon,'coefficient':co,'valuation':str(sum(w[e] for e in mon))} for mon,co in mr['terms'].items()]})
 result={'candidate_file':str(src),'candidate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'status':'PASS_EXACT_VERIFICATION','entries_checked':121,'failed_entries':badentries,'negative_entry_count':len(neg),'minors_checked':3025,'failed_minor_count':len(badminors),'failed_minor_indices':[m['index'] for m in badminors],'first_failed_minor':badminors[0] if badminors else None,'scope':'A necessary-condition check only. Failure excludes this candidate; success does not establish a lift.'}
 (P/(src.stem+'_REVIEW.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
