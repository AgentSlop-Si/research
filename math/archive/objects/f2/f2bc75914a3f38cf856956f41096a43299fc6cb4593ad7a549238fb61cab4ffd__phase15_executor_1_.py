"""Phase 15: exact dyadic-folded executor for the Phase-14 Galois residual.

N=power of 2, B=power of 2, 8<=B<N<=B*B, L=N/B.
DFT sign convention: X[k] = sum_j x[j] * zeta_N**(j*k).
Modular field: F_998244353; 3 is a primitive root.

Factor F_N = OrbitDFT * Q * A.  A's entry rule comes from Phase 14.
We do not construct A.  We execute A via L independent B-FFTs,
followed by an O(N) frequency-folding network and O(N) gathering.
The resulting *full* Fourier pipeline has exactly N*log2(N)/2
radix-2 butterflies, i.e., the ordinary FFT count (no speedup).
"""
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

P=998244353
GEN=3


def is_pow2(n):
    return n>0 and (n & (n-1)) ==0


@lru_cache(maxsize=None)
def root(n):
    assert is_pow2(n) and (P-1)%n==0
    w=pow(GEN,(P-1)//n,P)
    assert pow(w,n,P)==1 and (n==1 or pow(w,n//2,P)==P-1)
    return w


@lru_cache(maxsize=None)
def phase_powers(n):
    """All n-th-root powers, charged as O(n) scalar multiplications."""
    w=root(n)
    out=[1]*n
    for k in range(1,n):
        out[k]=out[k-1]*w%P
    return tuple(out)


def fft_radix2(values):
    n=len(values)
    assert is_pow2(n)
    out=[v%P for v in values]
    # O(n) total-bit-reversal index generation
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit
            bit>>=1
        j^=bit
        if i<j:
            out[i],out[j]=out[j],out[i]
    count=0
    length=2
    while length<=n:
        stride=phase_powers(n)[n//length]
        for left in range(0,n,length):
            w=1
            for k in range(length//2):
                u=out[left+k]
                t=out[left+k+length//2]*w%P
                out[left+k]=(u+t)%P
                out[left+k+length//2]=(u-t)%P
                w=w*stride%P
                count+=1
        length*=2
    assert count==n*(n.bit_length()-1)//2
    return out,count


def orbits(N,B):
    seen=bytearray(N)
    result=[]
    for start in range(N):
        if seen[start]:continue
        orbit=[];k=start
        while not seen[k]:
            seen[k]=1
            orbit.append(k)
            k=(1+B)*k%N
        assert k==start
        result.append(orbit)
    return result


@dataclass
class Statistics:
    N:int
    B:int
    L:int
    base_fft_butterflies:int=0
    folding_butterflies:int=0
    orbit_fft_butterflies:int=0
    residual_nonzeros:int=0
    output_rows:int=0

    @property
    def full_butterflies(self):
        return self.base_fft_butterflies+self.folding_butterflies+self.orbit_fft_butterflies

    def as_dict(self):
        return dict(N=self.N,B=self.B,L=self.L,
          base_fft_butterflies=self.base_fft_butterflies,
          folding_butterflies=self.folding_butterflies,
          orbit_fft_butterflies=self.orbit_fft_butterflies,
          full_butterflies=self.full_butterflies,
          expected_standard_fft_butterflies=self.N*(self.N.bit_length()-1)//2,
          residual_nonzeros_naive=self.residual_nonzeros,
          residual_output_rows=self.output_rows,
          all_butterflies_conserved=self.full_butterflies==self.N*(self.N.bit_length()-1)//2)


def precompute_residual(x,B):
    """A*x for orbit/e ordering. Returns (residual vector, orbits, stats).
    Stored spectra indexed by d in {1,2,...,L}; each has d rows of B values.
    """
    N=len(x)
    assert is_pow2(N) and is_pow2(B) and 8<=B<N and N<=B*B
    L=N//B
    assert is_pow2(L)
    s=Statistics(N,B,L)
    # Fine grid z[L][a][h]=x[a+L*h]. One B-FFT for each a.
    spectra={L:[]}
    for a in range(L):
        y,c=fft_radix2([x[a+L*h] for h in range(B)])
        spectra[L].append(y)
        s.base_fft_butterflies+=c

    # Exact frequency folding: Y[d/2,a](q)
    #  = Y[d,a](2q mod B) + zeta_B^q * Y[d,a+d/2](2q mod B).
    # The q+B/2 partner reuses the same twiddle/product with a minus.
    zB=root(B)
    tw=phase_powers(B)[:B//2]
    d=L
    while d>1:
        half=d//2
        smaller=[]
        for a in range(half):
            row0=spectra[d][a]
            row1=spectra[d][a+half]
            new=[0]*B
            for q in range(B//2):
                u=row0[2*q]
                v=tw[q]*row1[2*q]%P
                new[q]=(u+v)%P
                new[q+B//2]=(u-v)%P
                s.folding_butterflies+=1
            smaller.append(new)
        spectra[half]=smaller
        d=half

    # Grab the *one* nonzero character in each orbit for each input column.
    # If k0=g*u, g=L/d, u odd (d>1), and e=u*a mod d, then
    # (A*x)[orbit,e] = zeta_B**((u*a-e)//d) * Y[d,a](u).
    cycles=orbits(N,B)
    result=[]
    for orb in cycles:
        d=len(orb);g=L//d;k0=orb[0]
        assert k0%g==0
        u=k0//g
        assert 0<=u<B
        inv_u=pow(u,-1,d) if d>1 else 0
        for e in range(d):
            a=e*inv_u%d if d>1 else 0
            c=(u*a-e)//d
            assert u*a-e==d*c
            result.append(spectra[d][a][u]*phase_powers(B)[c%B]%P)
            s.output_rows+=1
    s.residual_nonzeros=N*len(cycles)
    assert len(result)==N
    assert s.folding_butterflies==(N-B)//2
    assert s.base_fft_butterflies==(N//2)*(B.bit_length()-1)
    return result,cycles,s


def orbit_finish(y,cycles,N,B,stats=None):
    """(B_orbit * Q) y, with orbit FFTs of lengths d."""
    assert len(y)==N
    L=N//B
    result=[0]*N
    ptr=0
    for orbit in cycles:
        d=len(orbit)
        g=L//d
        tmp=[]
        for e in range(d):
            r=e*g
            tmp.append(y[ptr+e]*phase_powers(N)[r]%P)
        values,c=fft_radix2(tmp)
        if stats is not None:
            stats.orbit_fft_butterflies+=c
        for t,k in enumerate(orbit):
            result[k]=values[t]
        ptr+=d
    assert ptr==N
    return result


def folded_galois_fft(x,B):
    residual,cycles,stats=precompute_residual(x,B)
    out=orbit_finish(residual,cycles,len(x),B,stats)
    assert stats.full_butterflies==len(x)*(len(x).bit_length()-1)//2
    return out,stats


def sparse_residual_oracle(x,B):
    N=len(x);L=N//B;zB=root(B)
    ans=[]
    for orbit in orbits(N,B):
        k0=orbit[0];d=len(orbit);g=L//d
        for e in range(d):
            r=e*g
            total=0
            for j in range(N):
                if k0*j %L==r:
                    h=(k0*j-r)//L
                    total+=x[j]*pow(zB,h,P)
            ans.append(total%P)
    return ans


def direct_dft(x):
    n=len(x);w=root(n)
    return [sum(x[j]*pow(w,k*j,P) for j in range(n))%P for k in range(n)]


if __name__=='__main__':
    import json,random,time
    random.seed(1515)
    for N,B in [(16,8),(32,8),(64,8),(128,16),(256,16),(256,32),(512,32),(1024,32),(1024,64),(2048,64)]:
        x=[random.randrange(P) for _ in range(N)]
        start=time.perf_counter()
        y,groups,s=precompute_residual(x,B)
        if N<=1024:
            assert y==sparse_residual_oracle(x,B),(N,B,'residual mismatch')
        out=orbit_finish(y,groups,N,B,s)
        if N<=1024:
            assert out==direct_dft(x),(N,B,'DFT mismatch')
        else:
            # All output bins are checked against an independent B-FFT radix-2 DFT.
            assert out==fft_radix2(x)[0],(N,B,'FFT mismatch')
        assert s.full_butterflies==N*(N.bit_length()-1)//2
        record=s.as_dict();record['time_s']=round(time.perf_counter()-start,4)
        record['verified']=True
        print(json.dumps(record))
