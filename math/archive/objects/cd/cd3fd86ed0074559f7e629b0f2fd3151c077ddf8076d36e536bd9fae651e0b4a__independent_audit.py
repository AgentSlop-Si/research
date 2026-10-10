"""Independent checks; imports only independently authored evaluator and packages.
Uploaded JSON is read as data. No uploaded executable is run or imported.
"""
from pathlib import Path
import json
import math
import random
import hashlib
from fractions import Fraction
import numpy as np
from independent_mixer import Mixer, Forest, Arithmetic, validate_and_invert

BASE = Path(__file__).resolve().parent
P = 998244353


def invert_mod(a):
    n = len(a)
    v = [[int(x) % P for x in row] + [int(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if v[i][j])
        v[j], v[pivot] = v[pivot], v[j]
        q = pow(v[j][j], -1, P)
        v[j] = [x*q % P for x in v[j]]
        for i in range(n):
            if i != j:
                c = v[i][j]
                v[i] = [(x-c*y) % P for x,y in zip(v[i],v[j])]
    return [row[n:] for row in v]


def dense_forest(parents, alpha, inverse=False):
    n=len(parents); imag=pow(3,(P-1)//4,P)
    sign=-1 if inverse else 1
    q=[[int(i==j) for j in range(n)] for i in range(n)]
    for i,parent in enumerate(parents):
        if parent!=-1:
            q[i][parent]=q[parent][i]=(-sign*imag*alpha)%P
    r=invert_mod(q)
    return [[(2*r[i][j]-int(i==j))%P for j in range(n)] for i in range(n)]


def mv(a,x):
    return [sum(v*w for v,w in zip(row,x))%P for row in a]


def exact_checks():
    out=[]; rng=random.Random(1381551)
    for n in (2,4,6,8,16,32,64,128,256,1024):
        perm=list(range(n));rng.shuffle(perm);s=Mixer(perm,p=P)
        assert s.op.count==9*n+2*s.tree_size+6
        for _ in range(3):
            x=[rng.randrange(P) for _ in range(n)]
            assert s.apply(s.apply(x),True)==x
            assert s.apply(s.apply(x,True))==x
            assert s.involution(s.involution(x))==x
        before=s.op.count;s.apply(x);forward=s.op.count-before
        before=s.op.count;s.apply(x,True);reverse=s.op.count-before
        assert forward==41*n//2+8*s.tree_size-16
        assert reverse==45*n//2+8*s.tree_size-15
        if n<=16:
            ds=[]
            for f,a in ((s.path1,pow(32,-1,P)),(s.path2,pow(32,-1,P)),(s.tree,2)):
                for inv in (False,True):
                    d=dense_forest(f.parents,a,inv)
                    for j in range(f.n):
                        x=[int(i==j) for i in range(f.n)]
                        assert f.apply(x,inv)==mv(d,x)
            # Independently assemble the full block action from dense Cayleys.
            c1=dense_forest(s.path1.parents,pow(32,-1,P))
            c2=dense_forest(s.path2.parents,pow(32,-1,P))
            b=dense_forest(s.tree.parents,2)
            bi=dense_forest(s.tree.parents,2,True)
            ie=pow(3,(P-1)//4,P)*pow(512,-1,P)%P
            for j in range(n):
                x=[int(i==j) for i in range(n)];u=mv(c1,mv(c2,x))
                ru=mv(b,u[n//2:])+mv(bi,u[:n//2])
                q=[(a+ie*z)%P for a,z in zip(u,ru)]
                assert s.apply(x)==q
        out.append({'n':n,'fresh_vectors_each_direction':3,'setup_field_ops':9*n+2*s.tree_size+6,
                    'forward_field_ops':forward,'inverse_field_ops':reverse,'passed':True})
    for bad in ([0,0],[-1,0],[0,2],[True,0]):
        try:validate_and_invert(bad)
        except ValueError:pass
        else:raise AssertionError('bad permutation accepted')
    return out


def covariance_checks():
    out=[]
    for n in (8,16,32,64,128):
        order=list(range(n));random.Random(20261009+n).shuffle(order)
        s=Mixer(order,p=P);cols=[]
        for j in range(n):cols.append(s.apply([int(i==j) for i in range(n)]))
        w=pow(3,(P-1)//n,P);nonzero=0
        for i in range(n):
            for j in range(n):
                nonzero+=(cols[(j+1)%n][i]-pow(w,i,P)*cols[j][i])%P!=0
                assert (pow(w,i*((j+1)%n),P)-pow(w,i,P)*pow(w,i*j,P))%P==0
        assert nonzero==n*n
        out.append({'n':n,'nonzero_stage_covariance_entries':nonzero,'fourier_defect_entries':0})
    return out


def exact_tree_formula():
    out=[]
    for depth in range(1,19):
        d=[Fraction(1)]
        for h in range(1,depth+1):d.append(1+8/d[-1])
        t=[1/d[depth]]
        for j in range(1,depth+1):t.append(2*t[-1]/d[depth-j])
        assert t[0]+4*t[1]==1
        assert t[-1]-2*t[-2]==0
        for j in range(1,depth):assert t[j]-2*t[j-1]+4*t[j+1]==0
        D=[1,1]
        for j in range(depth):D.append(D[-1]+8*D[-2])
        assert t[-1]==Fraction(2**depth,D[depth+1])
        leaf_norm=2**depth * 2*t[-1]
        assert leaf_norm==Fraction(2*4**depth,D[depth+1])
        out.append({'depth':depth,'root_leaf_amplitude':str(t[-1]),'leaf_l1':str(leaf_norm)})
    return out


def graph_edges(order):
    n=len(order);inverse=validate_and_invert(order)
    return list(zip(range(n-1),range(1,n)))+list(zip(inverse[:-1],inverse[1:]))


def exact_gap_certificates():
    source=json.loads((BASE/'extracted/phase12/phase11_spectral_witnesses.json').read_text())
    claimed={v['n']:v for v in json.loads((BASE/'extracted/phase12/phase11_spectral_certificates.json').read_text())}
    out=[]
    for key,witness in source.items():
        n=int(key);a=[[4-n*int(i==j) for j in range(n)] for i in range(n)]
        for i,j in graph_edges(witness['row_reordering_permutation']):
            a[i][i]+=4*n;a[j][j]+=4*n;a[i][j]-=4*n;a[j][i]-=4*n
        previous=1;minors=[]
        for k in range(n):
            pivot=a[k][k];assert pivot>0;minors.append(pivot)
            for i in range(k+1,n):
                for j in range(i,n):
                    value,remainder=divmod(pivot*a[i][j]-a[i][k]*a[k][j],previous)
                    assert remainder==0
                    a[i][j]=a[j][i]=value
            previous=pivot
        digest=hashlib.sha256(';'.join(map(str,minors)).encode()).hexdigest()
        assert digest==claimed[n]['pivot_sequence_sha256']
        out.append({'n':n,'all_leading_minors_positive':True,'pivot_hash_matches':True,
                    'pivot_sequence_sha256':digest})
    return out


def numerical_checks():
    out=[];rng=random.Random(915)
    for n in (16,32,64,128):
        order=list(range(n));rng.shuffle(order);s=Mixer(order)
        a=np.column_stack([s.apply([int(i==j) for i in range(n)]) for j in range(n)])
        err=float(np.linalg.norm(a.conj().T@a-np.eye(n),2));assert err<1e-12
        edges=graph_edges(order);worst=1
        for _ in range(32):
            I=set(rng.sample(range(n),n//2));J=set(range(n))-I
            E=sum((i in I)!=(j in I) for i,j in edges)
            k=(E+31)//32
            sv=np.linalg.svd(a[np.ix_(list(I),list(J))],compute_uv=False)
            assert sv[k-1]>=1/64-1e-12;worst=min(worst,float(sv[k-1]))
        # Audit the exact geometric resolvent identity independently on tree.
        m=n//2;adj=np.zeros((m,m))
        for i,p in enumerate(s.tree.parents):
            if p!=-1:adj[i,p]=adj[p,i]=1
        E=np.eye(m)-(np.eye(m)+4*adj@adj)/37
        assert np.linalg.norm(E,2)<=36/37+1e-12
        H=2/37*(np.eye(m)+2j*adj)
        exact=2*np.linalg.inv(np.eye(m)-2j*adj)-np.eye(m)
        accum=-np.eye(m,dtype=complex);power=np.eye(m)
        for k in range(605):
            accum+=H@power;power=power@E
        tail=float(np.linalg.norm(exact-accum,2))
        bound=(14/37)*(36/37)**605/(1-36/37)
        assert tail<=bound+1e-12
        out.append({'n':n,'unitarity_spectral_error':err,'random_cuts':32,
                    'minimum_required_cut_singular':worst,'tree_series_terms':605,
                    'tree_series_tail':tail,'theorem_tail_bound':bound})
    return out


def main():
    assert 4096*72**604 < 73**604
    assert Fraction(29**2)*(1+Fraction(29,512)) < 1024
    result={'uploaded_code_executed':False,'exact_executor':exact_checks(),
            'exact_covariance':covariance_checks(),'exact_tree_formula':exact_tree_formula(),
            'exact_gap_certificates':exact_gap_certificates(),'numerical':numerical_checks(),
            'gate_constants':{'z':73/72,'weighted_stage_bound':29**2*(1+29/512),
                              'tail_per_stage_604':1024*(72/73)**604,
                              'log_support_base':math.log(6144)+604*math.log(20)}}
    assert result['gate_constants']['tail_per_stage_604']<1/4
    (BASE/'independent_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':'passed','exact_lengths':len(result['exact_executor']),
                      'exact_graph_certificates':len(result['exact_gap_certificates']),
                      'numerical_lengths':len(result['numerical'])},indent=2))


if __name__=='__main__':main()
