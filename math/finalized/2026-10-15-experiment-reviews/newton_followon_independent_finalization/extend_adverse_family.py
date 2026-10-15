"""Optional larger exact width check; the r=1024 capacity is about 100 million bits."""
from pathlib import Path
import json, math
root=Path(__file__).resolve().parent
beta=0.998327339802923082
rows=[]
for r in (4,8,16,32,64,128,256,512,1024):
    m=r*(r.bit_length()-1)**2;p=(1<<m)-1;s=2*r-2
    val=lambda x:(abs(x)&-abs(x)).bit_length()-1
    factval=lambda n:n-n.bit_count()
    numer_total=m+factval(s-1)
    lams=[numer_total-val(p+t)-factval(t)-factval(s-t) for t in range(s+1)]
    Q=math.prod(p+j for j in range(r));N=Q.bit_length()
    samples=[p-2-math.prod(range(t-r+2,t+1)) if t>=r-1 else p-2 for t in range(s+1)]
    assert all(x>0 and x.bit_length()==m and x&1 for x in samples)
    assert all(N-l>=2*m for l in lams)
    assert all(m+factval(j-2)<N for j in range(2,2*r))
    ratio=(2*r-1)*2*m*math.log(2*m)**beta/(2*N*math.log(2*N)**beta)
    rows.append({'r':r,'m':m,'N':N,'min_required_precision':N-max(lams),'all_sample_bits':m,'all_sample_products_full':True,'optimistic_potential':ratio})
(root/'ADVERSE_FAMILY_EXTENSION.json').write_text(json.dumps({'rows':rows,'limit':2**(1-beta)},indent=2)+'\n')
print(rows[-1])
