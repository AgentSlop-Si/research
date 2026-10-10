#!/usr/bin/env python3
"""Independent exact audit. Reads data only; never imports/executes supplied code.

Arithmetic: sum all length-three paths in the group ring Z[C_p x C_d].
Reduce the C_d coordinate by a freshly constructed cyclotomic polynomial.
Since gcd(p,d)=1, the remaining polynomial vanishes at (zeta_p,zeta_d)
iff all its p coefficients in Q(zeta_d) are equal (a multiple of Phi_p).
"""
from pathlib import Path
from collections import defaultdict
from functools import lru_cache
from copy import deepcopy
from fractions import Fraction
import hashlib, json, math, time, zipfile

HERE=Path(__file__).resolve().parent
INPUT=HERE/'input_snapshot'
ORIGINAL=HERE.parent/'research_cycle_1535/subgroup_fourier_weights'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok, msg):
    if not ok: raise ValueError(msg)
def prime(n): return n>=2 and all(n%i for i in range(2,math.isqrt(n)+1))
def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def trim(a):
    while len(a)>1 and not a[-1]: a.pop()
    return a

def monic_divide(a,b):
    a=a[:]; q=[0]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        t=len(a)-len(b); c=a[-1]; q[t]=c
        for j,v in enumerate(b): a[t+j]-=c*v
        trim(a)
    require(not any(a), 'inexact polynomial division')
    return trim(q)

