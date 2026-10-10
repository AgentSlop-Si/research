"""Fresh review controls. Never imports, executes, compiles or parses assigned programs.
Reads only snapshotted JSON data; independent elementary algebra and graph routines.
"""
from pathlib import Path
import hashlib, itertools, json
from fractions import Fraction

BASE = Path(__file__).resolve().parent

def rank_over_prime(rows, p):
    work = [[v % p for v in row] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        candidates = [k for k in range(pivot_row, len(work)) if work[k][column]]
        if not candidates:
            continue
        selected = candidates[0]
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, p)
        for below in range(pivot_row + 1, len(work)):
            coefficient = work[below][column] * inverse % p
            work[below] = [(a - coefficient*b) % p for a, b in zip(work[below], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row

def rational_inverse(matrix):
    n = len(matrix)
    columns = [[Fraction(v) for v in row] + [Fraction(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if columns[i][k])
        columns[k], columns[pivot] = columns[pivot], columns[k]
        scale = columns[k][k]
        columns[k] = [v/scale for v in columns[k]]
        for i in range(n):
            if i != k:
                multiplier = columns[i][k]
                columns[i] = [a - multiplier*b for a, b in zip(columns[i], columns[k])]
    return [row[n:] for row in columns]

# Graph is rebuilt as a successor relation, rather than loading executable code.
data_path = BASE/'data_inputs/S01_CONSTRUCTOR_N2048_CUT.json'
cut_data = json.loads(data_path.read_text())
n = cut_data['N']
assert n == 2048 and cut_data['stages'] == 4
assert cut_data['I'] == list(range(683)) and cut_data['J'] == list(range(1365, 2048))
removed = {tuple(v) for v in cut_data['removed_nodes']}
assert len(removed) == len(cut_data['removed_nodes']) == 676
limits = {'input': (0,n), 'output': (0,n), 'lower_state': (1,n), 'upper_state': (0,n-1)}
assert all(0 <= s < 4 and k in limits and limits[k][0] <= j < limits[k][1] for s,k,j in removed)

def reverse_eleven_bits(j):
    answer = 0
    for _ in range(11):
        answer = 2*answer + j%2
        j //= 2
    return answer

def successors(v):
    stage, kind, j = v
    if kind == 'input':
        yield stage, 'output', j
        if j+1 < n: yield stage, 'lower_state', j+1
        if j > 0: yield stage, 'upper_state', j-1
    elif kind == 'output':
        if stage+1 < 4: yield stage+1, 'input', reverse_eleven_bits(j)
    elif kind == 'lower_state':
        yield stage, 'output', j
        if j+1 < n: yield stage, 'lower_state', j+1
    elif kind == 'upper_state':
        yield stage, 'output', j
        if j > 0: yield stage, 'upper_state', j-1

def reachable(blocked):
    pending = [(0, 'input', j) for j in cut_data['J'] if (0,'input',j) not in blocked]
    seen = set(pending)
    while pending:
        v = pending.pop()
        for w in successors(v):
            if w not in blocked and w not in seen:
                seen.add(w)
                pending.append(w)
    return seen

targets = {(3,'output',i) for i in cut_data['I']}
reached = reachable(removed)
assert not (targets & reached)
assert targets <= reachable(set())
p = 65537
assert all(p % divisor for divisor in range(2,257))
w = pow(3, 32, p)
assert pow(w,2048,p) == 1 and pow(w,1024,p) != 1
nodes = [pow(w,j,p) for j in cut_data['J']]
determinant = 1
for i, node in enumerate(nodes):
    for earlier in nodes[:i]:
        determinant = determinant * (node-earlier) % p
assert determinant != 0
cut_result = {'input_sha256':hashlib.sha256(data_path.read_bytes()).hexdigest(), 'N':n, 'cut_size':len(removed), 'target_count':len(targets), 'reached_target_count':len(targets & reached), 'empty_cut_reaches_all_targets':True, 'finite_field':p, 'root':w, 'fourier_vandermonde_determinant':determinant, 'essentiality_not_rechecked':True, 'scope':'This exact four-stage graph and selected block; graph-to-matrix representation remains an explicit mathematical hypothesis.'}

# Exhaustive small permutation control using direct D-P matrices and cycle products.
permutation_results = []
for length, modulus, omega in [(2,97,96),(3,97,35),(4,97,22),(5,101,95),(6,97,36)]:
    assert pow(omega,length,modulus)==1
    assert all(pow(omega,d,modulus)!=1 for d in range(1,length))
    count, smallest = 0, length
    for permutation in itertools.permutations(range(length)):
        matrix = [[0]*length for _ in range(length)]
        for j in range(length):
            matrix[j][j] = pow(omega,j,modulus)
            matrix[permutation[j]][j] -= 1
        numerical_rank = rank_over_prime(matrix,modulus)
        remaining = set(range(length))
        singular_cycles = 0
        while remaining:
            current = min(remaining)
            total = 0
            while current in remaining:
                remaining.remove(current)
                total += current
                current = permutation[current]
            singular_cycles += total % length == 0
        assert numerical_rank == length-singular_cycles
        count += 1
        smallest = min(smallest,numerical_rank)
    assert smallest == length//2
    permutation_results.append({'N':length,'field':modulus,'primitive_root':omega,'permutations':count,'minimum_rank':smallest})

# A concrete guard counterexample to reading residual=0 as a valid Green equality.
# pi=identity, all weights=1 gives A=B=0. No inverse exists, but A F B-A-B=0.
sandwich_guard = {'N':2,'permutations':[[0,1],[0,1]],'weights':[[1,1],[1,1]],'A_rank':0,'B_rank':0,'sandwich_residual_is_zero':True,'valid_green_resolvents':False,'classification':'Precondition counterexample, not execution of the supplied function.'}

# A dense inverse and full realignment rank can coexist with sparse+rank-one inverse.
size = 4
swap = [0,2,1,3]
a, epsilon = Fraction(1,400), Fraction(1,16000000)
u = [2,1,1,1]
sparse = [[Fraction(i==j)-a*Fraction(swap[i]==j) for j in range(size)] for i in range(size)]
inverse_operator = [[sparse[i][j]+epsilon*u[i] for j in range(size)] for i in range(size)]
operator = rational_inverse(inverse_operator)
assert all(v for row in inverse_operator for v in row)
assert max(sum(v!=0 for v in row) for row in sparse)==2
realigned = [[operator[2*i+j][2*k+l] for j in range(2) for l in range(2)] for i in range(2) for k in range(2)]
modulus = 1000003
residue = [[v.numerator*pow(v.denominator,-1,modulus)%modulus for v in row] for row in realigned]
assert rank_over_prime(residue,modulus)==4
assert len({sum(row) for row in operator})>1
counterfamily = {'N':4,'a':str(a),'epsilon':str(epsilon),'inverse_dense':True,'inverse_sparse_part_max_row_degree':2,'inverse_correction_rank':1,'operator_realignment_rank_over_Q':4,'certifying_modulus':modulus,'nonconstant_ones_response':True,'scope':'Finite exact rational counterexample to using dense inverse/full realignment alone as exclusion from sparse-plus-low-rank classes; not a DFT.'}

metadata = []
for path in sorted((BASE/'data_inputs').glob('S21_audit*.json')):
    for row in json.loads(path.read_text()):
        actual = next(j for j in range(row['N']) if j not in row['interpolated_columns'])
        metadata.append({'input_snapshot':path.name,'N':row['N'],'fitted_columns':row['interpolated_columns'],'actual_probe_by_source_control_flow':actual,'reported_probe':row['out_of_sample_basis_column'],'mislabeled':actual!=row['out_of_sample_basis_column'],'mismatch_counts_not_reexecuted':True})
assert len(metadata)==17 and sum(row['mislabeled'] for row in metadata)==16
profiles = json.loads((BASE/'data_inputs/S29_source_RESULTS.json').read_text())['groups']['operation_profiles']
profile_results = []
for row in profiles:
    numerator, denominator = row['new_arithmetic'], row['baseline_arithmetic']
    assert numerator > denominator and row['ratio']==numerator/denominator
    profile_results.append({'N':row['N'],'reported_new_arithmetic':numerator,'reported_baseline_arithmetic':denominator,'ratio_exact':str(Fraction(numerator,denominator)),'ratio_float':numerator/denominator,'reported_word_proxy_separate_metric':True,'underlying_operation_counts_not_reexecuted':True})

result = {'status':'PASS','review_date':'2026-10-10','assigned_source_execution':False,'assigned_source_import':False,'assigned_source_compile':False,'assigned_source_AST_parse':False,'fresh_checker_executed':True,'cut_certificate':cut_result,'small_permutation_rank_controls':permutation_results,'sandwich_missing_invertibility_guard':sandwich_guard,'dense_inverse_counterexample':counterfamily,'phase32_saved_metadata':metadata,'growing_fiber_reported_profile_arithmetic':profile_results}
(BASE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','cut_size':len(removed),'cut_targets':len(targets),'vandermonde_determinant':determinant,'permutations_checked':sum(r['permutations'] for r in permutation_results),'phase32_metadata_rows':len(metadata),'phase32_mislabeled':sum(r['mislabeled'] for r in metadata),'profiles_above_baseline':len(profile_results)},indent=2))
