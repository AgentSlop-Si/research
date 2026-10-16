"""Read a supplied JSON certificate as data; never import supplied code.

These checks cover rational margins and symbolic address permutations only.
They do not run the rank-saving network or certify whole-machine complexity.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import hashlib, json, zipfile

archive = Path(__file__).with_name('subnlogn_research_checkpoint_v12_direct_layout_2026-10-16.zip')
with zipfile.ZipFile(archive) as z:
    assert sum(i.file_size for i in z.infolist()) < 2_000_000
    assert z.testzip() is None
    raw = z.read('subnlogn_research/parameter_certificate_v12.json')
    cert = json.loads(raw)

def rational(v):
    return F(v['numerator'], v['denominator'])

p = {k: rational(v) if isinstance(v, dict) else v for k,v in cert['parameters'].items()}
L = F(13815511, 1000000)
# Exact rank deficits read from pinned primary section 03, not Budget code.
eta_b, eta_c = F(339,22587335000000), F(73,19906842167500)
a, b = eta_b/L, eta_c/L
tau, sigma, eps, c, k = p['tau'], p['sigma'], p['epsilon'], p['c'], p['kappa']
assert (tau,sigma) == (1-a,1-b)
assert p['beta']==F(1,2) and p['delta']==F(1,16)
assert p['lam']==1-a*a and p['lam_prime']==1-a*a/2
assert c==a*(1-2*a)/(2*(1-a)) and eps==F(1,40)
term=total=F(1)
for j in range(1,100):
    term=term*L/j
    total+=term
assert total>1_000_000  # omitted terms positive: exp(L)>10^6
assert 0<tau<1 and 0<sigma<1
assert L*(1-tau)<=eta_b and L*(1-sigma)<=eta_c
assert max(tau,sigma)<p['lam']<1
assert tau*(1+c/p['beta'])<p['lam']
assert max(p['lam'],sigma+p['beta']*(1-sigma))<p['lam_prime']<1
assert min(c,eps,p['delta'],k)>0
assert eps<F(1,12) and eps*p['guard_power']<1
assert tau+eps*(1-tau)<1
assert F(3,4)+p['delta']+F(3,2)*eps<1
assert eps*(1+c)<1 and eps+p['delta']<1
margins=(1-eps*(1+c), eps*c*(1-tau), eps*(1-p['lam_prime']),
         (1-tau)*(1-eps), F(1,4)-p['delta']-F(3,2)*eps,
         1-p['delta']-eps,eps)
assert margins==tuple(rational(x) for x in cert['margins'])
assert min(margins)>=2*k
assert k==a*a*(1-2*a)/(160*(1-a))
old=a**3*(1-2*a)/4
assert old==rational(cert['old_kappa'])
assert k==rational(cert['new_kappa'])
assert k/old==rational(cert['ratio'])==1/(40*a*(1-a))
assert eps*(2-tau)>1-tau
assert 1/(eps*c)==rational(cert['new_necessary_log2_b'])
assert 1/(a*(1-a)*c)==rational(cert['old_necessary_log2_b'])

def equal_exchange(seq, start, width, gap):
    other=start+width+gap
    return seq[:start]+seq[other:other+width]+seq[start+width:other]+seq[start:start+width]+seq[other+width:]

def move_bit(seq, source, destination):
    out=seq[:]
    value=out.pop(source)
    out.insert(destination,value)
    return out

def direct_bits(seq,prefix,a,gap,b):
    out=seq[:]
    if a<b:
        out=move_bit(out,prefix+a+gap,prefix)
    out=equal_exchange(out,prefix+(a!=b),min(a,b),gap)
    if a>b:
        out=move_bit(out,prefix,prefix+b+gap)
    return out

local_cases=0
for prefix,a,gap,b,suffix in product(range(3),range(1,5),range(5),range(1,5),range(3)):
    if abs(a-b)>1: continue
    seq=list(range(prefix+a+gap+b+suffix))
    h=seq[prefix:prefix+a]
    g=seq[prefix+a:prefix+a+gap]
    d=seq[prefix+a+gap:prefix+a+gap+b]
    expected=seq[:prefix]+d+g+h+seq[prefix+a+gap+b:]
    assert direct_bits(seq,prefix,a,gap,b)==expected
    local_cases+=1

def swap_positions(bits,widths,i,j):
    if i>j:i,j=j,i
    out=direct_bits(bits,sum(widths[:i]),widths[i],sum(widths[i+1:j]),widths[j])
    new=widths[:]
    new[i],new[j]=new[j],new[i]
    return out,new

reversals=exposures=0
for d in range(1,9):
    for widths_tuple in product((1,2), repeat=d):
        widths=list(widths_tuple)
        fields=[[(i,j) for j in range(w)] for i,w in enumerate(widths)]
        original=[v for field in fields for v in field]
        out,shape=original[:],widths[:]
        for i in range(d//2):out,shape=swap_positions(out,shape,i,d-1-i)
        assert out==[v for field in reversed(fields) for v in field]
        assert shape==widths[::-1]
        reversals+=1
        for i in range(d-1):
            out,shape=swap_positions(original,widths,i,d-1)
            assert out[-widths[i]:]==fields[i]
            restored,oldshape=swap_positions(out,shape,i,d-1)
            assert restored==original and oldshape==widths
            exposures+=1

def frac(x):return {'numerator':x.numerator,'denominator':x.denominator}
result={'status':'PASS_SCOPED_CONDITIONAL_CHECKS',
 'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
 'certificate_sha256':hashlib.sha256(raw).hexdigest(),
 'archive_crc_pass':True,'supplied_code_executed':False,
 'rational_parameter_and_margin_checks':'all asserted exact conditions passed',
 'new_kappa':frac(k),'old_kappa':frac(old),'ratio':frac(k/old),
 'symbolic_swap_cases':local_cases,'symbolic_reversal_shapes':reversals,
 'symbolic_expose_restore_cases':exposures,
 'scope':'Conditional scalar inequalities and symbolic coordinate permutations only. No source-code replay, full numerical composition, huge network execution, whole-machine proof, runtime benchmark or novelty verification.'}
# A separate, explicitly conditional parameter point under the same listed
# inequalities. It does not change or silently replace the supplied certificate.
eps_alt=F(1,21)
a_rank=1-tau
k_alt=eps_alt*c*a_rank/2
alt_margins=(1-eps_alt*(1+c),eps_alt*c*a_rank,eps_alt*(1-p['lam_prime']),
             a_rank*(1-eps_alt),F(1,4)-p['delta']-F(3,2)*eps_alt,
             1-p['delta']-eps_alt,eps_alt)
assert eps_alt<F(1,12) and eps_alt*p['guard_power']<1
assert min(alt_margins)>=2*k_alt>0
assert k_alt/k==F(40,21)
assert eps_alt*(2-tau)>a_rank
result['additional_parameter_point']={
 'status':'Exact witness for the same displayed conditional inequalities only',
 'epsilon':frac(eps_alt),'kappa':frac(k_alt),'factor_over_supplied_v12':frac(k_alt/k),
 'necessary_log2_b':frac(1/(eps_alt*c)),
 'all_other_parameters':'unchanged',
 'scope':'No optimality, novelty, implementation or full-framework theorem claim.'}
Path(__file__).with_name('INDEPENDENT_CONTRACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
