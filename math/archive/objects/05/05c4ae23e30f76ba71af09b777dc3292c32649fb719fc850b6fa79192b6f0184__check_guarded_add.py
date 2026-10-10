"""Independent 64-bit bounded-word verification of the new uploaded guarded-sum idea.
Tests the accumulation primitive; does not benchmark a complete FFT/table builder.
"""
import random,json

def layout(G,bound,word_bits):
    h=(2*bound*G).bit_length() # 2**h > max lane sum
    lanes=word_bits//h
    if not lanes:raise ValueError('no complete lane fits')
    return h,lanes

def prepack(row,G,bound,W):
    h,t=layout(G,bound,W); out=[]
    for s in range(0,len(row),t):
        word=sum((v+bound)<<(h*j) for j,v in enumerate(row[s:s+t]))
        assert all(-bound<=v<=bound for v in row[s:s+t])
        assert word.bit_length()<=W
        out.append(word)
    return out

def packed_sum(rows,B,G,bound,W):
    h,t=layout(G,bound,W); words=[0]*len(rows[0]); adds=0
    for row in rows:
        for j,v in enumerate(row):
            words[j]+=v; adds+=1
            assert words[j].bit_length()<=W # No hidden giant integer or word overflow.
    mask=(1<<h)-1
    out=[((words[j//t]>>(h*(j%t)))&mask)-G*bound for j in range(B)]
    return out,adds

rng=random.Random(20261009);blocks=0;lanes=0;records=[]
for G in [1,2,4,8,16,32,64,128,256]:
 for bound in [1,3,8,17]:
  for B in [1,7,32,64,129]:
   h,t=layout(G,bound,64)
   for mode in ['random','max','min','alternating']:
    raw=[]
    for i in range(G):
     raw.append([rng.randint(-bound,bound) if mode=='random' else bound if mode=='max' else -bound if mode=='min' else (bound if (i+j)%2 else -bound) for j in range(B)])
    packed=[prepack(row,G,bound,64) for row in raw]
    got,adds=packed_sum(packed,B,G,bound,64)
    assert got==[sum(row[j] for row in raw) for j in range(B)]
    assert adds==G*((B+t-1)//t)
    blocks+=1;lanes+=B
   records.append({'groups':G,'lane_bound':bound,'B':B,'guarded_lane_bits':h,'lanes_per_64bit_word':t,'words_per_table_result':(B+t-1)//t})
print(json.dumps({'status':'passed','block_cases':blocks,'lane_sums_checked':lanes,'physical_word_bits':64,'records':records,'scope':'Every packed word and accumulated word stayed within64bits. Repacking was charged separately and is intended for table construction, never repeated inside timed lookups. Full FFT/sampling/phasor-table implementation not tested here.'},indent=2))
