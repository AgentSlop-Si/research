"""Freeze previously accepted evidence; performs integrity checks only, no scientific calculation."""
from pathlib import Path
import hashlib, json, shutil, zipfile
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent

def digest(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def manifest_check(directory, filename, key=None, rooted=False):
    base=ROOT/directory
    obj=json.loads((base/filename).read_text())
    rows=obj[key] if key else obj
    if isinstance(rows,dict): rows=[{'path':p,'sha256':h} for p,h in rows.items()]
    for row in rows:
        p=(ROOT if rooted else base)/row['path']
        got=digest(p)
        assert got['sha256']==row['sha256'],p
        if 'bytes' in row: assert got['bytes']==row['bytes'],p
    return {'manifest':f'{directory}/{filename}', **digest(base/filename), 'entries_verified':len(rows),'status':'PASS'}

checks=[
 manifest_check('free_singleton_basefield_acceptance','FILE_HASHES.json',rooted=True),
 manifest_check('parameter_cubic_lower_bound','MANIFEST.json','files'),
 manifest_check('cubic_thirteen_independent_acceptance','MANIFEST.json','members'),
 manifest_check('degree_five_twelve_acceptance','MANIFEST.json'),
 manifest_check('pinned_sixteen_acceptance','MANIFEST.json'),
]
# Verify the pinned inputs of the two newly accepted extension reviews.
for dirname,key in [('parameter_cubic_lower_bound',None),('cubic_thirteen_independent_acceptance','sources')]:
    p=ROOT/dirname/'SOURCE_HASHES.json'; data=json.loads(p.read_text()); rows=data[key] if key else data
    for row in rows:
        got=digest(ROOT/row['path']); assert got['sha256']==row['sha256']; assert got['bytes']==row['bytes']
    checks.append({'source_bindings':str(p.relative_to(ROOT)),**digest(p),'entries_verified':len(rows),'status':'PASS'})

specs=[
 ('A','Accepted free-singleton equality over F23','free_singleton_basefield_acceptance/REVIEW.md',[
  'free_singleton_basefield_acceptance/FILE_HASHES.json','free_singleton_basefield_acceptance/RESULTS.json',
  'free_singleton_basefield_acceptance/SOURCE_HASHES.json','free_singleton_basefield_acceptance/REPLAY_VERIFICATION.json',
  'free_singleton_basefield_acceptance/independent_review.py','free_singleton_basefield_candidate/outputs/WITNESS.json'],
  'Unpinned_Singleton_F23_Exact14_Independent_ACCEPT_2026-10-14.zip'),
 ('B','Accepted all-extension baseline and cubic exclusion','parameter_cubic_lower_bound/REVIEW.md',[
  'parameter_cubic_lower_bound/MANIFEST.json','parameter_cubic_lower_bound/RESULTS.json',
  'parameter_cubic_lower_bound/SOURCE_HASHES.json','parameter_cubic_lower_bound/REPLAY_VERIFICATION.json',
  'parameter_cubic_lower_bound/independent_verify.py'],None),
 ('C','Accepted cubic witness and exact minimum thirteen','cubic_thirteen_independent_acceptance/REVIEW.md',[
  'cubic_thirteen_independent_acceptance/MANIFEST.json','cubic_thirteen_independent_acceptance/ACCEPTANCE.json',
  'cubic_thirteen_independent_acceptance/outputs/INDEPENDENT_RESULTS.json',
  'cubic_thirteen_independent_acceptance/SOURCE_HASHES.json','cubic_thirteen_independent_acceptance/REPLAY_VERIFICATION.json',
  'cubic_thirteen_independent_acceptance/dependencies/RAW_CERTIFICATE.json','cubic_thirteen_independent_acceptance/independent_verify.py'],
  'N11_Cubic_Field_Thirteen_Bank_Independent_ACCEPT_2026-10-14.zip'),
 ('D','Accepted degree-five witness used as free-domain upper bound','degree_five_twelve_acceptance/REVIEW.md',[
  'degree_five_twelve_acceptance/MANIFEST.json','degree_five_twelve_acceptance/RESULTS.json',
  'degree_five_twelve_acceptance/MINIMAL_WITNESS.json','degree_five_twelve_acceptance/REPLAY_AND_CONTROLS.json',
  'degree_five_twelve_acceptance/independent_check.py'],
  'Signed_Bank_Twelve_Extension_Field_Independent_ACCEPT_2026-10-13.zip'),
 ('E','Accepted pinned (4,4) base-field minimum sixteen for comparison','pinned_sixteen_acceptance/REVIEW.md',[
  'pinned_sixteen_acceptance/MANIFEST.json','pinned_sixteen_acceptance/ACCEPTANCE.json'],
  'Signed_Bank_Pinned_F23_Exact_Sixteen_Independent_ACCEPT_2026-10-14.zip'),
 ('F','Bounded prior-art comparison; historical novelty unresolved','pinned_bank_literature/REPORT.md',[],None),
]
records=[]
for label,role,report,supporting,archive in specs:
    files=[]
    for rel in [report]+supporting:
        src=ROOT/rel
        # Snapshot the research evidence; executable source is bound but not run or copied.
        dst=None
        if src.suffix!='.py':
            name=label+'__'+rel.replace('/','__')
            dest=OUT/'sources'/name; shutil.copyfile(src,dest)
            assert digest(src)==digest(dest)
            dst=str(dest.relative_to(OUT))
        files.append({'original_path':rel,'snapshot_path':dst,**digest(src)})
    record={'id':label,'role':role,'report_path':report,'files':files}
    if archive:
        p=ROOT/archive; sealp=ROOT/(archive+'.seal.json'); seal=json.loads(sealp.read_text()); got=digest(p)
        assert got['sha256']==seal['sha256']; assert got['bytes']==seal['bytes']
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            matches=[n for n in z.namelist() if n.endswith('REVIEW.md') and hashlib.sha256(z.read(n)).hexdigest()==digest(ROOT/report)['sha256']]
            assert matches,(archive,report)
        dest=OUT/'sources'/(label+'__'+sealp.name);shutil.copyfile(sealp,dest)
        record['accepted_archive']={'original_path':archive,**got,'seal_snapshot':str(dest.relative_to(OUT)),'matching_report_members':matches,'integrity':'PASS'}
    records.append(record)

payload={
 'created_date':'2026-10-14','status':'ALL_SELECTED_SOURCE_INTEGRITY_CHECKS_PASS',
 'synthesis_scope':'Original N11 q13 free-cross-singleton physical-bank minima 14/13/12 over F23, F23^3, F23^5',
 'scientific_programs_executed_by_synthesis':False,'external_writes':False,
 'source_checks':checks,'sources':records,
 'dependency_map':{'F23_exact14':['A'],'F23_cubed_exact13':['B','C'],'F23_fifth_exact12':['B','D'],'pinned_comparisons':['B','E'],'literature_limits':['F']},
 'mathematical_dependency_gaps':[],
 'remaining_prerequisites_before_paper_submission':[
  'Write a self-contained proof exposition with the exact replayable certificates.',
  'Explain the mathematical or operational motivation for the restricted dictionary.',
  'Obtain broader specialist literature comparison before asserting historical novelty.',
  'Obtain ordinary external mathematical review; these internal computational/proof audits are not journal peer review.'
 ],
 'snapshot_limit':'This is a source-bound synthesis, not a replacement for the full original review and replay packages. Source code is hashed, never executed by this packaging script.'
}
(OUT/'SOURCE_BINDINGS.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'source_manifests':checks,'sources':len(records),'status':payload['status']},indent=2))
