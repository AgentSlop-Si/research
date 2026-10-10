import json
import math
from pathlib import Path
import numpy as np


def normalized_dft(n: int) -> np.ndarray:
    j = np.arange(n)[:, None]
    k = np.arange(n)[None, :]
    return np.exp(-2j * np.pi * j * k / n) / math.sqrt(n)


def random_unitary(n: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
    q, r = np.linalg.qr(z)
    # normalize QR phases so this is deterministic for a fixed RNG stream
    d = np.diag(r)
    phase = np.ones_like(d)
    nz = np.abs(d) > 0
    phase[nz] = d[nz] / np.abs(d[nz])
    return q @ np.diag(np.conj(phase))


def permutation_matrix(p: np.ndarray) -> np.ndarray:
    n = len(p)
    P = np.zeros((n,n), dtype=np.complex128)
    P[np.arange(n), p] = 1.0
    return P


def local_prefixes(B: int, K: float):
    """A toy exact B-point primitive with a deliberately ill-conditioned prefix.

    P1 = D has cond(D)=K.
    P2 = F_B D^{-1}, so P2 P1 = F_B and the completed primitive is unitary.

    This is *not* a fast circuit; it is only a sanity-check object for the
    condition-reset lemma.
    """
    F = normalized_dft(B)
    scales = np.geomspace(1.0, float(K), B)
    D = np.diag(scales.astype(np.complex128))
    Dinv = np.diag((1.0/scales).astype(np.complex128))
    return [D, F @ Dinv], F


def embed_fiber_operator(local: np.ndarray, N: int, B: int, P: np.ndarray) -> np.ndarray:
    base = np.kron(np.eye(N//B, dtype=np.complex128), local)
    return P.conj().T @ base @ P


def run_case(N=64, B=4, macro_levels=8, K=1e4, seed=0):
    assert N % B == 0
    rng = np.random.default_rng(seed)
    prefixes, F = local_prefixes(B, K)
    Q = np.eye(N, dtype=np.complex128)
    rows = []
    max_cond = 1.0
    local_conds = [float(np.linalg.cond(x)) for x in prefixes]

    for level in range(macro_levels):
        p = rng.permutation(N)
        P = permutation_matrix(p)
        # During the local primitive, previous completed work Q is unitary.
        running = Q
        for step, local in enumerate(prefixes, start=1):
            G = embed_fiber_operator(local, N, B, P)
            # prefixes[1] is the SECOND gate, not cumulative. Build the actual
            # cumulative local state explicitly.
            if step == 1:
                cumulative_local = prefixes[0]
            else:
                cumulative_local = prefixes[1] @ prefixes[0]
            cumulative_global = embed_fiber_operator(cumulative_local, N, B, P) @ Q
            c = float(np.linalg.cond(cumulative_global))
            max_cond = max(max_cond, c)
            rows.append({
                "level": level,
                "step": step,
                "condition": c,
                "local_cumulative_condition": float(np.linalg.cond(cumulative_local)),
            })

        # Completed local block is unitary. Add an arbitrary unitary mixing to
        # model permutations/twiddles/reindexing between macro levels.
        Ublock = embed_fiber_operator(F, N, B, P)
        mix = random_unitary(N, rng)
        Q = mix @ Ublock @ Q
        completed_cond = float(np.linalg.cond(Q))
        rows.append({"level": level, "step": "completed+unitary_mix", "condition": completed_cond})
        max_cond = max(max_cond, completed_cond)

    return {
        "N": N,
        "B": B,
        "macro_levels": macro_levels,
        "target_local_condition": K,
        "local_gate_conditions": local_conds,
        "max_global_condition": max_cond,
        "final_condition": float(np.linalg.cond(Q)),
        "rows": rows,
    }


def main():
    out = []
    for N, levels in [(16, 12), (64, 10)]:
        for K in [1e2, 1e4, 1e6]:
            out.append(run_case(N=N, B=4, macro_levels=levels, K=K, seed=1234))
    path = Path(__file__).with_name("condition_reset_results.json")
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")
    for r in out:
        ratio = r['max_global_condition']/r['target_local_condition']
        print(f"N={r['N']:>3} levels={r['macro_levels']:>2} K={r['target_local_condition']:.0e} "
              f"max_global={r['max_global_condition']:.6g} final={r['final_condition']:.6g} "
              f"max/K={ratio:.6g}")

if __name__ == "__main__":
    main()
