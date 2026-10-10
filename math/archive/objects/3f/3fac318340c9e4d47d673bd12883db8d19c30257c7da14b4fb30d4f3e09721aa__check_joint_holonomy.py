#!/usr/bin/env python3
"""Fresh exact finite-instance joint fiber holonomy controls."""
from pathlib import Path
import sys,json,itertools
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'four_character_decomposition'))
from check_four_character_identities import cover_and_splice,lift,build_walsh_route,LABELS,P
I=tuple(range(4))
def compose(a,b): return tuple(a[x] for x in b)
def inverse(a): return tuple(a.index(x) for x in I)
def chi(c,e): return (-1)**((c&e).bit_count()%2)
def closure(generators):
    group={I}; todo=[I]
    while todo:
        x=todo.pop()
        for g in generators:
            h=compose(g,x)
            if h not in group: group.add(h); todo.append(h)
    return group
def audit(routes,a,b):
    p,phis=routes[0]; n=a*b
    gauges=[None]*n; gauges[0]=I; vertex=0; tree=[]
    for _ in range(n-1):
        tree.append(vertex)
        gauges[p[vertex]]=compose(phis[vertex],gauges[vertex]);vertex=p[vertex]
    assert all(g is not None for g in gauges)
    generators=[]
    for j,(p,phis) in enumerate(routes):
        for v in range(n):
            g=compose(inverse(gauges[p[v]]),compose(phis[v],gauges[v]))
            generators.append((j,v,g))
    assert all(g==I for j,v,g in generators if j==0 and v in set(tree))
    group=closure(set(g for j,v,g in generators))
    witness=next(((j,v,g,k,w,h,compose(g,h),compose(h,g))
        for j,v,g in generators for k,w,h in generators if compose(g,h)!=compose(h,g)),None)
    # All checked instances share this fixed Walsh character in the tree gauge.
    fixed=[]
    for c in range(1,4):
        if all(all(chi(c,g[e])==chi(c,g[0])*chi(c,e) for e in I) for g in group): fixed.append(c)
    assert len(group)==8 and witness is not None and fixed==[1]
    rotations=[g for g in group if compose(compose(g,g),compose(g,g))==I and compose(g,g)!=I]
    assert len(rotations)==2
    r=rotations[0]
    reflection=next(g for g in group if g!=I and compose(g,g)==I and compose(compose(g,r),g)==inverse(r))
    assert closure([r,reflection])==group
    return {'N':n,'joint_group_order':len(group),'group_elements':sorted(group),
            'noncommuting_witness':{'edge_a':list(witness[:2]),'holonomy_a':witness[2],
                'edge_b':list(witness[3:5]),'holonomy_b':witness[5],'ab':witness[6],'ba':witness[7]},
            'dihedral_generators':[r,reflection],'fixed_nonzero_Walsh_characters':fixed,
            'common_scalar_four_channel_gauge_exists':False,
            'common_permutation_representation_blocks':[1,1,2]}

