"""Independent, bounded review controls. No candidate code is imported.

Only JSON/report artifacts are read. No elimination is performed.
"""
import collections
import hashlib
import itertools
import json
import math
import pathlib
import signal
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = (HERE.parent / 'candidate')
EXPECTED_REPORT = '684f31a2b2d8e66204ae3c69dc8c819d291ced773dedd7ffdfcb30c5366d0ae6'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name):
    return json.loads((SOURCE/name).read_text())

def check_manifest():
    manifest = load('MANIFEST.json')
    assert digest(SOURCE/'REPORT.md') == EXPECTED_REPORT
    assert len({row['path'] for row in manifest['files']}) == len(manifest['files'])
    for row in manifest['files']:
        p = SOURCE/row['path']
        assert p.stat().st_size == row['bytes']
        assert digest(p) == row['sha256']
    for row in load('SOURCE_BINDINGS.json'):
        p = (SOURCE / row['public_source_path'])
        assert p.stat().st_size == row['bytes']
        assert digest(p) == row['sha256']
    return {'candidate_files':len(manifest['files']), 'source_bindings':3,
            'report_sha256':EXPECTED_REPORT}

def quadruples(total):
    for a in range(total+1):
        for b in range(total-a+1):
            for c in range(total-a-b+1):
                yield (a,b,c,total-a-b-c)

def patterns(r):
    # Split into odd and even stride totals before enumerating.
    for odd in range(8,r+1):
        for o in quadruples(odd):
            for e in quadruples(r-odd):
                yield tuple(z for pair in zip(o,e) for z in pair)

def transform(n,k):
    out=[0]*8
    for s in range(1,9):
        residue=(s*pow(3,k,16))%16
        out[min(residue,16-residue)-1]+=n[s-1]
    return tuple(out)

def orbit(n):
    return frozenset(transform(n,k) for k in range(4))

def check_coverage():
    stored=load('ALL_LENGTHS_INDEX.json')['layers']
    assert [row['length'] for row in stored] == list(range(8,15))
    results={}; pure=0; total_patterns=total_orbits=0
    all_sets={}
    for row in stored:
        r=row['length']; full=set(patterns(r)); all_sets[r]=full
        count_formula=sum(math.comb(o+3,3)*math.comb(r-o+3,3) for o in range(8,r+1))
        assert len(full)==count_formula==row['patterns']
        reps={min(orbit(n)) for n in full}
        assert len(row['representatives'])==len(reps)==row['orbits']
        assert set(map(tuple,row['representatives']))==reps
        fixed=[sum(transform(n,k)==n for n in full) for k in range(4)]
        assert sum(fixed)//4 == len(reps) and sum(fixed)%4==0
        expected_pure={n for n in reps if sum(v>0 for v in n)==1}
        assert set(map(tuple,row['excluded_pure_odd_representatives']))==expected_pure
        assert len(expected_pure)==1
        pure+=1;total_patterns+=len(full);total_orbits+=len(reps)
        results[str(r)]={'patterns':len(full),'orbits':len(reps),'Burnside_fixed':fixed}
    padded=load('RESIDUAL_INDEX.json')
    assert len(padded['systems'])==12922==padded['representatives']
    assert padded['total_literal_patterns']==total_patterns==105435
    assert padded['patterns_before_symmetry']==50940
    assert {int(r):c for r,c in padded['counts_by_literal_length'].items()}=={r:len(full) for r,full in all_sets.items()}
    union=set(); statuses=collections.Counter()
    for row in padded['systems']:
        n=tuple(row['representative']); members=list(map(tuple,row['orbit']))
        expected=orbit(n)
        assert min(expected)==n and len(members)==len(set(members))
        assert set(members)==expected and not union.intersection(expected)
        union.update(expected)
        status='EXCLUDED_PURE_ODD_STRIDE' if sum(v>0 for v in n)==1 else 'RESIDUAL_UNSOLVED'
        assert row['status']==status
        statuses[status]+=1
    assert union==all_sets[14]
    for r,full in all_sets.items():
        assert all((n[0]+14-r,)+n[1:] in union for n in full)
    assert total_orbits==26783 and pure==7
    assert statuses=={'RESIDUAL_UNSOLVED':12921,'EXCLUDED_PURE_ODD_STRIDE':1}
    return {'per_length':results,'all_literal_patterns':total_patterns,
            'all_orbits':total_orbits,'all_unresolved_orbits':total_orbits-pure,
            'padded_orbits':12922,'padded_unresolved':12921,
            'padding_checked_patterns':total_patterns}

# Cyclotomic elements are sparse exponent dictionaries with a^16=-1.
def reduce_a(p):
    out=collections.Counter()
    for e,c in p.items():
        q,r=divmod(e,16);out[r]+=(-1 if q%2 else 1)*c
    return {e:c for e,c in out.items() if c}

