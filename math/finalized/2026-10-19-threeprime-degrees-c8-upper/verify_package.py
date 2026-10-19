"""Read-only packaging verifier. Never imports or executes research code."""
from pathlib import Path
import hashlib
import base64
import binascii
import gzip
import json

ROOT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_text())

def require(condition, message):
    if not condition:
        raise ValueError(message)

def safe(name):
    p = Path(name)
    require(not p.is_absolute() and '..' not in p.parts, 'Unsafe package path: ' + name)
    return ROOT / p

def source_data(name):
    entries = read('SOURCE_REPRESENTATIONS.json')['files']
    matches = [e for e in entries if e['logical_path'] == name]
    if not matches:
        return safe(name).read_bytes()
    require(len(matches) == 1, 'Duplicate logical representation')
    item = matches[0]
    require(not safe(name).exists(), 'Both logical and encoded source exist')
    require(item['encoded_path'] == name + '.gz.b64', 'Unexpected encoded path')
    require(item['codec'] == 'gzip+base64', 'Unknown representation codec')
    encoded = safe(item['encoded_path']).read_bytes()
    require(hashlib.sha256(encoded).hexdigest() == item['encoded_sha256'] and len(encoded) == item['encoded_bytes'], 'Encoded representation mismatch')
    require(encoded.endswith(b'\n') and b'\r' not in encoded, 'Noncanonical base64 newlines')
    lines = encoded[:-1].split(b'\n')
    require(all(len(x) == 76 for x in lines[:-1]) and 1 <= len(lines[-1]) <= 76, 'Noncanonical base64 line width')
    packed = base64.b64decode(b''.join(lines), validate=True)
    canonical = base64.b64encode(packed)
    require(encoded == b'\n'.join(canonical[i:i+76] for i in range(0,len(canonical),76)) + b'\n', 'Noncanonical base64 encoding')
    require(len(packed) == item['compressed_bytes'] and hashlib.sha256(packed).hexdigest() == item['compressed_sha256'], 'Compressed representation mismatch')
    require(packed[:10] == bytes([31,139,8,0,0,0,0,0,2,255]), 'Nondeterministic gzip header')
    decoded = gzip.decompress(packed)
    require(len(decoded) == item['source_bytes'] and hashlib.sha256(decoded).hexdigest() == item['source_sha256'], 'Decoded source mismatch')
    require(item['source_bytes'] > 2000000 and name.endswith('/NEGATIVE_CONTROLS.json'), 'Unapproved representation scope')
    require(item['reversible'] is True and item['scientific_bytes_changed'] is False, 'Invalid representation claim')
    return decoded

def source_entries(manifest, style):
    if style == 'files':
        return manifest['files']
    if style in ('certificate', 'review_files'):
        return [dict(path=n, **v) for n, v in manifest[style].items()]
    raise ValueError('Unknown source manifest style: ' + style)

