#!/usr/bin/env python3
"""Exact integer necessary-condition screen for two bidirectional scan stages.
No fitting, floating point, or assumptions about scan coefficient nonzeros.
The internal permutation is P[p[j], j]=1, with zero-based indices.
"""
import argparse
from fractions import Fraction
from itertools import permutations
import json
from math import factorial
from pathlib import Path


def reverse_bits(j, m):
    return int(format(j, f'0{m}b')[::-1], 2)


def screen(p):
    n = len(p)
    assert sorted(p) == list(range(n))
    counts = [0] * (n + 1)
    best = (-1, 0, 0, 0, 0)
    for l, value in enumerate(p, 1):
        for k in range(1, n + 1):
            counts[k] += int(value < k)
            signed = n * counts[k] - k * l
            if abs(signed) > best[0]:
                best = (abs(signed), k, l, counts[k], signed)
    numerator, k, l, q, signed = best
    # Independently verify the reported maximum witness directly.
    assert q == sum(value < k for value in p[:l])
    assert numerator == abs(n * q - k * l)
    return dict(passes=numerator <= 2*n,
                max_discrepancy=str(Fraction(numerator,n)),
                scaled_max_discrepancy=numerator,
                witness=dict(k=k,l=l,q=q,signed_discrepancy=str(Fraction(signed,n))))


def structured(n):
    m = n.bit_length()-1
    assert n == 1 << m
    r = [reverse_bits(j,m) for j in range(n)]
    yield 'bit_reversal', {}, r
    for t in range(n):
        yield 'cyclic_translation', {'t':t}, [(j+t)%n for j in range(n)]
        yield 'cyclic_reflection', {'t':t}, [(t-j)%n for j in range(n)]
    for s in range(1,m):
        yield 'bit_rotation', {'s':s}, [((j<<s)|(j>>(m-s)))&(n-1) for j in range(n)]
    for a in range(n):
        yield 'bit_reversal_output_xor', {'a':a}, [x^a for x in r]
        # An input XOR gives the same family, since R(j XOR a)=R(j) XOR R(a).
    for t in range(n):
        yield 'bit_reversal_output_translation', {'t':t}, [(x+t)%n for x in r]
        yield 'bit_reversal_input_translation', {'t':t}, [r[(j+t)%n] for j in range(n)]


def run(n):
    m=n.bit_length()-1
    rows=[]
    for family,param,p in structured(n):
        rows.append(dict(family=family,parameters=param,**screen(p)))
    bits=[]
    for sigma in permutations(range(m)):
        p=[sum(((j>>sigma[t])&1)<<t for t in range(m)) for j in range(n)]
        bits.append(dict(sigma=list(sigma),**screen(p)))
    assert len(bits)==factorial(m)
    assert len({tuple(row['sigma']) for row in bits})==factorial(m)
    families={}
    for row in rows:
        f=families.setdefault(row['family'],dict(total=0,passing=[]))
        f['total']+=1
        if row['passes']:
            f['passing'].append({k:v for k,v in row.items() if k!='family'})
    return dict(n=n,threshold_scaled=2*n,structured_family_summary=families,
                structured_candidates=rows,bit_coordinate_permutations=bits,
                bit_coordinate_summary=dict(total=len(bits),
                    passing=[row for row in bits if row['passes']],
                    minimum_max_discrepancy=str(Fraction(min(row['scaled_max_discrepancy'] for row in bits),n)),
                    minimizers=[row for row in bits if row['scaled_max_discrepancy']==min(x['scaled_max_discrepancy'] for x in bits)]))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default=str(Path(__file__).with_name('discrepancy_results.json')))
    args=parser.parse_args()
    result={'meaning':'Passing only means this necessary screen does not reject the candidate. It does not assert that a factorization exists.',
            'permutation_convention':'P[p[j],j]=1; sigma maps output bit t from input bit sigma[t].',
            'results':[run(32),run(64)]}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    for record in result['results']:
        print('N=',record['n'])
        for name,summary in record['structured_family_summary'].items():
            print(name, 'passing',len(summary['passing']),'of',summary['total'])
            print('  passing parameters:',[x['parameters'] for x in summary['passing']])
        summary=record['bit_coordinate_summary']
        print('bit-coordinate permutations: passing',len(summary['passing']),'of',summary['total'], 'minimum discrepancy',summary['minimum_max_discrepancy'])
        print('  passing sigma:',[x['sigma'] for x in summary['passing']])
        print('  minimizers:',[(x['sigma'],x['witness']) for x in summary['minimizers']])
    print('Full exact witnesses:',args.output)

if __name__=='__main__':
    main()
