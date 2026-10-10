#!/usr/bin/env python3
"""Independent data-only audit. Never imports or executes submitted Python.
Sparse polynomial arithmetic uses integer coefficients and a distinguished z
exponent; all z powers are reduced by z^4=-1 at every operation.
"""
import argparse, collections, hashlib, itertools, json, math, random
from fractions import Fraction
from pathlib import Path

class Poly:
    def __init__(self, terms=None): self.d={k:int(v) for k,v in (terms or {}).items() if v}
    @staticmethod
    def c(n): return Poly({(0,()):n})
    @staticmethod
    def x(i): return Poly({(0,(i,)):1})
    @staticmethod
    def z(e):
        e%=8
        return Poly({(e%4,()):1 if e<4 else -1})
    def __add__(self,o):
        if isinstance(o,int): o=Poly.c(o)
        d=self.d.copy()
        for k,v in o.d.items(): d[k]=d.get(k,0)+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self): return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,o): return self+(-o if isinstance(o,Poly) else -int(o))
    def __rsub__(self,o): return -self+o
    def __mul__(self,o):
        if isinstance(o,int): o=Poly.c(o)
        d=collections.defaultdict(int)
        for (a,m),v in self.d.items():
            for (b,n),w in o.d.items():
                e=a+b
                d[(e%4,tuple(sorted(m+n)))]+=v*w*(1 if e<4 else -1)
        return Poly(d)
    __rmul__=__mul__
    def __eq__(self,o): return isinstance(o,Poly) and self.d==o.d
    def evaluate(self,x,p,w):
        return sum(c*pow(w,e,p)*math.prod(x[i] for i in m) for (e,m),c in self.d.items())%p
    def grouped(self):
        d=collections.defaultdict(lambda:[0]*4)
        for (e,m),v in self.d.items(): d[m][e]=v
        return dict(d)

P=[7,0,6,3,4,1,2,5]
O=Poly.c(1); Z=Poly.c(0)
def det(A):
    """Subset expansion, independently usable over Fraction or Poly."""
    n=len(A); dp={0:1}
    for row in range(n):
        nq={}
        for mask,val in dp.items():
            for col in range(n):
                if mask>>col&1: continue
                sign=-1 if (mask>>(col+1)).bit_count()%2 else 1
                nm=mask|(1<<col)
                term=val*A[row][col]*sign
                nq[nm]=nq.get(nm,0)+term
        dp=nq
    return dp[(1<<n)-1]

def stage(L,V,U,W,D):
    return [[D[i] if i==j else L[i]*V[j] if i>j else U[i]*W[j] for j in range(len(D))] for i in range(len(D))]

def image(C):
    return [[sum(Poly.z(i*k)*C[k][P[j]] for k in range(8)) for j in range(8)] for i in range(8)]

def minors(B):
    out={}
    for i in range(2,7):
        for j in range(1,i): out[f'lower_{i}_{j}']=B[i][j]*B[7][0]-B[i][0]*B[7][j]
    for i in range(1,6):
        for j in range(i+1,7): out[f'upper_{i}_{j}']=B[i][j]*B[0][7]-B[i][7]*B[0][j]
    return out

def read_export(path):
    obj=json.loads(path.read_text()); out={}
    for eq in obj['equations']:
        d={}; previous=None
        for m,c in eq['terms']:
            m=tuple(m)
            assert list(m)==sorted(m) and all(isinstance(v,int) for v in m)
            assert previous is None or previous<m, 'duplicate or unsorted monomial'
            previous=m
            assert len(c)==4 and any(c) and all(isinstance(v,int) for v in c)
            for e,v in enumerate(c):
                if v: d[(e,m)]=v
        assert eq['name'] not in out
        out[eq['name']]=Poly(d)
    return obj,out