@lru_cache(None)
def cyclotomic(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in divisors(n)[:-1]: a=monic_divide(a,list(cyclotomic(d)))
    return tuple(a)

@lru_cache(None)
def w_basis(d):
    f=cyclotomic(d); degree=len(f)-1; basis=[]
    for exponent in range(d):
        a=[0]*(max(degree,exponent+1)); a[exponent]=1
        for i in range(len(a)-1,degree-1,-1):
            c=a[i]
            if c:
                for j,v in enumerate(f): a[i-degree+j]-=c*v
        basis.append(tuple(a[:degree]))
    return tuple(basis)

def normal_form(poly,p,d):
    """Canonical sparse Q-basis coefficients for a group-ring polynomial."""
    wb=w_basis(d); degree=len(wb[0]); zrows={}
    for (a,b),value in poly.items():
        if value:
            row=zrows.setdefault(a%p,[0]*degree)
            for q,c in enumerate(wb[b%d]): row[q]+=value*c
    last=zrows.get(p-1,[0]*degree)
    out={}
    for a in range(p-1):
        row=zrows.get(a,[0]*degree)
        for q in range(degree):
            c=row[q]-last[q]
            if c: out[a,q]=c
    return out

def raw_poly(terms,p,d):
    result=defaultdict(int)
    for a,b,c in terms: result[a%p,b%d]+=c
    return {key:value for key,value in result.items() if value}

def parse(graph, strict=True):
    p,d=graph['p'],graph['d']; denominators=graph['denominators']
    require(prime(p) and p%2 and d in divisors(p-1), 'invalid prime/divisor')
    require(graph['m']==(p-1)//d,'bad m')
    g=graph['primitive_root']; h=graph['subgroup_generator']; m=graph['m']
    require(len({pow(g,i,p) for i in range(p-1)})==p-1, 'not primitive')
    require(h==pow(g,m,p),'wrong h')
    reps=graph['coset_representatives']
    require(reps==[pow(g,i,p) for i in range(m)],'wrong cosets')
    require(sorted(a*pow(h,t,p)%p for a in reps for t in range(d))==list(range(1,p)), 'not a partition')
    rows={}; maximum_bounds={}; edgecounts={}; nonzero=0
    for name in 'ABC':
        den=denominators[name]; require(type(den)==int and den>0,'bad denominator')
        if strict: require(den==({'A':1,'B':d,'C':1}[name]),'unexpected denominator')
        layers=[[] for _ in range(p)]; seen=set(); bound=Fraction(0)
        for row,col,terms in graph[name]:
            require(type(row)==int and type(col)==int and 0<=row<p and 0<=col<p,'bad vertex')
            require((row,col) not in seen,'duplicate edge')
            seen.add((row,col))
            require(terms and all(len(t)==3 and all(type(v)==int for v in t) for t in terms),'invalid terms')
            pol=raw_poly(terms,p,d)
            require(normal_form(pol,p,d),'zero listed edge')
            nonzero+=1
            b=Fraction(sum(abs(c) for _,_,c in terms),den); bound=max(bound,b)
            if strict: require(b<=1,'triangle bound exceeds one')
            layers[row].append((col,pol))
        rows[name]=layers; maximum_bounds[name]=str(bound); edgecounts[name]=len(seen)
    if strict:
        require(edgecounts=={'A':1+d*(p-1),'B':1+2*m+d*m*m,'C':1+d*(p-1)},'wrong edge counts')
    return rows,edgecounts,maximum_bounds,nonzero

def check_identity(graph,sign=1,strict=True,all_entries=True):
    p,d=graph['p'],graph['d']; rows,counts,bounds,nz=parse(graph,strict)
    den=math.prod(graph['denominators'].values()); checked=0; mismatch=[]
    for k in range(p):
        sums=[defaultdict(int) for _ in range(p)]
        for ccol,cpoly in rows['C'][k]:
            for bcol,bpoly in rows['B'][ccol]:
                for j,apoly in rows['A'][bcol]:
                    dest=sums[j]
                    for (ca,cb),cv in cpoly.items():
                        for (ba,bb),bv in bpoly.items():
                            for (aa,ab),av in apoly.items():
                                dest[(ca+ba+aa)%p,(cb+bb+ab)%d]+=cv*bv*av
        for j,poly in enumerate(sums):
            poly[(sign*k*j)%p,0]-=den
            nf=normal_form(poly,p,d); checked+=1
            if nf:
                mismatch.append([k,j])
                if not all_entries: return {'pass':False,'first_mismatch':[k,j]}
    return {'pass':not mismatch,'entries_checked':checked,'mismatch_count':len(mismatch),
            'first_mismatch':mismatch[0] if mismatch else None,'edges':counts,
            'total_edges':sum(counts.values()),'weights_exact_nonzero':nz,
            'maximum_triangle_bounds':bounds}

def expected_formula_matches(graph):
    p,d,m=graph['p'],graph['d'],graph['m']; h=graph['subgroup_generator']; reps=graph['coset_representatives']
    expected={name:{} for name in 'ABC'}
    expected['A'][0,0]=[[0,0,1]]; expected['C'][0,0]=[[0,0,1]]
    expected['B'][0,0]=[[0,0,d]]
    for i,a in enumerate(reps):
        expected['B'][0,1+i*d]=[[0,0,d]]
        expected['B'][1+i*d,0]=[[0,0,d]]
        for l in range(d):
            slot=1+i*d+l
            for t in range(d):
                ext=a*pow(h,t,p)%p
                expected['A'][slot,ext]=[[0,(-l*t)%d,1]]
                expected['C'][ext,slot]=[[0,(-l*t)%d,1]]
            for r,b in enumerate(reps):
                expected['B'][1+r*d+l,slot]=[[a*b*pow(h,t,p)%p,(l*t)%d,1] for t in range(d)]
    for name in 'ABC':
        actual={(r,c):raw_poly(t,p,d) for r,c,t in graph[name]}
        require(set(actual)==set(expected[name]),'formula support mismatch')
        for key,terms in expected[name].items():
            diff=defaultdict(int,actual[key])
            for mon,coef in raw_poly(terms,p,d).items(): diff[mon]-=coef
            require(not normal_form(diff,p,d),'formula weight mismatch')
    return True

def negative_control(name,graph,mutator,sign=1):
    g=deepcopy(graph); mutator(g)
    try:
        result=check_identity(g,sign=sign,strict=False,all_entries=False)
        rejected=not result['pass']; reason=result.get('first_mismatch')
    except ValueError as e: rejected=True; reason=str(e)
    require(rejected,'negative control unexpectedly passed: '+name)
    return {'name':name,'rejected':rejected,'reason':reason}

def main():
    start=time.perf_counter()
    original_hashes={p.name:sha(p) for p in ORIGINAL.iterdir() if p.is_file()} if ORIGINAL.is_dir() else None
    snapshot_hashes={p.name:sha(p) for p in INPUT.iterdir() if p.is_file()}
    require(original_hashes is None or original_hashes==snapshot_hashes,'snapshot differs from source')
    (HERE/'INPUT_SHA256.json').write_text(json.dumps(snapshot_hashes,indent=2)+'\n')
    supplied=json.loads((INPUT/'EXACT_SUBGROUP_RESULTS.json').read_text())
    supplied_by_file={r['graph_file']:r for r in supplied['results']}
    manifest=json.loads((INPUT/'MANIFEST.json').read_text())
    require(all(snapshot_hashes[name]==h for name,h in manifest.items()),'author manifest mismatch')
    z=zipfile.ZipFile(INPUT/'exact_subgroup_fourier_certificate.zip')
    require(all(hashlib.sha256(z.read(name)).hexdigest()==snapshot_hashes[name] for name in z.namelist()),'archive mismatch')
    # Cyclotomic/reducer controls, including algebraic cancellation and nonzero.
    require(cyclotomic(1)==(-1,1),'Phi1')
    require(cyclotomic(6)==(1,-1,1),'Phi6')
    require(cyclotomic(10)==(1,-1,1,-1,1),'Phi10')
    for d in {1,2,3,4,5,6,7,8,10}:
        require(not normal_form({(0,i):v for i,v in enumerate(cyclotomic(d))},11 if d!=7 else 29,d),'Phi_d does not vanish')
        require(not normal_form({(i,0):1 for i in range(11)},11,d),'Phi_p does not vanish')
        require(normal_form({(0,0):1},11,d)=={(0,0):1},'one vanished')
    rows=[]; controls=[]; graphs=[]
    for path in sorted(INPUT.glob('graph_p*_d*.json'),key=lambda x: (json.loads(x.read_text())['p'],json.loads(x.read_text())['d'])):
        graph=json.loads(path.read_text()); graphs.append(graph)
        r=check_identity(graph); require(r['pass'],'identity failed '+path.name)
        r.update({'file':path.name,'p':graph['p'],'d':graph['d'],'sha256':sha(path),'formula_matches':expected_formula_matches(graph)})
        author=supplied_by_file[path.name]
        require(author['sha256']==r['sha256'] and author['edges']==r['edges'] and author['exact_entries_checked']==r['entries_checked'] and author['total_edges']==r['total_edges'],'supplied result mismatch')
        require(r['total_edges']==3+2*graph['d']*(graph['p']-1)+(graph['p']**2-1)//graph['d'],'formula mismatch')
        rows.append(r); print(path.name, 'PASS',r['entries_checked'],'entries',r['total_edges'],'edges',flush=True)
        for layer in 'ABC':
            controls.append(negative_control(path.name+': missing '+layer+' DC edge',graph,lambda x,L=layer: x[L].pop(next(i for i,e in enumerate(x[L]) if e[:2]==[0,0]))))
        if graph['d']>1:
            controls.append(negative_control(path.name+': omitted B normalization',graph,lambda x:x['denominators'].__setitem__('B',1)))
        controls.append(negative_control(path.name+': wrong Fourier sign',graph,lambda x:None,sign=-1))
    control_graph=next(g for g in graphs if g['p']==11 and g['d']==5)
    controls.append(negative_control('duplicate edge',control_graph,lambda g:g['A'].append(deepcopy(g['A'][0]))))
    controls.append(negative_control('zero edge',control_graph,lambda g:g['A'][0][2].__setitem__(0,[0,0,0])))
    def bad_phase(g):
        edge=next(e for e in g['A'] if e[2][0][1]!=0)
        edge[2][0][1]+=1
    controls.append(negative_control('single root phase corrupted',control_graph,bad_phase))
    optimization=[]
    for p in range(3,102,2):
        if not prime(p): continue
        choices=[(3+2*d*(p-1)+(p*p-1)//d,d) for d in divisors(p-1)]
        edges,d=min(choices)
        optimization.append({'p':p,'d':d,'edges':edges,'paired_baseline_edges':(p*p+8*p-3)//2})
    require(optimization==supplied['exact_divisor_optimization_through_101'],'divisor enumeration mismatch')
    require(len(rows)==17 and sum(r['entries_checked'] for r in rows)==28209,'coverage mismatch')
    require(original_hashes is None or original_hashes=={p.name:sha(p) for p in ORIGINAL.iterdir() if p.is_file()},'source changed')
    result={'verdict':'PASS_CLASSICAL_BASELINE','author_code_executed_or_imported':False,
            'method':'Fresh Python integer group-ring path expansion; exact cyclotomic normal form; no numerical tolerance.',
            'graph_count':len(rows),'exact_target_entries':sum(r['entries_checked'] for r in rows),
            'exact_nonzero_edge_checks':sum(r['weights_exact_nonzero'] for r in rows),'rows':rows,
            'negative_controls':controls,'negative_control_count':len(controls),
            'source_manifest_entries_verified':len(manifest),'source_archive_byte_matches':len(z.namelist()),
            'source_originals_unchanged':True if original_hashes is not None else None,'source_originals_available':original_hashes is not None,'divisor_optimization':optimization,
            'f11_divisor_choices':{str(d):3+20*d+120//d for d in divisors(10)},
            'limitations':['Classical baseline only; no novelty certificate.','103 is the F11 optimum only among divisor-subgroup choices.','Does not rule out other three-layer Fourier graphs below 103.','Bounded rational search is separately scoped and is not a global proof.'],
            'runtime_seconds':round(time.perf_counter()-start,3),'reviewer_source_sha256':sha(Path(__file__))}
    (HERE/'INDEPENDENT_GRAPH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS:',len(rows),'graphs,',result['exact_target_entries'],'identities,',result['exact_nonzero_edge_checks'],'edge weights,',len(controls),'negative controls; seconds',result['runtime_seconds'],flush=True)

if __name__=='__main__': main()
