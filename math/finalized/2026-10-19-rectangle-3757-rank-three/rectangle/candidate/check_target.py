#!/usr/bin/env python3
"""Exact target controls. No historical checker imports; no finite-field ranks."""
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
from math import gcd, prod, comb
import hashlib, json, time

ROOT=Path(__file__).resolve().parent
N=3757

def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def require(condition, message):
    if not condition:
        raise AssertionError(message)

# A determinant at a prime-order root is an integer coefficient vector of
# degree below ell. It vanishes iff the vector is constant, because the
# characteristic-zero minimal polynomial is 1+X+...+X^(ell-1).
def prime_det_vector(rows, cols, ell):
    k=len(rows)
    result=[0]*ell
    for sigma, sign in PERMS[k]:
        exponent=sum(rows[i]*cols[sigma[i]] for i in range(k))%ell
        result[exponent]+=sign
    return result

PERMS={}
for k in range(1,5):
    PERMS[k]=[(sigma, (-1)**sum(sigma[i]>sigma[j] for i in range(k) for j in range(i+1,k)))
              for sigma in permutations(range(k))]

def compositions(n,k):
    if k==1:
        yield (n,)
    else:
        for first in range(1,n-k+2):
            for tail in compositions(n-first,k-1):
                yield (first,)+tail