def apow(e): return reduce_a({e:1})
def add(*ps):
    out=collections.Counter()
    for p in ps:
        for e,c in p.items():out[e]+=c
    return {e:c for e,c in out.items() if c}
def mul(a,b):
    out=collections.Counter()
    for i,x in a.items():
        for j,y in b.items():out[i+j]+=x*y
    return reduce_a(out)

def matrix_product(a,b):
    return [[add(*(mul(a[i][k],b[k][j]) for k in range(16)))
             for j in range(16)] for i in range(16)]

def check_target():
    q=[apow(t*t) for t in range(16)]
    c=[[apow(-(i-j)**2) for j in range(16)] for i in range(16)]
    qm=[[q[(i-j)%16] for j in range(16)] for i in range(16)]
    expected=[[({0:16} if i==j else {}) for j in range(16)] for i in range(16)]
    assert matrix_product(c,qm)==expected
    assert matrix_product(qm,c)==expected
    for r,t in itertools.product(range(16),repeat=2):
        assert q[(t-r)%16]==mul(apow(r*r-2*r*t),q[t])
    for t in range(16):
        assert apow(9*((11*t)%16)**2)==q[t]
    bad_q=[dict(v) for v in q];bad_q[5]=add(bad_q[5],{0:1})
    bad_qm=[[bad_q[(i-j)%16] for j in range(16)] for i in range(16)]
    wrong=matrix_product(c,bad_qm)
    assert wrong!=expected
    rejected=sum(wrong[i][j]!=expected[i][j] for i in range(16) for j in range(16))
    return {'left_inverse_entries':256,'right_inverse_entries':256,
            'shift_coefficients':256,'Galois_symmetry_coefficients':16,
            'mutated_target_mismatching_entries':rejected}

def cyclic_mul(a,b):
    out=[0]*16
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[(i+j)%16]+=x*y
    return out

def evaluate(rows,values):
    return [sum(c*math.prod(v**e for v,e in zip(values,exp)) for exp,c in row) for row in rows]

def check_benchmark():
    spec=load('BENCHMARK_SYSTEM.json'); n=tuple(spec['counts'])
    assert n==(2,2,2,2,2,1,2,1) and sum(n)==14
    assert spec['field']=={'symbol':'a','minimal_polynomial':'a^16+1','characteristic':0}
    assert spec['strides']==list(range(1,9))
    assert spec['variables']==[f'b{s}_{j}' for s,size in enumerate(n,1) for j in range(1,size+1)]+['u']
    assert spec['equations']==[{'i':i,'form':'c_i - a^(i*i mod 32) c_0'} for i in range(1,16)]+[{'form':'u*c_0 - 1'}]
    # Bit masks give a separately implemented squarefree monomial basis.
    polys={(0,0):1};offset=0
    for s,size in enumerate(n,1):
        new=collections.Counter()
        for (res,mask),coef in polys.items():
            new[(res,mask)]+=coef
            for j in range(1,size+1):new[((res+s*j)%16,mask|(1<<(offset+j-1)))]+=coef
        polys=dict(new);offset+=size
    stored={}
    for i,row in enumerate(spec['cyclic_coefficients']):
        for exp,c in row:
            assert len(exp)==14 and set(exp)<={0,1}
            key=(i,sum(p<<j for j,p in enumerate(exp)))
            assert key not in stored
            stored[key]=c
    assert stored==polys and len(polys)==2916
    equation_terms=0; max_degree=0
    for i in range(1,16):
        equation_terms+=len(spec['cyclic_coefficients'][i])+len(spec['cyclic_coefficients'][0])
        for row in (spec['cyclic_coefficients'][i],spec['cyclic_coefficients'][0]):
            max_degree=max(max_degree,max(sum(exp) for exp,c in row))
    equation_terms+=len(spec['cyclic_coefficients'][0])+1
    max_degree=max(max_degree,1+max(sum(exp) for exp,c in spec['cyclic_coefficients'][0]))
    assert equation_terms==5692 and max_degree==9
    # Repeated roots, zero parameters, lost leading coefficients and internal zeros.
    alpha_groups=[[2,2],[0,2],[2,-2],[0,0],[3,3],[0],[2,-2],[2]]
    values=[];expected=[1]+[0]*15
    for s,alphas in enumerate(alpha_groups,1):
        g=[1]
        for a in alphas:
            nxt=[0]*(len(g)+1)
            for j,v in enumerate(g):nxt[j]+=v;nxt[j+1]-=a*v
            g=nxt
            f=[0]*16;f[0]=1;f[s]=-a
            expected=cyclic_mul(expected,f)
        values.extend(g[1:])
    assert evaluate(spec['cyclic_coefficients'],values)==expected
    # A genuine benchmark zero-product solution of I is rejected by J.
    bad=[0]*14;names=spec['variables'][:-1]
    bad[names.index('b4_2')]=-1;bad[names.index('b8_1')]=1
    assert evaluate(spec['cyclic_coefficients'],bad)==[0]*16
    assert all(u*0-1!=0 for u in (-10,0,1,11))
    altered=dict(stored);key=next(iter(altered));altered[key]+=1
    assert altered!=polys
    return {'symbolic_terms':len(polys),'variables':15,'equations':16,
            'equation_terms':equation_terms,'max_degree':max_degree,
            'degenerate_factorization_coefficients':16,
            'zero_product_rejected':True,'symbolic_mutation_rejected':True}

