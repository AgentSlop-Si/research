"""Independent set-based verifier for all restricted support certificates.

The verifier never uses or imports the source programs or the generating C++
implementation. Every accepted seed supplies an 8x8 triangular nonzero minor.
"""
from pathlib import Path
import json, hashlib
from itertools import combinations
from collections import Counter
P=Path(__file__).resolve().parent
S=P/'source/extracted/fft_cyclotomic_zero_forcing_v34'
E=json.loads((S/'topology_11.json').read_text())['layers']

# Independently traverse the network forward from each input.
single=[];forced=[set(),set(),set()];multiplicity=Counter()
for input_node in range(11):
    paths={input_node:[[]]}
    for layer in E:
        nxt={}
        for idx,(dst,src) in enumerate(layer):
            for path in paths.get(src,[]):nxt.setdefault(dst,[]).append(path+[idx])
        paths=nxt
    for output_node in range(11):
        p=paths.get(output_node,[]);multiplicity[len(p)]+=1
        if len(p)==1:
            single.append({'output':output_node,'input':input_node,'edges':p[0]})
            for l,i in enumerate(p[0]):forced[l].add(i)
claim=json.loads((P/'unique_path_receipt.json').read_text())
assert sorted(single,key=lambda q:(q['output'],q['input']))==claim['single_routes']
assert [sorted(t) for t in forced]==claim['forced_unit_edges']
assert len(single)==22 and list(map(len,forced))==[18,18,19]
allowed=[set(range(33))-f for f in forced]
seen=[set(),set(),set()];hist=[Counter(),Counter(),Counter()];digest=hashlib.sha256()
first=[]

def triangular_witness(layer,deleted,seed):
    rows=[set() for _ in range(11)]
    for index,(r,c) in enumerate(layer):
        if index not in deleted:rows[r].add(c)
    known=set(seed);steps=[]
    while len(known)<11:
        for row,columns in enumerate(rows):
            unknown=columns-known
            if len(unknown)==1:
                column=next(iter(unknown));known.add(column);steps.append((row,column));break
        else:return None
    assert len({r for r,c in steps})==len(steps)
    # In this order each witness row has no later selected column, so the
    # selected square submatrix is lower triangular with nonzero diagonal.
    for t,(r,c) in enumerate(steps):
        assert c in rows[r]
        assert not any(later in rows[r] for _,later in steps[t+1:])
    return steps

for line in (P/'restricted_seed_certificates.txt').read_text().splitlines():
    l,mask,seedmask=map(int,line.split());assert 0<=l<3
    assert mask not in seen[l];seen[l].add(mask)
    deleted={j for j in range(33) if mask>>j&1}
    assert mask==sum(1<<j for j in deleted) and deleted<=allowed[l]
    seed={j for j in range(11) if seedmask>>j&1}
    assert seedmask==sum(1<<j for j in seed) and len(seed)==3
    steps=triangular_witness(E[l],deleted,seed)
    assert steps is not None and len(steps)==8,(l,mask,seedmask)
    hist[l][len(deleted)]+=1
    digest.update((str((l,mask,seedmask,steps))+'\n').encode())
    if len(first)<=l:first.append({'layer':l,'deleted':sorted(deleted),'seed':sorted(seed),'triangular_minor':steps})

for l in range(3):
    # Generate the complete powerset independently of the generator's order.
    expected={0}
    for e in sorted(allowed[l]):expected|={m|(1<<e) for m in list(expected)}
    assert seen[l]==expected
    assert all(hist[l][z]==len(list(combinations(allowed[l],z))) for z in range(len(allowed[l])+1))
assert triangular_witness(E[0],set(),set()) is None
assert triangular_witness([],set(),{0,1,2}) is None
out={'passes':True,'single_route_count':len(single),'path_multiplicity_histogram':dict(sorted(multiplicity.items())),
     'forced_unit_edge_indices':[sorted(f) for f in forced],
     'optional_nonunit_edge_indices':[sorted(a) for a in allowed],
     'pattern_counts':list(map(len,seen)),'total_patterns':sum(map(len,seen)),
     'every_pattern_has_triangular_nonzero_minor_order':8,
     'all_patterns_and_steps_sha256':digest.hexdigest(),
     'first_witness_by_layer':first,'controls':{'empty_seed_rejected':True,'empty_support_rejected':True}}
(P/'restricted_verifier_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
