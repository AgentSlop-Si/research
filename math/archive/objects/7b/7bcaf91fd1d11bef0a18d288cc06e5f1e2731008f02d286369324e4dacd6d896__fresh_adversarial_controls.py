"""New second-pass controls. No supplied program is read, imported, or executed.
Finite tests are falsification aids and are not asymptotic runtime evidence.
"""
from fractions import Fraction as F
from itertools import product
import json, math, hashlib
from pathlib import Path
import mpmath as mp
import numpy as np
mp.mp.dps=90

def pow2(e): return F(2**e) if e>=0 else F(1,2**(-e))

class Alphabet:
    def __init__(self,p,lo,hi):
        self.p,self.lo,self.hi=p,lo,hi
        self.E=hi-lo+1
        self.eb=(self.E).bit_length() # ceil(log2(E+1))
        self.rb=p+self.eb+1
        self.mask=(1<<self.rb)-1
        self.b=2*self.rb
        self.top=(2-pow2(-p))*pow2(hi)
    def decode(self,c):
        f=c&((1<<self.p)-1)
        e=(c>>self.p)&((1<<self.eb)-1)
        s=-1 if c>>(self.p+self.eb) else 1
        if not 1<=e<=self.E:return F(0)
        return s*((1<<self.p)+f)*pow2(self.lo+e-1-self.p)
    def quant(self,x):
        if not x or abs(x)<pow2(self.lo):return 0,False
        s=int(x<0); x=abs(x)
        if x>=pow2(self.hi+1):
            return (s<<(self.p+self.eb)) | (self.E<<self.p) | ((1<<self.p)-1),True
        e=x.numerator.bit_length()-x.denominator.bit_length()
        if x<pow2(e):e-=1
        f=int(x/pow2(e-self.p))-(1<<self.p)
        assert self.lo<=e<=self.hi and 0<=f<(1<<self.p)
        return (s<<(self.p+self.eb))|((e-self.lo+1)<<self.p)|f,False
    def cdecode(self,c): return self.decode(c&self.mask),self.decode(c>>self.rb)
    def cquant(self,z):
        a,sa=self.quant(z[0]); b,sb=self.quant(z[1]);return a|(b<<self.rb),sa or sb

def exact_table_control():
    A=Alphabet(1,0,0) # 6 bits/complex: every padded 2-input key is affordable
    K=F(181,256)
    saturated=0; outputs=0; table=[]; canonical_count=0
    for code in range(1<<A.rb):
        v=A.decode(code); q,s=A.quant(v)
        assert not s and A.decode(q)==v
        canonical_count+=int(q==code)
    for key in range(1<<(2*A.b)):
        x=A.cdecode(key&((1<<A.b)-1)); y=A.cdecode(key>>A.b)
        result=[]; flags=[]
        for z in [(K*(x[0]+y[0]),K*(x[1]+y[1])),(K*(x[0]-y[0]),K*(x[1]-y[1]))]:
            c,s=A.cquant(z);result.append(c);flags.append(s); outputs+=1
        payload=result[0]|(result[1]<<A.b)
        assert payload < (1<<(2*A.b))
        assert [payload&((1<<A.b)-1),payload>>A.b]==result
        saturated+=any(flags);table.append(payload)
    # The maximal reachable-in-alphabet pair demonstrates why total clipping matters.
    v=A.top; c,s=A.cquant((2*K*v,F(0)))
    assert s and A.cdecode(c)==(A.top,F(0))
    # Entire dyadic grid around transitions: exact nonoverflow quantizer inequality.
    B=Alphabet(4,-4,3); cases=0
    for z in range(-16384,16385):
        x=F(z,1024); c,s=B.quant(x)
        if not s: assert abs(B.decode(c)-x)<=pow2(-B.p)*abs(x)+pow2(B.lo)
        cases+=1
    return {'complete_padded_keys':len(table),'complex_outputs':outputs,'keys_with_clipping':saturated,'canonical_real_codes':canonical_count,'exact_quantizer_grid_cases':cases,'table_payload_sha256':hashlib.sha256(json.dumps(table).encode()).hexdigest()}

def tzdiv(x,d): return x//d if x>=0 else -((-x)//d)

def recurrence_control():
    rows=[]
    for H,p in product([2,4,8,16,64,256,1024],[2,8,24]):
        v=H.bit_length()-1; Q=p+v+12; S=1<<Q
        omega=mp.e**(-2j*mp.pi/H)
        cr=int(mp.nint(mp.re(omega)*S));ci=int(mp.nint(mp.im(omega)*S))
        coeferr=abs(mp.mpc(cr,ci)/S-omega)
        assert coeferr<=mp.mpf(1)/S
        zr,zi=S,0; maximum=mp.mpf(0)
        for j in range(H):
            maximum=max(maximum,abs(mp.mpc(zr,zi)/S-omega**j))
            zr,zi=tzdiv(zr*cr-zi*ci,S),tzdiv(zr*ci+zi*cr,S)
        bound=mp.mpf(6)*H/S
        assert maximum<=bound
        rows.append({'H':H,'p':p,'Q':Q,'max_error_over_u':float(maximum*(1<<p)),'proved_bound_over_u':6/4096})
    return rows

