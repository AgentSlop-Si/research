"""Self-authored mathematical controls; imports no supplied or patched research code."""
import json
from math import gcd
from pathlib import Path


def root_of_order(n, p):
    for a in range(2, p):
        if pow(a, n, p) == 1 and all(pow(a, d, p) != 1 for d in range(1, n) if n % d == 0):
            return a
    raise AssertionError((n, p))


def dft(v, omega, p):
    n = len(v)
    return [sum(v[j] * pow(omega, j*k, p) for j in range(n)) % p for k in range(n)]


def matrix_rank(a, p):
    a = [list(row) for row in a]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[pivot], a[r] = a[r], a[pivot]
        scale = pow(a[r][c], -1, p)
        a[r] = [x * scale % p for x in a[r]]
        for i in range(len(a)):
            if i != r:
                scale = a[i][c]
                a[i] = [(x - scale*y) % p for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def det_permutations(a, p):
    # Leibniz expansion differs from the supplied elimination determinant.
    import itertools
    answer = 0
    for s in itertools.permutations(range(len(a))):
        sign = (-1) ** sum(s[i] > s[j] for i in range(len(a)) for j in range(i+1,len(a)))
        term = sign
        for i,j in enumerate(s):
            term = term*a[i][j] % p
        answer = (answer + term) % p
    return answer


def cubic_coefficients(R, w, offset, p):
    # Expand the 3x3 Hankel determinant over polynomial factors directly.
    import itertools
    out = [0,0,0,0]
    for perm in itertools.permutations(range(3)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(3) for j in range(i+1,3))
        poly = [sign]
        for i,j in enumerate(perm):
            k = offset+i+j
            linear = (R[k], -R[k]*pow(w,k,p))
            nxt = [0]*(len(poly)+1)
            for z,x in enumerate(poly):
                for t,y in enumerate(linear):
                    nxt[z+t] = (nxt[z+t]+x*y) % p
            poly = nxt
        out = [(x+y) % p for x,y in zip(out,poly)]
    return out


def sylvester(a,b):
    return [[0]*i + list(reversed(v)) + [0]*(2-i) for v in (a,b) for i in range(3)]


def resonance_controls():
    cases = false_rejections = 0
    for p in (17,41,73,97,193):
        for n in range(2,33):
            if (p-1) % n:
                continue
            omega = root_of_order(n,p)
            for delta in range(1,n):
                g = gcd(n,delta)
                for alpha in range(1,p):
                    actual = sum((1-alpha*pow(omega,delta*k,p)) % p == 0 for k in range(n))
                    expected = g if pow(alpha,n//g,p) == 1 else 0
                    old = g>1 and pow(alpha,n,p)==1
                    new = g>1 and pow(alpha,n//g,p)==1
                    assert actual == expected
                    assert new == (actual > 1)
                    assert not new or old
                    false_rejections += old and not new
                    cases += 1
    controls=[]
    for p,omega,r,known_at_2 in ((73,10,[37,37,5,5,50,50,62,62],62), (97,33,[49,49,65,65,11,11,72,72],48)):
        n,delta,alpha=8,2,omega
        R=dft(r,omega,p)
        h=[(r[j]-alpha*r[(j-delta)%n])%p for j in range(n)]
        assert h==[1,1,0,0,0,0,0,0]
        denominators=[(1-alpha*pow(omega,delta*k,p))%p for k in range(n)]
        assert all(denominators)
        H=dft(h,omega,p)
        reconstructed=[H[k]*pow(denominators[k],-1,p)%p for k in range(n)]
        assert reconstructed==R
        w=pow(omega,delta,p)
        cubics=[cubic_coefficients(R,w,o,p) for o in (0,1)]
        assert all(sum(v*pow(alpha,i,p) for i,v in enumerate(a))%p==0 for a in cubics)
        assert cubics[0][-1] and cubics[1][-1]
        assert matrix_rank(sylvester(*cubics),p)==5
        at_2=det_permutations(sylvester(*(cubic_coefficients(R,2,o,p) for o in (0,1))),p)
        assert at_2==known_at_2
        controls.append({'p':p,'N':n,'omega':omega,'delta':delta,'alpha':alpha,'residual':r,'forcing':h,'full_dft':R,'poles':0,'resultant_at_2':at_2,'gcd_degree':1,'domain':'complete-engine-compatible roots' if p==97 else 'residual gate only; no 16th root'})
    # Independent exact single-pole reconstruction and multipole-policy rejection.
    p,n,omega=97,8,33
    for delta,alpha,r,expected_poles in ((1,1,[1,1,1,1,0,0,0,0],1),(2,1,[1,0,1,0,0,0,0,0],2)):
        R=dft(r,omega,p)
        h=[(r[j]-alpha*r[(j-delta)%n])%p for j in range(n)]
        assert sum(x!=0 for x in h)==2
        H=dft(h,omega,p)
        denom=[(1-alpha*pow(omega,delta*k,p))%p for k in range(n)]
        assert denom.count(0)==expected_poles
        restored=[H[k]*pow(denom[k],-1,p)%p if denom[k] else sum(r[j]*pow(omega,j*k,p) for j in range(n))%p for k in range(n)]
        assert restored==R
        assert (gcd(n,delta)>1 and pow(alpha,n//gcd(n,delta),p)==1)==(expected_poles>1)
    # Perturbation invisible to the first eight probes; full-coordinate test detects it.
    n,p=16,193
    omega=root_of_order(n,p)
    polynomial=[1]
    for k in range(8):
        a=pow(omega,k,p)
        new=[0]*(len(polynomial)+1)
        for j,c in enumerate(polynomial):
            new[j]=(new[j]-a*c)%p
            new[j+1]=(new[j+1]+c)%p
        polynomial=new
    mutant=polynomial+[0]*(n-len(polynomial))
    assert dft(mutant,omega,p)[:8]==[0]*8
    defect=[(mutant[j]-omega*mutant[(j-2)%n])%p for j in range(n)]
    assert sum(x!=0 for x in defect)>2
    return {'predicate_cases':cases,'old_false_rejections':false_rejections,'new_policy_mismatches':0,'minimal_controls':controls,'single_pole_and_multipole_controls':True,'eight_probe_mutant_defect_support':sum(x!=0 for x in defect)}


def weil_controls():
    shears=entries=covariance_entries=0
    records=[]
    for p,k,ell in ((3,1,7),(5,1,11),(7,1,29),(3,2,19),(5,2,101),(3,3,109),(7,2,197)):
        q=p**k
        zeta=root_of_order(q,ell)
        for b in range(q):
            v=k if b==0 else 0
            if b:
                t=b
                while t%p==0:
                    v+=1;t//=p
            g=p**v
            m=q//g
            direct=[]
            old=[]
            for t in range(q):
                direct.append(pow(q,-1,ell)*sum(pow(zeta,(-b*z*z*pow(2,-1,q)+t*z)%q,ell) for z in range(q))%ell)
                old.append(pow(q,-1,ell)*sum(pow(zeta,(b*z*z*pow(2,-1,q)+t*z)%q,ell) for z in range(q))%ell)
            if b==0:
                assert direct==[1]+[0]*(q-1)
            else:
                u=b//g
                eta=pow(zeta,g,ell)
                scalar=pow(m,-1,ell)*sum(pow(eta,(-u*z*z*pow(2,-1,m))%m,ell) for z in range(m))%ell
                assert scalar!=0
                predicted=[0 if t%g else scalar*pow(eta,((t//g)**2*pow(2*u,-1,m))%m,ell)%ell for t in range(q)]
                assert direct==predicted
                assert sum(x!=0 for x in direct)==m
                ratio=direct[0]**2*pow(direct[g]*direct[-g]%ell,-1,ell)%ell
                assert ratio==pow(eta,-pow(u,-1,m),ell)
                assert pow(ratio,m,ell)==1 and all(pow(ratio,d,ell)!=1 for d in range(1,m) if m%d==0)
                assert direct!=old
                opposite=[pow(q,-1,ell)*sum(pow(zeta,((q-b)*z*z*pow(2,-1,q)+t*z)%q,ell) for z in range(q))%ell for t in range(q)]
                assert opposite==direct
            # Every matrix entry is the circulant row evaluated at y-x.
            for x in range(q):
                for y in range(q):
                    assert direct[(y-x)%q]==direct[(x-y)%q]
                    entries+=1
                    for a,c in ((1,0),(0,1),(2,4)):
                        shifted=(a+b*c)%q
                        lhs=direct[(y+a-x)%q]*pow(zeta,(c*(y+a*pow(2,-1,q)))%q,ell)%ell
                        rhs=pow(zeta,(c*(x-shifted*pow(2,-1,q)))%q,ell)*direct[(y-x+shifted)%q]%ell
                        assert lhs==rhs
                        covariance_entries+=1
            shears+=1
        records.append({'p':p,'k':k,'q':q,'coefficient_prime':ell,'zeta':zeta,'all_b':q})
    # Independent group relation: W^-1 L(-b) W = U(b), in integer matrices.
    W=((0,-1),(1,0)); Wi=((0,1),(-1,0))
    def product(a,b):
        return tuple(tuple(sum(a[i][t]*b[t][j] for t in range(2)) for j in range(2)) for i in range(2))
    for b in range(-10,11):
        assert product(product(Wi,((1,0),(-b,1))),W)==((1,b),(0,1))
    return {'scalar_cases':shears,'matrix_entries_covered_by_translation':entries,'weyl_covariance_entries':covariance_entries,'all_nonzero_wrong_sign_controls_distinct':True,'signed_cross_ratio_verified':True,'field_cases':records,'group_relation_cases':21,'does_not_execute_candidate':True}


if __name__=='__main__':
    results={'execution_scope':'Only this newly self-authored control program. No supplied or patched module imported or executed.','resonance':resonance_controls(),'weil':weil_controls()}
    target=Path(__file__).with_name('INDEPENDENT_MATH_RESULTS.json')
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
