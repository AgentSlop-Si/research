#!/usr/bin/env python3
"""Fresh stdlib-only Phase16 audit. Source files are data, never imported/executed."""
import ast
from collections import deque
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import hashlib,json,math,random,sys,zipfile

P=65537
R=random.Random(161022)

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def matmul(A,B): return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*B)] for row in A]
def matadd(A,B,c=1): return [[(x+c*y)%P for x,y in zip(a,b)] for a,b in zip(A,B)]
def rank(A):
    A=[r[:] for r in A]; k=0
    for j in range(len(A[0])):
        q=next((q for q in range(k,len(A)) if A[q][j]%P),None)
        if q is None: continue
        A[k],A[q]=A[q],A[k]; f=pow(A[k][j],-1,P); A[k]=[f*v%P for v in A[k]]
        for q in range(k+1,len(A)):
            f=A[q][j]
            if f: A[q]=[(x-f*y)%P for x,y in zip(A[q],A[k])]
        k+=1
        if k==len(A):break
    return k

def inverse(A):
    n=len(A); B=[r[:]+ident(n)[i] for i,r in enumerate(A)]
    for j in range(n):
        q=next((q for q in range(j,n) if B[q][j]%P),None)
        if q is None: raise ValueError('singular')
        B[j],B[q]=B[q],B[j]; f=pow(B[j][j],-1,P); B[j]=[f*v%P for v in B[j]]
        for q in range(n):
            if q!=j:
                f=B[q][j]
                if f:B[q]=[(x-f*y)%P for x,y in zip(B[q],B[j])]
    return [r[n:] for r in B]

def maps(s):
    return [[((x+2*y+k)%s)*s+y for x in range(s) for y in range(s)] for k in [0,1]]+[[x*s+(y+2*x+k)%s for x in range(s) for y in range(s)] for k in [0,1]]
