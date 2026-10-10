"""Independent exact Haar/Walsh split control. No uploaded code imports."""
import json
from pathlib import Path


def hword(n, offset=0):
    out = []
    bit = 1
    while bit < n:
        out += [(offset+i, offset+i+bit) for i in range(n) if not i & bit]
        bit *= 2
    return out


def haarword(n, offset=0):
    if n == 1:
        return []
    m = n // 2
    return [(offset+i, offset+i+m) for i in range(m)] + haarword(m, offset)


def detailword(n):
    out = []
    size = 2
    while size < n:
        out += hword(size, size)
        size *= 2
    return out


def replay(n, word):
    rows = [[int(i == j) for j in range(n)] for i in range(n)]
    for a, b in word:
        u, v = rows[a], rows[b]
        rows[a] = [x+y for x, y in zip(u, v)]
        rows[b] = [x-y for x, y in zip(u, v)]
    return rows


def expected_h(n):
    return [[(-1)**((i & j).bit_count()) for j in range(n)] for i in range(n)]


def expected_d(n):
    rows = [[0]*n for _ in range(n)]
    rows[0][0] = rows[1][1] = 1
    size = 2
    while size < n:
        h = expected_h(size)
        for i in range(size):
            for j in range(size):
                rows[size+i][size+j] = h[i][j]
        size *= 2
    return rows


results = []
for n in [2, 4, 8, 16, 32, 64]:
    w, d = haarword(n), detailword(n)
    assert len(w) == n - 1
    assert len(w) + len(d) == (n//2)*(n.bit_length()-1)
    assert replay(n, d) == expected_d(n)
    assert replay(n, w+d) == expected_h(n)
    results.append({"N": n, "haar_calls": len(w), "detail_calls": len(d),
                    "total_calls": len(w)+len(d), "full_matrix_exact": True})
assert 31**200 < 32**199
report = {"checks": results, "31^200<32^199": True,
          "W16_haar_word": haarword(16), "D16_baseline_word": detailword(16),
          "target_D16": "diag(I2,H2,H4,H8)",
          "proved_fast_word": False,
          "next_goal": "D16 in at most 16 H2 calls on exactly 16 arbitrary-data registers"}
path = Path(__file__).with_name('haar_split_control.json')
path.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
