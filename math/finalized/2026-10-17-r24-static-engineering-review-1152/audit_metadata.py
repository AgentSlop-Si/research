#!/usr/bin/env python3
"""Review-authored data-only R24 audit. Never imports or runs archive programs."""
import argparse
import hashlib
import json
import random
import statistics
import zipfile
from pathlib import Path

EXPECTED_ARCHIVE_SHA256 = 'c82b7f54f626087d40bc6c066f3529846ee5578ddd27d25cf34a18829f2c570c'

def check(ok, msg):
    if not ok:
        raise ValueError(msg)

def digest(values):
    return hashlib.sha256(b''.join(v.to_bytes(4, 'little') for v in values)).hexdigest()

def audit(archive):
    archive_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
    check(archive_hash == EXPECTED_ARCHIVE_SHA256, 'Unexpected archive version')
    with zipfile.ZipFile(archive) as z:
        check(len(z.namelist()) == len(set(z.namelist())), 'Duplicate archive member')
        manifest = json.loads(z.read('MANIFEST.json'))
        for name, expected_hash in manifest.items():
            check(hashlib.sha256(z.read(name)).hexdigest() == expected_hash, 'Manifest mismatch: '+name)
        b = json.loads(z.read('benchmarks.json'))
        v = json.loads(z.read('validation.json'))
        preserved = json.loads(z.read('input_hashes.json'))['preserved_members']
        for name, expected_hash in preserved.items():
            check(hashlib.sha256(z.read(name)).hexdigest() == expected_hash, 'Preserved-member hash mismatch')
    rows=[]; total=0
    rng=random.Random(b['seed'])
    names=['r23_generic','r23_radix2','inline_radix2','r24_speedrun']
    for r in b['rows']:
        n=r['n'];g=n.bit_length()-1
        check(n == 1<<g, 'Non-power-of-two length')
        check(r['root'] == pow(3,(b['modulus']-1)//n,b['modulus']), 'Root mismatch')
        hashes=[digest([rng.randrange(b['modulus']) for _ in range(n)]) for _ in range(3)]
        check(hashes == r['input_sha256'], 'Seeded input hash mismatch')
        stats_out={}
        for mode in ('prepared','cold'):
            for trial in range(b['samples_per_shape'][mode]):
                order=names.copy();rng.shuffle(order)
            stats_out[mode]={}
            for name,s in r[mode].items():
                a=s['samples_ms'];total+=len(a)
                check(len(a)==b['samples_per_shape'][mode], 'Sample count mismatch')
                q=statistics.quantiles(a,n=4,method='inclusive')
                expected={'median_ms':statistics.median(a),'min_ms':min(a),'max_ms':max(a),'q1_ms':q[0],'q3_ms':q[2]}
                check(all(s[k]==value for k,value in expected.items()), 'Statistics mismatch')
                ratio=s['median_ms']/r[mode]['r24_speedrun']['median_ms']
                check(r[mode+'_ratios'][name]==ratio, 'Ratio mismatch')
                stats_out[mode][name]={'median_ms':s['median_ms'],'ratio_to_r24':ratio}
        m=n*g//2-n+1;a=n*g
        check(r['counts']['r24']=={'multiplications':m,'additions':a}, 'R24 count mismatch')
        check(r['counts']['inline_radix2']==r['counts']['r24'], 'Inline count mismatch')
        check(r['counts']['r23']=={'multiplications':2*n*g,'additions':(5*n//2)*(g//2)+n*(g%2)}, 'R23 count mismatch')
        rows.append({'n':n,'g':g,'author_statistics_recomputed':stats_out})
    check(total==b['checked_timed_calls']==336, 'Total sample mismatch')
    # Independently reconstruct coverage counts from loop bounds, without transforms.
    plans=vectors=basis=entries=compiler_plans=0
    for max_log in (4,5,6,7,7):
        for logn in range(max_log+1):
            n=1<<logn
            stride_count=1 if n==1 else (n//2 if n<=16 else 3)
            count=5+(n if n<=32 else 0)
            plans+=stride_count;vectors+=stride_count*count
            basis+=stride_count*(n if n<=32 else 0);entries+=stride_count*count*n
            compiler_plans+=stride_count*(n<=64)
    expected={'small_plans':plans,'small_vectors':vectors,'basis_vectors_included':basis,
              'entries_small':entries,'exhaustive_vectors':17**2+3**4,'roundtrips':plans,
              'compiler_positive_plans':compiler_plans,'compiler_vector_checks':compiler_plans+8,
              'compiler_rejections':6*8,'input_rejections':2*(6+4),'tracked_arithmetic_checks':2*11}
    check(all(v[k]==value for k,value in expected.items()), 'Validation coverage mismatch')
    check(sum(row['entries'] for row in v['large'])==698368, 'Large entry count mismatch')
    return {'audit_kind':'data-only metadata consistency and independently derived count checks',
            'uploaded_programs_executed':False,'performance_rerun':False,
            'archive_sha256':archive_hash,'verified_manifest_entries':len(manifest),
            'preserved_member_hashes_internally_consistent':len(preserved),
            'original_R23_archive_independently_compared':False,
            'author_timing_samples':total,'seeded_input_hashes_reproduced':len(rows)*3,
            'author_output_hashes_recomputed':False,
            'recorded_validation_coverage_matches_loop_bounds':expected,
            'recorded_large_output_entries':698368,
            'all_timed_log2_sizes_even':all(r['g']%2==0 for r in rows),
            'rows':rows,'status':'PASS: static/data consistency only'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--archive',type=Path,default=Path(__file__).parent/'source/fft_R24_speedrun_2026-10-17.zip')
    ap.add_argument('--output',type=Path,default=Path(__file__).parent/'metadata_audit.json')
    args=ap.parse_args()
    result=audit(args.archive)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])
    print('Manifest entries:',result['verified_manifest_entries'])
    print('Author timing samples:',result['author_timing_samples'])
    print('Seeded input hashes reproduced:',result['seeded_input_hashes_reproduced'])
