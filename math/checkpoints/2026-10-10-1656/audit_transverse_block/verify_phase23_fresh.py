"""Fresh bounded audit. Reads source JSON as data; never imports source programs."""
import hashlib, itertools, json, math
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'extracted/fft_hero0_phase23_coupled_dual_bridge_2026-10-10/fft_hero0_phase23_dual_bridge'
P = 65537
receipt = {'method': 'Fresh independently written checker; no supplied programs run or imported.'}
receipt['source_archive_sha256'] = hashlib.sha256((BASE/'source/fft_hero0_phase23_coupled_dual_bridge_2026-10-10.zip').read_bytes()).hexdigest()
manifest = json.loads((SOURCE/'SHA256SUMS.json').read_text())
receipt['source_manifest'] = {n: len((SOURCE/n).read_bytes())==v['bytes'] and hashlib.sha256((SOURCE/n).read_bytes()).hexdigest()==v['sha256'] for n,v in manifest.items()}
assert all(receipt['source_manifest'].values())
receipt['prime_check_65537'] = all(P%d for d in range(2,math.isqrt(P)+1))
receipt['generator_order_65537'] = pow(3,65536,P)==1 and pow(3,32768,P)!=1
assert receipt['prime_check_65537'] and receipt['generator_order_65537']

def eliminate(A,p):
    A = [[int(v)%p for v in row] for row in A]
    rank=0
    for col in range(len(A[0])):
        hit=next((r for r in range(rank,len(A)) if A[r][col]),None)
        if hit is None: continue
        A[rank],A[hit]=A[hit],A[rank]
        inv=pow(A[rank][col],-1,p)
        A[rank]=[(v*inv)%p for v in A[rank]]
        for r in range(rank+1,len(A)):
            scale=A[r][col]
            A[r]=[(x-scale*y)%p for x,y in zip(A[r],A[rank])]
        rank+=1
        if rank==len(A): break
    return rank

def determinant3(M):
    ans=0
    for perm in itertools.permutations(range(3)):
        inversions=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        ans+=(-1)**inversions*math.prod(int(M[i][perm[i]]) for i in range(3))
    return ans%P

