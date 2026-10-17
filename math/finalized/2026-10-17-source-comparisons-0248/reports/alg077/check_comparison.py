#!/usr/bin/env python3
"""Fresh exact diagnostics for the ALG-077 contract comparison.

No predecessor code or external library imported. These tests check arithmetic
and evidence integrity; they do not certify either algorithm or nonexistence
of a reduction.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    expected = {
        'V11_AUDIT.md': '29d7a474e8ccded269595078cbe44f1557f78b5ab4891a92d7ded8eecd390f25',
        'CHARGED_TAYLOR_PRECISION_EXTENSION.md': 'ef1423c115d5ef1b62060d5cd6c2baa179b0e3c84e1faf55ddfb759470b472a6',
    }
    sources = []
    for name, digest in expected.items():
        data = (ROOT / 'sources' / name).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        assert actual == digest, (name, actual)
        sources.append({'path': 'sources/' + name, 'sha256': actual, 'bytes': len(data)})

    # Taylor section 2's integer nearest-grid rule, with upward ties.
    grid_points = 0
    for n in range(2, 1001):
        q = 1 << (n-1).bit_length()
        assert n <= q < 2*n
        j = [(2*k*q+n)//(2*n) for k in range(n)]
        assert len(set(j)) == n and min(j) == 0 and max(j) < q
        for k, jk in enumerate(j):
            theta = Fraction(k*q-jk*n, n)
            assert abs(theta) <= Fraction(1, 2)
            assert Fraction(k, n) == Fraction(jk, q) + theta/q
            grid_points += 1

    # Equal nonzero errors attain ||e||_2^2 / ||e||_inf^2 = N.
    norm_cases = []
    for n in [1, 2, 3, 16, 31, 1024]:
        a = Fraction(7, 19)
        l2_squared = sum(a*a for _ in range(n))
        linf_squared = a*a
        assert l2_squared / linf_squared == n
        norm_cases.append({'N': n, 'squared_ratio': n})

    # Abstract scalar countermodel of a composition-only inference:
    # C(y)=y, D(d)=d, Chat(y)=2y, Dhat(d)=d/2.
    # Dhat(Chat(y))=D(C(y)) exactly, but Dhat(d)!=D(d).
    composition_counterexample = []
    for y in [Fraction(-3), Fraction(1), Fraction(7, 5)]:
        composite_error = 2*y/2-y
        summary_error = y/2-y
        assert composite_error == 0 and summary_error != 0
        composition_counterexample.append({'input':str(y),'composite_error':str(composite_error),'summary_error':str(summary_error)})

    # Exact accounting only: a full Q scan is not a selected-N output write.
    scan_cases = []
    for n in [3, 9, 17, 65, 257, 1025]:
        q = 1 << (n-1).bit_length()
        for rank in [1, 2, 7, 31]:
            scans = rank*q
            assert rank*n <= scans < 2*rank*n
            w = (n+1).bit_length()
            bits = n*w
            assert bits//w == n
            scan_cases.append({'N':n,'Q':q,'R':rank,'scan_visits':scans,'w':w,'encoded_payload_bits':bits})

    proposal = json.loads((ROOT/'OWNER_PROPOSAL.json').read_text())
    assert proposal['stable_id'] == 'ALG-077'
    assert proposal['unchanged']['priority'] == 34
    assert proposal['unchanged']['status'] == 'TO RESEARCH'
    assert proposal['external_writes'] is False
    assert len(proposal['proposed_fields']) == 6
    assert all(c['field'] in ('Next bounded action','Pass / stop condition') for c in proposal['proposed_fields'])

    result = {
        'passed': True,
        'source_bytes': sources,
        'nearest_grid': {'lengths':999, 'exact_point_checks':grid_points},
        'tight_norm_transfer': norm_cases,
        'composition_only_counterexample': composition_counterexample,
        'scan_and_payload_accounting': scan_cases,
        'owner_proposal_scope_checks': 'passed',
        'limits': ['No predecessor program execution', 'No numerical/production certification',
                   'No external algorithm replay', 'No universal complexity lower bound',
                   'No proof that no adapter can exist'],
    }
    (ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'grid_points':grid_points,'source_hashes':len(sources),'owner_cells':6}))

if __name__ == '__main__':
    main()
