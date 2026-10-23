"""Data-only integrity/provenance checker. Does not execute scientific programs."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, zipfile

P = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def expected(item):
    return {key: item[key] for key in ('bytes', 'sha256')}

def same(data, item):
    return pin(data) == expected(item)

def safe(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name

def main():
    m = json.loads((P / 'PUBLIC_MANIFEST.json').read_text())
    direct = m['direct_files']; archives = m['archives']
    require(len(direct) == len({x['path'] for x in direct}), 'Duplicate direct file')
    require(len(archives) == len({x['path'] for x in archives}), 'Duplicate archive')
    paths = {x['path'] for x in direct} | {x['path'] for x in archives} | {'PUBLIC_MANIFEST.json'}
    require({p.name for p in P.iterdir() if p.is_file()} == paths, 'Public file inventory mismatch')
    require(not any(p.is_dir() for p in P.iterdir()), 'Unexpected public directory')
    for x in direct:
        require(safe(x['path']), 'Unsafe direct path')
        require(same((P / x['path']).read_bytes(), x), 'Direct file hash mismatch: ' + x['path'])
    data = {}; archive_bytes = 0
    for x in archives:
        require(safe(x['path']), 'Unsafe ZIP path')
        b = (P / x['path']).read_bytes(); archive_bytes += len(b)
        require(same(b, x), 'ZIP pin mismatch: ' + x['path'])
        require(len(b) <= 409600, 'ZIP exceeds 409600-byte cap')
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            require(z.testzip() is None, 'ZIP CRC failure')
            names = z.namelist()
            require(len(names) == len(set(names)), 'Duplicate ZIP member')
            require(len(x['members']) == len({y['path'] for y in x['members']}), 'Duplicate member declaration')
            require(set(names) == {y['path'] for y in x['members']}, 'ZIP member inventory mismatch')
            for y in x['members']:
                n = y['path']; require(safe(n), 'Unsafe member path')
                require(n not in data, 'Duplicate cross-ZIP member')
                data[n] = z.read(n)
                require(same(data[n], y), 'ZIP member pin mismatch: ' + n)
    projection = m['projection']
    require(json.loads(data['PUBLIC_PROJECTION.json']) == projection, 'Projection copies differ')
    require(json.loads(data['SCOPED_RESULT.json']) == m['scope'], 'Scope copies differ')
    require(json.loads(data['SOURCE_CLOSURE.json']) == m['source_closure'], 'Closure copies differ')
    correspondence = projection['source_correspondence']
    maps = {x['source_path']: x for x in correspondence}
    require(len(maps) == len(correspondence) == projection['source_entries'], 'Mapping count mismatch')
    omissions = {x['source_path']: x for x in projection['omissions']}
    require(len(omissions) == len(projection['omissions']), 'Duplicate omission')
    require(not (set(omissions) & set(maps)), 'Omitted source retained')
    require(len(maps) + len(omissions) == projection['original_packet_files'], 'Original packet inventory mismatch')
    for x in omissions.values():
        require(x['published'] is False and x['scientific'] is False, 'Omission classification invalid')
        require(x['source_path'].startswith('author/helpers/'), 'Unexpected source omitted')
    edits = {x['source_path']: x for x in projection['projections']}
    require(len(edits) == len(projection['projections']), 'Duplicate projection')
    require(set(edits) <= set(maps), 'Projection without mapping')
    reconstruction = m['original_archive']; chunks = reconstruction['chunks']
    parts = []; offset = 0
    for x in chunks:
        require(x['offset'] == offset, 'Source-archive chunk is not contiguous')
        require(same(data[x['path']], x), 'Source-archive chunk mismatch')
        parts.append(data[x['path']]); offset += x['bytes']
    original_archive = b''.join(parts)
    require(pin(original_archive) == reconstruction['original'] == reconstruction['public'], 'Reconstructed archive pin mismatch')
    require(reconstruction['source_path'] not in data, 'Original archive unexpectedly duplicated')
    expected_payload = {'PUBLIC_PROJECTION.json', 'SCOPED_RESULT.json', 'SOURCE_CLOSURE.json'} | {x['path'] for x in chunks} | {x['archive_path'] for x in correspondence if 'archive_path' in x}
    require(set(data) == expected_payload, 'Unclassified ZIP payload')
    data[reconstruction['source_path']] = original_archive
    for n, x in maps.items():
        b = data[n]
        require(pin(b) == x['public'], 'Public mapping pin mismatch: ' + n)
        if x['disposition'] in ('byte-exact', 'byte-exact-reassembled'):
            require(x['original'] == x['public'], 'False byte-exact claim')
            require(n not in edits, 'Exact source is projected')
            if x['disposition'] == 'byte-exact-reassembled':
                require(n == reconstruction['source_path'] and x['reconstruction'] == 'original_archive', 'Unexpected reconstruction')
        else:
            require(x['disposition'] == 'documentary-locator-only' and n in edits, 'Undeclared projection')
            require(not n.endswith('.py'), 'Program projection forbidden')
            e = edits[n]
            require(e['original'] == x['original'] and e['public'] == x['public'], 'Projection pins mismatch')
            require(b.count(e['replacement'].encode()) == e['occurrences'], 'Projection marker mismatch')
    with zipfile.ZipFile(io.BytesIO(original_archive)) as z:
        require(z.testzip() is None, 'Original archive CRC failure')
        names = z.namelist(); inventory = reconstruction['members']
        require(len(names) == len(set(names)), 'Duplicate original archive member')
        require(len(inventory) == len({x['path'] for x in inventory}), 'Duplicate original member declaration')
        require(set(names) == {x['path'] for x in inventory}, 'Original archive inventory mismatch')
        historical = {}
        for x in inventory:
            n = x['path']; require(safe(n), 'Unsafe original member')
            historical[n] = z.read(n)
            require(same(historical[n], x), 'Original member mismatch: ' + n)
        sums = []
        for line in historical[reconstruction['original_manifest_path']].decode().splitlines():
            digest, rel = line.strip().split('  ', 1); n = 'phase56/' + rel
            require(safe(rel), 'Unsafe original checksum path')
            require(pin(historical[n])['sha256'] == digest, 'Original checksum mismatch: ' + n)
            sums.append({'path': n, 'sha256': digest})
        require(sums == reconstruction['original_manifest_entries'], 'Original checksum inventory differs')
        require({x['path'] for x in sums} | {reconstruction['original_manifest_path']} == set(names), 'Original checksum closure incomplete')
    for n in ['PHASE56_THEOREMS.md', 'PHASE56_START_HERE.md', 'fourier_fit_experiment.py', 'jacobian_probe.py']:
        require(data['author/source/' + n] == historical['phase56/' + n], 'Historical source copy mismatch: ' + n)
    def original(n):
        require(n in maps or n in omissions, 'Unclassified original entry: ' + n)
        return (maps[n] if n in maps else omissions[n])['original']
    for x in projection['historical_manifests']:
        require(same(data[x['path']], x), 'Original manifest bytes differ')
        require(maps[x['path']]['disposition'] == 'byte-exact', 'Original manifest was edited')
    am = json.loads(data['author/MANIFEST.json'])
    for x in am['files']:
        require(original('author/' + x['path']) == {'bytes': x['size_bytes'], 'sha256': x['sha256']}, 'Candidate original inventory mismatch')
    rm = json.loads(data['review/MANIFEST.json'])
    for n, x in rm.items():
        require(original('review/' + n) == x, 'Review original inventory mismatch: ' + n)
    ab = json.loads(data['author/SOURCE_BINDING.json'])
    require(ab['original_source_archive']['sha256'] == pin(original_archive)['sha256'], 'Candidate archive binding mismatch')
    for k in ['original_theorem', 'original_cycle_sampling_read_only']:
        x = ab[k]
        require(pin(historical[x['archive_path']])['sha256'] == x['sha256'], 'Candidate historical binding mismatch')
    for x in ab['candidate_files']:
        require(original('author/' + x['path'])['sha256'] == x['sha256'], 'Candidate self-binding mismatch')
    rb = json.loads(data['review/BINDINGS.json']); verdict = json.loads(data['review/VERDICT.json'])
    require(rb['author_manifest'] == original('author/MANIFEST.json') == verdict['author_manifest'], 'Review author-manifest binding mismatch')
    require(rb['inventory'] == am, 'Review embedded author inventory mismatch')
    require(rb['original_archive'] == pin(original_archive), 'Review original archive binding mismatch')
    require(data['review/RESULT.json'] == data['review/RESULT_OPT.json'], 'Stored normal/optimized results differ')
    result = json.loads(data['review/RESULT.json'])
    require(result['total'] == 62 == verdict['independent_checks'] == m['scope']['stored_independent_controls'], 'Stored control count mismatch')
    require(verdict['decision'] == m['scope']['status'], 'Scope/decision mismatch')
    for x in m['direct_science_copies']:
        require((P / x['path']).read_bytes() == data[x['archive_path']], 'Direct scientific copy mismatch')
    programs = m['source_closure']['scientific_programs']
    require(len(programs) == len({(x['container'], x['path']) for x in programs}), 'Duplicate program declaration')
    observed = {(('reconstructed original archive' if n in historical else 'evidence-01.zip'), n) for n in list(data) + list(historical) if n.endswith('.py')}
    require(observed == {(x['container'], x['path']) for x in programs}, 'Scientific program inventory incomplete')
    for x in programs:
        b = historical[x['path']] if x['container'] == 'reconstructed original archive' else data[x['path']]
        require(x['byte_exact'] is True and same(b, x), 'Scientific program pin mismatch')
    require(len({x['sha256'] for x in programs}) == m['source_closure']['unique_scientific_program_sha256_count'], 'Unique program count mismatch')
    print(json.dumps({'verified': True, 'archive_parts': len(archives), 'archive_bytes': archive_bytes, 'source_entries': len(maps), 'original_packet_files': projection['original_packet_files'], 'original_archive_members': len(historical), 'original_archive_checksum_entries': len(sums), 'candidate_inventory_entries': len(am['files']), 'review_inventory_entries': len(rm), 'excluded_non_scientific_files': len(omissions), 'documentary_projections': len(edits), 'scientific_program_locations': len(programs), 'scientific_programs_unique': len({x['sha256'] for x in programs}), 'stored_review_controls': result['total'], 'scientific_execution': False, 'turnkey_scientific_replay_certified': False}, sort_keys=True))

if __name__ == '__main__':
    main()
