"""Bounded label-compression experiment, independent exact binary-form checks.

Pinned input: Swapnil-jain/integer-mult-kappa, commit
f2176bc1124821bf17eb63725bd366d7bdc020a3, complex two-stage producer.
The candidate family is the exact support span and that span plus one
coordinate unit, strictly below the original coordinate-cover label.
Greedy topological replacements must preserve all adjacent residuals.
This is not a search of every possible binary subspace or global optimum.
"""
import sys, json, time, math
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'upstream'))
from producer import NStar3, compile_roles
from cert import cert

def basis(vs):
    piv = {}
    for x in vs:
        while x:
            p = x.bit_length() - 1
            if p in piv: x ^= piv[p]
            else:
                piv[p] = x
                break
    for p in sorted(piv):
        for q in piv:
            if q > p and ((piv[q] >> p) & 1): piv[q] ^= piv[p]
    return tuple(piv[p] for p in sorted(piv, reverse=True))

def contains(B, x):
    for y in B:
        if x & (1 << (y.bit_length()-1)): x ^= y
    return x == 0

def dot(x,y): return (x & y).bit_count() & 1

def nullspace(rows, n):
    rows = list(basis(rows)); piv = {r.bit_length()-1:r for r in rows}
    out = []
    for j in range(n):
        if j in piv: continue
        x = 1 << j
        for p,r in piv.items():
            if (r>>j)&1: x |= 1<<p
        out.append(x)
    return out

@lru_cache(None)
def form_ok(B):
    if not B: return True
    gram = [sum(dot(x,y)<<j for j,y in enumerate(B)) for x in B]
    return len(basis(gram)) == len(B) and any(x.bit_count()&1 for x in B)

@lru_cache(None)
def edge_ok(U,V):
    if not all(contains(V,x) for x in U): return False
    rows = [sum(dot(u,v)<<i for i,v in enumerate(V)) for u in U]
    R=[]
    for coeff in nullspace(rows,len(V)):
        x=0
        for i,v in enumerate(V):
            if (coeff>>i)&1: x ^= v
        R.append(x)
    return form_ok(basis(R))

def original_labels(c):
    out={}; true={}; cover={}; common={}; sizes={}
    for n in sorted(c.active):
        if c.args[n]:
            a,b=c.args[n]
            true[n]=basis(true[a]+true[b]); cover[n]=cover[a]|cover[b]
            common[n]=common[a]&common[b]; sizes[n]=sizes[a]+sizes[b]
        else:
            x=sum(1<<j for j in c.triples[n-1])
            true[n]=(x,); cover[n]=common[n]=x; sizes[n]=1
        out[n] = true[n] if sizes[n]==1 or common[n].bit_count()>=2 else basis(1<<j for j in range(c.h) if (cover[n]>>j)&1)
    return out,true,cover

def validate(c,labs,F):
    failures=Counter(); counts=Counter()
    for n in sorted(c.active):
        U=labs[n]
        counts['label']+=1; failures['label'] += not form_ok(U)
        counts['complement']+=1; failures['complement'] += not edge_ok(U,F)
        if c.args[n]:
            for a in c.args[n]:
                counts['producer_edge']+=1; failures['producer_edge']+=not edge_ok(labs[a],U)
    for S,n,_ in c.pieces:
        t=sum(1<<j for j in S)
        V=basis(nullspace([t],c.h))
        counts['piece_edge']+=1; failures['piece_edge']+=not edge_ok(labs[n],V)
    return dict(counts=counts,failures=failures)

