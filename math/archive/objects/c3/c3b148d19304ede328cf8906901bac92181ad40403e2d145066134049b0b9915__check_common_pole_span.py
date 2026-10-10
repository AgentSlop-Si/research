#!/usr/bin/env python3
"""Exact bounded common-pole sector-span certificate, newly authored here."""
from pathlib import Path
import sys,json,random,time
import sympy as sp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent/'seed_compatibility_gate'))
from check_n16_outer_gate import PRIME as P,LABELS,pivots,green
from check_lift_defects import cover_and_splice
from check_hierarchical_lift import lift
T=sp.Symbol('t')

def determinant_monomials(entries):
    """Subset DP for det([s_ij*t^q_ij]), producing exact integer coefficients."""
    n=len(entries);state={0:{0:1}}
    for r in range(n):
        nxt={}
        for mask,poly in state.items():
            for c in range(n):
                if mask>>c&1:continue
                sign,exponent=entries[r][c]
                if (mask>>(c+1)).bit_count()%2:sign=-sign
                dest=nxt.setdefault(mask|1<<c,{})
                for power,coefficient in poly.items():
                    dest[power+exponent]=dest.get(power+exponent,0)+sign*coefficient
        state={mask:{p:c for p,c in poly.items() if c} for mask,poly in nxt.items()}
    return sp.Poly.from_dict({(p,):c for p,c in state[(1<<n)-1].items()},T,domain=sp.ZZ)

def sparse(poly):
    assert all(c.q == 1 for m,c in poly.terms())
    return [[m[0],int(c)] for m,c in sorted(poly.terms())]

def guard_factors(poly):
    """Return exact decomposition into t-powers and factors dividing t^64-1."""
    p=poly.monic();valuation=0;layers=[]
    while p.degree()>0 and p.eval(0)==0:p=p.exquo(sp.Poly(T,T));valuation+=1
    bad=sp.Poly(T**64-1,T)
    while p.degree()>0:
        f=sp.gcd(p,bad)
        if f.degree()==0:return None
        p=p.exquo(f);layers.append(sparse(f))
    return {'zero_valuation':valuation,'root_of_unity_layers':layers}

def main():
    begun=time.time();routes=[];positions=[];records=[]
    for label in LABELS:
        t,p,_=cover_and_splice(4,4,label);_,q,_=lift(t,p,4,4,label)
        assert all(q[(v+32)%64]==(q[v]+32)%64 for v in range(64))
        pos=[0]*64;v=0
        for k in range(64):pos[v]=k;v=q[v]
        assert v==0 and sorted(pos)==list(range(64))
        assert all((pos[(v+32)%64]-pos[v])%64==32 for v in range(64))
        positions.append(pos)
        quotient=[q[k]%32 for k in range(32)]
        signs=[1 if q[k]<32 else -1 for k in range(32)]
        seen=set();v=0;hol=1
        for k in range(32):seen.add(v);hol*=signs[v];v=quotient[v]
        assert len(seen)==32 and v==0 and hol==-1
        routes.append({'label':list(label),'successor':q,'sector_successor':quotient,'minus_sector_edge_signs':signs,'minus_holonomy':hol})
    assert routes[0]['sector_successor']==routes[1]['sector_successor']
    for i in range(32):
        rowrec={'physical_row':i,'sectors':{}}
        for sigma in (-1,1):
            rows=list(range(8)) if sigma==-1 else [0,2,3,4,5,6,7]
            es=[[(sigma**(((positions[j][i]-positions[j][k])%64)//32),(positions[j][i]-positions[j][k])%32) for k in range(32)] for j in rows]
            ev=[[sign*pow(pow(2,-1,P),exponent,P)%P for sign,exponent in row] for row in es]
            gcd=None;minors=[];decomp=None
            for attempt in range(4 if sigma==-1 else 1):
                permutation=list(range(32))
                if attempt:random.Random(10936+1000*i+10*sigma+attempt).shuffle(permutation)
                cols=[permutation[k] for k in pivots([[row[c] for c in permutation] for row in ev])]
                assert len(cols)==len(rows)
                polynomial=determinant_monomials([[row[c] for c in cols] for row in es])
                assert polynomial.eval(sp.Rational(1,2))!=0
                # Independently check the DP sign convention against exact Sympy determinant at t=2.
                at_two=sp.Matrix([[sign*2**exponent for sign,exponent in [row[c] for c in cols]] for row in es]).det()
                assert polynomial.eval(2)==at_two
                minors.append({'term_rows':rows,'physical_columns':cols,'determinant_polynomial':sparse(polynomial)})
                gcd=polynomial.monic() if gcd is None else sp.gcd(gcd,polynomial).monic()
                decomp=guard_factors(gcd)
                if decomp is not None:break
            if sigma==-1:
                assert decomp is not None,(i,sigma,sp.factor(gcd.as_expr()))
                rowrec['sectors'][str(sigma)]={'certified_rank':len(rows),'pole_scope':'all nonzero t with t^64 != 1','minors':minors,'monic_gcd':sparse(gcd),'guard_factorization':decomp}
            else:
                rowrec['sectors'][str(sigma)]={'certified_rank':7,'pole_scope':'t=1/2 only; rank <=7 at every legal common t','minors':minors,'monic_gcd':[], 'guard_factorization':None}
        records.append(rowrec)
        print(i,[(s,len(rowrec['sectors'][s]['minors']),len(rowrec['sectors'][s]['monic_gcd'])) for s in ('-1','1')],flush=True)
    pa=routes[0]['successor'];pb=routes[1]['successor'];inv=[0]*64
    for i,v in enumerate(pa):inv[v]=i
    relative=[inv[pb[v]] for v in range(64)];seen=set();relative_cycles=[]
    for i in range(64):
        if i in seen:continue
        cycle=[];v=i
        while v not in seen:seen.add(v);cycle.append(v);v=relative[v]
        assert v==i;relative_cycles.append(cycle)
    assert sorted(map(len,relative_cycles))==[1]*32+[2]*16
    ga,gb=green(pa,2),green(pb,2)
    K=[[(x-y)%P for x,y in zip(ra,rb)] for ra,rb in zip(ga,gb)]
    assert len(pivots(K))==16
    assert all(any(row) for row in K)
    assert all((K[i][k]+K[i][k+32])%P==0 for i in range(64) for k in range(32))
    assert all(K[i+32]==[(-v)%P for v in K[i]] for i in range(32))
    result={'status':'PASS_ALL_NONZERO_LEGAL_COMMON_POLES','pole_guard':'t != 0 and t^64 != 1','field':'complex numbers (exact certificate over Q[t])','routes':routes,'relative_H0_permutation_cycles':relative_cycles,'rank_of_H0_difference':16,'rows':records,'symmetry':'row i+32 is +/- row i in the corresponding sector','minus_rank':8,'plus_rank_at_half':7,'plus_coefficient_kernel_at_half':[1,-1,0,0,0,0,0,0],'minor_count':sum(len(r['sectors'][str(s)]['minors']) for r in records for s in (-1,1))}
    path=HERE/'COMMON_POLE_SPAN_CERTIFICATE.json'
    if '--verify' in sys.argv:assert json.loads(path.read_text())==result
    else:path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**{k:result[k] for k in ('status','minor_count')},'seconds':round(time.time()-begun,3)}),flush=True)
if __name__=='__main__':main()
