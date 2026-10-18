"""Independent exact controls; standard-library correctness oracles only."""
from pathlib import Path
import sys, json, random, hashlib
from math import factorial, comb
from collections import Counter
from itertools import product as tuples
from functools import lru_cache
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'candidate'))
import guarded_sharing as g
R=random.Random(0x1515C0FFEE)
counts=Counter(); transcript=hashlib.sha256()
def record(kind,payload):
    counts[kind]+=1
    transcript.update(json.dumps([kind,payload],sort_keys=True,separators=(',',':')).encode())
def value(c,z):
    ans=0
    for x in reversed(c): ans=ans*z+x
    return ans
def convolution(a,b):
    # Independent output-diagonal oracle.
    return [sum(a[i]*b[k-i] for i in range(max(0,k-len(b)+1),min(len(a)-1,k)+1)) for k in range(len(a)+len(b)-1)]
def polynomial_roots(roots):
    c=[1]
    for z in roots:
        c=[-z*c[0]]+[c[j-1]-z*c[j] for j in range(1,len(c))]+[c[-1]]
    return c

def hankel_controls():
    # Enumerate the Hankel space, rather than all outer products.
    for L in range(1,10):
        accepted=[]; mask=(1<<L)-1
        for anti in range(1,1<<(2*L-1)):
            rows=[(anti>>i)&mask for i in range(L)]
            nonzero={r for r in rows if r}
            if len(nonzero)==1: accepted.append(anti)  # rank one over F2
        expected=sorted(set([1,1<<(2*L-2),(1<<(2*L-1))-1]))
        assert accepted==expected
        assert len(accepted)==(1 if L==1 else 3)
        if L>=3: assert len(accepted)<2*L-1
        record('exhaustive_hankel_spaces',[L,(1<<(2*L-1))-1,accepted])

def interpolation_controls():
    for d in [0,1,2,3,4,7,8,15,16,31,32,64]:
        f=factorial(d); gamma=0
        while f%2==0: f//=2; gamma+=1
        assert gamma==g.guard_for_degree(d)
        for H in [1,3,8,17,65,137]:
            for variant in range(3):
                # Signed representatives substantially wider than either modulus.
                c=[R.randrange(-(1<<(H+gamma+19)),1<<(H+gamma+19)) for _ in range(d+1)]
                if variant==0: c=[(-1)**k*(1<<(H+k%5)) for k in range(d+1)]
                W=H+gamma
                samples=[value(c,j)%(1<<W) for j in range(d+1)]
                stats={}; answer=g.interpolate_consecutive(samples,H,stats)
                assert answer==[x%(1<<H) for x in c]
                assert stats['difference_subtractions']==d*(d+1)//2
                assert stats['basis_small_actions']==d*(d+1)//2
                assert stats['odd_division_steps']==(d+1)*H
                record('signed_wide_interpolations',[d,H,variant,answer])
    for d in [2,3,4,7,8,15,16,31,32,63,64]:
        gamma=g.guard_for_degree(d)
        for H in [1,2,9,65]:
            c=[x*(1<<(H-1)) for x in polynomial_roots(range(d))]
            assert c[-1]%(1<<H)!=0
            for G in range(gamma):
                for z in [-1003,-d-1,-1,0,1,d-1,d,d+1,1009]:
                    assert value(c,z)%(1<<(H+G))==0
                record('all_lower_guards_null_witness',[d,H,G])
            zero=g.interpolate_consecutive([0]*(d+1),H)
            assert zero!=[x%(1<<H) for x in c]
            record('missing_guard_detected',[d,H])

def factorable_controls():
    for L in [2,3,4,5,8,12,17]:
        d=2*L-2; t=factorial(d).bit_length()
        for H in [2*t+2,2*t+3,4*t+7]:
            u=(H-1)//2; v=H-1-u
            a=[x<<u for x in polynomial_roots(range(-L+2,1))]
            b=[x<<v for x in polynomial_roots(range(-2*L+3,-L+2))]
            assert len(a)==len(b)==L and min(a+b)>=0 and max(a+b)<1<<H
            c=convolution(a,b); gamma=g.guard_for_degree(d)
            assert c[-1]%(1<<H)==1<<(H-1)
            for z in [-71,-d-1,-1,0,1,d+1,73]:
                assert value(a,z)*value(b,z)%(1<<(H+gamma-1))==0
            got=g.guarded_convolution(a,b,H)
            assert got==[x%(1<<H) for x in c]
            record('canonical_factorable_witnesses',[L,H,got])

