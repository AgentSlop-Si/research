from linear_cse_probe import build_before,build_after
from collections import defaultdict,Counter
from fused120 import make_fused120_plan
from crt15 import P,GENERATOR

def canonical(v):
    if v and next((x for x in v if x),0)<0:return tuple(-a for a in v)
    return v

b,pre=build_before();a,post=build_after()
B=[b.nodes[i] for i in pre] # not actual vecs
rows=[next(z for z in b.byvector.values() if z.id==idx).vec for idx in pre]
A=[tuple(next(z for z in a.byvector.values() if z.id==idx).vec[j] for idx in post) for j in range(144)]
for name,vs in [('B',rows),('A',A)]:
    g=defaultdict(list)
    for j,v in enumerate(vs):g[canonical(v)].append(j)
    d=[t for t in g.values() if len(t)>1]
    print(name,'exact signed vector repetition',len(d),'largest',max(map(len,d),default=1),'groups',d[:25])

p=make_fused120_plan(120,p=P,gen=GENERATOR)
cs=[p.d120[v][u][t] for v in range(6) for u in range(3) for t in range(8)]
for name,vs in [('B',rows),('A',A)]:
    count=0; examples=[]
    for i in range(144):
        for j in range(i+1,144):
            if cs[i]!=cs[j]:continue
            if canonical(vs[i])==canonical(vs[j]):count+=1;examples.append((i,j))
    print(name,'equal-coefficient signed same form',count,examples[:20])
print('diagonal coefficient counts',Counter(cs).most_common(8))
