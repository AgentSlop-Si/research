"""Fresh reviewer-authored arithmetic and metadata checks; no supplied code execution."""
from fractions import Fraction
from pathlib import Path
import json,re,hashlib
P=Path(__file__).parent
rows=json.loads((P/'SOURCE_INDEX.json').read_text())
tests=[]
for r in rows:
 lines=(P/r['snapshot']).read_text().splitlines()
 declared=[i for i,s in enumerate(lines,1) if re.match(r'\s+def test_',s)]
 mains=[i for i,s in enumerate(lines,1) if 'unittest.main(' in s]
 if declared:tests.append({'index':r['index'],'sha256':r['sha256'],'test_declaration_lines':declared,'unittest_main_lines':mains,'discovery_declarations':len(declared),'direct_before_first_main':sum(i<mains[0] for i in declared) if mains else None,'method':'lexical line matching only, not AST or execution'})
x=float(2**53)
naive=(x+1.0)-x
exact=Fraction(2**53)+1-Fraction(2**53)
a=-1.0+2.0**-52
separate=a*1e16+1e16
combined=(a+1.0)*1e16
result={'method':'fresh independent reviewer arithmetic; no imports/exec/eval/compile/AST of supplied text','cancellation':{'float_large_sum':naive,'exact_large_sum':str(exact),'separate_products':separate,'combined_factor':combined,'exact_fraction':str((Fraction(a)+1)*10**16)},'promotion_work':{'model':'copy r*q complex128 elements on default eighth query before H==0 branch','q':8,'r_cases':[1,100,10000],'copy_bytes':[16*8*r for r in [1,100,10000]],'scope':'arithmetic operation-count witness from reviewed control flow; no engine execution'},'test_declarations':tests}
assert naive==0.0 and exact==1 and separate==2.0 and combined>2.2
(P/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Fresh arithmetic checks passed; lexical test declarations',sum(x['discovery_declarations'] for x in tests))
