"""Exact Fourier conjugates of path Green operators, without Fourier calls.

The implementation is in exact field arithmetic. It is not automatically a
bounded-word or stable floating-point algorithm. Primitive q is supplied.
"""
from collections import Counter


class Counted:
    def __init__(self,field):
        self.field=field;self.zero=field.zero;self.one=field.one;self.count=Counter()
    def add(self,a,b):self.count['add']+=1;return self.field.add(a,b)
    def sub(self,a,b):self.count['sub']+=1;return self.field.sub(a,b)
    def mul(self,a,b):self.count['mul']+=1;return self.field.mul(a,b)
    def inv(self,a):self.count['inverse']+=1;return self.field.inv(a)
    def integer(self,a):self.count['integer_embed']+=1;return self.field.integer(a)


class FourierPathGreen:
    """Prepare T, T+I, T+I/2 and their diagonal-plus-rank-two conjugates.

    T has diagonal3 and adjacent off-diagonal -1. All scalar setup is paid.
    Over C all pivots below are nonzero. Finite-field pivots must also be
    nonzero; unsupported modular pivots raise rather than divide by zero.
    """
    def __init__(self,field,n,q):
        if n<4 or n&(n-1):raise ValueError('dyadic N>=4 required')
        self.n=n;self.c=c=Counted(field)
        self.two=c.integer(2);self.three=c.integer(3)
        self.half=c.inv(self.two);self.quarter=c.mul(self.half,self.half)
        self.eighth=c.mul(self.quarter,self.half)
        self.inv_n=c.inv(c.integer(n))
        self.roots=[c.one]
        for _ in range(1,n):self.roots.append(c.mul(self.roots[-1],q))
        if c.mul(self.roots[-1],q)!=c.one or self.roots[n//2]==c.one:
            raise ValueError('primitive Nth root required')
        self.minus=[self.roots[-j%n] for j in range(n)]
        self.diagonal=[c.sub(c.sub(self.three,self.roots[j]),self.minus[j]) for j in range(n)]
        self.v1=[c.mul(self.inv_n,p) for p in self.roots]
        self.source={};self.target={}
        for name,alpha in [('zero',c.zero),('one',c.one),('half',self.half)]:
            self.source[name]=self._prepare_source(alpha)
            self.target[name]=self._prepare_target(alpha)
        self.preparation_operations=dict(c.count)

    def _prepare_source(self,alpha):
        c=self.c;main=c.add(self.three,alpha);inverses=[];pivot=main
        for j in range(self.n):
            if pivot==c.zero:raise ValueError('zero source pivot')
            inverse=c.inv(pivot);inverses.append(inverse)
            if j+1<self.n:pivot=c.sub(main,inverse)
        return inverses

    def _prepare_target(self,alpha):
        c=self.c;g=[]
        for value in self.diagonal:
            value=c.add(value,alpha)
            if value==c.zero:raise ValueError('zero target diagonal pivot')
            g.append(c.inv(value))
        w2=[c.mul(g[j],self.minus[j]) for j in range(self.n)]
        a,b,d,e=c.one,c.zero,c.zero,c.one
        for j in range(self.n):
            a=c.add(a,c.mul(self.v1[j],g[j]))
            b=c.add(b,c.mul(self.v1[j],w2[j]))
            d=c.add(d,c.mul(self.inv_n,g[j]))
            e=c.add(e,c.mul(self.inv_n,w2[j]))
        determinant=c.sub(c.mul(a,e),c.mul(b,d))
        if determinant==c.zero:raise ValueError('singular Woodbury correction')
        reciprocal=c.inv(determinant)
        correction=(c.mul(e,reciprocal),c.mul(b,reciprocal),
                    c.mul(d,reciprocal),c.mul(a,reciprocal))
        return g,w2,correction

    def source_t(self,x):
        if len(x)!=self.n:raise ValueError('exactly N input coordinates required')
        c=self.c;n=self.n
        out=[c.mul(self.three,v) for v in x]
        for j in range(n-1):
            out[j]=c.sub(out[j],x[j+1]);out[j+1]=c.sub(out[j+1],x[j])
        return out

    def target_h(self,y):
        if len(y)!=self.n:raise ValueError('exactly N input coordinates required')
        c=self.c;n=self.n;first=second=c.zero
        for j in range(n):
            first=c.add(first,c.mul(self.roots[j],y[j]))
            second=c.add(second,y[j])
        first=c.mul(first,self.inv_n);second=c.mul(second,self.inv_n)
        return [c.add(c.add(c.mul(self.diagonal[j],y[j]),first),c.mul(self.minus[j],second))
                for j in range(n)]

    def source_solve(self,x,name='zero'):
        if len(x)!=self.n:raise ValueError('exactly N input coordinates required')
        c=self.c;g=self.source[name];rhs=list(x)
        for j in range(1,self.n):rhs[j]=c.add(rhs[j],c.mul(g[j-1],rhs[j-1]))
        out=[c.zero]*self.n;out[-1]=c.mul(g[-1],rhs[-1])
        for j in range(self.n-2,-1,-1):out[j]=c.mul(g[j],c.add(rhs[j],out[j+1]))
        return out

    def target_solve(self,y,name='zero'):
        if len(y)!=self.n:raise ValueError('exactly N input coordinates required')
        c=self.c;g,w2,(a,b,d,e)=self.target[name]
        z=[c.mul(g[j],y[j]) for j in range(self.n)]
        first=second=c.zero
        for j in range(self.n):
            first=c.add(first,c.mul(self.v1[j],z[j]))
            second=c.add(second,c.mul(self.inv_n,z[j]))
        u=c.sub(c.mul(a,first),c.mul(b,second))
        v=c.sub(c.mul(e,second),c.mul(d,first))
        return [c.sub(c.sub(z[j],c.mul(g[j],u)),c.mul(w2[j],v)) for j in range(self.n)]

    def source_s(self,x):
        c=self.c
        return [c.add(a,b) for a,b in zip(self.source_solve(x),self.source_solve(x,'one'))]

    def target_s(self,y):
        c=self.c
        return [c.add(a,b) for a,b in zip(self.target_solve(y),self.target_solve(y,'one'))]

    def source_s_inverse(self,x):
        c=self.c
        return [c.sub(c.add(c.mul(self.half,t),c.mul(self.quarter,v)),c.mul(self.eighth,g))
                for t,v,g in zip(self.source_t(x),x,self.source_solve(x,'half'))]

    def target_s_inverse(self,y):
        c=self.c
        return [c.sub(c.add(c.mul(self.half,t),c.mul(self.quarter,v)),c.mul(self.eighth,g))
                for t,v,g in zip(self.target_h(y),y,self.target_solve(y,'half'))]
