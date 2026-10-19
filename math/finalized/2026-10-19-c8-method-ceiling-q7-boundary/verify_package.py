"""Verify this publication candidate without running any scientific programs."""
from pathlib import Path
import base64, gzip, hashlib, io, json, re, sys, zipfile

def require(ok, message):
    if not ok: raise ValueError(message)
def sha(data): return hashlib.sha256(data).hexdigest()
def info(data): return {'bytes':len(data),'sha256':sha(data)}
def path(root,name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and bool(p.parts),'Unsafe relative path')
    result=root/p
    require(not result.is_symlink(),'Symlink in public payload')
    require(root.resolve() in result.resolve().parents,'Path escapes package')
    return result
def manifest_rows(obj):
    for key in ('files','review_files','entries','certificate'):
        if key in obj:
            val=obj[key]
            return [dict(path=k,**v) for k,v in val.items()] if isinstance(val,dict) else val
    require(obj and all(isinstance(v,dict) and 'sha256' in v and 'bytes' in v for v in obj.values()),'Unknown source manifest schema')
    return [dict(path=k,**v) for k,v in obj.items()]
def decode(data,representation):
    if representation=='EXACT_COPY': return data
    require(representation=='GZIP_BASE64','Unknown source representation')
    return gzip.decompress(base64.b64decode(b''.join(data.split()),validate=True))

