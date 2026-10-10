#!/usr/bin/env python3
"""Independent replay of saved gate words; no experiment imports."""
import argparse
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json


def replay(word, dimension):
    rows=[{i:Q(1)} for i in range(dimension)]
    for op,dst,src,value in word:
        assert 0 <= dst < dimension
        if op=='neg':
            assert src is None
            rows[dst]={i:-a for i,a in rows[dst].items()}
        else:
            assert op=='add' and 0 <= src < dimension and src!=dst
            scalar=Q(value)
            for i,a in rows[src].items():
                rows[dst][i]=rows[dst].get(i,Q(0))+scalar*a
                if rows[dst][i]==0:
                    del rows[dst][i]
    return [sorted((i,str(a)) for i,a in row.items()) for row in rows]


def verify(root):
    summary=json.loads((root/'summary.json').read_text())
    for case in summary['cases']:
        n=case['real_scalar_inputs']
        name=f"t{case['t']}_r{case['r']}_s{case['start_stage']}"
        data=json.loads((root/(name+'_certificate.json')).read_text())
        expected=[{i:Q(1)} for i in range(case['dirty_lift']['full_state_dimension'])]
        targets=[{i:Q(a) for i,a in row} for row in data['normalized_target_matrix']]
        for j,target in enumerate(targets):
            expected[n+j].update(target)
        normalized=[sorted((i,str(a)) for i,a in row.items()) for row in expected]
        for key in ('baseline_word','candidate_word'):
            if key in data:
                actual=replay(data[key],len(expected))
                assert actual==normalized,(name,key)
                digest=hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest()
                assert digest==case['dirty_lift']['full_state_matrix_sha256']
        # Rebuild all subexpression incidences directly from the target matrix.
        pairs={};triples={};outputs=set()
        from itertools import combinations
        def key(row):
            m=min(row)
            return tuple(sorted((i,str(a/row[m])) for i,a in row.items()))
        for row in targets:
            assert len(row)==4 and all(abs(a)==Q(1,4) for a in row.values())
            outputs.add(key(row))
            for size,counts in ((2,pairs),(3,triples)):
                for ids in combinations(row,size):
                    k=key({i:row[i] for i in ids})
                    counts[k]=counts.get(k,0)+1
        assert len(outputs)==n and max(pairs.values())<=2 and max(triples.values())<=1
        assert case['baseline_add_sub']==case['candidate_add_sub']==2*n
        print(name, 'independent word and incidence certificate PASS')
    return True


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results',type=Path,nargs='?',default=Path(__file__).parent/'results')
    verify(p.parse_args().results)
