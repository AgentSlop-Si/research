"""Exact symbolic certificates and finite falsification controls.
No finite list of primes is used as a substitute for REPORT.md's uniform proof.
"""
from pathlib import Path
from fractions import Fraction as F
import json, math, sympy as S
OUT=Path(__file__).resolve().parent

def vp(a,p):
    assert a
    n=0
    while a%p==0:a//=p;n+=1
    return n

def three_certificate():
    t=S.symbols('t');J=9
    zero=S.Poly(0,t);E=[S.Poly(1,t)]+[zero]*J;O=E[:]
    for k in range(1,10):
        En=[(O[j-1] if j else zero)*t**3-O[j]*t**3+E[j]*((1+t)**(2*k-1)-1) for j in range(J+1)]
        On=[En[j]+O[j]*((1+t)**(2*k)-1) for j in range(J+1)]
        E,O=En,On
    ms=[25,28,24,21];us=[1,2,2,1];cert=[]
    for j,poly in enumerate(O):
        coeff={int(a[0]):int(c) for a,c in poly.terms()}
        L=9+2*j
        assert min(coeff)>=L
        rawmin=min(a+18*vp(c,3) for a,c in coeff.items())
        if j<4:
            m,u=ms[j],us[j]
            assert min(a for a,c in coeff.items() if c%3)==m
            assert coeff[m]%3==u
            assert 18+L>m
            lowest=[(a,c%3) for a,c in coeff.items() if a+18*vp(c,3)==rawmin]
            assert lowest==[(m,u)]
            assert rawmin-21==[4,7,3,0][j]
        cert.append({'V_degree':j,'proven_t_divisibility':L,'integer_coefficients':coeff,'raw_weight_at_e18':rawmin,'normalized_weight_at_e18':rawmin-21,'first_mod3_unit_degree':min(a for a,c in coeff.items() if c%3),'first_mod3_unit':next(c%3 for a,c in sorted(coeff.items()) if c%3)})
    assert all(c['normalized_weight_at_e18']>=0 for c in cert)
    assert [c['V_degree'] for c in cert if c['normalized_weight_at_e18']==0]==[3]
    (OUT/'THREE_CERTIFICATE.json').write_text(json.dumps({'recurrence':'E_k=t^3(V-1)O_(k-1)+((1+t)^(2k-1)-1)E_(k-1); O_k=E_k+((1+t)^(2k)-1)O_(k-1)','all_s_reason':'For each of j=0,1,2,3, 18+L_j>m_j, so the unique p-unit term stays lowest for every e>=18.','coefficients':cert},indent=2)+'\n')
    return [{k:c[k] for k in c if k!='integer_coefficients'} for c in cert]

def integer_control(p):
    N=p*p;B=p*(p-1);E=F(N,2)+2*B;D=N+E-p;Wn=N+2*B;d=F(B,2)
    def W(m):return m+(p-1)*(m//p)+(N-p)*(m//N)
    def T(m):return m+F(p-2,2)*((m+p-1)//p)
    def delta(m):return T(m)-F(W(m),2)
    for m in range(2*N+1):
        c,rem=divmod(m,N);a,b=divmod(rem,p)
        assert 2*delta(m)==a*(p-1)+b+(p-2)*(b>0)
        assert (delta(m)==0)==(m in [0,N,2*N])
    mv=[];hv=[];dv=[]
    for k in range(1,2*N,2):
        w=W(2*N-1)-W(k)-W((2*N-1-k)//2)+T(k)
        if k==N:assert w==E
        else:assert w>=E+F(p-1,2)
        mv.append((w-E,k))
    for k in range(0,2*N+1,2):
        w=W(2*N)-W(k)-W((2*N-k)//2)+T(k)
        if k in [0,2*N]:assert w==Wn
        else:assert w>=Wn+d+F(p-1,2)
        hv.append((w-Wn,k))
        for m in range(k):
            j=k-m
            wt=W(2*N)-W((2*N-k)//2)-W(m)+T(m)-p**vp(j,p)
            eta=p+F(W(j-1),2)-p**vp(j,p)
            assert wt-D>=eta+delta(m)
            if (k,m)==(2*N,N):assert wt==D
            else:assert wt>=D+F(p-1,2)
            dv.append((wt-D,k,m))
    return {'p':p,'neighbor_leading':[(str(w),k) for w,k in mv if w==0],'neighbor_min_nonpivot_gap':str(min(w for w,k in mv if k!=N)),'H_min_nonpivot_gap':str(min(w for w,k in hv if k not in [0,2*N])),'derivative_leading':[(str(w),k,m) for w,k,m in dv if w==0],'derivative_min_nonpivot_gap':str(min(w for w,k,m in dv if (k,m)!=(2*N,N)))}

def field_control(p,s,jet=None):
    if jet is None:jet=min(p+1,10)
    N=p*p;order=p**s;gap=order//p;e=order-gap;W=3*N-2*p;d=p*(p-1)//2
    one=[1]+[0]*(e-1)
    def shift(v,k):
        out=[0]*e
        for j,b in enumerate(v):
            if not b:continue
            j=(j+k)%order
            if j<e:out[j]+=b
            else:
                for l in range(p-1):out[j-e+l*gap]-=b
        return out
    def tmul(v,k):
        for _ in range(k):v=[a-b for a,b in zip(shift(v,1),v)]
        return v
    def val(v):
        cs=v[:]
        for a in range(e-2,-1,-1):
            for j in range(a,e-1):cs[j]+=cs[j+1]
        vals=[]
        for j,b in enumerate(cs):
            if not b:continue
            vv=vp(b,p);vals.append((j+vv*e,(b//p**vv)*(-1)**vv%p))
        return min(vals) if vals else None
    E=[one]+[[0]*e for _ in range(jet)];O=[v[:] for v in E]
    for k in range(1,N+1):
        En=[]
        for j in range(jet+1):
            zpart=tmul([a-b for a,b in zip(O[j-1] if j else [0]*e,O[j])],p)
            edge=shift(E[j],2*k-1)
            En.append([a+b-c for a,b,c in zip(zpart,edge,E[j])])
        On=[]
        for j in range(jet+1):
            edge=shift(O[j],2*k)
            On.append([a+b-c for a,b,c in zip(En[j],edge,O[j])])
        E,O=En,On
    values=[val(v) for v in O]
    jets=[(v[0]-W,v[1]) if v else None for v in values]
    if p==3:assert jets[:4]==[(4,1),(7,2),(3,2),(0,1)]
    else:
        assert jets[0][0]>p
        assert jets[1]==(d+1,pow(8,-1,p))
        assert jets[p]==(0,1) if p<=jet else True
    return {'p':p,'s':s,'e':e,'W':W,'d':d,'normalized_V_jets':jets,'central_root_derivative_claim':str(F(76,3)) if p==3 else str(W+d+1)}

if __name__=='__main__':
    three=three_certificate();print('Exact p=3 integer certificate: PASS',flush=True)
    integers=[integer_control(p) for p in [3,5,7,11,13,17,19,23]];print('Finite Newton-gap controls: PASS',flush=True)
    fields=[]
    for p,s in [(3,3),(3,4),(5,3),(7,3),(11,3)]:
        row=field_control(p,s);fields.append(row);print(json.dumps(row),flush=True)
    (OUT/'CONTROL_RESULTS.json').write_text(json.dumps({'exact_three_certificate_summary':three,'finite_integer_controls':integers,'finite_original_cyclotomic_controls':fields},indent=2)+'\n')
    print('ALL CONTROLS PASS; finite field controls are not a uniform proof.',flush=True)