def division_controls():
    for H in [1,2,7,8,9,63,64,65,130,257]:
        for odd in [1,3,13,257,(1<<65)-1,(1<<193)+17]:
            for source in [0,(1<<H)-1,R.randrange(1<<H)]:
                state=[]; q=g.odd_divide_bits(source,odd,H,lambda *x:state.append(x))
                assert (q*odd-source)%(1<<H)==0
                for bit,digit,qbit,old,new in state:
                    assert 0<=new<odd and 2*new==old+odd*qbit-digit
                    assert digit==(source>>bit)&1
                assert len(state)==H
                record('wide_odd_divisions',[H,odd,source,q])
                counts['division_transitions']+=len(state)

def service_controls():
    original_small=g.mul_small; original_div=g.odd_divide_bits
    for L in [1,2,3,4,7,8,13,17]:
        n=2*L-1; gamma=g.guard_for_degree(n-1)
        for H in [1,2,7,16,63,131]:
            W=H+gamma
            a=[R.randrange(1<<W) for _ in range(L)]
            b=[R.randrange(1<<W) for _ in range(L)]
            calls=[]; small_calls=[]; division_calls=[]
            def product(x,y):
                calls.append([x.bit_length(),y.bit_length()]); return g.karatsuba(x,y)
            def small(x,k,w):
                small_calls.append([k,w]); return original_small(x,k,w)
            def divide(x,u,w,trace=None):
                division_calls.append([u,w]); return original_div(x,u,w,trace)
            g.mul_small=small; g.odd_divide_bits=divide
            try: answer=g.guarded_convolution(a,b,H,product=product)
            finally: g.mul_small=original_small; g.odd_divide_bits=original_div
            assert answer==[x%(1<<H) for x in convolution(a,b)]
            assert len(calls)==n and all(max(c)<=W for c in calls)
            assert len(small_calls)==2*n*L+(n-1)+n*(n-1)//2
            assert len(division_calls)==n
            for k,(odd,width) in enumerate(division_calls):
                f=factorial(k)
                while f%2==0: f//=2
                assert odd==f and width==H
            # Independent W-bit lifts of same H-bit classes preserve full output.
            aa=[x%(1<<H)+R.randrange(1<<gamma)*(1<<H) for x in a]
            bb=[x%(1<<H)+R.randrange(1<<gamma)*(1<<H) for x in b]
            assert g.guarded_convolution(aa,bb,H)==answer
            record('instrumented_guarded_services',[L,H,len(calls),len(small_calls),answer])
    for H in [1,2,3,7,8,65,129]:
        cases=[]
        for i in range(3):
            for j in range(3):
                a=[0]*3;b=[0]*3;a[i]=1;b[j]=1;cases.append((a,b))
        for _ in range(11): cases.append(([R.randrange(1<<H) for _ in range(3)],[R.randrange(1<<H) for _ in range(3)]))
        for a,b in cases:
            calls=[]
            def product(x,y): calls.append((x,y));return g.karatsuba(x,y)
            answer=g.six_product_three(a,b,H,product=product)
            assert len(calls)==6
            assert answer==[x%(1<<H) for x in convolution(a,b)]
            record('six_product_basis_and_random',[H,a,b,answer])

def image_controls():
    for L in [1,2,3,4,7,8,16]:
        for m,H in [(1,1),(1,7),(3,3),(3,9),(6,13)]:
            # A random nonzero mod-2 linear form on the Taylor vector pulls back
            # to a form with at least one odd coefficient on the chunk vector.
            ell=[R.randrange(1<<H) for _ in range(L)]
            ell[R.randrange(L)]|=1
            coeff=[sum(ell[j]*comb(i,j) for j in range(i+1))%(1<<H) for i in range(L)]
            oddindex=next(i for i,c in enumerate(coeff) if c&1)
            images={(coeff[oddindex]*x)%(1<<H) for x in range(1<<m)}
            assert len(images)==1<<m
            record('bounded_image_capacity',[L,m,H,oddindex])

