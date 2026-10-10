#!/usr/bin/env python3
"""Explicit N16-to-N64 model and exact necessary-gate controls; no search."""
from pathlib import Path
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'seed_compatibility_gate'))
from check_n16_outer_gate import cycles,green,PRIME,pivots,LABELS
from check_lift_defects import cover_and_splice,fiber
from check_hierarchical_lift import lift
P=PRIME
def commutator_x(a):
    n=len(a);half=n//2
    return [[(a[(i+half)%n][j]-a[i][(j+half)%n])%P for j in range(n)] for i in range(n)]
def rank(a):return len(pivots(a))
def main():
    ps=cycles(16);large=[];records=[]
    for label,p in zip(LABELS,ps):
        ts,pp,_=cover_and_splice(4,4,label);assert pp==p
        tl,pl,rec=lift(ts,p,4,4,label);large.append(pl);records.append(rec)
    gs=[green(p,j+2) for j,p in enumerate(large)]
    assert all(rank([g[i] for g in gs])==8 for i in range(64))
    assert all(not any(any(row) for row in commutator_x(g)) for g in gs)
    z=pow(3,(P-1)//64,P);assert pow(z,32,P)==P-1
    target=[[pow(z,i*j,P) for j in range(64)] for i in range(64)]
    bank=[[0]*64 for _ in range(64)];active=[0,1,4,5]
    for x in range(8):
        for y in range(8):
            for yy in range(8):bank[8*x+y][8*x+yy]=pow(z,8*y*yy,P) if x in active else int(y==yy)
    assert rank(commutator_x(target))==32
    assert not any(any(row) for row in commutator_x(bank))
    masks=[]
    for character in range(4):
        values=[0]*64
        for v in range(16):
            for e,j in enumerate(fiber(v,4,4)):values[j]=(-1)**((character&e).bit_count()%2)%P
        diagonal=[[int(i==j)*values[i] for j in range(64)] for i in range(64)]
        unequal=sum(values[j]!=values[j+32] for j in range(32))
        actual=rank(commutator_x(diagonal))
        assert actual==2*unequal==([0,0,64,64][character])
        masks.append({'character':character,'commutator_rank':actual,'high_x_unequal_pairs':unequal})
    model={'status':'EXPLICIT_SYSTEM_AND_CONTROLS_ONLY','small_N':16,'large_N':64,
           'small_cycle_successors':ps,'nested_large_cycle_successors':large,
           'labels':LABELS,'pole_denominators':list(range(2,10)),
           'small_active_blocks':[0,1],'large_active_blocks':active,
           'large_bank_block_size':8,'small_grid':[4,4],'large_grid':[8,8],
           'full_physical_unknowns':1536,'mean_anchored_unknowns':1152,
           'mean_anchor_layer_scales':[1,1,2],'large_complex_entry_equations':4096,
           'small_isolated_root_coordinates':256,'small_root_equations':256,
           'coupled_mean_anchored_unknowns':1408,'coupled_mean_anchored_equations':4352,
           'full_outer_elimination':{'inner_unknowns':1024,'outer_unknowns':512,'compatibility_equations':3584,'pivot_minors':64},
           'anchored_outer_elimination':{'inner_character_unknowns':768,'remaining_outer_mean_constraints':128,'compatibility_equations':3584},
           'target_field':'Q[u]/(u^32+1), embedding 0<arg(u)<pi/16; small z=u^4',
           'green_entry_formula':'If P_j^p(k)=i, G_j[i,k]=d_j^(64-p)/(d_j^64-1), 0<=p<64',
           'equation_formula':'(sum diag(A_2j)G_j)(sum diag(A_1j)G_j) B64 (sum diag(A_0j)G_j) - [u^(i*k)] = 0 entrywise',
           'anchor_formula':'A_lj(v,e)=gamma_l*a_small_lj(v)+sum_(c=1)^3 b_ljvc*(-1)^(c dot e)',
           'fixed_inverse_guards':[(j+2)**64-1 for j in range(8)],'physical_endpoint_guards':1536,
           'mask_character_controls':masks,'target_high_x_commutator_rank':32,
           'necessary_total_high_x_unequal_pairs_across_24_masks':16,
           'route_lift_records':records,
           'no_numerical_coefficient_search_performed':True}
    source=HERE/'DYADIC_AFFINE_CHART.json'
    if not source.exists():source=HERE.parent/'n16_existence_milestone/DYADIC_AFFINE_CHART.json'
    if source.exists():model['accepted_small_chart_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    (HERE/'N16_TO_N64_SYSTEM.json').write_text(json.dumps(model,indent=2)+'\n')
    print(json.dumps({'status':'PASS','large_entry_equations':4096,'full_parameters':1536,'mean_anchored_parameters':1152,'target_commutator_rank':32,'searched_candidates':0}),flush=True)
if __name__=='__main__':main()
