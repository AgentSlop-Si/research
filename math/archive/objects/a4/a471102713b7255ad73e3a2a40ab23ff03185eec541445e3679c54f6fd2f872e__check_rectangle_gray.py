#!/usr/bin/env python3
"""Independent integer-only rectangle and Gray-path checks."""
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
def rev(i,m): return int(format(i,f'0{m}b')[::-1],2)
rect=[];gray=[]
for m in range(1,19):
 n=1<<m
 w=(n+1)//3 if m%2 else (n-1)//3
 t=(2*n-1)//3 if m%2 else w
 c=(2*n+3*m+2)//9 if m%2 else (n+3*m-1)//9
 actual=sum(rev(i,m)<t for i in range(w))
 assert actual==c
 # 9N D = 3mN+N-(-1)^m, entirely integral.
 assert 9*(c*n-w*t)==(3*m+1)*n-(-1)**m
 rect.append({'m':m,'N':n,'W':w,'t':t,'count':c,'discrepancy_numerator':c*n-w*t,'discrepancy_denominator':n})
 q=[i^(i>>1) for i in range(n)]
 d=[0]*(n+1)
 for a,b in zip(q,q[1:]):
  a,b=sorted([a,b]);d[a+1]+=1;d[b+1]-=1
 crossings=[];v=0
 for threshold in range(1,n):
  v+=d[threshold];crossings.append(v)
 assert max(crossings)==m
 witness=(n+1)//3 if m%2 else (2*n+1)//3
 assert crossings[witness-1]==m
 maxruns=max((v+1+int(t>n//2))//2 for t,v in enumerate(crossings,1))
 assert maxruns==m//2+1
 if m>1:
  h=n//2;prev=[i^(i>>1) for i in range(h)]
  assert q==prev+[h+x for x in reversed(prev)]
  assert (q[h-1],q[h])==(h//2,3*h//2)
 gray.append({'m':m,'N':n,'maximum_crossings':m,'maximizing_threshold':witness,'maximum_prefix_preimage_runs':maxruns})

recurrences=[]
for parity in [0,1]:
 m=2 if parity==0 else 1
 n=1<<m;w=(n-1)//3 if not parity else(n+1)//3
 t=w if not parity else(2*n-1)//3;c=1
 for step in range(50):
  assert c==((n+3*m-1)//9 if not parity else(2*n+3*m+2)//9)
  assert 9*(c*n-w*t)==(3*m+1)*n-(-1)**m
  if parity==0: c,w,t=c+w+1,4*w+1,n+w
  else: c,w,t=c+2*w,4*w-1,2*n+t
  n*=4;m+=2
 recurrences.append({'parity':parity,'checked_steps':50,'last_m':m-2})

m=27;n=1<<m;w=(n+1)//3;t=(2*n-1)//3;c=(2*n+3*m+2)//9
assert c*n-w*t>9*n
out={'direct_rectangle_checks':rect,'gray_path_checks':gray,'integer_recurrence_checks':recurrences,
 'first_certified_A3_QS1_exponent':m,'cutoff_N':n,'cutoff_rectangle':{'W':w,'t':t,'count':c,'floor_mean':w*t//n,'count_minus_floor_mean':c-w*t//n},
 'source_credit':'Explicit bit-reversal rectangle and Gray recurrence proposed by paired constructor; independently proved and checked here.',
 'uploaded_code_executed':False}
(ROOT/'RECTANGLE_GRAY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
