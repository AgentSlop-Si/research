"""Fresh certified sparse-modal evaluation of the original Q16 BUCKETS operator.

No predecessor module is imported. Input semantic binding is the live adapter's
job; this numerical engine consumes an exact finite Fourier-mode description.
All B output coordinates are materialized and charged. No recovery is executed.
"""
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from collections import Counter

M=1<<28; B=1<<17; T=2048; G=512; H=1536; R=57; ELL=1<<20
P=464; K=560; TERMS=128; LIMIT=2*T+H-1
MAX_SUPPORT=16; MAX_COEFFICIENT_BITS=1024
MAX_OPERATIONS=30_000_000; MAX_INTEGER_BITS=20000; MAX_SLOTS=8_000_000

class Failure(ValueError): pass

class Meter:
    def __init__(self):
        self.operations=Counter(); self.numeric_operations=0; self.bitwork=0
        self.produced=0; self.width=1; self.slots=0; self.bytecount=0
    def r(self,name,args,out):
        widths=[max(1,abs(x).bit_length()) for x in (*args,out)]
        self.width=max(self.width,*widths); self.numeric_operations+=1
        if self.width>MAX_INTEGER_BITS or self.numeric_operations>MAX_OPERATIONS:
            raise Failure('RESOURCE_LIMIT: integer arithmetic')
        self.operations[name]+=1; self.bitwork+=128*(sum(widths)+8)**2
        self.produced+=widths[-1]+1
        return out
    def add(self,a,b): return self.r('add',(a,b),a+b)
    def sub(self,a,b): return self.r('subtract',(a,b),a-b)
    def mul(self,a,b): return self.r('multiply',(a,b),a*b)
    def div(self,a,b): return self.r('floor_divide',(a,b),a//b)
    def ceil(self,a,b): return self.sub(0,self.div(self.sub(0,a),b))
    def mod(self,a,b): return self.r('modulo',(a,b),a%b)
    def shift(self,n):
        if type(n) is not int or not 0<=n<MAX_INTEGER_BITS: raise Failure('RESOURCE_LIMIT: shift')
        return self.r('binary_power',(n,),1<<n)
    def power(self,a,n):
        z=1
        while n:
            if n&1: z=self.mul(z,a)
            n=self.div(n,2)
            if n: a=self.mul(a,a)
        return z
    def event(self,name,n=1): self.operations[name]+=n
    def alloc(self,n):
        if type(n) is not int or n<0 or self.slots+n>MAX_SLOTS: raise Failure('RESOURCE_LIMIT: logical slots')
        self.slots+=n; self.event('allocated_slots',n)
    def bytes(self,n): self.bytecount+=n; self.event('source_bytes',n)
    def report(self):
        ev=sum(self.operations.values())+self.bytecount+1024
        width=self.width+ev.bit_length()+32
        controls=4096*ev*width*width
        return {'operations':dict(sorted(self.operations.items())), 'numeric_operations':self.numeric_operations,
            'max_integer_bits':self.width,'allocated_slots':self.slots,'source_bytes':self.bytecount,
            'arithmetic_bit_work_upper':self.bitwork,'control_bit_work_upper':controls,
            'total_bit_work_upper':self.bitwork+controls+(1<<75),
            'cumulative_storage_upper_bits':self.produced+4096*ev*width+(1<<42),
            'model':'schoolbook arithmetic and cumulative logical storage; not CPU/RSS',
            'fixed_dependency_loading_envelope_bitwork':1<<75,'fixed_dependency_loading_envelope_storage_bits':1<<42}

@dataclass(frozen=True)
class I:
    lo:int
    hi:int
    def __post_init__(self):
        if type(self.lo) is not int or type(self.hi) is not int or self.lo>self.hi: raise Failure('INTERNAL: interval')

class Arithmetic:
    def __init__(self,L): self.L=L; self.S=L.shift(K)
    def add(self,a,b): return I(self.L.add(a.lo,b.lo),self.L.add(a.hi,b.hi))
    def sub(self,a,b): return I(self.L.sub(a.lo,b.hi),self.L.sub(a.hi,b.lo))
    def neg(self,a): return I(self.L.sub(0,a.hi),self.L.sub(0,a.lo))
    def scale(self,a,n):
        x=self.L.mul(a.lo,n); y=self.L.mul(a.hi,n)
        return I(min(x,y),max(x,y))
    def divide_integer(self,a,d): return I(self.L.div(a.lo,d),self.L.ceil(a.hi,d))
    def mul(self,a,b):
        products=[self.L.mul(x,y) for x in (a.lo,a.hi) for y in (b.lo,b.hi)]
        self.L.alloc(4)
        return I(self.L.div(min(products),self.S),self.L.ceil(max(products),self.S))
    def quotient(self,a,b):
        if b.lo<=0: raise Failure('CERTIFICATE: denominator')
        lo=[];hi=[];self.L.alloc(8)
        for x in (a.lo,a.hi):
            for y in (b.lo,b.hi):
                n=self.L.mul(x,self.S); lo.append(self.L.div(n,y));hi.append(self.L.ceil(n,y))
        return I(min(lo),max(hi))
    def clip(self,a,low,high):
        if a.hi<low or a.lo>high: raise Failure('CERTIFICATE: disjoint analytic interval')
        self.L.event('analytic_interval_intersection')
        return I(max(low,a.lo),min(high,a.hi))
    def positive_power(self,a,n):
        if a.lo<0: raise Failure('INTERNAL: nonnegative power')
        z=I(self.S,self.S)
        while n:
            if n&1: z=self.mul(z,a)
            n=self.L.div(n,2)
            if n: a=self.mul(a,a)
        return self.clip(z,0,self.S)

class Sine:
    def __init__(self,A):
        self.A=A;self.L=A.L;self.S=A.S; L=self.L;S=self.S
        def atan(q):
            lo=hi=0; qp=q; q2=L.mul(q,q); terms=K+8
            for j in range(terms):
                d=L.mul(L.add(L.mul(2,j),1),qp)
                a=L.div(S,d);b=L.ceil(S,d)
                if j&1:lo=L.sub(lo,b);hi=L.sub(hi,a)
                else:lo=L.add(lo,a);hi=L.add(hi,b)
                qp=L.mul(qp,q2);L.event('machin_atan_term')
            tail=L.ceil(S,L.mul(2*terms+1,qp))
            return I(lo,L.add(hi,tail)) # terms even; next term positive.
        self.pi=A.sub(A.scale(atan(5),16),A.scale(atan(239),4))
        if not 3*S<self.pi.lo<=self.pi.hi<4*S: raise Failure('CERTIFICATE: pi')
        fac=1
        for j in range(2,258):fac=L.mul(fac,j);L.event('shared_factorial_step')
        self.tail=L.ceil(L.shift(K+257),fac)
        if self.tail>1:raise Failure('CERTIFICATE: Taylor tail')
    def sin_pi(self,p,q):
        L=self.L;S=self.S;A=self.A
        if type(p) is not int or type(q) is not int or q<=0:raise Failure('DOMAIN: sine argument')
        a=L.mod(p,L.mul(2,q));sign=1
        if a>q:a=L.sub(2*q,a);sign=-1
        if L.mul(2,a)>q:a=L.sub(q,a)
        L.event('sine_evaluation')
        if not a:L.event('exact_zero_sine');return I(0,0)
        if 2*a==q:L.event('exact_unit_sine');return I(sign*S,sign*S)
        lo=L.div(L.mul(self.pi.lo,a),q);hi=L.ceil(L.mul(self.pi.hi,a),q)
        x=L.div(L.add(lo,hi),2); rad=max(L.sub(x,lo),L.sub(hi,x))
        if not 0<=x<=2*S:raise Failure('CERTIFICATE: reduced angle')
        xx=L.mul(x,x);SS=L.mul(S,S);tl=th=sl=sh=x
        for j in range(1,TERMS):
            den=L.mul(SS,L.mul(2*j,2*j+1))
            tl=L.div(L.mul(tl,xx),den);th=L.ceil(L.mul(th,xx),den)
            if j&1:sl=L.sub(sl,th);sh=L.sub(sh,tl)
            else:sl=L.add(sl,tl);sh=L.add(sh,th)
            L.event('sine_taylor_term')
        margin=L.add(rad,self.tail);out=I(L.sub(sl,margin),L.add(sh,margin))
        if sign<0:out=A.neg(out)
        return A.clip(out,-S,S)
    def phase(self,n,tau):
        u=self.L.mod(self.L.mul(n,tau),M)
        return self.sin_pi(M+4*u,2*M),self.A.neg(self.sin_pi(2*u,M))

def nearest(n,d,L):
    a=L.div(n,d); rem=L.sub(n,L.mul(a,d));twice=L.mul(2,rem)
    L.event('nearest_even')
    return L.add(a,1) if twice>d or (twice==d and a&1) else a

@dataclass(frozen=True)
class Result:
    numerators:tuple
    bits:int
    certificates:tuple
    source_entries:tuple
    alpha_power:int
    sigma:int
    tau:int
    tail_grid_units:int
    active_bins:tuple

class SparseBucketEngine:
    def __init__(self):
        L=self.ledger=Meter();L.bytes(len(Path(__file__).read_bytes()))
        self.A=A=Arithmetic(L);self.sine=Sine(A);S=A.S
        beta=Fraction(5,56);m=28
        ceil=lambda p,q:(p+q-1)//q
        k=1<<ceil(2*beta.numerator*m,beta.denominator)
        expected_B=1<<ceil((beta.denominator+2*beta.numerator)*m,2*beta.denominator)
        if not (beta*m>=2 and 0<beta<Fraction(1,2) and M==1<<m and B==expected_B and B>=4096*k and M%B==0 and M//B==T and T>=4 and R==2*m+1 and P==16*m+16 and 2*R*(ELL-1)+1<M):
            raise Failure('DOMAIN: full theorem window guards')
        L.event('all_theorem_window_guards_checked')
        if L.mul(2*H+1,L.power(M,4))>L.power(16,R):raise Failure('CERTIFICATE: window delta')
        self.tail_den=L.power(20,2*R)
        if L.mul(3073,L.shift(480))>=self.tail_den:raise Failure('CERTIFICATE: far tail <2^-480')
        period=M//ELL
        self.num_sines=tuple(self.sine.sin_pi(a,period) for a in range(period//2+1));L.alloc(3*len(self.num_sines))
        L.event('numerator_root_preparation',len(self.num_sines))
        prefix=[I(S,S)];L.alloc(3)
        for d in range(1,LIMIT+1):
            rem=L.mod(d,period);rem=min(rem,period-rem)
            num=self.num_sines[rem]
            if num.lo==num.hi==0:phi=I(0,0);L.event('exact_zero_phi')
            else:
                den=A.scale(self.sine.sin_pi(d,M),ELL)
                ratio=A.clip(A.quotient(num,den),0,S)
                phi=A.positive_power(ratio,2*R)
            prefix.append(A.add(prefix[-1],phi));L.alloc(3);L.event('phi_evaluation')
        self.prefix=tuple(prefix);L.alloc(len(prefix))
        self.C=A.add(I(S,S),A.scale(self.range_sum(1,G),2))
        if self.C.lo<S:raise Failure('CERTIFICATE: normalizer >=1')
        self.windows={};L.event('engine_preparation')
    def range_sum(self,a,b):
        if not 0<=a<=b<=LIMIT:raise Failure('INTERNAL: prefix range')
        return self.prefix[b] if a==0 else self.A.sub(self.prefix[b],self.prefix[a-1])
    def window(self,d):
        if type(d) is not int or not 0<=d<2*T:raise Failure('DOMAIN: retained window shift')
        if d not in self.windows:
            A=self.A
            if d>=H:z=self.range_sum(d-H,d+H)
            else:z=A.add(I(A.S,A.S),A.add(self.range_sum(1,H-d),self.range_sum(1,H+d)))
            self.windows[d]=A.clip(A.quotient(z,self.C),0,(2*H+1)*A.S)
            self.ledger.alloc(4);self.ledger.event('shifted_window_evaluation')
        return self.windows[d]
    def run(self,entries,h,sigma,tau):
        L=self.ledger;A=self.A;S=A.S
        if type(entries) is not tuple or not 1<=len(entries)<=MAX_SUPPORT:raise Failure('DOMAIN: sparse support cap')
        if any(type(v)is not int for v in (h,sigma,tau)) or not 0<=h<=1028 or not 0<sigma<M or not sigma&1 or not 0<=tau<M:raise Failure('DOMAIN: normalization or bucket schedule')
        prev=-1;norm=0;l1=0
        for row in entries:
            if type(row)is not tuple or len(row)!=3 or any(type(v)is not int for v in row):raise Failure('GRAMMAR: exact sparse entries')
            n,re,im=row
            if not prev<n<M or n<0 or (re==0 and im==0) or max(abs(re).bit_length(),abs(im).bit_length())>MAX_COEFFICIENT_BITS:raise Failure('DOMAIN: canonical sparse entries')
            norm=L.add(norm,L.add(L.mul(re,re),L.mul(im,im))); l1=L.add(l1,abs(re)+abs(im));prev=n
        alpha=L.shift(h)
        if not L.mul(alpha,alpha)>=norm or not L.mul(4,norm)>L.mul(alpha,alpha):raise Failure('DOMAIN: norm in (1/2,1]')
        # Every omitted complex contribution is bounded by eta*|c|/alpha.
        # Component l1 is an exact upper bound on complex magnitude.
        tail=L.ceil(L.mul(L.mul(2*H+1,l1),S),L.mul(self.tail_den,alpha))
        U=L.shift(K-P)
        if tail>=U:raise Failure('CERTIFICATE: tail exceeds output budget')
        accum={}; retained=[]
        for n,re,im in entries:
            phre,phim=self.sine.phase(n,tau)
            cr=A.divide_integer(A.sub(A.scale(phre,re),A.scale(phim,im)),alpha)
            ci=A.divide_integer(A.add(A.scale(phim,re),A.scale(phre,im)),alpha)
            shift=L.mod(L.mul(sigma,n),M);base=(-shift)//T
            for off in range(-2,3):
                j=L.mod(base+off,B);q=L.mod(L.add(L.mul(j,T),shift),M);d=min(q,M-q)
                L.event('candidate_shift_checked')
                if d>=2*T:continue
                w=self.window(d);old=accum.get(j,(I(0,0),I(0,0)))
                accum[j]=(A.add(old[0],A.mul(w,cr)),A.add(old[1],A.mul(w,ci)))
                retained.append((n,j,d));L.alloc(12);L.event('retained_modal_contribution')
        cert=[];values={}
        for j,(re,im) in sorted(accum.items()):
            qr=nearest(L.add(re.lo,re.hi),2*U,L);qi=nearest(L.add(im.lo,im.hi),2*U,L)
            er=max(abs(L.sub(L.mul(qr,U),re.lo)),abs(L.sub(L.mul(qr,U),re.hi)))
            ei=max(abs(L.sub(L.mul(qi,U),im.lo)),abs(L.sub(L.mul(qi,U),im.hi)))
            if L.add(L.mul(er,er),L.mul(ei,ei))>L.mul(L.sub(U,tail),L.sub(U,tail)):
                raise Failure('CERTIFICATE: complex radius plus omitted tail')
            values[j]=(qr,qi);cert.append((j,qr,qi,re.lo,re.hi,im.lo,im.hi,er,ei));L.alloc(12)
        outputs=[];L.alloc(B)
        for j in range(B):
            outputs.append(values.get(j,(0,0)));L.alloc(3);L.event('bucket_output')
        out=tuple(outputs);L.alloc(B)
        self.last_retained=tuple(retained);L.alloc(4*len(retained))
        L.event('sparse_buckets_call')
        return Result(out,P,tuple(cert),entries,h,sigma,tau,tail,tuple(sorted(accum)))
