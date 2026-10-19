"""Read-only publication verifier. Executes no scientific checker or source code."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok: raise ValueError(msg)
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT/p).read_text())
def safe(p):
    q=Path(p)
    require(bool(p) and not q.is_absolute() and '..' not in q.parts,'Unsafe path: '+p)
    return ROOT/q
def entries(d):
    for key in ('files','review_files','certificate'):
        if key in d:
            x=d[key]; return x if isinstance(x,list) else [dict(path=k,**v) for k,v in x.items()]
    return [dict(path=k,**v) for k,v in d.items()]
def verify():
    allow=read('PRESERVATION_ALLOWLIST.json')['files']
    require(allow==sorted(set(allow)),'Allowlist duplicated or unsorted')
    allpaths=list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in allpaths),'Symlink in payload')
    actual=sorted(str(p.relative_to(ROOT)) for p in allpaths if p.is_file())
    require(actual==allow,'Exact public allowlist mismatch')
    manifest=read('MANIFEST.json')
    names=[x['path'] for x in manifest['files']]
    require(len(names)==len(set(names)),'Duplicate manifest entry')
    require(set(names)==set(allow)-{'MANIFEST.json','SEAL.json'},'Manifest coverage mismatch')
    for x in manifest['files']:
        p=safe(x['path'])
        require(p.stat().st_size==x['bytes'] and h(p)==x['sha256'],'Manifest hash/size mismatch: '+x['path'])
    seal=read('SEAL.json')
    for key,name in [('manifest_sha256','MANIFEST.json'),('allowlist_sha256','PRESERVATION_ALLOWLIST.json'),('acceptance_sha256','FINAL_ACCEPTANCE.json'),('scope_sha256','CLAIM_SCOPE.json'),('owner_dispositions_sha256','OWNER_DISPOSITIONS.json')]:
        require(h(safe(name))==seal[key],'Seal mismatch: '+name)
    cp=read('COPY_BINDINGS.json'); cpaths=[x['public_path'] for x in cp['files']]
    require(len(cpaths)==len(set(cpaths)),'Duplicate copy binding')
    for x in cp['files']:
        p=safe(x['public_path'])
        require(h(p)==x['source_sha256']==x['public_sha256'],'Source copy hash mismatch')
        require(p.stat().st_size==x['source_bytes']==x['public_bytes'],'Source copy size mismatch')
        require(x['transformation']=='EXACT_COPY','Source transformation found')
    require(len(cp['source_sets'])==12,'Incorrect source-set count')
    for s in cp['source_sets']:
        mp=safe(s['public_prefix']+'/MANIFEST.json')
        require(h(mp)==s['manifest_sha256'],'Source manifest binding mismatch')
        es=entries(json.loads(mp.read_text()))
        require(len(es)==s['manifest_entries'] and s['complete_manifest_payload'] is True,'Incomplete source manifest')
        for x in es:
            p=safe(s['public_prefix']+'/'+x['path'])
            require(h(p)==x['sha256'] and p.stat().st_size==x['bytes'],'Source manifest payload mismatch')
    refs=read('SOURCE_REFERENCE_MAP.json')['files']
    require(len(refs)==len(cp['files']),'Reference-map coverage mismatch')
    lookup={(x['source_package'],x['source_relative_path']):x for x in cp['files']}
    for x in refs:
        z=lookup[(x['source_package'],x['source_relative_path'])]
        require(x['preserved_path']==z['public_path'] and x['source_sha256']==z['source_sha256'],'Reference-map mismatch')
    omission=read('OMISSIONS.json')
    require(omission['omitted_manifest_declared_source_files']==[],'Manifest evidence omitted')
    for z in omission['verified_duplicate_archives']:
        require(z['all_members_equal_preserved_files'] is True and z['archive_container_republished'] is False,'Archive boundary mismatch')
        for x in z['members']:
            b=lookup[(z['source_package'],x['path'])]
            require(x['sha256']==b['source_sha256'] and x['bytes']==b['source_bytes'],'Archive member missing or mismatched')
    before=read('c8_lower/review/SOURCE_BINDINGS_BEFORE.json')
    require(before==read('c8_lower/review/SOURCE_BINDINGS_AFTER.json'),'C8 review source snapshots differ')
    archive_lookup={(x['source_package'],x['path']):x for x in omission['verified_duplicate_archives']}
    audit_rows=list(before.values())+read('f020_third_block/review/INPUT_VERIFICATION.json')['files']
    for x in audit_rows:
        sp=Path(x['path']); parts=sp.parts
        require(len(parts)>3 and parts[:3]==('/','workspace','shared'),'Unexpected scientific source root')
        key=(parts[3],str(Path(*parts[4:])))
        b=lookup.get(key)
        if b is None:
            z=archive_lookup.get(key)
            require(z is not None and z['sha256']==x['sha256'] and z['bytes']==x['bytes'],'Unpreserved audit source')
        else:
            require(b['source_sha256']==x['sha256'] and b['source_bytes']==x['bytes'],'Audit source copy mismatch')
    final=read('FINAL_ACCEPTANCE.json')
    require(final['packaging_independent_review']=='PENDING' and final['root_release']=='PENDING','Premature release state')
    require(final['publication_authorized_by_this_packet'] is False,'Packet supplies release authority')
    fixed={'c8':('96f8bfbf90d0fe6e1bfea4cf1cd03b94cca95468bfe7e2d9bcbf0884efa53b6c','775cd4687ed5a9d252c634b488b2f9f5c06c4563644dbceaa583301fe3c035af','PASS'),'f020':('042d50f56a07262323d5f0480e03bf546418669375e482db95a8575d878407b1','4f11d0bcf0a264224884a6dfce7a2cf1b0bf3c9ddc90b68b8e2c332a58bedf6d','ACCEPT')}
    for k,(cm,rm,verdict) in fixed.items():
        x=final['scientific_results'][k]
        for field in ('candidate_manifest','review_manifest','proof','review','verdict'):
            require(h(safe(x[field+'_path']))==x[field+'_sha256'],'Acceptance hash mismatch')
        require(x['candidate_manifest_sha256']==cm and x['review_manifest_sha256']==rm,'Frozen scientific target changed')
        require(read(x['verdict_path'])['verdict']==x['verdict']==verdict,'Scientific acceptance missing')
    cv=read('c8_lower/review/VERDICT.json'); fv=read('f020_third_block/review/VERDICT.json')
    require(cv['candidate_proof_sha256']==final['scientific_results']['c8']['proof_sha256'],'C8 verdict/proof mismatch')
    require(fv['candidate_manifest_sha256']==fixed['f020'][0] and fv['candidate_report_sha256']==final['scientific_results']['f020']['proof_sha256'],'F020 verdict/candidate mismatch')
    require(cv['independent_exact_assertions']==1190 and fv['independent_exact_assertions']==386,'Recorded independent counts changed')
    require(cv['corrections_required']==[] and fv['blocking_issues']==[] and fv['proof_issues']==[],'Unresolved scientific blocker')
    scope=read('CLAIM_SCOPE.json'); c=scope['c8']; f=scope['f020']
    require(c['strict_lower']=='sin(3*pi/16+1/1000000)' and c['inherited_upper']=='sqrt(1+sqrt(sqrt(2)-1))/2','Wrong C8 interval')
    require(c['dimension']==8 and c['correction_rank']==0 and c['arbitrary_phases_covered'] is True,'Wrong C8 model')
    for k in ('global_periodicity_assumed','periodic_surrogate_used','compression_invariance_or_unitarity_assumed','exact_global_optimum_established','minimizer_classification_established'):
        require(c[k] is False,'C8 unsupported claim: '+k)
    require(f['b_range']=='0<=b<min(3p,p^s)' and f['new_degrees']=='2p<b<3p for s>=2','Wrong F020 degree scope')
    require(f['p']=='every odd prime' and f['s']=='every integer s>=1' and f['q']=='every primitive p^s-th root','Wrong F020 quantifier')
    require(f['discriminant_valuation']=='p*(4*p-3)+2*p*r+r*(r-1)/2+(r%2)*(2*p-2)' and f['valuation_normalization']=='v(q-1)=1','Wrong discriminant scope')
    for k in ('b_at_least_3p_covered','unrestricted_F020_closed','all_A_closed','new_root_order_census'):
        require(f[k] is False,'F020 unsupported claim: '+k)
    for k in ('historical_novelty_claim','fft_algorithm_or_complexity_improvement_claim','scientific_reruns_during_packaging'):
        require(scope[k] is False,'Unsupported package claim: '+k)
    owners=read('OWNER_DISPOSITIONS.json')
    for x in owners['owners'].values():
        require(x['broader_owner_remains_open'] is True,'Owner closed')
        for k in ('owner_closure','status_change','priority_change'): require(x[k] is False,'Owner change claimed')
    require(owners['owners']['F020']['priority']==58 and owners['owners']['F020']['alias']=='F023','F020 metadata changed')
    for k in ('canonical_records_modified','scores_changed','status_census_changed'): require(owners[k] is False,'Canonical record mutation')
    for k in ('scientific_reruns_during_packaging','external_writes','prior_packets_modified'): require(seal[k] is False,'Invalid packaging activity')
    for n in actual:
        require(Path(n).suffix.lower() not in {'.pdf','.docx','.xlsx','.zip','.png','.jpg','.pyc'},'Disallowed file type')
        require(Path(n).suffix.lower() in {'.json','.md','.py','.log','.txt',''},'File extension outside publication allowlist')
    return {'verdict':'PASS','public_files':len(actual),'public_bytes':sum(safe(p).stat().st_size for p in actual),'exact_source_copies':len(cp['files']),'complete_source_manifest_sets':len(cp['source_sets']),'scientific_programs_executed':False,'external_writes':False}
if __name__=='__main__': print(json.dumps(verify(),indent=2))
