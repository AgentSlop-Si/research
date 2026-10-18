"""Independent bounded-variation reviewer. Algebraic roots; no trig/oracle import."""
from fractions import Fraction
from math import isqrt
from pathlib import Path
from dataclasses import asdict
import hashlib,json,sys,time
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'candidate'
Q=512
U=1<<Q

def ceildiv(a,b):return -((-a)//b)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[1],-x[0])
def scale(x,a,b=1):
    p=[a*x[0],a*x[1]]
    return min(p)//b,ceildiv(max(p),b)
def mul(x,y):
    p=[a*b for a in x for b in y]
    return min(p)//U,ceildiv(max(p),U)
def sqrt_interval(x):
    assert x[0]>=0
    a=isqrt(x[0]*U);b=isqrt(x[1]*U)
    if b*b<x[1]*U:b+=1
    assert a*a<=x[0]*U and b*b>=x[1]*U
    return a,b

def roots(n):
    """Enclose exp(2*pi*i*k/n) by exact half-angles then interval recurrence."""
    assert n>=4 and not n&(n-1)
    c=(0,0);s=(U,U);size=4
    while size<n:
        c,s=sqrt_interval(scale(add((U,U),c),1,2)),sqrt_interval(scale(add((U,U),neg(c)),1,2))
        size*=2
    result=[];z=((U,U),(0,0))
    for k in range(n):
        result.append(z)
        z=(add(mul(z[0],c),neg(mul(z[1],s))),add(mul(z[0],s),mul(z[1],c)))
    assert z[0][0]<=U<=z[0][1] and z[1][0]<=0<=z[1][1]
    return result

def inverse_sqrt(n):
    a=isqrt(U*U//n);b=a+(a*a*n<U*U)
    assert a*a*n<=U*U<=b*b*n
    return a,b

def direct_targets(values,n,offset,h):
    table=roots(n);root=inverse_sqrt(n);result=[]
    for k in range(n):
        re=(0,0);im=(0,0)
        for j,(a,b) in enumerate(values):
            c,s=table[((j-offset)*k)%n]
            re=add(re,add(scale(c,a),scale(s,b)))
            im=add(im,add(scale(c,b),scale(s,-a)))
        result.append((scale(mul(re,root),1,1<<h),scale(mul(im,root),1,1<<h)))
    return result

def squared_error(pair,target,bits):
    return sum((max(abs(Fraction(v,1<<bits)-Fraction(a,U)),abs(Fraction(v,1<<bits)-Fraction(b,U)))**2 for v,(a,b) in zip(pair,target)),Fraction(0))
def fj(x):return [x.numerator,x.denominator]
def dump(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')

def check_independent_math():
    original=json.loads((SOURCE/'ORIGINAL.json').read_text());values=original['data']
    m=original['m'];N=1<<(m-2);M=4*N
    assert len(values)==N
    E=sum(a*a+b*b for a,b in values)
    jumps=[values[0]]+[(a-c,b-d) for (a,b),(c,d) in zip(values[1:],values[:-1])]+[values[-1]]
    B=sum(abs(a)+abs(b) for a,b in jumps)
    C=isqrt(N*B*B//(4*E));C+=C*C*4*E<N*B*B
    h=0
    while (1<<(2*h))<E:h+=1
    R2=Fraction(E,1<<(2*h));K=C*(1<<ceildiv(m,4));P=16*m+16
    assert Fraction(1,4)<R2<=1
    assert (C-1)**2*4*E<N*B*B<=C*C*4*E
    assert (N,E,B,C,h,K)==(512,1145,6,3,6,24)
    start=time.monotonic()
    targets=direct_targets(values,M,(N-1)//2,h)
    original_targets=direct_targets(values,N,0,h)
    dump('ALGEBRAIC_TARGETS.json',{'Q':Q,'centered':targets,'original_normalized':original_targets})
    # Entire omitted tail can be checked before saved output becomes available.
    omitted=[]
    for k,t in enumerate(targets):
        if min(k,M-k)>K:
            sq=squared_error((0,0),t,P)
            assert sq*sq*M<=R2*R2
            omitted.append((sq,k))
    maximum,frequency=max(omitted)
    result={'N':N,'M':M,'E':E,'B':B,'C':C,'h':h,'scale':h-original['F'],'cutoff':K,'sparse_records':2*K+1,
        'direct_centered_terms':N*M,'direct_original_terms':N*N,'omitted_coefficients_checked':len(omitted),
        'maximum_omitted_squared_upper':fj(maximum),'maximum_omitted_frequency':frequency,
        'oracle':'512-bit nested radical roots by half-angle identities, interval root recurrence and exact integer outward rounding; no production/previous oracle arithmetic imports',
        'seconds':time.monotonic()-start}
    dump('INDEPENDENT_MATH.json',result)
    print(json.dumps(result),flush=True)

def reproduce_front():
    sys.path.insert(0,str(HERE.parent/'candidate'))
    import bounded_variation as front
    original=json.loads((SOURCE/'ORIGINAL.json').read_text())
    start=time.monotonic();estimates,receipt=front.produce(original)
    print('Independent fresh provider reproduced; beginning complete semantic source replay.',flush=True)
    okay,replay=front.replay(original,estimates);assert okay
    assert receipt['events']['dense_coordinate_visits']==replay['replay_production']['events']['dense_coordinate_visits']==512
    assert receipt['events']['coefficient_outputs']==replay['replay_production']['events']['coefficient_outputs']==49
    dump('FRESH_SOURCE_REPRODUCTION.json',{'estimates':asdict(estimates),'production':receipt,'semantic_source_replay':replay,'replay_passed':okay,'seconds':time.monotonic()-start})
    print('Independent fresh provider plus complete semantic source replay passed.',flush=True)

def check_saved():
    original=json.loads((SOURCE/'ORIGINAL.json').read_text());saved=json.loads((SOURCE/'OUTPUT.json').read_text())
    targets=json.loads((HERE/'ALGEBRAIC_TARGETS.json').read_text());math=json.loads((HERE/'INDEPENDENT_MATH.json').read_text())
    repro_path=HERE/'FRESH_SOURCE_REPRODUCTION.json'
    reproduction=json.loads(repro_path.read_text()) if repro_path.exists() else None
    if reproduction is not None:assert saved['estimates']==reproduction['estimates']
    assert saved['source']==saved['estimates']['source']
    assert saved['source']['blocks']==[[173,1,0],[384,2,0],[512,-1,0]]
    src=saved['source'];est=saved['estimates'];out=saved['output'];N=src['N'];M=4*N
    assert src['energy']==math['E'] and src['variation_factor']==math['C'] and src['scale']==math['scale']
    assert est['cutoff']==math['cutoff'] and len(est['pairs'])==math['sparse_records']
    support=dict(est['pairs']);assert len(support)==len(est['pairs'])
    assert sorted(support)==[k for k in range(M) if min(k,M-k)<=est['cutoff']]
    R2=Fraction(src['energy'],1<<(2*src['h']));rho2=Fraction(1,1<<(2*est['bits']))
    retained=[];overall=[]
    for k,target in enumerate(targets['centered']):
        sq=squared_error(support.get(k,(0,0)),target,est['bits'])
        assert sq*sq*M<=R2*R2
        if k in support:assert sq<=rho2;retained.append(sq)
        overall.append(sq)
    rows=[squared_error(pair,target,out['bits']+src['scale']) for pair,target in zip(out['pairs'],targets['original_normalized'])]
    assert len(rows)==N
    maximum=max(rows);fraction=Fraction(1,10000)
    while maximum>R2*fraction*fraction:fraction+=Fraction(1,10000)
    claimed=json.loads((SOURCE/'TARGET_CHECKS.json').read_text())
    assert maximum<=R2*Fraction(*claimed['relative_error_upper_rational'])**2
    # Original physical scale check is explicit, not target renaming.
    assert src['scale']==src['h']-original['F']
    assert out['bits']==max(0,out['normalized_bits']-src['scale'])
    shift=max(0,src['scale']-out['normalized_bits'])
    assert all(a%(1<<shift)==b%(1<<shift)==0 for a,b in out['pairs'])
    dump('INDEPENDENT_OUTPUT_CHECKS.json',{'all_original_rows_checked':N,'all_centered_coefficients_checked':M,
        'retained_complex_rho_checks':len(retained),'global_beta_one_quarter_checks':len(overall),'fresh_source_pairs_identical':None if reproduction is None else True,
        'original_scale_back_exact':True,'maximum_original_squared_error_upper':fj(maximum),
        'maximum_original_row':rows.index(maximum),'relative_error_upper_rational':fj(fraction),
        'candidate_claimed_relative_error_upper':claimed['relative_error_upper_rational'],
        'maximum_retained_squared_error_upper':fj(max(retained)),
        'row_squared_error_upper':[fj(v) for v in rows]})
    print(json.dumps({'all_saved_results_independently_accepted':True,'relative_error_upper':fj(fraction)}),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='math':check_independent_math()
    elif sys.argv[1]=='front':reproduce_front()
    elif sys.argv[1]=='saved':check_saved()
