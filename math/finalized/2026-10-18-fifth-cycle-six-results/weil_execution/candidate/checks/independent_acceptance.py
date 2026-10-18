"""Fresh oracle over emitted data. Imports no candidate/package source."""
import ast
import collections
import copy
import hashlib
import itertools
import json
import math
import pathlib
import re

BASE = pathlib.Path(__file__).resolve().parents[1]
WORK = BASE / "work"
counts = collections.Counter()

def check(ok, category):
    counts[category] += 1
    if not ok:
        raise AssertionError(category)

def read(name):
    return json.loads((BASE / name).read_text())

def prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))

def kernel(q, b, ell, root):
    inv2 = pow(2, -1, q)
    invq = pow(q, -1, ell)
    chirp = [pow(root, (-b * t * t * inv2) % q, ell) for t in range(q)]
    # One direct sum per difference, then use circulant indexing.
    differences = [
        sum(chirp[t] * pow(root, d * t, ell) for t in range(q)) * invq % ell
        for d in range(q)
    ]
    return [[differences[(y - x) % q] for y in range(q)] for x in range(q)]

def multiply(x, y, q):
    a,b,c,d = x
    e,f,g,h = y
    return ((a*e+b*g)%q, (a*f+b*h)%q, (c*e+d*g)%q, (c*f+d*h)%q)

def valuation(b, p, k):
    if not b:
        return k
    return next(v for v in range(k + 1) if b % (p ** (v + 1)))

initial = read("INPUT_HASHES.json")
for rec in initial:
    current = (WORK / rec["file"]).read_bytes()
    check(len(current) == rec["bytes"], "source_member_byte_length")
    check(hashlib.sha256(current).hexdigest() == rec["sha256"], "source_member_hash")
history = [rec for rec in initial if rec["file"].startswith("historical_outputs/")]
check(len(history) == 5, "historical_file_count")
for rec in history:
    check(hashlib.sha256((WORK / rec["file"]).read_bytes()).hexdigest() == rec["sha256"], "historical_preservation")
for line in (WORK / "MANIFEST.sha256").read_text().splitlines():
    digest, name = line.split("  ", 1)
    check(hashlib.sha256((WORK/name).read_bytes()).hexdigest() == digest, "package_manifest")

