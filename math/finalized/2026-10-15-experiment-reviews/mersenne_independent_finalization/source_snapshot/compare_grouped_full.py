import benchmark as B
from grouped_fold import encode_group
from check import encode
import random,statistics,json
from pathlib import Path
R=random.Random(90152);rows=[]
for N in [256,1024,2048,8192]:
 X=R.getrandbits(N)|(1<<(N-1));Y=R.getrandbits(N)|(1<<(N-1))
 for label,m,d,bi,enc in [('p2_sequential',19,2,False,encode),('p2_grouped',19,2,False,encode_group),('binary',38,1,True,encode)]:
  B.encode=enc;v=[B.run(X,Y,m,d,bi) for _ in range(5)]
  row={'N':N,'kind':label,**v[0]}
  for k in ['total_ms','convert_ms','convolution_ms','carry_reconstruct_ms']:row[k]=statistics.median(x[k] for x in v)
  rows.append(row)
Path(__file__).with_name('GROUPED_FULL_RESULTS.json').write_text(json.dumps({'rows':rows,'scope':'Five-run medians; matched38-bit nominal blocks, same inputs/backend, full timing; purePython bounded experiment'},indent=2))
print(json.dumps(rows,indent=2))
