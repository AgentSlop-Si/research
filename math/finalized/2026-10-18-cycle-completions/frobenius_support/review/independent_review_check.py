#!/usr/bin/env python3
"""Independent reconstruction; no candidate or inherited code execution/import."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from functools import lru_cache

P,N,Q = 53,13,16
SOURCE = Path(__file__).resolve().parent.parent / 'candidate'
OUT = Path(__file__).resolve().parent

def sha(b): return hashlib.sha256(b).hexdigest()

def peval(h,x):
    value=0
    for a in h[::-1]: value=(value*x+a)%P
    return value

@lru_cache(None)
def G(e,d,a,b):
    r,ell=(e*a)%N,(d*b)%N
    if r+ell>=N: return 0
    omega=pow(Q,(e*d)%N,P)
    # Product over r, unlike the candidate's additive Pascal recurrence.
    num=den=1
    for i in range(1,r+1):
        num=num*(1-pow(omega,ell+i,P))%P
        den=den*(1-pow(omega,i,P))%P
    assert den
    return num*pow(den,-1,P)%P

def target(a,b):
    # Literal Weyl extraction from F[t+a,t]=q^(-(t+a)t).
    coefficient=sum(pow(Q,(-((t+a)%N)*t-b*t)%N,P) for t in range(N))*pow(N,-1,P)%P
    return coefficient*pow(7,-1,P)%P

@lru_cache(None)
def moment_poly(a,b):
    assert b<=a<=12-b
    gp=G(1,1,a,b)
    gi=G(-1,1,13-b,b)
    assert gp and gi
    degree=13-a-b
    v=[0]*(degree+1)
    v[0]=target(a,b)*pow(gp,-1,P)%P
    v[degree]=-G(-1,1,a,b)*pow(gi*gp%P,-1,P)%P
    return tuple(v)

def last_poly(h):
    out=[0]*9
    for j,c in enumerate(h):
        for k,v in enumerate(moment_poly(4+j,1)):
            out[k]=(out[k]+c*v)%P
    return out

def rref(a):
    rows=[[(v%P) for v in row] for row in a]
    rank=0; pivots=[]
    for j in range(len(rows[0])-1):
        found=next((i for i in range(rank,len(rows)) if rows[i][j]),None)
        if found is None: continue
        rows[found],rows[rank]=rows[rank],rows[found]
        inv=pow(rows[rank][j],-1,P)
        rows[rank]=[v*inv%P for v in rows[rank]]
        for i in range(len(rows)):
            if i!=rank:
                c=rows[i][j]
                rows[i]=[(v-c*w)%P for v,w in zip(rows[i],rows[rank])]
        pivots.append(j);rank+=1
        if rank==len(rows): break
    return rows,pivots

def main():
    bindings={}
    manifest=json.loads((SOURCE/'SHA256SUMS.json').read_text())
    for name,expected in manifest.items():
        body=(SOURCE/name).read_bytes()
        assert sha(body)==expected,(name,'candidate manifest mismatch')
        bindings[name]={'sha256':sha(body),'bytes':len(body)}
    pins=json.loads((SOURCE/'SOURCE_PINS.json').read_text())
    for pin in pins:
        b=(SOURCE/pin['local_path']).read_bytes()
        assert sha(b)==pin['local_sha256']
        if 'git_blob' in pin:
            git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            assert git==pin['git_blob']
            bindings[pin['local_path']]['git_blob']=git
    assert pow(Q,N,P)==1 and all(pow(Q,i,P)!=1 for i in range(1,N))
    gamma=sum(pow(Q,-t*t%N,P) for t in range(N))*pow(N,-1,P)%P
    assert gamma==7
    for a in range(N):
        for b in range(N):
            assert target(a,b)==pow(Q,10*(a+b)**2%N,P)
    reflection_checks=0
    for e in [-1,1]:
        for d in [-1,1]:
            for a in range(N):
                for b in range(N):
                    assert G(e,d,a,b)==G(-e,-d,-a%N,-b%N)
                    assert target(a,b)==target(-a%N,-b%N)
                    reflection_checks+=1
    # Verify support isolation throughout all forced windows, independently.
    for b in range(1,7):
        a=13-b
        assert G(-1,1,a,b)
        assert not any(G(e,d,a,b) for e,d in [(1,1),(1,-1),(-1,-1)])
        for a in range(b,13-b):
            assert G(1,1,a,b)
            assert G(1,-1,a,b)==G(-1,-1,a,b)==0
    u=[moment_poly(a,1)[0] for a in range(4,12)]
    v=[-moment_poly(a,1)[-1]%P for a in range(4,12)]
    assert u==[19,45,51,21,12,21,49,6]
    assert v==[1,16,25,40,36,46,41,12]
    def displayed(h):
        return [sum(x*y for x,y in zip(u,h))%P]+[-v[7-k]*h[7-k]%P for k in range(8)]
    # Affine coefficientwise checking gives every h in F53^7, no parameter sample inference.
    basis=[[int(i==j) for i in range(8)] for j in range(8)]
    for h in basis: assert last_poly(h)==displayed(h)
    for h0 in range(P):
        h=[h0]+[0]*6+[1]
        ph=last_poly(h)
        assert ph[8]==-h0%P
        assert ph[1]==41 # -12, independent of all lower coefficients
        assert any(ph)
    # All 53 values of every coefficient, with the other free coefficients zero.
    exceptional_controls=0
    for j in range(7):
        for value in range(P):
            h=[0]*7+[1];h[j]=value
            ph=last_poly(h)
            assert ph==displayed(h) and ph[1]==41
            for y in range(P):
                assert peval(ph,y)==sum(h[k]*peval(moment_poly(4+k,1),y) for k in range(8))%P
            exceptional_controls+=1
    windows=[(1,a) for a in range(1,5)]+[(2,2),(2,3)]
    fresh=[];hist=Counter();degree_hist=Counter();zero_h0=0
    ranks=[]
    for y in range(1,P):
        E=[[peval(moment_poly(a+j,b),y) for j in range(8)] for b,a in windows]
        reduced,pivots=rref([row[:7]+[-row[7]%P] for row in E])
        assert pivots==list(range(6))
        ranks.append({'y':y,'rank':len(pivots),'pivots':pivots})
        for lam in range(P):
            h=[(row[7]-row[6]*lam)%P for row in reduced]+[lam,1]
            assert all(sum(c*x for c,x in zip(row,h))%P==0 for row in E)
            roots=[x for x in range(1,P) if peval(h,x)==0]
            assert len(roots)<7
            ph=last_poly(h)
            assert peval(ph,y)==0 and ph[1]==41
            degree=max(i for i,x in enumerate(ph) if x)
            if h[0]: assert degree==8
            else: zero_h0+=1
            degree_hist[degree]+=1;hist[len(roots)]+=1
            fresh.append({'y':y,'lambda':lam,'H':h,'nonzero_roots':roots})
    candidate=json.loads((SOURCE/'BASEFIELD_PREMISE_REGRESSION.json').read_text())
    assert fresh==candidate
    # Top coefficient alone is not essential to the orbit descent: monicity prevents zero polynomial.
    zero_constant=last_poly([0,1,0,0,0,0,0,1])
    assert zero_constant[8]==0 and zero_constant[7]!=0 and zero_constant[1]==41
    # Degree 37 chart exceptions cannot hide in a <=8-degree descent root over coprime degrees.
    f37=[35,0,0,17,49,13,18,6,21,47,41,6,37,8,18,3,51,33,26,11,50,50,16,3,24,25,25,9,32,7,44,49,45,2,40,14,41,1]
    assert all(peval(f37,y) for y in range(P))
    results={'verdict':'PASS','candidate_code_executed':False,
      'gaussian_method':'Finite product over r, independent of candidate additive recurrence',
      'literal_target_coefficient_checks':169,'gamma':gamma,
      'reflection_checks':reflection_checks,'last_window_u':u,'last_window_v':v,
      'formal_affine_basis_checks':8,'individual_coefficient_specializations':exceptional_controls,
      'leading_coefficient':'-h0','unconditional_Y_coefficient':41,
      'base_field_polynomials':len(fresh),'nonzero_root_evaluations':len(fresh)*52,
      'root_count_histogram':dict(sorted(hist.items())), 'max_nonzero_roots':max(hist),
      'all_basefield_census_records_match':True,'basefield_matrix_ranks':ranks,
      'descent_polynomial_degree_histogram':dict(sorted(degree_hist.items())),
      'zero_h0_polynomials':zero_h0,
      'mutation_observation':'h0=0 lowers exact degree but does not invalidate nonzero-polynomial descent because Y coefficient is -12',
      'inherited_dependencies_not_replayed':['all-extension degree-six lower-bound minors','eighteen-bank raw matrix inverses'],
      'source_bindings':bindings,'failures':0}
    (OUT/'INDEPENDENT_ARITHMETIC.json').write_text(json.dumps(results,indent=2)+'\n')
    (OUT/'FRESH_BASEFIELD_CENSUS.json').write_text(json.dumps(fresh,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k not in ['source_bindings','basefield_matrix_ranks']},indent=2))

if __name__=='__main__':main()