def verify(root):
    root=Path(root).resolve()
    def read(name): return path(root,name).read_bytes()
    def js(name): return json.loads(read(name))
    seal=js('SEAL.json'); manifest_bytes=read('MANIFEST.json'); manifest=json.loads(manifest_bytes)
    require(info(manifest_bytes)==seal['manifest'],'Package manifest/seal mismatch')
    declared=manifest['files']; require(len(declared)==len({r['path'] for r in declared}),'Duplicate public manifest path')
    expected={r['path'] for r in declared}|{'MANIFEST.json','SEAL.json'}
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    require(actual==expected,'Unlisted or missing public payload')
    allow=js('PRESERVATION_ALLOWLIST.json')
    require(len(allow['public_paths'])==len(set(allow['public_paths'])),'Duplicate allowlist entry')
    require(set(allow['public_paths'])==expected,'Public allowlist mismatch')
    for row in declared:
        require(info(read(row['path']))=={k:row[k] for k in ('bytes','sha256')},'Stored-file integrity mismatch: '+row['path'])
    copy=js('COPY_BINDINGS.json'); files=copy['files']; sets=copy['source_sets']
    require(len(files)==len({r['logical_path'] for r in files}),'Duplicate logical source')
    require(len(files)==len({r['public_path'] for r in files}),'Duplicate physical source')
    require(len(sets)==12 and sum(s['role']=='primary' for s in sets)==4,'Wrong selected source sets')
    payload={}; by_source={}
    forbidden=re.compile(rb'thread_id|message_id|file_id|document_id|spreadsheet_id|docs\.google\.com|chatgpt\.com|/root/|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',re.I)
    for row in files:
        stored=read(row['public_path'])
        require(info(stored)=={'bytes':row['public_bytes'],'sha256':row['public_sha256']},'Transport hash mismatch')
        data=decode(stored,row['representation'])
        require(info(data)=={'bytes':row['source_bytes'],'sha256':row['source_sha256']},'Decoded source mismatch')
        require(not forbidden.search(data),'Private identifier in decoded scientific source')
        if data.startswith(b'PK\x03\x04'):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for name in z.namelist():
                    require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe archive member')
                    if not name.endswith('/'):
                        require(not forbidden.search(z.read(name)),'Private identifier in archive member')
        payload[row['logical_path']]=data
        by_source[(row['source_package'],row['source_relative_path'])]=data
    for item in sets:
        raw=payload[item['manifest_path']]
        require(info(raw)=={'bytes':item['manifest_bytes'],'sha256':item['manifest_sha256']},'Original source manifest mismatch')
        entries=manifest_rows(json.loads(raw))
        require(len(entries)==item['manifest_entries'],'Wrong source manifest entry count')
        require(len(entries)==len({r['path'] for r in entries}),'Duplicate source-manifest entries')
        for row in entries:
            logical=item['public_prefix']+'/'+row['path']
            require(logical in payload,'Source manifest payload missing: '+logical)
            require(info(payload[logical])=={k:row[k] for k in ('bytes','sha256')},'Original source manifest payload mismatch: '+logical)
        for name in item['extra_bound_files']:
            logical=item['public_prefix']+'/'+name
            require(logical in payload,'Extra bound source missing')
            if name=='SEAL.sha256':
                require(payload[logical].decode().split()[0]==item['manifest_sha256'],'Original source seal mismatch')
    ledger=js('RESTORATION_LEDGER.json')['files']
    require(len(ledger)==len(files),'Restoration ledger incomplete')
    require({r['logical_path'] for r in ledger}==set(payload),'Restoration ledger logical set mismatch')
    file_index={r['logical_path']:r for r in files}
    for row in ledger:
        source=file_index[row['logical_path']]
        require(row=={'logical_path':source['logical_path'],'public_path':source['public_path'],'representation':source['representation'],'restored_bytes':source['source_bytes'],'restored_sha256':source['source_sha256'],'transport_bytes':source['public_bytes'],'transport_sha256':source['public_sha256']},'Restoration ledger binding mismatch')
    omissions=js('OMISSIONS.json')
    require(omissions['manifest_declared_files_omitted']==[] and omissions['scientific_evidence_omitted']==[],'Undeclared evidence omission')
    require(omissions['private_administrative_files_included']==[],'Private administrative inclusion')
    accept=js('FINAL_ACCEPTANCE.json')
    require(set(accept['results'])=={'c8_method','q7_boundary'},'Wrong accepted-result set')
    for key,item in accept['results'].items():
        for field in ('candidate_manifest','review_manifest','proof','review','verdict'):
            bound=item[field]
            require(bound['logical_path'] in payload,'Acceptance source missing')
            require(info(payload[bound['logical_path']])=={k:bound[k] for k in ('bytes','sha256')},'Final acceptance hash mismatch')
            require(file_index[bound['logical_path']]['public_path']==bound['public_path'],'Acceptance storage path mismatch')
        verdict=json.loads(payload[item['verdict']['logical_path']])
        require(item['verdict_status']==verdict.get('verdict',verdict.get('status')),'Verdict label mismatch')
    c8=accept['results']['c8_method']; q7=accept['results']['q7_boundary']
    cv=json.loads(payload[c8['verdict']['logical_path']]); qv=json.loads(payload[q7['verdict']['logical_path']])
    require(cv['verdict']=='PASS_SCOPED' and cv['candidate_proof_sha256']==c8['proof']['sha256'],'C8 acceptance binding mismatch')
    require(qv['status']=='PASS' and qv['candidate_manifest_sha256']==q7['candidate_manifest']['sha256'] and qv['candidate_report_sha256']==q7['proof']['sha256'],'Q7 acceptance binding mismatch')
    require(q7['candidate_manifest']['sha256']=='5664318bea1b9be54d36b8dc99c3733c016f5e09a18375c581daa1505d0fc95c','Wrong frozen q7 candidate')
    require(q7['review_manifest']['sha256']=='517b2f9c0d5a45882fb88b81c75bc6f2cb77cdecc3801bf2907037981f7cdfb1','Wrong final q7 review')
    require(c8['candidate_manifest']['sha256']=='2369c46276e7c197e6e9cd9c37c340b00cbe639fd0030c5c05cfe7f8dab14505','Wrong frozen C8 candidate')
    require(c8['review_manifest']['sha256']=='1b74a1c8b44a3541b3b82e9f1ff10655f4dedb926ff172e890915643ee5896dc','Wrong final C8 review')
    # Verify all 38 exact original source references made by the current C8 review.
    before=payload['c8_method/review/SOURCE_BINDINGS_BEFORE.json']
    require(before==payload['c8_method/review/SOURCE_BINDINGS_AFTER.json'],'C8 source immutability receipts differ')
    refs=json.loads(before); require(len(refs)==38,'C8 source receipt entry count changed')
    for name,bound in refs.items():
        parts=Path(name).parts
        require(parts[:3]==('/','workspace','shared'),'Unexpected source-reference prefix')
        key=(parts[3],str(Path(*parts[4:])))
        require(key in by_source,'Bound C8 source omitted')
        require(info(by_source[key])=={k:bound[k] for k in ('bytes','sha256')},'C8 inherited binding mismatch')
    # The independent q7 review retains the entire candidate subtree unchanged.
    for logical,data in list(payload.items()):
        if logical.startswith('q7_boundary/candidate/'):
            twin=logical.replace('q7_boundary/candidate/','q7_boundary/review/candidate_rerun/',1)
            require(twin in payload and payload[twin]==data,'Q7 candidate-rerun evidence differs')
    scope=js('CLAIM_SCOPE.json'); cm=scope['c8_method']; qm=scope['q7_boundary']
    require(cm['strict_feasible_epsilon_range']=='0 < epsilon < epsilon_star' and cm['angle_increment']=='epsilon/2','C8 endpoint/sine normalization changed')
    require(not any(cm[k] for k in ('endpoint_is_admissible_in_strict_test','actual_global_optimum_established','all_possible_uses_of_proof_slack_optimized','method_ceiling_non_equality_with_true_optimum_proved')),'C8 overclaim')
    require(qm['N']==35 and qm['degrees']==[8,9,10,11,12,13],'Q7 exact degree scope changed')
    require(not any(qm[k] for k in ('complete_order35_classification','complete_fiveprime_classification','middle_interval_2q_through_4q_covered','full_square_mask_census_claim','new_gap_method_or_optimal_rate')),'Q7 overclaim')
    require(qm['combined_with_inherited_qge11']=='No equality mask at N=5q for prime q>5 and integer q<d<2q.','Combined scope changed')
    require(not any(scope[k] for k in ('historical_novelty_claim','world_first_claim','general_fft_gain_claim','scientific_reruns_during_packaging')),'Unsupported global claim')
    owners=js('OWNER_DISPOSITIONS.json')
    require(owners['owner_closures']==0 and owners['status_changes']==0 and owners['priority_changes']==0 and owners['scores_changed'] is False and owners['canonical_records_modified'] is False,'Owner scope changed')
    for own in owners['owners'].values():
        require(own['owner_closure'] is False and own['priority_change'] is False,'Broad owner incorrectly closed')
    require(owners['owners']['M-SPARSE-DEFECT']['priority']==42,'Sparse owner priority changed')
    require(accept['packaging_independent_review']=='PENDING' and accept['external_publication']=='NOT_PERFORMED' and accept['publication_authorized_by_this_packet'] is False,'Local-only release gate changed')
    return {'status':'PASS','public_files':len(actual),'source_files':len(files),'source_sets':len(sets),'manifest_entries_verified':sum(s['manifest_entries'] for s in sets),'lossless_representations':sum(r['representation']=='GZIP_BASE64' for r in files),'c8_current_review_source_bindings_verified':len(refs),'scientific_programs_executed':False,'external_writes':False}

if __name__=='__main__':
    try:
        print(json.dumps(verify(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent),indent=2))
    except Exception as exc:
        print(json.dumps({'status':'FAIL','reason':str(exc)}),file=sys.stderr)
        raise SystemExit(1)
