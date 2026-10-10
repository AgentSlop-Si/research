#!/usr/bin/env python3
"""Independent finite permutation and exact-rational audit of the common D8 gate."""
import itertools,json,random
from fractions import Fraction
from pathlib import Path
BASE=Path(__file__).parent
LABELS=[(axis,c,s) for axis in ('H','V') for c in (0,1) for s in (-1,1)]
ID=tuple(range(4));ROT=(1,2,3,0);SWAPX=(2,3,0,1)
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(p):
    out=[0]*len(p)
    for i,j in enumerate(p):out[j]=i
    return tuple(out)
def cycles(p):
    seen=set();out=[]
    for v in range(len(p)):
        if v in seen:continue
        c=[];w=v
        while w not in seen:seen.add(w);c.append(w);w=p[w]
        assert w==v;out.append(c)
    return out

def closure(gens):
    group={ID};todo=[ID]
    while todo:
        p=todo.pop()
        for g in gens:
            q=compose(g,p)
            if q not in group:group.add(q);todo.append(q)
    return group
D8={p for p in itertools.permutations(range(4)) if {frozenset((p[0],p[2])),frozenset((p[1],p[3]))}=={frozenset((0,2)),frozenset((1,3))}}
assert len(D8)==8

def dimensions(n):
    k=n.bit_length()-1;assert n==1<<k
    b=1<<(k//2);a=n//b;return a,b

def cover(a,b,label):
    axis,c,s=label
    return [((x+s*(2*y+c))%a)*b+y if axis=='H' else x*b+(y+s*(2*x+c))%b for x in range(a) for y in range(b)]
def splice(p,tails):
    q=p[:]
    for j,t in enumerate(tails):q[t]=p[tails[(j+1)%len(tails)]]
    return q

def init(a,b):return [splice(p,[min(c) for c in cycles(p)]) for p in (cover(a,b,label) for label in LABELS)]
def physical(a,b,v,e):
    x,y=divmod(v,b);return (x+a*(e//2))*2*b+y+b*(e%2)
def sheet(a,b,v):
    x,y=divmod(v,2*b);return 2*(x//a)+y//b

def make_lift(a,b,small,label,require_even=True):
    n=a*b;ts=cover(a,b,label);tl=cover(2*a,2*b,label);eta=[0]*n
    for v in range(n):eta[ts[v]]=small[v]
    pre=[]
    for v in tl:
        x,y=divmod(v,2*b);xx,yy=divmod(eta[(x%a)*b+y%b],b)
        pre.append((xx+a*(x//a))*2*b+yy+b*(y//b))
    proj=lambda v:((v//(2*b))%a)*b+(v%(2*b))%b
    assert all(proj(pre[v])==small[proj(v)] for v in range(4*n))
    maps=[tuple(sheet(a,b,pre[physical(a,b,v,e)]) for e in range(4)) for v in range(n)]
    axis,c,sgn=label;total=0
    for x in range(a):
        for y in range(b):
            carry=(x+sgn*(2*y+c))//a if axis=='H' else (y+sgn*(2*x+c))//b
            total+=carry
            expected=tuple(2*((e//2+carry+(2*b//a)*(e%2))%2)+e%2 if axis=='H' else 2*(e//2)+(e%2+carry)%2 for e in range(4))
            assert maps[b*x+y]==expected and maps[b*x+y] in D8
    assert total==sgn*(b*(b-1+c) if axis=='H' else a*(a-1+c))
    monodromy=ID
    for v in cycles(small)[0]:monodromy=compose(maps[v],monodromy)
    cc=cycles(pre)
    if require_even:
        assert monodromy==ID and len(cc)==4 and all(len(c)==n for c in cc)
        tails=sorted(next(v for v in c if proj(v)==0) for c in cc)
        assert tails==[physical(a,b,0,e) for e in range(4)]
    else:tails=sorted(min(v for v in c if proj(v)==0) for c in cc)
    lifted=splice(pre,tails);assert len(cycles(lifted))==1
    post=[tuple(sheet(a,b,lifted[physical(a,b,v,e)]) for e in range(4)) for v in range(n)]
    final=ID
    for v in cycles(small)[0]:final=compose(post[v],final)
    if require_even:assert final==ROT and post[0]==compose(maps[0],ROT)
    if require_even:
        assert all(p in D8 and compose(p,SWAPX)==compose(SWAPX,p) for p in post)
        assert all(lifted[(v+2*n)%(4*n)]==(lifted[v]+2*n)%(4*n) for v in range(4*n))
    return lifted,post,{'carry_sum':total,'premerge_monodromy':monodromy,'premerge_cycle_lengths':list(map(len,cc)),'postmerge_monodromy':final,'all_postmerge_maps_in_D8':all(p in D8 for p in post)}

def bank_holonomy(a,b,small,expected=None):
    large=[];edge=[];route_records=[]
    for p,label in zip(small,LABELS):
        q,maps,rec=make_lift(a,b,p,label);large.append(q);edge.append(maps);route_records.append(rec)
    n=a*b;transport=[None]*n;transport[0]=ID
    for v in cycles(small[0])[0][:-1]:transport[small[0][v]]=compose(edge[0][v],transport[v])
    assert all(t is not None for t in transport)
    hol={}
    for j in range(8):
        for v in range(n):hol[(j,v)]=compose(inverse(transport[small[j][v]]),compose(edge[j][v],transport[v]))
    group=closure(set(hol.values()));assert group==D8
    if expected:
        assert sorted(group)==sorted(tuple(g) for g in expected['group_elements'])
        w=expected['noncommuting_witness'];ga=hol[tuple(w['edge_a'])];gb=hol[tuple(w['edge_b'])]
        assert list(ga)==w['holonomy_a'] and list(gb)==w['holonomy_b']
        assert list(compose(ga,gb))==w['ab'] and list(compose(gb,ga))==w['ba'] and compose(ga,gb)!=compose(gb,ga)
    witnesses=next((g,h) for g in sorted(set(hol.values())) for h in sorted(set(hol.values())) if compose(g,h)!=compose(h,g))
    return large,{'N':n,'group_order':len(group),'group_elements':sorted(group),'noncommuting_pair':witnesses,'eight_route_controls':route_records}

def finite_instances():
    source=json.loads((BASE/'sources/JOINT_HOLONOMY_CONTROLS.json').read_text());out=[]
    for record in source['one_level_instances']:
        a,b=dimensions(record['N']);_,result=bank_holonomy(a,b,init(a,b),record);out.append(result)
    for seed in (4,8,16):
        a,b=dimensions(seed);small=init(a,b)
        for level in range(3):
            expected=next(r for r in source['hierarchical_chain_instances'] if r['seed_N']==seed and r['level']==level)
            small,result=bank_holonomy(a,b,small,expected);result.update({'seed_N':seed,'level':level});out.append(result);a,b=2*a,2*b
    assert len(out)==17
    extra=[];rng=random.Random(850034)
    for b in (2,4,6,10):
        for a in (b,2*b):
            for label in LABELS:
                order=rng.sample(range(a*b),a*b);small=[0]*(a*b)
                for j,v in enumerate(order):small[v]=order[(j+1)%len(order)]
                _,_,rec=make_lift(a,b,small,label);extra.append({'a':a,'b':b,'label':label,**rec})
    _,_,odd=make_lift(2,1,[1,0],('H',1,1),False);assert odd['premerge_monodromy']==SWAPX and odd['premerge_cycle_lengths']==[4,4]
    assert closure([ROT])=={ID,ROT,compose(ROT,ROT),inverse(ROT)}
    return {'source_instances':out,'arbitrary_small_order_even_grid_controls':extra,'b_one_boundary':odd,'positive_cyclic_group_order':len(closure([ROT]))}

def masks_and_banks():
    W=[[(-1)**((c&e).bit_count()%2) for e in range(4)] for c in range(4)];groups=[0,1,2,2];out=[]
    for mask in itertools.product((0,1),repeat=4):
        mat=[[Fraction(sum(W[c][e]*mask[e]*W[d][e] for e in range(4)),4) for d in range(4)] for c in range(4)]
        fine=all(not mat[c][d] for c in range(4) for d in range(4) if groups[c]!=groups[d])
        coarse=all(not mat[c][d] for c in range(4) for d in range(4) if (c//2)!=(d//2))
        assert fine==(len(set(mask))==1);assert coarse==(mask[0]==mask[2] and mask[1]==mask[3])
        out.append({'mask':mask,'preserves_1_1_2':fine,'preserves_2_2':coarse})
    p=998244353;banks=[]
    for n in (4,8,16,32,64):
        a,b=dimensions(n);length=4*n;w=pow(3,(p-1)//length,p);rho=pow(3,(p-1)//(2*b),p)
        active=set(range(a//2))
        def entry(i,j):
            x,y=divmod(i,2*b);xx,z=divmod(j,2*b)
            if x!=xx:return 0
            return pow(rho,y*z,p) if x%a in active else int(y==z)
        assert all(entry(i,j)==entry((i+2*n)%length,(j+2*n)%length) for i in range(length) for j in range(length))
        assert pow(w,0,p)==1 and pow(w,2*n*(2*n+1),p)==p-1
        banks.append({'small_N':n,'entries':length*length,'Fourier_counterexample':[1,p-1]})
    # The independently certified N16 seed bank is not this pulled-back bank.
    def seed_bank(i,j):
        if i//4!=j//4:return 0
        return pow(pow(3,(p-1)//4,p),(i%4)*(j%4),p) if i//4<2 else int(i==j)
    assert seed_bank(0,1)==1 and seed_bank(8,9)==0
    return {'binary_mask_controls':out,'pulled_back_bank_controls':banks,'N16_seed_bank_high_x_commutation_counterexample':[1,0]}

if __name__=='__main__':
    result={'status':'PASS','finite_holonomy':finite_instances(),'mask_and_bank':masks_and_banks(),'scope':'All-size D8 containment and mask/symmetry proof; joint D8 equality only for the enumerated instances'}
    (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS: 17 complete source holonomy instances, 64 arbitrary-order even-grid lifts, all mask and bank controls')
