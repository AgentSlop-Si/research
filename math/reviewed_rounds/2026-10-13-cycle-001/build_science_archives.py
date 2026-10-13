"""Build hash-verified evidence archives without altering sealed inputs."""
from pathlib import Path
import hashlib
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
WORKSPACE = BASE.parent
OUT = BASE / 'followon_stage'

GROUPS = {
    'rs_b27': [('next_cycle_rs', 'FILE_MANIFEST.json'), ('next_cycle_rs_review', 'MANIFEST.json')],
    'rs_b29': [('next_cycle_b29', 'FILE_MANIFEST.json'), ('next_cycle_b29_review', 'FILE_MANIFEST.json')],
    'chirp_rank_two': [('next_cycle_chirp', 'MANIFEST.json'), ('next_cycle_chirp_review', 'MANIFEST.json')],
    'prefix_p13': [('next_cycle_prefix', 'MANIFEST.json'), ('next_cycle_prefix_completion', 'MANIFEST.json'), ('next_cycle_prefix_full_review', 'MANIFEST.json')],
    'rs_b27_fusion': [('next_cycle_fusion', 'MANIFEST.json'), ('next_cycle_fusion_review', 'MANIFEST.json'), ('next_cycle_fusion_prior', 'MANIFEST.json')],
    'gaussian_preweights': [('next_cycle_approx', 'MANIFEST.json'), ('next_cycle_approx_review', 'MANIFEST.json')],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def add_sealed(folder, manifest_name, payloads):
    manifest = folder / manifest_name
    data = json.loads(manifest.read_text())
    files = data.get('files', data.get('artifacts'))
    entries = [dict(v,path=k) for k,v in files.items()] if isinstance(files,dict) else files
    for entry in entries:
        name = entry.get('path',entry.get('file',entry.get('name')))
        path = (folder/name).resolve()
        assert path.is_relative_to(WORKSPACE.resolve())
        content = path.read_bytes()
        assert sha(content) == entry['sha256'], path
        if 'bytes' in entry:
            assert len(content) == entry['bytes'], path
        payloads[str(path.relative_to(WORKSPACE))] = content
    payloads[str(manifest.relative_to(WORKSPACE))] = manifest.read_bytes()


def write_archive(name, payloads):
    archive = OUT/'archives'/f'{name}.zip'
    inventory = [{'path':path,'bytes':len(data),'sha256':sha(data)} for path,data in sorted(payloads.items())]
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path,data in sorted(payloads.items()):
            info = zipfile.ZipInfo(path,(2026,10,13,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert z.namelist() == sorted(payloads)
        for row in inventory:
            assert sha(z.read(row['path'])) == row['sha256']
    return {'path':str(archive.relative_to(OUT)), 'bytes':archive.stat().st_size,
            'sha256':sha(archive.read_bytes()), 'files':inventory,
            'reproducibility':'Sealed evidence snapshot. Historical dependencies and source-specific path assumptions remain documented in the component reports; not a standalone full-project environment.'}


def main():
    (OUT/'archives').mkdir(parents=True,exist_ok=True)
    index=[]
    for group,components in GROUPS.items():
        payloads={}
        for folder,manifest in components:
            add_sealed(BASE/folder,manifest,payloads)
        if group=='rs_b27_fusion':
            correction=BASE/'next_cycle_management/FUSION_PUBLICATION_CORRECTION.md'
            payloads[str(correction.relative_to(WORKSPACE))]=correction.read_bytes()
        index.append(write_archive(group,payloads))
    payloads={}
    add_sealed(WORKSPACE/'next_cycle_qtorus_control','REVIEW_SEAL.json',payloads)
    index.append(write_archive('qtorus_finite_control',payloads))
    result={'status':'Local sealed science archives verified; not yet published',
            'archives':index,'archive_count':len(index),'source_file_count':sum(len(x['files']) for x in index),
            'total_archive_bytes':sum(x['bytes'] for x in index)}
    (OUT/'SCIENCE_ARCHIVES.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='archives'}))


if __name__=='__main__':
    main()
