"""Independent fixed-capacity tree and exact ledger controls.

This file was authored after the candidate's contract was read. No candidate
or historical program is run or imported. Divmod is the exact transition
oracle; the full prescribed chunk/stage count is recorded explicitly.
"""
from pathlib import Path
import json
import random


def run():
    rng = random.Random(170103)
    checked = ledger_cases = coverage_cases = 0
    examples = []
    for m in range(2, 9):
        for d in range(1, 5):
            p = (1 << m)-1
            Q = p**d
            for h in range(1, 6):
                L = 1 << h
                for x in (0, 1, Q**L-1, rng.randrange(Q**L)):
                    volumes = [0, 0, 0]
                    def convert(value, s):
                        assert 0 <= value < Q**s
                        if s == 1:
                            return [value]
                        D = d*s//2
                        r = [0]*D
                        q = 0
                        for j in reversed(range(d*s)):
                            chunk = (value >> (m*j)) & p
                            for i in range(D):
                                chunk, r[i] = divmod((r[i] << m) + chunk, p)
                                assert 0 <= chunk <= p
                                volumes[0] += m
                            q = (q << m)+chunk
                        low = 0
                        for i, z in enumerate(reversed(r), 1):
                            low = low*p+z
                            volumes[1] += m*i
                        assert (q, low) == divmod(value, Q**(s//2))
                        return convert(low,s//2)+convert(q,s//2)
                    ds = convert(x,L)
                    def rebuild(vals):
                        s = len(vals)
                        if s == 1:
                            return vals[0]
                        low = rebuild(vals[:s//2])
                        high = rebuild(vals[s//2:])
                        for unused in range(d*s//2):
                            high = (high << m)-high
                            volumes[2] += d*m*s
                            assert 0 <= high < (1 << (d*m*s))
                        return high+low
                    assert rebuild(ds)==x
                    expect_v = d*d*m*L*(L-1)
                    # Integer form avoids rounding ambiguities in the formula.
                    expect_a_times4 = m*d*d*L*(L-1)+m*d*L*h
                    assert 4*volumes[1]==expect_a_times4
                    assert volumes[0]==volumes[2]==expect_v
                    checked += 1
                ledger_cases += 1
                examples.append({"m":m,"d":d,"L":L,"V":expect_v,
                                 "A_times_4":expect_a_times4})
            for N in [d*m, d*m+1, 2*d*m, 7*d*m, 31*d*m]:
                threshold = (N+d*(m-1)-1)//(d*(m-1))
                L=1
                while L < threshold:
                    L *= 2
                C=d*m*L
                assert L>=2 and N<=C<4*N and Q**L >= 1<<N
                # Every internal node's divisor bit width meets the repaired
                # uniform generic division interface.
                s=L
                while s>=2:
                    c=d*m*s
                    b=(Q**(s//2)).bit_length()
                    assert (c+3)//4 <= b <= c//2
                    s//=2
                coverage_cases+=1
    result={"status":"PASS","fixed_tree_roundtrips":checked,
            "exact_transition_assembly_reconstruction_ledger_cases":ledger_cases,
            "coverage_and_divisor_width_cases":coverage_cases,
            "rows":examples,
            "qualification":"Exactness and exact volume controls, not physical timing or an unrestricted lower bound."}
    Path(__file__).with_name("FIXED_TREE_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))


if __name__ == '__main__':
    run()
