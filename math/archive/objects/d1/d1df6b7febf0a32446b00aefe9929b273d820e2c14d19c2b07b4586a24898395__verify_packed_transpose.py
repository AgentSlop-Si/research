"""Independent bit-permutation check. No uploaded module is imported or run."""
from pathlib import Path
import json,random

def masks(G,q):
    assert G>0 and G&(G-1)==0
    out=[]
    for j in range(G.bit_length()-1):
        mask=0
        for r in range(G):
            for c in range(G):
                if (r>>j)&1==0 and (c>>j)&1==1:
                    mask |= ((1<<q)-1) << ((r*G+c)*q)
        out.append((q*(1<<j)*(G-1),mask))
    return out

def packed_transpose(x,G,q,ms):
    for d,m in ms:
        t=((x>>d)^x)&m
        x ^= t^(t<<d)
    return x

def oracle(x,G,q):
    y=0
    for r in range(G):
        for c in range(G):
            y |= ((x>>((r*G+c)*q))&((1<<q)-1)) << ((c*G+r)*q)
    return y

rng=random.Random(938251)
results=[]
for G in [1,2,4,8,16,32]:
 for q in [1,2,3,4,5,7]:
    ms=masks(G,q)
    # Every bit basis vector is a complete certificate for this bit-linear map.
    for pos in range(q*G*G):
        x=1<<pos
        assert packed_transpose(x,G,q,ms)==oracle(x,G,q)
    for _ in range(25):
        x=rng.getrandbits(q*G*G)
        assert packed_transpose(x,G,q,ms)==oracle(x,G,q)
    # Independent gather/chunk/transposition/extract check.
    B=4*G
    rows=[[rng.randrange(1<<q) for _ in range(B)] for _ in range(G)]
    packed=[sum(v<<(q*c) for c,v in enumerate(row)) for row in rows]
    columns=[]
    for chunk in range(B//G):
        square=sum(((row>>(chunk*G*q))&((1<<(G*q))-1))<<(r*G*q)
                   for r,row in enumerate(packed))
        trans=packed_transpose(square,G,q,ms)
        for lane in range(G):
            key=(trans>>(lane*G*q))&((1<<(G*q))-1)
            values=[(key>>(r*q))&((1<<q)-1) for r in range(G)]
            columns.append(values)
    assert columns==[[rows[r][c] for r in range(G)] for c in range(B)]
    results.append({'G':G,'q':q,'square_bits':q*G*G,'basis_bits_checked':q*G*G,'random_words_checked':25,'gather_lanes_checked':B,'fits_word_condition':'q*G*G <= w','mask_count':len(ms)})
out={'basis_bits_checked':sum(r['basis_bits_checked'] for r in results),'random_words_checked':sum(r['random_words_checked'] for r in results),'gather_lanes_checked':sum(r['gather_lanes_checked'] for r in results),'all_passed':True,'cases':results}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
