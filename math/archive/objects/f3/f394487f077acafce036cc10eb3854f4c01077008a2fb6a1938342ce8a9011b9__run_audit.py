"""Exact checks of the regularization and the finite singular-limit identity."""
import json
from pathlib import Path
from cyclic import prepare, apply_regularized
from prior_exact_arithmetic import PrimeField, CyclotomicField, mm, mv, fourier


def diag(f,x): return [[value if i==j else f.zero for j in range(len(x))] for i,value in enumerate(x)]
def scale(f,s,a): return [[f.mul(s,x) for x in row] for row in a]
def add(f,a,b): return [[f.add(x,y) for x,y in zip(row,other)] for row,other in zip(a,b)]
def product(f,*factors):
    out=factors[0]
    for factor in factors[1:]: out=mm(f,out,factor)
    return out
def polynomial(f,a,kernel):
    ident=diag(f,[f.one]*len(a)); out=scale(f,kernel[-1],ident)
    for coefficient in kernel[-2::-1]: out=add(f,mm(f,a,out),scale(f,coefficient,ident))
    return out
def power(f,a,n):
    out=diag(f,[f.one]*len(a))
    for _ in range(n): out=mm(f,out,a)
    return out


def data(f,n):
    q=f.root(n); powers=[f.power(q,j) for j in range(n)]
    qi=[powers[-j%n] for j in range(n)]; ni=f.inv(f.integer(n))
    fact=[f.one]
    for j in range(1,n):fact.append(f.mul(fact[-1],f.sub(f.one,powers[j])))
    kernel=[f.inv(x) for x in fact]
    u=diag(f,qi)
    weights=[f.sub(q,qi[j]) for j in range(n-1)]+[f.neg(f.mul(q,ni))]
    w=[[weights[i] if j==(i+1)%n else f.zero for j in range(n)] for i in range(n)]
    c=add(f,u,w); v=scale(f,f.neg(f.one),mm(f,w,diag(f,powers)))
    g=[f.one]
    for i in range(n-1):g.append(f.mul(g[-1],f.inv(v[i][i+1])))
    e=[f.one]
    for k in range(1,n):e.append(f.mul(e[-1],f.sub(f.one,qi[k])))
    a=[[f.one if i==j+1 else f.zero for j in range(n)] for i in range(n)]
    transform=fourier(f,n)
    inverse_transform=scale(f,ni,[[powers[-i*j % n] for j in range(n)] for i in range(n)])
    return q,kernel,u,w,c,v,g,e,a,transform,inverse_transform


def regular_parameters(p,n):
    # Oracle setup only. Enumerating a field is not a proposed algorithm step.
    roots={pow(a,n,p):a for a in range(1,p)}
    for t in range(2,p):
        target=(1-pow(t,n,p))%p
        if target in roots:return t,roots[target]
    return None


def one_case(f,n,label,parameters=None):
    q,k,u,w,c,v,g,e,a,ft,fi=data(f,n)
    gi=[f.inv(x) for x in g];ei=[f.inv(x) for x in e]
    ident=diag(f,[f.one]*n)
    assert power(f,v,n)==ident
    assert mm(f,u,v)==scale(f,q,mm(f,v,u))
    # The limit is exact and does not use numerical near-singular evaluation.
    jordan=product(f,diag(f,e),a,diag(f,ei))
    assert product(f,ft,diag(f,gi),c,diag(f,g),fi)==jordan
    h=polynomial(f,c,k)
    limit=product(f,diag(f,g),fi,diag(f,e),polynomial(f,a,k),diag(f,ei),ft,diag(f,gi))
    assert limit==h
    result={'field':label,'n':n,'limit_matrix_identity':True,'limit_basis_outputs':n}
    if parameters:
        t,alpha=parameters;plan=prepare(f,n,q,t,alpha)
        ct=add(f,u,scale(f,t,w))
        d=product(f,diag(f,g),fi,diag(f,plan['d']),ft,diag(f,gi))
        di=product(f,diag(f,g),fi,diag(f,plan['di']),ft,diag(f,gi))
        assert product(f,d,di)==ident
        assert scale(f,alpha,product(f,d,u,di))==ct
        assert power(f,ct,n)==scale(f,f.power(alpha,n),ident)
        hdirect=polynomial(f,ct,k)
        for j in range(n):
            x=[f.one if i==j else f.zero for i in range(n)]
            observed,cost=apply_regularized(f,plan,x)
            assert observed==mv(f,hdirect,x)
        ell=n.bit_length()-1
        assert cost=={'mul':2*n*ell+7*n,'add':2*n*ell,'sub':2*n*ell}
        result.update(t=t,alpha=alpha,regular_basis_outputs=n,action_cost=cost,
                      scalar_preparation=plan['preparation'])
    return result


def main():
    rows=[]
    for p in (257,65537):
        f=PrimeField(p)
        for n in (2,4,8,16,32):
            rows.append(one_case(f,n,f'F_{p}',regular_parameters(p,n)))
    for n in (2,4,8):rows.append(one_case(CyclotomicField(n),n,f'Q(zeta_{n})'))
    result={'status':'PASS','cases':len(rows),
            'limit_basis_outputs':sum(r['limit_basis_outputs'] for r in rows),
            'regular_basis_outputs':sum(r.get('regular_basis_outputs',0) for r in rows),
            'scope':'Regular parameter costs four FFTs; singular target retains a full triangular kernel.',
            'cases_detail':rows}
    path=Path(__file__).with_name('audit_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases_detail'},indent=2))


if __name__=='__main__':main()