def integrated_controls():
    for m,L in [(2,1),(2,9),(3,13),(7,17),(16,11),(65,7),(130,5),(257,3)]:
        limit=1<<(m*L)
        for x,y in [(0,limit-1),(limit-1,limit-1),(1,limit-1),(R.randrange(limit),R.randrange(limit)),(R.randrange(limit),R.randrange(limit))]:
            stats={}; answer=g.multiply_guarded_interface(x,y,m,L,stats=stats)
            a=[(x>>(m*i))&((1<<m)-1) for i in range(L)]
            b=[(y>>(m*i))&((1<<m)-1) for i in range(L)]
            assert answer==x*y and stats['final_coefficients']==convolution(a,b)
            W=stats['W_forward'];H=stats['H_final'];n=2*L-1
            c=[sum(a[i]*comb(i,j) for i in range(j,L)) for j in range(L)]
            d=[sum(b[i]*comb(i,j) for i in range(j,L)) for j in range(L)]
            assert max(c+d)<1<<W
            observed=max(max((value(c,j)%(1<<W)).bit_length(),(value(d,j)%(1<<W)).bit_length()) for j in range(n))
            assert observed==stats['maximum_sample_bits'] and observed<=stats['sample_capacity']
            record('complete_default_backend_products',[m,L,x,y,answer,observed])

def schedule_controls():
    threshold=16
    for exponent in [7,10,13,16,19,22]:
        N=1<<exponent
        for beta in [0,1,2]:
            for guard in [0,1,2]:
                @lru_cache(None)
                def tree(v):
                    if v<=threshold: return (v,1,0)
                    L=max(2,min(v-1,(v.bit_length()-1)**beta))
                    h=min(v-1,(v+L-1)//L+guard)
                    assert h*L>=v and h<=v and 2*(2*L-1)*h>=3*v
                    volume,leaves,depth=tree(h)
                    return ((2*L-1)*volume,(2*L-1)*leaves,depth+1)
                volume,leaves,D=tree(N)
                Lmax=max(2,exponent**beta)
                assert N<=threshold*(Lmax**D)
                assert volume*(2**D)>=N*(3**D)
                record('finite_full_expansion_schedules',[N,beta,guard,volume,leaves,D])


def canonical_small_width_scope_control():
    # All integer values modulo q depend only on the node modulo q. For H=1,
    # L=4 this exhaustively proves guard 3 sufficient although Gamma(6)=4.
    L=4; rows=[]; arrays=list(tuples(range(2),repeat=L))
    for G in range(5):
        modulus=1<<(1+G); seen={}; collision=None; checked=0
        for a in arrays:
            for b in arrays:
                coefficients=tuple(x%2 for x in convolution(a,b))
                samples=tuple(value(a,z)*value(b,z)%modulus for z in range(modulus))
                previous=seen.get(samples)
                checked+=1
                if previous is not None and previous['coefficients']!=coefficients:
                    collision=[previous,{'coefficients':coefficients,'left':a,'right':b}]
                    break
                seen[samples]={'coefficients':coefficients,'left':a,'right':b}
            if collision is not None: break
        assert (collision is None)==(G>=3)
        row={'H':1,'L':L,'Gamma':4,'guard':G,'checked_input_pairs':checked,'collision':collision,'unique_sample_signatures':len(seen)}
        rows.append(row); record('canonical_small_width_scope_controls',row)
    (ROOT/'SMALL_WIDTH_SCOPE_COUNTERCONTROL.json').write_text(json.dumps({'status':'PASS','result':'For canonical H=1, L=4 factors, the sample-only minimum uniform guard is 3, less than Gamma(6)=4.','periodicity':'Polynomial values modulo q are periodic in the integer node with period q, so the complete residue-node signatures cover every integer node.','controls':rows},indent=2)+'\n')

if __name__=='__main__':
    hankel_controls(); interpolation_controls();factorable_controls();division_controls();service_controls();image_controls();integrated_controls();schedule_controls();canonical_small_width_scope_control()
    result={'status':'PASS','counts':dict(counts),'digest':transcript.hexdigest(),'scope':'Finite independent controls, not proofs of asymptotic complexity.'}
    (ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
