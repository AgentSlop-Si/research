"""Independent finite controls; no historical research implementation imported."""
import json, random, hashlib
from pathlib import Path

OUT=Path(__file__).resolve().parent

def scan_divmod(x,m):
    assert isinstance(m,int) and m>=2 and x>=0
    B=1<<m; p=B-1
    n=max(1,x.bit_length()); block_count=(n+m-1)//m
    q=0; r=0; prefix=0
    for j in range(block_count-1,-1,-1):
        a=(x>>(j*m)) & (B-1)
        s=r+a
        assert 0<=s<=2*p-1
        e=int(s>=p)
        c=r+e
        r=s-e*p
        assert 0<=c<B and 0<=r<p
        q=q*B+c
        prefix=prefix*B+a
        assert prefix==p*q+r
    return q,r,m*block_count

def encode_p(x,m):
    if not x:return [0],m
    ds=[]; scan=0
    while x:
        x,r,cost=scan_divmod(x,m)
        ds.append(r); scan+=cost
    return ds,scan

def assemble_groups(ds,m,d):
    assert d>=1
    out=[]; cost=0
    for k in range(0,len(ds),d):
        v=0
        for a in reversed(ds[k:k+d]):
            cost+=m+max(1,v.bit_length())
            v=(v<<m)-v+a
        out.append(v)
    return out,cost

def reconstruct_groups(ds,m,d):
    # Start at the actual top group. Never pad a sole top group to d positions.
    v=ds[-1]; cost=max(1,v.bit_length())
    for a in reversed(ds[:-1]):
        for _ in range(d):
            cost+=m+max(1,v.bit_length())
            v=(v<<m)-v
        cost+=max(1,v.bit_length(),a.bit_length())
        v+=a
    return v,cost

def native_digits(x,Q):
    if x==0:return [0]
    ds=[]
    while x:
        x,r=divmod(x,Q); ds.append(r)
    return ds

stats={"transition_checks":0,"single_division_checks":0,"grouped_roundtrip_checks":0,
       "sequential_cost_cases":0,"outside_domain_controls":{},"seed":202610170012}
for m in range(2,11):
    B=1<<m; p=B-1
    for r in range(p):
        for a in range(B):
            s=r+a; e=int(s>=p); c=r+e; rr=s-e*p
            assert divmod(r*B+a,p)==(c,rr)
            assert c<B and 0<=rr<p
            stats['transition_checks']+=1
for m in range(2,13):
    for x in range(4096):
        q,r,cost=scan_divmod(x,m)
        assert (q,r)==divmod(x,(1<<m)-1)
        stats['single_division_checks']+=1
rng=random.Random(stats['seed'])
ratios=[];examples=[]
for N in list(range(2,49))+[63,64,65,127,128,129,255,256,257,511,512,1024,2048]:
    ms=sorted(set([2,3,min(4,N),max(2,N//3),max(2,N//2),max(2,N-1),N]))
    for m in ms:
        if m>N: continue
        xs=sorted(set([(1<<(N-1)),(1<<N)-1,(1<<(N-1))|rng.getrandbits(N-1)]))
        for x in xs:
            q,r,cost=scan_divmod(x,m)
            assert (q,r)==divmod(x,(1<<m)-1)
            stats['single_division_checks']+=1
            base,scan=encode_p(x,m); K=len(base)
            p=(1<<m)-1
            assert base==native_digits(x,p)
            assert K<=2*N/m+1
            target=N*N/m
            ratio=scan/target
            # Universal safe constants for this fixed-block full-scan ledger.
            assert 0.125<=ratio<=8
            ratios.append(ratio);stats['sequential_cost_cases']+=1
            for d in sorted(set([1,2,3,5,max(1,K//2),K,K+1,2*K+3])):
                grouped,group_cost=assemble_groups(base,m,d)
                assert grouped==native_digits(x,p**d)
                y,recon_cost=reconstruct_groups(grouped,m,d)
                assert y==x
                assert group_cost<=16*target and recon_cost<=16*target
                stats['grouped_roundtrip_checks']+=1
            if N in [64,256,1024,2048] and x==(1<<N)-1:
                examples.append({"N":N,"m":m,"K":K,"p_scan_padded_bits":scan,"ratio_to_N2_over_m":ratio})
# Values below p and zero, including m>N and very large d, are valid arithmetic.
for m in [2,3,4,8,31,64,127]:
    for x in [0,1,2,3,7,15,31,255]:
        base,_=encode_p(x,m)
        for d in [1,2,7,100]:
            grouped,_=assemble_groups(base,m,d)
            assert grouped==native_digits(x,((1<<m)-1)**d)
            assert reconstruct_groups(grouped,m,d)[0]==x
            stats['grouped_roundtrip_checks']+=1
# m=1 division exists but positional conversion is invalid: quotient never decreases.
assert divmod(13,(1<<1)-1)==(13,0)
stats['outside_domain_controls']['m1_p1']='Division by 1 exists; repeated quotient remains x, so base-1 conversion is invalid.'
stats['outside_domain_controls']['composite_p15']='m=4 is included throughout; primality is unnecessary for these identities.'
stats['outside_domain_controls']['m_gt_N']='Arithmetic checked, but unqualified Theta(N^2/m) does not uniformly cover input reading.'
stats['outside_domain_controls']['large_d']='d>K tested only with an unpadded top group and no explicit Q materialization in the reviewed algorithm.'
stats['scan_ratio_min']=min(ratios);stats['scan_ratio_max']=max(ratios)
stats['selected_cost_examples']=examples
stats['result']='PASS; finite controls only, symbolic proof must establish asymptotic statement.'
(OUT/'FRESH_RESULTS.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps({k:v for k,v in stats.items() if k!='selected_cost_examples'},indent=2))
