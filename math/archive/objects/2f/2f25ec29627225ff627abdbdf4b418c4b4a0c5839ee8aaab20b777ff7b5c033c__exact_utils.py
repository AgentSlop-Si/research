"""Review-authored modular linear algebra; no external dependencies."""
class Field:
    def __init__(self,p):
        self.p=p
    def inv(self,x):
        assert x % self.p
        return pow(x,-1,self.p)
    def eye(self,n):
        return [[int(i==j) for j in range(n)] for i in range(n)]
    def mul(self,a,b):
        bt=list(zip(*b));p=self.p
        return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]
    def rank(self,a):
        b=[row[:] for row in a];r=0;p=self.p
        for c in range(len(b[0])):
            t=next((i for i in range(r,len(b)) if b[i][c]%p),None)
            if t is None:continue
            b[r],b[t]=b[t],b[r];v=self.inv(b[r][c])
            for i in range(r+1,len(b)):
                z=b[i][c]*v%p
                if z:b[i]=[(x-z*y)%p for x,y in zip(b[i],b[r])]
            r+=1
            if r==len(b):break
        return r
    def det(self,a):
        b=[row[:] for row in a];out=1;p=self.p
        for c in range(len(b)):
            t=next((i for i in range(c,len(b)) if b[i][c]%p),None)
            if t is None:return 0
            if c!=t:b[c],b[t]=b[t],b[c];out=-out
            out=out*b[c][c]%p;v=self.inv(b[c][c])
            for i in range(c+1,len(b)):
                z=b[i][c]*v%p
                if z:b[i]=[(x-z*y)%p for x,y in zip(b[i],b[c])]
        return out%p
    def inverse(self,a):
        n=len(a);b=[row[:]+e for row,e in zip(a,self.eye(n))];p=self.p
        for c in range(n):
            t=next((i for i in range(c,n) if b[i][c]%p),None)
            if t is None:raise ValueError('singular')
            b[c],b[t]=b[t],b[c];v=self.inv(b[c][c]);b[c]=[x*v%p for x in b[c]]
            for i in range(n):
                if i!=c:
                    z=b[i][c]
                    if z:b[i]=[(x-z*y)%p for x,y in zip(b[i],b[c])]
        return [row[n:] for row in b]
    def solve(self,a,b):
        return [row[0] for row in self.mul(self.inverse(a),[[x] for x in b])]


def root(n,p,g):
    assert (p-1)%n==0
    z=pow(g,(p-1)//n,p)
    assert pow(z,n,p)==1
    if n>1 and n&(n-1)==0:assert pow(z,n//2,p)!=1
    return z


def prime_by_trial_division(p):
    from math import isqrt
    return p>=2 and (p==2 or p%2 and all(p%d for d in range(3,isqrt(p)+1,2)))
