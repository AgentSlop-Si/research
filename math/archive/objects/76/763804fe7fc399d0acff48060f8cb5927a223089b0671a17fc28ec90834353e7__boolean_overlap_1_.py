"""A fully exact, single-threaded audit of Boolean-quotient linear extraction.

NOT a new FFT algorithm. Given an arithmetic DAG, compute its degree <= 1
multilinear projection on {0,1}^n via one-hot evaluations, and construct an
ordinary linear arithmetic DAG for the projection.

Only +,-,* and constants over a prime field.  A projected scalar coefficient
requires input-independent preparation.  `audit` explicitly charges dictionary
arithmetic during the preparation; the resulting linear DAG's gate count is
reported separately.  No complex numeric oracle, memoized FFT, or threads.
"""
from __future__ import annotations
from dataclasses import dataclass
import random

P=998244353
PRIMITIVE=3


@dataclass(frozen=True)
class Node:
    op: str
    a: int=-1
    b: int=-1
    val: int=0


class Circuit:
    def __init__(self, n: int, p: int=P):
        if n < 1 or p < 2:
            raise ValueError("n must be positive and modulus >= 2")
        self.n=n; self.p=p; self.nodes:list[Node]=[]
        self.inputs=[self._put('input', val=i) for i in range(n)]
        self._consts={}

    def _put(self, op, a=-1, b=-1, val=0):
        i=len(self.nodes);self.nodes.append(Node(op,a,b,val));return i

    def const(self, v:int):
        v%=self.p
        if v not in self._consts:
            self._consts[v]=self._put('const',val=v)
        return self._consts[v]

    def add(self, a,b):return self._put('add',a,b)
    def sub(self, a,b):return self._put('sub',a,b)
    def mul(self, a,b):return self._put('mul',a,b)
    def neg(self,a):return self.sub(self.const(0),a)

    def eval_all(self,x):
        if len(x)!=self.n:raise ValueError("incorrect input length")
        p=self.p;vs=[]
        for node in self.nodes:
            op=node.op
            if op=='input':v=int(x[node.val])
            elif op=='const':v=node.val
            elif op=='add':v=vs[node.a]+vs[node.b]
            elif op=='sub':v=vs[node.a]-vs[node.b]
            elif op=='mul':v=vs[node.a]*vs[node.b]
            else:raise ValueError(op)
            vs.append(v%p)
        return vs

    def eval(self,x,outputs):
        vals=self.eval_all(x)
        return [vals[i] for i in outputs]

    def work(self):
        return sum(node.op in ('add','sub','mul') for node in self.nodes)

    def onehot_audit(self):
        """Return per-wire f(0), (f(e_i)-f(0)) coefficients.

        The operation count is a *proxy* for coefficient dictionary work, not a
        C/word-RAM exact instruction trace. It includes all visited entries.
        """
        p=self.p
        base=[];delta=[];pair_overlap=0;prod_hist=[];meta=0
        for v,node in enumerate(self.nodes):
            if node.op=='input':
                c=0; d={node.val:1}; meta+=1
            elif node.op=='const':
                c=node.val;d={}
            else:
                ac,bc=base[node.a],base[node.b]
                ad,bd=delta[node.a],delta[node.b]
                keys=ad.keys()|bd.keys()
                d={};meta+=len(ad)+len(bd)+1
                if node.op=='add':
                    c=(ac+bc)%p
                    for i in keys:
                        t=(ad.get(i,0)+bd.get(i,0))%p
                        if t:d[i]=t
                elif node.op=='sub':
                    c=(ac-bc)%p
                    for i in keys:
                        t=(ad.get(i,0)-bd.get(i,0))%p
                        if t:d[i]=t
                elif node.op=='mul':
                    c=ac*bc%p
                    overlap=len(ad.keys()&bd.keys())
                    pair_overlap+=overlap;prod_hist.append((v,overlap))
                    meta+=overlap
                    for i in keys:
                        da,db=ad.get(i,0),bd.get(i,0)
                        t=(ac*db+bc*da+da*db)%p
                        if t:d[i]=t
                else:raise ValueError(node.op)
            base.append(c);delta.append(d)
        return {'base':base,'delta':delta,'overlap':pair_overlap,
                'product_overlap_histogram':prod_hist,'metadata_work_proxy':meta,
                'max_support':max(map(len,delta)),'total_support':sum(map(len,delta))}

    def project_linear(self, outputs, audit=None):
        """Construct linear/affine circuit for f(0)+sum_i(f(e_i)-f(0))*x_i.

        All new multiplication gates have a constant input. The preparation
        of scalar coefficients is separate and *not* assumed free in audits.
        """
        if audit is None:audit=self.onehot_audit()
        q=Circuit(self.n,self.p);p=self.p
        zero=q.const(0)
        ids=[]
        def plus(a,b):
            if a==zero:return b
            if b==zero:return a
            return q.add(a,b)
        def minus(a,b):
            if b==zero:return a
            if a==zero:return q.sub(zero,b)
            return q.sub(a,b)
        def scaled(a,c):
            c%=p
            if a==zero or c==0:return zero
            if c==1:return a
            return q.mul(a,q.const(c))
        for v,node in enumerate(self.nodes):
            if node.op=='input':lv=q.inputs[node.val]
            elif node.op=='const':lv=zero
            elif node.op=='add':lv=plus(ids[node.a],ids[node.b])
            elif node.op=='sub':lv=minus(ids[node.a],ids[node.b])
            elif node.op=='mul':
                a,b=node.a,node.b
                lv=plus(scaled(ids[a],audit['base'][b]),
                        scaled(ids[b],audit['base'][a]))
                for i in sorted(audit['delta'][a].keys() & audit['delta'][b].keys()):
                    coef=audit['delta'][a][i]*audit['delta'][b][i]%p
                    lv=plus(lv,scaled(q.inputs[i],coef))
            else:raise ValueError(node.op)
            ids.append(lv)
        result=[]
        for j in outputs:
            result.append(plus(q.const(audit['base'][j]),ids[j]))
        return q,result

    def check_linear(self):
        """All data-data nonlinear multiplications forbidden."""
        symbolic=[]
        for node in self.nodes:
            if node.op=='input':symbolic.append(False)
            elif node.op=='const':symbolic.append(True)
            elif node.op in ('add','sub'):
                symbolic.append(symbolic[node.a] and symbolic[node.b])
            elif node.op=='mul':
                if not(symbolic[node.a] or symbolic[node.b]):return False
                symbolic.append(symbolic[node.a] and symbolic[node.b])
            else:raise ValueError(node.op)
        return True


