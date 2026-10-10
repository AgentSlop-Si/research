"""Read-only mathematical experiment against pinned upstream producer.

Tests replacing coordinate-cover labels by exact spans of their supported
weight-three vectors. No external state is changed.
"""
import sys, json, time
from collections import Counter
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/upstream')
from producer import NStar3
from frames import Checker, echelon, perp_in, nondeg, ok_res

def basis(xs): return list(echelon(xs).values())

def main(h):
    t0 = time.time()
    c = NStar3(h)
    ch = Checker(c)
    old = {n: ch.label(n) for n in c.active}
    true = {}
    for n in sorted(c.active):
        true[n] = basis([v for a in c.args[n] for v in true[a]]) if c.args[n] else old[n]
    F = [1 << p for p in range(h)]
    bad = Counter()
    for n in c.active:
        L = true[n]
        if not (nondeg(L) and ok_res(L)): bad['label'] += 1
        if not ok_res(perp_in(F,L)): bad['complement'] += 1
        if c.args[n]:
            for a in c.args[n]:
                if not ch.edge(true[a],L): bad['producer_edge'] += 1
    for S,n,_ in c.pieces:
        if not ch.edge(true[n],perp_in(F,[sum(1<<p for p in S)])): bad['piece_edge'] += 1
    reductions = Counter((len(old[n]),len(true[n])) for n in c.active if len(old[n]) != len(true[n]))
    print(json.dumps(dict(h=h,active=len(c.active),roles=c.roles,changed_nodes=sum(reductions.values()),
        dimension_pairs={str(k):v for k,v in sorted(reductions.items())},invalid=dict(bad),
        seconds=time.time()-t0),indent=2),flush=True)

if __name__=='__main__': main(int(sys.argv[1]))