def half(s):return [x*s+(y+s//2)%s for x in range(s) for y in range(s)]
def green(pi,w):
    A=ident(len(pi))
    for i,j in enumerate(pi):A[i][j]=(A[i][j]-w[i])%P
    return inverse(A)
def pureweights(plans,c,d):return [[v*d[i]*pow(d[pi[i]],-1,P)%P for i in range(len(d))] for pi,v in zip(plans,c)]
def monomial(tau,d):
    n=len(d); M=[[0]*n for _ in d]
    for j in range(n):M[tau[j]][j]=d[tau[j]]*pow(d[j],-1,P)%P
    return M

def forest(plans,weights,c):
    n=len(plans[0]); edges=[[] for _ in range(n)]
    for t,pi in enumerate(plans):
        for i,j in enumerate(pi):
            z=c[t]*pow(weights[t][i],-1,P)%P
            edges[i].append((j,z));edges[j].append((i,pow(z,-1,P)))
    d=[None]*n; components=0
    for root in range(n):
        if d[root] is not None:continue
        components+=1;d[root]=1;todo=deque([root])
        while todo:
            i=todo.popleft()
            for j,z in edges[i]:
                if d[j] is None:d[j]=d[i]*z%P;todo.append(j)
    w0=pureweights(plans,c,d)
    defects=[(t,i) for t in range(len(plans)) for i in range(n) if weights[t][i]!=w0[t][i]]
    return d,components,defects

# A quotient tower over Q: i^2=-1, a^2=1-2i, b^2=1+8i, c^2=1-16i.
# Inverses explicitly prove units, so all resulting identities hold under every
# complex embedding, including the supplied principal square-root choices.
def vadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vneg(a):return tuple(-x for x in a)
def vsub(a,b):return vadd(a,vneg(b))
def radicand(n):
    if n==2:return (Q(-1),)
    return (Q(1),Q({4:-2,8:8,16:-16}[n]))+(Q(0),)*(n//2-2)
@lru_cache(None)
def vmul(a,b):
    n=len(a)
    if not any(a) or not any(b):return (Q(0),)*n
    if n==1:return (a[0]*b[0],)
    h=n//2;aa,ab=a[:h],a[h:];ba,bb=b[:h],b[h:]
    return vadd(vmul(aa,ba),vmul(vmul(ab,bb),radicand(n)))+vadd(vmul(aa,bb),vmul(ab,ba))
@lru_cache(None)
def vinv(a):
    n=len(a)
    if n==1:
        if not a[0]:raise ZeroDivisionError('nonunit')
        return (1/a[0],)
    h=n//2;x,y=a[:h],a[h:]
    t=vinv(vsub(vmul(x,x),vmul(vmul(y,y),radicand(n))))
    return vmul(x,t)+vneg(vmul(y,t))
def rat(x):return (Q(x),)+(Q(0),)*15
def unit(k):return (Q(0),)*k+(Q(1),)+(Q(0),)*(15-k)
ZERO=rat(0);ONE=rat(1);IM=unit(1)
ROOTS={vsub(ONE,vmul(rat(2),IM)):unit(2),vadd(ONE,vmul(rat(8),IM)):unit(4),vsub(ONE,vmul(rat(16),IM)):unit(8)}
def parse_expr(text):
    """Strict inert-data grammar; no eval, compile, exec, import or sympify."""
    def visit(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:return rat(n.value)
        if isinstance(n,ast.Name) and n.id=='I':return IM
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return vneg(visit(n.operand))
        if isinstance(n,ast.BinOp):
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,ast.Add):return vadd(a,b)
            if isinstance(n.op,ast.Sub):return vsub(a,b)
            if isinstance(n.op,ast.Mult):return vmul(a,b)
            if isinstance(n.op,ast.Div):return vmul(a,vinv(b))
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt' and len(n.args)==1 and not n.keywords:
            return ROOTS[visit(n.args[0])]
        raise ValueError('certificate expression outside restricted grammar')
    return visit(ast.parse(text,mode='eval').body)
def vmm(A,B):
    out=[]
    for row in A:
        r=[]
        for col in zip(*B):
            v=ZERO
            for a,b in zip(row,col):v=vadd(v,vmul(a,b))
            r.append(v)
        out.append(r)
    return out

def f4_check(source):
    c=json.loads((source/'EXACT_F4_CERTIFICATE.json').read_text())
    F,X,Y=[[[parse_expr(z) for z in row] for row in c[key]] for key in ['fourier_unnormalized','first_rook_factor_X','second_rook_factor_Y']]
    powers=[ONE,vneg(IM),vneg(ONE),IM]
    assert F==[[powers[i*j%4] for j in range(4)] for i in range(4)]
    assert vmm(Y,X)==F
    for A in [X,Y]:
        assert all(A[i][j]==ZERO for i in range(4) for j in range(4) if i//2!=j//2 and i%2!=j%2)
    pis=[list(range(4)),[2,3,0,1],list(range(4)),[1,0,3,2]]
    I=[[ONE if i==j else ZERO for j in range(4)] for i in range(4)]
    invchecks=0;zero_weights=0;variable_id=[]
    for stagekey,target in [('first_stage_weight_vectors',X),('second_stage_weight_vectors',Y)]:
        total=[[ZERO]*4 for _ in range(4)]
        ws=[[parse_expr(z) for z in row] for row in c[stagekey]]
        for slot,(pi,w) in enumerate(zip(pis,ws)):
            zero_weights+=sum(z==ZERO for z in w)
            A=[r[:] for r in I]; G=[[ZERO]*4 for _ in range(4)]
            for i in range(4):A[i][pi[i]]=vsub(A[i][pi[i]],w[i])
            for i,j in enumerate(pi):
                if i==j:G[i][i]=vinv(vsub(ONE,w[i]))
                else:
                    den=vinv(vsub(ONE,vmul(w[i],w[j])))
                    G[i][i]=den;G[i][j]=vmul(w[i],den)
            assert vmm(A,G)==I and vmm(G,A)==I;invchecks+=1
            total=[[vadd(a,b) for a,b in zip(r,s)] for r,s in zip(total,G)]
            if slot==2:variable_id.append(w[0]!=w[1])
        assert total==target
    assert any(variable_id)
    # Deliberately corrupt one certificate weight and prove the affected inverse changes.
    w=parse_expr(c['first_stage_weight_vectors'][2][0]);assert vinv(vsub(ONE,w))!=vinv(vsub(ONE,vadd(w,ONE)))
    for bad in ['__import__("os")','I.real','sqrt(2)','1.5']:
        try:parse_expr(bad)
        except (ValueError,KeyError):pass
        else:raise AssertionError('unsafe expression accepted')
    return {'status':'PASS','exact_inverses_verified_both_sides':invchecks,'exact_stage_sums':2,'exact_product_YX_equals_F4':True,'zero_weight_occurrences':zero_weights,'variable_identity_generator_in_each_stage':variable_id,'variable_identity_generator_excludes_any_common_constant_reference':any(variable_id),'arithmetic':'stdlib Fraction, 16-dimensional quadratic quotient tower; strict AST data parser','principal_sqrt_dependency':'identities hold for every embedding, hence supplied branches','negative_controls':5}

def main():
    source=Path(__file__).parent/'source'
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    out={'status':'PASS','source_code_executed_or_imported':False,'dependencies':'Python standard library only'}
    exhaustive=[];nperm=0
    for n in range(2,9):
        allowed={(u,b) for u in range(n) for b in range(n) if u*u%n==1 and 2*b%n==0 and b*b%n==0};found=[]
        for tau in permutations(range(n)):
            nperm+=1;inv=[0]*n
            for j,k in enumerate(tau):inv[k]=j
            b=tau[0]
            # j=0 forces the weights a_j/a_0 = omega^(b*tau(j)).
            commutes=all((i*(tau[j]-b)+b*tau[j]-j*inv[i])%n==0 for i in range(n) for j in range(n))
            u=(tau[1]-b)%n
            classified=(u,b) in allowed and all(tau[j]==(u*j+b)%n for j in range(n))
            assert commutes==classified
            if commutes:found.append([u,b])
        exhaustive.append({'N':n,'commuting_permutation_supports':found})
    out['monomial_classification_exhaustive_permutations']=nperm;out['monomial_classification_small_sizes']=exhaustive
    vertexchecks=0
    for s in range(2,34,2):
        q=half(s);n=s*s
        for pi in maps(s):
            assert sorted(pi)==list(range(n))
            for i in range(n):assert pi[q[i]]==q[pi[i]];vertexchecks+=1
        b=q[0];u=(q[1]-b)%n
        assert not (u*u%n==1 and 2*b%n==0 and b*b%n==0 and all(q[j]==(u*j+b)%n for j in range(n)))
    out['Margulis_half_y_commutation_vertex_checks']=vertexchecks;out['exact_gauge_no_go_checked_sides']=list(range(2,34,2))
    fullranks=[]
    for s in [2,4,8]:
        n=s*s;z=pow(3,(P-1)//n,P);F=[[pow(z,i*j,P) for j in range(n)] for i in range(n)]
        for k in range(4):
            d=[1]*n if k==0 else [R.randrange(1,P) for _ in range(n)]
            M=monomial(half(s),d);C=matadd(matmul(F,M),matmul(M,F),-1);r=rank(C);assert r==n
            fullranks.append({'N':n,'gauge':k,'rank':r})
    out['fresh_gauged_commutator_ranks']=fullranks
    forestchecks=[];rankcontrols=[];conjugations=0
    for s in [2,4]:
        n=s*s;plans=maps(s);c=[2,3,5,7];d=[R.randrange(1,P) for _ in range(n)];w=pureweights(plans,c,d)
        recovered,nc,defects=forest(plans,w,c);assert not defects and pureweights(plans,c,recovered)==w
        bad=[r[:] for r in w];loop=next((t,i) for t,p in enumerate(plans) for i,j in enumerate(p) if i==j);t,i=loop;bad[t][i]=bad[t][i]*2%P
        _,_,defects=forest(plans,bad,c);assert defects==[loop]
        forestchecks.append({'s':s,'edges':4*n,'components':nc,'one_self_loop_defect':list(loop)})
        base=[green(pi,wi) for pi,wi in zip(plans,w)]
        for pi,cj,G in zip(plans,c,base):
            H=green(pi,[cj]*n)
            assert G==[[d[i]*H[i][j]*pow(d[j],-1,P)%P for j in range(n)] for i in range(n)];conjugations+=1
        M=monomial(half(s),d)
        T0=matmul(matadd(base[0],base[1],3),matadd(base[2],base[3],5));assert rank(matadd(matmul(T0,M),matmul(M,T0),-1))==0
        for k in range(7):
            changed=[r[:] for r in w]
            for slot in R.sample(range(4*n),k):
                t,i=divmod(slot,n);changed[t][i]=changed[t][i]*11%P
            gs=[green(pi,wi) for pi,wi in zip(plans,changed)]
            T=matmul(matadd(gs[0],gs[1],3),matadd(gs[2],gs[3],5));rd=rank(matadd(T,T0,-1));rc=rank(matadd(matmul(T,M),matmul(M,T),-1));assert rd<=k and rc<=2*k
            rankcontrols.append({'N':n,'changed_occurrences':k,'rank_difference':rd,'rank_commutator':rc})
    out['fresh_forest_controls']=forestchecks;out['exact_resolvent_conjugations']=conjugations;out['rank_edit_controls']=rankcontrols
    n=16;pi=maps(4)[1];a=[2]*n;b=a[:];b[0]=3;A=green(pi,a);B=green(pi,b);r1=rank(matadd(B,A,-1));r2=rank(matadd(matmul(B,B),matmul(A,A),-1));assert(r1,r2)==(1,2)
    out['shared_parameter_countercontrol']={'one_occurrence_rank':r1,'two_occurrences_rank':r2,'charged_occurrences':2}
    # Root-of-unity kernel count is equivalent to solving delta*j=e (mod N).
    kernelcases=0
    for n in range(2,81):
        for delta in range(1,n):
            g=math.gcd(n,delta)
            for e in range(n):
                z=sum(delta*j%n==e for j in range(n));assert z==(g if e%g==0 else 0);kernelcases+=1
    out['exact_root_kernel_support_cases']=kernelcases
    gaps=[]
    for s in range(3,257):
        n=s*s;p=next(t for t in range(2,n+1) if n%t==0);g=n-n//p-(2*s-1);assert g>0
        if s in [3,4,5,6,8,16,32,64,128,256]:gaps.append({'s':s,'gap':g})
    out['rook_support_gaps']=gaps;out['rook_support_sides_checked']=254
    # Exact signed-sum identity underlying the phase-only gap for small even s:
    # floating controls accompany the independent all-size proof in REVIEW.md.
    phase=[]
    for s in [4,6,8,10,12,16,20]:
        h=s//2;angles=[math.pi*y/s for y in range(h)]
        expected=1/(math.sqrt(2)*math.sin(math.pi/(2*s)))
        best=max(abs(sum(sign*complex(math.cos(a),math.sin(a)) for sign,a in zip(signs,angles))) for signs in product([-1,1],repeat=h))
        assert abs(best-expected)<1e-11
        bound=math.sqrt(2-2*math.sqrt(2)/(s*math.sin(math.pi/(2*s))))/2
        assert bound>0
        phase.append({'s':s,'signed_sum_max':best,'distance_lower_bound':bound})
    out['phase_gap_numerical_formula_controls']=phase
    # Complete the square exactly, no numerical orthogonality testing needed.
    qchecks=0
    for n in range(2,41):
        for d in range((n-1)//2+1):
            alpha=Q(d,n)
            for t in [Q(0),Q(1,3),Q(1),Q(2),alpha/(1-alpha)]:
                lhs=1+t*t-alpha*(1+t)**2
                rhs=(1-2*alpha)/(1-alpha)+(1-alpha)*(t-alpha/(1-alpha))**2
                assert lhs==rhs;qchecks+=1
    out['exact_Frobenius_quadratic_identities']=qchecks
    out['F4_certificate']=f4_check(source)
    sourcehashes=json.loads((source/'SHA256SUMS.json').read_text());assert len(sourcehashes)==17
    for name,v in sourcehashes.items():
        data=(source/name).read_bytes();assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
    out['source_manifest_entries_verified']=len(sourcehashes)
    outer=source/'fft_hero0_phase16_gauge_curvature_2026-10-10.zip'
    assert hashlib.sha256(outer.read_bytes()).hexdigest()=='2b0cabeea7b373bb47942db4e2d86f7dd8577ea5e41bb5e5bbaeab8d043847d0'
    assert hashlib.sha256((source/'prior_phase15_bundle.zip').read_bytes()).hexdigest()=='94cb33b22de6ecd0cf73c104b9f281a92abfe4ca4748f1e99577ead072dd7285'
    with zipfile.ZipFile(outer) as z:assert z.testzip() is None
    out['source_zip_and_predecessor_identity_verified']=True
    tree=ast.parse((source/'test_phase16.py').read_text());testcount=sum(isinstance(n,ast.FunctionDef) and n.name.startswith('test_') for n in ast.walk(tree));assert testcount==19
    out['source_test_definitions_counted_not_run']=testcount
    out['uploaded_counts_and_seeded_floats_reproduced']=False
    target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
