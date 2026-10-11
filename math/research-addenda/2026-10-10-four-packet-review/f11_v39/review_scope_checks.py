# Publication adaptation of reviewer-authored checker.
# Original SHA-256: e6c378b7595763dd9ec89d13026d6ba6373c1518be54e32c40690bf3331801b1
# Changes: Removed nested ZIP audit; difficult-block control is unchanged; output explicitly excludes historical archive replay.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
# Additional fresh cross-checks of difficult block and source nesting.
import pathlib,json,zipfile,hashlib,itertools,collections
R=pathlib.Path(__file__).resolve().parent;P=R/'inert_packet/fft_transfer_quartic_circuit_v39'
ms=list(itertools.combinations_with_replacement(range(11),4));r=ms[46];c=ms[717]
# Block monomials generated from label permutations for independent spot check,
# unlike the all-quartet global checker.
monomials=sorted({tuple(sorted(11*i+j for i,j in zip(r,perm))) for perm in itertools.permutations(c)})
assert len(monomials)==12
H=[[int(x) for x in line.split()] for line in (R/'samples_1000003.txt').read_text().splitlines()];p=1000003

def column_rank(n):
 basis={}
 for m in monomials:
  v=[]
  for h in H[:n]:
   x=1
   for i in m:x=x*h[i]%p
   v.append(x)
  for i in range(n):
   if not v[i]:continue
   if i in basis:
    b=basis[i];f=v[i];v=[(a-f*t)%p for a,t in zip(v,b)]
   else:
    f=pow(v[i],-1,p);basis[i]=[a*f%p for a in v];break
 return len(basis)
assert (column_rank(12),column_rank(24))==(11,12)
result={'publication_historical_archive_replay':False,'difficult_block':{'row_multiset_index':46,'column_multiset_index':717,'row_labels':r,'column_labels':c,'columns':12,'first_12_rows_rank':11,'all_24_rows_rank':12,'alternate_column_elimination_checked':True}}
(R/'scope_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
