#!/usr/bin/env python3
"""Fresh exact checks. Does not import or execute supplied R30 code."""
from fractions import Fraction as F
import hashlib, json
from pathlib import Path

OUT = Path(__file__).resolve().parent

def bitrev(j, D):
    return int(format(j, '0%db' % D)[::-1], 2)

def stage(rows, m, N):
    """Exact coefficients represented by exponents of a primitive Nth root.
    Disjoint supports are verified before merging, so no polynomial simplification
    or numerical root approximations are needed.
    """
    nrows = [None] * N
    step = 1 << m
    half = step >> 1
    for q in range(0, N, step):
        for j in range(half):
            a, b = q+j, q+j+half
            assert not (rows[a].keys() & rows[b].keys())
            phase = j * (N // step)
            ra = dict(rows[a]); rb = dict(rows[a])
            for col, exponent in rows[b].items():
                ra[col] = (exponent + phase) % N
                rb[col] = (exponent + phase + N//2) % N
            nrows[a], nrows[b] = ra, rb
    return nrows

def fft_case(D):
    N=1 << D
    rows=[{bitrev(r,D):0} for r in range(N)]
    for m in range(1,D+1):
        rows=stage(rows,m,N)
    for r in range(N):
        assert len(rows[r])==N
        for c in range(N):
            assert rows[r][c] == (r*c)%N
    window_count=0; entries_checked=0; interval_count=0
    k1_blocks=0
    for a in range(1,D+1):
        rows=[{r:0} for r in range(N)]
        for b in range(a,D+1):
            rows=stage(rows,b,N); k=b-a+1
            interval_count += 1
            mask=((1<<k)-1) << (a-1)
            for r,row in enumerate(rows):
                assert len(row)==1<<k
                assert all((r^c)&~mask == 0 for c in row)
                entries_checked += len(row)
            window_count += N//(1<<k)
            if k==1:
                bit=1<<(a-1)
                for r in range(N):
                    if not r&bit:
                        s=r^bit
                        cross=(rows[r][r]+rows[s][s]-rows[r][s]-rows[s][r])%N
                        assert cross == N//2
                        k1_blocks += 1
    assert window_count == N*(D-1)+1
    assert interval_count == D*(D+1)//2
    assert k1_blocks == N*D//2
    generic = N*D//2 - 3*N//2 + 2
    # A separate direct instruction-loop count, not just formula evaluation.
    butterflies=trivial=i_phase=nontrivial=0
    for m in range(1,D+1):
        for q in range(0,N,1<<m):
            for j in range(1<<(m-1)):
                butterflies += 1
                e=j*(N//(1<<m))
                if e==0: trivial += 1
                elif 4*e==N: i_phase += 1
                else: nontrivial += 1
    assert butterflies == N*D//2
    assert trivial == N-1
    assert i_phase == N//2-1
    assert nontrivial == generic
    return dict(D=D,N=N,full_transform_entries_checked=N*N,
        whole_stage_intervals=interval_count,component_windows=window_count,
        eligible_rho_pm3=0,one_stage_blocks=k1_blocks,
        interval_nonzero_entries_checked=entries_checked,
        complex_additions=N*D,general_complex_twiddle_multiplications=generic,
        real_additions_4mult_twiddles=2*N*D+2*generic,
        real_multiplications_4mult_twiddles=4*generic)

# Exact Gaussian rationals, independent of a numerical complex library.
def z(a=0,b=0): return (F(a),F(b))
def za(x,y): return (x[0]+y[0],x[1]+y[1])
def zn(x): return (-x[0],-x[1])
def zs(x,y): return za(x,zn(y))
def zm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def zi(x):
    d=x[0]*x[0]+x[1]*x[1]
    assert d
    return (x[0]/d,-x[1]/d)
def zd(x,y): return zm(x,zi(y))
def ms(A,s): return [[zm(x,s) for x in row] for row in A]
def mm(A,B):
    return [[za(zm(A[r][0],B[0][c]),zm(A[r][1],B[1][c])) for c in range(2)] for r in range(2)]
def ma(A,B): return [[za(A[r][c],B[r][c]) for c in range(2)] for r in range(2)]
def cross(A): return zd(zm(A[0][0],A[1][1]),zm(A[0][1],A[1][0]))
def inv(A):
    det=zs(zm(A[0][0],A[1][1]),zm(A[0][1],A[1][0]))
    return ms([[A[1][1],zn(A[0][1])],[zn(A[1][0]),A[0][0]]],zi(det))

def gaussian_checks():
    I=[[z(1),z()],[z(),z(1)]]
    C=[[z(F(1,2),F(1,2)),z(F(1,2),F(-1,2))],
       [z(F(1,2),F(-1,2)),z(F(1,2),F(1,2))]]
    Z=[[z(1),z()],[z(),z(-1)]]
    M=[[z(),z(0,-1)],[z(0,1),z()]]
    H=[[z(1),z(1)],[z(1),z(-1)]]
    assert mm(mm(inv(C),Z),C)==M
    assert mm(M,M)==I
    rows=[]
    # Include exact ±i positive controls and noneligible real controls.
    for rho in [z(3),z(-3),z(2),z(-2),z(0,1),z(0,-1)]:
        Q=ma(I,ms(Z,zn(rho)))
        R=mm(mm(inv(C),inv(Q)),C)
        explicit=ms(ma(I,ms(M,rho)),zi(zs(z(1),zm(rho,rho))))
        assert R==explicit
        cr=cross(R)
        assert cr == zi(zm(rho,rho))
        if rho in (z(3),z(-3)): assert cr==z(F(1,9))
        if rho in (z(0,1),z(0,-1)):
            assert cr==z(-1)
            # u=-i is M[0,1]. B(t) = (1-rho^2) L R D.
            u=M[0][1]; t=z(2,3)
            L=[[z(1),z()],[z(),zd(u,rho)]]
            D=[[z(1),z()],[z(),zd(t,zm(rho,u))]]
            B=[[z(1),t],[z(1),zn(t)]]
            assert ms(mm(mm(L,R),D),zs(z(1),zm(rho,rho)))==B
        rows.append(dict(rho=str(rho),cross_ratio=str(cr)))
    assert cross(H)==z(-1)
    # Exact positive-control full butterfly identity for the generalized rho=i.
    Ri=ms(ma(I,ms(M,z(0,1))),z(F(1,2)))
    assert ms(mm(Z,Ri),z(2))==H
    # Negative controls: changing the butterfly's minus sign changes cross ratio.
    assert cross([[z(1),z(1)],[z(1),z(1)]])==z(1)
    # A rho=3 block is full rank but not projectively a butterfly.
    assert cross(ms(ma(I,ms(M,z(3))),z(F(-1,8))))!=cross(H)
    return rows

def phase_support_checks():
    # Exact finite-field corroboration only; proof over C is in PROOF.md.
    p=65537
    # 3 is primitive of order 65536, verified rather than assumed.
    assert pow(3,65536,p)==1 and pow(3,32768,p)!=1
    cases=[]
    for D in range(1,11):
        N=1<<D; eta=pow(3,65536//(2*N),p)
        assert pow(eta,N,p)==p-1
        for s in range(D+1):
            S=list(range(s))
            weights=[]
            for h in S:
                t=pow(eta,1<<h,p)
                assert t not in (1,p-1)
                weights.append(((1+t)*pow(2,-1,p)%p,(1-t)*pow(2,-1,p)%p))
            coeff=[1]
            for a,b in weights:
                coeff=[c*a%p for c in coeff]+[c*b%p for c in coeff]
            assert len(coeff)==1<<s and all(coeff)
            cases.append(dict(D=D,selected_axes=s,distinct_xor_terms=len(coeff)))
    return cases

def main():
    cases=[fft_case(D) for D in range(1,11)]
    # Original archive provenance only; exact source excerpts are in source/.
    source_provenance=json.loads((OUT/'SOURCE_PROVENANCE.json').read_text())
    result={
      "status":"PASS",
      "method":"Fresh exact symbolic root exponents, exact Gaussian rational checks, and separately labeled finite-field corroboration.",
      "supplied_code_executed":False,
      "source_archive_sha256":source_provenance['original_archive_sha256'],
      "fft_cases":cases,
      "gaussian_checks":gaussian_checks(),
      "phase_support_checks":phase_support_checks(),
      "scope":"Explicit radix-two DIT stage/component windows under invertible monomial boundary changes; not all Fourier factorizations."
    }
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"status":result["status"],"largest_fft":cases[-1],
        "total_full_transform_entries":sum(c["full_transform_entries_checked"] for c in cases),
        "total_component_windows":sum(c["component_windows"] for c in cases),
        "phase_support_cases":len(result["phase_support_checks"])},indent=2))

if __name__=='__main__':
    main()
