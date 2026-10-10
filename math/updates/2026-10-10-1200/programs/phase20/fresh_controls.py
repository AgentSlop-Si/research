"""Independent exact audit. Never import, execute or compile supplied programs.

Only standard-library imports. Uploaded Python is read as inert text by ast.parse
to locate the dense-reference operation-count discrepancy. Fresh algorithms use
literal matrix identities, a recursive NTT, and direct finite-field elimination.
"""
from pathlib import Path
from math import gcd, lcm
import ast
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
RNG = random.Random(202610101207)


def prime(p):
    return p >= 2 and all(p % d for d in range(2, int(p ** .5) + 1))


def fields_for(order, count=2):
    found = []
    for k in range(1, 100000):
        p = k * order + 1
        if p > 2 and prime(p):
            found.append(p)
            if len(found) == count:
                return found
    raise AssertionError('no test field found')


def divisors_prime(n):
    answer = []
    for d in range(2, n + 1):
        if n % d == 0 and prime(d):
            answer.append(d)
    return answer


def root(n, p):
    if n == 1:
        return 1
    for x in range(2, p):
        w = pow(x, (p - 1) // n, p)
        if pow(w, n, p) == 1 and all(pow(w, n // d, p) != 1 for d in divisors_prime(n)):
            return w
    raise AssertionError('missing root')


def dft(x, w, p):
    n = len(x)
    return [sum(x[t] * pow(w, -k*t % n, p) for t in range(n)) % p for k in range(n)]


def ntt_recursive(x, w, p):
    """Fresh recursive negative-exponent transform, different from source loop."""
    n = len(x)
    if n == 1:
        return [x[0] % p]
    a = ntt_recursive(x[::2], w*w % p, p)
    b = ntt_recursive(x[1::2], w*w % p, p)
    z = 1
    step = pow(w, -1, p)
    lo, hi = [], []
    for u, v in zip(a, b):
        lo.append((u + z*v) % p)
        hi.append((u - z*v) % p)
        z = z*step % p
    return lo + hi


def conv(a, b, rho, p):
    size = 1 << (len(a) + len(b) - 2).bit_length()
    aa = ntt_recursive(a + [0]*(size-len(a)), rho, p)
    bb = ntt_recursive(b + [0]*(size-len(b)), rho, p)
    raw = ntt_recursive([x*y % p for x,y in zip(aa,bb)], pow(rho,-1,p), p)
    return [x*pow(size,-1,p) % p for x in raw]


def matvec(a,x,p):
    return [sum(u*v for u,v in zip(row,x)) % p for row in a]


def matmul(a,b,p):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) % p
             for j in range(len(b[0]))] for i in range(len(a))]


def rank(a,p):
    a = [row[:] for row in a]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r,len(a)) if a[i][j] % p), None)
        if pivot is None:
            continue
        a[r],a[pivot]=a[pivot],a[r]
        scale=pow(a[r][j],-1,p)
        a[r]=[z*scale % p for z in a[r]]
        for i in range(r+1,len(a)):
            scale=a[i][j]
            a[i]=[(v-scale*u) % p for v,u in zip(a[i],a[r])]
        r+=1
    return r


