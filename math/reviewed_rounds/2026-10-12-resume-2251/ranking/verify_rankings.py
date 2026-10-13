"""Recompute published next-cycle priorities and identity coverage from explicit inputs."""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

p=Path(__file__).with_name('all_research_ranked.json')
data=json.loads(p.read_text())
weights={'information_gain':Decimal('0.25'),'tractability':Decimal('0.25'),
         'novelty_opportunity':Decimal('0.20'),'scope_impact':Decimal('0.15'),
         'evidence_readiness':Decimal('0.15')}
rows=data['records']
assert len(rows)==327
assert len({r['record_id'] for r in rows})==327
assert sum(r['canonical_counted'] for r in rows)==178
assert sum(r['novelty_view'] for r in rows)==216
for r in rows:
    d=r['dimension_scores']
    assert all(type(d[k]) is int and 0<=d[k]<=5 for k in weights)
    w=sum(weights[k]*d[k] for k in weights)
    raw=1+int((Decimal(99)*w/5).quantize(Decimal(1),rounding=ROUND_HALF_UP))
    cap=r['score_cap']
    score=raw if cap is None else min(raw,cap)
    assert raw==r['raw_priority_1_100'],r['record_id']
    assert score==r['priority_1_100'],r['record_id']
    assert 1<=score<=100 and r['provisional'] is True
    assert r['source_rows'] and r['next_bounded_task'] and r['stopping_condition']
print('PASS: 327 unique records; 178 canonical; 216 novelty views; every formula, cap, source and action checked.')
print('This verifies arithmetic and coverage, not proof correctness or historical novelty.')
