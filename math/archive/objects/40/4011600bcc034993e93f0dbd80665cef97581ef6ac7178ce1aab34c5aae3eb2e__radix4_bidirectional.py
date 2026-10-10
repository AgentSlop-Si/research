"""Exact radix-4 DFT control using bidirectional-sum scan stages.
No dense transform is used by scan_fft. This is ordinary mixed-radix FFT,
encoded in the proposed stage model, not a new asymptotic FFT.
"""
import json, random
from pathlib import Path


def scan_stage(x, radix, iroot, p):
    """x is gathered into independent radix-2/4 groups, in leaf column order."""
    n=len(x)
    if radix == 4:
        aa=[0,-1,-iroot,-1]; bb=[1,1,-1,1]
        cc=[1,-1,-1,0]; dd=[-1,-3,3,-3]
    elif radix == 2:
        aa=[0,1]; bb=[1,1]; cc=[1,0]; dd=[-1,-3]
    else: raise ValueError('radix must be 2 or 4')
    f=[0]*n; u=[0]*n
    for j in range(n):
        r=j%radix
        f[j]=((bb[r]*x[j]+aa[r]*f[j-1]) if r else bb[r]*x[j])%p
    for j in range(n-1,-1,-1):
        r=j%radix
        u[j]=((bb[r]*x[j]+cc[r]*u[j+1]) if r+1<radix else bb[r]*x[j])%p
    return [(f[j]+u[j]+dd[j%radix]*x[j])%p for j in range(n)]


def make_plan(n, root, p):
    assert n>0 and n&(n-1)==0
    lg=n.bit_length()-1
    radices=([2] if lg%2 else []) + [4]*(lg//2)
    assert pow(root,n,p)==1 and (n==1 or pow(root,n//2,p)!=1)
    rev=[]
    for pos in range(n):
        q=pos; source=0; place=n
        for radix in radices:
            digit=q%radix; q//=radix; place//=radix
            source+=digit*place
        rev.append(source)
    plans=[]; m=1; coefficient_multiplications=0; root_multiplications=0
    def root_power_of_two(exponent):
        nonlocal root_multiplications
        value=root
        while exponent>1:
            value=value*value%p; exponent//=2; root_multiplications+=1
        return value
    ir=root_power_of_two(n//4) if n>=4 else 0
    for radix in radices:
        m*=radix; stride=m//radix
        stage_root=root_power_of_two(n//m)
        col=[1,3,0,2] if radix==4 else [0,1]
        row=[0,2,1,3] if radix==4 else [0,1]
        tw=[]; t=1
        for j in range(stride):
            powers=[1,t]
            if radix==4:
                if j==0: powers += [1,1]
                else:
                    t2=t*t%p
                    powers += [t2, t2*t%p]
                    coefficient_multiplications+=2
            tw.append(powers)
            if j+1<stride:
                t=t*stage_root%p; coefficient_multiplications+=1
        gather=[]; scatter=[]; scalars=[]
        for base in range(0,n,m):
            for j in range(stride):
                for r in col:
                    gather.append(base+j+r*stride); scalars.append(tw[j][r])
                for r in row:
                    scatter.append(base+j+r*stride)
        plans.append((radix,gather,scatter,scalars))
    return rev, plans, coefficient_multiplications, root_multiplications, ir


def scan_fft(x, root, p, plan=None, counters=None):
    n=len(x)
    if plan is None: plan=make_plan(n,root,p)
    rev, stages, prep, root_prep, ir=plan
    a=[x[j]%p for j in rev]
    for radix,gather,scatter,scalars in stages:
        gathered=[a[j]*s%p if s!=1 else a[j] for j,s in zip(gather,scalars)]
        y=scan_stage(gathered,radix,ir,p)
        a=[0]*n
        for pos,value in zip(scatter,y): a[pos]=value
        if counters is not None:
            counters['stage_count']+=1
            counters['scan_multiplications']+=5*n-2*(n//radix)
            counters['scan_additions']+=4*n-2*(n//radix)
            counters['twiddle_data_multiplications']+=sum(s!=1 for s in scalars)
            counters['permutation_words']+=2*n
    return a


def direct_dft(x,root,p):
    n=len(x)
    return [sum(x[j]*pow(root,k*j,p) for j in range(n))%p for k in range(n)]


def check():
    rng=random.Random(20261009)
    records=[]; total_columns=0; random_vectors=0
    for p,g in [(998244353,3),(2013265921,31)]:
        for n in [2,4,8,16,32,64,128,256]:
            root=pow(g,(p-1)//n,p); plan=make_plan(n,root,p)
            for j in range(n):
                x=[0]*n; x[j]=1
                actual=scan_fft(x,root,p,plan)
                expected=[pow(root,k*j,p) for k in range(n)]
                assert actual==expected,(p,n,j)
                total_columns+=1
            for trial in range(3):
                x=[rng.randrange(p) for _ in range(n)]
                assert scan_fft(x,root,p,plan)==direct_dft(x,root,p),(p,n,trial)
                random_vectors+=1
            counters=dict(stage_count=0,scan_multiplications=0,scan_additions=0,
                          twiddle_data_multiplications=0,permutation_words=n)
            scan_fft([0]*n,root,p,plan,counters)
            counters['twiddle_preparation_multiplications']=plan[2]
            counters['root_preparation_multiplications']=plan[3]
            counters['root_preparation_method']='Explicit repeated squaring for each stage root and the fourth root; O((log N)^2) field operations'
            if n.bit_length()%2==1:  # n=4**s
                s=(n.bit_length()-1)//2
                assert counters['stage_count']==s
                assert counters['scan_multiplications']==9*n*s//2
                assert counters['scan_additions']==7*n*s//2
                assert counters['twiddle_data_multiplications']==3*n*s//4-n+1
                assert counters['twiddle_preparation_multiplications']==n-1-3*s
            records.append(dict(prime=p,N=n,basis_columns_checked=n,random_vectors_checked=3,**counters))
    result=dict(status='all exact checks passed',basis_columns_checked=total_columns,
                random_vectors_checked=random_vectors,records=records,
                scope='Finite modular checks plus the accompanying all-N radix identity. No sublogarithmic-stage claim.')
    Path(__file__).with_name('radix4_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': check()