def inverse(a,p):
    n=len(a)
    aug=[row[:] + [int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if aug[i][k] % p)
        aug[k],aug[pivot]=aug[pivot],aug[k]
        scale=pow(aug[k][k],-1,p)
        aug[k]=[v*scale % p for v in aug[k]]
        for i in range(n):
            if i!=k:
                scale=aug[i][k]
                aug[i]=[(v-scale*u) % p for v,u in zip(aug[i],aug[k])]
    return [row[n:] for row in aug]


def coefficients(n,p,w):
    g=dft([pow(w,-t*t % n,p) for t in range(n)],w,p)
    return g, [[g[(a+b)%n]*pow(n,-1,p)%p for b in range(n)] for a in range(n)]


def factor_action(x,n,p,w,g):
    invn=pow(n,-1,p)
    if n%2:
        inv4=pow(4,-1,n)
        diagonal=[pow(w,t*t*inv4 % n,p) for t in range(n)]
        f=dft([u*v % p for u,v in zip(diagonal,x)],w,p)
        return [g[0]*invn*diagonal[a]*f[-a*pow(2,-1,n)%n] % p for a in range(n)]
    m=n//2
    kap=m%2
    y=[0]*n
    for rp in [0,1]:
        cp=(kap-rp)%2
        d=(rp+cp-kap)//2
        diagonal=[pow(w,(t*t+(2*d+kap)*t)%n,p) for t in range(m)]
        f=dft([diagonal[b]*x[2*b+cp]%p for b in range(m)], w*w%p,p)
        scalar=g[kap]*invn*pow(w,(d*d+kap*d)%n,p)%p
        for a in range(m):
            y[2*a+rp]=scalar*diagonal[a]*f[-a % m]%p
    return y


def qbinom_table(n,w,p):
    rows=[[1]]
    for degree in range(1,n):
        old=rows[-1]
        new=[1]
        for b in range(1,degree):
            new.append((old[b]+pow(w,degree-b,p)*old[b-1])%p)
        new.append(1)
        rows.append(new)
    return rows


def chart_data(n,p,w,alpha,beta):
    delta=(1-pow(alpha,n,p)-pow(beta,n,p))%p
    assert alpha and beta and delta
    phi=[1]
    for t in range(1,n):
        phi.append(phi[-1]*(1-pow(w,t,p))%p)
    gam=sum(pow(w,-t*t%n,p) for t in range(n))*pow(n,-1,p)%p
    A=[phi[t]*pow(alpha,-t,p)%p for t in range(n)]
    B=[phi[t]*pow(beta,-t,p)%p for t in range(n)]
    H=[pow(w,t*t*pow(4,-1,n)%n,p)*pow(phi[t],-1,p)%p for t in range(n)]
    return delta*gam%p,A,B,H


def small_coeff_controls():
    totals={'field_root_cases':0,'coefficient_entries':0,'complete_matvecs':0,
            'Weyl_synthesis_entries':0,'C_F_chirp_F_entries':0,'parity_classes':{},
            'wrong_scale_detected':False,'wrong_even_parity_detected':False}
    for n in range(2,65):
        for p in fields_for(n):
            w0=root(n,p)
            for w in sorted(set([w0,pow(w0,-1,p)])):
                g,C=coefficients(n,p,w)
                totals['field_root_cases']+=1
                totals['coefficient_entries']+=n*n
                assert rank(C,p)==n
                assert sum(v==0 for row in C for v in row)==(0 if n%2 else n*n//2)
                for r in range(n):
                    assert g[(r+2)%n]==g[r]*pow(w,(r+1)%n,p)%p
                    if not n%2:
                        assert bool(g[r])==(r%2==(n//2)%2)
                if n%2:
                    for r in range(n):
                        assert g[r]==g[0]*pow(w,r*r*pow(4,-1,n)%n,p)%p
                else:
                    kap=(n//2)%2
                    for j in range(n//2):
                        assert g[kap+2*j]==g[kap]*pow(w,(j*j+kap*j)%n,p)%p
                    key=str(n%4)
                    totals['parity_classes'][key]=totals['parity_classes'].get(key,0)+1
                for trial in range(3):
                    x=[RNG.randrange(p) for _ in range(n)]
                    assert factor_action(x,n,p,w,g)==matvec(C,x,p)
                    totals['complete_matvecs']+=1
                    if n%2:
                        inv4=pow(4,-1,n)
                        z=[x[b]*pow(w,-b*b*inv4%n,p)%p for b in range(n)]
                        y=matvec(C,z,p)
                        recovered=[y[-2*k%n]*pow(g[0]*pow(n,-1,p)*pow(w,(-2*k%n)**2*inv4%n,p)%p,-1,p)%p for k in range(n)]
                        assert recovered==dft(x,w,p)
                if n<=16:
                    for k in range(n):
                        for t in range(n):
                            a=(k-t)%n
                            y=sum(C[a][b]*pow(w,b*t%n,p) for b in range(n))%p
                            assert y==pow(w,-k*t%n,p)
                            totals['Weyl_synthesis_entries']+=1
                    F=[[pow(w,-a*b%n,p) for b in range(n)] for a in range(n)]
                    FD=[[F[a][t]*pow(w,-t*t%n,p)%p for t in range(n)] for a in range(n)]
                    CD=matmul(FD,F,p)
                    assert [[v*pow(n,-1,p)%p for v in row] for row in CD]==C
                    totals['C_F_chirp_F_entries']+=n*n
                if n==5:
                    totals['wrong_scale_detected'] |= any(g[(a+b)%n]!=C[a][b] for a in range(n) for b in range(n))
                if n==6:
                    totals['wrong_even_parity_detected'] |= g[0]==0 and g[1]!=0
    return totals


def chart_controls():
    totals={'field_cases':0,'weight_entries':0,'full_matvec_trials':0,
            'full_NTT_output_coordinates':0,'large_full_cases':[],
            'wrong_normalization_detected':False,'weight_action_is_not_DFT_detected':False}
    cases=[]
    for n in range(3,64,2):
        L=1<<(2*n-2).bit_length()
        cases.extend((n,p) for p in fields_for(lcm(n,L)))
    cases.extend([(255,783361),(1023,6285313)])
    for n,p in cases:
        L=1<<(2*n-2).bit_length()
        w=root(n,p);rho=root(L,p)
        alpha,beta=next((a,b) for a in range(1,min(p,10)) for b in range(1,min(p,10))
                        if (1-pow(a,n,p)-pow(b,n,p))%p)
        scalar,A,B,H=chart_data(n,p,w,alpha,beta)
        qb=qbinom_table(n,w,p)
        g,C=coefficients(n,p,w)
        delta=(1-pow(alpha,n,p)-pow(beta,n,p))%p
        W=[]
        for a in range(n):
            row=[]
            for b in range(n):
                v=scalar*A[a]*B[b]*H[a+b]%p if a+b<n else 0
                if a+b<n:
                    sector=pow(alpha,a,p)*pow(beta,b,p)*qb[a+b][b]*pow(delta,-1,p)%p
                    assert v*sector%p==C[a][b]
                row.append(v)
            W.append(row)
        if n<=63:
            assert rank(W,p)==n
        assert all(W[a][n-1-a] for a in range(n))
        for a in range(n):
            for j in range(a):
                assert W[a][n-1-j]==0
        for t in range(1,n):
            assert H[t]*pow(H[t-1],-1,p)%p==pow(w,(2*t-1)*pow(4,-1,n)%n,p)*pow(1-pow(w,t,p),-1,p)%p
        totals['field_cases']+=1
        totals['weight_entries']+=n*n
        for trial in range(3 if n<=63 else 1):
            x=[RNG.randrange(p) for _ in range(n)]
            v=[B[b]*x[b]%p for b in range(n)][::-1]
            z=conv(H,v,rho,p)
            fast=[scalar*A[a]*z[n-1+a]%p for a in range(n)]
            assert fast==matvec(W,x,p)
            totals['full_matvec_trials']+=1
            totals['full_NTT_output_coordinates']+=n
            totals['wrong_normalization_detected'] |= any(y!=y*L%p for y in fast)
            totals['weight_action_is_not_DFT_detected'] |= fast!=dft(x,w,p) if n<=31 else False
        if n>63:
            totals['large_full_cases'].append({'n':n,'p':p,'L':L,'all_outputs_checked':True})
    return totals


def green_filter_controls():
    totals={'resolvent_matrices':0,'filtered_sector_matrices':0,'entry_checks':0}
    for n,p in [(3,97),(4,17),(5,641),(6,97),(7,449),(9,577)]:
        w=root(n,p);alpha=beta=1;delta=(-1)%p
        inverses=[]
        for ell in range(n):
            for j in range(n):
                M=[[int(k==t) for t in range(n)] for k in range(n)]
                for t in range(n):
                    M[(t+1)%n][t]=(M[(t+1)%n][t]-pow(w,ell,p))%p
                    M[t][t]=(M[t][t]-pow(w,j+t,p))%p
                inv=inverse(M,p)
                assert matmul(M,inv,p)==[[int(k==t) for t in range(n)] for k in range(n)]
                inverses.append((ell,j,inv))
                totals['resolvent_matrices']+=1
        qb=qbinom_table(n,w,p)
        for a in range(n):
            for b in range(n):
                R=[[sum(pow(w,(-a*ell-b*j)%n,p)*Z[k][t] for ell,j,Z in inverses)*pow(n*n,-1,p)%p
                    for t in range(n)] for k in range(n)]
                sector=qb[a+b][b]*pow(delta,-1,p)%p if a+b<n else 0
                expected=[[sector*pow(w,b*t%n,p)%p if k==(t+a)%n else 0 for t in range(n)] for k in range(n)]
                assert R==expected
                totals['filtered_sector_matrices']+=1
                totals['entry_checks']+=n*n
    return totals


def charged_power(e):
    return e.bit_length()+e.bit_count()-1


def even_chart_and_boundary_controls():
    """Audit corollary, not attributed to the uploaded theorem."""
    result={'even_field_cases':0,'entries':0,'rank_N_cases':0,'rank_N_minus_one_cases':0,
            'complete_convolution_trials':0,'nonprime_is_not_validated':None}
    for n in range(2,41,2):
        L=1<<(2*n-2).bit_length()
        for p in fields_for(lcm(n,L)):
            w=root(n,p);rho=root(L,p)
            g,C=coefficients(n,p,w)
            phi=[1]
            for t in range(1,n):phi.append(phi[-1]*(1-pow(w,t,p))%p)
            # alpha=beta=1, so delta=-1. Use literal Gauss vector, no odd inverse of 4.
            H=[g[t]*pow(n,-1,p)*pow(phi[t],-1,p)%p for t in range(n)]
            W=[[-phi[a]*phi[b]*H[a+b]%p if a+b<n else 0 for b in range(n)] for a in range(n)]
            qb=qbinom_table(n,w,p)
            for a in range(n):
                for b in range(n-a):assert W[a][b]*(-qb[a+b][b])%p==C[a][b]
            expected=n if n%4==2 else n-1
            assert rank(W,p)==expected
            result['rank_N_cases' if n%4==2 else 'rank_N_minus_one_cases']+=1
            x=[RNG.randrange(p) for _ in range(n)]
            v=[phi[b]*x[b]%p for b in range(n)][::-1]
            z=conv(H,v,rho,p)
            assert [-phi[a]*z[n-1+a]%p for a in range(n)]==matvec(W,x,p)
            result['complete_convolution_trials']+=1
            result['even_field_cases']+=1
            result['entries']+=n*n
    n,p,w=3,91,29
    assert not prime(p) and (p-1)%n==0 and pow(w,n,p)==1 and pow(w,1,p)!=1
    result['nonprime_is_not_validated']={'n':n,'p':p,'w':w,
        'passes_supplied_root_checks':True,'not_a_field':True,
        'character_sum_not_zero':sum(pow(w,t,p) for t in range(n))%p}
    return result


def validation(n):
    return charged_power(n)+sum(charged_power(n//d) for d in divisors_prime(n))


def source_cost_audit():
    text=(HERE/'source/unpacked/phase20.py').read_text()
    tree=ast.parse(text)  # Read-only syntax tree; never compile or evaluate.
    cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='TriangularGreenChart')
    fun=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='apply_naive')
    outer=next(x for x in fun.body if isinstance(x,ast.For))
    inner=next(x for x in outer.body if isinstance(x,ast.For))
    calls=[x.func.attr for x in ast.walk(inner) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr in ['times','plus','minus','inverse']]
    assert sorted(calls)==['plus','times','times']
    source=json.loads((HERE/'source/unpacked/AUDIT_RESULTS.json').read_text())
    result={'inert_source_inner_loop_calls':calls,'literal_per_entry_operations':3,'cases':[]}
    for ns,c in source['larger_cases'].items():
        n=int(ns);L=c['ntt_length'];q=n*(n+1)//2
        prep=11*n+1+2*charged_power(n)+validation(n)+validation(L)
        online=9*L*(L.bit_length()-1)//2+4*L+4*n-1
        assert prep==c['preprocessing_ops']
        assert online==c['online_ops']
        dense=3*q+2*n
        corrected=(dense+prep)/(online+prep)
        result['cases'].append({'n':n,'L':L,'prep':prep,'online':online,'fused_total':prep+online,
            'source_dense_online_claim':c['dense_triangular_reference_field_ops'],
            'correct_literal_dense_online':dense,'correct_literal_dense_cold':dense+prep,
            'literal_online_over_fused_total':dense/(prep+online),
            'apples_to_apples_cold_speedup':corrected,
            'optimized_shared_input_direct_online':2*q+3*n,
            'optimized_direct_cold_speedup':(2*q+3*n+prep)/(online+prep)})
    n=65536
    m=n//2
    radix=lambda size:size-1+3*size*(size.bit_length()-1)//2
    even=validation(n)+5*n+4+2*radix(m)
    assert even==source['operation_comparisons']['even_N_65536_coefficient_action']['coefficient_matrix_fast_ops']
    assert radix(n)==source['operation_comparisons']['even_N_65536_coefficient_action']['ordinary_DFT_radix2_ops']
    n=8191;L=1<<(2*n-2).bit_length()
    blue=validation(n)+validation(L)+(n-1)+n+3*radix(L)+L+2+(n-1)+2*n
    coeff=validation(n)+5*n+1+blue
    assert blue==source['operation_comparisons']['odd_N_8191_coefficient_action']['ordinary_DFT_Bluestein_ops']
    assert coeff==source['operation_comparisons']['odd_N_8191_coefficient_action']['coefficient_matrix_Bluestein_ops']
    result['full_coefficient_counts']={'even65536':even,'radix65536':radix(65536),'odd8191':coeff,'bluestein8191':blue}
    result['radix65536_with_same_root_validation']=radix(65536)+validation(65536)
    result['generic_even_direct_fallback_formula']='N^2 + 6N + 2 + validation(N), when N/2 is not a power of two'
    result['generic_even_fallback_example_N30']=30*30+6*30+2+validation(30)
    return result


def main():
    report={'method':'Fresh exact controls; source remains inert; no external writes.',
            'small_coefficients':small_coeff_controls(),
            'charts':chart_controls(),
            'Green_sector_normalization':green_filter_controls(),
            'audit_even_chart_corollary_and_boundaries':even_chart_and_boundary_controls(),
            'static_cost_audit':source_cost_audit()}
    assert report['small_coefficients']['wrong_scale_detected']
    assert report['small_coefficients']['wrong_even_parity_detected']
    assert report['charts']['wrong_normalization_detected']
    assert report['charts']['weight_action_is_not_DFT_detected']
    report['fresh_script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
