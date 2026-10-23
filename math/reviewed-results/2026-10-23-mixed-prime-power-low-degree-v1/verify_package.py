"""Data-only package integrity verifier. Never executes archived scientific code."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, zipfile

P=Path(__file__).resolve().parent
def require(condition,message):
    if not condition:
        raise RuntimeError(message)
def pin(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def same(data,item):
    return pin(data)=={key:item[key] for key in ('bytes','sha256')}
def rows(raw):
    x=json.loads(raw)
    if isinstance(x,dict) and 'files' in x:
        x=x['files']
    if isinstance(x,dict):
        return [dict(path=k,**v) for k,v in x.items()]
    return [dict(path=v.get('path',v.get('file')),bytes=v.get('bytes',v.get('size')),sha256=v['sha256']) for v in x]
def pointer(obj,path):
    for field in path.lstrip('/').split('/'):
        obj=obj[int(field)] if isinstance(obj,list) else obj[field]
    return obj
def main():
    m=json.loads((P/'PUBLIC_MANIFEST.json').read_text())
    pieces=[]
    for item in m['archive']['parts']:
        data=(P/item['path']).read_bytes()
        require(same(data,item),'Archive part mismatch: '+item['path'])
        require(len(data)<=409600,'Oversized raw archive part')
        pieces.append(data)
    data=b''.join(pieces)
    require(same(data,m['archive']),'Assembled archive mismatch')
    z=zipfile.ZipFile(io.BytesIO(data))
    require(z.testzip() is None,'ZIP CRC failure')
    names=z.namelist()
    require(len(names)==len(set(names)),'Duplicate ZIP member')
    require(set(names)=={x['path'] for x in m['archive']['members']},'ZIP member inventory mismatch')
    for name in names:
        p=PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts,'Unsafe archive member')
        require((z.getinfo(name).external_attr>>16)&0o170000==0o100000,'Non-regular ZIP member')
    for item in m['archive']['members']:
        require(same(z.read(item['path']),item),'Member mismatch: '+item['path'])
    projection=m['projection']
    require(json.loads(z.read('PUBLIC_PROJECTION.json'))==projection,'Projection metadata mismatch')
    require(json.loads(z.read('SCOPED_RESULT.json'))==m['scope'],'Scope metadata mismatch')
    maps={x['archive_path']:x for x in projection['source_correspondence']}
    omissions={x['archive_path']:x for x in projection['omitted_non_scientific_sources']}
    require(len(maps)==projection['included_source_entries'],'Included source count mismatch')
    require(len(maps)+len(omissions)==projection['source_entries_examined'],'Original source count mismatch')
    require(not(set(maps)&set(omissions)),'Included source also omitted')
    require(set(names)==set(maps)|{'SCOPED_RESULT.json','PUBLIC_PROJECTION.json'},'Source coverage mismatch')
    originals={name:x['original'] for name,x in maps.items()}
    originals.update({name:x['original'] for name,x in omissions.items()})
    for name,item in maps.items():
        raw=z.read(name)
        require(pin(raw)==item['public'],'Public source correspondence mismatch: '+name)
        if item['disposition']=='byte-exact':
            require(item['original']==item['public'] and not item['changes'],'False exact-copy claim')
            if 'original_git_blob_sha' in item:
                actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
                require(actual==item['original_git_blob_sha'],'Remote original Git blob mismatch')
        else:
            require(item['disposition']=='documentary-projection','Unknown source disposition')
            require(name.endswith('SOURCE_BINDINGS.json'),'Unexpected projection target')
            require(len(item['changes'])==1,'Unexpected projection field count')
            change=item['changes'][0]
            require(change['json_pointer']=='/0/original' and change['scientific_claim_changed'] is False,'Unexpected projected field')
            require(pointer(json.loads(raw),change['json_pointer'])==change['public_value'],'Projected value mismatch')
    require(sum(x['disposition']=='byte-exact' for x in maps.values())==projection['byte_exact_entries'],'Exact-copy count mismatch')
    require(sum(x['disposition']=='documentary-projection' for x in maps.values())==projection['projected_entries'],'Projection count mismatch')
    manifest_checks=0
    for item in projection['historical_manifests']:
        raw=z.read(item['archive_path'])
        require(same(raw,item),'Original manifest bytes changed')
        for row in rows(raw):
            name=item['inventory_prefix']+'/'+row['path']
            expected={'bytes':row.get('bytes',row.get('size')),'sha256':row['sha256']}
            require(name in originals and originals[name]==expected,'Original inventory mismatch: '+name)
            manifest_checks+=1
    for item in projection['historical_seals']:
        raw=z.read(item['archive_path'])
        require(same(raw,item),'Original seal changed')
        require(raw.decode().split()[0]==item['target_original_sha256'],'Seal record mismatch')
        require(originals[item['target_archive_path']]['sha256']==item['target_original_sha256'],'Sealed original digest mismatch')
    for item in projection['scientific_binding_fields']:
        value=pointer(json.loads(z.read(item['source'])),item['json_pointer'])
        require(value==item['expected_original_sha256']==originals[item['target_archive_path']]['sha256'],'Scientific binding mismatch')
    for item in projection['source_bindings']:
        row=json.loads(z.read(item['binding_document']))[item['entry_index']]
        name=item['target_archive_path']
        require(row['sha256']==item['expected_original_sha256']==originals[name]['sha256'],'Source SHA mismatch')
        require(row.get('bytes',row.get('size'))==originals[name]['bytes'],'Source size mismatch')
        if item['target_disposition']=='omitted_non_scientific':
            require(name in omissions and name not in names,'Omitted record present')
        else:
            require(name in maps,'Missing scientific source')
        if 'expected_git_blob_sha' in item:
            raw=z.read(name)
            require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['expected_git_blob_sha']==row['git_blob_sha'],'Source Git blob mismatch')
    for item in projection['stored_byte_equivalences']:
        left=z.read(item['left']);right=z.read(item['right'])
        require(left==right and pin(left)['sha256']==item['sha256'],'Stored equivalence mismatch')
    for item in projection['scientific_programs']:
        require(same(z.read(item['archive_path']),item),'Scientific program changed')
        require(item['executed'] is False and maps[item['archive_path']]['disposition']=='byte-exact','Scientific source preservation mismatch')
    for item in m['direct_science_copies']:
        require((P/item['path']).read_bytes()==z.read(item['archive_path']),'Direct scientific copy mismatch')
    expected={'PUBLIC_MANIFEST.json'}|{x['path'] for x in m['direct_files']}|{x['path'] for x in m['archive']['parts']}
    require({x.name for x in P.iterdir()}==expected,'Unexpected direct package member')
    for item in m['direct_files']:
        require(same((P/item['path']).read_bytes(),item),'Direct file mismatch: '+item['path'])
    require(all(x.stat().st_size<=409600 for x in P.iterdir()),'Oversized public raw file')
    print(json.dumps({'verified':True,'archive_bytes':len(data),'archive_members':len(names),'included_sources':len(maps),'explicit_non_scientific_omissions':len(omissions),'original_manifest_member_checks':manifest_checks,'scientific_execution':False},sort_keys=True))
if __name__=='__main__':
    main()
