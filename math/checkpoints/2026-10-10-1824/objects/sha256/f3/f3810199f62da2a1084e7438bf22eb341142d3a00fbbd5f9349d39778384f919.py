"""Independent exact audit. Reads predecessor JSON strictly as inert data.
No predecessor Python is imported or executed. Gaussian rows are rebuilt by
q-Pascal recursion; inverse residues are solved by quotient multiplication.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
AUTHOR = ROOT / 'research_cycle_1810/direct_axis_guard'
t = S.symbols('t')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def clean(a, p):
    a = [v % p for v in a]
    while a and a[-1] == 0:
        a.pop()
    return a

def remainder(a, b, p):
    a, b = clean(a, p), clean(b, p)
    inv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        offset = len(a) - len(b)
        multiple = a[-1] * inv % p
        a = clean([v - (multiple * b[i-offset] if offset <= i < offset + len(b) else 0)
                   for i, v in enumerate(a)], p)
    return a

def multiply(a, b, p):
    v = [0] * max(0, len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            v[i+j] += x*y
    return clean(v,p)

def poly_gcd(a, b, p):
    a, b = clean(a,p), clean(b,p)
    while b:
        a, b = b, remainder(a,b,p)
    return [v * pow(a[-1], -1, p) % p for v in a] if a else []

def divide_one(g, p):
    # Synthetic division, ascending coefficient representation.
    assert sum(g) % p == 0
    q = [0] * (len(g)-1)
    q[-1] = g[-1] % p
    for j in range(len(q)-2, -1, -1):
        q[j] = (g[j+1] + q[j+1]) % p
    assert (g[0]+q[0]) % p == 0
    return q

def echelon(matrix, p, reduced=False):
    a = [[v % p for v in row] for row in matrix]
    pivots = []
    if not a:
        return a, pivots
    r = 0
    for j in range(len(a[0])):
        nonzero = next((i for i in range(r,len(a)) if a[i][j]), None)
        if nonzero is None:
            continue
        a[r], a[nonzero] = a[nonzero], a[r]
        inv = pow(a[r][j], -1, p)
        a[r] = [v*inv % p for v in a[r]]
        rows = range(len(a)) if reduced else range(r+1,len(a))
        for i in rows:
            if i != r and a[i][j]:
                mult = a[i][j]
                a[i] = [(x-mult*y) % p for x,y in zip(a[i],a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    return a, pivots

def rank(matrix,p):
    return len(echelon(matrix,p)[1])

def determinant(matrix,p):
    a = [[v % p for v in row] for row in matrix]
    answer = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            answer *= -1
        answer = answer * a[j][j] % p
        inv = pow(a[j][j],-1,p)
        for i in range(j+1,len(a)):
            mult = a[i][j] * inv % p
            for k in range(j+1,len(a)):
                a[i][k] = (a[i][k]-mult*a[j][k]) % p
            a[i][j] = 0
    return answer % p

def quotient_powers(g, N, p):
    m = len(g)-1
    powers = []
    v = [1] + [0]*(m-1)
    for _ in range(N):
        powers.append(v)
        high = v[-1]
        v = [(-high*g[0]) % p] + [(v[j-1]-high*g[j]) % p for j in range(1,m)]
    return powers

def axis_matrix(g,N,p):
    v = quotient_powers(g,N,p)
    return [v[j] + [1] + v[(-j) % N] for j in range(N)]

def inverse_rhs(g,N,p):
    # Solve H(t)R(t)=g(0)S_N(t) in F_p[t]/g by coefficient elimination,
    # independently of the author's extended-Euclidean inverse routine.
    m = len(g)-1
    h = list(reversed(g))
    columns = [remainder([0]*j+h,g,p) for j in range(m)]
    rhs = remainder([g[0]]*N,g,p)
    equations = [[col[i] if i<len(col) else 0 for col in columns]
                 + [rhs[i] if i<len(rhs) else 0] for i in range(m)]
    answer,pivots = echelon(equations,p,reduced=True)
    assert pivots == list(range(m)), 'The reciprocal multiplication matrix is singular.'
    return clean([row[-1] for row in answer],p)

def criterion(g,N,p):
    h = g[:]
    removed = False
    if sum(h)%p == 0:
        h = divide_one(h,p)
        removed = True
        if sum(h)%p == 0:
            return {'applicable':False}
    m = len(h)-1
    if not h[0] or 2*m <= N-1 or poly_gcd(h,list(reversed(h)),p) != [1]:
        return {'applicable':False}
    R = inverse_rhs(h,N,p)
    failed = (not R or R[0] == 0) and len(R)-1 <= N-m-1
    if failed:
        e = N-m-1
        B = list(reversed(R+[0]*(e+1-len(R))))
        assert B[0] == 1 and (not B or B[-1] == 0)
        B = clean(B,p)
        lhs1 = multiply(list(reversed(h)),R,p)
        lhs2 = multiply(h,B,p)
        difference = [(lhs1[i] if i<len(lhs1) else 0)+(lhs2[i] if i<len(lhs2) else 0)
                      - h[0] for i in range(N)]
        assert clean(difference,p) == []
    return {'applicable':True,'removed_simple_root_one':removed,'residual_degree':m,
            'inverse_residue':R or [0],'predicted_axis_rank':N-int(failed)}

def gaussian_table(q,p,N):
    # q-binomial [n k]_q = [n-1 k]_q + q^(n-k)[n-1 k-1]_q.
    rows = [[1]]
    for n in range(1,N):
        old = rows[-1]
        rows.append([1] + [((old[k] if k<len(old) else 0) + pow(q,n-k,p)*old[k-1]) % p
                           for k in range(1,n)] + [1])
    return rows

def rebuild_recurrence(N,d,p,q):
    qplus = gaussian_table(q,p,N)
    qminus = gaussian_table(pow(q,-1,p),p,N)
    h = pow(4,-1,N)
    m = N-d
    matrix,labels = [],[]
    for b in range(1,d-1):
        amplitude = pow(qminus[2*b][b],-1,p)
        for a in range(1,d-b):
            row = []
            for k in range(m+1):
                j = a+k
                gaussian_minus = qminus[N-j+b][b] if j>b else 0
                value = pow(q,h*(j+b)**2,p)-amplitude*gaussian_minus
                row.append(value*pow(qplus[j+b][b],-1,p) % p)
            matrix.append(row)
            labels.append([a,b])
    return matrix,labels

def test_author_data():
    data = json.loads((AUTHOR/'FRESH_AXIS_CONTROLS.json').read_text())
    output=[]
    for c in data['recurrence_cases']:
        N,d,m,p,q = [c[key] for key in ('N','d','m','p','q')]
        assert S.isprime(p) and (p-1)%N == 0
        assert pow(q,N,p)==1 and all(pow(q,N//ell,p)!=1 for ell in S.factorint(N))
        A,labels = rebuild_recurrence(N,d,p,q)
        assert A == c['matrix'] and labels == c['row_labels']
        r = rank(A,p)
        assert r == c['matrix_rank'] == c['rank_bound'] == min((d-1)*(d-2)//2,4*d-11)
        assert len(c['basis']) == m+1-r and rank(c['basis'],p) == m+1-r
        assert all(sum(x*y for x,y in zip(row,b))%p == 0 for row in A for b in c['basis'])
        fixed=[]
        for b in c['basis']:
            fixed=poly_gcd(fixed,b,p)
        assert fixed == c['kernel_fixed_gcd_mod_p']
        assert all(j<m for j in c['pivot_columns'])
        minor = determinant([[A[i][j] for j in c['pivot_columns']] for i in c['selected_rows']],p)
        assert minor == c['defining_minor'] != 0
        # Independently check that saturation gives the all-ones functional.
        ones_in_rowspace = rank(A+[[1]*(m+1)],p)==r
        saturated = r==4*d-11
        if saturated:
            assert ones_in_rowspace and all(sum(b)%p==0 for b in c['basis'])
        samples=[]
        for s in c['samples']:
            g=s['g']
            assert len(g)==m+1 and g[-1]==1
            assert all(sum(x*y for x,y in zip(row,g))%p==0 for row in A)
            deriv=[j*g[j]%p for j in range(1,len(g))]
            assert poly_gcd(g,deriv,p)==s['derivative_gcd']
            assert poly_gcd(g,list(reversed(g)),p)==s['reciprocal_gcd']
            X=axis_matrix(g,N,p)
            axisrank=rank(X,p)
            assert axisrank==s['axis_rank']
            if axisrank==N:
                assert determinant([[row[j] for j in s['axis_pivot_columns']] for row in X],p)==s['axis_minor']!=0
            test=criterion(g,N,p)
            assert test['applicable']==s['corrected_criterion']['applicable']
            if test['applicable']:
                assert test==s['corrected_criterion']
                assert test['predicted_axis_rank']==axisrank
            samples.append({'applicable':test['applicable'],'axis_rank':axisrank})
        baseline=c['samples'][0]
        assert baseline['g'][0] and baseline['derivative_gcd']==[1] and baseline['axis_rank']==N
        output.append({'N':N,'d':d,'p':p,'q':q,'rank':r,'defining_minor':minor,
                       'saturated_refined_bound':saturated,'ones_in_rowspace_mod_p':ones_in_rowspace,
                       'kernel_gcd_mod_p':fixed,'distinct_sample_polynomials':len({tuple(s['g']) for s in c['samples']}),
                       'samples':samples})
        print('Verified author recurrence case',N,d,flush=True)
    return output

def rational_axis(g,N):
    m=S.degree(g,t)
    ps=[S.Poly(S.rem(t**j,g,t),t) for j in range(N)]
    mat=S.Matrix([[ps[j].nth(i) for i in range(m)]+[1]+[ps[(-j)%N].nth(i) for i in range(m)]
                  for j in range(N)])
    return mat

def test_rational():
    records=[]
    for n,r in [(5,1),(7,1),(9,1),(5,3),(5,5),(5,7),(6,2)]:
        N=n*r
        g=2+sum(t**(j*r) for j in range(1,n-1))
        m=(n-2)*r
        H=S.expand(t**m*g.subs(t,1/t))
        A=t**(N-r)+t**r-2
        J=S.expand(t**N*A.subs(t,1/t)-2*(1-t**N))
        assert S.gcd(g,H)==1 and S.gcd(g,S.diff(g,t))==1
        assert S.rem(A,g,t)==0 and J==A and A.subs(t,1)==0
        R=S.rem(2*sum(t**j for j in range(N))*S.invert(H,g,t),g,t)
        assert R.subs(t,0)==0 and S.degree(R,t)<=N-m-1
        X=rational_axis(g,N)
        rankQ=X.rank()
        assert rankQ==N-1
        coeff=S.Matrix([S.expand(A).coeff(t,j) for j in range(N)])
        assert X.T*coeff==S.zeros(2*m+1,1)
        records.append({'n':n,'r':r,'N':N,'m':m,'axis_rank_Q':rankQ,'inverse_remainder':str(R)})
    h=t**9+t**6+t**3+2
    g=S.expand((t-1)*h)
    assert S.gcd(g,S.diff(g,t))==1 and rational_axis(g,15).rank()==14
    # A deliberately nonsquarefree characteristic-zero test.
    g=(t-2)**3
    assert S.gcd(g,S.expand(t**3*g.subs(t,1/t)))==1
    repeated_rank=rational_axis(g,5).rank()
    x,y=S.symbols('x y')
    g=t**3+t**2+t+2
    H=2*t**3+t**2+t+1
    bezout=S.Poly(S.cancel((g.subs(t,x)*H.subs(t,y)-g.subs(t,y)*H.subs(t,x))/(x-y)),x,y)
    B=S.Matrix([[bezout.coeff_monomial(x**i*y**j) for j in range(3)] for i in range(3)])
    assert B.tolist()==[[-1,-1,-3],[-1,-3,-1],[-3,-1,-1]] and B.det()==20
    assert S.resultant(g,H,t)==-20
    return {'family_cases':records,'simple_root_one_variant_rank_Q':14,
            'nonsquarefree_test_t_minus_two_cubed_rank_Q':repeated_rank,
            'bezout_matrix':B.tolist(),'bezout_determinant':int(B.det()),'reciprocal_resultant':-20}

def exhaustive_small_fields():
    counts=Counter()
    bad_examples=[]
    for p,maxN in [(2,9),(3,6),(5,5)]:
        for N in range(2,maxN+1):
            for m in range((N+1)//2,N):
                for coeff in product(range(p),repeat=m):
                    if not coeff[0]:
                        continue
                    g=list(coeff)+[1]
                    if poly_gcd(g,list(reversed(g)),p)!=[1]:
                        continue
                    test=criterion(g,N,p)
                    assert test['applicable'] and not test['removed_simple_root_one']
                    actual=rank(axis_matrix(g,N,p),p)
                    assert actual==test['predicted_axis_rank'] and actual>=N-1
                    repeated=poly_gcd(g,[i*g[i]%p for i in range(1,len(g))],p)!=[1]
                    counts['applicable']+=1
                    counts['characteristic_'+str(p)]+=1
                    counts['nonsquarefree']+=repeated
                    counts['rank_N_minus_one']+=actual==N-1
                    counts['nonsquarefree_rank_N_minus_one']+=repeated and actual==N-1
                    if actual==N-1 and len(bad_examples)<12:
                        bad_examples.append({'p':p,'N':N,'g':g,'nonsquarefree':repeated})
    # Repeated-root family obtained when substitution exponent equals characteristic.
    N,p,g=15,3,[2,0,0,1,0,0,1,0,0,1]
    result=criterion(g,N,p)
    assert result['predicted_axis_rank']==14==rank(axis_matrix(g,N,p),p)
    assert poly_gcd(g,[i*g[i]%p for i in range(1,len(g))],p)!=[1]
    return {'exhaustive_counts':dict(counts),'sample_deficiencies':bad_examples,
            'additional_nonsquarefree_F3_N15':{'g':g,'axis_rank':14,'criterion':result}}

def main():
    files=sorted(p for p in AUTHOR.iterdir() if p.is_file())
    hashes={str(p.relative_to(ROOT)):sha(p) for p in files}
    old=json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())['sources']
    for item in old:
        assert sha(ROOT/item['path'])==item['sha256']
    result={'status':'PASS','predecessor_programs_executed_or_imported':False,
            'author_file_hashes_at_run':hashes,
            'author_source_bindings_verified':old,
            'recurrence_cases':test_author_data(),
            'rational_controls':test_rational(),
            'small_field_controls':exhaustive_small_fields()}
    assert hashes=={str(p.relative_to(ROOT)):sha(p) for p in files}, 'Author bytes changed during audit.'
    result['summary']={'recurrence_pairs':len(result['recurrence_cases']),
                       'samples':sum(len(c['samples']) for c in result['recurrence_cases']),
                       'applicable_samples':sum(s['applicable'] for c in result['recurrence_cases'] for s in c['samples']),
                       'refined_rank_saturated_pairs':sum(c['saturated_refined_bound'] for c in result['recurrence_cases']),
                       'distinct_sample_polynomials_per_pair_total':sum(c['distinct_sample_polynomials'] for c in result['recurrence_cases'])}
    (OUT/'INDEPENDENT_EXACT_CONTROLS.json').write_text(json.dumps(result,indent=2,default=int)+'\n')
    print(json.dumps(result['summary']),flush=True)
    print(json.dumps(result['small_field_controls']['exhaustive_counts']),flush=True)

if __name__=='__main__':
    main()
