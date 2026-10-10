"""Seeded GF(2) mixing experiment; ranks are exact over C, not modular estimates."""
from __future__ import annotations
import random
import json
from parity_oracle import best_witness


def sample_mixer_columns(k: int, rng: random.Random):
    """Same row-add/swap walk as earlier source but without building 2**k arrays."""
    cols = [1 << i for i in range(k)]
    for _ in range(2*k*k):
        i, j = rng.sample(range(k), 2)
        if rng.randrange(4) == 0:
            mask = (1 << i) | (1 << j)
            cols = [c ^ ((((c >> i) & 1) ^ ((c >> j) & 1)) * mask) for c in cols]
        else:
            cols = [c ^ (((c >> j) & 1) << i) for c in cols]
    return cols


def sample_trial(k: int, seed: int):
    rng = random.Random(seed)
    stages = [sample_mixer_columns(k, rng) for _ in range(3)]
    return best_witness(k, stages)


def evaluate(ks=(8,9,10,11,12), count=50):
    report={}
    for k in ks:
        records=[sample_trial(k, 20261010000 + 10000*k + j) for j in range(count)]
        gaps=[x['gap'] for x in records]
        report[str(1 << k)]={
            'trials': count, 'failed_rank_gate': sum(x > 0 for x in gaps),
            'survived_gate': sum(x <= 0 for x in gaps),
            'max_fourier_minus_capacity': max(gaps),
            'min_fourier_minus_capacity': min(gaps),
            'example_excluded': next((records[j] for j,x in enumerate(gaps) if x>0),None),
            'example_survivor': next((records[j] for j,x in enumerate(gaps) if x<=0),None)
        }
        print(f'N={1<<k} rank_gate_rejected={report[str(1<<k)]["failed_rank_gate"]}/{count} '
              f'max_deficit={max(gaps)} min_deficit={min(gaps)}',flush=True)
    return report

if __name__ == '__main__':
    result=evaluate()
    from pathlib import Path
    with open(Path(__file__).resolve().parent/'MIXER_EXPERIMENT.json','w') as f:
        json.dump(result,f,indent=2)