run = read("RUN_RECORD.json")
check(run["exit_status"] == 0, "driver_exit")
test_ast = ast.parse((WORK / "test_checkpoint.py").read_text())
expected_tests = {n.name for n in ast.walk(test_ast) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")}
stderr = (BASE / "logs/run_all.stderr.log").read_text()
actual_tests = re.findall(r"^(test_\w+) \([^\n]+\) \.\.\. ok$", stderr, flags=re.M)
check(len(actual_tests) == 13, "actual_test_group_count")
check(set(actual_tests) == expected_tests and len(set(actual_tests)) == 13, "actual_named_test_groups")
check("\nRan 13 tests in " in stderr and stderr.rstrip().endswith("OK"), "unittest_terminal_status")
check((BASE / "logs/run_all.stdout.log").read_text().rstrip().endswith("v25 sign-corrected derivative: all requested checks passed"), "driver_terminal_status")

results = read("work/results.json")
independent = read("work/independent_results.json")
summary = read("work/RESULT_SUMMARY.json")
expected_hierarchy = []
expected_support = []
for p,k in ((3,2),(3,3),(5,2),(7,2)):
    q = p ** k
    for v in range(k+1):
        length = p ** (k-v)
        expected_hierarchy.append({
            "p":p, "k":k, "N":q, "valuation":v, "blocks":p**v,
            "block_length":length, "row_support":length, "cross_ratio_order":length,
            "radix_p_dense_terms":(k-v)*p*q,
        })
        expected_support.append({"p":p,"k":k,"valuation":v,"support":length,"cross_order":length})
check(len(results["hierarchy"]) == 13, "fresh_hierarchy_count")
check(len(independent["support_certificates"]) == 13, "fresh_support_count")
for actual, expected in zip(results["hierarchy"], expected_hierarchy, strict=True):
    check(actual == expected, "fresh_hierarchy_row")
for actual, expected in zip(independent["support_certificates"], expected_support, strict=True):
    check(actual == expected, "fresh_independent_support_row")
check(summary["automated_tests"] == len(actual_tests) == 13, "fresh_summary_test_count")
check(summary["independent_support_certificates"] == 13, "fresh_summary_support_count")
check(summary["tested_dimensions"] == [9,25,27,49], "fresh_summary_dimensions")
for key in ("main_positive","main_negative","status"):
    check(summary[key] == results[key], "fresh_summary_consistency")

groups = {}
censuses = {}
for q,p,k in ((9,3,2),(25,5,2)):
    group = [
        s for s in itertools.product(range(q), repeat=4)
        if (s[0]*s[3]-s[1]*s[2]) % q == 1
    ]
    census = collections.Counter(valuation(s[1],p,k) for s in group)
    expected = {0:486,1:108,2:54} if q==9 else {0:12500,1:2000,2:500}
    check(census == expected, "independent_sl2_census")
    check(len(group) == sum(expected.values()), "independent_sl2_size")
    groups[q] = group
    censuses[q] = dict(census)
check(results["sl2_z9_size"] == 648, "emitted_sl2_size")
check(results["sl2_z9_valuation_counts"] == {"0":486,"1":108,"2":54}, "emitted_sl2_counts")
check(independent["sl2_q9"] == {"group_size":648,"valuation_counts":{"0":486,"1":108,"2":54},"easy_subgroup_size":162}, "emitted_independent_group_record")

group9 = groups[9]
subgroups = {}
for level, expected_size in ((1,162),(2,54)):
    H = {s for s in group9 if s[1] % (3**level) == 0}
    check(len(H) == expected_size, "independent_subgroup_size")
    for a,b,c,d in H:
        check((d,(-b)%9,(-c)%9,a) in H, "independent_subgroup_inverse")
    for x in H:
        for y in H:
            check(multiply(x,y,9) in H, "independent_subgroup_closure")
    subgroups[level] = len(H)
borel = {s for s in group9 if s[1] == 0}
unseen = set(group9)
cosets = []
while unseen:
    representative = min(unseen)
    orbit = {multiply(multiply(l,representative,9),r,9) for l in borel for r in borel}
    check(orbit <= unseen, "independent_double_coset_disjointness")
    unseen -= orbit
    cosets.append({"valuation":valuation(representative[1],3,2),"size":len(orbit)})
cosets.sort(key=lambda x:(x["valuation"],x["size"]))
check(results["z9_borel_double_cosets"] == cosets, "emitted_double_cosets")
check(cosets == [{"valuation":0,"size":486},{"valuation":1,"size":54},{"valuation":1,"size":54},{"valuation":2,"size":54}], "independent_double_coset_sizes")

obs = read("logs/candidate_q9.stdout.json")
check(read("OBSERVATION_RUN_RECORD.json")["exit_status"] == 0, "observation_exit")
check((obs["q"],obs["p"],obs["k"]) == (9,3,2), "observed_parameter_dispatch")
q,ell,root = obs["q"],obs["modulus"],obs["root"]
check(prime(ell) and ell % q == 1, "independent_coefficient_prime")
check(pow(root,q,ell)==1 and len({pow(root,j,ell) for j in range(q)})==q, "independent_root_exact_order")
check([r["b"] for r in obs["rows"]] == list(range(-9,18)), "observed_scalar_domain")
canonical = {}
for row in obs["rows"]:
    b = row["b"]
    expected = kernel(q,b,ell,root)
    for label in ("fourier","gauss","completed"):
        matrix = row[label]
        check(len(matrix)==q and all(len(r)==q for r in matrix), "observed_matrix_shape")
        for x,y in itertools.product(range(q),repeat=2):
            check(matrix[x][y] == expected[x][y], "independent_q9_entry")
    if 0 <= b < q:
        canonical[b] = row["fourier"]
for b in range(q):
    U = canonical[b]
    g = math.gcd(b,q)
    for x,y in itertools.product(range(q),repeat=2):
        check((U[x][y]!=0) == ((y-x)%g==0), "independent_q9_support")
    if b==0:
        check(U==[[int(x==y) for y in range(q)] for x in range(q)], "independent_q9_identity")
    else:
        ratio=U[0][0]*U[g][g]*pow(U[0][g]*U[g][0]%ell,-1,ell)%ell
        target=pow(root,(-g*pow(b//g,-1,q//g))%q,ell)
        check(ratio==target, "independent_q9_signed_ratio")
        check(len({pow(ratio,j,ell) for j in range(q//g)})==q//g and pow(ratio,q//g,ell)==1, "independent_q9_ratio_order")
        check(U != kernel(q,-b,ell,root), "wrong_positive_chirp_rejected")
    inv2=pow(2,-1,q)
    for a,c,x,y in itertools.product(range(q),repeat=4):
        ap=(a+b*c)%q
        left=U[x][(y+a)%q]*pow(root,(c*(y+a*inv2))%q,ell)%ell
        right=pow(root,(c*(x-ap*inv2))%q,ell)*U[(x-ap)%q][y]%ell
        check(left==right, "independent_q9_covariance_entry")
for b,c,x,y in itertools.product(range(q),repeat=4):
    actual=sum(canonical[b][x][z]*canonical[c][z][y] for z in range(q))%ell
    check(actual==canonical[(b+c)%q][x][y], "independent_q9_additive_entry")

# Mutation controls exercise the independent data comparisons, not supplied assertions.
mutated = copy.deepcopy(canonical[1])
mutated[0][0] = (mutated[0][0]+1)%ell
check(mutated != kernel(q,1,ell,root), "one_entry_mutation_rejected")
check(canonical[1] != kernel(q,2,ell,root), "scalar_dispatch_mutation_rejected")
bad_summary = dict(summary, automated_tests=10)
check(bad_summary["automated_tests"] != len(actual_tests), "stale_summary_mutation_rejected")

output = {
    "verdict":"PASS",
    "oracle_source_sha256":hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    "candidate_imported_by_oracle":False,
    "actual_test_groups":actual_tests,
    "assertion_counts":dict(sorted(counts.items())),
    "actual_assertions":sum(counts.values()),
    "q9_observed_field":{"modulus":ell,"root":root},
    "q9_scalar_observation_domain":list(range(-9,18)),
    "independent_sl2_counts":censuses,
    "independent_subgroup_sizes":subgroups,
    "independent_double_cosets":cosets,
    "historical_files_unchanged":len(history),
    "all_source_members_unchanged":len(initial),
    "scope":"Fresh finite corrected-package acceptance; no original historical source replay.",
}
(BASE/"INDEPENDENT_ACCEPTANCE.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
print(json.dumps(output,indent=2,sort_keys=True))
