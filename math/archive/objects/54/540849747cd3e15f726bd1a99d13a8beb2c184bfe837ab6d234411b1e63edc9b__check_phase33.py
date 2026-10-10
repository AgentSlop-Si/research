#!/usr/bin/env python3
"""Independent reconstruction of the stated Phase33 formulas and instances."""
import json
from pathlib import Path
from random import Random
from exact_utils import Field,root,prime_by_trial_division


def specified_cycles(n,q,seed):
    # Reconstruct the documented seeded input instance, not uploaded code.
    rng=Random(seed+17*n);orders=[];successors=[]
    while len(orders)<q:
        order=list(range(n));rng.shuffle(order)
        successor=[0]*n
        for i,v in enumerate(order):successor[v]=order[(i+1)%n]
        slope=(successor[1]-successor[0])%n
        affine=all(successor[x]==(slope*x+successor[0])%n for x in range(n))
        if affine or successor in successors:continue
        if any(all(successor[t[x]]==t[successor[x]] for x in range(n)) for t in successors):continue
        orders.append(order);successors.append(successor)
    return orders


def entries(order,alpha,columns,p):
    n=len(order);pos=[0]*n
    for i,v in enumerate(order):pos[v]=i
    assert alpha%p and (1-pow(alpha,n,p))%p
    den=pow((1-pow(alpha,n,p))%p,-1,p)
    powers=[pow(alpha,i,p)*den%p for i in range(n)]
    return [[powers[(pos[i]-pos[j])%n] for j in columns] for i in range(n)]


def two_term():
    expected={998244353:[719251419,637742998,945626350,12457656,573672172,619466537,201128490,631340830],
              2013265921:[1918301059,179591294,334935703,508324165,280352103,1724252133,812437798,1572229769]}
    out=[]
    for nindex,n in enumerate([8,16,32,64,128,256,512,1024]):
        cycles=specified_cycles(n,2,330033)
        for p,g in [(998244353,3),(2013265921,31)]:
            assert prime_by_trial_division(p)
            field=Field(p);w=root(n,p,g)
            a,b=[entries(c,alpha,[0,1,2],p) for c,alpha in zip(cycles,[3,5])]
            k=[]
            for i,((A,C,E),(B,D,H)) in enumerate(zip(a,b)):
                f1,f2=pow(w,-i,p),pow(w,-2*i,p)
                k.append([C*H%p,-D*E%p,-f2*B*C%p,f2*A*D%p,f1*B*E%p,-f1*A*H%p])
                # Direct 3x3 expansion control with unrelated nonzero gauges.
                aa,bb,cc,dd=2,7,11,13
                direct=field.det([[A,B,1],[aa*C%p,bb*D%p,f1],[cc*E%p,dd*H%p,f2]])
                compound=[aa*dd,bb*cc,aa,bb,cc,dd]
                assert direct==sum(x*y for x,y in zip(k[-1],compound))%p
            det=field.det(k[:6]);assert det==expected[p][nindex]!=0
            out.append({'N':n,'prime':p,'rows':list(range(6)),'minor':k[:6],'determinant':det})
    return out


def five_term(n):
    p=998244353;field=Field(p);w=root(n,p,3)
    cycles=specified_cycles(n,5,320031)
    e=[entries(c,7+2*s,list(range(6)),p) for s,c in enumerate(cycles)]
    left=[];jacobian=[];residual=[];last=[]
    for i in range(n):
        b=[[e[s][i][j] for s in range(5)] for j in range(5)]
        bi=field.inverse(b)
        rhs=[pow(w,-i*j,p) for j in range(5)]
        l=[sum(bi[s][j]*rhs[j] for j in range(5))%p for s in range(5)]
        assert all(l)
        assert all(sum(b[j][s]*l[s] for s in range(5))%p==rhs[j] for j in range(5))
        h=[e[s][i][5] for s in range(5)]
        z=[sum(h[s]*bi[s][ell] for s in range(5))%p for ell in range(5)]
        row=[-z[ell]*b[ell][s]*l[s]%p for ell in range(1,5) for s in range(5)]
        row += [h[s]*l[s]%p for s in range(5)]
        jacobian.append(row);left.append(l);last.append([h[s]*l[s]%p for s in range(5)])
        residual.append((pow(w,-5*i,p)-sum(h[s]*l[s] for s in range(5)))%p)
    right=field.solve(last[:5],[pow(w,-5*i,p) for i in range(5)])
    assert all(right)
    mismatch=[i for i in range(n) if (sum(x*y for x,y in zip(last[i],right))-pow(w,-5*i,p))%p]
    assert mismatch==list(range(5,n))
    result={'N':n,'whole_matched_columns':5,'extra_exact_rows':list(range(5)),
            'extra_mismatches':len(mismatch),'right_extra_gauges':right,'all_left_gauges_nonzero':True}
    if n>=32:
        rank=field.rank(jacobian);aug=field.rank([r+[v] for r,v in zip(jacobian,residual)])
        assert rank==25 and aug==26
        result.update({'jacobian_rank':rank,'augmented_rank':aug,'base_extra_column_mismatches':sum(bool(v) for v in residual)})
    return result


def separated_groups(orders):
    n=len(orders[0]);m=n//2
    left=set(orders[0][:m]);right=set(orders[0][-m:])
    for order in orders[1:]:
        union=[v for v in order if v in left or v in right]
        lower=set(union[:m]);upper=set(union[m:])
        candidates=[(left&lower,right&upper),(left&upper,right&lower)]
        a,b=max(candidates,key=lambda pair:min(len(pair[0]),len(pair[1])))
        m//=2;left=set(sorted(a)[:m]);right=set(sorted(b)[:m])
    return sorted(left),sorted(right)


def separated_controls():
    p=998244353;out=[]
    for q,n in [(2,64),(3,256),(4,2048),(5,8192)]:
        orders=specified_cycles(n,q,4512)
        a,b=separated_groups(orders);m=n//(1<<q)
        assert len(a)==len(b)==m and not set(a)&set(b)
        for s,order in enumerate(orders):
            pos={v:i for i,v in enumerate(order)}
            assert max(pos[x] for x in a)<min(pos[x] for x in b) or max(pos[x] for x in b)<min(pos[x] for x in a)
            block=entries(order,3+2*s,b,p)
            pivot=block[a[0]][0];assert pivot
            for i in a:
                assert all(block[i][j]*pivot%p==block[i][0]*block[a[0]][j]%p for j in range(m))
        assert m*m>q*n
        out.append({'N':n,'q':q,'group_size':m,'rank_one_checked_entries_per_term':m*m,
                    'spectral_error_floor_squared_numerator':m*m-q*n,
                    'spectral_error_floor_squared_denominator':n*(m-q)})
    return out


def main():
    data={'status':'PASS','two_term_certificates':two_term(),
          'five_term_controls':[five_term(n) for n in [8,16,32,64,128,256,512,1024,4096]],
          'separated_controls':separated_controls(),
          'scope':'Finite fixed-pair exclusion; nonsingular-chart dimension; local Jacobian; partial interpolation; additive-only all-N gate.'}
    Path('PHASE33_RESULTS.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','two_term_certificates':len(data['two_term_certificates']),
                      'five_term_sizes':len(data['five_term_controls']),'largest_five_term_N':4096,'separated_cases':4},sort_keys=True))


if __name__=='__main__':main()
