# ALG-034 bounded producer-binding completion candidate

Fresh executable completion of the missing input-to-producer-to-adapter gate.
Read `PROOF.md` for scope, soundness, exact stop boundary and resource contracts.

Run `python checks.py` in this directory. The checks import the fresh producer,
the unchanged reviewed policy implementation, and the text-reviewed pinned
adapter/BUCKETS dependencies. They do not execute old test programs or an old
ALG-034 producer. Standard-library Python only; no network or external writes.

Public entrypoints:

- `producer.execute(raw,state,t=16,q=None,p=None,adapt=True)`: compute from original exact input.
- `producer.verify(raw,state,t,q,packet,p=None)`: fully recompute and compare a proposed result.
- `run.packet()`: ordinary serializable proof statement, not an authenticated attestation.

`raw` has exactly F, real, imag, with ordinary integer lists.
`state` has exactly N, B, a, beta. Exact root/rounding arithmetic, immutable actual
output and direct pinned adapter invocation discharge the legacy upstream premise.
No editable metadata flag can manufacture a successful semantic-verifier result.

Successful numerical radius: C*2^(W-F-p) from the sampled target U_N P x.
Explicit local limits: N<=64, raw component width<=1024, p<=4096, 4 million
metered operations, 100000 working integer bits. Resource/domain exclusions are
truthful failures, not weakened mathematical claims. Zero branches remain distinct.

The retained adapter cannot host ANY theorem sparse Q16 instance: its N<=4096
cap contradicts B_Q>=4096k with k>=2 and B_Q<=N. A valid N=64 reduced BUCKETS
fixture is actually executed and clearly identified as such. The broader owner
is not closed by this bounded implementation.

Publication remains disabled for this task. No external service was changed.