def check_guards():
    y=sp.symbols('y');cases=0;singular=0
    examples=[[],[0],[2],[2,2],[2,-2],[0,2],[1],[-1],[0,0,2]]
    for s in range(1,9):
        d=math.gcd(16,s);m=16//d
        for alphas in examples:
            g=sp.Poly(sp.prod(1-a*y for a in alphas),y)
            resultant=int(sp.resultant(y**m-1,g.as_expr(),y))
            guards=math.prod(1-a**m for a in alphas)
            assert resultant==guards
            coefficients=[0]*16
            for (j,),value in g.terms():coefficients[(s*j)%16]+=int(value)
            matrix=sp.Matrix(16,16,lambda i,j:coefficients[(i-j)%16])
            assert int(matrix.det())==resultant**d
            assert (resultant!=0)==all(a**m!=1 for a in alphas)
            cases+=1;singular+=resultant==0
    # Full mixed-product determinant identity with degenerate coefficient choices.
    alphas_by_stride=[[2,2],[0,2],[2,-2],[0,0],[3,3],[0],[2,-2],[2]]
    p=[1]+[0]*15;rhs=1
    for s,alphas in enumerate(alphas_by_stride,1):
        d=math.gcd(16,s);m=16//d
        rhs*=math.prod(1-a**m for a in alphas)**d
        for a in alphas:
            f=[0]*16;f[0]=1;f[s]=-a;p=cyclic_mul(p,f)
    determinant=int(sp.Matrix(16,16,lambda i,j:p[(i-j)%16]).det())
    assert determinant==rhs!=0
    return {'individual_group_examples':cases,'singular_guard_examples':singular,
            'mixed_determinant_identity':True}

def check_pure():
    certs=load('PURE_STRIDE_CERTIFICATES.json')
    assert len(certs)==28
    assert {(c['length'],c['stride']) for c in certs}==set(itertools.product(range(8,15),(1,3,5,7)))
    for c in certs:
        r,s=c['length'],c['stride'];i=(15*s)%16
        support={(j*s)%16 for j in range(r+1)}
        assert 0 not in {(j*s)%16 for j in range(1,r+1)} and i not in support
        assert c['equation_index']==i
        assert c['coefficient_claim']=={'c_0':1,'c_i':0}
        assert c['multiplier']=={'sign':-1,'a_exponent_mod_32':(-i*i)%32}
        assert mul({e:-v for e,v in apow(-i*i).items()}, {e:-v for e,v in apow(i*i).items()})=={0:1}
    return {'literal_certificates':28,'orbits_across_layers':7,'padded_orbits':1}

def check_resource():
    result=load('RESOURCE_RESULT.json');status=load('ELIMINATION_STATUS.json')
    start=json.loads((SOURCE/'ELIMINATION.log').read_text())
    assert result['returncode']==-int(signal.SIGXCPU)==-24
    assert not result['wall_timeout'] and result['wall_seconds']<210
    assert result['child_max_rss_kib']*1024<2*1024**3
    assert status['status']=='RESOURCE_LIMIT_CPU_NO_BASIS' and start['status']=='RUNNING'
    assert not (SOURCE/'ELIMINATION_BASIS.txt').exists()
    for key in ('counts','field','variables','equations','input_terms','maximum_total_degree','order','method','cpu_limit_seconds','address_space_limit_bytes','sympy_version','setup_seconds'):
        assert status[key]==start[key]
    return {'archived_returncode':result['returncode'],'signal':'SIGXCPU',
            'archived_wall_seconds':result['wall_seconds'],
            'archived_child_cpu_seconds':result['child_cpu_seconds'],
            'archived_peak_RSS_KiB':result['child_max_rss_kib'],
            'elimination_replayed':False,'no_basis_artifact':True,
            'measurement_scope':'Archived telemetry and inspected source; not a new runtime measurement.'}

if __name__=='__main__':
    results={}
    for name,fn in [('frozen_input',check_manifest),('coverage',check_coverage),
                    ('target',check_target),('benchmark',check_benchmark),
                    ('guards',check_guards),('pure_certificates',check_pure),
                    ('resource',check_resource)]:
        results[name]=fn()
        print(name+': PASS',flush=True)
    results['verdict']='PASS_FORMULATION_COVERAGE_AND_RESOURCE_BLOCKER_ONLY'
    results['minimum_interval_unchanged']=[8,15]
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
