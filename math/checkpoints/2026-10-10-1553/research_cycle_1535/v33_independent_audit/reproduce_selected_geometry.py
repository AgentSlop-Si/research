"""Public input-only reproduction copy. Full-provenance control is audit_geometry.py.
Only manifest/ZIP provenance reads differ; no mathematics was changed.
Not executed or imported during preservation. Run in a writable copy.
"""
"""Independent v33 controls. Source programs are neither imported nor executed."""
from pathlib import Path
import hashlib, json, math, random

BASE=Path(__file__).resolve().parent
SRC=BASE/'source'/'fft_gain_gauge_fourier_v33'
top=json.loads((SRC/'topology_11.json').read_text())
weights=json.loads((SRC/'weights_11.json').read_text())
layers=weights['layers']; n=11; q=weights['field_prime']; z=weights['root']
assert q==1000000123 and all(q%d for d in range(2,math.isqrt(q)+1))
assert z!=1 and pow(z,11,q)==1
assert all(len(layer)==33 for layer in layers)
assert all([[i,j] for i,j,w in layer]==mask for layer,mask in zip(layers,top['layers']))
assert all(0<w<q for layer in layers for i,j,w in layer)
assert all(len({(i,j) for i,j,w in layer})==33 for layer in layers)
assert all(sum(i==v for i,j,w in layer)==3 and sum(j==v for i,j,w in layer)==3 for layer in layers for v in range(n))

def product(layers):
    current=[[int(i==j) for j in range(n)] for i in range(n)]
    for layer in layers:
        nxt=[[0]*n for _ in range(n)]
        for dst,src,w in layer:
            for j in range(n): nxt[dst][j]=(nxt[dst][j]+w*current[src][j])%q
        current=nxt
    return current

def elimination(a, determinant=False):
    a=[list(row) for row in a]; m=len(a); k=len(a[0]); rank=0; det=1
    for c in range(k):
        piv=next((r for r in range(rank,m) if a[r][c]%q),None)
        if piv is None: continue
        if piv!=rank: a[piv],a[rank]=a[rank],a[piv];det=-det
        value=a[rank][c]%q;det=det*value%q
        a[rank]=[v*pow(value,-1,q)%q for v in a[rank]]
        for r in range(rank+1,m):
            s=a[r][c]%q
            if s: a[r]=[(v-s*u)%q for v,u in zip(a[r],a[rank])]
        rank+=1
        if rank==m: break
    return (det%q if rank==m==k else 0) if determinant else rank

# Differentiate by independently propagating one dual-number tangent per edge.
# This works directly with the sparse evaluator, rather than the source's
# closed-form layer-specific derivative expressions.
def derivative(which):
    current=[[int(i==j) for j in range(n)] for i in range(n)]
    tangent=[[0]*n for _ in range(n)]; edge=0
    for layer in layers:
        nxt=[[0]*n for _ in range(n)]; dt=[[0]*n for _ in range(n)]
        for dst,src,w in layer:
            for j in range(n):
                nxt[dst][j]=(nxt[dst][j]+w*current[src][j])%q
                dt[dst][j]=(dt[dst][j]+w*tangent[src][j]+(current[src][j] if edge==which else 0))%q
            edge+=1
        current,tangent=nxt,dt
    return tangent

H=product(layers)
saved=list(map(int,(SRC/'transfer_11.txt').read_text().split()))
assert saved[:2]==[n,q] and saved[2:]==sum(H,[])
assert all(H[i][j] for i in range(n) for j in range(n))
dH=[derivative(e) for e in range(99)]
J=[]; Jrat=[]; Jres=[]; residual=[]
for i in range(1,n):
    for j in range(1,n):
        N=H[i][j]*H[0][0]%q;D=H[i][0]*H[0][j]%q;t=pow(z,i*j,q)
        residual.append((N-t*D)%q)
        row=[];rrow=[]
        for M in dH:
            dN=(M[i][j]*H[0][0]+H[i][j]*M[0][0])%q
            dD=(M[i][0]*H[0][j]+H[i][0]*M[0][j])%q
            row.append((D*dN-N*dD)%q)
            rrow.append((dN-t*dD)%q)
        J.append(row);Jrat.append([v*pow(D,-2,q)%q for v in row]);Jres.append(rrow)

