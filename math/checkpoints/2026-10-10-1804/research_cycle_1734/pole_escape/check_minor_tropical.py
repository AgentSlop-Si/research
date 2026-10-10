"""Fresh exact 2x2-minor tropical checks via vertex-disjoint directed paths."""
import json,pathlib,itertools,collections
root=pathlib.Path(__file__).resolve().parent
L=json.loads((root/'topology_11.json').read_text())['layers']
w=json.loads((root/'tropical_pole_witness.json').read_text())['weights']
P=collections.defaultdict(list)
for a,(u,j) in enumerate(L[0]):
 for b,(v,ub) in enumerate(L[1]):
  if ub!=u:continue
  for c,(i,vc) in enumerate(L[2]):
   if vc==v:P[i,j].append({'edges':(a,33+b,66+c),'internal':(u,v)})
allchecks=[];failed=[];hist=collections.Counter()
for rows in itertools.combinations(range(11),2):
 for cols in itertools.combinations(range(11),2):
  families=[]
  for sign,os in [(1,rows),(-1,rows[::-1])]:
   for p,q in itertools.product(P[os[0],cols[0]],P[os[1],cols[1]]):
    if any(a==b for a,b in zip(p['internal'],q['internal'])):continue
    es=tuple(sorted(p['edges']+q['edges']))
    families.append({'sign':sign,'edges':es,'valuation':sum(w[e] for e in es)})
  # Distinct vertex-disjoint paths cannot yield the same edge set.
  assert len({tuple(x['edges']) for x in families})==len(families)
  vals=[f['valuation'] for f in families];m=min([1]+vals);cnt=([1]+vals).count(m)
  rec={'rows':rows,'cols':cols,'family_count':len(families),'minimum':m,'minimum_count_including_target':cnt,'families':families}
  hist[(m,cnt)]+=1
  allchecks.append(rec)
  if cnt<2:failed.append(rec)
receipt={'checked_minors':len(allchecks),'failed_minors':len(failed),'passed_minors':len(allchecks)-len(failed),'first_failed':failed[0] if failed else None,'minimum_histogram':[[list(k),v] for k,v in sorted(hist.items())],'failed_minor_coordinates':[[r['rows'],r['cols']] for r in failed],'scope':'Normalized witness only; necessary 2x2 Fourier-minor conditions, not a global pole exclusion.'}
(root/'minor_tropical_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(root/'minor_tropical_full_certificate.json').write_text(json.dumps(allchecks,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['failed_minor_coordinates','minimum_histogram']},indent=2))
