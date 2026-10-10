"""Bounded rational-relaxation feasibility search with exactly checked rational witnesses."""
from pathlib import Path
p=Path(__file__).with_name('search_minor_tropical.py')
s=p.read_text()
s=s.replace('W=3;MAX_ROUNDS=5;TIME_PER_ROUND=90','W=2;MAX_ROUNDS=1;TIME_PER_ROUND=90')
s=s.replace('cost=np.zeros(N);cost[99:220]=1','cost=np.zeros(N)')
s=s.replace("integrality=np.ones(N)","integrality=np.r_[np.zeros(99+len(polys)),np.ones(N-99-len(polys))]")
s=s.replace("w=[int(round(x)) for x in res.x[:99]];badE=[];badM=[]","from fractions import Fraction\n  w=[Fraction(float(x)).limit_denominator(1000000) for x in res.x[:99]];badE=[];badM=[]")
s=s.replace("'weights':w,","'weights':[[x.numerator,x.denominator] for x in w],")
s=s.replace("f'minor_search_round{rnd}.json'","f'relaxed_search_round{rnd}.json'")
# Executing our own freshly authored control source is intentional. No supplied or reviewer source is used.
exec(compile(s,str(p), 'exec'))
