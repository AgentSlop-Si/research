# Publication adaptation of reviewer-authored checker.
# Original SHA-256: cc7331df8a78185e74fd537ed234e5afcb30c7a6f0737888bdd9d8c9c297ccef
# Changes: Omitted provider/provenance receipt assembly and earlier-review path dependencies; all mathematical result assertions unchanged.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
import pathlib,json,hashlib,platform,subprocess,math
import numpy
R=pathlib.Path(__file__).resolve().parent

def readlog(name):
 d={};hist={};extra=[]
 for line in (R/name).read_text().splitlines():
  words=line.split()
  if words[0]=='HIST':hist[words[1]]=int(words[2])
  elif words[0]=='EXTRA_ROWS':extra.append(list(map(int,words[1:])))
  else:d[words[0]]=float(words[1]) if words[0]=='SECONDS' else int(words[1])
 if hist:d['block_histogram']=hist
 if extra:d['extra_rows']=extra
 return d
one=readlog('global_1000003.log');two=readlog('global_1000033.log');negative=readlog('negative_control.log');selected=readlog('selected_pivots.log')
expected={'1':21901,'2':24200,'3':111925,'4':127050,'6':36300,'7':245025,'12':326700,'24':108900}
for prime,v,first in [(1000003,one,1),(1000033,two,0)]:
 assert v['PRIME']==prime and v['BLOCKS']==1002001 and v['COLUMNS']==9381251 and v['GENERATED']==math.comb(124,4)
 assert v['block_histogram']==expected and v['FINAL_DEFICIENT']==0 and v['INITIAL_DEFICIENT']==first
 assert sum(expected.values())==v['BLOCKS'] and sum(int(k)*n for k,n in expected.items())==v['COLUMNS']
assert one['extra_rows']==[[46,717,12,11,12]]
assert negative['BLOCKS']==20020 and negative['FINAL_DEFICIENT']==18810
# Avoid duplicating every deliberately deficient control block in the result.
negative.pop('extra_rows')
assert selected=={'COLUMNS':1663740,'TERMS':21770715,'DISTINCT_EDGE_MONOMIALS':19337020,'UNIT_PIVOTS':1663740,'CROSS_COLUMN_PIVOT_OCCURRENCES':32223,'ALL_CROSS_OCCURRENCES_STRICTLY_EARLIER':1,'ALL_PIVOTS_DISTINCT':1,'ALL_OWN_COEFFICIENTS_ONE':1}
res={'review_utc_date':'2026-10-10','status':'complete fresh replay passed','global_prime_1000003':one,'global_prime_1000033':two,'negative_control':negative,'selected_unit_pivots':selected,'selected_preparation':json.loads((R/'selected_preparation.json').read_text()),'scope_checks':json.loads((R/'scope_checks.json').read_text()),'global_scope':'Formal transfer polynomials of total degree at most four: characteristic zero and characteristics 1000003 and 1000033.','selected78_scope':'Formal selected-transfer polynomials of total degree at most four over every field.','target_specialized_parameter_eliminations':'Not excluded or contradicted; retain the existing guards and scope of E25/E41 and resultant chains.','uploaded_or_inherited_research_programs_executed':False,'all_global_blocks_replayed':True,'all_selected_pivot_occurrences_replayed':True,'external_writes_performed':False}
(R/'independent_replay_results.json').write_text(json.dumps(res,indent=2)+'\n')
print('All complete mathematical replay outputs passed exact expectations. Historical archive replay was omitted.')
