from pathlib import Path
import json, hashlib, copy, collections, shutil, datetime, html, csv, zipfile
ROOT=Path('research_cycle_0958')
OUT=ROOT/'integration/next_version_v2'
BASE=ROOT/'integration/final_v6/STATUS_REGISTER.json'
if (OUT/'FINAL_MANIFEST.json').exists(): raise SystemExit('Frozen supplement: create a new version rather than overwrite approved outputs.')
def load(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def uniq(xs): return list(dict.fromkeys(xs))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
base=load(BASE); reg=copy.deepcopy(base)
reg['version']='cycle-0958-local-supplement-v2'
reg['as_of_utc']=now
reg['delivery_state']='LOCAL_ONLY_NOT_UPLOADED_NOT_WRITTEN_TO_SHEET'
reg['baseline']={'register':str(BASE),'sha256':sha(BASE),'accepted_checkpoint':base['acceptance_checkpoint'],'preserved_files':load(OUT/'BASELINE_HASHES.json')}
reg['scope'].update({'all_178_proofs_audited':False,'existing_view_rows':30,'catalogue_statement_rows':178,'prior_sheet_unchanged':True,'supplied_research_programs_executed':False,'worldwide_novelty_certified':False,'no_new_discovery_count':True})
reg['count_warning']='Counts describe overlapping audit tasks, receipts, views, or finite controls. None is a count of independent discoveries or production-ready algorithms.'
reg['status_definitions'].update({'constructionopen':'Accepted tests/obstructions do not settle every specified constructive target.','certificateopen':'Fresh exhaustive or independent certificate obligation remains.','mixedscopes':'Read individual accepted, rejected and open rows; no blanket acceptance.'})
reg['independent_review_baseline']=copy.deepcopy(base['independent_review'])
reg['supplement_review_ledgers']=[]
rows=[]
for name in ['supplement_v1','supplement_v2','supplement_v3','supplement_v4']:
 p=ROOT/'review'/name
 if not (p/'ACCEPTANCE_RECEIPT.json').exists(): continue
 receipt=load(p/'ACCEPTANCE_RECEIPT.json'); ledger=load(p/'review_ledger.json')
 reg['supplement_review_ledgers'].append({'id':name,'receipt_path':str(p/'ACCEPTANCE_RECEIPT.json'),'receipt_sha256':sha(p/'ACCEPTANCE_RECEIPT.json'),'receipt':receipt,'ledger_path':str(p/'review_ledger.json'),'ledger_sha256':sha(p/'review_ledger.json'),'rows':ledger['rows']})
 for row in ledger['rows']:
  a=copy.deepcopy(row);a['review_ledger_id']=name; a.setdefault('proof_scope',a.get('scope','')); a.setdefault('remaining_obligation','Read listed exact scope and the ledger open/rejected rows.'); rows.append(a)
reg['independent_review']={'baseline':base['independent_review'],'supplement_rows':rows,'policy':'Exact scoped decisions only. Historical rows remain preserved in their original ledgers; later decisions supersede only explicitly identified scopes.'}
byrid={a['id']:a for a in rows}
sources=[]
def source(sid,title,path,review_ids=(),kind='reviewed_proof',copy_to_pack=True):
 path=Path(path)
 if not path.exists(): return None
 if not path.is_absolute() and path.parts[0]!='research_cycle_0958': path=ROOT/path
 if not path.exists(): return None
 accepted=[i for i in review_ids if i in byrid and byrid[i]['verdict']=='ACCEPT']
 s={'id':sid,'title':title,'source':str(path),'sha256':sha(path),'review_ids':list(review_ids),'kind':kind,'independently_reviewed_exact_hash': bool(accepted) and all(byrid[i].get('reviewed_artifact_sha256')==sha(path) for i in accepted)}
 if copy_to_pack:
  dest=OUT/'evidence'/f'{sid}{path.suffix}';dest.parent.mkdir(exist_ok=True);shutil.copy2(path,dest);s['member']=str(dest.relative_to(OUT))
 sources.append(s);return s
source('SP01','Mask proof and scoped finite certificates',ROOT/'review/supplement_v1/sources/masks/THEOREMS_AND_DISPOSITIONS.md',['S01','S02','S03','S04','S05','S17','S18'])
source('SP02','Composite RS guarded extension',ROOT/'review/supplement_v1/sources/composite/COMPOSITE_GUARD_EXTENSION.md',['S06','S07','S08','S09','S19'])
source('SP03','Inverse multiplier preparation contract',ROOT/'review/supplement_v1/sources/inverse/INVERSE_MULTIPLIER_CONTRACT.md',['S10','S11','S12','S13','S20'])
source('SP04','Fixed F60 exact identities and norm certificate',ROOT/'review/supplement_v1/sources/fixed60/FIXED60_EXACT_AND_NORM_CERTIFICATE.md',['S14','S15','S16'])
source('SP05','Phase41 theorems and finite Jacobian audit',ROOT/'review/supplement_v2/sources/phase41/THEOREMS_AND_AUDIT.md',['I01','I02','I03','I05'])
source('SP06','Fixed-branch separator fusion',ROOT/'review/supplement_v2/sources/phase41_fusion/FIXED_BRANCH_SEPARATOR_FUSION.md',['I04'])
source('SP07','Magnetic Green average proof and model audit',ROOT/'review/supplement_v2/sources/hero17/PHASE18_PROOF_AND_MODEL_AUDIT.md',['I06','I07','I08','I09','I11','I28','I29'])
source('SP08','Sparse magnetic sectors and triangular support',ROOT/'review/supplement_v2/sources/hero17_extension/SPARSE_WEIGHT_AND_TRIANGULAR_SUPPORT_FUSION.md',['I10'])
source('SP09','Corrected primitive Weyl covariance audit',ROOT/'review/supplement_v2/sources/weil/PROOFS_AND_DISPOSITIONS.md',['I12','I13','I14','I15','I16','I17','I18'])
source('SP10','Rational Fourier channel audit',ROOT/'review/supplement_v2/sources/rational/THEOREMS_AND_AUDIT.md',['I19','I20','I21','I22','I23','I24','I26','I27'])
source('SP11','Fresh inherited C01 and F015 audit',ROOT/'inherited_reaudit/final_v1/AUDIT.md',[],kind='independent_review_pending')
source('SP12','Exhaustive N16 cubic mask certificate',ROOT/'masks/n16_supplement/N16_THEOREM_AND_CERTIFICATE.md',[],kind='independent_review_pending')
for old_source in reg['sources']:old_source['member_origin']='Previously delivered baseline proof pack, not this delta pack'
for new_source in sources:new_source['member_origin']='This supplement'
reg['sources'].extend(sources)
source_by={s['id']:s for s in reg['sources']}
tasks={t['queue_id']:t for t in reg['tasks']}
def patch(q,result,proof,activity,construction,implementation,priority,remaining,reviewids,sourceids):
 t=tasks[q]
 t.update({'current_result':result,'proof_state':proof,'task_state':activity,'status':activity,'proof_closed':proof in ['proofclosed','conditionalclosed','guardedclosed'],'construction_state':construction,'implementation_state':implementation,'priority_state':priority,'remaining_obligation':remaining,'next_actions':[remaining],'publication_readiness':'Read scoped proof, priority and implementation fields separately; no worldwide novelty certification.'})
 t['review_ids']=uniq(t.get('review_ids',[])+reviewids);t['source_ids']=uniq(t.get('source_ids',[])+sourceids)
 t['review_records']=t.get('review_records',[])+[byrid[i] for i in reviewids if i in byrid]
 t['source_hashes']=t.get('source_hashes',[])+[{'id':i,'sha256':source_by[i]['sha256'],'member':source_by[i].get('member'),'exact_reviewed_hash':source_by[i].get('independently_reviewed_exact_hash',False)} for i in sourceids]
patch('Q26','Accepted homogeneous Macaulay exclusion, guarded lifting, N4/N8 exhaustive no-factorization and constrained open-set theorem. N16 fresh complete cubic enumeration in both primes is separately awaiting independent acceptance.','certificateopen','reviewpending','No factorization constructed; rank deficiency alone would not construct one.','N4/N8 reviewer replay accepted. N16 owner reconstruction: 10,483,200 distinct mappings per prime, cubic only; supplied executors unexecuted.','Specific formulation priority unresolved; no all-N claim.','Accept the separate N16 final hash; retain N32 sampled-only status and all frozen graph/coupling guards.',['S01','S02','S03','S17'],['SP01','SP12'])
patch('Q27','Target-fiber equivalence and four-ratio local dominance are accepted. Phase41 separately excludes two unitary-cycle summands for N>8 and gives fixed-branch ceilings. Surviving full target fibers remain open.','constructionopen','active','Guarded full-matrix Fourier target identity missing in surviving size/model; local dominance and partial numerical fits are insufficient.','Exact local finite controls accepted; no production constructor.','Classical compatibility/dimension ingredients; exact obstruction priority remains scoped and unresolved.','Choose one surviving chart; prove an exact all-row identity or target-specific exclusion with all guards, then charge synthesis and precision.',['S04','S05','S18','I01','I02','I03','I04','I05'],['SP01','SP05','SP06'])
patch('Q29','Accepted parity-complete inverse Hermite pairing with its exact exception, augmented same-component criterion, and unconditional composite families d=sp for s in {3,7,11}, every prime p=1 mod4.','guardedclosed','active','All-composite and repeated-prime extension open.','Abstract theorem with independent exact reduced-content and adverse-component controls.','Classical antecedents explicit; narrow application priority unresolved pending full-paper incorporation.','Prove augmented-content prime support and lower guards for general s; repeated-prime cases need separate analysis. Resonance at -1 and legal scalar-bank minima are unchanged.',['S06','S07','S08','S09','S19'],['SP02'])
patch('Q30','Accepted conditional inverse transfer, corrected full-chirp bounded-word sup-norm preparation, exact-field boundary recurrence and root-specific singularity countercontrols. General bounded-word magnetic inverse preparation remains open.','conditionalclosed','active','Full-chirp subclass constructed under its word model; general stable spectrum gap/preparation missing.','Fresh controls only; exact-field O(N) recurrence does not establish bounded-word robustness, bit cost, or production speed.','Spectral transfer and Stieltjes-Wigert mechanism classical; no novel generic inverse claim.','Provide stable sup-norm multiplier preparation and useful complex spectral floor under the compiler word/range contract; include precision and full costs.',['S10','S11','S12','S13','S20','I11'],['SP03','SP07'])
patch('Q32','Accepted F60 characteristic-zero factorization, fixed graph count and norm/coefficient-error route. Generic-field assertion of exactly 17 setup products is rejected by the F61 specialization.','proofclosed','proofclosed','Fixed kernel algebra closed; no growing-radix construction or global optimum established.','Production validation open: internal rounding budget and supported-field/count repair required; 444 additions and 69 prepared scalars are scoped graph counts.','Fixed-size arithmetic and classical factorization mechanisms do not establish asymptotic novelty.','Repair universal setup-count assertion, certify graph-wise internal rounding and actual coefficient preparation, then benchmark the full charged implementation.',['S14','S15','S16'],['SP04'])
# Preserve inherited proof acceptance while separately identifying the new certificate-review boundary.
patch('Q11','Inherited five-dimensional exact Green-length theorem retained; fresh 576-pair/624-branch lower-certificate reconstruction and upper guards are available, with second review pending.','proofclosed','reviewpending','Exact N5 construction retained; no full-B upper bound beyond N5.','Fresh independent author reconstruction; second-review receipt pending. No production or stability result.','Exact additive-length application priority remains unresolved; Green structure is classical.','Finish second-review acceptance of fresh C01 audit/certificates; then retain priority and any larger-N extension as separate obligations.',[],['SP11'])
patch('Q14','Inherited cap and aggregate growing-fiber theorems have now received a fresh full-text audit and fresh exact controls; second-review acceptance pending.','proofclosed','reviewpending','Original cap/aggregate algorithms retained with supplied roots and guarded Green domain.','Fresh exact controls; no new bit-complexity, stability or production validation.','Classical transform ingredients; exact intermediate-fiber/rejection interface remains unresolved.','Finish second review of original F015 statements and source dependencies; preserve separation from related S2 improvement.',[],['SP11'])
newtask_specs=[
 ('Q34','Audit Phase41 cycle obstructions','IN-01',['P41-A','P41-B','P41-C','P41-D','P41-E','P41-F','P41-S'],['I01','I02','I03','I04','I05'],['SP05','SP06'],'Two unitary-cycle Fourier summands excluded for N>8; 26 exact Jacobian records and fixed-branch ceilings accepted.','Surviving small/all-row target membership remains open; no Fourier construction.','Fresh independent finite certificates only.','Cayley/dimension mechanisms classical; exact exclusion priority unresolved.','No-D fixed sums: r2 N<=340 and r3 N<=4426; free-D r2 N<=1330 and r3 N<=17602. Products and broader nonunitary decorations are not covered.'),
 ('Q35','Audit magnetic Green averages','IN-02',['H17P18-A','H17P18-B','H17P18-C','H17P18-D','H17P18-E','H17P18-F','H17P18-X1','H17P18-X2','H17P18-X3'],['I06','I07','I08','I09','I10','I11','I28','I29'],['SP07','SP08'],'Uniform O(N) exact-field whole-vector average, rank formulas, O(N min(ell+1,K-ell)) sectors and all-odd same-K support exclusion accepted.','Exact-field evaluator proved; no all-input faster full Fourier construction.','Root supplied; coefficient/inverse and full-output field arithmetic charged; root discovery, bounded-word stability, bit complexity and actual speed unverified.','q-binomial and Weyl mechanisms classical; precise project corollary priority unresolved.','Same-K support obstruction applies to odd N>=3 without extra gauges, different coordinate systems or products. General bounded-word transfer remains open.'),
 ('Q36','Audit primitive Weyl embeddings','IN-03',['WV27-'+str(i).zfill(2) for i in range(1,12)],['I12','I13','I14','I15','I16','I17','I18'],['SP09'],'Corrected primitive Weyl classification, guarded extraction, bounded-exponent spectator result and single/multicycle ambient-swap obstruction accepted.','Nonzero extraction scalar alpha=ell(Ua) must be supplied; PE=I alone does not suffice.','Arbitrary similarity and growing multiplicity costs/norms are not free.','Primitive Weyl and intertwiner structure classical; restricted architecture/application priority unresolved.','Retain exponent-dividing-N hypothesis, nonzero coupling, and literal ambient-swap architecture. No universal cheap injection/extraction or runtime lower bound.'),
 ('Q37','Audit rational Fourier channels','IN-04',['RC'+str(i).zfill(2) for i in range(1,13)],['I19','I20','I21','I22','I23','I24','I25','I26','I27','I28','I29'],['SP10'],'Galois rank formula, arbitrary-depth scalar-linear gate cut, isolated diagonal optimum, nonzero normalization and correctly charged E/J/P fusion accepted.','No new general full Fourier construction.','Restricted scalar-linear model only; original CSE and warm-operation ledger not reconstructed.','Exact rational-character/multiplicative-complexity priority unresolved.','Charge whole target; do not add isolated-stage ranks or multiply independent branch/gate lower bounds. No unrestricted N log N lower bound.')]
for q,title,intake,claimids,rids,sids,result,construction,implementation,priority,remaining in newtask_specs:
 t={'queue_id':q,'title':title,'work_kind':'theory_review','queue_priority':2,'fusion_ids':[],'theorem_ids':[],'prior_candidate_ids':[],'catalogue_ids':[],'source_claim_ids':claimids,'incoming_id':intake,'dependencies':[],'historical_inventory':None};reg['tasks'].append(t);tasks[q]=t
 patch(q,result,'proofclosed','proofclosed',construction,implementation,priority,remaining,rids,sids)
for item,q in zip(reg['incoming_source_claims'],['Q34','Q35','Q36','Q37']):
 item.update({'state':'Scoped independent review complete; corrected claims, rejections and open limits retained','activity':'Incorporated in local supplement','queue_id':q,'review_ids':tasks[q]['review_ids'],'next':tasks[q]['remaining_obligation']})
# Preserve every source-family structured ID, with no inference that each row is novel.
reg['source_family_claims']={
 'rational_channels':load(ROOT/'rational_channels/final_v1/STATUS_REGISTER.json'),
 'weil_v27':load(ROOT/'weil_v27/CLAIM_LEDGER.json'),
 'phase41':load(ROOT/'phase41_supplement/final_v1/FINDINGS.json'),
 'magnetic_phase18':load(ROOT/'backends/phase18_audit/findings.json'),
 'composite_guard':load(ROOT/'composite_guard/final_v1/FINDINGS.json'),
 'backends':load(ROOT/'backends/final_v1/findings.json'),
 'masks':load(ROOT/'masks/final_v1/FINDINGS.json'),
 'n16_exhaustion':load(ROOT/'masks/n16_supplement/FINDINGS.json'),
 'inherited_reaudit':load(ROOT/'inherited_reaudit/final_v1/STATUS.json')}
# Subsequent independent receipts are matched by exact artifact hash, never by optimistic labels.
for sid,q,words in [('SP11','Q11',['green','C01']),('SP11','Q14',['fiber','F015']),('SP12','Q26',['N16'])]:
 s=source_by[sid]
 matches=[a for a in rows if a['verdict']=='ACCEPT' and a.get('reviewed_artifact_sha256')==s['sha256'] and (('C01' in a['claim']) if q=='Q11' else ('F015' in a['claim']) if q=='Q14' else True)]
 if matches:
  ids=[a['id'] for a in matches];t=tasks[q]
  t['review_ids']=uniq(t['review_ids']+ids);t['review_records'].extend(matches);t['task_state']=t['status']='proofclosed';t['proof_state']='proofclosed';t['proof_closed']=True
  s['review_ids']=uniq(s['review_ids']+ids);s['independently_reviewed_exact_hash']=True;s['kind']='reviewed_proof'
  for sh in t['source_hashes']:
   if sh['id']==sid:sh['exact_reviewed_hash']=True
  if q=='Q11':
   t['current_result']='Fresh full-text inherited C01 audit, decisive five-dimensional lower certificate, upper identities and guards independently accepted at the exact supplementary hash.'
   t['implementation_state']='Fresh certificate/control reconstruction independently reviewed; no production or numerical-stability claim.'
   t['remaining_obligation']='Exact additive-length priority unresolved; no full-B upper construction beyond N=5.'
  elif q=='Q14':
   t['current_result']='Original F015 cap and aggregate theorems freshly reread and independently accepted with fresh exact controls and all guarded Green-domain assumptions.'
   t['implementation_state']='Fresh exact controls independently reviewed; bit complexity, numerical stability and production validation remain separate.'
   t['remaining_obligation']='Resolve exact intermediate-fiber and rejection-interface priority; any bounded-word implementation requires its own complete contract.'
  else:
   t['current_result']='Original Phase39 N4/N8/N16 finite seven-Green exclusion closed: N16 complete cubic enumeration of 10,483,200 mappings per prime independently accepted; no quartic exhaustion or all-N extension.'
   t['construction_state']='Guarded exclusion for fixed cycles/couplings at N4/N8/N16; no positive factorization construction.'
   t['implementation_state']='Both N16 cubic enumeration records independently reviewed; min rank10, no alternative minor, row mask1023. N16 quartics and N32 remain sampled only.'
   t['remaining_obligation']='Larger sizes and broader graph/coupling families remain unclassified; Q27 target-fiber construction is separate.'
  t['next_actions']=[t['remaining_obligation']]
for q,ids,sid in [('Q11',['H12','H13','H14','H15'],'SP11'),('Q14',['H11','H12','H14','H15'],'SP11'),('Q26',['N02','N04','N05'],'SP12')]:
 for i in ids:
  if i in byrid and byrid[i].get('reviewed_artifact_sha256')==source_by[sid]['sha256']:
   if i not in tasks[q]['review_ids']:tasks[q]['review_ids'].append(i);tasks[q]['review_records'].append(byrid[i])
   source_by[sid]['review_ids']=uniq(source_by[sid]['review_ids']+[i])
# Full primary comparisons are added only when complete reports exist.
reg['primary_comparisons']=[]
for key,folder in [('fourier','delvaux_comparison'),('theta','lubinsky_comparison')]:
 p=ROOT/'uploaded_primary_1040'/folder
 finding_path=p/('STATUS_DELTA.json' if key=='fourier' else 'FINDINGS.json')
 if not finding_path.exists(): continue
 find=load(finding_path)
 entry={'id':'PRIMARY-'+key.upper(),'source_directory':str(p),'findings':find}
 for f in p.glob('*'):
  if f.is_file() and f.suffix.lower() in ['.md','.json','.txt'] and 'ocr' not in f.name.lower():
   dest=OUT/'primary_comparisons'/key/f.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
 entry['report_members']=[str(f.relative_to(OUT)) for f in (OUT/'primary_comparisons'/key).glob('*')]
 reg['primary_comparisons'].append(entry)
# Refine priority without changing mathematical truth or claiming global novelty.
reg['priority_delta_rows']=[]
for comparison in reg['primary_comparisons']:
 f=comparison['findings']
 if comparison['id']=='PRIMARY-FOURIER':
  for a in f['updates']:
   t=tasks[a['queue_id']];t.setdefault('primary_dispositions',[]).append(a)
   t['priority_state']='Final Delvaux–Van Barel 2008 comparison complete. '+a['priority_status'].replace('_',' ')+'.'
   if a.get('established_overlap'):t['priority_state']+=' Classical overlap: '+' '.join(a['established_overlap'])
   t.setdefault('closed_obligations',[]).append('Final Delvaux–Van Barel 2008 full-article access and theorem comparison closed for this source.')
   reg['priority_delta_rows'].append({'comparison_id':comparison['id'],'queue_ids':[a['queue_id']],'claim_ids':a['claim_ids'],'demoted_or_classical':a.get('established_overlap',[]),'retained':a['retained'],'remaining':a['caveats'],'source_sha256':f['source_pdf_sha256']})
 else:
  mapping={'F020':['Q02'],'ALG-RS-LOCAL':['Q02'],'FUS-02':['Q02','Q03'],'F021':['Q03'],'ALG-SCALAR-CHIRP-BANK':['Q03'],'Q29':['Q29'],'ALG-RS-RECIPROCAL-CONTENT':['Q03','Q29'],'F023':['Q02'],'C03':['Q17'],'ALG-RECIPROCAL-PENCILS':['Q17'],'FUS-06':['Q08'],'ALG-EVEN-PRONY-EXTRA-POLE':['Q20'],'F143':['Q20']}
  for a in f['claim_dispositions']:
   qs=uniq([q for i in a['ids'] for q in mapping.get(i,[])])
   for q in qs:
    tasks[q].setdefault('primary_dispositions',[]).append(a)
    tasks[q].setdefault('closed_obligations',[]).append('Lubinsky–Saff mathematical-body comparison and exact normalization mapping closed; bibliography page 360 remains absent.')
   reg['priority_delta_rows'].append({'comparison_id':comparison['id'],'queue_ids':qs,'claim_ids':a['ids'],'demoted_or_classical':a['demote'],'retained':[a['retain']],'remaining':f['queue_obligation_changes']['remaining'],'source_sha256':f['source_pdf_sha256']})
  tasks['Q02']['priority_state']='Lubinsky–Saff full mathematical body checked: RS recurrence/self-reciprocity, root-of-unity factorization, static multiplicities and derivative restatements are classical. Exact moving-z local splitting, ordinary-discriminant coefficients and guarded arithmetic remain narrow candidates with priority unverified.'
  tasks['Q03']['priority_state']='Lubinsky–Saff Theorem 3.2 directly supplies the chirp Hankel determinant, shifted RS annihilator and forced-diagonal product after explicit maps. Retain only specified legal-node/resonance/minimum and guarded content/carry applications for further priority review.'
  tasks['Q29']['priority_state']='Lubinsky–Saff mathematical-body access/comparison closed. It does not settle the accepted 3p/7p/11p half-order simplicity families; exact application priority and broader source review remain open.'
  tasks['Q20']['priority_state']='Chirp Hankel determinant is row-reversed Lubinsky–Saff Theorem 3.2. Accepted h<=Q<=h+1 legal extra-pole construction remains a scoped application; no new general moment theory or h-pole optimum.'
reg['source_completeness']={'delvaux_final':'Full final article read and specified theorem comparison completed.','lubinsky_saff':'All mathematical-body pages331–359 visually read. Journal reference page 360 (references 9–36) absent; final two PDF pages blank. Earlier-attribution follow-up and Zhedanov 1997 full text remain open.','source_pdfs_redistributed':False,'scispace_metadata_used_as_proof':False}
reg['next_cycle_pending']=[
 {'id':'NEXT-MAGNETIC-SIGNED','title':'Test signed magnetic fusion','state':'next_cycle_pending','activity':'Research active outside this frozen checkpoint','proof_state':'candidate','construction_state':'Unestablished','implementation_state':'Unestablished','priority_state':'Unestablished','stop':'Return a scoped signed-sector theorem or exact blocker; do not delay current checkpoint.'},
 {'id':'NEXT-RS-AUGMENTED','title':'Test augmented content obstruction','state':'next_cycle_pending','activity':'Research active outside this frozen checkpoint','proof_state':'candidate','construction_state':'Unestablished','implementation_state':'Not applicable until scoped result','priority_state':'Unestablished','stop':'Prove a scoped augmented-content support result or exhibit an exact obstruction; do not delay current checkpoint.'}]
reg['scoped_supersessions']=[]
for q,old in [('Q26','S17')]:
 if tasks[q]['task_state']=='proofclosed':reg['scoped_supersessions'].append({'historical_review_id':old,'superseded_scope':'Independent exhaustive N16 cubic reconstruction only','new_review_ids':[i for i in tasks[q]['review_ids'] if i not in ['S01','S02','S03','S17']],'preserved_limits':['N16 quartic is sampled only','N32 sampled only','no all-N claim','Q27 target membership remains separate']})
reg['source_family_claims']['inherited_reaudit']={'frozen_author_status':reg['source_family_claims']['inherited_reaudit'],'current_review_overlay':{q:{k:tasks[q][k] for k in ['task_state','proof_state','review_ids','remaining_obligation']} for q in ['Q11','Q14']}}
reg['source_family_claims']['n16_exhaustion']={'frozen_author_findings':reg['source_family_claims']['n16_exhaustion'],'current_review_overlay':{k:tasks['Q26'][k] for k in ['task_state','proof_state','review_ids','remaining_obligation']}}

# Views retain all historical IDs and full statement data; supplements append context rather than replace theorem identities.
for v in reg['view_records']:
 v['supplement_task_ids']=['Q29'] if v['id']=='FUS-02' else [];ts=[tasks[q] for q in uniq(v['underlying_task_ids']+v['supplement_task_ids'])]
 v['supplement_task_states']=[{'queue_id':t['queue_id'],'proof_state':t['proof_state'],'construction_state':t['construction_state'],'implementation_state':t['implementation_state'],'priority_state':t['priority_state'],'remaining_obligation':t['remaining_obligation']} for t in ts]
 v['primary_dispositions']=[a for t in ts for a in t.get('primary_dispositions',[])];v['priority_state']=' '.join(uniq(t['priority_state'] for t in ts));v['construction_state']=' '.join(uniq(t['construction_state'] for t in ts))
 v['source_ids']=uniq(v['source_ids']+[sid for t in ts for sid in t['source_ids']]);v['review_ids']=uniq(v['review_ids']+[rid for t in ts for rid in t['review_ids']]);v['source_hashes']=[{'id':sid,'sha256':source_by[sid]['sha256'],'member':source_by[sid].get('member'),'exact_reviewed_hash':source_by[sid].get('independently_reviewed_exact_hash',False)} for sid in v['source_ids'] if sid in source_by]
 if v['id'] in ['C01','F015']:
  t=tasks['Q11' if v['id']=='C01' else 'Q14']
  for k in ['proof_state','current_result','priority_state','implementation_state','construction_state','remaining_obligation']:v[k]=t[k]
# Every original fusion stays visible, with its already-closed theorem and remaining gates separately stated.
fusion=[]
for f in reg['fusion_list']:
 a=copy.deepcopy(f);a['inherited_task_ids']=list(a['tasks']);a['supplement_task_ids']=['Q29'] if a['id']=='FUS-02' else ['Q34'] if a['id']=='NF-02' else [];a['tasks']=uniq(a['tasks']+a['supplement_task_ids']);ts=[tasks[q] for q in a['tasks']]
 a['proof_state']=a['state'];a['closed_inherited_obligations']=[{'queue_id':t['queue_id'],'accepted_result':t['current_result'],'review_ids':t['review_ids']} for t in ts if t['proof_closed']]
 a['remaining_obligations']=[{'queue_id':t['queue_id'],'obligation':t['remaining_obligation'],'construction':t['construction_state'],'implementation':t['implementation_state'],'priority':t['priority_state']} for t in ts]
 a['priority_state']=' '.join(uniq(t['priority_state'] for t in ts));a['implementation_state']=' '.join(uniq(t['implementation_state'] for t in ts));a['construction_state']=' '.join(uniq(t['construction_state'] for t in ts));a['count_as_new_discovery']=False;fusion.append(a)
newfusions=[
 ('NF-04','Sparse magnetic weights share one inverse','proofclosed',['Q07','Q35'],['I10'],'Accepted exact-field sparse-character evaluation with shared inverse and paid recognition/sector work.','Specific supplied-root dyadic recognition model; root discovery and bounded-word numerics excluded.','Supply coefficient representation, precision/error and complete implementation cost for finite-word transfer.'),
 ('NF-05','Fixed-orbit support excludes odd Fourier','proofclosed',['Q35'],['I10'],'At every odd N>=3, same-K weighted orbit sums have Weyl support at most N(K+1)/2<N², including K=N.','No extra gauges, coordinate changes, mixed K or stage products; not a runtime lower bound.','Any broader architecture needs a new proof with its exact grammar.'),
 ('NF-06','Cycle sums meet separator cutoffs','proofclosed',['Q04','Q34'],['I01','I04'],'Two unitary-cycle sums require N<=8; general two/three inverse sums obey inherited fixed-branch ceilings.','Individually routed Hamiltonian-cycle inverses; specified external freedom; no stage-product extension.','In surviving sizes, settle all-row Fourier membership rather than local Jacobian dominance.'),
 ('NF-07','Covariant extraction meets rational gates','proofclosed',['Q36','Q37'],['I13','I22'],'For nonzero alpha, whole physical E/J/P scalar-linear circuit inherits Fourier projection gate lower bound.','PE=I does not guarantee alpha!=0; no free nonrational normalization or uncharged E/P.','Give an actual charged stable constructor before asserting speed or general computational complexity.'),
 ('NF-08','Branch and scalar gates constrain together','proofclosed',['Q15','Q37'],['I23','I26'],'Fixed-pair representation branch bound and whole-target nonrational scalar-gate bound hold simultaneously.','They constrain distinct resources and are not multiplied; isolated stage ranks are not additive.','For proposed fused graph, prove a whole-target gate bound and count actual branches separately.'),
 ('NF-09','Composite RS families feed legal banks','guardedclosed',['Q02','Q03','Q29'],['S06','S07','S08','S09'],'All-A half-order overlap guards now close for d=sp, s in {3,7,11}, every prime p=1 mod4.','Existing resonance and scalar-bank model unchanged; not all composite or repeated-prime d.','Resolve general augmented-content prime support and exact application priority.'),
 ('NF-10','Certified inverse transfer uses chirp subclass','conditionalclosed',['Q01','Q30'],['S10','S11','S12','S13'],'Conditional two-transform inverse transfer gains an explicit full nondegenerate quadratic-chirp preparation route.','General boundary kernel has exact-field recurrence only; l2 transform errors do not yield needed sup-norm gap certificate.','Certify general bounded-word spectral preparation and conditioning under complete range/precision costs.')]
for fid,title,state,qs,rids,result,boundary,nextstep in newfusions:
 fusion.append({'id':fid,'title':title,'state':state,'proof_state':state,'tasks':qs,'review_ids':rids,'result':result,'scope':boundary,'next':nextstep,'construction_state':'No generic full Fourier construction follows.','implementation_state':'No production validation or benchmark claim.','priority_state':'Classical mechanisms and project-specific applications must be separated; no worldwide novelty certification.','closed_inherited_obligations':[{'queue_id':q,'accepted_result':tasks[q]['current_result'],'review_ids':tasks[q]['review_ids']} for q in qs if tasks[q]['proof_closed']],'remaining_obligations':[nextstep],'count_as_new_discovery':False})
reg['fusion_list']=fusion
reg['fusion_count_warning']='Fusion rows are alternative packages and implications of overlapping results, never automatically independent discoveries.'
reg['catalogue_coverage']={'source':str(ROOT/'CATALOGUE_COVERAGE_178.json'),'sha256':sha(ROOT/'CATALOGUE_COVERAGE_178.json'),'rows':178,'depth':'Statement/model/status/source coverage only; not 178 complete proof reaudits.'}
shutil.copy2(ROOT/'CATALOGUE_COVERAGE_178.json',OUT/'CATALOGUE_COVERAGE_178.json')
shutil.copy2(ROOT/'CATALOGUE_COVERAGE_178.csv',OUT/'CATALOGUE_COVERAGE_178.csv')
reg['counts']=dict(collections.Counter(t['task_state'] for t in reg['tasks']))
reg['scope']['queue_tasks']=len(reg['tasks'])
reg['scope']['supplement_review_rows']=len(rows)
reg['scope']['original_task_ids_preserved']=len(base['tasks'])
reg['acceptance_checkpoint']={'label':'Local next supplement; exact scoped receipts incorporated; freeze gates listed separately','as_of_utc':now,'later_supplements_incorporated':True,'baseline_register_sha256':sha(BASE),'receipt_ids':[x['id'] for x in reg['supplement_review_ledgers']]}
reg['freeze_gates']={'C01_independent_reaudit':tasks['Q11']['task_state']=='proofclosed','F015_independent_reaudit':tasks['Q14']['task_state']=='proofclosed','N16_independent_exhaustive_review':tasks['Q26']['task_state']=='proofclosed','full_fourier_primary_comparison':any(x['id']=='PRIMARY-FOURIER' for x in reg['primary_comparisons']),'full_theta_primary_comparison':any(x['id']=='PRIMARY-THETA' for x in reg['primary_comparisons'])}
reg['freeze_state']='READY_FOR_FINAL_QA' if all(reg['freeze_gates'].values()) else 'LOCAL_DRAFT_AWAITING_LISTED_GATES'
# This report deliberately describes delta only; baseline theorem text is preserved in the register.
report=[
 'Research supplement since the delivered checkpoint',
 '',
 'This local supplement records exact scoped changes after the delivered review-v2 checkpoint. It preserves all 30 existing views and all 178 catalogue entries. The catalogue remains statement coverage; it is not a claim that 178 full proofs were reaudited. Review and finite-test counts are not discovery counts.',
 '',
 'What is newly accepted',
 '',
 'Masks and target fibers. S01–S05 accept the guarded exclusion and compatibility machinery, complete N4/N8 exclusion, and local four-ratio dominance. '+tasks['Q26']['current_result']+' Local dominance never supplies a prescribed all-row Fourier target. Q27 remains open in surviving models.',
 '',
 'Composite Rogers–Szegő. S06–S09 accept the exact exceptional Hermite pair, augmented same-component criterion and the three all-prime families 3p, 7p and 11p for p=1 mod4. The general composite and repeated-prime extensions remain open; existing resonance and bank grammar are unchanged.',
 '',
 'Inverse and fixed F60 backends. S10–S15 accept the conditional inverse contract, full-chirp preparation subclass, exact-field recurrence, singularity controls, and fixed F60 algebra/norm certificates. S16 rejects the universal assertion of 17 setup products: F61 has 16. Production rounding, general bounded-word conditioning and measured speed remain separate.',
 '',
 'Phase41. I01–I04 accept the N>8 two-unitary-cycle exclusion, guarded phase/dimension statements, all 26 exact Jacobian records and the matched separator ceilings. Two/three arbitrary-amplitude inverse sums have no-D ceilings 340/4426 and free-D ceilings 1330/17602. The bounds concern the stated sum grammars. Full target membership is still open where these tests leave room.',
 '',
 'Magnetic averages. I06–I10 accept the O(N) exact-field whole-vector average, rank and sector identities, O(N min(ell+1,K-ell)) complementary sector work and the odd-N same-K triangular-support exclusion. Root discovery, bounded-word numerics, stability and practical speed are unverified. These are neither a generic faster Fourier transform nor an unrestricted lower bound.',
 '',
 'Weyl and rational channels. I12–I15 accept corrected covariance and architecture statements; I19–I24 accept Galois rank, arbitrary-depth scalar-linear gate cuts and matched whole-circuit fusions. The extraction scalar must be nonzero, ambient exponent assumptions matter, and E/P work and norms must be paid. Isolated-stage gate bounds cannot be added; independent branch and gate bounds cannot be multiplied.',
 '',
 'Inherited evidence',
 '',
 tasks['Q11']['current_result']+' '+tasks['Q11']['remaining_obligation'],
 '',
 tasks['Q14']['current_result']+' '+tasks['Q14']['remaining_obligation'],
 '',
 'Classical priority demotions from the uploaded full papers',
 '',
 'Delvaux–Van Barel 2008: bit-reversal rank-one hierarchy is classical (Lemma 7), and C02 at N=8 already follows from Theorem 9. Prime full spark is prior Theorem 4; negation pairing appears in Theorem 15. The general all-independent-orders N/4+1 minimax and critical-rectangle quantitative gap remain distinct relative to this article. No +1 claim applies to arbitrary half-square blocks, whose minimum is N/4. The specified Green, separator and gauge applications are not matched here, which does not clear worldwide priority.',
 '',
 'Lubinsky–Saff: RS recurrence, self-reciprocity, root-of-unity factorization and static multiplicities are classical. More strongly, the chirp Hankel determinant, shifted RS annihilator and forced-diagonal product follow directly from Theorem 3.2 after the explicit maps. Retain local splitting/discriminant/arithmetic and specified legal-node applications as narrow candidates requiring further priority work. The paper does not settle Q29 general composite simplicity.',
 '',
 'Both mathematical-body comparison blockers are closed. Lubinsky–Saff journal reference page 360 is missing, so references 9–36 and Zhedanov 1997 remain follow-up sources. Specific mappings and PDF hashes are recorded in PRIMARY_DELTAS.json; no whole source PDF or OCR text is redistributed.',
 '',
 'What still needs a result',
 '',
 '1. A guarded exact full-matrix Fourier target in a surviving model, or a precise target-specific exclusion.',
 '2. General composite and repeated-prime RS guards, including augmented-content prime support.',
 '3. General bounded-word inverse preparation and useful spectral conditioning.',
 '4. Certified eager/packed numerical executors, graph-wise rounding, complete setup costs and honest performance tests.',
 '5. Exact model-matched priority for the remaining narrow interfaces and applications.',
 '',
 'Two new investigations, signed magnetic fusion and augmented-content obstruction, are next-cycle pending and do not alter this checkpoint.',
 '',
 'The attached register keeps proof, construction, implementation and priority separate. Accepted restricted results do not establish a generic all-input exact o(N log N) Fourier algorithm or an unrestricted N log N arithmetic lower bound.',
 '',
 'Local state: '+reg['freeze_state']+'. No external upload or Sheet write has been made by this integration.'
]
(OUT/'DELTA_REPORT.txt').write_text('\n'.join(report)+'\n')
# Delta-only workbook: the original nine-tab checkpoint remains unchanged.
tabs=[]
def tab(name,headers,records,widths):
 tabs.append({'name':name,'headers':headers,'rows':records,'widths':widths,'freezeColumns':1,'minRowHeight':58,'maxRowHeight':510})
tab('Overview',['Area','Change as of '+now[:19]+' UTC','Boundary or next step'],[
 ['Checkpoint','Final local scoped supplement to the delivered review-v2 checkpoint','Original delivered Sheet and files unchanged; this workbook shows changes only.'],
 ['Original checkpoint',load(ROOT/'integration/FINAL_DELIVERY_RECEIPT.json')['newGoogleSheet']['url'],'Verified prior private nine-tab Sheet; preserved unchanged.'],
 ['Coverage','All 30 prior views and 178 statement catalogue rows remain in STATUS_REGISTER.json','Not all178 full proofs reaudited; audit/receipt/fusion counts are not discovery counts.'],
 ['Independent review','Supplement v1/v2 plus final C01/F015 and N16 receipts incorporated','Only the stated hypotheses and exact hashes are accepted.'],
 ['Source comparisons','Final Delvaux–Van Barel article and Lubinsky–Saff mathematical body compared','Lubinsky–Saff reference page 360 absent; Zhedanov 1997 and broader priority remain open.'],
 ['Construction','No generic faster exact full-output Fourier algorithm established','Surviving target fibers and broader RS/inverse constructions remain open.'],
 ['Implementation','Fresh exact controls and paper algorithms accepted at scoped models','No supplied research program execution, production validation or practical speed certification.'],
 ['Next cycle','Signed magnetic fusion and augmented-content obstruction are active investigations outside this checkpoint','Listed as pending; their future findings do not change this freeze.']], [170,630,660])
change_groups=[
 ('Mask exclusion',['Q26'],'S01–S03; N01–N03','N4/N8/N16 fixed Phase39 exclusion now fully independently accepted. N16:10,483,200 cubic mappings per prime; both products and fixed minor matched.','N16 quartics and N32/larger remain sampled only; no all-N or arbitrary-architecture result.'),
 ('Target compatibility',['Q27'],'S04–S05; I05','Guarded equivalence/local dominance accepted; exact surviving Fourier target still open.','Local Jacobian rank and partial numerical fits do not establish full all-row target membership.'),
 ('Composite RS',['Q29'],'S06–S09; S19','Unconditional d=sp for s=3,7,11 and all prime p=1 mod4; exact parity exception and augmented criterion accepted.','All-composite/repeated-prime/content-support extension open; resonance and scalar-bank minimum unchanged.'),
 ('Inverse preparation',['Q30'],'S10–S13; S20','Conditional inverse transfer plus full-chirp bounded-word subclass and exact-field recurrence accepted.','General bounded-word spectral floor and stable sup-norm preparation remain open.'),
 ('Fixed F60 backend',['Q32'],'S14–S16','Fixed factorization,444 additions/69 prepared scalars and norm/coefficient route accepted. Universal17-setup assertion rejected: F61 gives16.','Internal rounding, supported-field/count repair and production execution remain open; no growing-radix or optimality claim.'),
 ('Five-dimensional C01',['Q11'],'H01–H05','Fresh full proof and576-pair/4320-transition/624-branch lower certificate plus upper guards independently accepted.','Exact length3 uses quadratic-extension upper and complex lower in stated arithmetic family; base-field/growing upper and priority remain open.'),
 ('Growing-fiber F015',['Q14'],'H06–H10','Original cap/aggregate/full-output contracts freshly reaudited and independently accepted.','Supplied roots and both Green guards remain. Optional successful-prefix bound requires degree-trimmed BM; no tested fixed-buffer count or stability claim.'),
 ('Phase41 cycles',['Q34'],'I01–I04','N>8 two-unitary-cycle exclusion, all26 Jacobian records and fixed-branch ceiling application accepted.','No-D two/three ceilings340/4426; free-D1330/17602. Surviving target fibers open; products outside scope.'),
 ('Magnetic averages',['Q35'],'I06–I10','O(N) exact-field average, complementary sector work and all-odd same-K support exclusion accepted.','Supplied root/exact field only; no bit/stability/practical-speed claim, mixed-K/gauge/product extension or generic FFT result.'),
 ('Primitive Weyl',['Q36'],'I12–I18','Corrected representation/extraction, bounded-exponent spectators and literal ambient-swap obstructions accepted; overbroad inferences rejected.','Require nonzero extraction scalar; PE=I alone insufficient. Similarity/multiplicity work and norms must be charged.'),
 ('Rational channels',['Q37'],'I19–I29','Galois rank and arbitrary-depth scalar-linear gates plus correctly charged E/J/P fusions accepted.','No additive isolated-stage ranks or multiplied branch/gate bounds; no unrestricted N log N lower bound.')]
tab('Scoped changes',['Area','Task IDs','Paper proof change','Construction and scope','Implementation','Priority','Review IDs'],[[name,'; '.join(qs),change,boundary,'; '.join(uniq(tasks[q]['implementation_state'] for q in qs)),'; '.join(uniq(tasks[q]['priority_state'] for q in qs)),ids] for name,qs,ids,change,boundary in change_groups],[170,100,560,500,450,500,180])
tab('Priority deltas',['Source and claim IDs','Classical overlap or demotion','Retained narrow statement','Still open or important caveat','Source SHA256'],[[a['comparison_id']+' | '+'; '.join(a['claim_ids']),' '.join(a['demoted_or_classical']) or 'No matching stated theorem in this source; no novelty inference.',' '.join(a['retained']),' '.join(a['remaining']),a['source_sha256']] for a in reg['priority_delta_rows']],[230,620,620,600,560])
fusion_gate_rows=[]
for f in fusion:
 qs=f['tasks'];accepted='; '.join(uniq([i for q in qs for i in tasks[q]['review_ids']]))
 # Preserve original IDs while showing only their gate update, not repeating full theorem statements.
 closed='; '.join(uniq(tasks[q]['current_result'] for q in qs if q in ['Q11','Q14','Q26','Q29','Q30','Q32','Q34','Q35','Q36','Q37'])) or 'Inherited scoped proof status retained; read exact baseline statement.'
 remaining=f['next']
 if f['id']=='NF-02':closed='N4/N8/N16 mask exclusion and local compatibility proofs accepted; Phase41 excludes two unitary cycles for N>8.';remaining='Surviving full target fibers remain open. No local-dominance-to-global-target inference.'
 if f['id']=='FUS-02':closed='Hermite/content proof retained; 3p/7p/11p families accepted. Classical RS/moment mechanisms explicitly demoted.';remaining='General composite/repeated-prime guards and narrow application priority remain open.'
 if f['id']=='FUS-03':closed='Matrix proof retained; final Delvaux comparison closes source blocker and demotes bit reversal and N8 critical-rank corollary.';remaining='General minimax/gap application priority still open; arbitrary half-square minimum is N/4.'
 fusion_gate_rows.append([f['id'],f['title'],f['state'],closed,remaining,f['scope'],accepted])
for a in reg['next_cycle_pending']:fusion_gate_rows.append([a['id'],a['title'],a['state'],'No result accepted in this checkpoint',a['stop'],a['activity'],''])
tab('Fusion gates',['Fusion ID','Combination','Proof state','Closed since checkpoint','Remaining obligation','Boundary','Review IDs'],fusion_gate_rows,[155,330,170,660,620,510,220])
evidence_rows=[[s['id'],s['title'],s['member'],s['sha256'],'; '.join(s.get('review_ids',[])),'Scoped exact-hash review accepted' if s.get('independently_reviewed_exact_hash') else 'Read scoped source status'] for s in sources]
for b in reg['supplement_review_ledgers']:evidence_rows.append([b['id'],'Independent scoped review receipt','reviews/'+b['id']+'/review_ledger.json',b['ledger_sha256'],', '.join(a['id'] for a in b['rows']),'Immutable original review decisions retained; later scope supersessions explicit in register.'])
tab('Evidence',['ID','Evidence','Supplement member','SHA256','Review IDs','Meaning'],evidence_rows,[160,360,480,560,250,440])
payload={'title':'Research review supplement 2026-10-10','filename':'Research-review-supplement-2026-10-10.xlsx','outputDir':str(OUT/'workbook'),'as_of_utc':now,'publication_scope':'New private delta-only Sheet; preserve original delivered checkpoint; no whole source papers.','external_write_executed_by_integrator':False,'schema':'Workbook-ready payload; publishing authority belongs to parent and publishing worker.','tabs':tabs}
dump(OUT/'SHEET_PAYLOAD.json',payload)
dump(OUT/'FUSION_QUEUE.json',{'version':reg['version'],'as_of_utc':now,'count_warning':reg['fusion_count_warning'],'items':fusion,'inherited_follow_on_queue':reg['follow_on_queue'],'next_cycle_pending':reg['next_cycle_pending']})
dump(OUT/'PRIMARY_DELTAS.json',{'comparisons':reg['primary_comparisons'],'priority_delta_rows':reg['priority_delta_rows'],'source_completeness':reg['source_completeness']})
dump(OUT/'STATUS_REGISTER.json',reg)
# Keep exact receipt files separately, unchanged.
for b in reg['supplement_review_ledgers']:
 p=ROOT/'review'/b['id'];dest=OUT/'reviews'/b['id'];dest.mkdir(parents=True,exist_ok=True)
 for f in ['ACCEPTANCE_RECEIPT.json','review_ledger.json','REVIEW_SUMMARY.md','SOURCE_MANIFEST.json','MANIFEST.json']:
  if (p/f).exists():shutil.copy2(p/f,dest/f)
# Source manifest preserves required archive provenance without redistributing user source papers.
provenance=[]
for p in [ROOT/'backends/final_v1/MANIFEST.json',ROOT/'backends/phase18_audit/SOURCE_PROVENANCE.json',ROOT/'rational_channels/final_v1/ARTIFACT_MANIFEST.json',ROOT/'weil_v27/AUDIT_MANIFEST.json',ROOT/'phase41_supplement/final_v1/MANIFEST.json',ROOT/'composite_guard/final_v1/MANIFEST.json',ROOT/'masks/final_v1/MANIFEST.json',ROOT/'masks/n16_supplement/MANIFEST.json',ROOT/'inherited_reaudit/final_v1/SOURCE_MANIFEST.json',ROOT/'uploaded_primary_1040/MANIFEST.json']:
 provenance.append({'path':str(p),'sha256':sha(p),'contents':load(p)})
dump(OUT/'SOURCE_PACKAGE_PROVENANCE.json',provenance)
qa={'as_of_utc':now,'baseline_files_unchanged':all(sha(p)==h for p,h in reg['baseline']['preserved_files'].items()),'original_33_task_ids_preserved':set(t['queue_id'] for t in base['tasks']).issubset(tasks),'all_30_view_ids_preserved': [v['id'] for v in base['view_records']]==[v['id'] for v in reg['view_records']],'178_catalogue_rows_preserved':len(load(ROOT/'CATALOGUE_COVERAGE_178.json')['rows'])==178 and sha(OUT/'CATALOGUE_COVERAGE_178.json')==sha(ROOT/'CATALOGUE_COVERAGE_178.json'),'review_id_unique':len(byrid)==len(rows),'all_task_status_dimensions_present':all(all(k in t for k in ['proof_state','construction_state','implementation_state','priority_state']) for t in reg['tasks']),'no_source_pdfs_or_ocr_in_pack':not any(p.suffix.lower()=='.pdf' or 'ocr' in p.name.lower() for p in OUT.rglob('*') if p.is_file()),'external_mutations':False,'freeze_gates':reg['freeze_gates'],'source_hash_checks':[]}
for a in rows:
 p=a.get('evidence','').split(' §')[0]
 if Path(p).is_file() and a.get('reviewed_artifact_sha256'):
  qa['source_hash_checks'].append({'review_id':a['id'],'matches':sha(p)==a['reviewed_artifact_sha256'],'path':p})
qa['all_locatable_review_hashes_match']=all(x['matches'] for x in qa['source_hash_checks'])
dump(OUT/'INTEGRATION_QA.json',qa)
print(json.dumps({'state':reg['freeze_state'],'gates':reg['freeze_gates'],'task_counts':reg['counts'],'rows':len(rows),'qa':{k:v for k,v in qa.items() if k not in ['source_hash_checks','freeze_gates']}}))