modular=[]
expected={4:1024,8:8736,16:36857,32:17660}
for s in expected:
    n=s*s; z=pow(3,(P-1)//n,P); w=pow(z,s,P)
    M=[[pow(w,i*j,P) for j in (1,2,3)] for i in (1,2,3)]
    det=determinant3(M)
    assert det==expected[s]
    tested=[]
    for fixed in ((0,0),(1,s-1),(s-1,1)):
        for reverse in (False,True):
            x,b=fixed
            row_indices=([u*s+x for u in range(s) if u!=b] if reverse else [x*s+u for u in range(s) if u!=b])
            col_indices=([b*s+v for v in range(s) if v!=x] if reverse else [v*s+b for v in range(s) if v!=x])
            block=[[pow(z,i*j,P) for j in col_indices] for i in row_indices]
            r=eliminate(block,P)
            assert r==s-1
            tested.append({'fixed':fixed,'reverse':reverse,'rank':r})
    modular.append({'s':s,'root_order_verified':pow(z,n,P)==1 and pow(z,n//2,P)!=1,'minor3':det,'blocks':tested})
receipt['fresh_modular_checks']=modular

spectra=[]
for s in range(3,17):
    n=s*s; m=(s-1)//2
    idx=np.arange(n)
    F=np.exp(2j*np.pi*((idx[:,None]*idx[None,:])%n)/n)
    count=0; worst=0.; min_rank=s; min_mth=float('inf'); gram_err=0.
    for x in range(s):
        for b in range(s):
            for reverse in (False,True):
                rows=([u*s+x for u in range(s) if u!=b] if reverse else [x*s+u for u in range(s) if u!=b])
                cols=([b*s+v for v in range(s) if v!=x] if reverse else [v*s+b for v in range(s) if v!=x])
                block=F[np.ix_(rows,cols)]
                sv=np.linalg.svd(block,compute_uv=False)
                err=float(np.max(np.abs(sv-np.array([math.sqrt(s)]*(s-2)+[1.]))))
                worst=max(worst,err); assert err<1e-10
                imag_svs=np.linalg.svd(block.imag,compute_uv=False)
                rank=int(sum(imag_svs>1e-9)); min_rank=min(min_rank,rank)
                min_mth=min(min_mth,float(imag_svs[m-1]))
                assert rank>=m and imag_svs[m-1]>=math.sqrt(s/2-m)-1e-10
                if m>1: assert imag_svs[m-2]>=math.sqrt(s/2)-1e-10
                count+=1
            frequencies=[u if u!=b else s-u for u in range(1,m+1)]
            G=np.sin(2*np.pi*(np.asarray(frequencies)[:,None]*np.arange(s)[None,:]/s+x*b/s+np.asarray(frequencies)[:,None]*b/(s*s)))
            cut=np.delete(G,x,axis=1)
            target=(s/2)*np.eye(m)-np.outer(G[:,x],G[:,x])
            gram_err=max(gram_err,float(np.max(np.abs(cut@cut.T-target))))
    assert gram_err<1e-10
    spectra.append({'s':s,'blocks_both_orientations':count,'maximum_fourier_spectrum_error':worst,'minimum_imag_rank':min_rank,'m':m,'minimum_mth_imag_singular_value':min_mth,'maximum_selected_sine_gram_error':gram_err})
receipt['fresh_full_block_spectrum_and_sine_checks']=spectra

rng=np.random.default_rng(491031)
def make_rook(s,homogeneous=False):
    n=s*s; mats=[np.zeros((n,n),complex) for _ in range(4)]
    for k in range(4):
        horizontal=k in (0,2)
        prototype=rng.normal(size=(s,s))+1j*rng.normal(size=(s,s))
        for f in range(s):
            fiber=[u*s+f for u in range(s)] if horizontal else [f*s+u for u in range(s)]
            values=prototype if homogeneous and k in (1,2) else rng.normal(size=(s,s))+1j*rng.normal(size=(s,s))
            mats[k][np.ix_(fiber,fiber)]=values
    return mats

rook_checks=[]
for s in (4,8):
    n=s*s
    for homogeneous in (False,True):
        XH,XV,YH,YV=make_rook(s,homogeneous)
        T=(YH+YV)@(XH+XV)
        maxerror=0.; maxproduct=0; maxblockrank=0
        for x in range(s):
            for b in range(s):
                ys=[i for i in range(s) if i!=b]; aa=[i for i in range(s) if i!=x]
                rows=[x*s+y for y in ys]; cols=[a*s+b for a in aa]
                A=np.array([[YH[x*s+y,a*s+y] for a in aa] for y in ys])
                B=np.array([[XV[a*s+y,a*s+b] for a in aa] for y in ys])
                u=YV[rows,x*s+b]; v=XH[x*s+b,cols]
                residual=T[np.ix_(rows,cols)]-np.outer(u,v)-A*B
                maxerror=max(maxerror,float(np.max(np.abs(residual))))
                product=int(np.linalg.matrix_rank(A)*np.linalg.matrix_rank(B))
                rank=int(np.linalg.matrix_rank(T[np.ix_(rows,cols)]))
                assert rank<=1+product
                maxproduct=max(maxproduct,product); maxblockrank=max(maxblockrank,rank)
        assert maxerror<1e-10
        if homogeneous: assert maxproduct==1 and maxblockrank<=2
        rook_checks.append({'s':s,'homogeneous_crossed_pair':homogeneous,'max_two_path_residual':maxerror,'maximum_transverse_rank_product':maxproduct,'maximum_offrook_block_rank':maxblockrank})
receipt['fresh_rook_product_checks']=rook_checks

green=[]
for s in (4,8,16):
    n=s*s; mats=[np.zeros((n,n),complex) for _ in range(4)]
    cyclic=np.roll(np.eye(s),1,axis=0)
    for k in range(4):
        for f in range(s):
            weight=[.14+.21j,.20+.19j,.16+.25j,.12+.17j][k]
            if k in (0,3): weight+=(f/(2*s))*(.13+.11j)
            G=np.linalg.solve(np.eye(s)-weight*cyclic,np.eye(s))
            fiber=[u*s+f for u in range(s)] if k in (0,2) else [f*s+u for u in range(s)]
            mats[k][np.ix_(fiber,fiber)]=G
    T=(mats[2]+mats[3])@(mats[0]+mats[1])
    ii=np.arange(n); F=np.exp(2j*np.pi*((ii[:,None]*ii[None,:])%n)/n)
    measured=float(np.linalg.norm(F-T,'fro')/n)
    floor=math.sqrt(1-4/s+1/(s*s))
    assert measured>=floor
    green.append({'s':s,'full_complex_green_relative_error':measured,'proved_floor':floor,'normalization_F_frobenius':float(np.linalg.norm(F,'fro'))})
receipt['fresh_green_controls']=green
receipt['phase_budgets']={str(s):math.ceil(s*s*max((s-1)//2-2,0)/(s-1)) for s in (4,8,16,32,64)}
receipt['status']='PASS'
(BASE/'phase23_fresh_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','source_archive_sha256':receipt['source_archive_sha256'],'manifest_entries_verified':len(manifest),'prime':P,'minor3_determinants':expected,'both_orientation_spectrum_blocks':sum(v['blocks_both_orientations'] for v in spectra),'phase_budgets':receipt['phase_budgets'],'receipt':str(BASE/'phase23_fresh_receipt.json')},indent=2))
