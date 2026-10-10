#!/usr/bin/env python3
"""Fresh exact three-layer Fourier certificates. Does not import research source.
All ring arithmetic uses integer coefficients, with a global 1/d on middle B.
Graph verification multiplies the exported edge lists, not the derivation.
"""
from collections import defaultdict
from pathlib import Path
from time import perf_counter
import hashlib, json
import sympy as sp

OUT = Path(__file__).resolve().parent

def divisors(n):
    return [d for d in range(1,n+1) if n%d == 0]

def primitive_root(p):
    for g in range(2,p):
        if len({pow(g,k,p) for k in range(p-1)}) == p-1:
            return g
    raise ValueError(p)

def construct(p,d):
    assert sp.isprime(p) and (p-1)%d == 0
    m=(p-1)//d; g=primitive_root(p); h=pow(g,m,p)
    reps=[pow(g,i,p) for i in range(m)]
    slot=lambda i,l: 1+i*d+l
    # An edge is [output row,input column, [[z exponent,w exponent,numerator], ...]].
    # The A,C denominators are 1. All B denominators are d.
    A=[[0,0,[[0,0,1]]]]
    B=[[0,0,[[0,0,d]]]]
    C=[[0,0,[[0,0,1]]]]
    for i,a in enumerate(reps):
        for l in range(d):
            for t in range(d):
                j=a*pow(h,t,p)%p
                A.append([slot(i,l),j,[[0,(-l*t)%d,1]]])
                C.append([j,slot(i,l),[[0,(-l*t)%d,1]]])
        B.append([0,slot(i,0),[[0,0,d]]])
        B.append([slot(i,0),0,[[0,0,d]]])
    for r,b in enumerate(reps):
        for i,a in enumerate(reps):
            for l in range(d):
                terms=[[a*b*pow(h,t,p)%p,(l*t)%d,1] for t in range(d)]
                B.append([slot(r,l),slot(i,l),terms])
    return dict(p=p,d=d,m=m,primitive_root=g,subgroup_generator=h,
                coset_representatives=reps,root_convention='z=exp(2*pi*i/p), w=exp(2*pi*i/d)',
                matrix_identity='C B A = F_p, (F_p)[k,j]=z^(k*j)',
                internal_slot='1+i*d+l for coset i and character l',
                denominators=dict(A=1,B=d,C=1),A=A,B=B,C=C)

class ExactRing:
    def __init__(self,p,d):
        self.p=p;self.d=d
        x=sp.Symbol('x'); phi=sp.Poly(sp.cyclotomic_poly(d,x),x)
        self.wred=[]
        for k in range(d):
            rem=sp.rem(sp.Poly(x**k,x),phi)
            self.wred.append({int(e[0]):int(c) for e,c in rem.terms() if c})
    def poly(self,terms):
        x=defaultdict(int)
        for a,b,c in terms:x[a%self.p,b%self.d]+=c
        return {k:v for k,v in x.items() if v}
    def mul(self,a,b):
        c=defaultdict(int)
        for (i,j),u in a.items():
            for (k,l),v in b.items():c[(i+k)%self.p,(j+l)%self.d]+=u*v
        return {k:v for k,v in c.items() if v}
    def canon(self,a):
        out=defaultdict(int)
        for (i,j),v in a.items():
            zr={i:1} if i<self.p-1 else {k:-1 for k in range(self.p-1)}
            for k,u in zr.items():
                for l,w in self.wred[j].items():out[k,l]+=v*u*w
        return {k:v for k,v in out.items() if v}
    def matrix(self,edges):
        M={}
        for r,c,terms in edges:
            assert (r,c) not in M, 'parallel edge not merged'
            M[r,c]=self.poly(terms)
        return M
    def mm(self,L,R):
        rows=defaultdict(list)
        for (j,k),v in R.items():rows[j].append((k,v))
        out=defaultdict(lambda:defaultdict(int))
        for (i,j),u in L.items():
            for k,v in rows[j]:
                for mon,c in self.mul(u,v).items():out[i,k][mon]+=c
        return {k:{a:b for a,b in v.items() if b} for k,v in out.items()}

def verify(graph):
    start=perf_counter();p=graph['p'];d=graph['d'];m=graph['m']
    R=ExactRing(p,d)
    mats={name:R.matrix(graph[name]) for name in ('A','B','C')}
    nnz={name:sum(bool(R.canon(poly)) for poly in M.values()) for name,M in mats.items()}
    assert all(nnz[name]==len(graph[name]) for name in nnz), 'listed zero edge'
    P=R.mm(mats['C'],R.mm(mats['B'],mats['A']))
    for i in range(p):
        for j in range(p):
            expected=R.canon({(i*j%p,0):d})
            assert R.canon(P.get((i,j),{}))==expected, (p,d,i,j)
    predicted=3+2*d*(p-1)+(p*p-1)//d
    assert sum(nnz.values())==predicted
    assert nnz['A']==nnz['C']==1+d*(p-1)
    assert nnz['B']==1+2*m+d*m*m
    return dict(p=p,d=d,edges=nnz,total_edges=sum(nnz.values()),
                paired_baseline_edges=(p*p+8*p-3)//2,
                exact_entries_checked=p*p,all_listed_weights_nonzero=True,
                field='Q[z,w]/(Phi_p(z),Phi_d(w))',seconds=round(perf_counter()-start,4))

def main():
    cases=[(3,1),(3,2),(5,2),(7,2),(11,1),(11,2),(11,5),(11,10),
           (13,3),(17,4),(19,3),(29,4),(31,5),(43,6),(71,7),(89,8),(101,10)]
    results=[]
    for p,d in cases:
        graph=construct(p,d)
        path=OUT/f'graph_p{p}_d{d}.json'
        path.write_text(json.dumps(graph,indent=2)+'\n')
        # Cold reload ensures the checker reads the deliverable edge data.
        result=verify(json.loads(path.read_text()))
        result['graph_file']=path.name
        result['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        results.append(result); print(json.dumps(result),flush=True)
    best=[dict(p=p,d=min(divisors(p-1),key=lambda d:3+2*d*(p-1)+(p*p-1)//d),
               edges=min(3+2*d*(p-1)+(p*p-1)//d for d in divisors(p-1)),
               paired_baseline_edges=(p*p+8*p-3)//2)
          for p in list(sp.primerange(3,102))]
    report=dict(status='PASS',review_status='Self-checked classical baseline; awaiting independent review; not a novel accepted result.',fresh_independent_code=True,inherited_source_executed_or_imported=False,
                complex_exact_identity=True,three_layers_all_edges_counted=True,
                formula='3 + 2*d*(p-1) + (p*p-1)/d, d | p-1',results=results,
                exact_divisor_optimization_through_101=best,
                limitation='No F11 factorization below 103 edges established. Divisor subgroup family optimum at F11 is 103.',
                novelty='Classical character decomposition/Rader-convolution specialization; no novelty or general FFT breakthrough claim.')
    (OUT/'EXACT_SUBGROUP_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(results),'cases,',sum(r['exact_entries_checked'] for r in results),'entries',flush=True)

if __name__=='__main__':main()
