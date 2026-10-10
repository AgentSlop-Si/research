"""Fresh full-vector control using separate direct branch and fused algorithms."""
from pathlib import Path
import json,time
out=Path(__file__).resolve().parent
N=65536;K=64;M=N//K;p=65537;a=2;b=3;w=3
assert pow(w,N,p)==1 and pow(w,N//2,p)!=1
q=pow(w,M,p);assert pow(q,K,p)==1 and pow(q,K//2,p)!=1
x=[(i*i+17*i+11)%p for i in range(N)]
d=(1-pow(b,K,p))%p;c=pow(a,K,p);assert (pow(d,M,p)-pow(a,N,p))%p
# Fused: geometric seed, rolling window, then exact K-cycle closure.
t0=time.time();z=[0]*N;v=1
for j in range(K):z[0]=(z[0]+v*x[-j%N])%p;v=v*a%p
assert v==c
for i in range(1,N):z[i]=(a*z[i-1]+x[i]-c*x[(i-K)%N])%p
id=pow(d,-1,p);r=c*id%p;ic=pow((1-pow(r,M,p))%p,-1,p);fused=[0]*N
for s in range(K):
 v=0
 for i in range(s,N,K):v=(r*v+id*z[i])%p
 v=v*ic%p
 for i in range(s,N,K):v=(r*v+id*z[i])%p;fused[i]=v
fused_seconds=time.time()-t0
# Direct original branches: variable diagonal cycle, never the collapsed D.
t0=time.time();phase=[pow(q,i,p) for i in range(K)];invd=[pow((1-b*t)%p,-1,p) for t in phase]
acc=[0]*N
for j in range(K):
 rates=[a*invd[(i+j)%K]%p for i in range(K)]
 v=0;A=1
 for i in range(N):
  rr=rates[i%K];v=(rr*v+invd[(i+j)%K]*x[i])%p;A=A*rr%p
 assert A!=1
 v=v*pow((1-A)%p,-1,p)%p
 for i in range(N):
  v=(rates[i%K]*v+invd[(i+j)%K]*x[i])%p;acc[i]=(acc[i]+v)%p
avg=[v*pow(K,-1,p)%p for v in acc]
assert avg==fused
reference_seconds=time.time()-t0
# A few direct Fourier coefficients are a mismatch control, not a full DFT test.
mismatches=[]
for k in [0,1,2,3,7,31,255,1024,8191,32768,65535]:
 step=pow(w,-k%N,p);v=1;tot=0
 for xx in x:tot=(tot+xx*v)%p;v=v*step%p
 if tot!=fused[k]:mismatches.append(k)
assert mismatches
P=lambda t:t.bit_length()-1+t.bit_count()
source_setup=P(N)+P(N//2)+2*P(M)+2*P(K)+5
source_online=10*N+4*K-4+P(K)
assert (source_setup,source_online)==(74,655619)
res={'policy':'Fresh independent algorithms only; no source execution. Timings are incidental, not portable benchmarks.','N':N,'K':K,'prime':p,'omega':w,'alpha':a,'beta':b,'all_output_entries_compared':N,'direct_dft_mismatch_bins':mismatches,'source_control_flow_count_reconstructed_without_source_execution':{'setup':source_setup,'online':source_online,'total':source_setup+source_online},'fresh_fused_seconds':fused_seconds,'fresh_direct_branch_seconds':reference_seconds}
(out/'fresh_large_twirl_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
