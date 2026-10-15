"""Independent small controls. Does not import or run any inherited source code."""
import itertools, json, math, hashlib
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
def rank(a,p):
    a=[[int(x)%p for x in r] for r in a]; m=len(a);n=len(a[0]) if m else 0;r=0
    for j in range(n):
        z=next((i for i in range(r,m) if a[i][j]),None)
        if z is None:continue
        a[r],a[z]=a[z],a[r];iv=pow(a[r][j],-1,p);a[r]=[(x*iv)%p for x in a[r]]
        for i in range(m):
            if i!=r and a[i][j]:
                f=a[i][j];a[i]=[(x-f*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==m:break
    return r
def root(p,n):
    assert (p-1)%n==0
    div=[d for d in range(2,n+1) if n%d==0 and all(d%e for e in range(2,int(math.sqrt(d))+1))]
    for a in range(2,p):
        w=pow(a,(p-1)//n,p)
        if all(pow(w,n//d,p)!=1 for d in div):return w
    raise ValueError((p,n))
def F(n,p):
    w=root(p,n)
    return [[pow(w,j*k,p) for k in range(n)] for j in range(n)]
def defects(m,p,w):
    n=len(m)
    a=[[(m[j][(k+1)%n]-pow(w,j,p)*m[j][k])%p for k in range(n)] for j in range(n)]
    b=[[(m[j][k]*pow(w,k,p)-m[(j+1)%n][k])%p for k in range(n)] for j in range(n)]
    return a,b
def mv(a,x,p):return [sum(i*j for i,j in zip(r,x))%p for r in a]
out={'independently_authored':True,'inherited_programs_executed':False,'weyl':{},'parity':{},'tensor':{}}
sol=[]
for n in [2,3,4,6,8]:
    p=97;w=root(p,n); cols=[]
    for pos in range(n*n):
        m=[[int(i*n+j==pos) for j in range(n)] for i in range(n)]
        a,b=defects(m,p,w);cols.append(sum(a+b,[]))
    r=rank(list(zip(*cols)),p);assert r==n*n-1
    sol.append({'N':n,'p':p,'stacked_operator_rank':r})
out['weyl']['solution_space']=sol
probes=[]
for p,n in [(5,2),(7,3)]:
    w=root(p,n);f=F(n,p)
    for perturb in range(1,p):
        m=[r[:] for r in f];m[n-1][n-1]=(m[n-1][n-1]+perturb)%p
        a,b=defects(m,p,w);rho=rank(a+b,p)
        count=sum(all(v==0 for v in mv(a+b,x,p)) for x in itertools.product(range(p),repeat=n))
        assert count==p**(n-rho)
        calls=[0]
        def query(x):calls[0]+=1;return mv(m,x,p)
        assert query([1]+[0]*(n-1))==[1]*n
        for x in [list(range(n)),[1]*n]:
            query(x);query([x[(j-1)%n] for j in range(n)]);query([pow(w,j,p)*x[j]%p for j in range(n)])
        assert calls[0]==7
        probes.append({'p':p,'N':n,'perturbation':perturb,'defect_rank':rho,'accepted_vectors':count,'possible_vectors':p**n,'two_round_candidate_calls':calls[0]})
    m=[[2*x%p for x in r] for r in f];a,b=defects(m,p,w)
    assert rank(a+b,p)==0 and mv(m,[1]+[0]*(n-1),p)!=[1]*n
out['weyl']['exhaustive_calibrated_probes']=probes
rng=np.random.default_rng(202610152121);numeric=[]
for n in [2,3,4,5,6,8,9,12,16]:
    w=np.exp(-2j*np.pi/n);f=w**np.outer(np.arange(n),np.arange(n))/np.sqrt(n)
    z=np.roll(np.eye(n),1,axis=0);d=np.diag(w**np.arange(n));m=f@d
    residual=np.hypot(np.linalg.norm(m@z-d@m),np.linalg.norm(m@d-z.T@m))
    c=np.trace(f.conj().T@m)/n;dist=np.linalg.norm(m-c*f);ratio=residual/dist
    gap=2*np.sin(np.pi/n);assert abs(ratio-gap)<1e-12
    m=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));c=np.trace(f.conj().T@m)/n
    residual=np.hypot(np.linalg.norm(m@z-d@m),np.linalg.norm(m@d-z.T@m));dist=np.linalg.norm(m-c*f)
    assert residual+1e-10>=gap*dist
    numeric.append({'N':n,'equality_ratio':float(ratio),'sharp_gap':float(gap),'random_ratio':float(residual/dist)})
out['weyl']['complex_numerical_controls']=numeric
cases=0
for p in [97,193]:
 for n in [4,8,16]:
    f=F(n,p);k=n.bit_length()-1
    for a in range(1,n):
     for b in range(1,n):
      expected=n//4 if a.bit_length()+b.bit_length()-2<=k-2 else n//2
      for s,t in itertools.product(range(2),repeat=2):
       rr=[i for i in range(n) if (i&b).bit_count()%2==t]
       cc=[i for i in range(n) if (i&a).bit_count()%2==s]
       actual=rank([[f[i][j] for j in cc] for i in rr],p);assert actual==expected
       cases+=1
out['parity']['modular_parity_blocks']={'count':cases,'primes':[97,193],'lengths':[4,8,16],'all_nonzero_masks':True,'all_four_signs':True,'purpose':'corroboration, not characteristic-zero proof'}
universal=[]
for p in [12289,65537]:
 f=F(16,p);rr=[0,1,2,3,4,6,7,12];cc=[0,1,2,3,4,13,6,7]
 actual=rank([[f[i][j] for j in cc] for i in rr],p);assert actual==({12289:7,65537:8}[p]);universal.append({'p':p,'rank':actual})
out['parity']['universal_set_specialization_warning']=universal
boundary=sum(((i&16).bit_count()^( (i+1)&16).bit_count())&1 for i in range(511))
assert boundary==31
out['parity']['weighted_capacity_regression']={'k':9,'t':2,'r':2,'mask':16,'boundaries':[boundary,boundary],'wrong_unweighted':62,'correct_weighted':124,'required_rank_lower_bound':128}
def tensor(q,m,p):
 n=q*m;w=root(p,n)
 return {(s,h,t,u):pow(w,(-h*t-m*s*t-q*h*u)%n,p) for s,h,t,u in itertools.product(range(q),range(m),range(q),range(m))}
tc=[]
for q,m in [(1,1),(1,7),(7,1),(2,2),(2,3),(3,2),(3,3),(2,4),(4,2),(4,4),(3,4),(4,3),(5,6),(6,5)]:
 p=20161;n=q*m
 if n==1:w=1;tens={(0,0,0,0):1}
 else:w=root(p,n);tens=tensor(q,m,p)
 for (s,h,t,u),v in tens.items():assert v==pow(w,(-(h+m*s)*(t+q*u))%n,p)
 cuts=[]
 for left,right,expected in [((0,1),(2,3),n),((0,2),(1,3),min(q,m)),((0,3),(1,2),n)]:
  dims=[q,m,q,m];rs=list(itertools.product(*[range(dims[i]) for i in left]));cs=list(itertools.product(*[range(dims[i]) for i in right]));mat=[]
  for rr in rs:
   row=[]
   for cc in cs:
    v=[0]*4
    for a,i in enumerate(left):v[i]=rr[a]
    for a,i in enumerate(right):v[i]=cc[a]
    row.append(tens[tuple(v)])
   mat.append(row)
  actual=rank(mat,p);assert actual==expected;cuts.append(actual)
 tc.append({'Q':q,'M':m,'p':p,'cut_ranks_sh_tu__st_hu__su_ht':cuts})
out['tensor']['exact_digit_and_cut_controls']=tc
# The equality characterization reduces bijectively to all pairs of invertible 2x2 matrices.
gl=[]
for e in itertools.product(range(5),repeat=4):
 if (e[0]*e[3]-e[1]*e[2])%5:
  nnz=sum(x!=0 for x in e);mono=all(sum(e[2*i+j]!=0 for j in range(2))==1 for i in range(2)) and all(sum(e[2*i+j]!=0 for i in range(2))==1 for j in range(2));gl.append((nnz,mono))
hits=0
for (na,ma),(nb,mb) in itertools.product(gl,repeat=2):
 assert na*nb>=4 and ((na*nb==4)==(ma and mb));hits+=na*nb==4
out['tensor']['support_equality_exhaustion']={'field':5,'invertible_2x2_count':len(gl),'endpoint_pairs':len(gl)**2,'N_entry_minimizers':hits}
out['limitations']=['Fresh exact finite and numerical controls corroborate proofs and do not replace them.','No historical large run, original implementation, timing claim, worldwide novelty claim or unrestricted Fourier complexity theorem is verified.','No external service writes.']
(HERE/'FRESH_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','parity_cases':cases,'tensor_pairs':len(gl)**2,'tensor_sizes':len(tc),'weyl_probe_cases':len(probes)},indent=2))
