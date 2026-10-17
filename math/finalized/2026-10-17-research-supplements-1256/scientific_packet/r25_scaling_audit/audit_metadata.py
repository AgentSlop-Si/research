"""Reviewer-written data-only R25 audit. Never imports/evaluates uploaded code.

Usage: python audit_metadata.py [--r24-source PATH]
All independent structural checks below manipulate formal root exponents or
integer formulas; they do not run the submitted generator or benchmark.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'source' / 'fft_R25_growing_blocks_2026-10-17.zip'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def expected_ledger(n, qmax, policy):
    g = n.bit_length() - 1
    m = n*g//2 - n + 1
    c = (g+qmax-1)//qmax
    return dict(multiplications=m, additions=n*g,
                reductions=n*(c+1)+(m if policy == 'products' else 0),
                vector_reads=n*(c+1), vector_writes=n*(c+1), blocks=c)

def expected_storage(n, qmax):
    left=n.bit_length()-1; h=1; tw=0; groups=0; biggest=1
    while left:
        q=min(left,qmax); b=2**q
        tw+=(b-1)*(h-1)+b//2-1
        h*=b; left-=q; groups+=1; biggest=max(biggest,b)
    return dict(bit_permutation_entries=n, twiddle_residues=tw,
                group_descriptors=groups, max_kernel_coordinates=biggest,
                working_vector_entries=n)

def check_storage(record, n, qmax):
    for k,v in expected_storage(n,qmax).items():
        require(record[k]==v, 'storage '+str((n,qmax,k)))
    require(record['source_characters']>=0, 'source length nonnegative')

def check_stats(record):
    values=record['samples_ms']
    require(all(math.isfinite(x) and x>0 for x in values), 'positive samples')
    expected={'median_ms':statistics.median(values)}
    if 'min_ms' in record:
        quart=statistics.quantiles(values,n=4,method='inclusive')
        expected.update(min_ms=min(values),max_ms=max(values),q1_ms=quart[0],q3_ms=quart[2])
    for k,v in expected.items():
        require(record[k]==v, 'statistic '+k)
    return len(values)

def structural_checks():
    # A butterfly coefficient is a root exponent modulo N. Minus signs add N/2.
    # Supports are disjoint, so this exact formal computation needs no numeric DFT.
    maps=coefficients=0
    for q in range(1,9):
        b=2**q
        for h in (1,2,4,8):
            n=b*h
            for j in range(min(h,3)):
                rows=[{i:0} for i in range(b)]
                for t in range(1,q+1):
                    width=2**t; half=width//2
                    for start in range(0,b,width):
                        for a in range(half):
                            lo=start+a; hi=lo+half
                            exponent=(j+a*h)*(n//(h*width))
                            l=rows[lo]; r=rows[hi]
                            require(not (l.keys() & r.keys()),'disjoint butterfly supports')
                            rows[lo]={**l,**{k:(e+exponent)%n for k,e in r.items()}}
                            rows[hi]={**l,**{k:(e+exponent+n//2)%n for k,e in r.items()}}
                for k,row in enumerate(rows):
                    for l,e in row.items():
                        reverse=int(format(l,f'0{q}b')[::-1],2)
                        expected=(reverse*j + k*reverse*h)%n
                        require(e==expected,'formal regrouping coefficient')
                        coefficients+=1
                maps+=1
    partitions=0
    # Includes every composition of g through g=12, not only uniform blocks.
    for g in range(13):
        n=2**g
        for cuts in range(2**max(0,g-1)):
            parts=[]; last=0
            for level in range(1,g):
                if cuts & (1<<(level-1)):
                    parts.append(level-last);last=level
            if g:parts.append(g-last)
            h=1; m=a=0
            for q in parts:
                b=2**q
                local_m=sum((b//(2**t))*(2**(t-1)-1) for t in range(1,q+1))
                local_a=sum(b for _ in range(q))
                m+=(n//b)*local_m+(n//b-n//(b*h))*(b-1)
                a+=(n//b)*local_a;h*=b
            require((m,a)==(n*g//2-n+1,n*g),'telescoping partition count')
            partitions+=1
    return dict(formal_group_maps_checked=maps,formal_coefficients_checked=coefficients,
                arbitrary_partitions_checked=partitions,
                scope='Independent formal-exponent and count sanity checks, not execution of submitted kernels or a formal proof assistant.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--r24-source',type=Path);args=ap.parse_args()
    raw=ARCHIVE.read_bytes()
    with zipfile.ZipFile(ARCHIVE) as z:
        names=z.namelist();require(len(names)==len(set(names)),'unique members')
        require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'safe member paths')
        data={n:z.read(n) for n in names}
    read=lambda n:json.loads(data[n])
    manifest=read('MANIFEST.json')
    require(set(manifest)==set(names)-{'MANIFEST.json'},'complete manifest')
    for name,digest in manifest.items():require(sha(data[name])==digest,'payload hash '+name)
    base=read('baseline_input.json'); verified_old=0
    for name,digest in base['members'].items():
        require(sha(data['baseline_r24/'+name])==digest,'baseline digest '+name)
        if args.r24_source:
            require((args.r24_source/name).read_bytes()==data['baseline_r24/'+name],'prior R24 match '+name)
            verified_old+=1
    bundle=read('benchmarks.json'); sample_count=0; traces=0; stats_count=0; main=[]
    for run in bundle['main_runs']:
        r=run['result'];n=r['N'];g=r['log2N'];p=r['p'];require(n==2**g,'N/log')
        require(run==read(f'benchmark_{n}.json'),'aggregate main copy')
        require(r['root']==pow(3,(p-1)//n,p),'benchmark root')
        require(pow(r['root'],n,p)==1 and pow(r['root'],n//2,p)==p-1,'root exact order')
        variants=list(r['variants']);total=0
        for name,modes in r['variants'].items():
            for mode,record in modes.items():
                count=check_stats(record);total+=count;stats_count+=1
                require(count==r['warm_trials' if mode=='prepared' else 'cold_trials'],'sample repetitions')
        require(total==r['checked_timing_calls']==72,'main call count');sample_count+=total
        rng=random.Random(250300+g)
        # Regenerate only RNG draws to verify serialized randomized run order.
        for _ in range(3*n):rng.randrange(p)
        expected_trace=[]
        for mode,reps in [('prepared',r['warm_trials']),('cold',r['cold_trials'])]:
            for trial in range(reps):
                order=variants.copy();rng.shuffle(order)
                expected_trace.append(dict(mode=mode,trial=trial,input_index=trial%3,order=order))
        require(r['order_trace']==expected_trace,'seeded chronological order');traces+=len(expected_trace)
        for name,ledger in r['ledgers'].items():
            policy,q=name.split('_');q=int(q)
            require(ledger==expected_ledger(n,q,policy),'main ledger')
            check_storage(r['plan_storage'][name],n,q)
        ratios={}
        for name in ('boundary_4','boundary_6','boundary_8','products_4'):
            ratios[name]={mode:r['variants']['R24'][mode]['median_ms']/r['variants'][name][mode]['median_ms'] for mode in ('prepared','cold')}
        main.append(dict(N=n,medians_ms={k:{m:v['median_ms'] for m,v in z.items()} for k,z in r['variants'].items()},r24_over_candidate=ratios))
    confirmation=read('confirmation.json');require(bundle['confirmation']==confirmation,'aggregate confirmation copy')
    conf_count=0
    for modes in confirmation['variants'].values():
        for record in modes.values():conf_count+=check_stats(record);stats_count+=1
    require(conf_count==confirmation['checked_calls']==36,'confirmation count')
    sample_count+=conf_count;require(sample_count==bundle['completed_checked_timing_calls']==324,'all counted calls')
    sup=read('evidence/confirmation_superseded.json');sup_count=0
    for modes in sup['variants'].values():
        for record in modes.values():sup_count+=check_stats(record)
    small=read('validation_small.json');large=read('validation_large.json');width=read('large_width_audit.json');validation=read('validation.json')
    require(validation['small']==small and validation['large']==large and validation['large_width_audit']==width,'validation aggregate copies')
    expected=dict(plans=0,vector_comparisons=0,basis_included=0,operation_instrumentations=0,roundtrips=0,distinct_input_root_cases=0)
    for p in (17,97,193,257):
        for g in range(8):
            n=2**g
            if (p-1)%n:continue
            roots=1 if n<=2 else 2;basis=n if n<=16 else 4;plans=2*min(6,max(g,1));vectors=7+basis
            expected['plans']+=roots*plans;expected['operation_instrumentations']+=roots*plans
            expected['vector_comparisons']+=roots*plans*vectors;expected['basis_included']+=roots*plans*basis
            expected['roundtrips']+=roots*plans;expected['distinct_input_root_cases']+=roots*vectors
    expected['plans']+=42;expected['operation_instrumentations']+=42;expected['vector_comparisons']+=42
    expected['invalid_rejections']=13
    for k,v in expected.items():require(small[k]==v,'small coverage '+k)
    require(len(small['width_records'])==42,'small width record count')
    for row in small['width_records']+width:
        n=row['N'];q=row['used_bits'];policy=row['policy'];g=n.bit_length()-1
        require(row['ledger']==expected_ledger(n,q,policy),'width ledger')
        check_storage(row['storage'],n,q)
        used=min(q,g);ell=998244353 .bit_length()
        ceiling=(2*ell+used) if policy=='products' else (used+1)*ell+used
        require(row['proved_bit_ceiling']==ceiling and row['measured_peak_bits']<=ceiling,'recorded width ceiling')
    require(large['unique_vectors']==len(large['rows'])==10,'large distinct vectors')
    require(large['full_vector_comparisons']==sum(r['candidate_plans'] for r in large['rows'])==40,'large comparisons')
    require(large['output_entries_checked']==sum(r['N']*r['candidate_plans'] for r in large['rows'])==3489792,'large entries')
    require([(r['N'],r['input_kind']) for r in large['rows']]==[(2**g,kind) for g in (11,13,15,17,18) for kind in ('full_random','alternating')],'large sizes/kinds')
    receipt_path=ROOT/'source'/'fft_R25_clean_replay_2026-10-17.json';receipt=json.loads(receipt_path.read_bytes())
    require(receipt['archive_sha256']==sha(raw),'replay archive digest')
    require(receipt['sealed_payload_files']==len(manifest)==46,'replay payload count')
    require([r['args'] for r in receipt['commands']]==[['verify_manifest.py'],['validate.py','--suite','small'],['validate.py','--suite','large']],'replay scope')
    require(all(r['returncode']==0 for r in receipt['commands']),'recorded replay return codes')
    summary=dict(status='PASS_DATA_AND_STATIC_AUDIT',archive_sha256=sha(raw),sealed_payload_files=len(manifest),
        preserved_r24_members=len(base['members']),independently_compared_prior_r24_members=verified_old,
        main_calls=sample_count-conf_count,confirmation_calls=conf_count,total_counted_calls=sample_count,
        distributions_recomputed=stats_count,main_order_trace_records_checked=traces,
        superseded_calls_checked_but_excluded=sup_count,main_environment=bundle['main_runs'][0]['environment'],
        main_results=main,small_coverage=expected,stored_width_records_checked=len(small['width_records'])+len(width),
        large_coverage={k:large[k] for k in ('full_vector_comparisons','output_entries_checked','unique_vectors')},
        structural_sanity=structural_checks(),author_replay_scope=receipt['scope'],
        independent_execution='Only this reviewer-written data/formula audit. No submitted module imported or executed; no timing or full transform replay.',
        not_independently_reproduced=['transform output hashes','measured integer peak widths','benchmark timings','generated source character counts'])
    (ROOT/'metadata_audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('main_results','main_environment')},indent=2))

if __name__=='__main__':main()
