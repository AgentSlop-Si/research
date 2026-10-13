"""Fresh reviewer controls only. Never imports or executes reviewed scientific code."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
from itertools import product
from collections import Counter
from fractions import Fraction
import json

BASE = Path('/workspace/scratch/928904ebc9b0')
ROOT = BASE/'q16_next_gate_1651'
OUT = BASE/'q16_materialization_review_1659'
COUNTS = Counter()

def check(x, name):
    if not x:
        raise AssertionError(name)
    COUNTS[name] += 1

def digest(b):
    return sha256(b).hexdigest()

archive = BASE/'Q16_Exact_Input_Interface_Gap_Ledger_2026-10-13.zip'
check(digest(archive.read_bytes()) == '1248773169d32ed606b2750843d6cf9992840dde2eb86ca974ed8637003d330e','archive_hash')
check(archive.stat().st_size == 120127,'archive_size')
with ZipFile(archive) as z:
    check(z.testzip() is None,'archive_crc')
    names = z.namelist()
    check(len(names)==len(set(names))==25,'archive_inventory')
    prefix='q16_next_gate_1651/'
    manifest=json.loads(z.read(prefix+'MANIFEST.json'))
    check(set(names)=={prefix+p for p in manifest}|{prefix+'MANIFEST.json'},'manifest_inventory')
    check(digest(z.read(prefix+'MANIFEST.json'))=='c695a4202d61ed76ec8f64ab1c486a42292492a89f279e86ef9b5b36b6c9bb4d','manifest_hash')
    for p,spec in manifest.items():
        data=z.read(prefix+p)
        check(digest(data)==spec['sha256'] and len(data)==spec['bytes'],'manifest_payload')
        check(data==(ROOT/p).read_bytes(),'local_equals_frozen')
    evidence=json.loads(z.read(prefix+'EVIDENCE.json'))
    for p,spec in evidence['files'].items():
        data=z.read(prefix+spec['frozen_copy'])
        check(digest(data)==spec['sha256'] and len(data)==spec['bytes'],'source_binding')
        check(data==(BASE/p).read_bytes(),'source_equals_frozen')

for p,spec in evidence['archives'].items():
    data=(BASE/p).read_bytes()
    check(digest(data)==spec['sha256'] and len(data)==spec['bytes'],'inherited_archive_hash')
with ZipFile(BASE/'q16_success_independent_1633/evidence/Q16_Sparse_Success_Contract_Bridge_Audit_2026-10-13.zip') as z:
    for file,copy in [('RECOVERED_EDITION.md','03_RECOVERED_EDITION.md.txt'),('buckets.py','06_buckets.py.txt'),('pipeline.py','07_pipeline.py.txt'),('fair_tape.py','08_fair_tape.py.txt')]:
        check(z.read('q16_success_bridge_audit_20261013/sources/'+file)==(ROOT/'evidence'/copy).read_bytes(),'frozen_bridge_byte_identity')
with ZipFile(BASE/'Q16_Sparse_Success_Contract_Bridge_Independent_Acceptance_2026-10-13.zip') as z:
    check(z.read('q16_success_independent_1633/INDEPENDENT_REVIEW.md')==(ROOT/'evidence/01_INDEPENDENT_REVIEW.md.txt').read_bytes(),'frozen_acceptance_identity')

# Two independent descriptions: forward scatter with repeated doubling and
# inverse gather with bit length. Neither is a production constructor.
def check_vector(raw,e,d=1):
    n=len(raw)
    assert n>=1
    m=(4*n-1).bit_length()
    M=1<<m
    check(4*n<=M<8*n,'padding_range')
    raw_copy=tuple(tuple(pair) for pair in raw)
    check(0<=e<=d*m and all(abs(x)<=1<<(d*m) for pair in raw for x in pair),'input_domain')
    A=max(abs(x) for pair in raw_copy for x in pair)
    if not A:
        check(all(x==0 for pair in raw_copy for x in pair),'complete_zero_case')
        return
    k=0; unit=1
    while unit<A:
        unit*=2; k+=1
    check(k==(A-1).bit_length(),'normalization_boundary')
    check(0<=k<=d*m and -d*m<=k-e<=d*m,'exponent_value_bounds')
    check(A<=unit and 2*A>unit,'strict_max_half')
    a0=(n-1)//2
    target=[None]*M
    occupied=set()
    for j,(a,b) in enumerate(raw_copy):
        r=(j-a0)%M
        check(r not in occupied,'center_injection')
        occupied.add(r)
        check(2*abs(j-a0)<=n and 8*abs(j-a0)<=M,'centered_support_bounds')
        target[r]=((a,k),(b,k))
    for r in range(M):
        if target[r] is None:
            target[r]=((0,k),(0,k))
    frozen=tuple(target)
    sq=0
    for r,cell in enumerate(frozen):
        j=r+a0
        if j>=M: j-=M
        check(j==(r+a0)%M,'single_subtraction_index')
        expected=raw_copy[j] if j<n else (0,0)
        check(cell==((expected[0],k),(expected[1],k)),'forward_inverse_identity')
        for num,exp in cell:
            check(type(num) is int and type(exp) is int and exp==k and 0<=exp<=k and abs(num)<=unit,'literal_cell_domain')
            sq+=num*num
    original_sq=sum(a*a+b*b for a,b in raw_copy)
    check(sq==original_sq,'exact_norm_preservation')
    check(4*sq>unit*unit and sq<=2*n*unit*unit,'strict_norm_interval')
    # Exact rational scaling, including negative lambda exponents.
    L=Fraction(2)**(k-e)
    for j in {0,n-1}:
        for num in raw_copy[j]:
            check(L*Fraction(num,unit)==Fraction(num,1<<e),'exact_scale_reconstruction')
    before=tuple(frozen)
    for pair in raw:
        pair[:]=[123456789,-987654321]
    check(frozen==before and all((frozen[(j-a0)%M][0][0],frozen[(j-a0)%M][1][0])==raw_copy[j] for j in range(n)),'input_mutation_isolation')
    COUNTS['nonzero_vector_cases']+=1

for n in (1,2,3):
    m=(4*n-1).bit_length()
    for fields in product((-2,-1,0,1,2),repeat=2*n):
        for e in {0,m}:
            check_vector([[fields[2*j],fields[2*j+1]] for j in range(n)],e)
    COUNTS['exhaustive_length_cases']+=1

for n in list(range(1,130))+[255,256,257,511,512,513,1023,1024,1025]:
    m=(4*n-1).bit_length()
    for d in (1,3):
        for A in sorted({1,2,3,(1<<(d*m-1)),(1<<(d*m-1))+1,(1<<(d*m))-1,1<<(d*m)}):
            for e in (0,d*m):
                raw=[[0,0] for _ in range(n)]
                raw[-1][1]=-A  # A nonzero last second field defeats early-zero exits.
                check_vector(raw,e,d)
                COUNTS['boundary_vector_cases']+=1

# Metadata only at large word widths. No enormous source is allocated.
for m in (2,3,46,128,1024,4096):
    for d in (1,3,7):
        for A in {1,1<<(d*m-1),(1<<(d*m-1))+1,(1<<(d*m))-1,1<<(d*m)}:
            k=(A-1).bit_length()
            check(0<=k<=d*m and A<=1<<k and 2*A>1<<k,'large_normalization_metadata')
            for e in (0,d*m):
                check(Fraction(2)**(k-e)*Fraction(A,1<<k)==Fraction(A,1<<e),'large_scale_metadata')

# Source-parameter eligibility checked symbolically with exact rationals.
beta=Fraction(1,4)
for m in (45,46,47,100):
    ceiling=lambda f:-(-f.numerator//f.denominator)
    M=1<<m; B=1<<ceiling((Fraction(1,2)+beta)*m); k=1<<ceiling(2*beta*m)
    T=M//B; W=2*(2*m+1)*(8*B-1)+1
    sparse=(M%B==0 and B>=4 and T>=4 and B>=4096*k and W<M)
    check(sparse==(m!=45),'symbolic_sparse_guard')
    if sparse:
        check(beta*m>=2 and (32*5*m+4)<M,'symbolic_outer_guard')
        check(Fraction(1,M**3)<=Fraction(1,M),'stronger_probability')
        check((16*m+16)+2*m+2==18*m+18,'accepted_output_width')

result={
 'verdict':'PASS',
 'scope':'Fresh exact reviewer controls; no candidate, scientific, historical, or inherited reviewer program imported or executed. No FFT/recovery execution and no production constructor acceptance.',
 'archive_sha256':digest(archive.read_bytes()),
 'script_sha256':digest(Path(__file__).read_bytes()),
 'counts':dict(sorted(COUNTS.items())),
 'checked_assertions':sum(v for k,v in COUNTS.items() if not k.endswith('_cases')),
}
(OUT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