def histogram(c,labs):
    """Independent event replay of the documented ten-operation frame schedule."""
    h=c.h; m=h*h; T=c.triples; v=len(T); N=v*v; cc=compile_roles(c)
    ops=[[] for _ in range(10)]
    for n,ins,outs in cc['gates']:
        roles=tuple(('s',q) for q in sorted(set(ins+outs)))
        ops[0].append((roles,0)); ops[3].append((roles,0))
        ops[5].append((roles,len(labs[n]))); ops[8].append((roles,h))
    ops[3].reverse(); ops[8].reverse()
    pieces=defaultdict(list)
    for i,slot in cc['pout'].items(): pieces[c.pieces[i][0]].append(slot)
    for t in T:
        names=[('*',)]+([('E',j) for j in t] if h-1 not in t else [('E',j) for j in range(h-1) if j not in t])
        ros=(('y',t),)+tuple(('s',cc['rout'][name]) for name in names)
        ops[1].append((ros,0)); ops[6].append((ros,0))
        if pieces[t]:
            ros=(('y',t),)+tuple(('s',q) for q in pieces[t])
            ops[2].append((ros,0)); ops[7].append((ros,h-1))
    for t,slot in cc['src'].items():
        ros=(('x',t),('s',slot)); ops[4].append((ros,1)); ops[9].append((ros,h))
    reverse=[[(ros,h-d) for ros,d in reversed(op)] for op in reversed(ops)]
    retained={('s',q) for q in cc['rout'].values()}
    H=Counter(); stage_data={}
    for stage,seq,designated in [(1,ops,6),(2,reverse,3)]:
        current={}; dpaths=defaultdict(list); copied=set(); pending={}
        lift=lambda d:d if stage==1 else m-h+d
        for k,op in enumerate(seq):
            for ros,d in op:
                target=lift(d)
                for ro in ros:
                    if ro[0]!='s': dpaths[ro].append(target); continue
                    if k==designated and ro in retained:
                        if ro not in copied:
                            copied.add(ro)
                            if stage==1:
                                r=abs(current.get(ro,0)-target)
                                if r: H[r]+=v
                            else: pending[ro]=target
                        continue
                    if ro in pending:
                        r=abs(target-pending.pop(ro))
                        if r:H[r]+=v
                    r=abs(target-current.get(ro,0))
                    if r:H[r]+=v
                    current[ro]=target
        assert len(current)==c.roles and not pending
        for d in current.values():
            if d!=m:H[m-d]+=v
        stage_data[stage]=dpaths
    p1=Counter((tuple(stage_data[1][('x',t)]),tuple(stage_data[1][('y',t)])) for t in T)
    p2=Counter((tuple(stage_data[2][('y',t)]),tuple(stage_data[2][('x',t)])) for t in T)
    for (x1,y1),n1 in p1.items():
        for (x2,y2),n2 in p2.items():
            for path in ([1,*x1,*x2,m],[0,*y1,*y2,m-1]):
                for x,y in zip(path,path[1:]):
                    if x!=y:H[abs(x-y)]+=n1*n2
    H[1]+=N
    W=2*N+2*v*c.roles
    return dict(hist=dict(sorted(H.items())),W=W,m=m,s=sum(r*n for r,n in H.items()))

def main(h):
    started=time.time(); c=NStar3(h); old,true,cover=original_labels(c); F=basis(1<<j for j in range(h))
    base_validation=validate(c,old,F); assert not any(base_validation['failures'].values())
    raw_validation=validate(c,true,F)
    print('Baseline validated',flush=True)
    children=defaultdict(list); outputs=defaultdict(list)
    for n in c.active:
        for a in c.args[n] or ():children[a].append(n)
    for S,n,_ in c.pieces:outputs[n].append(basis(nullspace([sum(1<<j for j in S)],h)))
    labels=dict(old); changed=[]; tested=0; locally_valid=0
    for n in sorted(c.active):
        if len(true[n])==len(old[n]):continue
        candidates={true[n]}
        for j in range(h):
            if (cover[n]>>j)&1:candidates.add(basis(true[n]+(1<<j,)))
        candidates=sorted((L for L in candidates if len(L)<len(old[n])),key=lambda L:(len(L),L))
        for L in candidates:
            tested+=1
            if not form_ok(L) or not edge_ok(L,F):continue
            if any(not edge_ok(labels[a],L) for a in (c.args[n] or ())):continue
            if any(not edge_ok(L,labels[b]) for b in children[n]):continue
            if any(not edge_ok(L,V) for V in outputs[n]):continue
            labels[n]=L;changed.append(dict(node=n,old=list(old[n]),new=list(L),support_dimension=len(true[n])))
            locally_valid+=1;break
    validation=validate(c,labels,F); assert not any(validation['failures'].values())
    retained_ids=[n for _,n in c.retained]
    assert all(labels[n]==old[n] for n in retained_ids), 'retained-centre budget changed'
    baseline=histogram(c,old); modified=histogram(c,labels)
    pinned=json.loads((HERE/'upstream'/'round6-histograms.json').read_text())['cx']
    assert baseline['hist']==dict(pinned['hist'])
    assert all(baseline[k]==pinned[k] for k in ('W','m','s'))
    assert baseline['s']==modified['s']==baseline['W']*h*h-len(c.triples)**2+2*len(c.triples)*((h-1)**2+h)
    for d in (baseline,modified):
        a,gap=cert(d['hist'],d['W'],d['m']);d['a']=str(a);d['a_float']=float(a);d['moment_gap']=str(gap)
    result=dict(source_commit='f2176bc1124821bf17eb63725bd366d7bdc020a3',h=h,active=len(c.active),roles=c.roles,
        candidate_family='exact support span, optionally plus one coordinate unit, strictly smaller than original label',
        candidates_tested=tested,changed_nodes=len(changed),dimension_reductions=dict(Counter(str((len(q['old']),len(q['new']))) for q in changed)),
        baseline_validation=base_validation,raw_support_validation=raw_validation,modified_validation=validation,
        retained_labels_unchanged=True,baseline_matches_pinned_histogram=True,
        baseline=baseline,modified=modified,changed_labels=changed,seconds=time.time()-started)
    (HERE/'reduction_results.json').write_text(json.dumps(result,indent=2)+'\n')
    summary={k:v for k,v in result.items() if k not in ('changed_labels','baseline','modified')}
    summary['baseline']={k:v for k,v in baseline.items() if k not in ('hist','moment_gap')}
    summary['modified']={k:v for k,v in modified.items() if k not in ('hist','moment_gap')}
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 24)
