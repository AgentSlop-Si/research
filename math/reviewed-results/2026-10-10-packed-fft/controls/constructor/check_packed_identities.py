#!/usr/bin/env python3
"""Fresh exact controls, authored for this derivation. No research code imported.
These are finite falsification controls, not a proof or a speed benchmark.
"""
import json
from pathlib import Path

counts = {}

def rev(x, v):
    y=0
    for _ in range(v): y=(y<<1)|(x&1); x>>=1
    return y

def pattern(s,h,lane,P,Q):
    return (Q*(P*h+lane))//(P*(1<<s))

def catalogue_check():
    total=0
    for v in range(1,11):
      for d in range(v+1):
       P=1<<d
       for g in range(1,8):
        Q=1<<g
        for ell in range(d+1,v+1):
         r=ell-d; s=min(r,g); L=1<<ell
         for a in range(1<<(r-1)):
          h=a>>max(r-g,0); ident=(1<<(s-1))-1+h
          assert 0<=ident<Q-1
          for lane in range(P):
           assert pattern(s,h,lane,P,Q)==Q*(P*a+lane)//L
           total+=1
    # Huge-span aligned boundary probes, without allocating the span.
    for d in range(7):
     for g in range(1,10):
      P=1<<d; Q=1<<g
      for r in range(g,g+30):
       H=1<<(r-1); shift=r-g
       probes={0,H-1,H//2,max(0,(1<<shift)-1),min(H-1,1<<shift)}
       for a in probes:
        h=a>>shift
        for lane in (0,P-1):
         assert pattern(g,h,lane,P,Q)==Q*(P*a+lane)//(P*(1<<r))
         total+=1
    counts['exact_catalogue_lane_identities']=total

def dit_symbolic_check():
    total=0
    for v in range(1,8):
      N=1<<v
      z=[{rev(k,v):0} for k in range(N)]
      for ell in range(1,v+1):
       L=1<<ell; H=L//2
       for start in range(0,N,L):
        for j in range(H):
         a=z[start+j]; b=z[start+j+H]
         assert not (a.keys() & b.keys())
         phase=j*(N//L)
         z[start+j]={**a,**{k:(e+phase)%N for k,e in b.items()}}
         z[start+j+H]={**a,**{k:(e+phase+N//2)%N for k,e in b.items()}}
      for k,row in enumerate(z):
       assert len(row)==N
       for j,e in row.items():
        assert e==k*j%N
        total+=1
    counts['exact_symbolic_dft_matrix_entries']=total

# Total compact toy alphabet: 00=0, 01=+1, 10=-1, 11=invalid ->0.
# Real dyadic coefficients (q-Q/2)/Q and scale 3/4 replace Fourier
# coefficients only in this layout control. Quantize toward zero into
# {-1,0,+1}, clipping outside that finite set. Every code/key is total.
def dec(code): return (0,1,-1,0)[code]
def quant(num,den): return 1 if num>=den else 2 if num<=-den else 0

def pair(a,b,q,Q):
    a=dec(a); b=dec(b); den=4*Q
    return quant(3*(a*Q+b*(q-Q//2)),den),quant(3*(a*Q-b*(q-Q//2)),den)

def unpack(word,P): return [(word>>(2*j))&3 for j in range(P)]
def pack(codes): return sum(c<<(2*j) for j,c in enumerate(codes))

def build(P,Q):
    g=Q.bit_length()-1; d=P.bit_length()-1
    large=[]; total=0
    for s in range(1,g+1):
     for h in range(1<<(s-1)):
      table=[]
      for key in range(1<<(4*P)):
       a=unpack(key,P); b=unpack(key>>(2*P),P)
       outa=[]; outb=[]
       for lane in range(P):
        x,y=pair(a[lane],b[lane],pattern(s,h,lane,P,Q),Q)
        outa.append(x);outb.append(y)
       table.append(pack(outa)|(pack(outb)<<(2*P)));total+=1
      large.append(table)
    small=[]
    for ell in range(1,d+1):
     L=1<<ell; H=L//2; table=[]
     for key in range(1<<(2*P)):
      out=unpack(key,P)
      for block in range(0,P,L):
       for j in range(H):
        out[block+j],out[block+j+H]=pair(out[block+j],out[block+j+H],Q*j//L,Q)
      table.append(pack(out));total+=1
     small.append(table)
    return small,large,total

def packed_run(codes,P,Q,small,large):
    N=len(codes); v=N.bit_length()-1; d=P.bit_length()-1; g=Q.bit_length()-1
    W=[0]*(N//P)
    for i,c in enumerate(codes):
     r=rev(i,v); W[r//P]|=c<<(2*(r%P))
    for ell in range(1,v+1):
     if ell<=d:
      W=[small[ell-1][x] for x in W]
     else:
      r=ell-d;s=min(r,g);base=(1<<(s-1))-1;span=1<<r;H=span//2
      for block in range(0,N//P,span):
       for a in range(H):
        ident=base+(a>>max(r-g,0))
        key=W[block+a]|(W[block+a+H]<<(2*P))
        out=large[ident][key]
        W[block+a]=out&((1<<(2*P))-1)
        W[block+a+H]=out>>(2*P)
    return [c for word in W for c in unpack(word,P)]

def scalar_run(codes,Q):
    N=len(codes); v=N.bit_length()-1
    z=[codes[rev(i,v)] for i in range(N)]
    for ell in range(1,v+1):
     L=1<<ell;H=L//2
     for block in range(0,N,L):
      for j in range(H):
       z[block+j],z[block+j+H]=pair(z[block+j],z[block+j+H],Q*j//L,Q)
    return z

def packed_controls():
    response_count=0; executions=0
    for P,Q in ((1,4),(2,4),(4,4)):
     small,large,n=build(P,Q); response_count+=n
     for N in (max(2,P),max(4,2*P),max(8,4*P),max(32,16*P)):
      # Exhaust inputs where feasible, else deterministic adversarial codes.
      samples=range(1<<(2*N)) if N<=4 else range(128)
      for seed in samples:
       if N<=4:codes=unpack(seed,N)
       else:
        x=seed+1;codes=[]
        for i in range(N):
         x=(1103515245*x+12345)&((1<<31)-1);codes.append((x>>17)&3)
       assert packed_run(codes,P,Q,small,large)==scalar_run(codes,Q)
       executions+=1
    counts['complete_toy_table_responses']=response_count
    counts['packed_vs_scalar_exact_executions']=executions

def incremental_reverse_check():
    updates=0
    for v in range(1,15):
     N=1<<v;r=0;flips=0
     for i in range(N):
      assert r==rev(i,v)
      if i+1<N:
       h=N>>1
       while r&h:r^=h;h>>=1;flips+=1
       r^=h;flips+=1
     assert flips<2*N
     updates+=N
    counts['amortized_bit_reversal_positions']=updates

catalogue_check();dit_symbolic_check();packed_controls();incremental_reverse_check()
result={'status':'PASS','arithmetic':'Python integers only; no floating point; fresh standalone code','counts':counts,'scope':'Exact finite controls for catalogue, DIT convention, total toy tables, packed layout, and amortized bit reversal. Not an analytic error proof, production executor, or novelty evidence.'}
Path(__file__).with_name('EXACT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
