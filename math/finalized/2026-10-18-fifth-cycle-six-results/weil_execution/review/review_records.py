"""Independent, data-only review. Never imports or executes package code."""
import ast
import base64
import collections
import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
ACCEPT = (ROOT.parent / 'candidate')
PRE = (ROOT.parent / 'preflight')
checks = collections.Counter()

def check(condition, label):
    checks[label] += 1
    if not condition:
        raise AssertionError(label)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def load(path):
    return json.loads(path.read_text())

source = load(ACCEPT/'SOURCE_BINDINGS.json')
upstream = load(PRE/'sources/SOURCE_BINDINGS_UPSTREAM.json')
zip_path = PRE/'sources/fft_local_ring_weil_v25_signfix.zip'
archive = zip_path.read_bytes()
check(len(archive) == source['archive_bytes'] == 257283, 'archive_length')
check(digest(archive) == source['archive_sha256'] == upstream['corrected_archive']['sha256'], 'archive_sha256')
check(blob(archive) == source['archive_git_blob'] == '70d29013db10fc0707cf5eb65b0e2d71119e6207', 'archive_git_blob')
check(base64.b64decode((PRE/'sources/archive.b64').read_bytes()) == archive, 'base64_archive_identity')
for rec in load(PRE/'PINNED_SOURCES.json'):
    check(blob((PRE/'sources'/rec['file']).read_bytes()) == rec['git_blob'], 'pinned_document_git_blob')

inputs = {r['file']:r for r in load(ACCEPT/'INPUT_HASHES.json')}
members = {r['member'].split('/',1)[1]:r for r in load(PRE/'MEMBER_HASHES.json')}
check(len(inputs) == len(members) == len(upstream['corrected_files']) == 17, 'member_count')
with zipfile.ZipFile(zip_path) as z:
    names = [info.filename for info in z.infolist()]
    check(len(names) == len(set(names)) == 17, 'unique_archive_members')
    check({n.split('/',1)[1] for n in names} == set(inputs) == set(members) == set(upstream['corrected_files']), 'exact_member_domain')
    for info in z.infolist():
        name = info.filename.split('/',1)[1]
        check(not info.filename.startswith('/') and '..' not in Path(info.filename).parts and stat.S_ISREG(info.external_attr >> 16), 'safe_regular_member')
        data = z.read(info)
        expected = inputs[name]
        check(len(data) == expected['bytes'] == members[name]['bytes'] == upstream['corrected_files'][name]['bytes'], 'member_length_bindings')
        check(digest(data) == expected['sha256'] == members[name]['sha256'] == upstream['corrected_files'][name]['sha256'], 'member_hash_bindings')
        check(data == (PRE/'static'/name).read_bytes() == (ACCEPT/'work'/name).read_bytes(), 'archive_static_work_byte_identity')
    check(not {'results.json','independent_results.json','RESULT_SUMMARY.json'} & set(inputs), 'fresh_outputs_not_archive_members')
check(digest((ACCEPT/'work/local_ring_weil.py').read_bytes()) == source['module_sha256'], 'core_binding')
for line in (ACCEPT/'work/MANIFEST.sha256').read_text().splitlines():
    sha,name = line.split('  ',1)
    check(digest((ACCEPT/'work'/name).read_bytes()) == sha, 'package_manifest_entry')
history = [name for name in inputs if name.startswith('historical_outputs/')]
check(len(history) == 5, 'historical_files_preserved')
check(digest((ACCEPT/'work/PRIOR_v24_COMPLETE.zip').read_bytes()) == '3d6bfe84b09b565e7e06ea6c93384d7a3352698cd90475947a01515b94910ce2', 'predecessor_preserved_inert')

for rec in load(ACCEPT/'MANIFEST.json'):
    data = (ACCEPT/rec['file']).read_bytes()
    check(len(data) == rec['bytes'] and digest(data) == rec['sha256'], 'acceptance_manifest_entry')
manifest_names = {r['file'] for r in load(ACCEPT/'MANIFEST.json')}
check(manifest_names == {str(f.relative_to(ACCEPT)) for f in ACCEPT.rglob('*') if f.is_file() and f.name != 'MANIFEST.json'}, 'acceptance_manifest_completeness')

