"""Independent, deterministic Phase 26 finite-field / spectral controls."""
from __future__ import annotations
import json,random,math
from pathlib import Path
from phase26_cuts import *


def fft_reference(x:list[int])->list[int]:
    n=len(x);y=x.copy();j=0
    for i in range(1,n):
        b=n//2
        while j&b:j^=b;b//=2
        j^=b
        if i<j:y[i],y[j]=y[j],y[i]
    root=pow(3,(P-1)//n,P)
    length=2
    while length<=n:
        step=pow(root,n//length,P)
        for s in range(0,n,length):
            w=1
            for u in range(length//2):
                a=y[s+u];b=y[s+u+length//2]*w%P
                y[s+u]=(a+b)%P
                y[s+u+length//2]=(a-b)%P
                w=w*step%P
        length*=2
    return y  # Unnormalized DFT: both Weyl identities still hold


def z_apply(x):
    return x[-1:]+x[:-1]


def z_inverse(x):
    return x[1:]+x[:1]


def d_apply(x,omega):
    n=len(x);w=1;out=[0]*n
    for j in range(n):out[j]=w*x[j]%P;w=w*omega%P
    return out


def weyl_defects(executor,x):
    n=len(x);omega=pow(3,(P-1)//n,P)
    mx=executor(x)
    one=executor(z_apply(x));d=d_apply(mx,omega)
    two=executor(d_apply(x,omega));z=z_inverse(mx)
    return (sum(a!=b for a,b in zip(one,d)),sum(a!=b for a,b in zip(two,z)))


def run():
    rows=[]
    for n in (64,128,256,1024,4096,16384):
        strides=[2,n//2+2,n//2+6,1]
        orders=[two_run_zigzag(n,a) for a in strides[:3]]+[list(range(n))]
        k,score=optimal_phase_cut(n,strides)
        I,J=phase_partition(n,k)
        edges=[crossing_edges(o,I,J) for o in orders]
        assert k==2 and edges==[3,3,11,2]
        q=8  # two sums, 4 Green resolvents per stage
        cutrank=2*sum(edges)
        rows.append({'n':n,'strides':strides,'chosen_modular_character':k,
                     'one_stage_crossing_edges':edges,'two_stage_cut_rank_bound':cutrank,
                     'minimum_Fourier_any_balanced_rank':n//4,
                     'spectral_distance_lower_bound':round(error_floor(n,cutrank),10)
                     if cutrank<n//2 else 0.0})
        print('n',n,'common character',k,'rank cap',cutrank,
              'Fourier universal rank >=',n//4,flush=True)
    rng=random.Random(260027)
    n=256;orders=[two_run_zigzag(n,a) for a in (2,n//2+2,n//2+6)]+[list(range(n))]
    layers=[]
    for stage in range(2):
        terms=[]
        for order in orders:
            weights=[rng.randrange(1,P) for _ in range(n)]
            lg=[rng.randrange(1,P) for _ in range(n)]
            rg=[rng.randrange(1,P) for _ in range(n)]
            terms.append(WeightedTerm(order,weights,lg,rg))
        layers.append(Layer(terms,[rng.randrange(1,P) for _ in range(n)]))
    I,J=phase_partition(n,2)
    rank=mod_rank(cut_minor(layers,I,J))
    assert rank==38
    root=pow(3,(P-1)//n,P)
    fourier=[[pow(root,i*j%n,P) for j in J] for i in I]
    rank_F=mod_rank(fourier)
    assert rank_F==128
    rows.append({'n':n,'exact_two_stage_weighted_Green_rank':rank,
                 'exact_Fourier_quarter_minor_rank':rank_F,
                 'phase_field_modulus':P,
                 'outside_row_col_scalings_and_permutations':'cannot overcome general rank-64 threshold'})
    print('exact n=256 modular ranks: candidate',rank,'Fourier minor',rank_F,flush=True)
    escapes=[]
    for n in (128,256,512,1024):
        orders=[generic_cycle(n,1900+j+100*n) for j in range(2)]+[list(range(n))]
        charscore=[]
        for k in range(1,n):
            I,J=phase_partition(n,k)
            charscore.append(sum(crossing_edges(o,I,J) for o in orders))
        kbest=1+min(range(n-1),key=lambda i:charscore[i])
        rng1=random.Random(19100+n)
        stages=[]
        for order in orders[:2]:
            alpha=[rng1.randrange(1,P) for _ in range(n)]
            stages.append(Layer([WeightedTerm(order,alpha)],
                                diag=[rng1.randrange(1,P) for _ in range(n)]))
        x=[rng1.randrange(P) for _ in range(n)]
        reference=weyl_defects(fft_reference,x)
        candidate=weyl_defects(lambda v:circuit_apply(v,stages),x)
        assert reference==(0,0)
        assert all(v>0 for v in candidate)
        escapes.append({'n':n,'min_phase_cut_edges_random_two_cycles_plus_Z':min(charscore),
                        'best_phase_character':kbest,
                        'random_Green_product_Weyl_nonzero_coordinates':candidate,
                        'reference_FFT_Weyl_nonzero_coordinates':reference})
        print('random-order control n',n,'best phase cut edges',min(charscore),
              'Weyl defect coordinates',candidate,flush=True)
    out={'status':'PASS','phase':26,'finite_field_prime':P,
         'examples':rows,'non_affine_controls':escapes,
         'note':'Finite-field exact tests support restricted rank theorem; non-affine controls are samples only. No new sub-NlogN FFT.'}
    Path(__file__).with_name('audit.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':run()
