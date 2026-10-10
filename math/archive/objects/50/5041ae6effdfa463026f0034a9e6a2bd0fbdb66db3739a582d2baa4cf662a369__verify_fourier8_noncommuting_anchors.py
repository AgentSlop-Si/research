#!/usr/bin/env python3
"""Bounded exact direction gates in Q[z]/(z^4+1); no parameter scan."""
import json
from pathlib import Path
from math import gcd
from functools import reduce

class K:
    def __init__(self,x=0): self.c=(x,0,0,0) if isinstance(x,int) else tuple(x)
    def __add__(self,o):
        o=cv(o);return K(tuple(a+b for a,b in zip(self.c,o.c)))
    __radd__=__add__
    def __neg__(self):return K(tuple(-a for a in self.c))
    def __sub__(self,o):return self+-cv(o)
    def __rsub__(self,o):return cv(o)+-self
    def __mul__(self,o):
        o=cv(o);r=[0]*4
        for i,a in enumerate(self.c):
            for j,b in enumerate(o.c):r[(i+j)%4]+=a*b*(-1 if i+j>=4 else 1)
        return K(r)
    __rmul__=__mul__
    def __bool__(self):return any(self.c)
    def __eq__(self,o):return self.c==cv(o).c
    def __pow__(self,n):
        assert n>=0;r=K(1);a=self
        while n:
            if n&1:r=r*a
            a=a*a;n//=2
        return r