run = load(ACCEPT/'RUN_RECORD.json')
obsrun = load(ACCEPT/'OBSERVATION_RUN_RECORD.json')
check(run['exit_status'] == obsrun['exit_status'] == 0, 'recorded_driver_observation_success')
check(datetime.datetime.fromisoformat(run['started_utc']) < datetime.datetime.fromisoformat(run['finished_utc']) < datetime.datetime.fromisoformat(obsrun['started_utc']), 'recorded_temporal_order')
for record in (run,obsrun):
    cmd = record['command']
    check('--unshare-net' not in cmd and '--unshare-all' not in cmd, 'network_namespace_not_claimed')
    check(all(flag in cmd for flag in ('--unshare-user','--unshare-pid','--unshare-uts','--unshare-ipc','--clearenv','--cpu=120','--as=536870912','--fsize=16777216','--nofile=128','--core=0')), 'recorded_containment_limits')
    mounts = [(cmd[i+1],cmd[i+2]) for i,x in enumerate(cmd[:-2]) if x == '--ro-bind']
    check(('/', '/') in mounts, 'whole_root_readonly_visibility')
    check(all(('/workspace/shared/weil_execution_preflight_20261018_1919/static/'+name,'/tmp/weil-work/'+name) in mounts for name in inputs), 'all_original_members_readonly_mounts')
    check('-O' not in cmd and '-OO' not in cmd and 'PYTHONOPTIMIZE' not in cmd and '-s' in cmd and '-B' in cmd, 'assertions_and_import_flags')

