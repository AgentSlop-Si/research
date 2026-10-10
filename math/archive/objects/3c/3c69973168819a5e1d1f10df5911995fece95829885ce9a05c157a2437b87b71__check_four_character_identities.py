#!/usr/bin/env python3
"""Fresh exact four-character identities; imports only authored route helpers."""
from pathlib import Path
import json
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "seed_compatibility_gate"))
from check_n16_outer_gate import PRIME as P, LABELS
from check_lift_defects import cover_and_splice, fiber, project
from check_hierarchical_lift import lift

INV4 = pow(4, -1, P)


def chi(c, e):
    return -1 if ((c & e).bit_count() & 1) else 1


def walsh(x, a, b):
    n = a * b
    return [sum(chi(c, e) * x[j] for e, j in enumerate(fiber(v, a, b))) % P
            for c in range(4) for v in range(n)]


def inverse_walsh(z, a, b):
    n = a * b
    x = [0] * (4 * n)
    for v in range(n):
        for e, j in enumerate(fiber(v, a, b)):
            x[j] = INV4 * sum(chi(c, e) * z[c * n + v] for c in range(4)) % P
    return x


def apply_green(q, weights, x):
    n = len(q)
    seen, out = bytearray(n), [0] * n
    for start in range(n):
        if seen[start]:
            continue
        order, v = [], start
        while not seen[v]:
            seen[v] = 1
            order.append(v)
            v = q[v]
        assert v == start
        carry, product = 0, 1
        for v in order:
            carry = (x[v] + weights[v] * carry) % P
            product = product * weights[v] % P
        assert product != 1
        previous = carry * pow((1 - product) % P, -1, P) % P
        for v in order:
            previous = (x[v] + weights[v] * previous) % P
            out[v] = previous
    return out


def fourier_apply(x, root):
    return [sum(value * pow(root, i * j, P) for j, value in enumerate(x)) % P
            for i in range(len(x))]


