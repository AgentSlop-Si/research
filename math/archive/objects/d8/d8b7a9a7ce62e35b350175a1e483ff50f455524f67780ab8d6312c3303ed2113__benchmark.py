from __future__ import annotations
import json, random, time
from cyclotomic_packet import character_packet_apply_direct, character_packet_apply_fused, MOD


def median(xs):
    xs=sorted(xs);return xs[len(xs)//2]


def run():
    rng=random.Random(1919); out=[]
    for n in (2047,8191,32767):
        perm=list(range(1,n))+[0]
        x=[rng.randrange(MOD) for _ in range(n)]
        for b in (4,8,16):
            s=b//2; alpha=7
            # warm and correctness
            d=character_packet_apply_direct(perm,alpha,b,s,x)
            f=character_packet_apply_fused(perm,alpha,b,s,x)
            assert d==f
            td=[];tf=[]
            reps=3 if n<10000 else 2
            for _ in range(reps):
                t=time.perf_counter();character_packet_apply_direct(perm,alpha,b,s,x);td.append(time.perf_counter()-t)
                t=time.perf_counter();character_packet_apply_fused(perm,alpha,b,s,x);tf.append(time.perf_counter()-t)
            md,mf=median(td),median(tf)
            out.append({"n":n,"packet_width":b,"direct_seconds":md,"fused_seconds":mf,"speedup":md/mf})
    return out

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
