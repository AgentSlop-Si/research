"""Fresh Phase44 checker; only standard libraries and mpmath are imported.

Reads frozen JSON data, never imports or executes any submitted Python program.
Uses dense differentiated path-sum Green matrices, followed by an ordinary
product rule and quotient rule, rather than the submitted rank-one/log formula.
All proof comparisons remain in outward-rounded real interval arithmetic.
"""
import argparse, hashlib, json, random, time
from pathlib import Path
from mpmath import iv, mp

ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--dps', type=int, default=70)
ap.add_argument('--radius', default='1e-20')
ap.add_argument('--output', default='fresh_interval_results.json')
args = ap.parse_args()
iv.dps = args.dps
mp.dps = args.dps
data_path = ROOT/'extracted/phase44_full_N8_box.json'
data = json.loads(data_path.read_text())
n = data['N']; depth = data['depth']
assert (n, depth, data['greens_per_layer']) == (8,4,3)
selected = data['selected_variable_indices']
frozen = data['frozen_indices']
assert len(selected) == len(set(selected)) == 98
assert len(frozen) == len(set(frozen)) == 12
assert set(selected).isdisjoint(frozen)
assert sorted(selected+frozen) == list(range(110))
assert len(data['center_decimals']) == 110
assert len(data['B_preconditioner_decimals']) == 98
assert all(len(row)==98 for row in data['B_preconditioner_decimals'])
assert all(type(s) is str for s in data['center_decimals'])
assert all(type(s) is str for row in data['B_preconditioner_decimals'] for s in row)
zero = iv.mpc(0); one = iv.mpc(1); ii = iv.mpc(0,1)

def matrix_zero(): return [[zero for _ in range(n)] for _ in range(n)]
def identity(): return [[one if r==c else zero for c in range(n)] for r in range(n)]
def product(A,B):
    return [[sum((A[r][k]*B[k][c] for k in range(n)),zero) for c in range(n)] for r in range(n)]
def unit(x): return iv.mpc(iv.cos(x),iv.sin(x))
def upper(x): return float(x.b)
def lower(x): return float(x.a)
def norm_inf(A): return max(sum((abs(x) for x in row),iv.mpf(0)).b for row in A)
def diagnostic(v): return float(v)

# Reproduce the declared seeded orders, then freeze the actual combinatorics.
architecture=[]
for stage in range(depth):
    rng=random.Random(44321+997*stage+n)
    cycles=[list(range(n))]
    for _ in range(2):
        c=list(range(n)); rng.shuffle(c); cycles.append(c)
    components=[{i} for i in range(n)]
    tree=[]; chords=[]
    for e in range(3*n):
        s,j=divmod(e,n); a,b=cycles[s][j-1],cycles[s][j]
        ca=next(C for C in components if a in C)
        cb=next(C for C in components if b in C)
        if ca is cb: chords.append(e)
        else:
            tree.append(e); components.remove(ca); components.remove(cb); components.append(ca|cb)
    assert tree==list(range(7)) and chords==list(range(7,24))
    architecture.append({'orders':cycles,'tree_edges':tree,'chord_edges':chords})
(ROOT/'fresh_architecture.json').write_text(json.dumps(architecture,indent=2)+'\n')

