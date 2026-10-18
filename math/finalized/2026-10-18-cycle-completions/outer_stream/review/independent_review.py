"""Reviewer-authored full-stream verification, independent from candidate tests/oracle."""
from fractions import Fraction as Q
from pathlib import Path
from math import isqrt, factorial
from dataclasses import replace
import sys, json, hashlib, random
HERE=Path(__file__).resolve().parent
SOURCE=Path(__file__).resolve().parent.parent / 'candidate'
sys.path.insert(0,str(HERE/'runtime'))
from outer_wrapper import Header, Outer, ReceiptLedger
from sparse_output import produce_medians
from full_transfer import FullTransfer, TransferConfig, TransferContractError, OuterDenseRequired, round_div_pow2, exact_complex_product

B=320;U=1<<B

def ceilq(a,b):
    return -((-a)//b)

def iadd(x,y):
    return x[0]+y[0],x[1]+y[1]

def isub(x,y):
    return x[0]-y[1],x[1]-y[0]

def imul(x,y):
    z=[a*b for a in x for b in y]
    return min(z)//U,ceilq(max(z),U)

def iscale(x,a,b=1):
    assert b>0
    z=(x[0]*a,x[1]*a)
    return min(z)//b,ceilq(max(z),b)

def idiv(x,y,normalization):
    assert y[0]>0 and normalization>0
    z=[Q(a*U,normalization*b) for a in x for b in y]
    return min(z).__floor__(),max(z).__ceil__()

def ipow(x,n):
    z=[Q(v,U)**n for v in x]
    if n%2==0 and x[0]<=0<=x[1]:z.append(Q(0))
    return (min(z)*U).__floor__(),(max(z)*U).__ceil__()

def build_pi():
    intervals=[]
    for d,mult in ((3,8),(7,4)):
        s=sum((Q((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(140)),Q())
        e=Q(1,281*d**281)
        intervals.append((mult*s,mult*(s+e)))
    return (sum(v[0] for v in intervals)*U).__floor__(),(sum(v[1] for v in intervals)*U).__ceil__()

class Truth:
    def __init__(self,N,M,D):
        self.N,self.M,self.s=N,M,D*(M.bit_length()-1)
        self.pi=build_pi()
        z=isqrt(M*U*U//N)
        assert z*z*N<=M*U*U<(z+1)*(z+1)*N
        self.root=z,z+1
        self.tail=ceilq((1<<129)*U,factorial(129))
        assert self.tail==1
        self.calls=0
    def sin(self,a):
        a=a%2
        if a>1:
            value=self.sin(2-a)
            return -value[1],-value[0]
        if a>Q(1,2):a=1-a
        if a==0:return 0,0
        if a==Q(1,2):return U,U
        x=iscale(self.pi,a.numerator,a.denominator)
        assert 0<=x[0]<=x[1]<2*U
        square=imul(x,x)
        term=x;answer=x
        # Includes all powers 1,3,...,127. Through degree 128 the remaining
        # Taylor error is bounded by 2**129/129! for the entire angle interval.
        for j in range(1,64):
            term=iscale(imul(term,square),1,(2*j)*(2*j+1))
            answer=isub(answer,term) if j%2 else iadd(answer,term)
        return answer[0]-self.tail,answer[1]+self.tail
    def coefficient(self,ell,k):
        self.calls+=1
        N,M,s=self.N,self.M,self.s
        f=Q(ell,N)-Q(k,M)
        f%=1
        if not f:
            v=Q(M//2+1,M)
            first=((v*U).__floor__(),(v*U).__ceil__())
            ratio=U,U
        else:
            den=self.sin(f)
            first=idiv(self.sin((M//2+1)*f),den,M)
            q=M//(8*s)
            ratio=idiv(self.sin((2*q+1)*f),den,2*q+1)
        amplitude=imul(imul(first,ipow(ratio,s)),self.root)
        phase=Q(2*((N-1)//2)*ell,N)
        return imul(amplitude,self.sin(Q(1,2)-phase)),imul(amplitude,self.sin(-phase))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def hashes():
    manifest=json.loads((SOURCE/'MANIFEST.json').read_text())
    for path,entry in manifest['files'].items():
        data=(SOURCE/path).read_bytes()
        assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],path
    bindings=json.loads((SOURCE/'SOURCE_BINDINGS.json').read_text())
    for key,entry in bindings.items():
        data=(SOURCE/entry['source_path']).read_bytes()
        assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],key
    for path in (HERE/'runtime').glob('*.py'):
        assert path.read_bytes()==(SOURCE/path.name).read_bytes()
    return {'manifest_sha256':sha(SOURCE/'MANIFEST.json'),'manifest_files':len(manifest['files']),'source_pins':len(bindings)}

def make(N,ks,rows,D=5,P=None,L=None):
    M=1<<(4*N-1).bit_length();m=M.bit_length()-1
    P=16*m+16 if P is None else P
    L=ReceiptLedger() if L is None else L
    run=produce_medians(M,P,ks,rows,L)
    return Outer(Header(N,M,D,P),run,L)

def rejects(fn,kind=ValueError):
    try:fn()
    except kind as e:return str(e)
    raise AssertionError('rejection missing')

def check_fixture(N,ks,rows,cfg):
    outer=make(N,ks,rows)
    true_medians=tuple((k,(sorted(row[j][0] for row in rows)[len(rows)//2],sorted(row[j][1] for row in rows)[len(rows)//2])) for j,k in enumerate(ks))
    assert outer.binding.output.pairs==true_medians
    prefix=outer.ledger.report()
    transfer=FullTransfer(outer,cfg)
    out=transfer.run();assert transfer.validate_output(out) is out
    assert len(out.pairs)==N and transfer.state=='COMPLETE'
    G=outer.binding.geometry;P=outer.binding.header.estimate_bits
    truth=Truth(N,G.M,G.D)
    coefficients=0;max_terms=0;ratios=[];intervals=[];signed_terms=0
    for ell,(real,imag) in enumerate(out.pairs):
        center=ell*G.M//N
        active={ (center+offset)%G.M for offset in range(-G.h,G.h+2) }
        assert len(active)==G.t
        sums=((0,0),(0,0));l1=0;count=0
        for k,(a,b) in true_medians:
            if k not in active:continue
            cr,ci=truth.coefficient(ell,k)
            real_interval=isub(iscale(cr,a),iscale(ci,b))
            imag_interval=iadd(iscale(ci,a),iscale(cr,b))
            sums=iadd(sums[0],real_interval),iadd(sums[1],imag_interval)
            l1+=abs(a)+abs(b);count+=1;coefficients+=1
            signed_terms+=int(cr[1]<0 or ci[1]<0)
        max_terms=max(max_terms,count)
        scaled_out=(Q(real,1<<out.bits)/(Q(2)**cfg.scale_power),Q(imag,1<<out.bits)/(Q(2)**cfg.scale_power))
        radii=[max(abs(scaled_out[j]-Q(v,U*(1<<P))) for v in sums[j]) for j in (0,1)]
        err2=radii[0]**2+radii[1]**2
        bound=Q(l1,1<<(P+(G.D+3)*G.m))+Q(1,1<<out.normalized_bits)
        assert err2<=bound*bound,(ell,err2,bound)
        ratios.append(err2/(bound*bound))
        intervals.append({'ell':ell,'count':count,'real':sums[0],'imag':sums[1]})
    assert coefficients==out.incidences==transfer.coefficients_evaluated==truth.calls
    assert coefficients==sum(r1-r0 for r0,r1,_ in outer.binding.endpoints)
    assert max_terms==out.max_row_terms
    assert out.max_accumulator_abs<(1<<(out.accumulator_signed_bits-1))
    paid=outer.kernel.paid
    assert paid.operations['coefficient_call']==paid.operations['certificate_pass']==coefficients
    assert paid.operations['pi_setup']==paid.operations['sqrt_setup']==1
    assert outer.ledger.events>prefix['events'] and outer.ledger.bit_work>prefix['bit_work']
    # Audit storage: result has N rows; production retains no E-record collection.
    assert not any(isinstance(v,(list,tuple)) and len(v)==coefficients for v in vars(outer).values())
    before=outer.ledger.events
    rejects(transfer.run)
    assert outer.ledger.events>before and transfer.state=='COMPLETE'
    rejects(lambda:transfer.validate_output(replace(out,bits=out.bits+1)))
    maxratio=max(ratios)
    (HERE/f'TRUTH_{N}.json').write_text(json.dumps({'bits':B+P,'rows':intervals},indent=2)+'\n')
    return out,{'N':N,'M':G.M,'D':G.D,'coefficients':coefficients,'rows':N,'oracle_bits':B,'signed_coordinate_terms':signed_terms,'max_row_terms':max_terms,'max_error_ratio_squared':{'numerator':maxratio.numerator,'denominator':maxratio.denominator},'max_accumulator_abs':out.max_accumulator_abs,'accumulator_signed_bits':out.accumulator_signed_bits,'output_bits':out.bits,'normalized_bits':out.normalized_bits,'scale_power':out.scale_power,'output_sha256':hashlib.sha256(json.dumps(out.pairs).encode()).hexdigest(),'prefix_receipt':prefix,'final_receipt':transfer.receipt()}

def controls():
    L=ReceiptLedger();rng=random.Random(618031);rounds=ties=products=0
    for shift in range(13):
        for n in range(-129,130):
            x=Q(n,1<<shift);a=x.__floor__();b=x.__ceil__()
            expected=min({a,b},key=lambda v:(abs(x-v),v%2))
            assert round_div_pow2(n,shift,L)==expected
            rounds+=1;ties+=int(a!=b and abs(x-a)==abs(x-b))
    for _ in range(2000):
        shift=rng.randrange(0,400);n=rng.randrange(-(1<<512),1<<512)
        x=Q(n,1<<shift);a=x.__floor__();b=x.__ceil__()
        expected=min({a,b},key=lambda v:(abs(x-v),v%2))
        assert round_div_pow2(n,shift,L)==expected;rounds+=1
        a,b,c,d=(rng.randrange(-(1<<320),1<<320) for j in range(4))
        real,imag=exact_complex_product(a,b,c,d,L)
        # Independent identities derive real/imag via sum and difference products.
        assert 2*real==(a+b)*(c-d)+(a-b)*(c+d)
        assert 2*imag==(a+b)*(c+d)-(a-b)*(c-d)
        products+=1
    classification=0
    for m in range(2,151):
        threshold=((1<<m)-5)//(32*m)
        for D in {5,6,7,11,99,max(5,threshold),max(5,threshold+1)}:
            assert (32*D*m+4<(1<<m))==(D<=threshold)
            assert 32*D*m+4!=(1<<m)
            assert Q(32*D*(m+1)+4,1<<(m+1))<Q(32*D*m+4,1<<m)
            classification+=1
    assert min(m for m in range(2,50) if 160*m+4<(1<<m))==11
    N,M,h=256,1024,801
    start=ceilq(-N*(h+1),M);stop=ceilq(N*(h+1),M)
    rr=[r%N for r in range(start,stop)]
    assert (start,stop,len(rr),len(set(rr)))==(-200,201,401,256)
    empty=make(257,(),((),))
    e=FullTransfer(empty,TransferConfig(1,8,-11,1)).run()
    assert e.bits==35 and e.pairs==((0,0),)*257 and empty.kernel is None
    malformed=[]
    for N in (1,2,3,7,63,128,255,256):
        o=make(N,(),((),))
        message=rejects(lambda:FullTransfer(o,TransferConfig(1,8,0,1)),OuterDenseRequired)
        assert o.kernel is None
        malformed.append({'case':f'dense N={N}','message':message})
    cap=3*2048*2048*(1<<192)
    for a,b in ((cap,0),(-cap,0),(0,cap),(0,-cap),(1<<20000,0)):
        o=make(257,(0,),(((a,b),),));before=o.ledger.report()
        message=rejects(lambda:FullTransfer(o,TransferConfig(1,8,0,1)))
        assert o.kernel is None and o.ledger.events>before['events']
        malformed.append({'case':'cap width '+str(max(abs(a).bit_length(),abs(b).bit_length())),'message':message})
    for cfg in (TransferConfig(0,3,0,1),TransferConfig(1,2,0,1),TransferConfig(1,-3,0,1),TransferConfig(1,3,0,0),TransferConfig(1,3,12,1),TransferConfig(1,3,True,1)):
        o=make(257,(),((),));rejects(lambda:FullTransfer(o,cfg));assert o.kernel is None
    # Arbitrarily wide original rows may have small medians: retention and replay
    # must be genuine, and paid at the original width, without rejecting the median.
    wide=1<<20000
    rows=(((-wide,wide),),((0,0),),((wide,-wide),))
    o=make(257,(0,),rows)
    assert o.binding.output.pairs==((0,(0,0)),) and o.ledger.max_bits>=20001
    assert o.binding.run._origin.rows is rows
    # Wide beta encoding is accepted and paid, not mistaken for a fixed encoding.
    o=make(257,(),((),));cfg=TransferConfig(1<<12000,8<<12000,0,1)
    t=FullTransfer(o,cfg);assert t.b==24 and o.ledger.max_bits>=12004
    # Old cumulative counters remain present in observations and future charges.
    L2=ReceiptLedger();L2.events=1<<1000;L2.bit_work=1<<1500;L2.produced_bits=1<<1400
    prior=L2.report();o=make(257,(),((),),L=L2)
    t=FullTransfer(o,TransferConfig(1,8,0,1));t.run()
    assert L2.events>prior['events'] and L2.bit_work>prior['bit_work'] and L2.produced_bits>prior['produced_bits']
    # Failure mutations only affect disposable harness-owned objects. Production
    # runtime copies remain untouched. Full coverage and binding checks must reject.
    mutations=[]
    for mode in ('drop_first','drop_middle','drop_last','repeat_first','reorder_first','foreign_source','changed_grid','changed_value'):
        o=make(257,(0,),(((0,0),),));orig=o.incidences;coefficient=o.coefficient
        if mode in ('foreign_source','changed_grid','changed_value'):
            if mode=='foreign_source':
                foreign=make(257,(0,),(((0,0),),));fi=next(foreign.incidences());fr=foreign.coefficient(fi)
                o.coefficient=lambda inc:fr
            elif mode=='changed_grid':o.coefficient=lambda inc:replace(coefficient(inc),p=92)
            else:o.coefficient=lambda inc:replace(coefficient(inc),real=1+coefficient(inc).real)
        else:
            def stream(mode=mode,orig=orig):
                it=iter(orig())
                if mode=='drop_first':next(it);yield from it
                elif mode=='drop_middle':
                    for j,inc in enumerate(it):
                        if j!=4:yield inc
                elif mode=='drop_last':
                    previous=next(it)
                    for inc in it:yield previous;previous=inc
                elif mode=='repeat_first':
                    first=next(it);yield first;yield first;yield from it
                else:
                    first=next(it);second=next(it);yield second;yield first;yield from it
            o.incidences=stream
        t=FullTransfer(o,TransferConfig(1,8,0,1));pre=o.ledger.events
        message=rejects(t.run)
        assert t.state=='FAILED' and t.output is None and o.ledger.events>pre
        mutations.append({'case':mode,'coefficients_evaluated':t.coefficients_evaluated,'message':message,'events':o.ledger.events})
    return {'signed_rounds':rounds,'exact_signed_ties':ties,'wide_exact_products':products,'classification_cases':classification,'dense_witness':{'lifts':401,'rows':256},'empty_rows':257,'wide_original_row_bits':20001,'wide_beta_bits':12004,'prior_counter_bits':1001,'malformed':malformed,'mutations':mutations,'control_receipt':L.report()}

def main():
    pin=hashes()
    N=257;M=2048;P=192;cap=3*M*M*(1<<P)
    pairs=((cap-17,-cap+19),(-cap+23,cap-29),(0,0),((1<<P)//3,-((1<<P)//5)))
    # Parenthesization matches exact intended -unit//5 from the candidate fixture.
    pairs=pairs[:-1]+(((1<<P)//3,(-(1<<P))//5),)
    rows=tuple(tuple((a+dr,b+di) for a,b in pairs) for dr,di in ((-3,5),(0,0),(7,-2)))
    first,fr=check_fixture(N,(0,1,1024,2047),rows,TransferConfig(1,8,31,3))
    author=json.loads((SOURCE/'RESULTS.json').read_text())
    assert [list(v) for v in first.pairs]==author['full_fixture']['output_pairs']
    assert fr['coefficients']==885 and first.bits==0
    second,sr=check_fixture(512,(0,),((((1<<P),0),),),TransferConfig(1,4,-17,2))
    assert sr['coefficients']==441 and second.bits==42
    assert Q(second.pairs[0][0],1<<second.bits)==Q(1025,1<<27) and second.pairs[0][1]==0
    assert sr['output_sha256']==author['negative_scale_fixture']['output_sha256']
    evidence={'verdict':'PASS','pins':pin,'primary':fr,'secondary':sr,'controls':controls()}
    assert hashes()==pin
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({'verdict':'PASS','primary_coefficients':885,'primary_rows':257,'secondary_coefficients':441,'secondary_rows':512,'independent_oracle_bits':B}))

if __name__=='__main__':main()
