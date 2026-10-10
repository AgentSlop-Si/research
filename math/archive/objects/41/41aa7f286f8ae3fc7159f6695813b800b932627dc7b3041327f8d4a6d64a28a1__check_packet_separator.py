#!/usr/bin/env python3
"""Independent controls for v19, including corrected inverse-density scope."""
import json
from pathlib import Path
from random import Random
from exact_utils import Field,root

P=998244353
F=Field(P)


def permutation_power(perm,step):
    out=[0]*len(perm);seen=set()
    for v in range(len(perm)):
        if v in seen:continue
        cycle=[];w=v
        while w not in seen:
            seen.add(w);cycle.append(w);w=perm[w]
        assert w==v
        for i,w in enumerate(cycle):out[w]=cycle[(i+step)%len(cycle)]
    return out


def green(perm,alpha):
    n=len(perm);den=F.eye(n)
    for v,w in enumerate(perm):den[w][v]=(den[w][v]-alpha)%P
    return F.inverse(den)


def shifted(g,perm,scalar):
    out=[None]*len(perm)
    for v,w in enumerate(perm):out[w]=[scalar*x%P for x in g[v]]
    return out


def packet_controls():
    rng=Random(84113);out=[]
    for n in (5,8,13,17):
        perm=list(range(n));rng.shuffle(perm)
        for b in (2,4,8):
            xi=root(b,P,3);alpha=3
            terms=[green(perm,alpha*pow(xi,r,P)%P) for r in range(b)]
            fused=green(permutation_power(perm,b),pow(alpha,b,P))
            rhs=[]
            for s in range(b):
                right=shifted(fused,permutation_power(perm,s),pow(alpha,s,P));rhs.append(right)
                left=[[sum(pow(xi,-r*s,P)*terms[r][i][j] for r in range(b))*F.inv(b)%P for j in range(n)] for i in range(n)]
                assert left==right
            coeff=[r*r+2*r+3 for r in range(b)]
            chat=[sum(coeff[r]*pow(xi,r*s,P) for r in range(b))*F.inv(b)%P for s in range(b)]
            literal=[[sum(coeff[r]*terms[r][i][j] for r in range(b))%P for j in range(n)] for i in range(n)]
            polynomial=[[b*sum(chat[s]*rhs[s][i][j] for s in range(b))%P for j in range(n)] for i in range(n)]
            assert literal==polynomial
            out.append({'N':n,'packet_width':b,'character_channels_checked':b,'arbitrary_weight_identity':True})
    return out


def polynomial_matrix(n,coeff):
    a=[[0]*n for _ in range(n)]
    for j in range(n):
        for step,value in enumerate(coeff):a[(j+step)%n][j]=(a[(j+step)%n][j]+value)%P
    return a


def rational_controls():
    out=[]
    for n in (11,17,32):
        for e in (0,1,2,3):
            for d in (0,1,2,3):
                m=(n-e)//2
                if d>=m:continue
                q=[1]+[3+2*j for j in range(d)]
                p=[2+j*j for j in range(e+1)]
                t=F.mul(F.inverse(polynomial_matrix(n,q)),polynomial_matrix(n,p))
                a=list(range(m+e,2*m+e));b=list(range(m))
                block=[[t[i][j] for j in b] for i in a]
                rank=F.rank(block);assert rank<=d
                out.append({'N':n,'denominator_degree':d,'numerator_degree':e,'rectangle_size':m,'rank':rank})
    return out


def separator_controls():
    rng=Random(198771);out=[]
    for u,s,v in [(3,1,4),(3,2,3),(4,3,2),(2,2,4)]:
        n=u+s+v
        for _ in range(100):
            a=[[rng.randrange(1,100) for j in range(n)] for i in range(n)]
            for i in range(u):
                for j in range(u+s,n):a[i][j]=0
            # Force a singular principal block, outside v19's sufficient guard.
            for j in range(u):a[0][j]=0
            try:ai=F.inverse(a);break
            except ValueError:pass
        else:raise AssertionError('No test matrix found')
        assert F.det([row[:u] for row in a[:u]])==0
        rank=F.rank([row[u+s:] for row in ai[:u]])
        complement=[row[u:] for row in a[:u+s]]
        assert rank==F.rank(complement)-s and rank<=s
        out.append({'U':u,'S':s,'V':v,'full_inverse_exists':True,'principal_UU_singular':True,
                    'reverse_VU_nonzero':True,'inverse_cross_rank':rank,'complementary_block_rank':F.rank(complement)})
    return out


def density_controls():
    out=[]
    for n in (4,8,16,17):
        z=root(n,P,3);assert z!=1
        fourier=[[pow(z,i*j,P) for j in range(n)] for i in range(n)]
        # Independent nonzero endpoint scalings and row/column permutations.
        row_order=list(reversed(range(n)));col_order=list(range(1,n))+[0]
        target=[[(i+2)*(j+3)*fourier[row_order[i]][col_order[j]]%P for j in range(n)] for i in range(n)]
        denominator=F.inverse(target)
        assert all(x for row in denominator for x in row)
        assert F.mul(denominator,target)==F.eye(n)
        out.append({'N':n,'inverse_nonzero_entries':n*n,'required_graph_treewidth':n-1})
    return out


def main():
    result={'status':'PASS','packet':packet_controls(),'rational_scan':rational_controls(),
            'guard_free_separator':separator_controls(),'direct_inverse_density':density_controls(),
            'correction':'A^-1 monomially Fourier implies dense A; no constant-degree sparse direct-inverse escape exists in this model.',
            'cost_scope':'Only a character-weight packet has the demonstrated O(N) single-stride solve; a general numerator must be charged.'}
    Path('PACKET_SEPARATOR_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','packet_cases':len(result['packet']),
                      'rational_cases':len(result['rational_scan']),'singular_principal_separator_cases':4,
                      'density_cases':4},sort_keys=True))


if __name__=='__main__':main()
