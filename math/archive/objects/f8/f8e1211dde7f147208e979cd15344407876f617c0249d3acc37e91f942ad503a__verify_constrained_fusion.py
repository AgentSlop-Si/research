#!/usr/bin/env python3
"""Fresh exact controls; imports only the Python standard library.

This is an oracle, not a proposed fast implementation. No predecessor code is
read, executed, or imported. All indexing and operators are defined here.
"""
import hashlib
import json
from pathlib import Path


def reverse(v, width):
    ans = 0
    for _ in range(width):
        ans = 2 * ans + (v & 1)
        v >>= 1
    return ans


def gamma(v):
    ans = 0
    while v:
        if v & 1:
            ans += v >> 1
        v >>= 1
    return ans


def avoid(v, width, b):
    return "0" * b not in format(v, "0%db" % width)


def words(t, b):
    return [k for k in range(1 << (t - 1), 1 << t)
            if k & 1 and avoid(k, t, b)]


def step(v, root, p):
    size = len(v)
    out = [0] * size
    weight = 1
    for s, value in enumerate(v):
        out[(2*s) % size] = (out[(2*s) % size] + value) % p
        out[(2*s+1) % size] = (out[(2*s+1) % size] + weight*value) % p
        weight = weight * root % p
    return out


def orbit(x, root, p, n):
    out = [x]
    for _ in range(n):
        out.append(step(out[-1], root, p))
    return out


def route(v, t, b, omega, eta, p):
    r = len(v)
    out = [0] * r
    valid = set(words(t, b))
    ratio = omega * pow(eta, p-2, p) % p
    for a, value in enumerate(v):
        k = a % (1 << t)
        if k in valid:
            dest = ((1 << b) * (a-k) + k) % r
            out[dest] = (out[dest] + pow(ratio, gamma(k), p)*value) % p
    return out


def support(n, b, t):
    return [(1 << (b+t))*q+k
            for q in range(1 << (n-2*b-t)) for k in words(t, b)]


def selected_locations(n, b):
    horizon = min(1 << (b-1), n-2*b)
    loc = []
    for t in range(1, horizon+1):
        for h in range(2*b+t, n+1):
            for a in support(n, b, t):
                loc.append((h, a, t))
    assert len({(h, a) for h, a, t in loc}) == len(loc)
    return loc


def packet_row(n, b, h, a, omega, p):
    N = 1 << n
    c = a % (1 << (h-b))
    q = a >> (h-b)
    f = reverse(c, h-b)
    phase = pow(omega, gamma(c), p)
    M = N >> h
    row = [0] * N
    for s in range(q, N, M):
        row[s] = phase * pow(omega, s*f, p) % p
    return row


def frequency_selected(ell, h, t, b):
    # Read the low h Fourier-frequency bits directly, rather than using routes.
    if (ell >> (h-b)) & ((1 << b)-1):
        return False
    gap = (ell >> (h-b-t)) & ((1 << t)-1)
    if not (gap & 1) or gap < (1 << (t-1)) or not avoid(gap, t, b):
        return False
    return not ((ell >> (h-2*b-t)) & ((1 << b)-1))


def spectral_weights(n, b):
    N = 1 << n
    horizon = min(1 << (b-1), n-2*b)
    return [sum(1 << h for t in range(1, horizon+1)
                for h in range(2*b+t, n+1)
                if frequency_selected(ell, h, t, b))
            for ell in range(N)]


