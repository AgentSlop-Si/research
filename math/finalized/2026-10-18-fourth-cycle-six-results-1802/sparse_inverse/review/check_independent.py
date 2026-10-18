#!/usr/bin/env python3
"""Independent audit. Does not import, execute, or rewrite the candidate checker."""
from pathlib import Path
import hashlib, itertools, json, time
from sympy import QQ, I, sqrt, Rational
from sympy.polys.matrices import DomainMatrix as DM
ROOT=(Path(__file__).resolve().parent / '../candidate')
HERE=Path(__file__).resolve().parent
K=QQ.algebraic_field(sqrt(2)*(1+I)/2)
z=K.unit
one=K.one
zero=K.zero

def mat(a): return DM(a,(len(a),len(a[0])),K)
def eye(n): return mat([[one if i==j else zero for j in range(n)] for i in range(n)])
def cut(a,rows,cols): return a.extract(list(rows),list(cols))
def decode_scalar(a): return sum((K.from_sympy(Rational(v))*z**i for i,v in enumerate(a)),zero)
def decode(a): return mat([[decode_scalar(v) for v in row] for row in a])
def value(v): return str(K.to_sympy(v))
def chart(a,d,l,m,u,v):
    rows=a.to_list()
    return all(rows[i][j]==(d[i] if i==j else l[i]*m[j] if i>j else u[i]*v[j]) for i in range(8) for j in range(8))

start=time.monotonic()
answer={'candidate_sha256':hashlib.sha256((ROOT/'REPORT.md').read_bytes()).hexdigest(),'independent_engine':'SymPy 1.14 DomainMatrix over QQ(zeta8); zeta8=sqrt(2)(1+i)/2','checks':{}}
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for e in manifest['files']:
    b=(ROOT/e['path']).read_bytes()
    assert len(b)==e['bytes']
    assert hashlib.sha256(b).hexdigest()==e['sha256']
