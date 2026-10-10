#!/usr/bin/env python3
"""Independent GF(17) audit; Python standard library only.

Uploaded programs are never imported, evaluated, or executed. Input JSON is data.
The enumerator reconstructs H by three-point Vandermonde interpolation, obtains
necessary tail equations by a separate three-mode interpolation, evaluates the
lower condition as a 4x4 Fourier determinant, and independently builds the upper
gates from 3x3 Fourier determinants. It tries ALL 17**2 gamma pairs for each
surviving h/t/beta tuple. Candidate matrices are built with generic linear solves
(2x2 interior, 3x3 boundary), and tested by direct matrix multiplication/minors.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

P=17
Z=9
N=8
PERM=[7,0,6,3,4,1,2,5]
POW=[[pow(Z,i*j,P) for j in range(N)] for i in range(N)]
INV={i:pow(i,-1,P) for i in range(1,P)}


def determinant(a):
    a=[[v%P for v in row] for row in a]
    d=1
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:a[pivot],a[j]=a[j],a[pivot];d=-d
        u=a[j][j];d=d*u%P
        for i in range(j+1,len(a)):
            r=a[i][j]*INV[u]%P
            for k in range(j+1,len(a)):a[i][k]=(a[i][k]-r*a[j][k])%P
    return d%P


def solve(a,b):
    n=len(a);a=[[v%P for v in row]+[b[i]%P] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:raise ZeroDivisionError('singular system')
        a[j],a[pivot]=a[pivot],a[j]
        a[j]=[v*INV[a[j][j]]%P for v in a[j]]
        for i in range(n):
            if i!=j:
                r=a[i][j]
                a[i]=[(u-r*v)%P for u,v in zip(a[i],a[j])]
    return [row[-1] for row in a]


def inverse_and_rank(a):
    n=len(a)
    a=[[v%P for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    rank=0
    for j in range(n):
        pivot=next((i for i in range(rank,n) if a[i][j]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        a[rank]=[v*INV[a[rank][j]]%P for v in a[rank]]
        for i in range(n):
            if i!=rank:
                r=a[i][j];a[i]=[(u-r*v)%P for u,v in zip(a[i],a[rank])]
        rank+=1
    return rank, [row[n:] for row in a] if rank==n else None


def d3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%P


def interpolate_weights(nodes,modes,targets):
    # Return rows expressing values at targets as combinations of node values.
    a=[[pow(Z,m*k,P) for m in modes] for k in nodes]
    out=[]
    for k in targets:
        out.append(solve(list(map(list,zip(*a))),[pow(Z,m*k,P) for m in modes]))
    return out


HEAD_WEIGHTS=interpolate_weights([0,1,2],[0,-1,-2],list(range(N)))
TAIL_WEIGHTS=interpolate_weights([3,4,5],[1,2,3],[6,7])


def tail_scaled(hs,h6,t,beta):
    h=hs[:6]+[h6]
    # Interpolate the first/later Fourier column difference between k=0,7.
    # t(z-1)L_k=(z-1)(1-beta*h0+beta*h_k)
    #                  +(t-1+beta*(h0-1))(z^(-k)-1).
    bnum=(t-1+beta*(h[0]-1))%P
    return [0]+[((Z-1)*(1-beta*h[0]+beta*h[k])+bnum*(pow(Z,-k,P)-1))%P for k in range(1,7)]+[t*(Z-1)%P]


def tail_residual(lhat):
    return [(lhat[k]-sum(w*lhat[j] for w,j in zip(weights,[3,4,5])))%P for k,weights in zip([6,7],TAIL_WEIGHTS)]


def lower_det(h,lhat):
    m=[]
    for i in range(4,8):
        m.append([sum(POW[i][k]*h[k] for k in range(3))%P,
                  sum(POW[i][k]*lhat[k] for k in range(4,8))%P,
                  POW[i][3],sum(POW[i][k]*h[k] for k in range(7))%P+POW[i][7]])
    return determinant(m)


def upper_coefficients(h,lhat):
    ds={}
    for k in (4,1,2,5):
        rows=[]
        for i in range(4):
            rows.append([sum(POW[i][r]*h[r] for r in range(k))%P,
                         sum(POW[i][r]*lhat[r] for r in range(k+1,8))%P,POW[i][k]])
        r0,r1,r2,r3=rows
        ds[k]=(d3(r1,r2,r3),-d3(r0,r2,r3)%P,-d3(r1,r0,r3)%P,d3(r1,r2,r0))
    a,b,c,d=ds[4]
    rs=[]
    for k in (1,2,5):
        aa,bb,cc,dd=ds[k]
        rs.append([(a*dd-aa*d)%P,(b*dd-bb*d)%P,(c*dd-cc*d)%P])
    return ds,rs


def poly_mod(terms):
    return [(tuple(m),sum(v*pow(Z,k,P) for k,v in enumerate(c))%P) for m,c in terms]


def peval(poly,x):
    total=0
    for m,c in poly:
        v=c
        for i in m:v=v*x[i]%P
        total+=v
    return total%P


def reconstruct(h,hs,lhat,t,beta,g1,g2):
    l=[v*INV[t*(Z-1)%P]%P for v in lhat]
    q1=[(v-g1)%P for v in POW[1]];q2=[(v-g2)%P for v in POW[2]]
    s1={k:sum(q1[i]*h[i] for i in range(k))%P for k in range(1,7)}
    s2={k:sum(q2[i]*h[i] for i in range(k))%P for k in range(1,7)}
    r1={k:sum(q1[i]*l[i] for i in range(k+1,8))%P for k in range(1,7)}
    r2={k:sum(q2[i]*l[i] for i in range(k+1,8))%P for k in range(1,7)}
    if any(not v for v in s1.values()):return None,'S1_zero'
    boundary=[[s1[6],r1[6],0],[hs[6],0,h[6]-hs[6]],[hs[7],-1,1-hs[7]]]
    if determinant(boundary)==0:return None,'boundary_determinant_zero'
    eta6,v6,rho=solve(boundary,[-q1[6],1,0])
    if (eta6-rho)%P==0:
        # The last two physical columns are proportional, hence singular.
        col6=[h[k]*eta6%P for k in range(6)]+[1,v6]
        col7=h+[1]
        assert all((a-rho*b)%P==0 for a,b in zip(col6,col7))
        return None,'alpha_zero'
    eta={6:eta6,7:1};v={0:t,6:v6}
    for k in range(1,6):
        matrix=[[s1[k],r1[k]],[s2[k],r2[k]]]
        if determinant(matrix)==0:return None,'Delta_zero'
        eta[k],v[k]=solve(matrix,[-q1[k],-q2[k]])
    c=[[int(i==j) if i==j else (h[i]*eta[j]%P if i<j else l[i]*v[j]%P) for j in range(8)] for i in range(8)]
    b=[[sum(POW[i][k]*c[k][PERM[j]] for k in range(8))%P for j in range(8)] for i in range(8)]
    assert all((b[i][1]-beta*b[i][0])%P==0 for i in range(2,8))
    assert all((b[i][2]-rho*b[i][0])%P==0 for i in range(3,8))
    assert all((b[1][j]-g1*b[0][j])%P==0 for j in range(2,8))
    assert all((b[2][j]-g2*b[0][j])%P==0 for j in range(3,8))
    return (c,b,l,v,eta),'ok'


def b_minors(b):
    residual={}
    for i in range(2,7):
        for j in range(1,i):residual[f'lower_{i}_{j}']=(b[i][j]*b[7][0]-b[i][0]*b[7][j])%P
    for i in range(1,6):
        for j in range(i+1,7):residual[f'upper_{i}_{j}']=(b[i][j]*b[0][7]-b[i][7]*b[0][j])%P
    assert len(residual)==30
    return residual


def run(src,out):
    start=time.monotonic()
    assert pow(Z,8,P)==1 and pow(Z,4,P)==P-1
    count=Counter();extra=Counter();reject=Counter();badcount=Counter();guard=Counter();certs=[]
    source_expected=json.loads((src/'exhaustive_GF17_chart.json').read_text())
    qdata=poly_mod(json.loads((src/'exact_spectral_minor.json').read_text())['terms'])
    cc=json.loads((src/'five_parameter_circuit.json').read_text())
    saved_g=[[[poly_mod(pol) for pol in entry] for entry in row] for row in cc['upper_matrix']]
    for hv in itertools.product(range(P),repeat=4):
        h0,h1,h2,h6=hv
        if not h0:extra['h0_zero_not_enumerated']+=1;continue
        count['h_checked']+=1
        hs=[sum(a*b for a,b in zip(w,hv[:3]))%P for w in HEAD_WEIGHTS]
        h=hs[:6]+[h6]
        r0=tail_residual(tail_scaled(hs,h6,0,0))
        rt=tail_residual(tail_scaled(hs,h6,1,0))
        rb=tail_residual(tail_scaled(hs,h6,0,1))
        sys=[[(rt[i]-r0[i])%P,(rb[i]-r0[i])%P] for i in range(2)]
        if determinant(sys)==0:count['tail_linear_exception']+=1;continue
        t,beta=solve(sys,[-v for v in r0])
        if not t:count['t_zero']+=1;continue
        lhat=tail_scaled(hs,h6,t,beta)
        assert tail_residual(lhat)==[0,0]
        x=[t,*hv,beta]
        q=lower_det(h,lhat)
        assert q==peval(qdata,x)
        extra['Q_export_direct_determinant_comparisons']+=1
        if q:extra['Q_nonzero_rejected']+=1;continue
        count['tail_plus_quartic']+=1
        qbeta=(lower_det(h,tail_scaled(hs,h6,t,(beta+1)%P))-q)%P
        extra['tail_plus_quartic_with_Q_beta_coefficient_zero']+=int(qbeta==0)
        ds,rs=upper_coefficients(h,lhat)
        grank=0 if not any(b or c for _,b,c in rs) else 1
        if any((rs[i][1]*rs[j][2]-rs[i][2]*rs[j][1])%P for i in range(3) for j in range(i+1,3)):grank=2
        extra[f'upper_gamma_coefficient_matrix_rank_{grank}']+=1
        from_data=[]
        for row in saved_g:
            vals=[]
            for entry in row:
                vals.append(sum(pow(beta,d,P)*peval(pol,x[:5]) for d,pol in enumerate(entry))%P)
            from_data.append(vals)
        assert rs==from_data
        extra['upper_coefficient_matrix_comparisons']+=1
        # Exhaust all pairs, including cases where no gamma pivot can be divided.
        for g1,g2 in itertools.product(range(P),repeat=2):
            extra['gamma_pairs_examined']+=1
            if any((a+b*g1+c*g2)%P for a,b,c in rs):continue
            # Independently cross-check through the component determinants.
            vals={k:((a+b*g1+c*g2)%P,d) for k,(a,b,c,d) in ds.items()}
            assert all((vals[4][0]*vals[k][1]-vals[k][0]*vals[4][1])%P==0 for k in (1,2,5))
            count['upper_necessary_gamma_pairs']+=1
            obj,reason=reconstruct(h,hs,lhat,t,beta,g1,g2)
            if obj is None:
                count['eight_param_exception']+=1;reject[reason]+=1;continue
            c,b,l,v,eta=obj
            rank,ainv=inverse_and_rank(c)
            count[f'C_rank_{rank}']+=1
            residual=b_minors(b)
            assert all(value==0 for name,value in residual.items() if name.endswith('_1') or name.endswith('_2') and name.startswith('lower_') or name.startswith('upper_1_') or name.startswith('upper_2_'))
            if rank<8:continue
            count['invertible_candidate']+=1
            extra['invertible_candidate_with_Q_beta_coefficient_zero']+=int(qbeta==0)
            assert all(sum(c[i][k]*ainv[k][j] for k in range(8))%P==int(i==j) for i in range(8) for j in range(8))
            bp=[[b[i][PERM.index(j)] for j in range(8)] for i in range(8)]
            assert all(sum(bp[i][k]*ainv[k][j] for k in range(8))%P==POW[i][j] for i in range(8) for j in range(8))
            successes=not any(residual.values())
            count['full_B_success']+=int(successes)
            badcount[str(sum(v!=0 for v in residual.values()))]+=1
            zero_guards=[]
            if not b[7][0]:zero_guards.append('B70')
            if not b[0][7]:zero_guards.append('B07')
            if not ainv[7][0]:zero_guards.append('A70')
            if not ainv[0][7]:zero_guards.append('A07')
            for name in zero_guards:guard[name+'_zero']+=1
            guard['all_four_corners_nonzero' if not zero_guards else 'one_or_more_corners_zero']+=1
            # Endpoint inverse formulas, checked against the independently computed inverse.
            lowprod=1;upprod=1
            for k in range(1,7):
                lowprod=lowprod*(1-l[k]*v[k])%P
                upprod=upprod*(1-h[k]*eta[k])%P
            det=determinant(c)
            assert ainv[7][0]*det%P==(-t*lowprod)%P
            assert ainv[0][7]*det%P==(-h0*upprod)%P
            certs.append({'parameters':x+[g1,g2],'det_C':det,'B70':b[7][0],'B07':b[0][7],
                          'A70':ainv[7][0],'A07':ainv[0][7],
                          'B_residuals':[residual[k] for k in sorted(residual)],
                          'zero_corner_guards':zero_guards})
    expected=source_expected['counts']
    matches=dict(count)==expected
    assert matches,{'actual':dict(count),'expected':expected}
    assert len(certs)==2546 and count['full_B_success']==0
    examples=[{'param':v['parameters'],'B_success':not any(v['B_residuals']),
               'nonzero_constraints':sum(bool(u) for u in v['B_residuals'])} for v in certs[:8]]
    assert examples==source_expected['examples']
    out.mkdir(parents=True,exist_ok=True)
    certobj={'prime':P,'root':Z,'permutation':PERM,'residual_order':sorted(b_minors([[0]*8 for _ in range(8)])),
             'candidates':certs}
    certbytes=(json.dumps(certobj,indent=2)+'\n').encode()
    (out/'independent_candidate_certificates.json').write_bytes(certbytes)
    files=['PROOF_CERTIFICATE.md','exhaust_smallfield.py','general_onion.py','dual_support.py',
           'adjacent_tail.py','upper_minor.py','exact_upper.py','exact_minor.py','five_parameter_gate.py',
           'exhaustive_GF17_chart.json','exact_spectral_minor.json','five_parameter_circuit.json']
    result={'prime':P,'root':Z,'permutation':PERM,'source_code_executed':False,
            'independent_method':'Vandermonde interpolation; Fourier determinants; every gamma pair; generic linear solves; direct C/B matrices and all 30 anchored minors',
            'counts':dict(count),'matches_every_submitted_counter':matches,'matches_all_eight_submitted_examples':True,
            'full_matrix_F_equals_BPA_checked_on_all_invertible_candidates':True,
            'additional_counts':dict(extra),'first_failed_reconstruction_guard_counts':dict(reject),
            'invertible_candidate_corner_guards':dict(guard),'nonzero_B_minor_count_histogram':dict(sorted(badcount.items(),key=lambda kv:int(kv[0]))),
            'candidate_certificates_sha256':hashlib.sha256(certbytes).hexdigest(),
            'candidate_examples':certs[:8],
            'source_sha256':{f:hashlib.sha256((src/f).read_bytes()).hexdigest() for f in files},
            'elapsed_seconds':round(time.monotonic()-start,3),
            'scope':'No solutions in this GF(17), z=9, fixed-P8 open chart. Does not cover extension fields, characteristic zero, other roots/permutations, singular tail systems, h0=0, t=0, or rational-reconstruction exceptions. Candidate count is a superset of the fully corner-regular locus; every candidate is rejected by a genuine B minor.'}
    (out/'independent_gf17_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('candidate_examples','source_sha256')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    parser.add_argument('--source-root',type=Path,default=here.parent/'extracted'/'fft_spectral_determinant_gate_2026-10-09')
    parser.add_argument('--output-dir',type=Path,default=here)
    args=parser.parse_args();run(args.source_root,args.output_dir)
