#!/usr/bin/env python3
"""Fresh exact N13 forced-window certificate. Standard library; no source imports.
All coefficient arrays are ascending powers in F_53[Y]."""
import argparse, hashlib, itertools, json
from pathlib import Path
P=53; Q=16; N=13

def trim(a):
    a=[x%P for x in a] or [0]
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)

def scale(a,c):return trim([x*c for x in a])
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)

def divmodp(a,b):
    a=trim(a);b=trim(b);assert b!=[0]
    q=[0]*max(1,len(a)-len(b)+1);ib=pow(b[-1],-1,P)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b);v=a[-1]*ib%P;q[k]=v
        for j,z in enumerate(b):a[k+j]=(a[k+j]-v*z)%P
        a=trim(a)
    return trim(q),a

def egcd(a,b):
    r0,r1=a,b;s0,s1=[1],[0];t0,t1=[0],[1]
    while r1!=[0]:
        q,r2=divmodp(r0,r1);r0,r1=r1,r2
        s0,s1=s1,sub(s0,mul(q,s1));t0,t1=t1,sub(t0,mul(q,t1))
    c=pow(r0[-1],-1,P)
    return scale(r0,c),scale(s0,c),scale(t0,c)

def modpow(a,k,m):
    z=[1]
    while k:
        if k&1:z=divmodp(mul(z,a),m)[1]
        a=divmodp(mul(a,a),m)[1];k//=2
    return z

def evaluate(a,x):
    z=0
    for v in reversed(a):z=(z*x+v)%P
    return z

def determinant(A):
    n=len(A);out=[0]
    for p in itertools.permutations(range(n)):
        v=[1]
        for i,j in enumerate(p):v=mul(v,A[i][j])
        parity=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2
        out=add(out,scale(v,(-1)**parity))
    return out

def gauss_product(e,d,a,b):
    r=e*a%N;l=d*b%N
    if r+l>=N:return 0
    w=pow(Q,e*d%N,P);num=den=1
    for i in range(1,l+1):
        num=num*(1-pow(w,r+i,P))%P;den=den*(1-pow(w,i,P))%P
    return num*pow(den,-1,P)%P

def moments(a,b):
    g=gauss_product(1,1,a,b);assert g
    const=pow(Q,10*(a+b)**2%N,P)*pow(g,-1,P)%P
    coeff=gauss_product(-1,1,a,b)*pow(gauss_product(-1,1,N-b,b)*g%P,-1,P)%P
    out=[const]+[0]*(N-a-b);out[-1]=(out[-1]-coeff)%P
    return trim(out)

def matrix_vector(A,x):
    out=[]
    for row in A:
        z=[0]
        for a,b in zip(row,x):z=add(z,mul(a,b))
        out.append(z)
    return out

def replacement_solution(A,b,omit):
    cols=[j for j in range(7) if j!=omit]
    B=[[row[j] for j in cols] for row in A];out=[[0] for _ in range(7)]
    for k,j in enumerate(cols):
        C=[[b[i] if l==k else row[l] for l in range(6)] for i,row in enumerate(B)]
        out[j]=determinant(C)
    return out

def make_certificate():
    labels=[(b,a) for b in (1,2) for a in range(b,N-b-7)]
    E=[[moments(a+j,b) for j in range(8)] for b,a in labels]
    A=[row[:7] for row in E];b=[scale(row[7],-1) for row in E]
    minors=[determinant([[row[j] for j in range(7) if j!=omit] for row in A]) for omit in range(7)]
    D0,D6=minors[0],minors[6]
    gcd,U,V=egcd(D6,D0);assert gcd==[1]
    f=scale(D6,pow(D6[-1],-1,P));assert len(f)==38
    first=modpow([0,1],P,f);frob=first
    for _ in range(36):frob=modpow(frob,P,f)
    assert frob==[0,1]
    irreducible_gcd,iu,iv=egcd(f,sub(first,[0,1]));assert irreducible_gcd==[1]
    n=[scale(d,(-1)**j) for j,d in enumerate(minors)]
    c6=replacement_solution(A,b,6);c0=replacement_solution(A,b,0)
    p=[add(mul(U,u),mul(V,v)) for u,v in zip(c6,c0)]
    assert matrix_vector(A,n)==[[0]]*6
    assert matrix_vector(A,p)==b
    assert matrix_vector(A,c6)==[mul(D6,z) for z in b]
    assert matrix_vector(A,c0)==[mul(D0,z) for z in b]
    return {'schema_version':1,'field_prime':P,'root':Q,'length':N,
            'coefficient_order':'ascending powers of Y, residues 0..52',
            'row_labels_b_a':[list(x) for x in labels],
            'E7':E,'maximal_minors_delete_columns_0_through_6':minors,
            'bezout':{'D6_multiplier':U,'D0_multiplier':V,'identity':[1]},
            'D6_monic':f,'irreducibility':{'degree':37,'X_to_53_mod_f':first,
            'X_to_53_power_37_mod_f':frob,'gcd_with_X_to_53_minus_X':[1],
            'f_multiplier':iu,'X_to_53_minus_X_multiplier':iv},
            'global_parameterization':{'particular_h0_through_h6':p,'kernel_h0_through_h6':n},
            'cramer_h6_zero_numerators':c6,'cramer_h0_zero_numerators':c0}