def main():
    start=time.perf_counter()
    cert={"N":N,"model":"complex cyclic Fourier, arbitrary nonempty Cartesian subsets", "logical_scope":"Finite checks supplement the parameter-complete proof; they do not enumerate all subsets."}
    stats={}
    # Source identity checks; snapshots are data, never executable inputs.
    sources=json.loads((ROOT/'SOURCE_PINS.json').read_text())
    for item in sources['sources']:
        data=(ROOT/item['snapshot']).read_bytes()
        require(len(data)==item['bytes'],'source length')
        require(hashlib.sha256(data).hexdigest()==item['sha256'],'source sha256')
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob'],'source Git blob')
    stats['source_snapshot_checks']=len(sources['sources'])

    # Every residue set occurring in the universal-minor Schur quotient.
    schur=[]
    for ell in (13,17):
        for k in range(1,5):
            denominator=prod(j-i for i in range(k) for j in range(i+1,k))
            require(gcd(denominator,ell)==1,'denominator invertible')
            frequencies={}
            for rows in combinations(range(ell),k):
                numerator=prod(rows[j]-rows[i] for i in range(k) for j in range(i+1,k))
                value=(numerator*pow(denominator,-1,ell))%ell
                require(value!=0,'Schur quotient is a unit')
                frequencies[value]=frequencies.get(value,0)+1
            require(sum(frequencies.values())==comb(ell,k),'complete row residue sets')
            schur.append({'prime':ell,'minor_size':k,'row_sets':comb(ell,k),'nonzero_quotient_residue_counts':frequencies})
    cert['schur_quotient_complete_residue_cases']=schur
    stats['schur_quotient_row_sets']=sum(x['row_sets'] for x in schur)

    # All concrete prime17 scalar matrices used in supported separation.
    # These are characteristic-zero cyclotomic determinant reductions.
    inversion=[]
    h=hashlib.sha256()
    for k in range(1,4):
        sets=list(combinations(range(17),k))
        count=0
        for rows in sets:
            for cols in sets:
                vec=prime_det_vector(rows,cols,17)
                require(any(v!=vec[0] for v in vec[1:]),'prime17 determinant nonzero')
                # Hash signed reduced coefficients, retaining a reproducible whole-set digest.
                reduced=[v-vec[-1] for v in vec[:-1]]
                h.update(bytes(v+128 for v in reduced))
                count+=1
        require(count==comb(17,k)**2,'complete inversion matrices')
        inversion.append({'s':k,'row_sets':len(sets),'column_sets':len(sets),'matrices':count})
    cert['prime17_inversion_complete_cases']=inversion
    cert['prime17_reduced_determinants_sha256']=h.hexdigest()
    stats['characteristic_zero_prime17_determinants']=sum(x['matrices'] for x in inversion)

    # Complete semiprime rank-one difference cases and their exact row capacity.
    differences=[]
    for delta in range(1,221):
        actual=sum((delta*a)%221==0 for a in range(221))
        require(actual==gcd(delta,221)<=17,'rank-one kernel size')
        differences.append({'delta':delta,'kernel_size':actual})
    cert['rank_one_semiprime_differences']=differences
    stats['semiprime_nonzero_differences']=len(differences)
    require(sum((0*a)%221==0 for a in range(221))==221,'one-column negative control')

    # Complete support partitions used for k<=4, including all simultaneous-zero counts.
    supports=[]
    for kp in range(1,5):
        for t in range(1,kp+1):
            for sizes in compositions(kp,t):
                for z0 in range(min(sizes)):
                    bound=17*z0+(13-z0)*(t-1)
                    require(bound<=17*(kp-1),'short-support bound')
                    supports.append({'nonzero_terms':kp,'frequency_groups':list(sizes),'simultaneous_zeros':z0,'zero_bound':bound})
    cert['short_support_complete_integer_parameters']=supports
    stats['short_support_parameter_cases']=len(supports)

    # Occupancy reduction is proved for all s,t>3 symbolically. All remaining
    # nine occupancy pairs and their exhaustive extremal capacities appear here.
    occupancy=[]
    for s,t in product(range(1,4), repeat=2):
        m=13*t
        if s==1:
            case={'s':s,'t':t,'branch':'one row residue','four_fibers_if_b_at_least':52,'four_rank_if_a_at_least':52}
        elif s==2:
            cap=2*17+(m-2)
            require(cap<=71<79,'two-rich-fiber capacity')
            case={'s':s,'t':t,'branch':'two row residues','max_fibers':m,'max_b_if_at_most_two_rich':cap,'forced_rich_fibers':3}
        else:
            cap=2*m
            require(cap<=78<79,'no-triple capacity')
            case={'s':s,'t':t,'branch':'three row residues','max_fibers':m,'max_b_without_triple':cap,'forced_triple_fiber':True}
        occupancy.append(case)
    cert['all_remaining_occupancy_pairs']=occupancy
    stats['occupancy_pairs']=len(occupancy)

    # Exhaust all nonzero supported-rank budgets and all compatible class sizes.
    budgets=[]
    row_size_cases=0
    max_sum=0
    for rho1,rho2 in product(range(1,4),repeat=2):
        if rho1+rho2>3:
            continue
        caps=[17 if r==1 else 34 for r in (rho1,rho2)]
        require(1 in (rho1,rho2),'rank-one forced')
        for a1 in range(1,caps[0]+1):
            for a2 in range(1,caps[1]+1):
                row_size_cases+=1
                max_sum=max(max_sum,a1+a2)
                require(a1+a2<=51,'rank budget forces a<=51')
        budgets.append({'ranks':[rho1,rho2],'row_capacity_bounds':caps,'max_total_rows':sum(caps)})
    cert['all_supported_rank_budgets']=budgets
    stats['compatible_two_block_row_sizes']=row_size_cases
    require(max_sum==51,'sharp two-block integer capacity')

    divisors=[d for d in range(1,N+1) if N%d==0]
    require(divisors==[1,13,17,221,289,3757],'all target divisors')
    ann=[]
    for d in divisors:
        case={'d':d,'row_bound':3*d,'column_bound':N//d}
        if 3*d>=52:
            require(N//d<=17,'three-projective-class contradiction')
        ann.append(case)
    cert['all_projective_annihilator_cases']=ann

    dangerous=[]
    for a in range(3,103):
        for b in range(a,min(N,3*N//a)+1):
            if 3*N*(a+b)<=238*a*b:
                require(a>51 and b>78,'structural exclusion of all dangerous shapes')
                dangerous.append({'a':a,'b':b,'area':a*b,'relation':'equality' if 3*N*(a+b)==238*a*b else 'strictly_below','excluded_by':'a>51 and b>78'})
    require(len(dangerous)==750,'inherited dangerous count')
    equality=[(x['a'],x['b']) for x in dangerous if x['relation']=='equality']
    require(equality==[(68,156)],'all scalar target equalities')
    save('DANGEROUS_SHAPES.json',dangerous)
    cert['dangerous_shape_summary']={'count':len(dangerous),'a_range':[min(x['a'] for x in dangerous),max(x['a'] for x in dangerous)],'b_range':[min(x['b'] for x in dangerous),max(x['b'] for x in dangerous)],'equality':equality,'none_are_asserted_Fourier_rectangles':True}
    stats['dangerous_shapes_excluded']=len(dangerous)

    minimum=None
    minimizers=[]
    scalar_count=0
    for a in range(3,N+1):
        for b in range(a,min(N,3*N//a)+1):
            if not (a<=51 or b<=78):
                continue
            value=Fraction(3*(a+b),a*b)
            require(value>=Fraction(16,221),'complete relaxed scalar density')
            scalar_count+=1
            if minimum is None or value<minimum:
                minimum=value; minimizers=[(a,b)]
            elif value==minimum:
                minimizers.append((a,b))
    require(minimum==Fraction(16,221) and minimizers==[(51,221)],'sharp scalar floor')
    cert['complete_dichotomy_stable_rank_shapes']={'count':scalar_count,'minimum':str(minimum),'minimizers':minimizers}
    stats['dichotomy_scalar_shapes']=scalar_count

    # Legal local rank-three extremizer: duplicated rows reduce exactly to
    # three distinct order221 characters. A 3x3 Vandermonde certifies rank3.
    R=[offset+221*i for offset in range(3) for i in range(17)]
    C=[17*j for j in range(221)]
    require(len(set(R))==51 and len(set(C))==221,'actual local sides')
    for offset in range(3):
        for i in range(17):
            for c in C:
                require(((offset+221*i)*c-offset*c)%N==0,'three duplicate row classes')
    exponents=sorted({j%221 for j in range(3)})
    require(len(exponents)==3,'Vandermonde nodes distinct')
    require(Fraction(3*(51+221),51*221)==minimum,'rank-three attainment density')
    cert['local_rank_three_attainment']={'rows':R,'columns':C,'rank_upper':'three repeated row classes','rank_lower':'rows0,1,2 and columns0,17,34 give an ordinary Vandermonde on three distinct order221 roots','density':str(minimum),'strict_cutoff_negative_control':True}
    stats['local_extremizer_entry_identities']=len(R)*len(C)

    D=min(d+N//d for d in divisors)
    E2=min(2*d+N//d for d in divisors if d<N)
    require(D==238 and E2==255,'baseline and rank-two density')
    require({tuple(sorted((d,N//d))) for d in divisors if d+N//d==D}=={(17,221)},'unique unordered equality sides')
    require(16*N>245**2 and min(E2,272)>245,'common strict higher-rank margin')
    require(N*D==894166,'target cost')
    cert['cost_and_equality']={'D':D,'E2':E2,'rank_three_numerator':272,'rank_ge_four_numerator_strict_lower':245,'rank_ge_four_square_check':[16*N,245**2],'common_nonsharp_area_penalty':'7/3757','optimal_cost':N*D,'rank_one_unordered_equality_sides':[17,221],'tile_count':N}

    # Full partition proof via unique row and column coset coordinates. This
    # checks every coordinate and every displacement product, then multiplies
    # their independent partitions; no sampled-entry claim is used.
    seen_r=[0]*N
    seen_c=[0]*N
    for x in range(221):
        for i in range(17): seen_r[x+221*i]+=1
    for y in range(17):
        for j in range(221): seen_c[y+17*j]+=1
    require(set(seen_r)=={1} and set(seen_c)=={1},'full coordinate partitions')
    for i in range(17):
        for j in range(221): require((221*i*17*j)%N==0,'all subgroup difference products')
    cert['complete_partition_certificate']={'row_cosets':221,'column_cosets':17,'row_and_column_coordinate_counts':[N,N],'all_coordinates_have_multiplicity_one':True,'difference_products_checked':N,'covered_entries_by_cartesian_product':N*N,'tile_cost':238,'total_cost':N*238}
    stats['partition_coordinate_checks']=2*N
    stats['partition_difference_products']=N

    cert['negative_controls']=[{'removed_condition':'at least two distinct semiprime columns','counterexample':'all221 rows and one column have rank1','row_count':221},{'weakened_condition':'a>=51 instead of a>51','counterexample':'the retained legal51-by-221 rank-three rectangle'}]
    stats['negative_controls']=2
    cert['status']='PASS'
    save('COVERAGE_CERTIFICATE.json',cert)
    stats['status']='PASS'
    stats['elapsed_seconds']=round(time.perf_counter()-start,6)
    stats['all_complex_rank_proofs']='Sections2--4 of REPORT.md; finite controls are supporting checks'
    save('RESULTS.json',stats)
    print(json.dumps(stats,indent=2,sort_keys=True))

if __name__=='__main__': main()