def fft_circuit(c:Circuit,x):
    n=len(x)
    if n==1:return list(x)
    if n & (n-1):raise ValueError("power-of-two length required")
    if (c.p-1)%n:raise ValueError("field lacks primitive nth root")
    half=n//2
    even=fft_circuit(c,x[::2])
    odd=fft_circuit(c,x[1::2])
    w=pow(PRIMITIVE,(c.p-1)//n,c.p)
    y=[-1]*n
    for j in range(half):
        term=c.mul(odd[j],c.const(pow(w,j,c.p)))
        y[j]=c.add(even[j],term)
        y[j+half]=c.sub(even[j],term)
    return y


def nonlinear_fft_case(n,variant='squares',p=P):
    c=Circuit(n,p)
    if variant=='plain':xs=list(c.inputs)
    elif variant=='squares':xs=[c.mul(t,t) for t in c.inputs]
    elif variant=='boolean_null':
        # x + x(1-x) == x on binary inputs, false for arbitrary field input.
        one=c.const(1)
        xs=[c.add(t,c.mul(t,c.sub(one,t))) for t in c.inputs]
    elif variant=='hybrid':
        one=c.const(1)
        xs=[c.add(c.mul(t,t),c.mul(t,c.sub(one,t))) for t in c.inputs]
    else:raise ValueError(variant)
    return c,fft_circuit(c,xs)


def direct_dft(x,p=P):
    """Independent defining-sum reference; skips literal zero coefficients."""
    n=len(x);w=pow(PRIMITIVE,(p-1)//n,p)
    active=[(j,int(t)%p) for j,t in enumerate(x) if int(t)%p]
    return [sum(v*pow(w,(k*j)%n,p) for j,v in active)%p for k in range(n)]


def experiment(sizes=(4,8,16,32,64),seed=20261009):
    rng=random.Random(seed);rows=[]
    for n in sizes:
        for variant in ('plain','squares','boolean_null','hybrid'):
            c,out=nonlinear_fft_case(n,variant)
            audit=c.onehot_audit(); q,z=c.project_linear(out,audit)
            assert q.check_linear()
            for i in range(n):
                x=[int(j==i) for j in range(n)]
                assert c.eval(x,out)==direct_dft(x)
                assert q.eval(x,z)==direct_dft(x)
            for _ in range(10):
                xb=[rng.randrange(2) for _ in range(n)]
                xf=[rng.randrange(P) for _ in range(n)]
                assert c.eval(xb,out)==direct_dft(xb)
                assert q.eval(xf,z)==direct_dft(xf)
            rows.append({'n':n,'variant':variant,'original_gates':c.work(),
                         'projected_linear_gates':q.work(),
                         'multiplication_overlap':audit['overlap'],
                         'metadata_work_proxy':audit['metadata_work_proxy'],
                         'total_support_storage':audit['total_support'],
                         'verified_columns':n,'verified_binary_vectors':10,
                         'verified_field_vectors':10})
    return rows


if __name__=='__main__':
    import json,argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='audit_results.json')
    args=parser.parse_args()
    rows=experiment()
    with open(args.output,'w') as f:json.dump({'model':'F_998244353','rows':rows},f,indent=2)
    for x in rows:
        print(f"n={x['n']:>3} {x['variant']:<12} gates={x['original_gates']:>5}"
              f" lift={x['projected_linear_gates']:>5} overlaps={x['multiplication_overlap']:>4}"
              f" prep_proxy={x['metadata_work_proxy']:>7}")
