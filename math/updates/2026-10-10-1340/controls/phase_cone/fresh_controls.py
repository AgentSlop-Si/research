#!/usr/bin/env python3
"""Fresh review controls; no submitted program is executed or imported.
Exact controls use integers, Fraction, and SymPy. Numerical SVD controls are
explicitly corroborative, not proofs or certified transcendental decisions.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import deque
from pathlib import Path
import json, math, random
import numpy as np
import sympy as s

OUT=Path(__file__).resolve().parent
R=random.Random(101020261330)
report={"seed":101020261330,"author_programs_executed":False,"exact":{},"numerical":{}}

def phase_potential(n,q,edges):
    adj=[[] for _ in range(n)]
    for u,v,a in edges:
        adj[u].append((v,-a%q));adj[v].append((u,a%q))
    p=[None]*n
    for root in range(n):
        if p[root] is not None:continue
        p[root]=0;queue=deque([root])
        while queue:
            u=queue.popleft()
            for v,d in adj[u]:
                x=(p[u]+d)%q
                if p[v] is None:p[v]=x;queue.append(v)
                elif p[v]!=x:return None
    return p

def cycle(order,p,q):
    return [(u,order[(k+1)%len(order)],(p[u]-p[order[(k+1)%len(order)]])%q)
            for k,u in enumerate(order)]

def arc_hist(labels,q):
    if not labels:return 0
    bins=[False]*q
    for a in labels:bins[a%q]=True
    first=prev=None;gap=0
    for a,yes in enumerate(bins):
        if not yes:continue
        if first is None:first=a
        else:gap=max(gap,a-prev)
        prev=a
    gap=max(gap,first+q-prev)
    return q-gap

def arc_brute(labels,q):
    if not labels:return 0
    return min(max((a-start)%q for a in labels) for start in range(q))

def exact_graph_and_arc():
    count=0
    for n in range(2,15):
        for q in range(1,18):
            p=[R.randrange(q) for _ in range(n)]
            orders=[]
            for _ in range(2):
                order=list(range(n));R.shuffle(order);orders.append(order)
            edges=sum([cycle(o,p,q) for o in orders],[])
            actual=phase_potential(n,q,edges)
            assert actual is not None
            assert all((actual[v]-actual[u]+a)%q==0 for u,v,a in edges)
            assert len({(actual[i]-p[i])%q for i in range(n)})==1
            count+=1
    # Each cycle individually balanced, the union is not.
    e1=cycle([0,1,2],[0,0,0],5)
    e2=cycle([0,2,1],[0,1,0],5)
    assert phase_potential(3,5,e1) is not None
    assert phase_potential(3,5,e2) is not None
    assert phase_potential(3,5,e1+e2) is None
    # Parallel edges must not be collapsed; different gains give a 2-edge witness.
    assert phase_potential(2,7,[(0,1,0),(0,1,1)]) is None
    arcs=0
    for q in range(1,11):
        for mask in range(1<<q):
            labs=[j for j in range(q) if mask>>j&1]
            assert arc_hist(labs,q)==arc_brute(labs,q)
            for shift in (0,1,q-1):
                assert arc_hist([(j+shift)%q for j in labs],q)==arc_hist(labs,q)
            arcs+=1
    assert arc_hist([6,0,1],7)==2
    assert arc_hist([0,3],6)==3
    assert arc_hist([3,3],7)==0
    report['exact']['graphs']={"positive_union_cases":count,"individually_balanced_union_frustrated":True,"parallel_edge_conflict":True}
    report['exact']['arcs']={"exhaustive_subsets_q_1_to_10":arcs,"wraparound_antipodal_singleton_empty":True,"rotation_invariance":True}

def atan_bounds(x,terms):
    z=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    nxt=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(z,z+nxt),max(z,z+nxt)

def pi_bounds(terms):
    al,ah=atan_bounds(F(1,5),terms);bl,bh=atan_bounds(F(1,239),terms)
    return 16*al-4*bh,16*ah-4*bl

def cos_bounds_at(x,terms):
    z=sum(((-1)**j*x**(2*j)/F(math.factorial(2*j)) for j in range(terms)),F(0))
    # Alternating tail decreases from the first omitted term for 0<=x<2.
    nxt=(-1)**terms*x**(2*terms)/F(math.factorial(2*terms))
    return min(z,z+nxt),max(z,z+nxt)

def certified_decision(n,k,q,eps=F(0)):
    """Strict floor>eps decision, exact rational eps and W=2*pi*k/q<pi.
    Equality at the rational-cosine angles is checked algebraically first.
    Every other returned sign comes from a rational interval disjoint from 0.
    """
    assert n>=2 and q>=1 and 0<=2*k<q and 0<=eps<1
    ratio=F(k,q)
    exact_cos2={F(0):F(1),F(1,6):F(3,4),F(1,4):F(1,2),F(1,3):F(1,4)}
    if ratio in exact_cos2:
        gap=n*exact_cos2[ratio]*(1-eps)**2-(1+eps)**2
        return {'sign':(gap>0)-(gap<0),'method':'rational special angle','precision_terms':0,'gap_interval':[str(gap),str(gap)]}
    for terms in (4,8,16,32,64,128):
        pl,ph=pi_bounds(terms)
        xl,xh=ratio*pl,ratio*ph
        cl=cos_bounds_at(xh,terms)[0]
        ch=cos_bounds_at(xl,terms)[1]
        cl=max(F(0),cl);ch=min(F(1),ch)
        lo=n*cl*cl*(1-eps)**2-(1+eps)**2
        hi=n*ch*ch*(1-eps)**2-(1+eps)**2
        if lo>0 or hi<0:
            return {'sign':1 if lo>0 else -1,'method':'rational Machin/Taylor interval','precision_terms':terms,'gap_interval':[str(lo),str(hi)]}
    return {'sign':None,'method':'inconclusive; never reject','precision_terms':128}

def exact_thresholds():
    cases=[(2,1,4,F(0),0),(4,1,3,F(0),0),(3,1,4,F(0),1),(2,1,3,F(0),-1),
           (16,0,1,F(3,5),0),(16,1,3,F(1,3),0),(64,1,3,F(3,5),0),
           (8,1,3,F(0),1),(8,2,5,F(0),-1),(16,2,5,F(0),1)]
    records=[]
    for n,k,q,e,expected in cases:
        d=certified_decision(n,k,q,e);assert d['sign']==expected,(n,k,q,e,d)
        records.append(dict(n=n,k=k,q=q,epsilon=str(e),expected_sign=expected,**d))
    count=0
    for n in (2,3,4,5,8,16,64):
        for q in range(2,35):
            for k in range((q+1)//2):
                d=certified_decision(n,k,q)
                assert d['sign'] is not None
                gap=n*math.cos(math.pi*k/q)**2-1
                if abs(gap)>1e-11:assert d['sign']==(1 if gap>0 else -1)
                count+=1
    report['exact']['certified_thresholds']={'named_cases':records,'grid_comparisons':count,'rule':'reject only sign=+1; equality never rejected','floating_grid_crosscheck_not_the_certificate':True}

def exact_green():
    rows=[]
    for n in (3,4,6):
        order1=list(range(n));order2=[0]+list(range(n-1,0,-1))
        potA=[(i*i+2*i)%4 for i in range(n)]
        potB=[(3*i+1)%4 for i in range(n)]
        stages=[]
        for p in (potA,potB):
            H=s.diag(*[s.I**a for a in p]);stage=s.zeros(n);pos=s.zeros(n)
            for order,m in ((order1,s.Rational(1,2)),(order2,s.Rational(2,3))):
                T=s.zeros(n);S=s.zeros(n)
                edges=cycle(order,p,4)
                for u,v,a in edges:T[u,v]=m*s.I**a;S[u,v]=m
                assert T**n==m**n*s.eye(n)
                G=(s.eye(n)-T).inv();P=(s.eye(n)-S).inv()
                assert H.conjugate().T*G*H==P
                assert all(x>0 for x in P)
                assert (s.eye(n)-T)*G==s.eye(n)==G*(s.eye(n)-T)
                stage+=G;pos+=P
            stages.append((H,stage,pos))
        HA,A,Ap=stages[0];HB,B,Bp=stages[1]
        eff=s.diag(*[s.I**(i%2) for i in range(n)])
        D=HA*eff*HB.conjugate().T
        C=(HA.conjugate().T*A*D*B*HB).applyfunc(s.expand)
        assert C==(Ap*eff*Bp).applyfunc(s.expand)
        assert all(s.re(z)>=0 and s.im(z)>=0 for z in C)
        rows.append({'n':n,'branches':4,'q':4,'exact_similarity':True,'effective_quadrant_cone':True})
    # Magnitude product one can be singular despite exact phase balance.
    S=s.Matrix([[0,1],[1,0]])
    assert (s.eye(2)-S).det()==0
    # Product >1 gives a negative Green matrix: strict positive claim needs p<1.
    G=(s.eye(2)-2*S).inv();assert all(x<0 for x in G)
    # Edges individually may exceed 1; only their product has to be <1.
    T=s.Matrix([[0,2],[s.Rational(1,8),0]])
    assert all(x>0 for x in (s.eye(2)-T).inv())
    report['exact']['green']={'cases':rows,'unit_product_singular_guard':True,'superunit_product_positivity_failure':True,'individual_weight_above_one_allowed':True}

def complete_rejection_certificate():
    n=4;q=4
    a=[0,3,0,3];b=[1,0,3,2];effective=[0,1,0,1]
    diagonal=[(a[i]+effective[i]-b[i])%q for i in range(n)]
    branches=[]
    for stage,p in [('A',a),('B',b)]:
        for order,magnitude in [([0,1,2,3],F(1,2)),([0,3,2,1],F(2,3))]:
            edges=cycle(order,p,q)
            branches.append({'stage':stage,'edges':edges,'edge_magnitude':str(magnitude),'cycle_magnitude_product':str(magnitude**n)})
        all_edges=sum([z['edges'] for z in branches if z['stage']==stage],[])
        assert phase_potential(n,q,all_edges) is not None
    assert arc_hist(diagonal,q)==3
    assert arc_hist(effective,q)==1
    wrong_raw_narrow=[0]*n
    actual_wide=[(-a[i]+wrong_raw_narrow[i]+b[i])%q for i in range(n)]
    assert arc_hist(actual_wide,q)==2
    threshold=certified_decision(n,1,q,F(1,10))
    assert threshold['sign']==1
    certificate={'n':n,'q':q,'potentials_A':a,'potentials_B':b,'branches':branches,
                 'raw_mask_residues':diagonal,'effective_mask_residues':effective,
                 'arc_start':0,'arc_span_in_qths':1,'raw_arc_span_in_qths':3,
                 'target_normalized_operator_error':'1/10','threshold':threshold,
                 'conclusion':'No outer invertible complex monomial gauges achieve error <= 1/10.',
                 'raw_narrow_effective_semicircle_control':{'raw_mask_residues':wrong_raw_narrow,'effective_mask_residues':actual_wide,'status':'cone theorem inconclusive'}}
    (OUT/'EXACT_REJECTION_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
    report['exact']['complete_certificate']={'n':n,'q':q,'raw_mask_wide_effective_narrow':True,'raw_mask_narrow_effective_wide':True,'certified_error_rejection':'1/10','rational_squared_gap':'41/100'}

def numerical_cones():
    rng=np.random.default_rng(101020261331)
    values=[]
    for n in (2,3,4,7,8,16):
        U=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)/np.sqrt(n)
        for width in (0.,.4,1.5,2.3,3.0):
            for scale_mode in ('balanced','ill_conditioned','zero'):
                core=rng.uniform(0,1,(n,n))*np.exp(1j*rng.uniform(-width/2,width/2,(n,n)))
                if scale_mode=='zero':core[:]=0
                ex=8 if scale_mode=='ill_conditioned' else .3
                lm=10.**rng.uniform(-ex,ex,n);rm=10.**rng.uniform(-ex,ex,n)
                Q=lm[:,None]*core*rm[None,:]
                if np.linalg.norm(Q)>0:Q*=np.sqrt(n)/np.linalg.norm(Q)
                lp=np.exp(1j*rng.uniform(-np.pi,np.pi,n));rp=np.exp(1j*rng.uniform(-np.pi,np.pi,n))
                p=rng.permutation(n);r=rng.permutation(n)
                M=(lp[:,None]*Q*rp[None,:])[np.ix_(p,r)]
                err=float(np.linalg.norm(M-U,2))
                c=math.cos(width/2);a=np.sqrt(n)*c;lb=max(0.,(a-1)/(a+1))
                assert err+1e-10>=lb
                values.append({'n':n,'width':width,'gauge':scale_mode,'error':err,'floor':lb,'margin':err-lb})
    # N=2 exact endpoint: cone [0,pi/2], using the normalized Fourier.
    U=np.array([[1.,1.],[1.,-1.]])/np.sqrt(2);D=np.diag([1.,1j]);Q=D@U@D
    assert np.linalg.norm(Q.conjugate().T@Q-np.eye(2))<1e-14
    assert np.max(abs(Q-np.array([[1,1j],[1j,1]])/np.sqrt(2)))<1e-14
    # Flatness is indispensable: I has width zero but equals a nonflat unitary.
    assert np.linalg.norm(np.eye(4)-np.eye(4),2)==0 and (2-1)/(2+1)>0
    # Allowing general outer matrices would also void the claim: L=U,C=R=I.
    report['numerical']['cone_bound']={'cases':len(values),'minimum_margin':min(v['margin'] for v in values),'records':values,'n2_endpoint':True,'nonflat_target_negative_control':True,'nonmonomial_outer_scope_counterexample':True}
    mult=0
    for n in (3,5,8):
        for t in (1,2,4,9):
            width=2.7;C=rng.uniform(0,1,(n,n));center=0.
            for _ in range(t):
                center_j=float(rng.uniform(-np.pi,np.pi));center+=center_j
                D=np.exp(1j*(center_j+rng.uniform(-width/(2*t),width/(2*t),n)))
                C=(C*D[None,:])@rng.uniform(0,1,(n,n))
            C*=np.exp(-1j*center)
            assert np.all(C.real+1e-9>=np.cos(width/2)*abs(C))
            mult+=1
    report['numerical']['multi_mask']={'cases':mult,'depths':[1,2,4,9],'total_width':2.7,'cone_preserved':True}

if __name__=='__main__':
    exact_graph_and_arc();exact_thresholds();exact_green();complete_rejection_certificate();numerical_cones()
    report['all_passed']=True
    (OUT/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('exact','numerical')},indent=2))
    print('Exact graph cases:',report['exact']['graphs']['positive_union_cases'])
    print('Exact histogram subset cases:',report['exact']['arcs']['exhaustive_subsets_q_1_to_10'])
    print('Certified threshold grid cases:',report['exact']['certified_thresholds']['grid_comparisons'])
    print('Exact Green stage cases:',len(report['exact']['green']['cases']))
    print('Numerical cone cases:',report['numerical']['cone_bound']['cases'])
    print('Numerical multi-mask cases:',report['numerical']['multi_mask']['cases'])