def verify():
    allow = read('PRESERVATION_ALLOWLIST.json')['files']
    require(allow == sorted(set(allow)), 'Allowlist duplicates or unsorted paths')
    actual = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file())
    require(actual == allow, 'Allowlist does not match exact public tree')
    require(not any(p.is_symlink() for p in ROOT.rglob('*')), 'Symlink in public tree')
    manifest = read('MANIFEST.json')
    names = [v['path'] for v in manifest['files']]
    require(set(names) == set(allow) - {'MANIFEST.json', 'SEAL.json'}, 'Manifest coverage mismatch')
    require(len(names) == len(set(names)), 'Duplicate manifest path')
    for item in manifest['files']:
        p = safe(item['path'])
        require(p.stat().st_size == item['bytes'] and digest(p) == item['sha256'], 'Manifest mismatch: ' + item['path'])
    seal = read('SEAL.json')
    for name, key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITIONS.json','owner_dispositions_sha256')]:
        require(digest(ROOT/name) == seal[key], 'Seal mismatch: ' + name)
    copies = read('COPY_BINDINGS.json')
    for item in copies['files']:
        p = safe(item['public_path'])
        require(digest(p) == item['public_sha256'] and p.stat().st_size == item['public_bytes'], 'Published source representation mismatch')
        data = source_data(item.get('logical_path', item['public_path']))
        require(hashlib.sha256(data).hexdigest() == item['source_sha256'] and len(data) == item['source_bytes'], 'Exact decoded source mismatch')
        require(item['transformation'] in ('EXACT_COPY', 'REVERSIBLE_GZIP_BASE64'), 'Unknown source transformation')
        if item['transformation'] == 'REVERSIBLE_GZIP_BASE64':
            require(item['decoded_sha256'] == item['source_sha256'] and item['decoded_bytes'] == item['source_bytes'], 'Decoded binding mismatch')
        else:
            require(item['source_sha256'] == item['public_sha256'] and item['source_bytes'] == item['public_bytes'], 'Literal copy mismatch')
    for item in copies['source_sets']:
        prefix = item['public_prefix']
        mp = safe(prefix + '/MANIFEST.json')
        require(digest(mp) == item['manifest_sha256'], 'Source manifest changed')
        for entry in source_entries(json.loads(mp.read_text()), item['style']):
            logical = prefix + '/' + entry['path']
            data = source_data(logical)
            require(hashlib.sha256(data).hexdigest() == entry['sha256'] and len(data) == entry['bytes'], 'Source coverage failure: ' + logical)
    representations = read('SOURCE_REPRESENTATIONS.json')
    expected = {'threeprime/candidate/NEGATIVE_CONTROLS.json', 'threeprime/review/NEGATIVE_CONTROLS.json'}
    require({e['logical_path'] for e in representations['files']} == expected and len(representations['files']) == 2, 'Representation coverage mismatch')
    require(all(safe(f).stat().st_size <= 2000000 for f in actual), 'Oversized physical publication file')
    require(digest(ROOT/'SOURCE_REPRESENTATIONS.json') == seal['representations_sha256'], 'Representation seal mismatch')
    accept = read('FINAL_ACCEPTANCE.json')
    for item in accept['results'].values():
        for field in ('proof','review','verdict'):
            require(digest(safe(item[field+'_path'])) == item[field+'_sha256'], 'Acceptance binding mismatch')
    require(read('threeprime/review/VERDICT.json')['verdict'] == 'PASS', 'Threeprime review not accepted')
    require(read('c8_upper/review/VERDICT.json')['verdict'] == 'ACCEPT', 'C8 review not accepted')
    scope = read('CLAIM_SCOPE.json')
    require(scope['threeprime']['positive_degrees'] == ['1','3','q','3q'], 'Wrong threeprime degree scope')
    require(scope['threeprime']['q_condition'] == 'q prime > 3', 'Wrong threeprime quantifier')
    require(scope['threeprime']['full_support_classification'] is False, 'Improper support classification')
    require(scope['threeprime']['general_pq_closure'] is False, 'Improper general pq closure')
    require(scope['c8']['upper'] == 'sqrt(1+sqrt(sqrt(2)-1))/2', 'Wrong C8 upper bound')
    require(scope['c8']['strict_lower'] == 'sin(3*pi/16)', 'Wrong inherited strict lower bound')
    require(scope['c8']['exact_global_optimum_established'] is False, 'Improper C8 optimality claim')
    require(scope['c8']['periodicity_role'] == 'witness only', 'Improper periodicity reduction')
    owners = read('OWNER_DISPOSITIONS.json')['owners']
    for owner, priority in [('M-SPARSE-DEFECT',42),('PHASE-DEFECT-RANK-20261011',37)]:
        require(owners[owner]['status'] == 'TO RESEARCH', 'Owner improperly closed')
        require(owners[owner]['priority'] == priority, 'Priority changed')
        require(owners[owner]['owner_closure'] is False, 'Owner closure claimed')
    for f in actual:
        require(not any(x in f.lower() for x in ['private_owner','live_celldata','full_native_owner','read_chunk','recommendations']), 'Private filename in public tree')
        require(Path(f).suffix.lower() not in {'.pdf','.docx','.xlsx','.zip','.png','.jpg','.pyc'}, 'Disallowed public file type')
    for flag in ('scientific_reruns_during_packaging','external_writes','prior_packets_modified'):
        require(seal[flag] is False, 'Invalid packaging activity flag')
    return {'verdict':'PASS','public_files':len(actual),'public_bytes':sum(safe(p).stat().st_size for p in actual),'unmodified_source_copies':sum(e['transformation']=='EXACT_COPY' for e in copies['files']),'reversible_encoded_sources':sum(e['transformation']=='REVERSIBLE_GZIP_BASE64' for e in copies['files']),'exact_restorable_sources':len(copies['files']),'source_sets':len(copies['source_sets']),'scientific_programs_executed':False}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
