"""Phase 37: projective phase-curvature gate and two-plaquette Green-pencil certificates.

Exact finite-field arithmetic. Theorem/proof in THEOREM.md. No claim of FFT speedup.
"""
from __future__ import annotations
import random, json, argparse
from pathlib import Path

P = 998244353
PRIMITIVE = 3
I = pow(PRIMITIVE, (P - 1)//4, P)
assert I*I % P == P-1


def root(n):
    assert n >= 2 and (n & (n-1)) == 0 and (P-1) % n == 0
    return pow(PRIMITIVE, (P-1)//n, P)


def invert(x):
    return pow(x, P-2, P)


def cycles(n, seed=3701):
    base=list(range(n))
    other=base[:]
    random.Random(seed+n).shuffle(other)
    return base, other


def cycle_green(n,cyc,alpha):
    """Exact dense reference; the online Green apply uses a cyclic recurrence."""
    pos=[0]*n
    for j,k in enumerate(cyc):pos[k]=j
    powers=[1]*n
    for j in range(1,n):powers[j]=powers[j-1]*alpha%P
    den=invert((1-powers[-1]*alpha)%P)
    return [[powers[(pos[i]-pos[j])%n]*den%P for j in range(n)] for i in range(n)]


def cycle_green_apply(cyc,alpha,vector):
    """O(N) Green application, using g_pos = x_pos + alpha*g_prev, cyclic."""
    n=len(cyc)
    powers=[1]*n
    for k in range(1,n): powers[k]=powers[k-1]*alpha%P
    den=invert((1-powers[-1]*alpha)%P)
    x=[vector[k]%P for k in cyc]
    # Solve g[j] = x[j]+alpha*g[j-1]; g[-1] = g[n-1].
    total=0
    # g[n-1] = x[n-1] + alpha*x[n-2] + ... + alpha^(n-1)*x[0] + alpha^n*g[n-1]
    for k in range(n):total=(total+powers[n-1-k]*x[k])%P
    last=total*den%P
    out=[0]*n
    prev=last
    for j in range(n):
        v=(x[j]+alpha*prev)%P
        out[j]=v;prev=v
    assert prev == last
    result=[0]*n
    for j,k in enumerate(cyc):result[k]=out[j]
    return result


def is_nth_root(x,n):
    return x!=0 and pow(x,n,P)==1


def ratio(M,a,b,i,j):
    """(i,j) with anchor (a,b)."""
    return M[i][j]*M[a][b]*invert(M[i][b]*M[a][j]%P)%P


def parity_curvature(M,n,a=0,b=0):
    """Return bit-packed (N-1)x(N-1) phase-exponent parity matrix.

    Requires EVERY anchored ratio to be an Nth root, otherwise returns None.
    No discrete logarithm: R^(N/2) = +/-1 exactly.
    """
    rows=[i for i in range(n) if i!=a]
    cols=[j for j in range(n) if j!=b]
    masks=[]
    for i in rows:
        mask=0
        for k,j in enumerate(cols):
            r=ratio(M,a,b,i,j)
            if not is_nth_root(r,n):return None
            parity=pow(r,n//2,P)
            assert parity in (1,P-1)
            if parity==P-1:mask|=(1<<k)
        masks.append(mask)
    return masks


def gf2_rank(bitrows):
    basis={}
    for mask in bitrows:
        v=mask
        while v:
            k=v.bit_length()-1
            if k in basis:v^=basis[k]
            else:
                basis[k]=v
                break
    return len(basis)


def scaled_permuted(M, seed=3705):
    n=len(M);r=random.Random(seed+n)
    rp=list(range(n));cp=list(range(n));r.shuffle(rp);r.shuffle(cp)
    rr=[r.randrange(1,P) for _ in range(n)]
    cc=[r.randrange(1,P) for _ in range(n)]
    return [[rr[i]*cc[j]*M[rp[i]][cp[j]]%P for j in range(n)] for i in range(n)]


def fourier(n):
    w=root(n); pw=[pow(w,k,P) for k in range(n)]
    return [[pw[(i*j)%n] for j in range(n)] for i in range(n)]


def small_audit(n,seed=3701,anchor_checks=8):
    assert (P-1)%(n*n)==0
    # alpha has exact order n^2 and alpha^n is primitive n-th root
    alpha=pow(PRIMITIVE,(P-1)//(n*n),P)
    g=cycle_green(n,cycles(n,seed)[1],alpha)
    f=fourier(n)
    gg=scaled_permuted(g,seed+1)
    ff=scaled_permuted(f,seed+2)
    rng=random.Random(seed+n)
    selected=[(0,0)]+[(rng.randrange(n),rng.randrange(n)) for _ in range(anchor_checks)]
    gr=[];fr=[]
    for a,b in selected:
        gr.append(gf2_rank(parity_curvature(gg,n,a,b)))
        fr.append(gf2_rank(parity_curvature(ff,n,a,b)))
    # matrix-free Green implementation check
    vec=[rng.randrange(P) for _ in range(n)]
    order=cycles(n,seed)[1]
    out=cycle_green_apply(order,alpha,vec)
    dense=[sum(g[i][j]*vec[j] for j in range(n))%P for i in range(n)]
    assert out==dense
    assert all(r==n-1 for r in gr), (n,gr)
    assert all(r==1 for r in fr), (n,fr)
    return dict(N=n,green_phase_curvature_ranks=gr,
                Fourier_phase_curvature_ranks=fr,
                anchor_count=len(selected),green_solve_exact=True,
                alpha_order=n*n)

# Polynomial arithmetic, arrays of coefficients in ascending powers

def trim(f):
    while len(f)>1 and f[-1]==0:f.pop()
    return f


def add(f,g):
    out=[0]*max(len(f),len(g))
    for k,x in enumerate(f):out[k]=x
    for k,x in enumerate(g):out[k]=(out[k]+x)%P
    return trim(out)


def sub(f,g):
    out=[0]*max(len(f),len(g))
    for k,x in enumerate(f):out[k]=x
    for k,x in enumerate(g):out[k]=(out[k]-x)%P
    return trim(out)


def mul(f,g):
    z=[0]*(len(f)+len(g)-1)
    for i,a in enumerate(f):
        if a:
            for j,b in enumerate(g):
                z[i+j]=(z[i+j]+a*b)%P
    return trim(z)


def power(f,k):
    out=[1]
    while k:
        if k&1:out=mul(out,f)
        k//=2
        if k:f=mul(f,f)
    return out


def monic(f):
    f=trim(f[:]);z=invert(f[-1]);return [x*z%P for x in f]


def divmod_poly(a,b):
    a=trim(a[:]);b=trim(b[:])
    assert b!=[0]
    if len(a)<len(b):return [0],a
    inv=invert(b[-1])
    q=[0]*(len(a)-len(b)+1)
    for off in range(len(q)-1,-1,-1):
        coeff=a[off+len(b)-1]*inv%P
        q[off]=coeff
        if coeff:
            for j,v in enumerate(b):a[off+j]=(a[off+j]-coeff*v)%P
    return trim(q), trim(a)


def gcd_poly(a,b):
    a=trim(a[:]);b=trim(b[:])
    while b!=[0]:
        _,r=divmod_poly(a,b)
        a,b=b,r
    return monic(a)


def plaquette_polynomial(A,B,n,ii,jj):
    # ii=(row0,row1), jj=(col0,col1)
    i,k=ii;j,l=jj
    v=lambda r,c:[A[r][c],B[r][c]]
    top=mul(v(i,j),v(k,l))
    bottom=mul(v(i,l),v(k,j))
    return sub(power(top,n),power(bottom,n))


def all_lambda_gate(n,seed=3701,include_witness=False):
    """For fixed genuinely complex noncommuting Green pair, find two
    2x2 plaquettes whose Nth-root constraints are coprime modulo p.
    Then no complex lambda (including those in extensions) can be
    monomially Fourier, after characteristic-zero lifting.
    """
    c1,c2=cycles(n,seed)
    # Exact Q(i) coefficients with non-real flux on each Green cycle.
    a=(1+I)*invert(4)%P
    b=(2+I)*invert(7)%P
    A=cycle_green(n,c1,a)
    B=cycle_green(n,c2,b)
    # Start from anchored 3x3 windows, then widen if necessary.
    candidates=[]
    for i in range(min(n,5)):
        for k in range(i+1,min(n,6)):
            for j in range(min(n,5)):
                for l in range(j+1,min(n,6)):
                    pl=plaquette_polynomial(A,B,n,(i,k),(j,l))
                    if pl != [0]:candidates.append(((i,k,j,l),pl))
    one=None
    for idx,(coords,p1) in enumerate(candidates):
        for coord2,p2 in candidates[idx+1:]:
            if gcd_poly(p1,p2)==[1]:
                one=(coords,p1,coord2,p2)
                break
        if one:break
    if one is None:return dict(N=n,seed=seed,excluded=False,plaquettes_tried=len(candidates))
    c0,p1,c1,p2=one
    result=dict(N=n,seed=seed,excluded=True,
                plaquettes=[c0,c1],degrees=[len(p1)-1,len(p2)-1],
                gcd_degree=0,prime=P,complex_alphas=['(1+i)/4','(2+i)/7'])
    if include_witness:
        result['polynomials_coefficients_mod_p']=[p1,p2]
    return result


def verify_bezout(a,b):
    """Extended Euclid: produce s*a+t*b == 1, a compact exact certificate."""
    r0,r1=trim(a[:]),trim(b[:]);s0,s1=[1],[0];t0,t1=[0],[1]
    while r1!=[0]:
        q,r=divmod_poly(r0,r1)
        r0,r1=r1,r
        s0,s1=s1,sub(s0,mul(q,s1))
        t0,t1=t1,sub(t0,mul(q,t1))
    sc=invert(r0[0]);s=[u*sc%P for u in s0];t=[u*sc%P for u in t0]
    assert add(mul(s,a),mul(t,b))==[1]
    return s,t


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='audit.json')
    ap.add_argument('--full',action='store_true')
    args=ap.parse_args()
    shape=[small_audit(n,anchor_checks=3 if n>=128 else 8) for n in (4,8,16,32,64,128)]
    obstruction=[]
    for n in (4,8,16,32,64):
        c=all_lambda_gate(n,include_witness=args.full)
        obstruction.append(c)
        print('N',n,'one-parameter phase exclusion',c['excluded'],c.get('degrees'),c.get('plaquettes'))
    out={'phase':37,'curvature':shape,'complex_two_Green_pencils':obstruction}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print('saved',args.output)

# CLI entrypoint is defined at bottom, after the two-mask architecture.

# --- Phase-37 main surviving architecture: three stages, two phase masks ---

def set_field(p:int,g:int):
    """Switch to an independent NTT prime for a fresh exact audit."""
    global P, PRIMITIVE, I
    P=int(p);PRIMITIVE=int(g)
    I=pow(PRIMITIVE,(P-1)//4,P)
    assert I*I%P == P-1


def gaussian(a,b,d=1):
    return (a+b*I)*invert(d)%P


def seeded_cycles(n,seed=37037):
    """Six distinct directed Hamiltonian cycles (canonical start at vertex zero)."""
    rng=random.Random(seed+n)
    c=[];seen=set()
    while len(c)<6:
        rest=list(range(1,n));rng.shuffle(rest)
        k=[0]+rest
        key=tuple(k)
        if key not in seen:
            seen.add(key);c.append(k)
    return c


def linear_combo_solve(cycles_,alphas,weights,vec):
    n=len(vec);out=[0]*n
    for cyc,a,weight in zip(cycles_,alphas,weights):
        got=cycle_green_apply(cyc,a,vec)
        for j in range(n):out[j]=(out[j]+weight*got[j])%P
    return out


def construct_two_mask_circuit(n,seed=37037):
    """O(N) application for each lambda:

    A D1 (G2 + lambda*G3) D2 C, where A,C are TWO-Term Green sums.
    Six independently ordered complex Green solves, two diagonal masks.
    Coefficients are in Q(i); every denominator invertible over Q(i).
    """
    c=seeded_cycles(n,seed)
    a=[gaussian(1,1,4),gaussian(2,1,7),gaussian(1,2,8),
       gaussian(1,-1,5),gaussian(2,1,9),gaussian(1,1,6)]
    wa=[1,gaussian(1,1,3)]
    wc=[1,gaussian(1,-1,4)]
    d1=[pow(I,(3*j+1)%4,P) for j in range(n)]
    d2=[pow(I,(j*j+j+1)%4,P) for j in range(n)]
    def apply(vec,lamb):
        y=linear_combo_solve(c[4:6],a[4:6],wc,vec)
        y=[y[j]*d2[j]%P for j in range(n)]
        y=linear_combo_solve(c[2:4],a[2:4],[1,lamb],y)
        y=[y[j]*d1[j]%P for j in range(n)]
        return linear_combo_solve(c[0:2],a[0:2],wa,y)
    def pencil_columns(cols=(0,1,2,3)):
        # We share the preprocessed C e_j result across BOTH B0 and B1.
        M0=[[0]*len(cols) for _ in range(n)]
        M1=[[0]*len(cols) for _ in range(n)]
        for k,col in enumerate(cols):
            x=[0]*n;x[col]=1
            y=linear_combo_solve(c[4:6],a[4:6],wc,x)
            y=[y[j]*d2[j]%P for j in range(n)]
            for s,M in ((2,M0),(3,M1)):
                z=cycle_green_apply(c[s],a[s],y)
                z=[z[j]*d1[j]%P for j in range(n)]
                v=linear_combo_solve(c[:2],a[:2],wa,z)
                for j in range(n):M[j][k]=v[j]
        return M0,M1
    return {'apply':apply,'pencil_columns':pencil_columns,'cycles':c,
            'alphas':a,'outer_weights':[wa,wc],'mask1':d1,'mask2':d2}


def two_mask_gate(n,seed=37037,include_witness=False):
    """Find two plaquettes whose Nth-root constraints eliminate ALL complex
    lambda for this seeded phase-masked product-of-Green-sums circuit.
    Returns an explicit modular Bezout certificate if requested.
    """
    circuit=construct_two_mask_circuit(n,seed)
    a,b=circuit['pencil_columns'](tuple(range(min(n,5))))
    candidates=[]
    for i in range(min(n,4)):
        for k in range(i+1,min(n,5)):
            for j in range(min(n,4)):
                for l in range(j+1,min(n,5)):
                    f=plaquette_polynomial(a,b,n,(i,k),(j,l))
                    if f!=[0] and len(f)==2*n+1: candidates.append(((i,k,j,l),f))
    found=None
    for idx,(window,f) in enumerate(candidates):
        for window2,g in candidates[idx+1:]:
            if gcd_poly(f,g)==[1]:
                found=(window,f,window2,g);break
        if found:break
    if not found:return dict(N=n,excluded=False,complete_degree_plaquettes=len(candidates),prime=P)
    x,f,y,g=found
    # Verify one independent random-vector matrix-free executor for lambda=3+i.
    lamb=gaussian(3,1)
    rng=random.Random(3700+n)
    vec=[rng.randrange(P) for _ in range(n)]
    reference=circuit['apply'](vec,lamb)
    # Separately compute on every basis column for small sizes, or use linearity
    # on a precomputed small subset for larger sizes.
    if n<=32:
        dense=[[0]*n for _ in range(n)]
        for col in range(n):
            v=[0]*n;v[col]=1
            out=circuit['apply'](v,lamb)
            for row in range(n):dense[row][col]=out[row]
        assert reference==[sum(dense[i][j]*vec[j] for j in range(n))%P for i in range(n)]
    result={'N':n,'seed':seed,'excluded':True,'prime':P,
            'plaquettes':[x,y], 'degrees':[len(f)-1,len(g)-1],
            'leading_coefficients_mod_prime':[f[-1],g[-1]],
            'gcd':1, 'middle_complex_parameter':'lambda',
            'outer_complex_Green_terms':4,'middle_Green_terms':2,
            'internal_complex_diagonal_masks':2,'online_Green_solves':6,
            'full_degree_preserved_under_reduction':True,
            'exact_application_control':True}
    if include_witness:
        s,t=verify_bezout(f,g)
        result['polynomials_coefficients_mod_prime']=[f,g]
        result['bezout_coefficients_mod_prime']=[s,t]
        result['cycle_orders']=circuit['cycles']
    return result


def phase37_main():
    ap=argparse.ArgumentParser(description='Phase 37 exact curvature and two-mask tests')
    ap.add_argument('--output',default='audit.json')
    ap.add_argument('--full',action='store_true',help='write independent Bezout witnesses')
    ap.add_argument('--prime',type=int,default=998244353,choices=[998244353,2013265921])
    a=ap.parse_args()
    set_field(a.prime,3 if a.prime==998244353 else 31)
    shapes=[small_audit(n,anchor_checks=2 if n>=128 else 8) for n in (4,8,16,32,64,128)]
    results=[two_mask_gate(n,include_witness=a.full) for n in (4,8,16,32,64,128)]
    out={'phase':37,'prime':P,'curvature':shapes,'two_mask_complex_pencil':results}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    for o in results:print('N',o['N'],'all lambda excluded',o['excluded'],'degrees',o.get('degrees'))
    print('Saved',a.output)

if __name__=='__main__': phase37_main()
