"""Fresh exact controls for the order-3q interior proof. No research code imported."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import sympy as sp
from sympy.polys.matrices import DomainMatrix

OUT = Path(__file__).resolve().parent
X = sp.Symbol('X')

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

class Roots:
    """Exact integer remainders of powers modulo the actual Phi_N."""
    def __init__(self, n):
        self.n = n
        self.phi = list(reversed([int(c) for c in sp.Poly(sp.cyclotomic_poly(n, X), X).all_coeffs()]))
        self.degree = len(self.phi) - 1
        self.zero = (0,) * self.degree
        self.powers = [self.reduce([0] * e + [1]) for e in range(n)]
    def reduce(self, p):
        p = list(p)
        for e in range(len(p)-1, self.degree-1, -1):
            c = p[e]
            for j, a in enumerate(self.phi):
                p[e-self.degree+j] -= c*a
        return tuple((p + [0]*self.degree)[:self.degree])
    def sum(self, exponents):
        a = [0]*self.degree
        for e in exponents:
            for j,c in enumerate(self.powers[e%self.n]):
                a[j] += c
        return tuple(a)

def divisor_mask(n, d):
    return [[int(r//d == c%(n//d)) for c in range(n)] for r in range(n)]

def grams(mask, d, q=None):
    n=len(mask); roots=Roots(n)
    assert set(map(sum,mask)) == {d}
    assert {sum(mask[r][c] for r in range(n)) for c in range(n)} == {d}
    result={}
    for order in ('row','column'):
        failures=[]; zeros={}; nonzeros={}
        for i in range(n):
            for j in range(n):
                if order=='row':
                    exponents=[(i-j)*k for k in range(n) if mask[i][k] and mask[j][k]]
                else:
                    exponents=[(j-i)*k for k in range(n) if mask[k][i] and mask[k][j]]
                residue=roots.sum(exponents)
                expected=(d,)+(0,)*(roots.degree-1) if i==j else roots.zero
                if i != j:
                    charorder=n//math.gcd(i-j,n)
                    target=zeros if residue==roots.zero else nonzeros
                    target[str(charorder)]=target.get(str(charorder),0)+1
                if residue != expected:
                    failures.append({'indices':[i,j], 'character_order':n//math.gcd(i-j,n),
                                     'overlap_size':len(exponents), 'residue':list(residue)})
        result[order]={'entries_checked':n*n,'zero_off_diagonal_by_order':zeros,
                       'nonzero_off_diagonal_by_order':nonzeros,'failures':failures}
    if q is not None:
        assert not any(f['character_order']==q for f in result['row']['failures'])
    return result

def from_crt(q, supports):
    n=3*q
    return [[int((c%3,c%q) in supports[(r%3,r%q)]) for c in range(n)] for r in range(n)]

def counter_mask(q, kind):
    supports={}
    if kind=='all_clique_q_plus_2':
        for a in range(3):
            for b in range(q):
                supports[a,b]={(a,v) for v in range(q)}|{((a+1)%3,b),((a+2)%3,(b+1)%q)}
        d=q+2
    elif kind=='balanced_all_split_q_plus_1':
        n=(q-1)//2
        for a in range(3):
            for b in range(q):
                u=a if b<n else (a+1)%3
                supports[a,b]={(u,v) for v in range(q)}|{((a+2)%3,b)}
        d=q+1
    elif kind=='two_single_cliques_q_plus_1':
        for a in range(2):
            for b in range(q):
                supports[a,b]={(a,v) for v in range(q)}|{(2,b)}
        for b in range(q-1):
            supports[2,b]={(2,v) for v in range(q)}|{(0,b)}
        supports[2,q-1]={(1,v) for v in range(q)}|{(0,q-1)}
        d=q+1
    elif kind=='singleton_empty_fiber_q_plus_1':
        # At each group: big clique q-1, singleton with weights 0,2,2,1,...,1.
        # Every fiber contributes q-1,1,1, but the singleton has no q-line.
        for a in range(3):
            extra=[((a+1)%3,0),((a+2)%3,0)]+[((a+1)%3,v) for v in range(3,q)]
            for b in range(q-1):
                supports[a,b]={(a,v) for v in range(q)}|{extra[b]}
            supports[a,q-1]={((a+i)%3,v) for i in (1,2) for v in (1,2)}|{((a+2)%3,v) for v in range(3,q)}
        d=q+1
    else:
        raise ValueError(kind)
    return from_crt(q,supports),d

def local_families(n):
    """Unordered fiber restrictions for a component of n rows."""
    if n==1:
        return [(m,) for m in range(8)]
    return [v for v in itertools.combinations_with_replacement(range(1,8),n)
            if all((v[i]&v[j]).bit_count()==1 for i in range(n) for j in range(i))]

def local_controls():
    records=[]
    fam={n:local_families(n) for n in range(1,14)}
    for q in (5,7,11,13):
        clique_count=0
        for vs in fam[q]:
            common=7
            union=0
            for v in vs: common&=v; union|=v
            assert common.bit_count()==1
            assert sum(v.bit_count() for v in vs)==q+union.bit_count()-1 <= q+2
            clique_count+=1
        splits=[]
        for n in range(1,q//2+1):
            m=q-n; admissible=0; saturated=0; singleton_weights=set()
            for left in fam[n]:
                lu=0
                for v in left:lu|=v
                for right in fam[m]:
                    ru=0
                    for v in right:ru|=v
                    if lu&ru: continue
                    incidence=sum(v.bit_count() for v in left+right)
                    assert incidence<=q+1
                    # A nonsingleton row can still be a tripleton locally.
                    # Its exclusion requires the global one-extra row budget.
                    if n==1: assert left[0]!=7
                    for size,vs,u in ((n,left,lu),(m,right,ru)):
                        assert sum(v.bit_count() for v in vs)==size+u.bit_count()-1
                    if incidence==q+1:
                        saturated+=1
                        counts=[sum(bool(v&(1<<j)) for v in left+right) for j in range(3)]
                        assert sorted(counts)==sorted([n,m,1])
                        if n==1: singleton_weights.add(left[0].bit_count())
                    admissible+=1
            splits.append({'component_sizes':[n,m],'admissible_local_multisets':admissible,
                           'saturated_multisets':saturated,'singleton_fiber_weights':sorted(singleton_weights)})
        records.append({'q':q,'single_clique_multisets':clique_count,'split_cases':splits})
    # Every possible labeled q=5 fiber: a nonsimplicial vertex has weight at least 2.
    tested=0; eligible=0
    for vs in itertools.product(range(8), repeat=5):
        tested+=1
        if any((vs[i]&vs[j]).bit_count()>1 for i in range(5) for j in range(i)):continue
        eligible+=1
        for r in range(5):
            neighbors=[s for s in range(5) if s!=r and vs[r]&vs[s]]
            if any(not(vs[s]&vs[t]) for s,t in itertools.combinations(neighbors,2)):
                assert vs[r].bit_count()>=2
    # Explicit q=5 global-row-budget check for the delicate singleton + K4 case.
    patterns=set()
    for left in fam[1]:
        for right in fam[4]:
            ru=0
            for v in right:ru|=v
            if left[0]&ru or sum(v.bit_count() for v in left+right)!=6:continue
            for perm in set(itertools.permutations(right)):
                patterns.add(tuple(v.bit_count() for v in left+perm))
    states={((0,0,0,0,0),False)}
    layer_counts=[]
    for layer in range(5):
        nxt=set()
        for weights,had_triple in states:
            for pattern in patterns:
                weights2=tuple(a+b for a,b in zip(weights,pattern))
                if max(weights2)>6:continue
                nxt.add((weights2,had_triple or 3 in pattern))
        states=nxt;layer_counts.append(len(states))
    terminal=[flag for weights,flag in states if weights==(6,6,6,6,6)]
    assert terminal==[False]
    return {'component_census':records,'q5_labeled_fibers_tested':tested,'eligible_q5_labeled_fibers':eligible,
            'q5_singleton_global_budget':{'patterns':len(patterns),'layer_states':layer_counts,
                                         'no_terminal_tripleton':True}}

def cancellation_controls():
    q=5;n=15;roots=Roots(n);vanishing=[]
    for mask in range(1<<n):
        support=[c for c in range(n) if mask>>c&1]
        if roots.sum(support)==roots.zero:
            fibers=all(len([c for c in support if c%q==v]) in (0,3) for v in range(q))
            lines=all(len([c for c in support if c%3==u]) in (0,q) for u in range(3))
            assert fibers or lines
            vanishing.append(mask)
    small_count=0
    for q in (5,7,11,13,17):
        n=3*q;roots=Roots(n)
        for h in range(1,n):
            for size in (1,2):
                for subset in itertools.combinations(range(n),size):
                    assert roots.sum(h*c for c in subset)!=roots.zero
                    small_count+=1
    return {'q5_binary_supports_tested':1<<15,'q5_vanishing_binary_supports':vanishing,
            'small_nonempty_overlap_nonvanishing_checks':small_count}

def original_model(n,d,mask):
    """Construct, invert, and verify in Q[z]/Phi_N using a standard algebraic field."""
    field=sp.QQ.algebraic_field(sp.CRootOf(sp.cyclotomic_poly(n,X),0))
    z=field.unit; power=[z**e for e in range(n)]; zero=field.zero;one=field.one
    def dm(rows):return DomainMatrix(rows,(n,n),field)
    def star(A):
        vals=A.to_list()
        def conjugate(v):
            ans=zero
            for c in v.to_list():ans=ans*power[-1]+field.convert(c)
            return ans
        return dm([[conjugate(vals[c][r]) for c in range(n)] for r in range(n)])
    H=dm([[power[r*c%n] for c in range(n)] for r in range(n)])
    D=dm([[power[r*c%n] if mask[r][c] else zero for c in range(n)] for r in range(n)])
    I=dm([[one if r==c else zero for c in range(n)] for r in range(n)])
    assert D*star(D)==I.scalarmul(field.convert(d))
    assert star(D)*D==I.scalarmul(field.convert(d))
    B=star(H-D).scalarmul(field.convert(sp.Rational(1,n-d)))
    M=B.inv();E=M-H
    assert B*M==I and M*B==I
    assert E*star(E)==I.scalarmul(field.convert(d))
    assert star(E)*E==I.scalarmul(field.convert(d))
    rows=B.to_list()
    assert {sum(v!=zero for v in row) for row in rows}=={n-d}
    assert {sum(rows[r][c]!=zero for r in range(n)) for c in range(n)}=={n-d}
    def encode(A):return [[[str(v) for v in c.to_list()] for c in row] for row in A.to_list()]
    return {'N':n,'d':d,'s':n-d,'coefficient_convention':'descending rational coefficients modulo Phi_N',
            'support_rows':[[c for c in range(n) if mask[r][c]] for r in range(n)],
            'B_tilde':encode(B),'M_tilde':encode(M),'E_tilde':encode(E),
            'both_mask_Grams':True,'both_inverse_products':True,'both_error_Grams':True,
            'all_inverse_row_and_column_supports':n-d,'normalized_squared_error':str(sp.Rational(d,n))}

def main():
    results={'historical_or_candidate_research_code_executed':False,'external_writes':False,
             'arithmetic':'integer cyclotomic remainders and SymPy rational algebraic fields'}
    crt=[]
    for q in (5,7,11,13,17):
        n=3*q;e3=q*pow(q,-1,3);eq=3*pow(3,-1,q);count=0
        for t in range(1,n):
            if math.gcd(t,n)!=1:continue
            for r in range(n):
                for c in range(n):
                    assert (t*r*c-t*((r%3)*(c%3)*e3+(r%q)*(c%q)*eq))%n==0
                    count+=1
        crt.append({'q':q,'primitive_multiplier_phase_checks':count})
    results['CRT']=crt
    results['local']=local_controls(); print('Local component controls passed',flush=True)
    results['cancellation']=cancellation_controls(); print('Cancellation controls passed',flush=True)
    positives=[]
    for n in (15,21,33):
        for d in (1,3,n//3,n):
            R=divisor_mask(n,d);checked=grams(R,d)
            assert all(not checked[k]['failures'] for k in checked)
            positives.append({'N':n,'d':d,'support_rows':[[c for c in range(n) if R[r][c]] for r in range(n)],'Grams':checked})
    # The connected order-eight mask and its odd CRT lift are immutable data inputs.
    baseline=Path('/workspace/shared/sparse_threeq_endpoint_20261019_1054/POSITIVE_CONTROLS.json')
    data=json.loads(baseline.read_text())
    for rec in data:
        if rec['n'] not in (8,24):continue
        n,d=rec['n'],rec['d'];R=rec['R']
        checked=grams(R,d);assert all(not checked[k]['failures'] for k in checked)
        reached={0};frontier={0}
        while frontier:
            nxt=set()
            for node in frontier:
                nxt.update(n+c for c in range(n) if node<n and R[node][c])
                nxt.update(r for r in range(n) if node>=n and R[r][node-n])
            frontier=nxt-reached;reached|=frontier
        assert len(reached)==2*n
        positives.append({'N':n,'d':d,'support_rows':[[c for c in range(n) if R[r][c]] for r in range(n)],
                          'Grams':checked,'support_connected':True})
    assert len(positives)==14
    write('POSITIVE_MASKS.json',positives)
    negatives=[]
    for q in (5,7,11,13):
        for kind in ('all_clique_q_plus_2','balanced_all_split_q_plus_1','two_single_cliques_q_plus_1','singleton_empty_fiber_q_plus_1'):
            R,d=counter_mask(q,kind);checked=grams(R,d,q)
            assert all(checked[k]['failures'] for k in checked)
            negatives.append({'q':q,'N':3*q,'d':d,'kind':kind,
                              'support_rows':[[c for c in range(3*q) if R[r][c]] for r in range(3*q)],'Grams':checked})
    write('NEGATIVE_CONTROLS.json',negatives);print('Full-mask controls passed',flush=True)
    witnesses=[]
    for n,d in ((15,1),(15,3),(15,5),(21,7)):
        witnesses.append(original_model(n,d,divisor_mask(n,d)))
        print('Original model passed',n,d,flush=True)
    for rec in positives:
        if rec['N']==8:
            R=[[int(c in rec['support_rows'][r]) for c in range(8)] for r in range(8)]
            witnesses.append(original_model(8,4,R));print('Connected original model passed',flush=True)
    write('ORIGINAL_MODEL_WITNESSES.json',witnesses)
    results['positive_mask_count']=len(positives);results['negative_mask_count']=len(negatives)
    results['original_model_count']=len(witnesses)
    results['full_Gram_entries_each_order']=sum(r['N']**2 for r in positives+negatives)
    results['inverse_product_entries_each_order']=sum(r['N']**2 for r in witnesses)
    results['error_Gram_entries_each_order']=sum(r['N']**2 for r in witnesses)
    results['data_source']={'path':str(baseline),'sha256':hashlib.sha256(baseline.read_bytes()).hexdigest()}
    write('INDEPENDENT_RESULTS.json',results)
    print(json.dumps({k:results[k] for k in ('positive_mask_count','negative_mask_count','original_model_count','full_Gram_entries_each_order')},indent=2),flush=True)

if __name__=='__main__':main()
