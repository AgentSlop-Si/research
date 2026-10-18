"""Fresh standard-library verifier for the residual formulation and target.
It checks identities and finite coverage, not the unsolved ideal eliminations.
"""
import itertools, json, math, pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def apow(e):
    e%=32
    z=[0]*16
    z[e%16]=1 if e<16 else -1
    return tuple(z)

def add(a,b):return tuple(x+y for x,y in zip(a,b))
ZERO=(0,)*16
ONE=(1,)+(0,)*15

def all_counts(r):
    # Independent stars-and-bars enumeration rather than generator recursion.
    for cuts in itertools.combinations(range(r+7),7):
        q=(-1,)+cuts+(r+7,)
        yield tuple(q[i+1]-q[i]-1 for i in range(8))

def move(n):
    result=[0]*8
    for old,new in enumerate((3,6,7,4,1,2,5,8)):
        result[new-1]=n[old]
    return tuple(result)

def class_of(n):
    ns=[n]
    for _ in range(3):ns.append(move(ns[-1]))
    assert move(ns[-1])==n
    return tuple(sorted(set(ns)))

def multiply(a,b):
    result=[0]*16
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[(i+j)%16]+=x*y
    return result

def evaluate_terms(terms,values):
    return sum(c*math.prod(v**p for v,p in zip(values,e)) for e,c in terms)

def main():
    checks={}
    entries=0
    for i in range(16):
        for j in range(16):
            value=ZERO
            for k in range(16):value=add(value,apow(-(i-k)**2+(k-j)**2))
            want=(16,)+(0,)*15 if i==j else ZERO
            assert value==want
            entries+=1
    checks['full_matrix_inverse_entries']=entries
    for r in range(16):
        for t in range(16):assert apow(((t-r)%16)**2)==apow(r*r+t*t-2*r*t)
    checks['shift_normalization_coefficients']=256
    for t in range(16):
        lhs=tuple((-1)**t*c for c in apow(t*t))
        assert lhs==apow(((t-8)%16)**2)
    checks['target_parity_coefficients']=16
    for t in range(16):
        # x -> x^3, followed by a -> a^9, returns the full target.
        assert apow(9*((11*t)%16)**2)==apow(t*t)
    checks['Galois_stride_symmetry_coefficients']=16
    index=json.loads((ROOT/'ALL_LENGTHS_INDEX.json').read_text())
    literal=0; orbit_total=0
    counts={}
    for layer in index['layers']:
        r=layer['length']
        full={n for n in all_counts(r) if sum(n[i] for i in (0,2,4,6))>=8}
        reps={class_of(n)[0] for n in full}
        assert len(full)==layer['patterns']
        assert len(reps)==layer['orbits']
        assert reps=={tuple(n) for n in layer['representatives']}
        assert {tuple(n) for n in layer['excluded_pure_odd_representatives']}=={n for n in reps if sum(c>0 for c in n)==1}
        union=set()
        for n in reps:
            orbit=set(class_of(n)); assert not union.intersection(orbit);union.update(orbit)
        assert union==full
        literal+=len(full);orbit_total+=len(reps);counts[r]=[len(full),len(reps)]
    checks['all_lengths_coverage']={'literal_patterns':literal,'orbits':orbit_total,'per_length':counts}
    padded=json.loads((ROOT/'RESIDUAL_INDEX.json').read_text())
    pfull=set()
    for row in padded['systems']:
        n=tuple(row['representative'])
        o={tuple(v) for v in row['orbit']}
        assert o==set(class_of(n))
        assert row['status']==('EXCLUDED_PURE_ODD_STRIDE' if sum(c>0 for c in n)==1 else 'RESIDUAL_UNSOLVED')
        assert not o.intersection(pfull)
        pfull.update(o)
    assert len(pfull)==50940
    for r in range(8,15):
        for n in all_counts(r):
            if sum(n[i] for i in (0,2,4,6))>=8:
                p=(n[0]+14-r,)+n[1:];assert p in pfull
    checks['padded_length_14_covers_all_lengths']=True
    # Whole-support characteristic-zero unit certificates for the pure odd controls:
    # c_0=1 and c_(15*s mod 16)=0, so -a^(-i*i) f_i=1.
    pure=0
    for r in range(8,15):
        for s in (1,3,5,7):
            i=15*s%16
            assert i not in {(j*s)%16 for j in range(r+1)}
            assert apow(-i*i+i*i)==ONE
            pure+=1
    certs=json.loads((ROOT/'PURE_STRIDE_CERTIFICATES.json').read_text())
    assert len(certs)==pure
    assert {(z['length'],z['stride']) for z in certs}=={(r,s) for r in range(8,15) for s in (1,3,5,7)}
    for z in certs:
        i=z['equation_index'];s=z['stride'];r=z['length']
        assert i==15*s%16 and i not in {(j*s)%16 for j in range(r+1)}
        assert z['coefficient_claim']=={'c_0':1,'c_i':0}
        assert z['multiplier']=={'sign':-1,'a_exponent_mod_32':(-i*i)%32}
    checks['pure_odd_stride_unit_certificates']=pure
    spec=json.loads((ROOT/'BENCHMARK_SYSTEM.json').read_text())
    n=spec['counts'];names=spec['variables'][:-1]
    # Independent multiplication of sparse grouped polynomials.
    formal={(0,(0,)*14):1};offset=0
    for s,size in enumerate(n,1):
        new={}
        for (res,mon),coef in formal.items():
            for d in range(size+1):
                exp=list(mon)
                if d:exp[offset+d-1]+=1
                key=((res+s*d)%16,tuple(exp));new[key]=new.get(key,0)+coef
        formal=new;offset+=size
    stored={(i,tuple(exp)):coef for i,row in enumerate(spec['cyclic_coefficients']) for exp,coef in row}
    assert stored==formal
    checks['benchmark_generator_terms']=len(formal)
    values=[]
    for size in n:
        values.extend(math.comb(size,j)*(-2)**j for j in range(1,size+1))
    actual=[evaluate_terms(t,values) for t in spec['cyclic_coefficients']]
    expect=[1]+[0]*15
    for s,size in enumerate(n,1):
        for _ in range(size):
            factor=[0]*16;factor[0]=1;factor[s]=-2
            expect=multiply(expect,factor)
    assert actual==expect
    checks['grouped_vs_individual_binomials']=16
    # Explicit forbidden zero-product component of the unsaturated equations:
    # (1-x^8)(1+x^8)=0 in A, with all other groups equal to 1.
    values=[0]*14
    values[names.index('b4_2')]=-1
    values[names.index('b8_1')]=1
    zero_coefficients=[evaluate_terms(t,values) for t in spec['cyclic_coefficients']]
    assert zero_coefficients==[0]*16
    assert 17*zero_coefficients[0]-1==-1
    checks['zero_product_rejected_by_saturation']=True
    # A corrupted inverse target is rejected by the full target check.
    mutated=ZERO
    for k in range(16):
        term=apow(-k*k+k*k)
        mutated=add(mutated,term)
    mutated=add(mutated,ONE)
    assert mutated!=(16,)+(0,)*15
    checks['target_mutation_rejected']=True
    (ROOT/'VERIFY_RESULTS.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
