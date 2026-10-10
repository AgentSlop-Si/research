"""Packed square-tile transpose: semantic checks, not a wall-clock RAM claim.
An admissible RAM instantiation must satisfy q*G*G <= word_bits.
"""
import random,json

def masks(G,q):
    assert G>=1 and G&(G-1)==0
    result=[]
    for j in range(G.bit_length()-1):
        s=1<<j; d=q*s*(G-1); mask=0
        for row in range(G):
            for col in range(G):
                if not(row&s) and col&s:
                    mask |= ((1<<q)-1) << (q*(row*G+col))
        result.append((d,mask))
    return result

def trans(x,ms):
    for d,m in ms:
        t=((x>>d)^x)&m
        x^=t^(t<<d)
    return x

def pack(a,q):
    return sum(v<<(q*i) for i,v in enumerate(a))

def unpack(x,count,q):
    mask=(1<<q)-1
    return [(x>>(q*i))&mask for i in range(count)]

rng=random.Random(20261009);tests=0;records=[]
for G in [1,2,4,8,16,32]:
    for q in [1,2,3,4,8]:
        ms=masks(G,q)
        for t in range(30):
            a=[rng.randrange(1<<q) for _ in range(G*G)]
            expected=[a[row*G+col] for col in range(G) for row in range(G)]
            assert unpack(trans(pack(a,q),ms),G*G,q)==expected
            assert trans(trans(pack(a,q),ms),ms)==pack(a,q)
            tests+=1
        records.append({'G':G,'symbol_bits':q,'required_word_bits':q*G*G,'delta_swap_rounds':len(ms)})
# First-table rows -> square tiles -> lane keys for an independently chosen map.
# The map models second-table evaluation; correctness does not assume it is a mean.
blocks=0
for G in [1,2,4,8,16]:
    q=3;ms=masks(G,q); B=8*G
    rows=[[rng.randrange(1<<q) for _ in range(B)] for _ in range(G)]
    packed=[pack(row,q) for row in rows]
    actual=[]
    for start in range(0,B,G):
        tile=0
        for row in range(G):
            piece=(packed[row]>>(q*start))&((1<<(q*G))-1)
            tile|=piece<<(q*G*row)
        by_lane=trans(tile,ms)
        actual += unpack(by_lane,G,q*G)
    expected=[pack([rows[row][col] for row in range(G)],q) for col in range(B)]
    assert actual==expected
    blocks+=1
print(json.dumps({'status':'passed','random_square_tile_tests':tests,'whole_output_block_tests':blocks,'records':records,'scope':'Python arbitrary-size integers verify identities only. Unit word-operation bounds apply only when all packed objects fit the specified RAM word.'},indent=2))