def checked_lift(ts,ps,a,b,label):
    tl,pl,rec=lift(ts,ps,a,b,label)
    assert rec['premerge_cycle_lengths']==[a*b]*4
    assert rec['merge_tails']==[0,b,2*a*b,2*a*b+b]
    _,_,phis,_=build_walsh_route(ps,pl,a,b)
    assert all(all(chi(1,g[e])==chi(1,g[0])*chi(1,e) for e in I) for g in phis)
    high_x_swap=(2,3,0,1)
    assert all(compose(g,high_x_swap)==compose(high_x_swap,g) for g in phis)
    assert all(pl[(i+2*a*b)%(4*a*b)]==(pl[i]+2*a*b)%(4*a*b) for i in range(4*a*b))
    # Sum the exact low-coordinate carries over the base grid.
    axis,c,sign=label
    if axis=='H':
        total=sum((x+sign*(2*y+c))//a for x in range(a) for y in range(b))
        assert total==sign*b*(b-1+c)
    else:
        total=sum((y+sign*(2*x+c))//b for x in range(a) for y in range(b))
        assert total==sign*a*(a-1+c)
    assert total%2==0
    # The complete large-cycle monodromy starting above base vertex zero is
    # exactly the same 4-cycle on literal high-bit sheet labels for every order.
    monodromy=I; vertex=0
    for _ in range(a*b):
        monodromy=compose(phis[vertex],monodromy); vertex=ps[vertex]
    assert vertex==0 and monodromy==(1,2,3,0)
    return tl,pl,phis

def mask_controls():
    count=0
    for a in itertools.product(range(2),repeat=4):
        m=[[sum(chi(c,e)*a[e]*chi(d,e) for e in I) for d in I] for c in I]
        fine=all(m[c][d]==0 for c in I for d in I if [0,1,2,2][c]!=[0,1,2,2][d])
        coarse=all(m[c][d]==0 for c in I for d in I if (c//2)!=(d//2))
        assert fine==(len(set(a))==1)
        assert coarse==(a[0]==a[2] and a[1]==a[3])
        count+=1
    return {'binary_masks_exhaustively_checked':count,'fine_block_preserving':'fiber-constant masks only',
            'coarse_2_plus_2_preserving':'a(0)=a(2) and a(1)=a(3)',
            'nonsingular_two_value_example':[1,2,1,2],'generic_mixing_example':[1,2,3,4]}

def bank_and_target_controls(a,b):
    n=a*b; root=pow(3,(P-1)//(4*n),P); blockroot=pow(root,2*a,P)
    def entry(i,j):
        x,y=divmod(i,2*b);xx,z=divmod(j,2*b)
        if x!=xx:return 0
        return pow(blockroot,y*z,P) if x%a<a//2 else int(y==z)
    for i in range(4*n):
        for j in range(4*n):
            assert entry(i,j)==entry((i+2*n)%(4*n),(j+2*n)%(4*n))
    assert pow(root,2*n*(2*n+1),P)==P-1 and pow(root,0,P)==1
    return {'N':n,'bank_simultaneous_shift_entries_checked':16*n*n,
            'Fourier_target_shift_counterexample':[1,P-1]}
def main():
    rebased=[]
    for a,b in [(2,2),(4,2),(4,4),(8,4),(8,8),(16,8),(16,16),(32,16)]:
        routes=[]
        for label in LABELS:
            ts,ps,_=cover_and_splice(a,b,label);_,pl,phis=checked_lift(ts,ps,a,b,label)
            routes.append((ps,phis))
        rec=audit(routes,a,b);rebased.append(rec);print('one-level',a*b,rec['joint_group_order'],flush=True)
    chains=[]
    for a,b in [(2,2),(4,2),(4,4)]:
        seed=a*b; current=[cover_and_splice(a,b,label)[:2] for label in LABELS]
        for level in range(3):
            routes=[];next_routes=[]
            for label,(ts,ps) in zip(LABELS,current):
                tl,pl,phis=checked_lift(ts,ps,a,b,label)
                routes.append((ps,phis));next_routes.append((tl,pl))
            rec=audit(routes,a,b);rec.update(seed_N=seed,level=level);chains.append(rec)
            print('chain',seed,level,a*b,rec['joint_group_order'],flush=True)
            a*=2;b*=2;current=next_routes
    cyclic=closure([(1,2,3,0)])
    assert len(cyclic)==4 and all(compose(g,h)==compose(h,g) for g in cyclic for h in cyclic)
    result={'status':'PASS','scope':'All-size D8 containment and common 1+1+2 route splitting; equality with D8 is checked on finite explicit instances, not claimed universally.',
            'one_level_instances':rebased,'hierarchical_chain_instances':chains,
            'positive_abelian_control_order':len(cyclic),'mask_controls':mask_controls(),
            'bank_symmetry_and_target_controls':[bank_and_target_controls(a,b) for a,b in [(2,2),(4,2),(4,4),(8,4),(8,8)]]}
    # Explicit b=1 boundary counterexample: horizontal c=1 on the 4-by-2
    # large grid has two cycles of length four, not four cycles of length two.
    boundary=[((x+2*y+1)%4)*2+y for x in range(4) for y in range(2)]
    seen=set();lengths=[]
    for v in range(8):
        if v in seen:continue
        w=v;length=0
        while w not in seen:seen.add(w);length+=1;w=boundary[w]
        assert w==v;lengths.append(length)
    assert lengths==[4,4]
    result['b_equals_one_boundary_control']={'a':2,'b':1,'c':1,'carry_sum':1,'premerge_cycle_lengths':lengths}
    (HERE/'JOINT_HOLONOMY_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