def validate(c):
    fresh=make_certificate();assert c==fresh
    E=c['E7'];A=[r[:7] for r in E];b=[scale(r[7],-1) for r in E]
    par=c['global_parameterization'];p=par['particular_h0_through_h6'];n=par['kernel_h0_through_h6']
    count=0
    for y in range(P):
        assert evaluate(c['D6_monic'],y)!=0
        for t in (0,1,2,52):
            h=[(evaluate(a,y)+t*evaluate(v,y))%P for a,v in zip(p,n)]
            assert any(evaluate(v,y) for v in n)
            for row,rhs in zip(A,b):assert sum(evaluate(v,y)*h[j] for j,v in enumerate(row))%P==evaluate(rhs,y)
            count+=1
    # Pinned chart reproduces the accepted original affine line, not a new proof of its full-sector acceptance.
    D6=c['maximal_minors_delete_columns_0_through_6'][6];D=evaluate(D6,1)
    c6=c['cramer_h6_zero_numerators']
    expected_const=[16,50,19,27,48,50,0]
    expected_slope=[31,25,11,10,15,22,1]
    for j in range(7):
        assert evaluate(c6[j],1)*pow(D,-1,P)%P==expected_const[j]
        v=1 if j==6 else evaluate(n[j],1)*pow(D,-1,P)%P
        assert v==expected_slope[j]
    # The genuine degree-37 chart singularity remains full rank by the alternative minor.
    f=c['D6_monic'];D0=c['maximal_minors_delete_columns_0_through_6'][0]
    assert divmodp(D6,f)[1]==[0] and divmodp(D0,f)[1]!=[0]
    # Negative controls: corrupt the target/particular solution, kernel and Bezout certificate.
    badp=[v[:] for v in p];badp[0]=add(badp[0],[1]);assert matrix_vector(A,badp)!=b
    badn=[v[:] for v in n];badn[0]=add(badn[0],[1]);assert matrix_vector(A,badn)!=[[0]]*6
    bz=c['bezout'];badU=add(bz['D6_multiplier'],[1])
    assert add(mul(badU,D6),mul(bz['D0_multiplier'],D0))!=[1]
    wrong_f=add(f,[1]);assert wrong_f!=f
    return {'verdict':'PASS','field_prime':P,'all_extension_rank':6,
            'minor_degrees':[len(v)-1 for v in c['maximal_minors_delete_columns_0_through_6']],
            'D6_leading_coefficient':D6[-1], 'D6_irreducible_degree':37,
            'bezout_multiplier_degrees':[len(bz[k])-1 for k in ('D6_multiplier','D0_multiplier')],
            'particular_degrees':[len(v)-1 for v in p],
            'kernel_degrees':[len(v)-1 for v in n],
            'base_field_parameter_regressions':count,'pinned_chart_coefficients_reproduced':14,
            'degree_37_chart_singularity_and_alternate_minor_checked':True,
            'negative_controls':{'particular_rejected':True,'kernel_rejected':True,'bezout_rejected':True},
            'historical_programs_executed':False,'support_search_performed':False,
            'scope':'Rank and affine support parameterization only; full-sector/splitting/existence unresolved.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--verify',type=Path)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    c=json.loads(args.verify.read_text()) if args.verify else make_certificate()
    receipt=validate(c)
    raw=(json.dumps(c,indent=2,sort_keys=True)+'\n').encode();receipt['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    if not args.verify:(args.out/'CERTIFICATE.json').write_bytes(raw)
    (args.out/'CHECK_RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))
if __name__=='__main__':main()