stderr = (ACCEPT/'logs/run_all.stderr.log').read_text()
names = re.findall(r'^(test_\w+) \([^\n]+\) \.\.\. ok$',stderr,re.M)
test_tree = ast.parse((ACCEPT/'work/test_checkpoint.py').read_text())
definitions = {n.name for n in ast.walk(test_tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
check(len(names) == len(set(names)) == 13 and set(names) == definitions, 'exact_13_named_groups')
check('Ran 13 tests in 0.342s' in stderr and stderr.rstrip().endswith('OK'), 'unittest_completion')
stdout = (ACCEPT/'logs/run_all.stdout.log').read_text()
check(stdout.rstrip().endswith('v25 sign-corrected derivative: all requested checks passed'), 'driver_completion')
oracle = load(ACCEPT/'INDEPENDENT_ACCEPTANCE.json')
check(oracle == load(ACCEPT/'logs/independent_acceptance.stdout.log'), 'oracle_output_identity')
check(oracle['verdict'] == 'PASS' and sum(oracle['assertion_counts'].values()) == oracle['actual_assertions'] == 102500, 'oracle_count_sum')
check(digest((ACCEPT/'checks/independent_acceptance.py').read_bytes()) == oracle['oracle_source_sha256'], 'oracle_source_binding')
check(digest((ACCEPT/'checks/observe_q9_candidate.py').read_bytes()) == obsrun['observer_sha256'], 'observer_source_binding')
for filename in ('logs/candidate_q9.stderr.log','logs/independent_acceptance.stderr.log'):
    check((ACCEPT/filename).read_bytes() == b'', 'empty_error_log')

results = load(ACCEPT/'work/results.json')
independent = load(ACCEPT/'work/independent_results.json')
summary = load(ACCEPT/'work/RESULT_SUMMARY.json')
oldsummary = load(ACCEPT/'work/historical_outputs/RESULT_SUMMARY.json')
check(summary['automated_tests'] == 13 and oldsummary['automated_tests'] == 10, 'fresh_historical_summary_separation')
check({**oldsummary,'automated_tests':13} == summary, 'summary_only_expected_change')
for name in ('results.json','independent_results.json'):
    check((ACCEPT/'work'/name).read_bytes() == (ACCEPT/'work/historical_outputs'/name).read_bytes(), 'sign_insensitive_output_equality')
domain = [(p,k,v) for p,k in ((3,2),(3,3),(5,2),(7,2)) for v in range(k+1)]
check(len(results['hierarchy']) == len(independent['support_certificates']) == 13, 'emitted_row_counts')
for (p,k,v),row,support in zip(domain,results['hierarchy'],independent['support_certificates'],strict=True):
    n = p**k
    m = p**(k-v)
    check(row == dict(p=p,k=k,N=n,valuation=v,blocks=p**v,block_length=m,row_support=m,cross_ratio_order=m,radix_p_dense_terms=(k-v)*p*n), 'hierarchy_arithmetic')
    check(support == dict(p=p,k=k,valuation=v,support=m,cross_order=m), 'support_arithmetic')
check(summary['tested_dimensions'] == [9,25,27,49], 'finite_dimensions')

observation = load(ACCEPT/'logs/candidate_q9.stdout.json')
q,ell,zeta = observation['q'],observation['modulus'],observation['root']
check((q,observation['p'],observation['k'],ell,zeta) == (9,3,2,19,4), 'q9_field_parameters')
check(all(ell%d for d in range(2,math.isqrt(ell)+1)) and pow(zeta,9,ell)==1 and pow(zeta,3,ell)!=1, 'prime_exact_root')
check([r['b'] for r in observation['rows']] == list(range(-9,18)), 'observation_scalar_domain')

def direct(b,x,y):
    return sum(pow(zeta,(-b*t*t*5+(y-x)*t)%9,ell) for t in range(9))*pow(9,-1,ell)%ell

canonical = {}
for row in observation['rows']:
    b = row['b']
    for label in ('fourier','gauss','completed'):
        matrix = row[label]
        check(len(matrix)==9 and all(len(r)==9 for r in matrix), 'matrix_shape')
        for x,y in itertools.product(range(9),repeat=2):
            check(matrix[x][y] == direct(b,x,y), 'direct_signed_entry')
    if 0 <= b < 9:
        canonical[b] = row['fourier']

def mm(A,B):
    return [[sum(A[x][t]*B[t][y] for t in range(9))%ell for y in range(9)] for x in range(9)]

def D(a,c):
    return [[pow(zeta,(c*(x-5*a))%9,ell) if y==(x-a)%9 else 0 for y in range(9)] for x in range(9)]

for b,U in canonical.items():
    g = math.gcd(b,9)
    for x,y in itertools.product(range(9),repeat=2):
        check((U[x][y]!=0) == ((y-x)%g==0), 'q9_support')
    if b:
        ratio=U[0][0]*U[g][g]*pow(U[0][g]*U[g][0]%ell,-1,ell)%ell
        check(ratio == pow(zeta,-g*pow(b//g,-1,9//g),ell), 'q9_signed_ratio')
        check(next(k for k in range(1,19) if pow(ratio,k,ell)==1) == 9//g, 'q9_residual_order')
        check(U != [[direct(-b,x,y) for y in range(9)] for x in range(9)], 'positive_chirp_rejected')
    else:
        check(U == [[int(x==y) for y in range(9)] for x in range(9)], 'q9_identity')
    for a,c in itertools.product(range(9),repeat=2):
        left,right = mm(U,D(a,c)),mm(D((a+b*c)%9,c),U)
        for x,y in itertools.product(range(9),repeat=2):
            check(left[x][y] == right[x][y], 'q9_covariance_direct_matrix')
for b,c in itertools.product(range(9),repeat=2):
    product=mm(canonical[b],canonical[c])
    for x,y in itertools.product(range(9),repeat=2):
        check(product[x][y] == canonical[(b+c)%9][x][y], 'q9_additive_direct_matrix')
changed = [row[:] for row in canonical[1]]
changed[0][0]=(changed[0][0]+1)%19
check(changed[0][0] != direct(1,0,0), 'mutation_changed_entry')
check(canonical[1] != canonical[2], 'mutation_wrong_dispatch')
check(oldsummary['automated_tests'] != len(names), 'mutation_stale_summary')

def vp(b,p):
    if not b:
        return 2
    return 1 if b%p==0 else 0

def mult(x,y):
    a,b,c,d=x
    e,f,g,h=y
    return ((a*e+b*g)%9,(a*f+b*h)%9,(c*e+d*g)%9,(c*f+d*h)%9)

groups={}
censuses={}
for n,p in ((9,3),(25,5)):
    G={t for t in itertools.product(range(n),repeat=4) if (t[0]*t[3]-t[1]*t[2])%n==1}
    census=dict(collections.Counter(vp(t[1],p) for t in G))
    check(census == ({0:486,1:108,2:54} if n==9 else {0:12500,1:2000,2:500}), 'sl2_independent_census')
    check(len(G) == (648 if n==9 else 15000), 'sl2_independent_size')
    groups[n],censuses[n]=G,census
G=groups[9]
for level,size in ((1,162),(2,54)):
    H={s for s in G if s[1]%(3**level)==0}
    check(len(H)==size, 'subgroup_size')
    for a,b,c,d in H:
        check((d,-b%9,-c%9,a) in H, 'subgroup_inverse')
    for x,y in itertools.product(H,repeat=2):
        check(mult(x,y) in H, 'subgroup_closure')
B={t for t in G if t[1]==0}
unseen=set(G)
cosets=[]
while unseen:
    rep=min(unseen)
    orbit={mult(mult(x,rep),y) for x,y in itertools.product(B,repeat=2)}
    check(orbit<=unseen, 'double_coset_disjointness')
    unseen-=orbit
    cosets.append({'valuation':vp(rep[1],3),'size':len(orbit)})
cosets.sort(key=lambda d:(d['valuation'],d['size']))
check(cosets == results['z9_borel_double_cosets'] == oracle['independent_double_cosets'], 'double_cosets_emitted_comparison')
check(results['sl2_z9_size']==648 and results['sl2_z9_valuation_counts']=={'0':486,'1':108,'2':54}, 'sl2_emitted_comparison')
check(independent['sl2_q9']=={'group_size':648,'valuation_counts':{'0':486,'1':108,'2':54},'easy_subgroup_size':162}, 'supplied_verifier_emitted_comparison')

# Audit the oracle's entire counted category map. Reviewer checks remain separate.
expected_counts={
 'actual_named_test_groups':1,'actual_test_group_count':1,'driver_exit':1,'driver_terminal_status':1,
 'emitted_double_cosets':1,'emitted_independent_group_record':1,'emitted_sl2_counts':1,'emitted_sl2_size':1,
 'fresh_hierarchy_count':1,'fresh_hierarchy_row':13,'fresh_independent_support_row':13,
 'fresh_summary_consistency':3,'fresh_summary_dimensions':1,'fresh_summary_support_count':1,'fresh_summary_test_count':1,'fresh_support_count':1,
 'historical_file_count':1,'historical_preservation':5,'independent_coefficient_prime':1,
 'independent_double_coset_disjointness':4,'independent_double_coset_sizes':1,
 'independent_q9_additive_entry':9**4,'independent_q9_covariance_entry':9**5,'independent_q9_entry':27*3*81,
 'independent_q9_identity':1,'independent_q9_ratio_order':8,'independent_q9_signed_ratio':8,'independent_q9_support':9**3,
 'independent_root_exact_order':1,'independent_sl2_census':2,'independent_sl2_size':2,
 'independent_subgroup_closure':162**2+54**2,'independent_subgroup_inverse':162+54,'independent_subgroup_size':2,
 'observation_exit':1,'observed_matrix_shape':27*3,'observed_parameter_dispatch':1,'observed_scalar_domain':1,
 'one_entry_mutation_rejected':1,'package_manifest':16,'scalar_dispatch_mutation_rejected':1,
 'source_member_byte_length':17,'source_member_hash':17,'stale_summary_mutation_rejected':1,'unittest_terminal_status':1,'wrong_positive_chirp_rejected':8,
}
check(oracle['assertion_counts']==expected_counts and sum(expected_counts.values())==102500, 'oracle_full_count_map')
tree=ast.parse((ACCEPT/'checks/independent_acceptance.py').read_text())
imports=[]
for node in ast.walk(tree):
    if isinstance(node,ast.Import):
        imports.extend(a.name for a in node.names)
    if isinstance(node,ast.ImportFrom):
        imports.append(node.module)
check(set(imports)=={'ast','collections','copy','hashlib','itertools','json','math','pathlib','re'}, 'oracle_only_standard_library_imports')

bindings=[]
for label,base in (('acceptance',ACCEPT),('preflight',PRE)):
    for path in sorted(base.rglob('*')):
        if path.is_file():
            data=path.read_bytes()
            bindings.append({'tree':label,'file':str(path.relative_to(base)),'bytes':len(data),'sha256':digest(data)})
report={
 'review_verdict':'PASS: exact corrected finite acceptance corroborated; bounded caveats retained',
 'review_method':'Read-only source/log/JSON review plus this newly authored checker; no candidate/package execution or import.',
 'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checker_sha256':digest(Path(__file__).read_bytes()),
 'reviewed_acceptance_report_sha256':digest((ACCEPT/'REPORT.md').read_bytes()),
 'archive_sha256':digest(archive),'archive_git_blob':blob(archive),
 'exact_named_groups':names,
 'accepted_oracle_count':102500,
 'reviewer_checks_separate_from_acceptance':dict(sorted(checks.items())),
 'reviewer_check_count':sum(checks.values()),
 'q9_signed_entries_independently_recomputed':checks['direct_signed_entry'],
 'q9_covariance_entries_independently_recomputed':checks['q9_covariance_direct_matrix'],
 'q9_additive_entries_independently_recomputed':checks['q9_additive_direct_matrix'],
 'sl2_censuses':censuses,'lower_borel_double_cosets':cosets,
 'historical_preservation':{'archive_members':17,'historical_outputs_files':5,'nested_predecessor_sha256':inputs['PRIOR_v24_COMPLETE.zip']['sha256']},
 'limitations':[
  'The record review is not a second execution of the downloaded package and is not an attestation independent of recorded logs.',
  'Git blob identities are locally recomputed from pinned snapshots; no fresh remote GitHub fetch is part of this review.',
  'The launcher mounts the whole existing root read-only. This restricts writes, not reads or credential-file visibility.',
  'No independent network namespace is established. Existing environment network restrictions are inherited.',
  'CPU/address-space limits are per process; no process-count or aggregate resource bound is recorded.',
  'The acceptance oracle has output/error logs and source binding, but no dedicated timestamped exit record. Its result is independently corroborated here.',
  'Recorded source/checker hashes and logs are evidence snapshots, not cryptographic execution attestations.',
  'Original historical source replay and unrecovered earlier API/review bytes remain open; no historical or global implementation coverage is inferred.',
 ],
 'source_bindings':bindings,
}
(ROOT/'REVIEW_MANIFEST.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='source_bindings'},indent=2,sort_keys=True))
