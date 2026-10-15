import random,json,time,statistics
from pathlib import Path
from grouped_fold import div_group,encode_group
from check import encode,decode
R=random.Random(9141);count=0;rows=[]
for m in [2,3,5,7,13,19]:
 for d in [1,2,3,4,8]:
  Q=((1<<m)-1)**d
  for n in [0,1,8,32,128,512,2048]:
   x=R.getrandbits(n)
   assert div_group(x,m,d)==divmod(x,Q)
   a,_=encode_group(x,m,d);assert decode(a,m,d)[0]==x;count+=1
for n in [256,1024,2048,8192]:
 x=R.getrandbits(n);m=19;d=2
 ts=[];us=[]
 for _ in range(7):
  t=time.perf_counter();a,l=encode(x,m,d);ts.append((time.perf_counter()-t)*1000)
  t=time.perf_counter();b,k=encode_group(x,m,d);us.append((time.perf_counter()-t)*1000)
  assert a==b
 rows.append({'N':n,'old_convert_ms':statistics.median(ts),'grouped_convert_ms':statistics.median(us),'old_folds':l['folds'],'grouped_folds':k['folds']})
Path(__file__).with_name('GROUPED_FOLD_RESULTS.json').write_text(json.dumps({'division_roundtrip_cases':count,'rows':rows,'scope':'One-input conversion medians, seven runs; no transform timing and no asymptotic claim'},indent=2))
print(count,rows)