answer['checks']['candidate_manifest_files']=len(manifest['files'])
bindings=json.loads((ROOT/'SOURCE_BINDINGS.json').read_text())
for e in bindings['bindings']:
    b=(ROOT/e['local_file']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']
    assert hashlib.sha256(b).hexdigest()==e['sha256']
answer['checks']['source_git_blob_matches']=len(bindings['bindings'])
owner=json.loads((ROOT/'sources/OWNER_RECORD.json').read_text())
assert owner['stable_id']=='M-NONLINEAR-COMPATIBILITY' and owner['status']=='TO RESEARCH' and owner['priority']==34
answer['checks']['owner_scope_and_priority']=True

F=mat([[z**(i*j) for j in range(8)] for i in range(8)])
assert z**8==one and all(z**j!=one for j in range(1,8))
assert F*mat([[z**(-i*j)/K(8) for j in range(8)] for i in range(8)])==eye(8)
counts={}
for m in range(1,9):
    count=0
    for a in range(8):
        rows=[(a+i)%8 for i in range(m)]
        for cols in itertools.combinations(range(8),m):
            d=cut(F,rows,cols).det()
            formula=z**(a*sum(cols))
            for j,k in itertools.combinations(cols,2): formula*=z**k-z**j
            assert d==formula and d!=zero
            count+=1
    counts[m]=count
answer['checks']['all_consecutive_square_minor_counts']=counts
answer['checks']['all_consecutive_square_minors']=sum(counts.values())

support=[set(c) for n in range(1,4) for c in itertools.combinations(range(8),n)]
unions={};pairs=0
for a,b in itertools.combinations_with_replacement(support,2):
    union=tuple(sorted(a|b));unions[union]=True;pairs+=1
assert pairs==4278 and len(unions)==246
assert all(cut(F,range(2,8),u).rank()==len(u) for u in unions)
answer['checks']['support_pairs']=pairs
answer['checks']['support_unions_checked_directly']=len(unions)

reported=json.loads((ROOT/'RESULTS.json').read_text())
# Regenerate the genuinely newly excluded chart stage from its generators.
a=eye(8).to_list();a[2][0]=a[5][7]=one;A=mat(a);C=A.inv()
assert A*C==eye(8) and C*A==eye(8)
d=[one]*8;l=[zero]*8;m=[zero]*8;u=[zero]*8;v=[zero]*8
l[2]=m[0]=u[5]=v[7]=one
assert chart(A,d,l,m,u,v)
assert A==decode(reported['strict_extension_witness']['A']) and C==decode(reported['strict_extension_witness']['C'])
assert cut(C,[2,5],[0,7]).det()==one
assert max(sum(row[j]!=zero for row in C.to_list()) for j in range(8))==2
assert C.to_list()[2][0]!=zero
answer['checks']['new_source_chart_witness']=True

# Independently invert the dense source stage and compute its disjoint minor.
D=mat([[K(3 if i==j else 1 if i>j else 2) for j in range(8)] for i in range(8)])
H=D.inv()
assert D*H==eye(8) and H*D==eye(8)
assert chart(D,[K(3)]*8,[one]*8,[one]*8,[K(2)]*8,[one]*8)
assert all(x!=zero for row in H.to_list() for x in row)
boundary_minor=cut(H,[0,2,4],[1,3,5]).det()
assert boundary_minor==K.from_sympy(Rational(-8,511))
answer['checks']['dense_boundary_minor']=value(boundary_minor)

# Independently reconstruct the five-sample collision by exact nullspace.
null=cut(F,range(3,8),range(6)).nullspace()
assert null.shape==(1,6)
w=null.to_list()[0]
assert all(t!=zero for t in w)
a=eye(8).to_list()
for i in range(8):
    a[i][0]=w[i] if i<6 and i%2==0 else zero
    a[i][1]=-w[i] if i<6 and i%2 else zero
collision=mat(a)
assert collision.det()!=zero
assert max(sum(row[j]!=zero for row in a) for j in range(8))==3
assert cut(F*collision,range(3,8),[0,1]).rank()==1
assert cut(F*collision,range(2,8),[0,1]).rank()==2
saved_collision=decode(reported['sampling_sharpness']['C'])
assert saved_collision.det()!=zero
assert cut(F*saved_collision,range(3,8),[0,1]).rank()==1
assert cut(F*saved_collision,range(2,8),[0,1]).rank()==2
assert saved_collision.det()==decode_scalar(reported['sampling_sharpness']['determinant'])
answer['checks']['independent_and_reported_sample_collisions']=True

# Independently reconstruct a rank-two repair attaining the kernel lemma bound.
T=cut(F,range(4,8),range(8))
right=cut(F,range(4,8),range(4,8)).inv()
a=eye(8).to_list()
for anchor,target in [(2,0),(3,1)]:
    tail=right*(-cut(F,range(4,8),[anchor]))
    for i in range(8):
        a[i][anchor]=(one if i==target or i==anchor else zero) if i<4 else tail.to_list()[i-4][0]
sharp=mat(a);R=sharp-eye(8)
assert sharp.det()==one and R.rank()==2 and cut(F*sharp,range(4,8),range(4)).rank()==2
assert sharp==decode(reported['rank_debit_sharpness']['C'])
answer['checks']['local_k_minus_r_bound_attained']=True

# A singular sparse core with a nontrivial repair, and three hypothesis mutations.
S=eye(8).to_list();S[0][0]=zero;S=mat(S);R=eye(8)-S
assert S.rank()==7 and R.rank()==1 and (S+R).rank()==8
assert cut(F*(S+R),[5,6,7],[0,1,2]).rank()==3
assert cut(F,[0,2,4,6],[0,4]).rank()==1
bad=eye(8).to_list()
for i in range(8): bad[i][1]=bad[i][0]
bad=mat(bad)
assert bad.det()==zero and cut(F*bad,range(2,8),[0,1]).rank()==1
answer['checks']['singular_sparse_core_allowed']=True
answer['checks']['nonconsecutive_and_dependent_mutations']=True

# Singular sparse core can also attain k-r in the general kernel lemma.
S=mat([[one,zero,zero,zero],[zero,one,zero,zero],[zero,zero,zero,one],[zero,zero,zero,zero]])
R=mat([[zero]*4,[zero]*4,[zero]*4,[zero,zero,one,zero]])
C=S+R;T=mat([[one,zero,zero,zero],[zero,one,zero,zero],[zero,zero,one,zero]])
assert S.rank()==3 and R.rank()==1 and C.det()!=zero and (T*S).rank()==S.rank()
assert cut(T*C,range(3),range(3)).rank()==2
answer['checks']['singular_core_general_lemma_sharpness']=True
answer['all_checks_passed']=True
answer['elapsed_seconds']=round(time.monotonic()-start,3)
(HERE/'RESULTS.json').write_text(json.dumps(answer,indent=2)+'\n')
print(json.dumps(answer,indent=2))