def rank(rows, p):
    if not rows:
        return 0
    a = [row[:] for row in rows]
    used = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(used, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[used], a[pivot] = a[pivot], a[used]
        inv = pow(a[used][col], p-2, p)
        a[used] = [v*inv % p for v in a[used]]
        for j in range(used+1, len(a)):
            z = a[j][col]
            if z:
                a[j] = [(v-z*w) % p for v, w in zip(a[j], a[used])]
        used += 1
        if used == len(a):
            break
    return used


def determinant(a, p):
    a = [row[:] for row in a]
    ans = 1
    for i in range(len(a)):
        j = next((j for j in range(i, len(a)) if a[j][i]), None)
        if j is None:
            return 0
        if j != i:
            a[i], a[j] = a[j], a[i]
            ans = -ans
        z = a[i][i]
        ans = ans*z % p
        inv = pow(z, p-2, p)
        for j in range(i+1, len(a)):
            c = a[j][i]*inv % p
            for k in range(i+1, len(a)):
                a[j][k] = (a[j][k]-c*a[i][k]) % p
    return ans % p


def actual_h(n, b, omega, p):
    N = 1 << n
    loc = selected_locations(n, b)
    # Build columns directly from source trajectories, not packet formulas.
    cols = []
    for s in range(N):
        x = [int(i == s) for i in range(N)]
        path = orbit(x, omega, p, n)
        cols.append([path[h][a << b] for h, a, t in loc])
    return [[cols[s][i] for s in range(N)] for i in range(len(loc))]


def source_controls(n, b, omega, p, basis):
    N = 1 << n
    r = N >> b
    eta = pow(omega, 1 << b, p)
    horizon = min(1 << (b-1), n-2*b)
    xs = [[(17*s*s+23*s+41) % p for s in range(N)]]
    if basis:
        xs += [[int(i == s) for i in range(N)] for s in range(N)]
    checked = packets = 0
    for x in xs:
        path = orbit(x, omega, p, n)
        jets = [[v[a << b] for a in range(r)] for v in path]
        for j in range(n+1):
            v = jets[j]
            for t in range(1, min(horizon, n-b-j)+1):
                v = step(v, eta, p)
                got = route(v, t, b, omega, eta, p)
                good = set(support(n, b, t))
                want = [jets[j+b+t][a] if a in good else 0 for a in range(r)]
                assert got == want, (n, b, j, t, "future alias")
                checked += r
        for h, a, t in selected_locations(n, b):
            row = packet_row(n, b, h, a, omega, p)
            value = sum(s*v for s, v in zip(row, x)) % p
            assert value == jets[h][a]
            packets += 1
    return {"n": n, "b": b, "field": p, "inputs": len(xs),
            "feedback_coordinates": checked, "packet_values": packets}


def gram_controls(n, b, omega, p):
    N = 1 << n
    loc = selected_locations(n, b)
    H = actual_h(n, b, omega, p)
    Hbar = actual_h(n, b, pow(omega, p-2, p), p)
    assert H == [packet_row(n, b, h, a, omega, p) for h, a, t in loc]
    G = [[sum(a[s]*c[v] for a, c in zip(Hbar, H)) % p
          for v in range(N)] for s in range(N)]
    weights = spectral_weights(n, b)
    # G eigenvectors are reciprocal-root Fourier columns.
    for ell, weight in enumerate(weights):
        vector = [pow(omega, (-s*ell) % N, p) for s in range(N)]
        got = [sum(v*z for v, z in zip(row, vector)) % p for row in G]
        assert got == [weight*z % p for z in vector]
    observed_rank = rank(H, p)
    assert observed_rank == sum(bool(w) for w in weights)
    # Exact finite-field image of det(I+H*H)=product(1+lambda).
    for s in range(N):
        G[s][s] = (G[s][s]+1) % p
    rhs = 1
    for w in weights:
        rhs = rhs*(1+w) % p
    assert determinant(G, p) == rhs
    return {"n": n, "b": b, "field": p, "rows": len(H),
            "rank": observed_rank, "nonzero_spectral_weights": sum(bool(w) for w in weights),
            "gram_entries": N*N, "eigenvector_coordinates": N*N,
            "weight_histogram": {str(w): weights.count(w) for w in sorted(set(weights))}}


def marker_controls():
    # Count exact isolated-marker occurrences for small b in a short block.
    evidence = []
    for b in range(1, 5):
        width = 2*(b+2)+3
        pattern = "1"+"0"*b+"1"
        good = 0
        for ell in range(1 << width):
            word = format(ell, "0%db" % width)
            starts = [i for i in range(width-len(pattern)+1)
                      if word[i:i+len(pattern)] == pattern]
            if len(starts) < 2:
                continue
            good += 1
            # Multiple P patterns force a valid neighboring-run pair.
            found = any(frequency_selected(ell, h, t, b)
                        for t in range(1, width-2*b+1)
                        for h in range(2*b+t, width+1))
            assert found
        evidence.append({"b": b, "width": width, "two_isolated_markers": good})
    # Integer cross-multiplied first/second-moment inequalities in the proof.
    for b in range(7, 257):
        m = 1 << (b-2)
        a = m-b-1
        den = 1 << (b+2)
        assert 2*a >= m
        assert 32*a >= den  # lambda >= 1/32
        assert 16*a <= den  # lambda <= 1/16
        assert den+a+4 < 2*den
        # lambda/(1+lambda+4p) >= 1/64.
        assert 64*a >= den+a+4
    return evidence


def main():
    data = {"scope": "Exact algebraic finite-field controls; complex magnitude bound is proved in the report.",
            "source_cases": [], "gram_cases": [], "marker_cases": []}
    p = 65537
    for n in range(3, 11):
        omega = pow(3, (p-1)//(1 << n), p)
        assert pow(omega, 1 << n, p) == 1
        assert pow(omega, 1 << (n-1), p) != 1
        for b in range(1, min(4, (n-1)//2)+1):
            data["source_cases"].append(source_controls(n, b, omega, p, n <= 6))
            if n <= 6:
                data["gram_cases"].append(gram_controls(n, b, omega, p))
    # A second characteristic and a distinct odd primitive-root embedding.
    p = 257
    for n, b in [(4, 1), (5, 2), (6, 2)]:
        omega = pow(3, 3*(p-1)//(1 << n), p)
        assert pow(omega, 1 << n, p) == 1 and pow(omega, 1 << (n-1), p) != 1
        data["source_cases"].append(source_controls(n, b, omega, p, True))
        data["gram_cases"].append(gram_controls(n, b, omega, p))
    data["marker_cases"] = marker_controls()
    data["summary"] = {
        "source_cases": len(data["source_cases"]),
        "source_inputs": sum(c["inputs"] for c in data["source_cases"]),
        "feedback_coordinates": sum(c["feedback_coordinates"] for c in data["source_cases"]),
        "packet_values": sum(c["packet_values"] for c in data["source_cases"]),
        "gram_cases": len(data["gram_cases"]),
        "gram_entries": sum(c["gram_entries"] for c in data["gram_cases"]),
        "eigenvector_coordinates": sum(c["eigenvector_coordinates"] for c in data["gram_cases"]),
        "moment_b_values": 250,
    }
    target = Path(__file__).with_name("CONSTRAINED_CONTROLS.json")
    target.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print(json.dumps(data["summary"], sort_keys=True))
    print("CONSTRAINED_CONTROLS.json SHA256 "+hashlib.sha256(target.read_bytes()).hexdigest())
    print("PASS: exact source aliases, packet rows, spectral Gram, ranks, determinant, and marker controls")


if __name__ == "__main__":
    main()