def fourier_controls(a, b, rng):
    n = a * b
    omega = pow(3, (P - 1) // (4 * n), P)
    zeta = pow(omega, 4, P)
    assert pow(omega, 2 * n, P) == P - 1
    entries = 0
    for c in range(4):
        u, v = divmod(c, 2)
        for row in range(n):
            x, y = divmod(row, b)
            r0, r1 = (2 * b * x + y) % n, (2 * b * x + y + b) % n
            for j in range(4 * n):
                t, s = divmod(j, 4)
                direct = sum(chi(c, e) * pow(omega, rr * j, P)
                             for e, rr in enumerate(fiber(row, a, b))) % P
                if s % 2 != u:
                    expected = 0
                else:
                    expected = (2 * pow(omega, (2 * b * x + y) * s, P)
                                * (pow(zeta, r0 * t, P)
                                   + (-1) ** v * pow(omega, b * s, P) * pow(zeta, r1 * t, P))) % P
                assert direct == expected
                entries += 1
    xvec = [rng.randrange(P) for _ in range(4 * n)]
    assert inverse_walsh(walsh(xvec, a, b), a, b) == xvec
    shorter = [fourier_apply(xvec[s::4], zeta) for s in range(4)]
    out = [0] * (4 * n)
    for c in range(4):
        u, v = divmod(c, 2)
        for row in range(n):
            xx, yy = divmod(row, b)
            r0, r1 = (2 * b * xx + yy) % n, (2 * b * xx + yy + b) % n
            out[c * n + row] = sum(
                2 * pow(omega, (2 * b * xx + yy) * s, P)
                * (shorter[s][r0] + (-1) ** v * pow(omega, b * s, P) * shorter[s][r1])
                for s in (u, u + 2)) % P
    target = fourier_apply(xvec, omega)
    assert out == walsh(target, a, b)
    assert inverse_walsh(out, a, b) == target
    return {"N": n, "a": a, "b": b, "exact_character_residue_entries": entries,
            "shorter_F_N_applications": 4, "vector_reconstruction_passes": True}


def bank_controls(b):
    rho = pow(3, (P - 1) // (2 * b), P)
    checked = 0
    for cout in range(4):
        u, v = divmod(cout, 2)
        for cin in range(4):
            up, w = divmod(cin, 2)
            for y in range(b):
                for z in range(b):
                    direct = INV4 * sum(
                        (-1) ** (u * ex + v * ey + up * ex + w * ee)
                        * pow(rho, (y + ey * b) * (z + ee * b), P)
                        for ex in (0, 1) for ey in (0, 1) for ee in (0, 1)) % P
                    expected = 0 if u != up else (
                        pow(rho, v * y, P) * sum(
                            pow(rho, 2 * y * t, P) * (-1) ** (w * ((2 * t + v) // b))
                            for t in range(b) if (2 * t + v) % b == z)) % P
                    assert direct == expected
                    checked += 1
    return {"b": b, "transformed_active_bank_entries": checked,
            "F_b_applications_per_active_small_block": 4}


def build_walsh_route(ps, pl, a, b):
    n = a * b
    route, signs, phis = [0] * (4 * n), [0] * (4 * n), []
    for v in range(n):
        phi = []
        for j in fiber(v, a, b):
            dest = pl[j]
            assert project(dest, a, b) == ps[v]
            x, y = divmod(dest, 2 * b)
            phi.append(2 * (x // a) + y // b)
        assert sorted(phi) == list(range(4))
        phis.append(phi)
        # Extract and independently verify the affine GF(2)^2 description.
        shift = phi[0]
        cols = [phi[1] ^ shift, phi[2] ^ shift]
        assert cols[0] and cols[1] and cols[0] != cols[1]
        assert all(phi[e] == shift ^ (cols[0] if e & 1 else 0) ^ (cols[1] if e & 2 else 0)
                   for e in range(4))
        matrix = [[sum(chi(co, phi[e]) * chi(ci, e) for e in range(4)) // 4
                   for ci in range(4)] for co in range(4)]
        assert all(sum(value != 0 for value in row) == 1 for row in matrix)
        for ci in range(4):
            choices = [(co, matrix[co][ci]) for co in range(4) if matrix[co][ci]]
            assert len(choices) == 1
            co, sign = choices[0]
            assert sign in (-1, 1)
            route[ci * n + v] = co * n + ps[v]
            signs[ci * n + v] = sign
        assert route[v] == ps[v] and signs[v] == 1
        # Check W P = signed_route W on each physical fiber basis vector.
        for e in range(4):
            got = [0] * 4
            for ci in range(4):
                co = route[ci * n + v] // n
                got[co] += signs[ci * n + v] * chi(ci, e)
            assert got == [chi(co, phi[e]) for co in range(4)]
    seen, cycles = bytearray(4 * n), []
    for v in range(4 * n):
        if seen[v]:
            continue
        w, length, product = v, 0, 1
        while not seen[w]:
            seen[w] = 1
            product *= signs[w]
            length += 1
            w = route[w]
        assert w == v
        cycles.append((length, product, v // n == 0))
    assert sorted((length, sign) for length, sign, trivial in cycles if not trivial) == [(n, -1), (2 * n, -1)]
    assert [(length, sign) for length, sign, trivial in cycles if trivial] == [(n, 1)]
    return route, signs, phis, cycles


def c4_transport(ps, phis, a, b):
    n = a * b
    order, v = [], 0
    for _ in range(n):
        order.append(v)
        v = ps[v]
    assert v == 0 and len(set(order)) == n
    transports = [None] * n
    transports[0] = list(range(4))
    for k in range(n - 1):
        transports[order[k + 1]] = [phis[order[k]][e] for e in transports[order[k]]]
    monodromy = [phis[order[-1]][e] for e in transports[order[-1]]]
    rho, e = [], 0
    for _ in range(4):
        rho.append(e)
        e = monodromy[e]
    assert e == 0 and len(set(rho)) == 4
    labels = [[0] * 4 for _ in range(n)]
    for v in range(n):
        for c in range(4):
            labels[v][transports[v][rho[c]]] = c
    for v in range(n):
        for e in range(4):
            assert labels[ps[v]][phis[v][e]] == (labels[v][e] + int(ps[v] == 0)) % 4
    return order, labels, monodromy


def apply_c4(x, labels, a, b, iota):
    n = a * b
    return [sum(pow(iota, s * labels[v][e], P) * x[j]
                for e, j in enumerate(fiber(v, a, b))) % P
            for s in range(4) for v in range(n)]


def route_green_controls(a, b, label_index, rng):
    n, label = a * b, LABELS[label_index]
    ts, ps, reps = cover_and_splice(a, b, label)
    tl, pl, rec = lift(ts, ps, a, b, label)
    signed_route, signs, phis, cycles = build_walsh_route(ps, pl, a, b)
    order, c4_labels, monodromy = c4_transport(ps, phis, a, b)
    omega = pow(3, (P - 1) // (4 * n), P)
    iota = pow(omega, n, P)
    assert pow(iota, 2, P) == P - 1
    tau = pow(label_index + 2, -1, P)
    big_guard = (1 - pow(tau, 4 * n, P)) % P
    assert big_guard
    guards = [(1 - pow(tau, n, P) * pow(iota, s, P)) % P for s in range(4)]
    product = 1
    for guard in guards:
        assert guard
        product = product * guard % P
    assert product == big_guard
    signed_weights = [0] * (4 * n)
    for source, target in enumerate(signed_route):
        signed_weights[target] = tau * signs[source] % P
    vectors = []
    if n <= 16:
        vectors = [[int(i == j) for i in range(4 * n)] for j in range(4 * n)]
    else:
        vectors = [[rng.randrange(P) for _ in range(4 * n)] for _ in range(3)]
    for x in vectors:
        g = apply_green(pl, [tau] * (4 * n), x)
        assert walsh(g, a, b) == apply_green(signed_route, signed_weights, walsh(x, a, b))
        c4x = apply_c4(x, c4_labels, a, b, iota)
        answer = []
        for s in range(4):
            weights = [tau] * n
            weights[0] = tau * pow(iota, s, P) % P
            answer.extend(apply_green(ps, weights, c4x[s * n:(s + 1) * n]))
        assert answer == apply_c4(g, c4_labels, a, b, iota)
    # Exact phase-gauge edge identities for all four homogeneous poles.
    for s in range(4):
        beta = pow(omega, s, P)
        eta = pow(iota, s, P)
        assert pow(beta, n, P) == eta
        diagonal = [0] * n
        for k, v in enumerate(order):
            diagonal[v] = pow(beta, (-k) % (4 * n), P)
        for v in range(n):
            phase = eta if ps[v] == 0 else 1
            assert phase * diagonal[v] * pow(diagonal[ps[v]], -1, P) % P == beta
    # General nonzero physical mask, checked in the common Walsh basis.
    mask = [[1 + v + 3 * e for e in range(4)] for v in range(n)]
    for v in range(n):
        hats = [INV4 * sum(chi(c, e) * mask[v][e] for e in range(4)) % P for c in range(4)]
        for d in range(4):
            for c in range(4):
                direct = INV4 * sum(chi(c, e) * mask[v][e] * chi(d, e) for e in range(4)) % P
                assert direct == hats[c ^ d]
    return {"N": n, "label": label, "walsh_signed_cycles": cycles,
            "sheet_monodromy": monodromy, "green_vector_checks": len(vectors),
            "full_entrywise_green_check": n <= 16,
            "four_channel_wrap_guards": guards,
            "guard_product_equals_large_guard": True,
            "homogeneous_pole_phase_gauges_verified": True,
            "scalar_Green_streams_after_C4_diagonalization": 4}


def main():
    rng = random.Random(456786)
    geometries = [(2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]
    fourier, routes = [], []
    for a, b in geometries:
        fourier.append(fourier_controls(a, b, rng))
        for j in range(8):
            routes.append(route_green_controls(a, b, j, rng))
        print("four characters", a * b, a, b, flush=True)
    guard_examples = []
    for values, expected_nonsingular, expected_nonzero_hats in [
            ([1, 1, 1, 1], True, 1), ([0, 1, 2, 4], False, 4)]:
        hats = [INV4 * sum(chi(c, e) * values[e] for e in range(4)) % P for c in range(4)]
        assert all(values) == expected_nonsingular
        assert sum(h != 0 for h in hats) == expected_nonzero_hats
        guard_examples.append({"physical_mask": values, "Walsh_coefficients_mod_p": hats,
                               "nonsingular": expected_nonsingular,
                               "nonzero_Walsh_coefficients": expected_nonzero_hats})
    result = {"status": "PASS", "prime": P,
              "scope": "Reusable exact decomposition and nonclosure controls; no Fourier-compatible Green coefficients or speedup.",
              "fourier_blocks": fourier, "bank_blocks": [bank_controls(b) for b in (2, 4, 8, 16)],
              "green_routes": routes, "mask_guard_controls": guard_examples,
              "cost_ledger": {"ordinary_F_N_transforms_for_full_F_4N": 4,
                              "F_b_transforms_per_active_small_bank_block": 4,
                              "small_scalar_Green_streams_per_eight_term_large_layer": 32,
                              "small_scalar_Green_streams_for_three_large_layers": 96,
                              "common_Walsh_signed_scans_per_eight_term_large_layer": 24,
                              "common_Walsh_scan_total_length_per_eight_term_large_layer": "32N",
                              "routing_phases_and_basis_work_per_fixed_order": "O(N), explicitly required",
                              "common_scalar_eight_order_closure": "Not established; common Walsh basis requires a coupled four-state family."},
              "provenance": "Fresh checker with freshly authored route helpers from the same constructor track; no uploaded code or numerical fitting."}
    (HERE / "FOUR_CHARACTER_CONTROLS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "route_instances": len(routes)}), flush=True)


if __name__ == "__main__":
    main()