def cv(x):return x if isinstance(x,K)else K(x)
def matmul(a,b):return [[sum((x*y for x,y in zip(row,col)),K())for col in zip(*b)]for row in a]
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def adj(a):return [[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]]
def sub(a,b):return [[x-y for x,y in zip(r,s)]for r,s in zip(a,b)]
def norm(a):
    g=reduce(gcd,(abs(c)for row in a for v in row for c in v.c),0)
    return [[K(tuple(c//g for c in v.c))for v in row]for row in a]if g else a

def dump(a):return [[list(v.c)for v in row]for row in a]
def perms(order):
    nxt={v:order[(i+1)%8]for i,v in enumerate(order)}
    prev={v:k for k,v in nxt.items()};return nxt,prev

def gate(B,pi,sigma):
    pn,pp=perms(pi);sn,sp=perms(sigma)
    edges=[];counts={0:0,1:0,2:0}
    for i in range(8):
      for k in range(i+1,8):
       avoid={i,pp[i],sp[i],k,pp[k],sp[k]}
       for j in range(8):
        if j in avoid:continue
        A,C=B[i][j],B[i][sn[j]];BB,D=B[pp[i]][j],B[pp[i]][sn[j]]
        E,G=B[k][j],B[k][sn[j]];F,H=B[pp[k]][j],B[pp[k]][sn[j]]
        h=norm([[A*H-C*F,BB*H-D*F],[-A*G+C*E,-BB*G+D*E]])
        rank=2 if det(h)else(1 if any(v for row in h for v in row)else 0)
        counts[rank]+=1;edges.append({'i':i,'k':k,'j':j,'h':h,'rank':rank})
    graph=[[]for _ in range(8)]
    for index,e in enumerate(edges):
        if e['rank']==2:
            graph[e['i']].append((e['k'],e['h'],index,False))
            graph[e['k']].append((e['i'],adj(e['h']),index,True))
    T=[None]*8;component=[None]*8;paths=[None]*8;roots=[]
    for root in range(8):
        if T[root] is not None:continue
        roots.append(root);T[root]=[[K(1),K()],[K(),K(1)]];component[root]=root;paths[root]=[]
        queue=[root]
        for i in queue:
            for k,h,idx,rev in graph[i]:
                if T[k]is not None:continue
                T[k]=norm(matmul(h,T[i]));component[k]=root;paths[k]=paths[i]+[(idx,rev)];queue.append(k)
    returns={root:[]for root in roots}
    for index,e in enumerate(edges):
        if e['rank']!=2:continue
        i,k=e['i'],e['k'];assert component[i]==component[k]
        r=norm(matmul(matmul(adj(T[k]),e['h']),T[i]));returns[component[i]].append((index,r))
    certificate=None
    for root,rs in returns.items():
        for u,(idx1,r1) in enumerate(rs):
            for idx2,r2 in rs[u+1:]:
                comm=sub(matmul(r1,r2),matmul(r2,r1));d=det(comm)
                if d:
                    used=set()
                    for idx in (idx1,idx2):
                        e=edges[idx];used.add(idx)
                        for vertex in (e['i'],e['k']):used.update(t[0]for t in paths[vertex])
                    certificate={'root':root,'return_edges':[idx1,idx2], 'return_matrices':[dump(r1),dump(r2)],'commutator_determinant':list(d.c),'tree_paths':{str(v):paths[v]for v in range(8)if component[v]==root},'source_edges':{str(idx):{'triple':[edges[idx][a]for a in ('i','k','j')],'transition':dump(edges[idx]['h'])}for idx in sorted(used)}}
                    break
            if certificate:break
        if certificate:break
    quads=[]
    for index,e in enumerate(edges):
        i,k=e['i'],e['k']
        if component[i]!=component[k]:continue
        h=e['h'];ell=[[-h[1][0],-h[1][1]],[h[0][0],h[0][1]]]
        tk=list(map(list,zip(*T[k])))
        m=matmul(matmul(tk,ell),T[i]);q=norm([[m[0][0],m[0][1]+m[1][0],m[1][1]]])[0]
        if any(q):quads.append({'edge':index,'root':component[i],'coefficients':[list(v.c)for v in q]})
    axis_checks=[]
    for root in roots:
        qs=[q for q in quads if q['root']==root]
        pivot=next((q for q in qs if sum(any(c)for c in q['coefficients'])==1),None)
        if pivot is None:continue
        cand=[]
        for axis in (0,1):
            bad=next((q['edge']for q in qs if any(q['coefficients'][0 if axis==0 else 2])),None)
            zeros=[v for v in range(8)if component[v]==root and not T[v][0][axis]]
            cand.append({'axis':axis,'violated_internal_edge':bad,'zero_base_rows':zeros})
        axis_checks.append({'root':root,'exhaustive_monomial_quadratic':pivot,'candidates':cand,'rejects_nonsingular_diagonal_endpoints':all(c['violated_internal_edge']is not None or c['zero_base_rows']for c in cand)})
    return {'equation_sources':[{'triple':[e[a]for a in ('i','k','j')],'rank':e['rank'],'transition':dump(e['h'])}for e in edges],'forest_paths':paths,'axis_guard_checks':axis_checks,'tree_transforms':[dump(t)for t in T],'nonzero_internal_quadratics':len(quads),'internal_quadratics':quads,'selected_row_equations':len(edges),'transition_ranks':counts,'rank_two_components':len(roots),'commutator_rejection':certificate is not None,'nonsingular_endpoint_chart_rejected':certificate is not None or any(t['rejects_nonsingular_diagonal_endpoints']for t in axis_checks),'certificate':certificate,'scope_if_not_rejected':'Only this shortcut was tested; no gate acceptance or synthesis is asserted.'}

z=K((0,1,0,0));F=[[z**(i*j%8)for j in range(8)]for i in range(8)]
orders={'natural':list(range(8)),'bit_reverse':[0,4,2,6,1,5,3,7],'evens_odds':[0,2,4,6,1,3,5,7],'gray':[0,1,3,2,6,7,5,4]}
pairs=[('natural','bit_reverse'),('natural','gray'),('evens_odds','gray'),('bit_reverse','gray')]
targets={}
for name,pairing in [('adjacent',[(i,i+1)for i in range(0,8,2)]),('halves',[(i,i+4)for i in range(4)])]:
    B=[[K()for _ in range(8)]for _ in range(8)]
    for a,b in pairing:
        for i in range(8):B[i][a]=F[i][a]+F[i][b];B[i][b]=F[i][a]-F[i][b]
    targets[name]=B # twice the specified target F8 K_pair/2; direction gate unchanged by scaling
results=[]
for anchor,B in targets.items():
    for p,s in pairs:
        pn,_=perms(orders[p]);sn,_=perms(orders[s])
        assert any(pn[sn[i]]!=sn[pn[i]]for i in range(8))
        ans=gate(B,orders[p],orders[s]);ans.update({'anchor':anchor,'orders':[p,s]});results.append(ans)
positive=[]
for p,s in pairs:
    pn,_=perms(orders[p]);sn,_=perms(orders[s]);B=[[K()for _ in range(8)]for _ in range(8)]
    for j in range(8):
        u=v=j
        for t in range(8):
            B[u][j]+=K((1-3**8)*2**t);B[v][j]+=K((1-2**8)*3**t);u=pn[u];v=sn[v]
    check=gate(B,orders[p],orders[s]);assert check['certificate'] is None
    for e in check['equation_sources']:
        h=[[K(v)for v in row]for row in e['transition']]
        ell=[[-h[1][0],-h[1][1]],[h[0][0],h[0][1]]]
        assert not (ell[0][0]-2*ell[0][1]-2*ell[1][0]+4*ell[1][1])
    assert not any(c['rejects_nonsingular_diagonal_endpoints']for c in check['axis_guard_checks'])
    positive.append({'orders':[p,s],'branch_weights':[2,3],'guards':[1-2**8,1-3**8],'genuine_two_green_sum_not_rejected':True})
assert all(c['certificate']is not None or any(t['rejects_nonsingular_diagonal_endpoints']for t in c['axis_guard_checks'])for c in results)
out={'positive_controls':positive,'field':'Q(zeta_8), zeta_8^4=-1; exact integer cyclotomic arithmetic','orders':orders,'cases':results,'search_budget':'Exactly two specified radix-2 anchor matrices and four specified noncommuting cycle pairs; no endpoint or edge parameter scan.','all_exact_checks_completed':True}
Path(__file__).with_name('FOURIER8_NONCOMMUTING_ANCHOR_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':[{k:v for k,v in r.items()if k not in ('certificate','internal_quadratics','tree_transforms','equation_sources','forest_paths','axis_guard_checks')}for r in results]},indent=2))