def kernel(t,M,s):
    # np.sinc(x)=sin(pi*x)/(pi*x), handles removable zero separately.
    L=M//4;q=M//(8*s)
    return ((2*L+1)/M)*np.sinc((2*L+1)*t)/np.sinc(t)*(np.sinc((2*q+1)*t)/np.sinc(t))**s

def interpolation_control():
    rng=np.random.default_rng(987621)
    rows=[]
    for N,t in [(129,2),(193,3),(257,6)]:
        M=1<<(4*N-1).bit_length();s=16+t;h=16*s+1
        assert M>=16*s and 2*h+2<M
        L=M//4;q=M//(8*s)
        g=np.ones(2*L+1)
        for _ in range(s):g=np.convolve(g,np.ones(2*q+1)/(2*q+1))
        freq=np.arange(-L-s*q,L+s*q+1)
        assert np.max(abs(g[abs(freq)<=M//8]-1))<2e-14
        alias=np.bincount(freq%N,weights=g*g,minlength=N)
        coords=np.arange(N)*M/N
        diff=coords[:,None]-np.arange(M)[None,:]
        circ=(diff+M/2)%M-M/2
        B=np.sqrt(M/N)*kernel(circ/M,M,s)
        # Alias spectral formula against independently formed dense Gram.
        opnorm=math.sqrt(max(np.linalg.eigvalsh(B@B.T)))
        aliasnorm=math.sqrt(max(alias));assert abs(opnorm-aliasnorm)<2e-12
        r=np.floor(coords).astype(int);mask=np.zeros((N,M),dtype=bool)
        for ell in range(N):mask[ell,(r[ell]+np.arange(-h,h+2))%M]=True
        E=np.where(mask,0,B)
        tailrow=np.max(np.sum(abs(E),axis=1));tailcol=np.max(np.sum(abs(E),axis=0))
        bound=12*4.0**(-s);assert max(tailrow,tailcol)<=bound*(1+1e-9)+1e-300
        maxidentity=0
        c=(N-1)//2
        for mode in range(4):
            x=np.zeros(N,dtype=complex)
            if mode<2:x[[0,N-1][mode]]=1
            elif mode==2:x[:]=1
            else:x=rng.standard_normal(N)+1j*rng.standard_normal(N)
            v=np.zeros(M,dtype=complex);v[(np.arange(N)-c)%M]=x
            z=np.fft.fft(v)/np.sqrt(M)
            result=np.exp(-2j*np.pi*c*np.arange(N)/N)*(B@z)
            target=np.fft.fft(x)/np.sqrt(N)
            err=np.linalg.norm(result-target)/np.linalg.norm(x)
            maxidentity=max(maxidentity,err)
            assert err<2e-12
        # True fractional-offset rounding, with a full selected set of offsets.
        a=math.ceil(math.log2((2**16)*(h+2)/(2**-t)));eta=2.0**(-a)
        theta=coords-r;theta_q=np.floor(theta/eta)*eta
        Bt=np.zeros_like(B)
        for ell in range(N):
            js=np.arange(-h,h+2)
            values=kernel((theta_q[ell]-js)/M,M,s)
            values_q=np.rint(values/eta)*eta
            Bt[ell,(r[ell]+js)%M]=np.sqrt(M/N)*values_q
        perturb=Bt-np.where(mask,B,0)
        schur=math.sqrt(np.max(np.sum(abs(perturb),axis=1))*np.max(np.sum(abs(perturb),axis=0)))
        assert schur<=15*(2*h+4)*eta
        rows.append({'N':N,'M':M,'t':t,'s':s,'h':h,'a':a,'exact_identity_relative_error':maxidentity,'alias_norm':aliasnorm,'matrix_norm':opnorm,'max_row_tail':float(tailrow),'max_column_tail':float(tailcol),'proved_tail_bound':bound,'offset_rounding_schur_bound':schur,'analytic_offset_bound':15*(2*h+4)*eta,'full_offset_table_entries_not_constructed':(2*h+2)*(1<<a)})
    return rows

def budgets():
    rows=[]
    for v,t in product([8,64,256,1024,1000000],[2,8,32]):
        p=t+10+(v+1-1).bit_length() # ceil(log2 1024(v+1)/2^-t)
        u=pow2(-p);tau=pow2(-v-p);L0=2*v+1
        # After coarse replacements sqrt(2H)<=2H, same recurrence budget.
        budget=14*L0*u
        assert budget<pow2(-t)
        E=2*v+p+5;eb=E.bit_length();b=2*(p+eb+1)
        r=(v//(4*b));m=(1<<(r.bit_length()-1)) if r else 0
        assert m*b<=v//4
        rows.append({'v':v,'t':t,'p':p,'complex_code_bits':b,'m':m,'relative_budget_over_delta':float(budget/pow2(-t))})
    return rows

result={'fresh_script':str(Path(__file__)), 'supplied_programs_executed':False, 'claim_scope':'exact toy-alphabet and rational-budget controls plus high-precision/double numerical falsification; not a production eager-table executor or novelty evidence', 'toy_table':exact_table_control(),'guarded_recurrence':recurrence_control(),'interpolation':interpolation_control(),'symbolic_budgets':budgets()}
Path('research_cycle_0958/algorithms/fresh_adversarial_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','toy_table':result['toy_table'],'recurrence_cases':len(result['guarded_recurrence']),'interpolation_cases':len(result['interpolation']),'budget_cases':len(result['symbolic_budgets'])},indent=2))
