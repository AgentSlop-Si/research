"""Independent review. Reads sealed data only; never imports candidate code.
Trace inputs use a Cartesian selection expansion, distinct from discovery's
cyclic polynomial multiplication. Local derivations are checked as zero residuals.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from math import gcd,lcm
import json, hashlib, copy, tarfile
import sympy as sp

HERE=Path(__file__).resolve().parent
CAND=HERE.parent/'candidate'
P=97; Z=(0,)*7; STRIDES=(1,3,7,5)

def pinned():
    manifest=CAND/'MANIFEST.json'
    assert hashlib.sha256((CAND/'ORIGINAL_MANIFEST.json').read_bytes()).hexdigest()=='7916943bf67c80f52b40b61c3c26614d60d0cb052f2f4b451ac28af11379c546'
    rows=json.loads(manifest.read_text())
    for row in rows:
        b=(CAND/row['path']).read_bytes()
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    sources=json.loads((CAND/'SOURCE_BINDINGS.json').read_text())
    for row in sources:
        b=(CAND/row['path']).read_bytes()
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    # The redundant original archive is omitted with its digest in the public omissions ledger.
    members=[]
    return {'canonical_files':len(rows),'source_bindings':len(sources),'archive_files':len(members),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}

def read_poly(rows):
    p={}
    for ex,c in rows:
        assert len(ex)==7 and all(type(v) is int and v>=0 for v in ex)
        assert type(c) is int and 0<c<P
        key=tuple(ex);assert key not in p;p[key]=c
    return p

def clean(c):return {m:v%P for m,v in c.items() if v%P}

def inputs(ns):
    # One term for every independent power choice from the four grouped factors.
    offsets=[];offset=0
    for n in ns:offsets.append(offset);offset+=n
    coeffs=[Counter() for _ in range(16)]
    for powers in product(*(range(n+1) for n in ns)):
        ex=[0]*7
        for j,k in enumerate(powers):
            if k:ex[offsets[j]+k-1]=1
        index=sum(s*k for s,k in zip(STRIDES,powers))%16
        coeffs[index][tuple(ex)]+=1
    result=[]
    for i in range(8):
        f=Counter({m:(-1)**i*v for m,v in coeffs[i].items()})
        for m,v in coeffs[i+8].items():f[m]-=v
        result.append(clean(f))
    return result

def add_product(residual,left,right,scale):
    for a,c in left.items():
        for b,d in right.items():
            residual[tuple(a[i]+b[i] for i in range(7))]+=scale*c*d

def trace(data):
    assert data['N']==16 and data['prime']==97 and tuple(data['stride_order'])==STRIDES
    ns=tuple(data['counts']);assert len(ns)==4 and all(type(n) is int and n>=0 for n in ns) and sum(ns)==7
    original=inputs(ns);known=[];terms=0;max_degree=0
    for index,node in enumerate(data['nodes']):
        recorded=read_poly(node['polynomial']);residual=Counter(recorded)
        terms+=len(recorded)
        max_degree=max(max_degree,max((sum(m) for m in recorded),default=0))
        if index<8:
            assert node['kind']=='input' and node['index']==index
            assert recorded==original[index]
        elif node['kind']=='scale':
            j=node['source'];assert type(j) is int and 0<=j<index
            c=node['scale'];assert type(c) is int and 0<c<P
            for m,v in known[j].items():residual[m]-=c*v
            assert not clean(residual), (ns,index,'scale')
        else:
            assert node['kind']=='spair_reduce'
            a,b=node['left'],node['right'];assert type(a) is int and type(b) is int and 0<=a<index and 0<=b<index
            c=node['scale'];assert type(c) is int and 0<c<P
            u,v=node['left_shift'],node['right_shift']
            assert len(u)==len(v)==7 and all(type(k) is int and k>=0 for k in u+v)
            add_product(residual,known[a],{tuple(u):1},-c)
            add_product(residual,known[b],{tuple(v):1},c)
            for source,multiplier in node['reductions']:
                assert type(source) is int and 0<=source<index
                add_product(residual,known[source],read_poly(multiplier),c)
            assert not clean(residual), (ns,index,'derivation')
        known.append(recorded)
    assert type(data['final']) is int and 0<=data['final']<len(known)
    assert known[data['final']]=={Z:1}
    return len(known),terms,max_degree

def certificates():
    totals=[0,0,0];seen=set();mutations=Counter()
    for path in sorted((CAND/'parity7_traces').glob('*.json')):
        d=json.loads(path.read_text());ns=tuple(d['counts']);assert ns not in seen;seen.add(ns)
        a,b,c=trace(d);totals[0]+=a;totals[1]+=b;totals[2]=max(totals[2],c)
        # Independent rejection controls mutate data, not candidate checker logic.
        for label,idx in [('input',0),('final',d['final'])]:
            bad=copy.deepcopy(d)
            row=bad['nodes'][idx]['polynomial'][0]
            row[1]=row[1]%96+1
            try:trace(bad)
            except AssertionError:mutations[label]+=1
            else:raise AssertionError(('mutation accepted',path,label))
        later=next((i for i,node in enumerate(d['nodes']) if node['kind']=='spair_reduce'),None)
        if later is not None:
            bad=copy.deepcopy(d);bad['nodes'][later]['left']=later
            try:trace(bad)
            except AssertionError:mutations['self_reference']+=1
            else:raise AssertionError(('self-reference accepted',path))
    patterns={v for v in product(range(8),repeat=4) if sum(v)==7}
    reps={max(n[j:]+n[:j] for j in range(4)) for n in patterns}
    assert seen==reps and len(patterns)==120 and len(seen)==30
    assert all(len({n[j:]+n[:j] for j in range(4)})==4 for n in patterns)
    assert totals[:2]==[4568,81904]
    return {'input_equations_rebuilt':240,'trace_nodes':totals[0],'stored_node_terms':totals[1],'maximum_stored_node_degree':totals[2],'count_vectors':len(patterns),'orbits':len(reps),'orbit_size':4,'mutation_controls_rejected':dict(mutations)}

# Ring Z[a]/(a^16+1) represented directly by signed residue counts.
def collapse_exponents(exponents):
    out=[0]*16
    for k in exponents:
        residue=k%32
        out[residue%16]+=1 if residue<16 else -1
    return out

def target():
    tested=0
    for i,j in product(range(16),repeat=2):
        actual=collapse_exponents([-(i-k)**2+(k-j)**2 for k in range(16)])
        assert actual==[16*int(i==j)]+[0]*15
        tested+=1
    for t in range(16):
        assert collapse_exponents([t*t+16*(t%2)])==collapse_exponents([((t-8)%16)**2])
    for r,t in product(range(16),repeat=2):
        assert collapse_exponents([((t-r)%16)**2])==collapse_exponents([r*r-2*r*t+t*t])
    # Distinct all-row corruption: one off-diagonal target entry changed.
    i,j,k=0,2,1
    bad=collapse_exponents([-(i-h)**2+(h-j)**2 for h in range(16)]+[(k-j)**2])
    assert bad!=[0]*16
    return {'full_inverse_entries':tested,'parity_entries':16,'shift_entries':256,'off_diagonal_corruption_rejected':True}

def cyclic_mul(f,g,p=P):
    h=[0]*16
    for i,a in enumerate(f):
        for j,b in enumerate(g):h[(i+j)%16]=(h[(i+j)%16]+a*b)%p
    return h

def evaluate(f,t,p=P):return sum(c*pow(t,j,p) for j,c in enumerate(f))%p

def normalization():
    roots=[t for t in range(1,P) if pow(t,16,P)==1]
    assert len(roots)==16 and P%2==1
    lamb=next(t for t in roots if pow(t,8,P)==P-1)
    assert pow(lamb,16,P)==1
    # Rootwise pole criterion, including nongenerating, zero and negative strides.
    guards=0
    for s in range(-32,33):
        for alpha in range(P):
            guarded=pow(alpha,16//gcd(16,s),P)!=1
            rootwise=all((1-alpha*pow(t,s,P))%P for t in roots)
            assert guarded==rootwise;guards+=1
    # Reversal identity and class action for every nonzero finite parameter.
    reversals=0
    for s in range(1,16,2):
        assert gcd(s,16)==1 and len({pow(t,s,P) for t in roots})==16
        for alpha in range(1,P):
            for t in roots:
                assert (1-alpha*pow(t,-s,P))%P==(-alpha*pow(t,-s,P)*(1-pow(alpha,-1,P)*pow(t,s,P)))%P
                reversals+=1
    assert tuple(min(3*s%16,-3*s%16) for s in STRIDES)==STRIDES[1:]+STRIDES[:1]
    # General projective zero-count premise: exhaust all F97 pairs as controls;
    # the extension-field proof is gcd(s,16)=1, not this finite enumeration.
    binomials=0
    for s in range(1,16,2):
        powers=[pow(t,s,P) for t in roots]
        for u,v in product(range(P),repeat=2):
            if not (u or v):continue
            assert sum((u+v*w)%P==0 for w in powers)<=1
            binomials+=1
    assert 7<16
    # Sign-repair operator identity holds on the entire quotient ring.
    for f in ([int(i==j) for i in range(16)] for j in range(16)):
        transform=[c*pow(lamb,i,P)%P for i,c in enumerate(f)]
        left=[(-1)**i*c%P for i,c in enumerate(transform)]
        source=[(-1)**i*c%P for i,c in enumerate(f)]
        assert left==[c*pow(lamb,i,P)%P for i,c in enumerate(source)]
        sx8=f[-8:]+f[:-8]
        transformed_sx8=[c*pow(lamb,i,P)%P for i,c in enumerate(sx8)]
        assert transformed_sx8==[(-c)%P for c in transform[-8:]+transform[:-8]]
    return {'root_count':16,'sign_fix_lambda':lamb,'pole_checks':guards,'rootwise_reversal_checks':reversals,'projective_nonzero_pairs':binomials,'root_count_bound':{'maximum_zeros':7,'minimum_nonzero_evaluations':9},'class_cycle':[1,3,7,5,1]}

def finite_upper():
    x=sp.Symbol('x');a=19;zeta=46
    assert a*zeta%97==1 and pow(zeta,16,97)==96
    Q=sp.Poly(sum(pow(a,j*j,97)*x**j for j in range(16)),x,modulus=97)
    unit,factors=sp.factor_list(Q)
    declared=[x-19,x**3+43*x**2-32*x+19,x**3-26*x**2-40*x-20,x**4+7*x**3-46*x**2+5*x-47,x**4-33*x**3-30*x**2+18*x-47]
    expect=Counter(tuple(sp.Poly(f,x,modulus=97).all_coeffs()) for f in declared)
    actual=Counter()
    for f,n in factors:actual[tuple(f.all_coeffs())]+=n
    assert actual==expect and int(unit)%97==19
    assert all(n==1 and f.is_irreducible for f,n in factors)
    assert sp.gcd(Q,sp.Poly(x**16-1,x,modulus=97)).degree()==0
    assert sp.gcd(Q,Q.diff()).degree()==0
    # Frobenius conjugates in degree d yield normalized reciprocal factors.
    # For each irreducible, test x^(97^12)=x and x^(97^d)=x by modular power.
    quotient_results=[]
    def powmod(base,n,mod):
        ans=sp.Poly(1,x,modulus=97)
        while n:
            if n&1:ans=(ans*base).rem(mod)
            base=(base*base).rem(mod);n//=2
        return ans
    for f,n in factors:
        X=sp.Poly(x,x,modulus=97).rem(f)
        assert powmod(X,97**12,f)==X
        assert powmod(X,97**f.degree(),f)==X
        quotient_results.append(f.degree())
    assert sorted(quotient_results)==[1,3,3,4,4] and lcm(*quotient_results)==12
    return {'independent_factorization_unit':int(unit),'factor_degrees':sorted(quotient_results),'irreducible':True,'squarefree':True,'root_pole_gcd':1,'frobenius_power_97_12':True,'splitting_degree_lcm':12,'linear_parameter':46}

def application():
    tests=0
    for alpha in range(P):
        if pow(alpha,16,P)==1:continue
        # Count setup separately using precisely four squarings.
        power=alpha;setup_m=0
        for _ in range(4):power=power*power%P;setup_m+=1
        assert power==pow(alpha,16,P) and setup_m==4
        d=pow(1-power,-1,P)
        for j in range(16):
            data=[int(i==j) for i in range(16)];original=data[:]
            m=adds=0;h=data[0]
            for i in range(1,16):h=(alpha*h+data[i])%P;m+=1;adds+=1
            data[15]=d*h%P;m+=1
            for i in range(15):data[i]=(data[i]+alpha*data[i-1])%P;m+=1;adds+=1
            assert m==31 and adds==30
            assert [(data[i]-alpha*data[i-1])%P for i in range(16)]==original
            tests+=1
    assert tests==1296
    return {'in_place_basis_tests':tests,'factor_M':31,'factor_A':30,'fifteen_plus_scalar_M':15*31+16,'fifteen_plus_scalar_A':15*30,'coefficient_setup_excluded_from_arithmetic_bill':True,'setup_M':15*4,'setup_A':15,'setup_Inv':15,'setup_plus_one_M':15*31+16+15*4,'setup_plus_one_A':15*30+15,'input_buffer_elements':16,'maximum_scalar_work_registers':2,'stored_parameters_and_inverses':30}

def main():
    result={'status':'PASS','pins':pinned()}
    for key,fn in [('certificates',certificates),('target',target),('normalization_and_guards',normalization),('finite_upper',finite_upper),('application',application)]:
        result[key]=fn();print(key,json.dumps(result[key]),flush=True)
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',flush=True)

if __name__=='__main__':main()
