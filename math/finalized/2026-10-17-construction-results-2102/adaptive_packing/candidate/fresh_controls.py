#!/usr/bin/env python3
"""New exact controls. Standard library only; no historical code imported.
Python multiplication is used for local control arithmetic and endpoint oracles,
not as a claimed asymptotic subroutine in the proof.
"""
from fractions import Fraction
from functools import lru_cache
from collections import Counter
import hashlib, json, math, pathlib, random, zipfile
HERE=pathlib.Path(__file__).resolve().parent

@lru_cache(None)
def native(rank):
    E=math.lcm(*range(1,rank+1)); d=E//rank; k=0; modulus=1
    for p in range(2,rank+1):
        if any(p%q==0 for q in range(2,math.isqrt(p)+1)): continue
        q=1
        while d%(q*p)==0: q*=p
        if q==1: continue
        u=1
        while E%(u*p)==0: u*=p
        target=(-pow(E//u,-1,q))%q
        k+=modulus*((target-k)*pow(modulus,-1,q)%q); modulus*=q
    assert modulus==d
    if d==1: k=1
    assert 1<=k<=max(1,d-1)
    P=1+k*E
    weights=[1]
    for j in range(1,rank+1): weights.append(weights[-1]*(1+(P-1)//j))
    assert weights[-1]%d==0
    beta=weights[-1]//d; s=beta.bit_length()-1
    assert beta>weights[-2]
    return P,s,tuple(weights[:-1])

@lru_cache(None)
def binomial(x,j):
    if x>=0: return math.comb(x,j) if x>=j else 0
    return (-1 if j%2 else 1)*math.comb(-x+j-1,j)

@lru_cache(None)
def nodes(rank):
    def norm(x): return sum(abs(binomial(x,j)) for j in range(rank))
    a=min(range(rank),key=lambda q:(max(norm(-q),norm(2*rank-2-q)),q))
    return tuple(range(-a,2*rank-1-a))

def coefficients(b,weights):
    out=[0]*len(weights)
    for j in range(len(weights)-1,-1,-1): out[j],b=divmod(b,weights[j])
    assert b==0
    return out

def evaluate(c,x): return sum((-1 if j%2 else 1)*z*binomial(x,j) for j,z in enumerate(c) if z)

def width(L,A,B): return 8*max(1,((2*L*A*B).bit_length()+7)//8)

def pack(values,w): return sum(v<<(j*w) for j,v in enumerate(values))

def unpack(value,w,length,bound):
    Q=1<<w; result=[]
    for _ in range(length):
        a=value%Q
        if 2*a>=Q: a-=Q
        assert abs(a)<=bound
        result.append(a); value=(value-a)//Q
    assert value==0
    return result

def interpolate(values,target,start):
    row=list(values); ans=0
    for j in range(len(values)):
        ans+=row[0]*binomial(target-start,j)
        row=[b-a for a,b in zip(row,row[1:])]
    return ans

def exact_floor_log2(value):
    value=Fraction(value); a,b=value.numerator,value.denominator
    assert a>0
    k=a.bit_length()-b.bit_length()
    if k>=0: return k if a>=b<<k else k-1
    return k if a<<(-k)>=b else k-1

def parameter_cell(R,D,C,sample=None):
    """Return an EXACT cell around a sample and an interior product multiple."""
    low,high=Fraction(1<<R),Fraction(3*(1<<(R-1)))
    sample=(low+high)/2 if sample is None else Fraction(sample)
    alpha=Fraction(1); S=1; stages=[]; c=C.bit_length()
    for _ in range(D):
        e=alpha*sample; r=exact_floor_log2(e+c); P,s,_=native(r)
        low=max(low,(Fraction(1<<r)-c)/alpha)
        high=min(high,(Fraction(1<<(r+1))-c)/alpha)
        b=2*(e/s+1)*C*C
        w=8*(exact_floor_log2(b)//8+1)
        low=max(low,(Fraction(1<<(w-8),2*C*C)-1)*s/alpha)
        high=min(high,(Fraction(1<<w,2*C*C)-1)*s/alpha)
        assert low<=sample<high
        stages.append((r,P,s,w,alpha)); S*=s; alpha*=Fraction(w,s)
    E=(low.numerator//low.denominator//S+1)*S
    return {'ok':low<E<high,'E':E,'S':S,'low':low,'high':high,'stages':stages}

def verify_cell(R,D,C,cell):
    assert cell['ok']; E=cell['E']; e=E; rows=[]; multiplicity=1
    for r,P,s,w,alpha in cell['stages']:
        assert e==alpha*E and e.denominator==1 if isinstance(e,Fraction) else e==alpha*E
        e=int(e); c=C.bit_length(); n=e+c
        assert n.bit_length()-1==r and e%s==0 and c<s and C<P
        K=e//s; assert width(K+1,C,C)==w
        child_e=K*w; child_n=child_e+c
        assert child_n<n
        rows.append({'rank':r,'point_bits':P.bit_length(),'block_bits':s,'slot_bits':w,
                     'exponent':e,'actual_parent_bits':n,'actual_child_bits':child_n,
                     'node_count':2*r-1,'actual_volume_numerator':(2*r-1)*child_n,
                     'actual_volume_denominator':n,'actual_volume':(2*r-1)*child_n/n,
                     'allocated_child_bits':(K+1)*w,'independent_calls_at_level':multiplicity})
        multiplicity*=2*r-1; e=child_e
    return {'R':R,'depth':D,'core':C,'core_bits':C.bit_length(),'root_exponent':E,
            'modulus_bits':cell['S'].bit_length(),
            'cell_width_floor_log2':exact_floor_log2(cell['high']-cell['low']),
            'steps':rows,'last_level_call_count':multiplicity,
            'last_actual_bits':int(e)+C.bit_length(),
            'total_last_level_bits':multiplicity*(int(e)+C.bit_length()),
            'root_bits':E+C.bit_length()}

def schoolbook(a,b):
    sign=-1 if (a<0)!=(b<0) else 1; a,b=abs(a),abs(b); out=0
    for j in range(b.bit_length()):
        if (b>>j)&1: out+=a<<j
    return sign*out

def adaptive(a,b,stats,depth=0,base=2048):
    n=max(abs(a).bit_length(),abs(b).bit_length()); stats['calls'][depth]+=1
    stats['sizes'].setdefault(depth,set()).add(n)
    if not a or not b: stats['zero']+=1; return 0
    if n<=base: stats['base']+=1; return schoolbook(a,b)
    sign=-1 if (a<0)!=(b<0) else 1; a,b=abs(a),abs(b)
    r=n.bit_length()-1; P,s,W=native(r); xs=nodes(r); L=(n+s-1)//s; mask=(1<<s)-1
    ac=[coefficients((a>>(s*j))&mask,W) for j in range(L)]
    bc=[coefficients((b>>(s*j))&mask,W) for j in range(L)]
    requests=[]
    for x in xs:
        ar=[evaluate(c,x) for c in ac]; br=[evaluate(c,x) for c in bc]
        A=max(map(abs,ar)); B=max(map(abs,br))
        if not A*B: requests.append(None);continue
        w=width(L,A,B); U=pack(ar,w); V=pack(br,w)
        requests.append((U,V,w,L*A*B))
    if any(z and max(abs(z[0]).bit_length(),abs(z[1]).bit_length())>=n for z in requests):
        stats['fallback']+=1; return sign*schoolbook(a,b)
    output=[]
    for z in requests:
        if z is None: stats['skipped_rows']+=1; output.append([0]*(2*L-1));continue
        U,V,w,bound=z
        product=adaptive(U,V,stats,depth+1,base)
        output.append(unpack(product,w,2*L-1,bound))
    result=0
    for j in range(2*L-1):
        value=interpolate([row[j] for row in output],-P,xs[0])
        result+=value<<(s*j)
    return sign*result

def fresh_stats(): return {'calls':Counter(),'sizes':{},'base':0,'zero':0,'fallback':0,'skipped_rows':0}
def serial_stats(st): return {**st,'calls':dict(st['calls']),'sizes':{k:sorted(v) for k,v in st['sizes'].items()}}


def main():
    # Portable provenance prelude; only source I/O changes from the reviewed script.
    # This version has not been executed during publication packaging.
    recorded=json.loads((HERE/'SOURCE_PINS.json').read_text())
    sha=recorded['archive_sha256']
    assert sha=='936bf7706643fc130c7cb1197848bf1c2bf193be533cdc01e6c3b265351c1581'
    pins={name:hashlib.sha256((HERE/'source'/name).read_bytes()).hexdigest()
          for name in recorded['source_members']}
    assert pins==recorded['source_members']
    assert (HERE/'source/fft_outside_crt/asymptotic/packed_outer.py').read_bytes()==(HERE/'source/predecessor/packed_outer.py').read_bytes()
    results={'scope':'Fresh exact arithmetic only; no historical module imports, no timing claim.',
             'metadata_cells':[],'exact_node_controls':[],'recursive_products':[],'sharing_controls':[]}
    for R in [16,20,24,32,64,128,256,512,1024]:
        c=3*R//4; C=(1<<(c-1))+1
        # Finite small controls use at least one level; theorem depth is separate.
        theorem_D=R//(16*math.ceil(math.log2(R))); D=max(1,theorem_D)
        cell=parameter_cell(R,D,C); row=verify_cell(R,D,C,cell);row['theorem_depth']=theorem_D
        results['metadata_cells'].append(row)
        print('Cell',R,'levels',D,'minimum actual volume',min(x['actual_volume'] for x in row['steps']),flush=True)
    # Locate an actual materializable two-level family without claiming that the
    # conservative asymptotic D estimate is positive at this small rank.
    R=17; C=(1<<(3*R//4-1))+1; two=None
    for q in range(1,32):
        candidate=parameter_cell(R,2,C,Fraction((1<<R)*(64+q),64))
        if candidate['ok'] and all(C<P for _,P,_,_,_ in candidate['stages']): two=candidate;break
    assert two is not None
    small=verify_cell(R,2,C,two);results['materialized_two_level_family']=small
    e=small['root_exponent']
    for stage in small['steps']:
        r,P,s,w=stage['rank'],native(stage['rank'])[0],stage['block_bits'],stage['slot_bits']
        K=e//s; X=C<<e; nodes_here=nodes(r); expected=C<<(K*w)
        for x in nodes_here:
            coeff=[0]*(K+1);coeff[-1]=C
            actual=pack(coeff,w); assert actual==expected and actual.bit_length()==stage['actual_child_bits']
            assert width(K+1,max(map(abs,coeff)),max(map(abs,coeff)))==w
        results['exact_node_controls'].append({'rank':r,'nodes':len(nodes_here),'actual_bits':X.bit_length(),
            'actual_child_bits':expected.bit_length(),'distinct_child_pairs':1})
        e=K*w
    E=small['root_exponent']; X=C<<E
    st=fresh_stats(); product=adaptive(X,X,st); assert product==X*X
    assert st['calls'][0]==1 and st['calls'][1]==33 and st['calls'][2]==759
    assert st['sizes'][1]=={7884} and st['sizes'][2]=={1036}
    results['recursive_products'].append({'label':'closed two-level actual family','bits':X.bit_length(),
        'stats':serial_stats(st),'output_sha256':hashlib.sha256(product.to_bytes((product.bit_length()+7)//8,'little')).hexdigest()})
    rng=random.Random(202610172046)
    for bits in [0,1,127,2048,4096,4096,4096,8192]:
        a=rng.getrandbits(bits); b=rng.getrandbits(bits)
        if bits: a|=1<<(bits-1); b|=1<<(bits-1)
        if bits%3==1:a=-a
        if bits%5==1:b=-b
        st=fresh_stats(); got=adaptive(a,b,st); assert got==a*b
        results['recursive_products'].append({'label':'signed/random/zero','bits':bits,'stats':serial_stats(st)})
    # Content extraction: actual dense input and full endpoint, with only the
    # small core product performed by the explicit schoolbook procedure.
    valuation=(X&-X).bit_length()-1; core=X>>valuation
    assert valuation==E and core==C
    extracted=schoolbook(core,core)<<(2*valuation); assert extracted==X*X
    results['sharing_controls'].append({'kind':'content extraction','input_bits':X.bit_length(),
        'valuation':valuation,'core_bits':core.bit_length(),'large_products_required':0,
        'small_product_bits':[core.bit_length(),core.bit_length()]})
    # Distinct/odd child perturbation and exact shared ordinary-value product.
    r=R;P,s,W=native(r);K=E//s;xs=nodes(r);w=width(K+1,C,C)
    assert E%s==0 and P<(1<<s)
    low_digits=coefficients(P,W);assert low_digits==[0,1]+[0]*(r-2)
    Y=X+P;assert Y%2==1
    children=[];raw=[]; common=schoolbook(C,C)
    for x in xs:
        assert evaluate(low_digits,x)==-x and abs(x)<C
        row=[0]*(K+1);row[0]=-x;row[-1]=C
        assert width(K+1,max(map(abs,row)),max(map(abs,row)))==w
        U=pack(row,w);assert U==(C<<(K*w))-x and U.bit_length()==(C<<(K*w)).bit_length()
        shared=(common<<(2*K*w))-(schoolbook(2*C,x)<<(K*w))+schoolbook(x,x)
        assert shared==U*U
        conv=unpack(shared,w,2*K+1,(K+1)*C*C)
        expected=[0]*(2*K+1);expected[0]=x*x;expected[K]=-2*C*x;expected[2*K]=C*C
        assert conv==expected
        raw.append(conv);children.append(U)
    assert len(set(children))==len(xs)
    assert sum(v%2!=0 for v in children)>=r-1
    values={j:interpolate([row[j] for row in raw],-P,xs[0]) for j in [0,K,2*K]}
    assert values=={0:P*P,K:2*C*P,2*K:C*C}
    reconstructed=sum(v<<(s*j) for j,v in values.items()); assert reconstructed==Y*Y
    results['sharing_controls'].append({'kind':'distinct odd perturbed children','input_bits':Y.bit_length(),
        'root_valuation':0,'node_count':len(xs),'distinct_child_pairs':len(set(children)),
        'odd_child_pairs':sum(v%2!=0 for v in children),'child_actual_bits':children[0].bit_length(),
        'large_products_required_by_shared_formula':0,'shared_core_product_count':1,
        'nonzero_outer_product_columns':[0,K,2*K],'exact_endpoint':True})
    # Source strict width boundary: exact powers of two require the next slot.
    boundaries=[]
    for q in range(1,65):
        B=1<<(8*q)
        real_width=8*(exact_floor_log2(Fraction(B))//8+1)
        source_width=8*((B.bit_length()+7)//8)
        assert real_width==source_width==8*(q+1)
        boundaries.append(q)
    results['strict_width_boundary_controls']=len(boundaries)
    results['totals']={'parameter_cells':len(results['metadata_cells'])+1,
       'aligned_exact_levels':sum(len(z['steps']) for z in results['metadata_cells'])+2,
       'materialized_aligned_node_calls':sum(z['nodes'] for z in results['exact_node_controls']),
       'complete_recursive_products':len(results['recursive_products']),
       'total_executor_calls':sum(sum(z['stats']['calls'].values()) for z in results['recursive_products']),
       'shared_perturbed_node_products':len(xs),'width_boundary_controls':len(boundaries)}
    (HERE/'CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results['totals'],indent=2),flush=True)
    print('All fresh controls passed.',flush=True)
if __name__=='__main__':main()
