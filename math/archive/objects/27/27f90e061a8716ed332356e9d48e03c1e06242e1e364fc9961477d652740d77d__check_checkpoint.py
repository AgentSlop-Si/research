"""Independent checkpoint audit; reads uploaded JSON/text only, imports no upload.
All algorithmic code here is authored for this audit from the mathematical specification.
"""
from pathlib import Path
from fractions import Fraction as F
import math, cmath, random, hashlib, json, itertools, argparse
ROOT=None
OUT=Path(__file__).resolve().parent

def rnd(n,d):
    q,r=divmod(abs(n),d)
    v=q+(2*r>=d)
    return -v if n<0 else v

def atan_interval(q,precision):
    s=F(0); n=0
    while True:
        t=F(1,(2*n+1)*q**(2*n+1))
        if t<F(1,2**precision):
            z=s+(-t if n%2 else t)
            return min(s,z),max(s,z)
        s += (-t if n%2 else t); n+=1

a,b=atan_interval(5,300); c,d=atan_interval(239,300)
PI_LO,PI_HI=16*a-4*d,16*b-4*c
assert 3<PI_LO<PI_HI<F(22,7)

def fixed_pi(P):
    u=(128*(P+1)**2).bit_length(); scale=1<<(P+u)
    parts=[]
    for q in (5,239):
        total=0;n=0
        while True:
            term=scale//((2*n+1)*q**(2*n+1))
            if not term:break
            total+=(-term if n%2 else term);n+=1
        parts.append(total)
    p=rnd(16*parts[0]-4*parts[1],1<<u)
    assert max(abs(F(p,1<<P)-PI_LO),abs(F(p,1<<P)-PI_HI))<F(1,1<<P)
    return p

def grid(Q,bits,certify=False):
    deg=next(k for k in range(1,1000) if F(4**(k+1),math.factorial(k+1))<=F(1,2**(bits+4)))
    P=bits+(256*(deg+1)).bit_length()+4;S=1<<P;p=fixed_pi(P); result=[]; worst=F(0)
    for a in range(Q):
        a=a-Q if 2*a>Q else a
        theta=rnd(2*p*a,Q); re,im=S,0; sr,si=S,0
        exact_re,exact_im=F(1),F(0); er,ei=F(1),F(0)
        for k in range(1,deg+1):
            re,im=rnd(-im*theta,S*k),rnd(re*theta,S*k)
            sr+=re;si+=im
            if certify:
                er,ei=-ei*theta/F(S*k),er*theta/F(S*k)
                exact_re+=er;exact_im+=ei
        if certify:
            rounding=abs(F(sr,S)-exact_re)+abs(F(si,S)-exact_im)
            phase=max(abs(F(theta,S)-2*a*PI_LO/Q),abs(F(theta,S)-2*a*PI_HI/Q))
            remainder=F(4**(deg+1),math.factorial(deg+1))
            total=rounding+phase+remainder
            assert total<F(1,1<<bits),(bits,Q,a,float(total))
            worst=max(worst,total)
        result.append((sr,si))
    return result,S,{'bits':bits,'Q':Q,'degree':deg,'precision':P,'max_exact_certificate':float(worst),'bound':2.**(-bits)}

