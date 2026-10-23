"""Read-only, data-only public evidence verification. Never executes archived code."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, struct, zipfile
P=Path(__file__).resolve().parent

def require(test,message):
    if not test: raise RuntimeError(message)
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def same(b,e): return pin(b)=={k:e[k] for k in ('bytes','sha256')}
def safe(n):
    p=PurePosixPath(n)
    return bool(n) and not p.is_absolute() and '..' not in p.parts and '\\' not in n

def archive(read,m):
    chunks=[]; offset=0; seen=set()
    for q in m['parts']:
        require(safe(q['path']) and q['path'] not in seen,'Unsafe or duplicate archive part')
        seen.add(q['path']); b=read(q['path'])
        require(same(b,q) and 0<len(b)<=409600,'Archive part hash/size mismatch: '+q['path'])
        require(q['offset']==offset,'Archive part offset mismatch'); offset+=len(b);chunks.append(b)
    raw=b''.join(chunks);require(same(raw,m),'Archive hash/size mismatch')
    z=zipfile.ZipFile(io.BytesIO(raw)); require(z.testzip() is None,'ZIP CRC failure')
    names=z.namelist(); require(len(names)==len(set(names)),'Duplicate archive member')
    require(all(safe(n) for n in names),'Unsafe archive member')
    require(len(m['members'])==len({x['path'] for x in m['members']}),'Duplicate declared member')
    require(set(names)=={x['path'] for x in m['members']},'Archive membership mismatch')
    for q in m['members']:require(same(z.read(q['path']),q),'Archive member mismatch: '+q['path'])
    return z,raw

def dependency(read,m):
    z,raw=archive(read,m['archive'])
    copies=m['projection']['correspondence']; c={x['archive_path']:x for x in copies}
    require(len(c)==len(copies)==m['projection']['source_entries'],'Dependency source inventory mismatch')
    for n,x in c.items():
        require(pin(z.read(n))==x['public'],'Dependency public correspondence mismatch')
        if x['disposition']=='byte-exact': require(x['original']==x['public'] and not x['changes'],'False dependency exact claim')
        else:
            require(x['disposition']=='administrative-only projection' and x['changes'],'Unknown inherited projection')
    for q in m['source_manifests']:
        b=z.read(q['archive_path']);require(same(b,q),'Dependency original inventory mismatch'); prefix=q['archive_path'].rsplit('/',1)[0]
        d=json.loads(b);require(len(d)==q['source_entries'],'Dependency original inventory count mismatch')
        for n,x in d.items():require(c[prefix+'/'+n]['original']==x,'Dependency original mapping mismatch')
    for q in m['direct_files']:require(same(read(q['path']),q),'Dependency direct file mismatch')
    for q in m['direct_science_copies']:require(read(q['path'])==z.read(q['archive_path']),'Dependency direct science mismatch')
    require(json.loads(z.read('PUBLIC_PROJECTION.json'))==m['projection'],'Dependency projection metadata mismatch')
    require(json.loads(z.read('SCOPED_RESULT.json'))==m['scope'],'Dependency scoped metadata mismatch')
    return z,raw

def main():
    m=json.loads((P/'PUBLIC_MANIFEST.json').read_bytes())
    direct=m['direct_files'];require(len(direct)==len({q['path'] for q in direct}),'Duplicate direct files')
    expected={q['path'] for q in direct}|{q['path'] for q in m['archive']['parts']}|{'PUBLIC_MANIFEST.json'}
    require({q.name for q in P.iterdir() if q.is_file()}==expected,'Direct inventory mismatch')
    for q in direct:
        require(safe(q['path']),'Unsafe direct path');require(same((P/q['path']).read_bytes(),q),'Direct file mismatch: '+q['path'])
    z,raw=archive(lambda n:(P/n).read_bytes(),m['archive'])
    projection=m['projection'];require(json.loads(z.read('PUBLIC_PROJECTION.json'))==projection,'Projection mismatch')
    require(json.loads(z.read('SCOPED_RESULT.json'))==m['scope'],'Scope mismatch')
    maps={q['archive_path']:q for q in projection['source_correspondence']}
    require(len(maps)==len(projection['source_correspondence'])==projection['source_entries'],'Source correspondence count mismatch')
    require(set(z.namelist())==set(maps)|{'PUBLIC_PROJECTION.json','SCOPED_RESULT.json'},'Unmapped archive members')
    for n,q in maps.items():require(pin(z.read(n))==q['public']==q['original'] and q['disposition']=='byte-exact','Source bytes not preserved: '+n)
    omitted={q['source_path']:q for q in projection['omissions']}
    require(not set(omitted)&set(maps),'Omitted source included')
    for q in omitted.values():require(q['published'] is False and q['classification']=='compiled-machine-cache','Unexpected omission')
    manifest_count=0
    for q in projection['historical_manifests']:
        b=z.read(q['archive_path']);require(same(b,q),'Current original manifest mismatch')
        d=json.loads(b);d=d['files'] if 'files' in d else d
        for n,e in d.items():
            name=q['inventory_prefix']+'/'+n;require(maps[name]['original']==e,'Original inventory mapping mismatch: '+name);manifest_count+=1
    bind=json.loads(z.read('review/BINDINGS.json'))
    require(bind['author_manifest']==pin(z.read('author/MANIFEST.json')),'Review-author manifest binding mismatch')
    for n,e in bind['author_members'].items():require(pin(z.read('author/'+n))==e,'Review original member binding mismatch')
    ab=json.loads(z.read('author/SOURCE_BINDINGS.json'))
    for n,digest in ab['bound_inert_source_hashes'].items():require(pin(z.read('author/'+n))['sha256']==digest,'Author inert binding mismatch')
    require(ab['original_model_same_session_authorship']['sha256']==pin(z.read('author/original_model.py'))['sha256'],'Original model binding mismatch')
    verdict=json.loads(z.read('review/VERDICT.json'))
    for key,name in [('author_manifest','author/MANIFEST.json'),('author_proof','author/PROOF.md'),('original_chart','author/sources/CHART.json')]:require(verdict[key]==pin(z.read(name)),'Verdict source binding mismatch')
    require(bind['original_chart']==pin(z.read('author/sources/CHART.json')),'Review chart binding mismatch')
    for a,b in [('author/EXACT_CONTROLS.json','author/EXACT_CONTROLS.log'),('review/EXACT_RESULT.json','review/EXACT_RESULT_OPT.json'),('review/RESULT.json','review/RESULT_NORMAL.json')]:require(z.read(a)==z.read(b),'Stored output pair differs')
    for r in (256,65281):
        b=z.read('author/MATRIX_'+str(r)+'.bin');require(struct.unpack('<II',b[:8])==(2268,1360) and len(b)==8+4*2268*1360,'Matrix dimensions/length mismatch')
        meta=json.loads(z.read('author/META_'+str(r)+'.json'));require(meta['matrix_sha256']==pin(b)['sha256'],'Matrix metadata binding mismatch')
    dep=m['dependency'];pre=dep['archive_prefix'];dm=json.loads(z.read(pre+'PUBLIC_MANIFEST.json'));dz,draw=dependency(lambda n:z.read(pre+n),dm)
    require(same(draw,dep['reassembled_archive']),'Pinned inherited archive mismatch')
    for q in dep['exact_cross_bindings']:require(z.read(q['current_archive_path'])==dz.read(q['dependency_member']),'Inherited bound dependency differs')
    for q in m['direct_science_copies']:require((P/q['path']).read_bytes()==z.read(q['archive_path']),'Direct scientific copy differs')
    require(m['scope']['coordinates']==[7,8,16,31,32,40] and m['scope']['coordinate_labels']==1,'Wrong six-phase scope')
    require(m['scope']['original_inverse_guards']==6 and m['scope']['owner_priority']==50,'Guard/owner scope mismatch')
    require(m['scope']['turnkey_scientific_replay_certified'] is False,'Unsupported replay claim')
    print(json.dumps({'verified':True,'archive_bytes':len(raw),'archive_parts':len(m['archive']['parts']),'archive_members':len(z.namelist()),'source_entries':len(maps),'historical_manifest_entries':manifest_count,'dependency_archive_bytes':len(draw),'dependency_archive_members':len(dz.namelist()),'current_programs_byte_exact':8,'excluded_caches':len(omitted),'scientific_execution':False,'turnkey_scientific_replay_certified':False},sort_keys=True))

if __name__=='__main__':main()