def compare(expected,path,nvar):
    obj,actual=read_export(path)
    assert set(actual)==set(expected)
    assert all(actual[k]==v for k,v in expected.items()),path
    grouped=[q.grouped() for q in actual.values()]
    assert all(0<=i<nvar for q in grouped for m in q for i in m)
    return dict(equations=len(actual),variables=nvar,maximum_degree=max(len(m) for q in grouped for m in q),terms=sum(map(len,grouped)),distinct_monomials=len({m for q in grouped for m in q}),all_coefficients_match=True,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def inverse_mod(A,p):
    n=len(A);a=[[int(v)%p for v in r]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
    for c in range(n):
        row=next((i for i in range(c,n) if a[i][c]),None)
        if row is None: return None
        a[c],a[row]=a[row],a[c];q=pow(a[c][c],-1,p);a[c]=[v*q%p for v in a[c]]
        for i in range(n):
            if i!=c:
                q=a[i][c];a[i]=[(u-q*v)%p for u,v in zip(a[i],a[c])]
    return [r[n:] for r in a]

def matmul(A,B,p=None):
    C=[[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
    return C if p is None else [[v%p for v in r] for r in C]

def numeric_minors(B,p):
    return [(B[i][j]*B[7][0]-B[i][0]*B[7][j])%p for i in range(2,7) for j in range(1,i)]+[(B[i][j]*B[0][7]-B[i][7]*B[0][j])%p for i in range(1,6) for j in range(i+1,7)]

def main(src,out):
    report={'method':'All arithmetic and checks independently authored; uploaded Python read as data only.'}
    x=[Poly.x(i) for i in range(26)]
    L=[Z]+x[:6]+[O];V=x[6:13]+[Z];U=[O]+x[13:19]+[Z];W=[Z]+x[19:26]
    C=stage(L,V,U,W,[O]*8);B=image(C);E=minors(B)
    report['quartic']=compare(E,src/'quartic_cyclotomic_equations.json',26)
    # Independent cofactor expansion, without assuming nonzero row generators.
    lower_cof=-det([[C[i][j] for j in range(7)] for i in range(1,8)])
    upper_cof=-det([[C[i][j] for j in range(1,8)] for i in range(7)])
    lower_formula=-V[0];upper_formula=-W[7]
    for k in range(1,7):
        lower_formula=lower_formula*(O-L[k]*V[k]); upper_formula=upper_formula*(O-U[k]*W[k])
    assert lower_cof==lower_formula and upper_cof==upper_formula
    out.mkdir(parents=True,exist_ok=True)
    def encoded(poly):
        return [[list(m),c] for m,c in sorted(poly.grouped().items())]
    (out/'corner_cofactor_certificate.json').write_text(json.dumps({'ring':'Z[z]/(z^4+1)','variable_order':'L1..L6,V0..V6,U1..U6,W1..W7','lower_adjugate_70':encoded(lower_cof),'upper_adjugate_07':encoded(upper_cof),'verified_by_independent_subset_determinant':True},indent=2)+'\n')
    report['new_corner_cofactor_identity']={'n8_formal_all_coefficients_match':True,'lower_cofactor_monomials':len(lower_cof.grouped()),'upper_cofactor_monomials':len(upper_cof.grouped()),'maximum_degree':max(len(m) for m in lower_cof.grouped()),'formula':'adj(C)[n-1,0] = -L[n-1]*V[0]*product(d[k]-L[k]*V[k], k=1..n-2); upper is the transpose version.'}
    y=[Poly.x(i) for i in range(21)];t=y[0];vv=[t]+y[1:7]+[Z];h=y[7:14];eta=[Z]+y[14:20]+[O];beta=y[20];lam=Poly.z(1)-1;D=t*lam
    numer=t-1+beta*(h[0]-1)
    T={k:lam*(1-beta*h[0]+beta*h[k])+numer*(Poly.z(-k)-1) for k in range(1,7)}
    Q=[]
    for i in range(8):
        row=[]
        for j in range(8):
            if i==j: a=D
            elif i>j: a=(D if i==7 else T[i])*vv[j]
            else: a=D*h[i]*eta[j]
            row.append(a)
        Q.append(row)
    R=image(Q);all_red=minors(R);zero=[k for k,v in all_red.items() if not v.d]
    assert set(zero)=={f'lower_{i}_1' for i in range(2,7)}
    report['sextic']=compare({k:v for k,v in all_red.items() if v.d},src/'reduced_sextic_equations.json',21)
    report['sextic']['five_removed_equations_identically_zero']=True
    primitive={};removed_t_powers={}
    for name,poly in all_red.items():
        if not poly.d: continue
        power=min(m.count(0) for _,m in poly.d);removed_t_powers[name]=power
        pp=Poly({(e,m[power:]):c for (e,m),c in poly.d.items()})
        back=pp
        for _ in range(power):back=back*t
        assert back==poly
        primitive[name]=pp
    primitive_obj={'ring':'Z[z]/(z^4+1)','variables':['t']+[f'V{i}' for i in range(1,7)]+[f'h{i}' for i in range(7)]+[f'eta{i}' for i in range(1,7)]+['beta'],'condition':'Equivalent to supplied reduced system only on t != 0; all determinant and corner saturation is still required.','removed_t_powers':removed_t_powers,'equations':[{'name':name,'terms':encoded(poly)} for name,poly in primitive.items()]}
    (out/'reduced_patch_primitive_equations.json').write_text(json.dumps(primitive_obj,indent=2)+'\n')
    profile=collections.Counter(max(len(m) for _,m in poly.d) for poly in primitive.values())
    assert dict(profile)=={3:4,4:6,5:1,6:14}
    report['new_patch_primitive_system']={'equations':25,'variables':21,'degree_profile':dict(sorted(profile.items())),'removed_t_powers':removed_t_powers,'terms':sum(len(poly.grouped()) for poly in primitive.values()),'distinct_monomials':len({m for poly in primitive.values() for m in poly.grouped()}),'exact_multiplication_recovers_original':True}
    # Stronger direct support identities: B_i1=beta B_i0 for all i=2..7.
    assert all(not (R[i][1]-beta*R[i][0]).d for i in range(2,8))
    report['sextic']['six_frequency_vanishings_formally_zero']=True
    lower_gaps=[D-T[k]*vv[k] for k in range(1,7)]
    upper_gaps=[1-h[k]*eta[k] for k in range(1,7)]
    (out/'explicit_sextic_saturation_certificate.json').write_text(json.dumps({'ring':'Q[z]/(z^4+1)','variable_order':['t']+[f'V{k}' for k in range(1,7)]+[f'h{k}' for k in range(7)]+[f'eta{k}' for k in range(1,7)]+['beta'],'saturation_product':'t*h0*det(Ctilde)*Btilde70*Btilde07*product(lower_gaps)*product(upper_gaps)','lower_gaps':[encoded(a) for a in lower_gaps],'upper_gaps':[encoded(a) for a in upper_gaps],'Btilde70':encoded(R[7][0]),'Btilde07':encoded(R[0][7]),'Ctilde_determinant_matrix':[[encoded(a) for a in row] for row in Q],'meaning':'Nonzero product is exactly the stipulated regular patch, with inverse corners enforced by proved cofactor products. Determinant is supplied as a matrix expression rather than expanded.'},indent=2)+'\n')
    def degree(poly): return max((len(m) for _,m in poly.d),default=-1)
    def scale_specialize(poly,values):
        dd=collections.defaultdict(int)
        for (e,m),v in poly.d.items(): dd[(e,(0,)*len(m))]+=v*math.prod(values[i] for i in m)
        return Poly(dd)
    detC_degree=degree(det([[scale_specialize(a,list(range(2,28))) for a in row] for row in C]))
    detQ_degree=degree(det([[scale_specialize(a,list(range(2,23))) for a in row] for row in Q]))
    assert detC_degree==14 and detQ_degree==22
    report['saturation_degrees']={'detC_exact':14,'detCtilde_exact':22,'quartic_saturation_product_exact':44,'quartic_Rabinowitsch_added_equation_exact':45,'sextic_saturation_product_exact':59,'sextic_Rabinowitsch_added_equation_exact':60,'reduced_lower_gap_degrees':[degree(a) for a in lower_gaps],'reduced_upper_gap_degrees':[degree(a) for a in upper_gaps],'proof_of_determinant_degree':'Row/column degree bounds 14 and22, with exact nonzero highest-degree coefficient after integer scaling specialization.'}
    # Chart-free full system, direct flat coordinate interpretation.
    q=[Poly.x(i) for i in range(184)];complete={}
    def ix(tag,i,j): return q[(0 if tag=='A' else 64)+8*i+j]
    for tag,start in [('A',128),('B',156)]:
        ll=[Z]+q[start:start+7];v=q[start+7:start+14]+[Z];u=q[start+14:start+21]+[Z];ww=[Z]+q[start+21:start+28]
        for i in range(8):
            for j in range(8):
                if i!=j: complete[f'{tag}_offdiag_{i}_{j}']=ix(tag,i,j)-(ll[i]*v[j] if i>j else u[i]*ww[j])
    for i in range(8):
        for j in range(8): complete[f'fft_entry_{i}_{j}']=sum(ix('B',i,k)*ix('A',P[k],j) for k in range(8))-Poly.z(i*j)
    report['quadratic']=compare(complete,src/'complete_quadratic_equations.json',184)
    # Exhaustive finite field n3 zero/nonzero family, with arbitrary diagonal.
    # GF(3) 9 live parameters, generators factor normalized? Instead all 4 lower
    # and 4 upper plus 3 diagonal would be 177147. GF(2) all 11 = 2048 is exhaustive.
    n3_total=0;n3_invertible=0;n3_corner=0
    for vals in itertools.product(range(2),repeat=11):
        ds=list(vals[:3]);ll=[0]+list(vals[3:5]);v=list(vals[5:7])+[0];u=list(vals[7:9])+[0];ww=[0]+list(vals[9:11])
        S=stage(ll,v,u,ww,ds);SI=inverse_mod(S,2);n3_total+=1
        if SI is None:continue
        n3_invertible+=1
        for p1,p2 in [((2,0),-ll[2]*v[0]*(ds[1]-ll[1]*v[1])),((0,2),-u[0]*ww[2]*(ds[1]-u[1]*ww[1]))]:
            assert SI[p1[0]][p1[1]]==p2%2
        n3_corner+=1
    report['new_corner_cofactor_identity']['exhaustive_GF2_n3_assignments']=n3_total
    report['new_corner_cofactor_identity']['exhaustive_GF2_n3_invertible']=n3_invertible
    # All sizes 2..12 and zero-heavy parameters, with direct determinant minors.
    rng=random.Random(901927);tested=0
    for n in range(2,13):
        for _ in range(30):
            ds=[rng.randrange(-2,3) for _ in range(n)];ll=[0]+[rng.randrange(-2,3) for _ in range(n-1)];v=[rng.randrange(-2,3) for _ in range(n-1)]+[0];u=[rng.randrange(-2,3) for _ in range(n-1)]+[0];ww=[0]+[rng.randrange(-2,3) for _ in range(n-1)]
            S=stage(ll,v,u,ww,ds)
            lo=(-1)**(n-1)*det([[S[i][j] for j in range(n-1)] for i in range(1,n)])
            hi=(-1)**(n-1)*det([[S[i][j] for j in range(1,n)] for i in range(n-1)])
            assert lo==-ll[-1]*v[0]*math.prod(ds[k]-ll[k]*v[k] for k in range(1,n-1))
            assert hi==-u[0]*ww[-1]*math.prod(ds[k]-u[k]*ww[k] for k in range(1,n-1))
            tested+=1
    report['new_corner_cofactor_identity']['integer_zero_heavy_tests_n2_to_n12']=tested
    # Fresh modular embeddings (all 4 primitive roots in each field).
    runs=[];saturation_checks=0;regular_reduced_samples=0
    for p in [17,97,257]:
        roots=[w for w in range(1,p) if pow(w,4,p)==p-1]
        assert len(roots)==4
        for w in roots:
            F=[[pow(w,i*j,p) for j in range(8)] for i in range(8)]
            checks=0
            for _ in range(12):
                vals=[rng.randrange(p) for _ in range(26)]
                cm=[[a.evaluate(vals,p,w) for a in row] for row in C];bm=matmul(F,[[cm[k][P[j]] for j in range(8)] for k in range(8)],p)
                assert [a.evaluate(vals,p,w) for a in E.values()]==numeric_minors(bm,p)
                ys=[rng.randrange(p) for _ in range(21)];ys[0]=rng.randrange(1,p);ys[7]=rng.randrange(1,p)
                qq=[[a.evaluate(ys,p,w) for a in row] for row in Q];dd=ys[0]*(w-1)%p;cc=[[v*pow(dd,-1,p)%p for v in row] for row in qq]
                bb=matmul(F,[[cc[k][P[j]] for j in range(8)] for k in range(8)],p)
                assert all((bb[i][1]-ys[20]*bb[i][0])%p==0 for i in range(2,8))
                assert [a.evaluate(ys,p,w) for a in all_red.values()]==[v*dd*dd%p for v in numeric_minors(bb,p)]
                ai=inverse_mod(cc,p)
                factors=[a.evaluate(ys,p,w) for a in lower_gaps+upper_gaps]
                patch_by_factors=bool(det(qq)%p and bb[7][0] and bb[0][7] and all(factors))
                patch_by_inverse=bool(ai is not None and bb[7][0] and bb[0][7] and ai[7][0] and ai[0][7])
                assert patch_by_factors==patch_by_inverse
                saturation_checks+=1;regular_reduced_samples+=patch_by_factors
                # Coordinate round trip from reduced to quartic, including zero interior generators.
                zs=[cc[k][0]*pow(ys[0],-1,p)%p for k in range(1,7)]+[ys[0]]+ys[1:7]+[ys[7+k]*pow(ys[7],-1,p)%p for k in range(1,7)]+[ys[7]*e%p for e in ys[14:20]]+[ys[7]]
                assert cc==[[a.evaluate(zs,p,w) for a in row] for row in C]
                # If regular lower output corner holds, beta is uniquely recovered.
                if bb[7][0]: assert bb[7][1]*pow(bb[7][0],-1,p)%p==ys[20]
                checks+=1
            runs.append({'p':p,'z':w,'zero_inclusive_quartic_and_sextic_samples':checks})
    report['independent_modular_checks']=runs
    report['explicit_saturation']={'reduced_factor_test_matches_inverse_corner_test':saturation_checks,'regular_among_tested':regular_reduced_samples}
    # Complete lift positive controls with independently chosen sparse generators.
    controls=0
    for p,w in [(17,2),(97,33)]:
        assert pow(w,4,p)==p-1
        for sparsity in [0,1,2,3]:
            for _ in range(12):
                vals=[0]*184; mats=[]
                for offset,gstart in [(0,128),(64,156)]:
                    for i in range(8): vals[offset+8*i+i]=rng.randrange(1,p)
                    for i in range(28): vals[gstart+i]=0 if sparsity==0 or rng.randrange(4)<sparsity else rng.randrange(p)
                    for i in range(8):
                        for j in range(8):
                            if i>j:vals[offset+8*i+j]=vals[gstart+i-1]*vals[gstart+7+j]%p
                            if i<j:vals[offset+8*i+j]=vals[gstart+14+i]*vals[gstart+21+j-1]%p
                    mats.append([vals[offset+i*8:offset+(i+1)*8] for i in range(8)])
                A,BB=mats;prod=matmul(BB,[A[k] for k in P],p)
                for name,eq in complete.items():
                    v=eq.evaluate(vals,p,w)
                    if name.startswith('fft_'):
                        i,j=map(int,name.split('_')[-2:]);assert v==(prod[i][j]-pow(w,i*j,p))%p
                    else: assert v==0
                controls+=1
    report['quadratic']['synthetic_sparse_and_zero_anchor_controls']=controls
    # The old forward-diagonal patch and the inverse-diagonal patch differ.
    af=[[Fraction(7,6)*int(i==j)-Fraction(1,6) for j in range(8)] for i in range(8)]
    cf=[[Fraction(6,7)*int(i==j)-Fraction(6,7) for j in range(8)] for i in range(8)]
    assert matmul(af,cf)==[[int(i==j) for j in range(8)] for i in range(8)]
    assert all(af[i][i]==1 and cf[i][i]==0 for i in range(8))
    report['forward_vs_inverse_diagonal_patch']={'exact_rational_check':True,'A':'(7/6)*I-(1/6)*J','C_inverse_of_A':'(6/7)*I-(6/7)*J','A_diagonal':1,'C_diagonal':0,'all_four_corner_anchors_nonzero':True,'scope':'This stage-level example distinguishes chart domains; it is not an F8 factorization.'}
    # Exact exceptional examples and singular Fourier roots.
    c3=[[Fraction(v) for v in row] for row in [[2,1,1],[1,1,1],[1,1,3]]]
    a3=[[Fraction(v) for v in row] for row in [[1,-1,0],[-1,Fraction(5,2),Fraction(-1,2)],[0,Fraction(-1,2),Fraction(1,2)]]]
    assert matmul(c3,a3)==[[Fraction(int(i==j)) for j in range(3)] for i in range(3)]
    assert det(c3)==2 and a3[2][0]==0 and a3[1][0]*a3[2][1]!=0
    # Exact symbolic Fourier row sums, no finite-field inference needed.
    ones=[1]*26
    assert all(a.evaluate(ones,17,2)==0 for a in E.values())
    assert all(sum(Poly.z(i*k) for k in range(8))==(Poly.c(8) if i==0 else Z) for i in range(8))
    # The all-ones C false positive persists for EVERY beta in the reduced system.
    # Substitute all variables except beta by 1, retaining beta formally.
    def substitute_ones_except(poly,keep):
        dd=collections.defaultdict(int)
        for (e,m),v in poly.d.items():dd[(e,tuple(i for i in m if i==keep))]+=v
        return Poly(dd)
    assert all(not substitute_ones_except(eq,20).d for eq in all_red.values())
    assert all(substitute_ones_except(Q[i][j],20)==lam for i in range(8) for j in range(8))
    report['reduced_singular_beta_line']={'formal_identity':True,'assignment':'t=V1=...=V6=h0=...=h6=eta1=...=eta6=1; beta arbitrary','C':'all-ones rank-one matrix','all_25_sextics':'zero identically in beta'}
    report['exceptional_examples']={'inverse_boundary_exact_rational_identity':True,'all_ones_false_positive_exact_cyclotomic_identity':True}
    # Check every hash listed by uploader, as provenance only.
    manifest=[]
    for line in (src/'SHA256SUMS.txt').read_text().splitlines():
        if not line.strip():continue
        digest,name=line.split(maxsplit=1);name=name.lstrip('*');path=src/name
        manifest.append({'file':name,'match':path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest})
    report['manifest']={'entries':len(manifest),'all_match':all(x['match'] for x in manifest),'mismatches':[x for x in manifest if not x['match']]}
    out.mkdir(parents=True,exist_ok=True);(out/'independent_inverse_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parent.parent/'source_material'/'fft_inverse_quartic_gate_2026-10-09');ap.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent);a=ap.parse_args();main(a.source_dir,a.output_dir)
