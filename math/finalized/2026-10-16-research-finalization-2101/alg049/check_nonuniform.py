#!/usr/bin/env python3
"""Fresh exact ALG-049 support checks. No historical program imports or execution."""
from pathlib import Path
from copy import deepcopy
import json, time, resource
import sympy as s
resource.setrlimit(resource.RLIMIT_CPU,(240,240))
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
ROOT=Path(__file__).resolve().parent
start=time.monotonic(); counts={}
def ck(key,value):
    if not value: raise AssertionError(key)
    counts[key]=counts.get(key,0)+1
z=s.symbols('z',nonzero=True); I=s.eye(8)
def simp(M): return M.applyfunc(s.cancel)
def equal(A,B):return A.shape==B.shape and all(s.cancel(x-y)==0 for x,y in zip(A,B))
def cycle(order,weights):
    n=len(order);M=s.zeros(n)
    if sorted(order)!=list(range(n)) or len(weights)!=n:raise ValueError('cycle grammar')
    for j,v in enumerate(order):M[order[(j+1)%n],v]=weights[j]
    return M
def inv(M):return simp(M.inv(method='DM'))
def star(M):return M.subs(z,1/z).T
M1=cycle(list(range(8)),[1]*7+[-1])
M2=cycle([0,1,3,4,5,6,2,7],[z,1,1,1,1,1,1/z,-1])
factors=[]
for M in [M1,M2]:
    ck('source_cycle_power',equal(M**8,-I))
    ck('source_cycle_unitarity',equal(star(M)*M,I))
    K=simp((2*I-M)*inv(I-M));Ki=inv(K)
    ck('source_K_identity',equal(K*(I-M),2*I-M))
    ck('source_inverse',equal(K*Ki,I))
    factors.append({'+':K,'-':Ki})
actual={};prefix={}
for a in '-+':
    for b in '-+':
        T=simp(factors[0][a]*factors[1][b]);Ti=inv(T)
        L=simp(star(T)*T);Li=simp(Ti*star(Ti))
        ck('inverse_Gram_order',equal(L*Li,I))
        actual[(a+b,'L')]=L;actual[(a+b,'Linv')]=Li;prefix[a+b]=T
cert=json.loads((ROOT/'ROW_CERTIFICATES.json').read_text())
expected_rows={('--','L'):1,('--','Linv'):0,('-+','L'):2,('-+','Linv'):2,('+-','L'):1,('+-','Linv'):3,('++','L'):0,('++','Linv'):0}
def validate(obj):
    assert obj['dimension']==8 and obj['phase_domain']=='abs(z)=1'
    assert len(obj['records'])==8
    seen=set()
    for r in obj['records']:
        key=(r['signs'],r['matrix']);assert key in expected_rows and key not in seen;seen.add(key)
        row=r['row'];assert row==expected_rows[key]
        assert len(r['edges'])==7
        others=set();bounds=[]
        for e in r['edges']:
            i,j=e['i'],e['j'];assert 0<=i<j<8 and row in (i,j)
            other=j if i==row else i;assert other not in others;others.add(other)
            co={int(k):s.Rational(v) for k,v in e['laurent'].items()}
            f=sum(v*z**k for k,v in co.items())
            assert s.cancel(f-actual[key][i,j])==0
            bound=s.Rational(e['lower_bound']);assert bound>0
            if e['method']=='coefficient_dominance':
                mag=sorted([abs(v) for v in co.values()],reverse=True)
                assert bound==mag[0]-sum(mag[1:])
            else:
                assert e['method']=='real_part_lower_bound' and key==('-+','L') and (i,j)==(2,3)
                assert s.cancel(f-(-27*z+55+28/z)/514)==0
                assert bound==s.Rational(27,257)
            bounds.append(bound)
        assert others==set(range(8))-{row}
        assert s.Rational(r['row_lower_bound'])==min(bounds)
    assert seen==set(expected_rows)
validate(cert);ck('complete_continuum_row_certificate',True)
for r in cert['records']:
    for e in r['edges']:ck('exact_row_entry_and_positive_bound',True)
mut=[]
def reject(name,obj):
    try:validate(obj)
    except (AssertionError,ValueError,KeyError,TypeError):mut.append(name);return
    raise AssertionError('mutation accepted: '+name)
