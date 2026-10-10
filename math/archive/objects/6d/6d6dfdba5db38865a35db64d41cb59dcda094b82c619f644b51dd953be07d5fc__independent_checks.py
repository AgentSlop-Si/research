#!/usr/bin/env python3
"""Fresh review-authored exact controls. Only Python standard library is used."""
import itertools
import json
from pathlib import Path
from exact_utils import Field, root

P=998244353
F=Field(P)
W=[[(-1)**((u*(e//2)+v*(e%2))%2)%P for e in range(4)] for u in range(2) for v in range(2)]
WI=[[z*F.inv(4)%P for z in row] for row in W]
LABELS=[(axis,c,s) for axis in ('H','V') for c in (0,1) for s in (-1,1)]


def mulvec(a,x):
    return [sum(v*w for v,w in zip(row,x))%P for row in a]


def cycles(p):
    seen=set();out=[]
    for v in range(len(p)):
        if v in seen:continue
        c=[];w=v
        while w not in seen:seen.add(w);c.append(w);w=p[w]
        assert w==v
        out.append(c)
    return out


def perm_matrix(p):
    return [[int(i==p[j]) for j in range(len(p))] for i in range(len(p))]


def fourier(n,z):
    return [[pow(z,i*j,P) for j in range(n)] for i in range(n)]


def fourier_channels():
    records=[]
    for b in (1,2,4,8):
        for a in (b,2*b):
            n=a*b
            for orientation in (1,-1):
                w=pow(root(4*n,P,3),orientation,P);z=pow(w,4,P)
                fn=fourier(n,z)
                powers=[pow(w,j,P) for j in range(4*n)]
                count=0
                for u,v in itertools.product(range(2),repeat=2):
                    for x,y in itertools.product(range(a),range(b)):
                        t0=(2*b*x+y)%n;t1=(t0+b)%n
                        for s in range(4):
                            for t in range(n):
                                j=4*t+s
                                direct=sum((-1)**(u*ex+v*ey)*powers[((2*b*(x+a*ex)+y+b*ey)*j)%(4*n)] for ex,ey in itertools.product(range(2),repeat=2))%P
                                predicted=0 if s%2!=u else 2*powers[((2*b*x+y)*s)%(4*n)]*(fn[t0][t]+(-1)**v*powers[b*s%(4*n)]*fn[t1][t])%P
                                assert direct==predicted
                                count+=1
                # Direct full Fourier vector and complete Walsh reconstruction.
                data=[(j*j*17+j*29+5)%P for j in range(4*n)]
                shorter=[mulvec(fn,data[s::4]) for s in range(4)]
                transformed=[sum(data[j]*powers[(i*j)%(4*n)] for j in range(4*n))%P for i in range(4*n)]
                channels=[]
                for u,v in itertools.product(range(2),repeat=2):
                    out=[]
                    for x,y in itertools.product(range(a),range(b)):
                        r=2*b*x+y
                        out.append(sum(2*powers[(r*s)%(4*n)]*(shorter[s][r%n]+(-1)**v*powers[b*s%(4*n)]*shorter[s][(r+b)%n]) for s in range(4) if s%2==u)%P)
                    channels.append(out)
                recovered=[0]*(4*n)
                for x,y,ex,ey in itertools.product(range(a),range(b),range(2),range(2)):
                    i=2*b*(x+a*ex)+y+b*ey
                    recovered[i]=sum((-1)**(u*ex+v*ey)*channels[2*u+v][b*x+y] for u,v in itertools.product(range(2),repeat=2))*F.inv(4)%P
                assert recovered==transformed
                records.append({'a':a,'b':b,'N':n,'orientation':orientation,'entry_checks':count,'four_shorter_transforms_and_inverse_Walsh':'PASS'})
    return records


def signed_permutations():
    records=[]
    for p in itertools.permutations(range(4)):
        m=F.mul(F.mul(W,perm_matrix(p)),WI)
        assert m[0]==[1,0,0,0] and [r[0] for r in m]==[1,0,0,0]
        dst=[];signs=[]
        for j in range(1,4):
            nz=[i for i in range(1,4) if m[i][j]]
            assert len(nz)==1 and m[nz[0]][j] in (1,P-1)
            dst.append(nz[0]-1);signs.append(m[nz[0]][j])
        assert sorted(dst)==[0,1,2]
        data={'sheet_permutation':p,'cycle_lengths':[len(c) for c in cycles(p)],'signed_character_destination':dst,'signs':[1 if s==1 else -1 for s in signs]}
        if len(cycles(p))==1:
            cc=cycles(dst);assert sorted(map(len,cc))==[1,2]
            totals=[]
            for c in cc:
                total=1
                for j in c:total=total*signs[j]%P
                assert total==P-1;totals.append(-1)
            data['nontrivial_signed_holonomy_cycles']=[{'length':len(c),'sign':sgn} for c,sgn in zip(cc,totals)]
        records.append(data)
    return records


def mgg(a,b,label):
    axis,c,s=label
    return [((x+s*(2*y+c))%a)*b+y if axis=='H' else x*b+(y+s*(2*x+c))%b for x in range(a) for y in range(b)]


def splice(p,tails):
    q=p[:]
    if len(tails)>1:
        for i,v in enumerate(tails):q[v]=p[tails[(i+1)%len(tails)]]
    return q


def lift(a,b,small,label):
    n=a*b;ts=mgg(a,b,label);tl=mgg(2*a,2*b,label)
    eta=[0]*n
    for v in range(n):eta[ts[v]]=small[v]
    pi=lambda w: ((w//(2*b))%a)*b+(w%(2*b))%b
    pre=[]
    for w in tl:
        x,y=divmod(w,2*b);xx,yy=divmod(eta[(x%a)*b+y%b],b)
        pre.append(2*b*(xx+a*(x//a))+yy+b*(y//b))
    tails=sorted(min(w for w in c if pi(w)==0) for c in cycles(pre))
    large=splice(pre,tails)
    assert len(cycles(large))==1 and all(pi(large[w])==small[pi(w)] for w in range(4*n))
    return large


def cycle_green(p,tau,x):
    """Full finite geometric identity; deliberately not a copy of a scan implementation."""
    n=len(p);assert len(cycles(p))==1 and pow(tau,n,P)!=1
    out=[0]*n;term=x[:];weight=1
    for k in range(n):
        out=[(a+weight*b)%P for a,b in zip(out,term)]
        nxt=[0]*n
        for j in range(n):nxt[p[j]]=term[j]
        term=nxt;weight=weight*tau%P
    factor=F.inv(1-pow(tau,n,P))
    return [a*factor%P for a in out]


def inspect_route(a,b,small,large,label,level):
    n=a*b;order=cycles(small)[0];assert len(order)==n and order[0]==0
    def physical(v,e):
        x,y=divmod(v,b)
        return 2*b*(x+a*(e//2))+y+b*(e%2)
    def fiber(w):
        x,y=divmod(w,2*b)
        return 2*(x//a)+y//b
    sigma=[]
    for v in order:sigma.append([fiber(large[physical(v,e)]) for e in range(4)])
    transport=[list(range(4))]
    for s in sigma:transport.append([s[e] for e in transport[-1]])
    hol=transport[-1];assert len(cycles(hol))==1
    sheet_order=cycles(hol)[0]
    # Walsh transform of each edge gives signed monomial transport of three channels.
    signed_dst=[0]*(3*n);signed_weight=[0]*(3*n)
    for i,s in enumerate(sigma):
        block=F.mul(F.mul(W,perm_matrix(s)),WI)
        for j in range(1,4):
            nz=[k for k in range(1,4) if block[k][j]];assert len(nz)==1
            signed_dst[3*i+j-1]=3*((i+1)%n)+nz[0]-1
            signed_weight[3*i+j-1]=block[nz[0]][j]
    sc=cycles(signed_dst);assert sorted(map(len,sc))==[n,2*n]
    for c in sc:
        sign=1
        for i in c:sign=sign*signed_weight[i]%P
        assert sign==P-1
    # Explicit cyclic-character gauge, indexed by the actual base vertices.
    w=root(4*n,P,3);xi=pow(w,n,P)
    channel=[]
    for s in range(4):
        beta=pow(w,s,P);matrix=[[0]*(4*n) for _ in range(n)]
        for i,v in enumerate(order):
            for k,e0 in enumerate(sheet_order):
                matrix[v][physical(v,transport[i][e0])]=pow(beta,i,P)*pow(xi,s*k,P)%P
        # A_s P_large = beta P_small A_s, checked entrywise.
        inverse_small=[0]*n
        for j,t in enumerate(small):inverse_small[t]=j
        for v in range(n):
            assert [matrix[v][large[j]] for j in range(4*n)]==[(beta*z)%P for z in matrix[inverse_small[v]]]
        channel.append(matrix)
    stacked=[row for mat in channel for row in mat]
    assert F.rank(stacked)==4*n
    data=[(j*j+11*j+37)%P for j in range(4*n)]
    guard=[]
    for tau in (0,2,3):
        assert pow(tau,4*n,P)!=1
        lg=cycle_green(large,tau,data)
        factors=[]
        for s,mat in enumerate(channel):
            beta=pow(w,s,P)
            assert mulvec(mat,lg)==cycle_green(small,tau*beta%P,mulvec(mat,data))
            factors.append((1-pow(tau*beta%P,n,P))%P)
        product=1
        for f in factors:product=product*f%P
        assert product==(1-pow(tau,4*n,P))%P
        guard.append({'tau':tau,'denominator_product':product})
    # Endpoint masks are generally 4 by 4 fiber matrices, not scalar channels.
    fiber_blocks=[]
    for v in range(n):
        block=[[channel[s][v][physical(v,e)] for e in range(4)] for s in range(4)]
        inv=F.inverse(block)
        mask=[1,2,4,8]
        conjugate=F.mul([[z*mask[e]%P for e,z in enumerate(row)] for row in block],inv)
        assert any(conjugate[i][j] for i in range(4) for j in range(4) if i!=j)
        fiber_blocks.append(block)
    return {'a':a,'b':b,'N':n,'label':label,'level':level,'holonomy':hol,'signed_sector_lengths':sorted(map(len,sc)),
            'signed_sector_signs':[-1,-1],'intertwining_channels':4,'inverse_Walsh_rank':4*n,
            'resolvent_controls':guard,'nonconstant_endpoint_mixes_channels':True},fiber_blocks


def routes():
    records=[];first_blocks={};mixing=[]
    for rectangular in (False,True):
        for label in LABELS:
            a,b=((4,2) if rectangular else (2,2))
            ts=mgg(a,b,label);small=splice(ts,[min(c) for c in cycles(ts)])
            for level in (1,2):
                large=lift(a,b,small,label)
                rec,blocks=inspect_route(a,b,small,large,label,level);records.append(rec)
                if level==1:
                    if rectangular in first_blocks:
                        before=first_blocks[rectangular]
                        nz=0
                        for x,y in zip(blocks,before):
                            change=F.mul(x,F.inverse(y))
                            nz+=sum(bool(change[i][j]) for i in range(4) for j in range(4) if i!=j)
                        mixing.append({'rectangle':rectangular,'label':label,'off_diagonal_fiber_change_entries':nz})
                    else:first_blocks[rectangular]=blocks
                a,b=2*a,2*b;small=large
    assert any(r['off_diagonal_fiber_change_entries'] for r in mixing)
    return records,mixing


def banks_and_masks():
    banks=[]
    for b in (1,2,4,8,16):
        for orientation in (1,-1):
            rho=pow(root(2*b,P,3),orientation,P);z=pow(rho,2,P)
            small=fourier(b,z);large=fourier(2*b,rho)
            # Local physical ordering ex*(2b)+Y; channels (u,v), then low y.
            local_w=[[0]*(4*b) for _ in range(4*b)]
            for u,v,y in itertools.product(range(2),range(2),range(b)):
                for ex,ey in itertools.product(range(2),repeat=2):
                    local_w[(2*u+v)*b+y][ex*(2*b)+y+b*ey]=(-1)**(u*ex+v*ey)%P
            inv=[[local_w[j][i]*F.inv(4)%P for j in range(4*b)] for i in range(4*b)]
            for active in (False,True):
                base=[[0]*(4*b) for _ in range(4*b)]
                for ex in range(2):
                    for y in range(2*b):
                        for t in range(2*b):
                            base[ex*2*b+y][ex*2*b+t]=large[y][t] if active else int(y==t)
                transformed=F.mul(F.mul(local_w,base),inv)
                count=0
                for u,v,uu,ww,y,zcol in itertools.product(range(2),range(2),range(2),range(2),range(b),range(b)):
                    predicted=0
                    if not active:predicted=int(u==uu and v==ww and y==zcol)
                    elif u==uu:
                        predicted=pow(rho,v*y,P)*sum(small[y][t]*(-1)**(ww*((2*t+v)//b)) for t in range(b) if (2*t+v)%b==zcol)%P
                    assert transformed[(2*u+v)*b+y][(2*uu+ww)*b+zcol]==predicted
                    count+=1
                banks.append({'b':b,'orientation':orientation,'active':active,'entry_checks':count})
    masks=[]
    for values in ([1,1,1,1],[1,2,4,8],[1,P-1,1,P-1],[0,1,2,4]):
        coeff=[sum(x*y for x,y in zip(row,values))*F.inv(4)%P for row in W]
        got=F.mul([[x*values[e]%P for e,x in enumerate(row)] for row in W],WI)
        want=[[coeff[c^d] for d in range(4)] for c in range(4)]
        assert got==want
        prod=1
        for v in values:prod=prod*v%P
        assert F.det(got)==prod
        masks.append({'values':values,'Walsh_coefficients':coeff,'conjugated_determinant':prod,'nonzero_coefficients':sum(bool(c) for c in coeff)})
    assert masks[0]['nonzero_coefficients']==1 and masks[0]['conjugated_determinant']
    assert masks[-1]['nonzero_coefficients']==4 and not masks[-1]['conjugated_determinant']
    return banks,masks


def main():
    f=fourier_channels();s=signed_permutations();r,m=routes();b,k=banks_and_masks()
    result={'status':'PASS','field':P,'primitive_generator':3,'fourier_channel_controls':f,'all_24_sheet_permutations':s,
            'hierarchical_route_controls':r,'order_dependent_gauge_controls':m,'bank_controls':b,'mask_controls':k,
            'summary':{'fourier_layout_sign_cases':len(f),'fourier_entry_equalities':sum(v['entry_checks'] for v in f),
                       'sheet_permutations':len(s),'four_cycle_holonomies':sum(len(v['cycle_lengths'])==1 for v in s),
                       'hierarchical_four_sheet_routes':len(r),'resolvent_channel_equalities':12*len(r),
                       'order_change_controls':len(m),'bank_cases':len(b),'bank_entry_equalities':sum(x['entry_checks'] for x in b),'mask_controls':len(k)}}
    path=Path(__file__).with_name('VERIFIED_RESULTS.json')
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result['summary'],sort_keys=True));print('PASS')

if __name__=='__main__':main()
