"""Controls for independently written v33 audit, not supplied source programs."""
import json, math, random, subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
Q=1000000123; N=11
M=json.loads((BASE/'geometry_matrices.json').read_text());H=M['H']

def det(A):
    A=[r[:] for r in A];result=1
    for c in range(len(A)):
        r=next((r for r in range(c,len(A)) if A[r][c]%Q),None)
        if r is None:return 0
        if r!=c:A[c],A[r]=A[r],A[c];result=-result
        x=A[c][c]%Q;result=result*x%Q;iv=pow(x,-1,Q)
        for r in range(c+1,len(A)):
            y=A[r][c]*iv%Q
            for j in range(c,len(A)):A[r][j]=(A[r][j]-y*A[c][j])%Q
    return result%Q

finite=json.loads((BASE/'finite_receipt.json').read_text())
assert sum(finite['all_minors_count_by_order'])==math.comb(22,11)-1==705431
assert sum(finite['routing_terminal_pairs_by_size'])==705431
assert all(x==0 for x in finite['zero_minors_by_order']+finite['failed_routing_pairs_by_size'])
assert det(H)==finite['full_determinant']
rng=random.Random(731121)
for k in range(1,12):
    for _ in range(30):
        rows=sorted(rng.sample(range(N),k));cols=sorted(rng.sample(range(N),k))
        assert det([[H[i][j] for j in cols] for i in rows])

original=(BASE/'independent_input.txt').read_text().splitlines()
def run(lines):
    return json.loads(subprocess.run([str(BASE/'audit_finite')],input='\n'.join(lines)+'\n',capture_output=True,text=True,check=True).stdout)
duplicate=original[:];duplicate[2]=duplicate[1]
d=run(duplicate)
assert d['full_determinant']==0 and sum(d['zero_minors_by_order'])>0
identity=original[:]
for i in range(N):identity[1+i]=' '.join(str(int(i==j)) for j in range(N))
t=run(identity)
assert t['full_determinant']==1
assert t['zero_minors_by_order']==[math.comb(N,k)**2-math.comb(N,k) for k in range(1,N+1)]
broken=original[:];pos=N+1
for lev in range(3):
    count=int(broken[pos]);pos+=1
    if lev==0:
        for e in range(count):
            dst,src=map(int,broken[pos+e].split())
            if src==0:broken[pos+e]=f'{dst} 1'
    pos+=count
b=run(broken)
assert sum(b['failed_routing_pairs_by_size'])>0 and b['failed_routing_pairs_by_size'][0]>=N

z=414936531
F=[[pow(z,i*j,Q) for j in range(N)] for i in range(N)]
def residual_count(A):
    return sum((A[i][j]*A[0][0]-F[i][j]*A[i][0]*A[0][j])%Q==0 for i in range(1,N) for j in range(1,N))
assert residual_count(F)==100
scaled=[[F[i][j]*(i+2)*(j+4)%Q for j in range(N)] for i in range(N)]
assert residual_count(scaled)==100
scaled[1][1]=(scaled[1][1]+1)%Q
assert residual_count(scaled)==99

result={'independent_gaussian_sample_minors':330,'full_determinant_crosscheck':True,
 'identity_matrix_minor_counts_correct':True,'duplicate_row_detected':True,
 'duplicate_row_zero_minor_count':sum(d['zero_minors_by_order']),
 'disconnected_input_detected':True,'disconnected_input_routing_failure_count':sum(b['failed_routing_pairs_by_size']),
 'fourier_crossratio_positive_control':100,'endpoint_scaled_fourier_positive_control':100,
 'single_interior_entry_mutation_pass_count':99,'source_programs_executed_or_imported':False}
(BASE/'controls_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