x=deepcopy(cert);x['dimension']=16;reject('wrong_dimension',x)
x=deepcopy(cert);x['phase_domain']='z != 0';reject('unrestricted_phase',x)
x=deepcopy(cert);x['records'].pop();reject('missing_sign_or_Gram',x)
x=deepcopy(cert);x['records'][0]['edges'].pop();reject('missing_seventh_edge',x)
x=deepcopy(cert);x['records'][0]['row']=0;reject('wrong_dense_row',x)
x=deepcopy(cert);x['records'][0]['edges'][0]['laurent']['0']='0';reject('altered_coefficient',x)
x=deepcopy(cert);x['records'][0]['edges'][0]['lower_bound']='999';reject('overstated_lower_bound',x)
x=deepcopy(cert);x['records'][0]['row_lower_bound']='1';reject('wrong_row_bound',x)
x=deepcopy(cert);x['records'][0]['matrix']='Linv';reject('wrong_Gram_orientation',x)
x=deepcopy(cert);x['records'][2]['edges'][2]['method']='coefficient_dominance';reject('unsupported_zero_dominance',x)
x=deepcopy(cert);x['records'][0]['edges'][1]=deepcopy(x['records'][0]['edges'][0]);reject('duplicate_edge',x)
# All 256 coefficient support sets, two orders, nonuniform weights, both Grams.
mask_counts={}
for order in [list(range(8)),[0,3,1,7,2,6,4,5]]:
    Q=cycle(order,[1,2,3,1,2,1,3,2]);powers=[Q**k for k in range(8)]
    pos={v:j for j,v in enumerate(order)}
    for mask in range(256):
        E=[k for k in range(8) if mask>>k&1];diff={(a-b)%8 for a in E for b in E}
        h=sum(((k+1)*powers[k] for k in E),s.zeros(8))
        for H in [h.T*h,h*h.T]:
            for i in range(8):
                for j in range(8):
                    if (pos[i]-pos[j])%8 not in diff:ck('forced_support_zero',H[i,j]==0)
            if E and len(diff)<8:
                ck('missing_edge_each_row',all(any(j!=i and H[i,j]==0 for j in range(8)) for i in range(8)))
        if order==list(range(8)):mask_counts[str(mask)]={'size':len(E),'difference_size':len(diff)}
        if len(E)<=3 and E:ck('all_three_term_supports_deficient',len(diff)<8)
ck('degree_three_missing_antipode',4 not in {(a-b)%8 for a in range(4) for b in range(4)})
# Zero weights are admitted by the support lemma; no Q inverse is taken.
Q=cycle(list(range(8)),[0,2,0,1,3,0,1,2]);h=I+Q+Q**2+Q**3
for H in [h.T*h,h*h.T]:
    for i in range(8):ck('zero_weight_support',H[i,(i+4)%8]==0)
# Uniform edge modulus is not needed, and the old diagonal hypothesis can fail.
Q=cycle(list(range(8)),[2,s.Rational(1,2),1,1,1,1,1,-1]);h=I-Q
ck('strict_new_nonconstant_inverse_Gram',len(set((h.T*h).diagonal()))>1 and h.det()!=0)
# Exact congruence order with a nonunitary monomial last separator.
perm=[2,0,7,1,5,3,6,4];S=s.zeros(8)
for j,v in enumerate(perm):S[v,j]=j+1
ck('nonunitary_monomial_control',S.det()!=0 and S.T*S!=I)
C=inv(h);Sinv=inv(S)
for signs,Tformal in prefix.items():
    T=simp(Tformal.subs(z,s.Rational(3,5)+4*s.I/5));L=simp(T.H*T);Li=inv(L)
    B=simp(T*S*C);c=s.Rational(7,3);E=simp(B.H*B-c*I);X=simp(inv(C)*Sinv)
    ck('full_nonunitary_congruence',equal(X.H*E*X,L-c*Sinv.H*inv(C).H*inv(C)*Sinv))
    ck('inverse_target_congruence',equal(inv(B.H*B),inv(C)*Sinv*Li*Sinv.H*inv(C).H))
# Guards: complete difference support does not force holes; arbitrary separator escapes.
P=cycle(list(range(8)),[1]*8);g=I+P+P**2+P**3+P**4
ck('full_difference_support_control',g.det()!=0 and all((g.T*g)[0,j]!=0 for j in range(1,8)))
T=simp(prefix['++'].subs(z,1));Sbad=inv(T)
ck('nonmonomial_escape',equal(T*Sbad,I) and any(sum(v!=0 for v in Sbad.row(i))>1 for i in range(8)))
ck('singular_factor_rejected_by_rank',(I-P).det()==0)
result={'state':'AUTHOR_CHECK_PASS_NOT_INDEPENDENT_ACCEPTANCE','checks':counts,'total_checks':sum(counts.values()),'mutation_rejections':mut,'support_masks':256,'cycle_orders':2,'exact_arithmetic':'SymPy rational and Gaussian-rational Laurent arithmetic; no floating tolerance','elapsed_seconds':round(time.monotonic()-start,3),'historical_programs_run':0,'external_writes':0}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
