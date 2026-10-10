#!/usr/bin/env python3
"""New audit code: treat all uploaded archive bytes as inert data."""
import hashlib, io, json, re, stat, zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
prior = json.loads((ROOT/'PRIOR_HASH_REFERENCE.json').read_text())
known_base = set(prior['baseline']['hashes'])
known_prev = set(prior['previous_additions']['hashes'])
known = known_base | known_prev
records, manifests, archives = [], [], []
bytes_seen = 0

def walk(blob, chain, depth=0):
    global bytes_seen
    assert depth < 12, 'archive nesting depth cap'
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        infos = z.infolist()
        assert len(infos) < 10000
        assert sum(i.file_size for i in infos) < 100_000_000
        content = {}
        for i in infos:
            p = PurePosixPath(i.filename)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
            assert not stat.S_ISLNK(i.external_attr >> 16)
            if i.is_dir():
                continue
            assert i.filename not in content, 'duplicate archive path'
            b = z.read(i)
            bytes_seen += len(b)
            assert bytes_seen < 500_000_000
            content[i.filename] = b
            digest = hashlib.sha256(b).hexdigest()
            records.append({'chain':chain,'member_path':i.filename,'sha256':digest,'bytes':len(b),
                            'known_in_base_texts':digest in known_base,
                            'known_in_prior_additions':digest in known_prev,
                            'new_to_combined_prior':digest not in known})
        for name, b in content.items():
            if PurePosixPath(name).name.lower() in ('sha256sums.txt','sha256sums','manifest.sha256'):
                for line in b.decode('utf-8').splitlines():
                    if not line.strip(): continue
                    m = re.fullmatch(r'([0-9a-fA-F]{64})\s+\*?(.+)',line)
                    if not m:
                        manifests.append({'chain':chain,'manifest':name,'line':line,'status':'unparsed'})
                        continue
                    expected, ref = m.groups()
                    candidates = [str(PurePosixPath(name).parent / ref), ref]
                    matches = list(dict.fromkeys(p for p in candidates if p in content))
                    good = [p for p in matches if hashlib.sha256(content[p]).hexdigest()==expected.lower()]
                    manifests.append({'chain':chain,'manifest':name,'referenced_path':ref,
                                      'resolved_path':good[0] if good else (matches[0] if matches else None),
                                      'expected':expected.lower(),
                                      'status':'pass' if good else ('mismatch' if matches else 'missing')})
            if name.lower().endswith('.zip'):
                walk(b,chain+'!/'+name,depth+1)

for p in sorted((ROOT/'source_archives').glob('*.zip')):
    b=p.read_bytes(); before=len(records)
    walk(b,p.name)
    sub=records[before:]
    archives.append({'archive':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                     'member_occurrences':len(sub),'unique_hashes':len({r['sha256'] for r in sub}),
                     'new_unique_hashes':len({r['sha256'] for r in sub if r['new_to_combined_prior']})})

summary={'member_occurrences':len(records),'unique_hashes':len({r['sha256'] for r in records}),
         'known_occurrences':sum(not r['new_to_combined_prior'] for r in records),
         'new_unique_hashes':len({r['sha256'] for r in records if r['new_to_combined_prior']}),
         'total_recursive_uncompressed_bytes':bytes_seen,'by_archive':archives,
         'source_manifest_entries':len(manifests),'source_manifest_passed':sum(r['status']=='pass' for r in manifests),
         'source_manifest_failures':[r for r in manifests if r['status']!='pass'],
         'comparison_scope':'528 baseline canonical text contents plus all 417 member occurrences of 14:50 additions; inventories remain distinct.'}
(ROOT/'SOURCE_MEMBER_INVENTORY.json').write_text(json.dumps(records,indent=2)+'\n')
(ROOT/'source_manifest_verification.json').write_text(json.dumps(manifests,indent=2)+'\n')
(ROOT/'recursive_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