edges=[(lev*n+src,(lev+1)*n+dst,w) for lev,layer in enumerate(layers) for dst,src,w in layer]
gauge=[[(int(v==dst)-int(v==src))*w%q for src,dst,w in edges] for v in range(44)]
gauge_products=[[sum(x*y for x,y in zip(row,g))%q for row in J] for g in gauge]
assert all(v==0 for a in gauge_products for v in a)
gauge_res_products=[[sum(x*y for x,y in zip(row,g))%q for row in Jres] for g in gauge]
cert=json.loads((SRC/'jacobian_certificate.json').read_text())
minor=[[J[r][c] for c in cert['pivot_columns']] for r in cert['pivot_rows']]
det=elimination(minor,True)
assert det==915710031==cert['minor_determinant_mod_q']
assert elimination(J)==56 and elimination(Jrat)==56 and elimination(gauge)==43

aff=json.loads((SRC/'affine_invariant_certificate.json').read_text())
evals=[]; all_sample_weights=[]
for seed in aff['evaluation_seeds']:
    rng=random.Random(seed)
    ls=[[(i,j,rng.randrange(1,q)) for i,j in mask] for mask in top['layers']]
    hh=product(ls)
    assert all(hh[i][0] and hh[0][i] for i in range(n))
    evals.append([1]+[hh[i][j]*hh[0][0]*pow(hh[i][0]*hh[0][j]%q,-1,q)%q for i in range(1,n) for j in range(1,n)])
    all_sample_weights.append([w for layer in ls for i,j,w in layer])
affdet=elimination(evals,True)
assert affdet==763214669==aff['determinant_mod_prime']

manifest=[]
for name,digest in {'topology_11.json': '4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a9a1ba59fd79a76a9b', 'weights_11.json': 'acee139d63218c72f0dc97f4dcf7ede67382ad1aa102d1e3d47195c752b69540', 'transfer_11.txt': 'ccface91887da90a75b57b64532b6af34f6f8a655e20f864a65b0bb20dd0d9c1', 'jacobian_certificate.json': 'd76647303e324d184602d11c223a62853cf2fd64e3033300eab38beb865dd7a1', 'affine_invariant_certificate.json': '216006dec70e0b84ffd48dc1d02386aba7bb0fc991bea246efabe4c48bf88407'}.items():
    got=hashlib.sha256((SRC/name).read_bytes()).hexdigest()
    assert got==digest
    manifest.append({'file':name,'sha256':got})

result={
 'original_source_zip_sha256_not_rechecked':'8daa679b23eadec2862fc8f3c4828a3bb87b469fb79536936436522fc5d04020',
 'manifest_files_verified':len(manifest),'field_prime_trial_division_verified':q,
 'root_order_verified':11,'edges':99,'layer_degrees_all_three':True,
 'transfer_matches_saved_121_entries':True,'fourier_residual_zero_count':residual.count(0),
 'first_fourier_residual':residual[0],
 'rational_crossratio_derivative_rank':elimination(Jrat),
 'denominator_squared_derivative_numerator_rank':elimination(J),
 'saved_jacobian_minor_determinant':det,
 'gauge_rank':elimination(gauge),'rational_derivative_gauge_annihilation':True,
 'target_residual_jacobian_rank_at_nontarget_point':elimination(Jres),
 'target_residual_gauge_image_rank_at_nontarget_point':elimination(gauge_res_products),
 'target_residual_gauge_vectors_annihilated':sum(all(v==0 for v in row) for row in gauge_res_products),
 'affine_evaluation_matrix_dimension':len(evals),'affine_evaluation_determinant':affdet,
 'source_programs_executed_or_imported':False,
}
(BASE/'geometry_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
(BASE/'manifest_receipt.json').write_text(json.dumps(manifest,indent=2)+'\n')
(BASE/'geometry_matrices.json').write_text(json.dumps({'H':H,'derivative_numerator':J,'rational_derivative':Jrat,'target_residual_derivative':Jres,'gauge':gauge,'residuals':residual,'affine_evaluation_matrix':evals,'affine_evaluation_weights':all_sample_weights}))
with (BASE/'independent_input.txt').open('w') as f:
    f.write(f'{n} {q}\n')
    for row in H:f.write(' '.join(map(str,row))+'\n')
    for layer in layers:
        f.write(f'{len(layer)}\n')
        for dst,src,w in layer:f.write(f'{dst} {src}\n')
print(json.dumps(result,indent=2))