def packed_case(n,K,B,Q0,Q1,g,H,w,seed):
    rng=random.Random(seed); G=K//g;r=(2*H*G).bit_length(); ell=w//r
    assert ell>0
    ph,S,_=grid(Q1,24);D=Q0*Q1
    table=[]; scalars=[]
    for ds in itertools.product(range(D),repeat=g):
        # Product order differs from numeric key order: assign explicitly below.
        key=sum(desc*D**pos for pos,desc in enumerate(ds))
        lanes=[]
        for t in range(B):
            vals=[ph[((desc%Q0)*(Q1//Q0)+t*(desc//Q0))%Q1] for desc in ds]
            lanes.append(tuple(max(-H,min(H,rnd(H*sum(x[c] for x in vals),g*S))) for c in (0,1)))
        packed=[[],[]]
        for c in (0,1):
            for a in range(0,B,ell):
                packed[c].append(sum((lanes[t][c]+H) << (r*(t-a)) for t in range(a,min(B,a+ell))))
        while len(table)<=key:table.append(None);scalars.append(None)
        table[key]=packed;scalars[key]=lanes
    assert len(table)==D**g and all(v is not None for v in table)
    rows=len(table); nchecks=0;max_error=0.;maxword=0
    for mode in range(7):
        samples=[(rng.randrange(n),rng.randrange(4)) for _ in range(K)]
        if mode==0:samples=[(n-1,3)]*K
        if mode==1:samples=[(0,k%4) for k in range(K)]
        if mode==2:samples=[(n//2,2*(k%2)) for k in range(K)]
        outputs=[]
        for m0 in range(0,n,B):
            keys=[]
            for a in range(0,K,g):
                ds=[]
                for j,sgn in samples[a:a+g]:
                    start=(sgn*(Q0//4)-rnd(Q0*(j*m0%n),n))%Q0
                    slope=(-rnd(Q1*j,n))%Q1
                    ds.append(start+Q0*slope)
                keys.append(sum(v*D**p for p,v in enumerate(ds)))
            total=[[0]*len(table[0][0]) for _ in (0,1)]
            for key in keys:
                for c in (0,1):
                    for z in range(len(total[c])):
                        total[c][z]+=table[key][c][z]
                        assert total[c][z]<1<<w
                        maxword=max(maxword,total[c][z].bit_length())
            for t in range(min(B,n-m0)):
                coord=[]
                for c in (0,1):
                    z,lane=divmod(t,ell)
                    val=((total[c][z]>>(r*lane))% (1<<r))-G*H
                    assert val==sum(scalars[key][t][c] for key in keys)
                    coord.append(val/(G*H))
                outputs.append(complex(*coord))
        target=[sum((1j)**sgn*cmath.exp(-2j*math.pi*j*m/n) for j,sgn in samples)/K for m in range(n)]
        error=max(abs(x-y) for x,y in zip(outputs,target));max_error=max(max_error,error)
        bound=math.pi/Q0+math.pi*(B-1)/Q1+2**-24+math.sqrt(2)/(2*H)
        assert error<=bound+1e-11
        nchecks+=n
    return {'N':n,'K':K,'B':B,'g':g,'table_rows':rows,'word_bits':w,'max_packed_bits':maxword,'words_per_row':len(table[0][0]),'outputs':nchecks,'max_error':max_error,'bound':bound}

def metadata():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())['files'];mismatch=[]
    for p,hash_ in manifest.items():
        if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=hash_:mismatch.append(p)
    assert not mismatch
    validation=json.loads((ROOT/'VALIDATION.json').read_text())
    for v in validation['audits']:
        assert hashlib.sha256((ROOT/v['result']).read_bytes()).hexdigest()==v['sha256']
        assert json.loads((ROOT/v['result']).read_text())['status']=='PASS'
    source_checks=[]
    for path in ROOT.rglob('*.json'):
        if 'materials' in path.parts:continue
        obj=json.loads(path.read_text())
        if not isinstance(obj,dict):continue
        for tag,val in obj.items():
            if isinstance(val,dict) and ('sha256' in tag or tag=='source_hashes'):
                for ref,expected in val.items():
                    candidates=[path.parent/ref,ROOT/ref]
                    for candidate in candidates:
                        if candidate.is_file():
                            assert hashlib.sha256(candidate.read_bytes()).hexdigest()==expected,(path,ref)
                            source_checks.append([str(path.relative_to(ROOT)),ref]);break
        for tag,target in [('reviewed_source_sha256','fft_wordram_decoder_research/guarded_decoder.py'),('reviewed_sampler_sha256','fft_wordram_integration/sampling.py')]:
            if tag in obj and path.parent.name=='fft_wordram_review_research':
                assert hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==obj[tag];source_checks.append([str(path.relative_to(ROOT)),target])
    for src,result,field in [
        ('fft_wordram_decoder_research/guarded_decoder.py','fft_wordram_decoder_research/results.json','source_sha256'),
        ('fft_bidirectional_graph_research/affine_cycle.py','fft_bidirectional_graph_research/results.json','source_sha256'),
        ('fft_bidirectional_graph_research/affine_cycle.py','fft_bidirectional_graph_research/independent_results.json','source_sha256'),
        ('fft_bidirectional_graph_research/run_audit.py','fft_bidirectional_graph_research/independent_results.json','author_audit_sha256')]:
        expected=json.loads((ROOT/result).read_text())[field]
        assert hashlib.sha256((ROOT/src).read_bytes()).hexdigest()==expected
        source_checks.append([result,src])
    assert len(source_checks)==validation['matched_source_hash_checks']==17
    assert sorted({src for result,src in source_checks}) != []
    integ=json.loads((ROOT/'fft_wordram_integration/results.json').read_text())
    assert len(integ['records'])==24 and sum(r['N'] for r in integ['records'])==10760
    assert max(r['total_error_over_mass'] for r in integ['records'])==integ['max_observed_total_error_over_mass']
    for r in integ['records']:
        assert r['total_error_over_mass']<=r['sampling_error_over_mass']+r['decoder_error_over_mass']+1e-12
        assert r['decoder_error_over_mass']<=r['decoder_error_bound']
        p=r['parameters']; assert p['materialized_table_rows']==p['possible_table_rows']==16384
    return {'manifest_files':len(manifest),'validation_result_hashes':len(validation['audits']),'additional_source_hash_bindings':len(source_checks),'integration_records_consistent':24}

def sampler_checks():
    cases=0;ticket_cases=0
    # Exhaustive exact probability of each accepted ticket, with finite rejection cap.
    for L in range(1,65):
        b=(L-1).bit_length();universe=1<<b
        for cap in range(1,7):
            p=sum((F(universe-L,universe))**r/F(universe) for r in range(cap))
            success=1-F(universe-L,universe)**cap
            assert p*L==success
            assert 1-success <= F(1,2**cap)
            ticket_cases+=1
    for n,a,delta,g in itertools.product((1,3,64,257,1<<40),(F(1,2),F(1,7)),(F(1,3),F(1,1<<50)),(1,3,17)):
        z=F(4*n)/delta;upper=(z.numerator+z.denominator-1)//z.denominator
        lg=(upper-1).bit_length(); t=4*lg/a**2;k=(t.numerator+t.denominator-1)//t.denominator;k=((k+g-1)//g)*g
        assert k*a*a>=4*lg and k%g==0;cases+=1
    return {'finite_cap_uniformity_certificates':ticket_cases,'rational_sample_budget_checks':cases}

def main():
    global ROOT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,help='Optional original checkpoint directory for read-only manifest/result-provenance checks. No code is imported.')
    args=parser.parse_args(); ROOT=args.source
    report={'scope':'Independently authored specification checks. Uploaded programs are never imported or executed.','sampler':sampler_checks()}
    if ROOT is not None: report['metadata']=metadata()
    report['trig']=[grid(64,b,True)[2] for b in (8,16,24,40,64)]
    report['full_tables']=[packed_case(*p) for p in [
        (29,42,4,32,128,1,64,64,3101),
        (37,40,2,8,16,2,32,64,3102),
        (73,202,40,4,4,2,64,64,3103),
        (1,8,1,4,4,2,32,64,3104),
    ]]
    report['status']='PASS';(OUT/'independent_checks_latest.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__=='__main__':main()
