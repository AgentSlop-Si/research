#!/usr/bin/env python3
"""Fresh independent finite controls. Standard library only. No predecessor imports/reads."""
import hashlib, json, pathlib
P=65537

def root(n, embedding=1):
    N=1<<n
    w=pow(3,(P-1)//N*embedding,P)
    assert pow(w,N,P)==1 and (N==1 or pow(w,N//2,P)!=1)
    return w

def rank(A):
    A=[list(r) for r in A]
    if not A:return 0
    r=0
    for c in range(len(A[0])):
        pivot=next((i for i in range(r,len(A)) if A[i][c]%P),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        z=pow(A[r][c],P-2,P)
        A[r]=[(a*z)%P for a in A[r]]
        for i in range(r+1,len(A)):
            if A[i][c]:
                z=A[i][c]
                A[i]=[(a-z*b)%P for a,b in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r

def selected_explicit(n,b):
    N=1<<n; L=1<<(b-1); E=set(); labels=[]
    for h in range(max(0,n-L),n+1):
        for t in range(1,L+1):
            if h<2*b+t:continue
            for k in range(1<<t):
                s=f'{k:0{t}b}'
                if not(s[0]==s[-1]=='1') or '0'*b in s:continue
                # f has MSB prefix 0^b rev_t(k) 0^b.
                prefix=int('0'*b+s[::-1]+'0'*b,2)
                free=h-2*b-t
                for tail in range(1<<free):
                    f=(prefix<<free)|tail
                    labels.append((h,f))
                    E.update(range(f,N,1<<h))
    return E,labels

def header_accept(v,n,b,K):
    # Independent predicate on bit positions, using only top K bits.
    L=1<<(b-1); ell=v<<(n-K)
    for h in range(n-L,n+1):
        if h<0:continue
        word=f'{ell% (1<<h):0{h}b}' if h else ''
        for t in range(1,L+1):
            if h<2*b+t:continue
            if word[:b]!='0'*b or word[b+t:b+t+b]!='0'*b:continue
            middle=word[b:b+t]
            if middle[0]==middle[-1]=='1' and '0'*b not in middle:
                return True
    return False

def direct_fft(v,w):
    N=len(v)
    return [sum(x*pow(w,s*k,P) for s,x in enumerate(v))%P for k in range(N)]

def radix_fft(v,w,counts):
    N=len(v)
    if N==1:return v[:]
    a=radix_fft(v[::2],w*w%P,counts); b=radix_fft(v[1::2],w*w%P,counts)
    out=[0]*N; z=1
    for i in range(N//2):
        t=z*b[i]%P
        out[i]=(a[i]+t)%P;out[i+N//2]=(a[i]-t)%P
        z=z*w%P
        counts['butterflies']+=1
    return out

def chirp(t,w):return pow(w,(-t*(t+1)//2)%(P-1),P)

def run():
    report={'model':'Finite controls in GF(65537); analytic report proves characteristic-zero statements.',
            'mask_cases':[], 'blocked_cases':[], 'kernel_rank_cases':[], 'digit_rank_cases':[],
            'negative_controls':{}, 'source_reads':'None by this verifier.'}
    for n,b in [(6,1),(7,1),(8,2),(9,2),(10,3),(11,3),(12,3),(16,4)]:
        L=1<<(b-1);assert L+2*b<=n
        E,labels=selected_explicit(n,b)
        K=min(n,2*L+2*b);B=1<<(n-K);Q=1<<K
        A=[v for v in range(Q) if header_accept(v,n,b,K)]
        routed={B*v+u for v in A for u in range(B)}
        assert E==routed
        start=1<<(n-b-1);length=1<<(n-2*b-1)
        assert set(range(start,start+length))<=E
        # Ancestors of just the t=1,h=n subfamily, not all E.
        ancestor_counts=[]
        for j in range(1,n-2*b):
            residues={a% (1<<j) for a in range(start,start+length)}
            count=(1<<(n-j))*len(residues)
            assert count==1<<n
            ancestor_counts.append(count)
        report['mask_cases'].append({'n':n,'b':b,'L':L,'K':K,'B':B,'Q':Q,'selected':len(E),'header_selected':len(A),'labels':len(labels),'interval_start':start,'interval_length':length,'full_ancestor_levels':len(ancestor_counts)})
    for n in range(2,10):
        N=1<<n;w=root(n)
        for K in sorted(set([1,n//2,n-1])):
            Q=1<<K;B=N//Q
            # Nontrivial independently chosen complete high-block mask.
            A=[v for v in range(Q) if (v*v+3*v+1)%5<2] or [0]
            x=[(s*s*17+13*s+9)%P for s in range(N)]
            direct=direct_fft(x,w)
            count={'butterflies':0}
            z=[radix_fft([x[a+Q*j] for j in range(B)],pow(w,Q,P),count) for a in range(Q)]
            first=count['butterflies']
            values=0
            for u in range(B):
                outer=radix_fft([z[a][u]*pow(w,a*u,P)%P for a in range(Q)],pow(w,B,P),count)
                for v in A:
                    assert outer[v]==direct[B*v+u]
                    values+=1
            assert first==N*(n-K)//2
            assert count['butterflies']==N*n//2
            report['blocked_cases'].append({'n':n,'K':K,'first_stage_butterflies':first,'total_butterflies':count['butterflies'],'verified_selected_outputs':values})
    for n in range(1,8):
        N=1<<n
        for embedding in [1,3]:
            w=root(n,embedding)
            H=[[chirp(i+j-(N-1),w) for j in range(N)] for i in range(N)]
            assert rank(H)==N
            # Rows may be arbitrary, columns consecutive: exact Vandermonde rank.
            rows=[s for s in range(N) if (s*s+3*s+1)%5<2] or [0]
            d=min(N,max(1,len(rows)//2))
            V=[[pow(w,e*s,P) for s in range(d)] for e in rows]
            assert rank(V)==min(len(rows),d)
            # Chirp recurrence creates input modulation instead of scalar closure.
            a=[(s*s+7*s+5)%P for s in range(N)]
            for ell in range(N-1):
                lhs=sum(a[s]*chirp(ell+1-s,w) for s in range(N))%P
                rhs=pow(w,-ell-1,P)*sum(a[s]*pow(w,s,P)*chirp(ell-s,w) for s in range(N))%P
                assert lhs==rhs
            orbit=[[pow(w,r*s,P)*chirp(-s,w)%P for s in range(N)] for r in range(N)]
            assert rank(orbit)==N
            report['kernel_rank_cases'].append({'n':n,'embedding':embedding,'Hankel_rank':N,'modulation_orbit_rank':N,'selected_rows':len(rows),'consecutive_source_columns':d})
    for n in range(2,11):
        N=1<<n;w=root(n)
        for k in sorted(set([1,n//2,n-1])):
            R=1<<(n-k);S=1<<k
            C=[[chirp((a<<k)+b,w) for b in range(S)] for a in range(R)]
            actual=rank(C);expected=min(R,S)
            assert actual==expected
            report['digit_rank_cases'].append({'n':n,'low_bits':k,'rows':R,'columns':S,'rank':actual})
    # Negative controls: missing input modulation and swapped Cooley indexing.
    N=16;w=root(4);a=[s*s+7*s+5 for s in range(N)]
    actual=sum(a[s]*chirp(1-s,w) for s in range(N))%P
    wrong=pow(w,-1,P)*sum(a[s]*chirp(-s,w) for s in range(N))%P
    assert actual!=wrong
    report['negative_controls']['omitted_modulation_detected']=True
    x=[s*s+11*s+2 for s in range(N)];d=direct_fft(x,w)
    assert any(d[4*v+u]!=d[4*u+v] for u in range(4) for v in range(4))
    report['negative_controls']['swapped_output_digits_detected']=True
    report['totals']={key:len(report[key]) for key in ['mask_cases','blocked_cases','kernel_rank_cases','digit_rank_cases']}
    return report

if __name__=='__main__':
    result=run()
    output=json.dumps(result,sort_keys=True,indent=2)+'\n'
    path=pathlib.Path(__file__).resolve().parent/'INDEPENDENT_CHECKS.json'
    path.write_text(output)
    print(json.dumps({'status':'PASS','totals':result['totals'],'sha256':hashlib.sha256(output.encode()).hexdigest()},sort_keys=True))