def build(radius, need_derivatives):
    x=[iv.mpf(s) for s in data['center_decimals']]
    if radius != '0':
        r=iv.mpf(radius)
        for k in selected: x[k] += iv.mpf([-r.b,r.b])
    factors=[]; derivatives={}; green_guards=[]; holonomies=[]; green_checks=[]
    p=0
    for stage,spec in enumerate(architecture):
        S=matrix_zero()
        weights=[one for _ in range(3*n)]
        var_of_edge={}
        for e in spec['chord_edges']:
            weights[e]=unit(x[p]); var_of_edge[e]=p; p+=1
        for s,order in enumerate(spec['orders']):
            w=weights[s*n:(s+1)*n]
            h=one
            for value in w: h*=value
            den=one-h
            assert abs(den).a > 0, 'Green holonomy denominator includes zero'
            green_guards.append(abs(den)); holonomies.append(h)
            G=matrix_zero()
            dGs={e:matrix_zero() for e in range(s*n,(s+1)*n) if e in var_of_edge and var_of_edge[e] in selected} if need_derivatives else {}
            for b in range(n):
                path=one; used=set()
                for steps in range(n):
                    a=(b+steps)%n
                    value=path/den
                    G[order[a]][order[b]]=value
                    S[order[a]][order[b]] += value
                    for e,dG in dGs.items():
                        dG[order[a]][order[b]]=ii*value*(int(e-s*n in used)+h/den)
                    e=(a+1)%n; used.add(e); path*=w[e]
            # Direct residual of (I-W)G=I, with no matrix inverse routine.
            for a in range(n):
                for b in range(n):
                    z=G[order[a]][b]-w[a]*G[order[a-1]][b]-int(order[a]==b)
                    assert 0 in z.real and 0 in z.imag
                    green_checks.append(abs(z))
            for e,dG in dGs.items(): derivatives[var_of_edge[e]]=(2*stage,dG)
        factors.append(S)
        if stage<depth-1: factors.append(None)
    assert p==68
    amp_ranges=[]
    for stage in range(depth-1):
        D=matrix_zero();D[0][0]=one
        for k in range(1,n):
            phase_idx=p+k-1; amp_idx=p+(n-1)+k-1
            amp=iv.exp(x[amp_idx]);z=amp*unit(x[phase_idx]);D[k][k]=z
            assert abs(z).a > 0
            amp_ranges.append(amp)
            if need_derivatives:
                for idx,dz in ((phase_idx,ii*z),(amp_idx,z)):
                    if idx in selected:
                        dD=matrix_zero();dD[k][k]=dz; derivatives[idx]=(2*stage+1,dD)
        factors[2*stage+1]=D;p+=14
    assert p==110
    prefixes=[identity()]
    for A in factors: prefixes.append(product(A,prefixes[-1]))
    suffixes=[None]*(len(factors)+1);suffixes[-1]=identity()
    for k in range(len(factors)-1,-1,-1): suffixes[k]=product(suffixes[k+1],factors[k])
    M=prefixes[-1]
    denominators=[M[0][j] for j in range(n)]+[M[r][0] for r in range(1,n)]
    assert all(abs(z).a>0 for z in denominators), 'Projective denominator includes zero'
    target=[[unit(-2*iv.pi*r*j/n) for j in range(n)] for r in range(n)]
    Q=[[M[r][j]*M[0][0]/(M[0][j]*M[r][0]) for j in range(n)] for r in range(n)]
    fcomplex=[Q[r][j]-target[r][j] for r in range(1,n) for j in range(1,n)]
    f=[z.real for z in fcomplex]+[z.imag for z in fcomplex]
    info={
       'min_green_one_minus_h_abs_lower':min(lower(z) for z in green_guards),
       'min_projective_denominator_abs_lower':min(lower(abs(z)) for z in denominators),
       'min_all_64_M_entry_abs_lower':min(lower(abs(z)) for row in M for z in row),
       'max_all_64_calibrated_F8_error_upper':max(upper(abs(Q[r][j]-target[r][j])) for r in range(n) for j in range(n)),
       'max_green_inverse_identity_error_upper':max(upper(z) for z in green_checks),
       'interstage_amplitude_min_lower':min(lower(z) for z in amp_ranges),
       'interstage_amplitude_max_upper':max(upper(z) for z in amp_ranges),
    }
    all64=[{'r':r,'j':j,'calibrated_error_absolute_upper_diagnostic':upper(abs(Q[r][j]-target[r][j])),
            'fourier_target_in_calibrated_interval': bool(target[r][j].real.a>=Q[r][j].real.a and target[r][j].real.b<=Q[r][j].real.b and target[r][j].imag.a>=Q[r][j].imag.a and target[r][j].imag.b<=Q[r][j].imag.b)} for r in range(n) for j in range(n)]
    if not need_derivatives: return f,info,all64
    Jc=[[zero for _ in selected] for _ in range(49)]
    for c,idx in enumerate(selected):
        pos,dA=derivatives[idx]
        dM=product(suffixes[pos+1],product(dA,prefixes[pos]))
        for r in range(1,n):
            for j in range(1,n):
                numerator=M[r][j]*M[0][0]
                denominator=M[0][j]*M[r][0]
                dnum=dM[r][j]*M[0][0]+M[r][j]*dM[0][0]
                dden=dM[0][j]*M[r][0]+M[0][j]*dM[r][0]
                Jc[(r-1)*7+j-1][c]=(dnum*denominator-numerator*dden)/(denominator*denominator)
        if (c+1)%20==0: print('Jacobian columns',c+1,flush=True)
    J=[[z.real for z in row] for row in Jc]+[[z.imag for z in row] for row in Jc]
    return f,J,info,all64

start=time.time()
f,center_info,center64=build('0',False)
B=[[iv.mpf(s) for s in row] for row in data['B_preconditioner_decimals']]
shifts=[sum((B[i][k]*f[k] for k in range(98)),iv.mpf(0)) for i in range(98)]
shift=max(abs(v).b for v in shifts)
print('Center shift upper',shift,flush=True)
_,J,box_info,box64=build(args.radius,True)
rows=[]
for i in range(98):
    errors=[iv.mpf(int(i==j))-sum((B[i][k]*J[k][j] for k in range(98)),iv.mpf(0)) for j in range(98)]
    rows.append(sum((abs(v).b for v in errors),iv.mpf(0)).b)
    if (i+1)%20==0: print('Contraction rows',i+1,'max',max(rows),flush=True)
contraction=max(rows)
radius=iv.mpf(args.radius)
proof={'shift_lt_radius_over_4':bool(shift<radius/4),
       'contraction_lt_half':bool(contraction<iv.mpf('0.5')),
       'shift_plus_contraction_radius_lt_radius':bool(shift+contraction*radius<radius),
       'shift_lt_1e_minus_55':bool(shift<iv.mpf('1e-55')),
       'contraction_lt_1e_minus_5':bool(contraction<iv.mpf('1e-5'))}
result={'input_certificate_sha256':hashlib.sha256(data_path.read_bytes()).hexdigest(),
        'interval_library':'mpmath 1.3.0 iv','interval_dps':args.dps,'radius_exact_decimal':args.radius,
        'free_real_coordinates':98,'fixed_real_coordinates':12,
        'max_Bf_upper_diagnostic':upper(shift),'contraction_upper_diagnostic':upper(contraction),
        'certified_rational_comparisons':proof,
        'strict_Banach_certificate_pass':all(proof[k] for k in ['shift_lt_radius_over_4','contraction_lt_half','shift_plus_contraction_radius_lt_radius']),
        'center':center_info,'box':box_info,'all64_center':center64,'all64_box':box64,
        'contraction_row_sum_upper_diagnostics':[upper(v) for v in rows],
        'seconds':time.time()-start,
        'source_code_executed':False,
        'meaning':'Exact full F8 existence nearby, with complex nonzero interstage diagonals and outer diagonal calibration; decimal center is not asserted to be an exact root.'}
(ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if not k.startswith('all64') and k!='contraction_row_sum_upper_diagnostics'},indent=2),flush=True)
assert result['strict_Banach_certificate_pass']
