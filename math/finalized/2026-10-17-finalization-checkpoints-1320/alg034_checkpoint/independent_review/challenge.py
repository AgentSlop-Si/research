"""Fresh independent controls for the separately inspected new consistency checker.

The candidate is imported only after its complete source has been read and
manually inspected. No historical producer, adapter, or archived program runs.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

from independent_oracle import canonical_dyadics, policy as oracle_policy, trim


HERE = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("fresh_inspected_binding_candidate", SOURCE)
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
RESULTS = []


def check(name, fn):
    try:
        detail = fn()
        RESULTS.append({"name": name, "pass": True, "detail": detail})
    except Exception as exc:
        RESULTS.append({"name": name, "pass": False,
                        "error": type(exc).__name__ + ": " + str(exc)})


def need_reject(fn):
    try:
        fn()
    except candidate.Rejection as exc:
        return exc.code
    raise AssertionError("invalid input was accepted")


def require_consistency(result):
    assert result["status"] == "BINDING_CONSISTENT_PRODUCER_UNVERIFIED", result
    for key in ("authenticated_provenance", "producer_execution_verified",
                "numerical_error_certificate_verified", "adapter_invoked",
                "downstream_integration_verified"):
        assert result[key] is False, (key, result[key])
    return result


def data(n=9, b=3):
    return {"F": 5, "real": [1] + [0] * (n-1), "imag": [0] * n}, {
        "N": n, "B": b, "a": 1, "beta": 0}


RAW, STATE = data()
Q, T = 4, 0
POLICY = candidate.derive_policy(RAW, STATE, T, Q)
PAYLOAD = {"kappa": POLICY["plan"]["kappa"],
           "real": [1] + [0] * 8, "imag": [0] * 9}
RECORD = candidate.make_record(RAW, STATE, T, Q, PAYLOAD)


def verify(record=None, raw=None, state=None, t=T, q=Q, p=None, reference=None):
    return candidate.verify(RAW if raw is None else raw, STATE if state is None else state,
                            t, q, RECORD if record is None else record,
                            p=p, expected_payload=reference)


def one_oracle_comparison(raw, state, t, q, extra_p=0):
    expected = oracle_policy(raw["real"], raw["imag"], raw["F"],
                             state["N"], state["B"], state["a"], state["beta"], t, q)
    p = expected.get("p_min")
    if p is not None:
        p += extra_p
    actual = candidate.derive_policy(raw, state, t, q, p=p)
    assert actual["outcome"] == expected["branch"]
    assert actual["W"] == expected["W"]
    assert actual["t"] == t and actual["q"] == q
    if expected["W"]:
        actual_pre = actual["prepass"]
        assert actual_pre["L"] == expected["L"] and actual_pre["D"] == expected["D"]
        assert actual_pre["modulus"] == expected["phi"]
        assert [x["g"] for x in actual_pre["blocks"]] == [trim(x) for x in expected["polynomials"]]
        assert [x["remainder"] for x in actual_pre["blocks"]] == expected["remainders"]
        assert [x["mass"] for x in actual_pre["blocks"]] == expected["masses"]
    if expected["branch"] == "NONZERO_PLAN":
        for key in ("A", "selected_block", "K", "G", "H", "C", "c", "p_min"):
            assert actual["plan"][key] == expected[key], (key, actual["plan"][key], expected[key])
        assert actual["p"] == p
        assert actual["plan"]["kappa"] == expected["W"] - raw["F"] - p
        assert actual["plan"]["radius"] == {"coefficient": expected["C"], "scale": expected["W"] - raw["F"] - p}
        assert actual["plan"]["mu_scale"] == -raw["F"] - (expected["D"] - 1) * expected["K"]
        I = state["B"] + 2 * (state["N"] - 1).bit_length() + 10
        assert actual["plan"]["I"] == I
        assert actual["plan"]["sufficient_65536_bit_width_bound"] == (p + I <= 65536)
    return expected["branch"]


def oracle_batch():
    rng = random.Random(3401254)
    total = 0
    outcomes = {}
    for n in range(3, 33):
        for b in sorted({3, n, (n + 3) // 2}):
            a = rng.choice([i for i in range(1, n) if __import__("math").gcd(i, n) == 1])
            state = {"N": n, "B": b, "a": a, "beta": rng.randrange(n)}
            raw = {"real": [rng.randrange(-32, 33) for _ in range(n)],
                   "imag": [rng.randrange(-32, 33) for _ in range(n)], "F": rng.randrange(-20, 21)}
            outcome = one_oracle_comparison(raw, state, rng.randrange(5), (n - 1).bit_length() + 2, total % 7)
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            total += 1
    for n in (6, 9):
        raw, state = data(n)
        raw["real"] = [1, -1] + [0] * (n - 2)
        outcome = one_oracle_comparison(raw, state, 0, (n - 1).bit_length())
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        assert outcome == ("EXACT_PROJECTED_ZERO" if n == 6 else "NONZERO_PLAN")
        total += 1
    for F in (-100, 0, 100):
        raw, state = data(6)
        raw.update(real=[0] * 6, F=F)
        outcome = one_oracle_comparison(raw, state, 0, 3)
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        total += 1
    return {"cases": total, "outcomes": outcomes}


check("independent_exact_policy_cases", oracle_batch)
check("baseline_only_consistency", lambda: require_consistency(verify()))
check("exact_payload_external_reference_only_consistency", lambda: require_consistency(verify(reference=PAYLOAD)))


def canonical_checks():
    examples = [([0, -24, 16], [0, 0, 8], 12), ([0, 0, 0], [0, 0, 0], -99),
                ([-1, 2, 0], [0, 0, 0], -30), ([-(1 << 1000), 0, 0], [0, 0, 0], 127)]
    for real, imag, F in examples:
        er, ei, ef = canonical_dyadics(real, imag, F)
        assert candidate.dyadic_value({"real": real, "imag": imag}, -F) == {"real": er, "imag": ei, "scale": -ef}
    r1, s = data(6)
    r1.update(real=[-3, 2, 0, 0, 0, 0], imag=[0, 1, 0, 0, 0, 0], F=-7)
    r2 = {"F": r1["F"] + 19, "real": [x << 19 for x in r1["real"]], "imag": [x << 19 for x in r1["imag"]]}
    p1, p2 = [candidate.derive_policy(r, s, 0, 3) for r in (r1, r2)]
    assert p1["input_value_sha256"] == p2["input_value_sha256"]
    assert p1["raw_input_sha256"] != p2["raw_input_sha256"]
    assert p1["W"] + 19 == p2["W"]
    zs = []
    for F in (-99, 0, 99):
        zs.append(candidate.derive_policy({"F": F, "real": [0]*6, "imag": [0]*6}, s, 0, 3))
    assert len({p["input_value_sha256"] for p in zs}) == 1
    assert len({p["raw_input_sha256"] for p in zs}) == 3
    assert candidate.strict_loads('{"zero":-0}') == {"zero": 0}
    assert candidate.canonical_bytes(candidate.strict_loads('{"zero":-0}')) == b'{"zero":0}'
    return "Equivalent dyadic values share value identity; exact submitted grids remain distinct; integer -0 canonicalizes to 0."


check("signed_zero_common_trailing_powers_and_original_identity", canonical_checks)


def modified_payload_attack():
    payload = copy.deepcopy(PAYLOAD)
    payload["real"] = [17, -29, 63, 2, -7, 19, 999, -47, 4]
    record = candidate.make_record(RAW, STATE, T, Q, payload)
    result = require_consistency(verify(record=record))
    assert result["exact_payload_matches_external_reference"] is None
    rejection = need_reject(lambda: verify(record=record, reference=PAYLOAD))
    return {"unreferenced_result": result["status"], "external_reference_rejection": rejection,
            "arbitrary_payload_is_not_a_numerical_certificate": True}


check("arbitrary_modified_payload_with_recomputed_hashes", modified_payload_attack)


def modified_input_attack():
    raw = copy.deepcopy(RAW)
    raw["real"][3] = -321
    pol = candidate.derive_policy(raw, STATE, T, Q)
    payload = {"kappa": pol["plan"]["kappa"], "real": [-100] * 9, "imag": [3] * 9}
    record = candidate.make_record(raw, STATE, T, Q, payload)
    result = require_consistency(verify(record=record, raw=raw, reference=payload))
    mismatch = need_reject(lambda: verify(record=record))
    return {"changed_caller_context": result["status"], "original_context_rejection": mismatch,
            "self_supplied_matching_reference_still_unverified": True}


check("arbitrary_modified_input_and_payload_with_recomputed_hashes", modified_input_attack)


for field in ("authenticated_provenance", "producer_execution_verified", "numerical_error_certificate_verified", "status"):
    def flagged(field=field):
        r = copy.deepcopy(RECORD)
        r[field] = "PROVEN_EXECUTION" if field == "status" else True
        return need_reject(lambda: verify(record=r))
    check("reject_self_asserted_top_level_" + field, flagged)


def rehash_record(r):
    def independent_hash(domain, value):
        encoded = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                             separators=(',', ':')).encode('ascii')
        return hashlib.sha256(b'ALG034:BINDING:V1\0' + domain.encode('ascii') + b'\0' + encoded).hexdigest()
    r["policy_sha256"] = independent_hash("policy", r["policy"])
    r["payload_grid_sha256"] = independent_hash("payload-grid", r["payload"])
    if r["payload"] is not None:
        pr, pi, pf = canonical_dyadics(r['payload']['real'], r['payload']['imag'], -r['payload']['kappa'])
        r["payload_value_sha256"] = independent_hash("dyadic-vector-value", {'real': pr, 'imag': pi, 'scale': -pf})
    r["binding_sha256"] = independent_hash("binding-record", {k:v for k,v in r.items() if k != "binding_sha256"})
    return r


for field in ("outcome", "W", "q", "t", "p", "raw_input_sha256", "input_value_sha256", "state_sha256"):
    def policy_attack(field=field):
        r = copy.deepcopy(RECORD)
        old = r["policy"][field]
        r["policy"][field] = old + 1 if type(old) is int else "forged"
        rehash_record(r)
        return need_reject(lambda: verify(record=r))
    check("reject_rehashed_policy_" + field, policy_attack)


for field in ("A", "selected_block", "K", "G", "H", "C", "c", "p_min", "I", "kappa", "mu_scale"):
    def plan_attack(field=field):
        r = copy.deepcopy(RECORD)
        r["policy"]["plan"][field] += 1
        rehash_record(r)
        return need_reject(lambda: verify(record=r))
    check("reject_rehashed_plan_" + field, plan_attack)


for field in ("policy_sha256", "payload_grid_sha256", "payload_value_sha256", "binding_sha256"):
    def hash_attack(field=field):
        r = copy.deepcopy(RECORD)
        r[field] = "0" * 64
        return need_reject(lambda: verify(record=r))
    check("reject_corrupt_" + field, hash_attack)


def domain_separation():
    domains = ["raw-input", "dyadic-vector-value", "canonical-state", "policy", "payload-grid", "binding-record"]
    assert len({candidate.digest(d, {"same": 1}) for d in domains}) == len(domains)
    return {"domains": domains}


check("hash_domain_separation", domain_separation)


for n, expected in ((6, "EXACT_PROJECTED_ZERO"), (9, "NONZERO_PLAN")):
    def parity(n=n, expected=expected):
        raw, state = data(n)
        raw["real"] = [1, -1] + [0]*(n-2)
        pol = candidate.derive_policy(raw, state, 0, (n-1).bit_length())
        assert pol["outcome"] == expected
        if expected != "NONZERO_PLAN":
            record = candidate.make_record(raw, state, 0, (n-1).bit_length())
            require_consistency(candidate.verify(raw,state,0,(n-1).bit_length(),record))
            need_reject(lambda: candidate.make_record(raw,state,0,(n-1).bit_length(),{"real":[0]*n,"imag":[0]*n,"kappa":0}))
            need_reject(lambda: candidate.derive_policy(raw,state,0,(n-1).bit_length(),p=0))
        return expected
    check("even_odd_projected_zero_control_N" + str(n), parity)


class IntSubclass(int):
    pass


class ListSubclass(list):
    pass


def raw_mutation(key, value):
    r = copy.deepcopy(RAW)
    r[key] = value
    return need_reject(lambda: verify(raw=r))


for label, key, value in [
    ("real_short", "real", [1]), ("imag_long", "imag", [0]*10),
    ("real_tuple", "real", tuple(RAW["real"])), ("real_list_subclass", "real", ListSubclass(RAW["real"])),
    ("real_bool", "real", [True]+[0]*8), ("real_float", "real", [1.0]+[0]*8),
    ("real_int_subclass", "real", [IntSubclass(1)]+[0]*8), ("real_string", "real", ["1"]+[0]*8),
    ("real_overwidth", "real", [1 << 1024]+[0]*8), ("F_bool", "F", True),
    ("F_float", "F", 5.0), ("F_overwidth", "F", 1 << 128)]:
    check("reject_raw_"+label, lambda key=key,value=value: raw_mutation(key,value))


for label, key, value in [("N_bool","N",True),("N_small","N",2),("N_cap","N",65),
                           ("B_small","B",2),("B_big","B",10),("a_not_unit","a",3),
                           ("a_zero","a",0),("beta_negative","beta",-1),("beta_big","beta",9)]:
    def invalid_state(key=key,value=value):
        s=copy.deepcopy(STATE);s[key]=value
        return need_reject(lambda: verify(state=s))
    check("reject_state_"+label,invalid_state)


for label, kwargs in [("t_negative",{"t":-1}),("t_bool",{"t":True}),("q_small",{"q":3}),
                       ("q_float",{"q":4.0}),("p_small",{"p":POLICY["p"]-1}),
                       ("p_bool",{"p":True}),("p_negative",{"p":-1})]:
    check("reject_precision_"+label,lambda kwargs=kwargs: need_reject(lambda:verify(**kwargs)))


for label, key, value in [("real_short","real",[1]),("real_tuple","real",tuple(PAYLOAD["real"])),
                           ("imag_bool","imag",[True]+[0]*8),("kappa_wrong","kappa",PAYLOAD["kappa"]+1),
                           ("kappa_float","kappa",float(PAYLOAD["kappa"])),
                           ("overwidth","real",[1 << 8192]+[0]*8)]:
    def payload_bad(key=key,value=value):
        r=copy.deepcopy(RECORD);r["payload"][key]=value
        return need_reject(lambda:verify(record=r))
    check("reject_payload_"+label,payload_bad)


def zero_approximation():
    p=copy.deepcopy(PAYLOAD);p["real"]=[0]*9;p["imag"]=[0]*9
    return need_reject(lambda:candidate.make_record(RAW,STATE,T,Q,p))


check("reject_zero_approximation_on_nonzero_plan",zero_approximation)


for label, text in [("duplicate",'{"x":1,"x":2}'),("float",'{"x":1.0}'),
                     ("exponent_float",'{"x":1e0}'),("nan",'{"x":NaN}'),
                     ("infinity",'{"x":Infinity}'),("trailing",'{}{}'),
                     ("bad_integer",'{"x":01}'),("oversize_integer",'{"x":'+'1'*2501+'}'),
                     ("lone_surrogate",'"\ud800"')]:
    check("reject_json_"+label,lambda text=text:need_reject(lambda:candidate.strict_loads(text)))


check("reject_deep_json_at_canonical_intake", lambda: need_reject(
    lambda: candidate.canonical_bytes(candidate.strict_loads('['*2000+'0'+']'*2000))))


for label, mutation in [
    ("tuple_policy_blocks",lambda r:r["policy"]["prepass"].update(blocks=tuple(r["policy"]["prepass"]["blocks"]))),
    ("tuple_policy_polynomial",lambda r:r["policy"]["prepass"]["blocks"][0].update(g=tuple(r["policy"]["prepass"]["blocks"][0]["g"]))),
    ("subclass_policy_blocks",lambda r:r["policy"]["prepass"].update(blocks=ListSubclass(r["policy"]["prepass"]["blocks"]))),
    ("nonjson_policy",lambda r:r.update(policy={"bad":object()})),
    ("set_policy",lambda r:r.update(policy={1,2})),
    ("policy_bool_instead_int",lambda r:r["policy"].update(W=True)),
    ("proof_flag_inside_policy",lambda r:r["policy"].update(producer_execution_verified=True))]:
    def malformed(mutation=mutation):
        r=copy.deepcopy(RECORD);mutation(r)
        return need_reject(lambda:verify(record=r))
    check("reject_record_"+label,malformed)


def cyclic_policy():
    r=copy.deepcopy(RECORD);a=[];a.append(a);r["policy"]={"cycle":a}
    return need_reject(lambda:verify(record=r))


check("reject_record_cyclic_policy",cyclic_policy)


def matching_larger_precision():
    p=POLICY["p"]+7
    pol=candidate.derive_policy(RAW,STATE,T,Q,p=p)
    payload=copy.deepcopy(PAYLOAD);payload["kappa"]=pol["plan"]["kappa"]
    r=candidate.make_record(RAW,STATE,T,Q,payload,p=p)
    require_consistency(verify(record=r,p=p))
    return need_reject(lambda:verify(record=r))


check("actual_fractional_precision_is_caller_bound",matching_larger_precision)


check("independently_recomputed_record_commitments", lambda: require_consistency(
    verify(record=rehash_record(copy.deepcopy(RECORD)))))


def cap_default_precision():
    raw,state=data(3)
    raw['F']=-(2**128-1)
    return need_reject(lambda:candidate.derive_policy(raw,state,2**128-1,2))


check("reject_default_precision_exceeding_explicit_metadata_cap",cap_default_precision)


def boundary_cases():
    count = 0
    for n,b in [(3,3),(63,3),(64,3),(64,64)]:
        raw,state=data(n,b)
        raw.update(F=-(2**127),real=[-(1<<1023)]+[0]*(n-1))
        pol=candidate.derive_policy(raw,state,2,(n-1).bit_length())
        payload={'real':[(1<<8191)]+[0]*(n-1),'imag':[0]*n,'kappa':pol['plan']['kappa']}
        record=candidate.make_record(raw,state,2,(n-1).bit_length(),payload)
        require_consistency(candidate.verify(raw,state,2,(n-1).bit_length(),record,expected_payload=payload))
        count += 1
    return {'admitted_max_width_boundary_cases':count}


check("accepted_exact_domain_boundaries",boundary_cases)


def common_grid_not_substitutable():
    raw=copy.deepcopy(RAW)
    raw.update(F=raw['F']+1,real=[x*2 for x in raw['real']],imag=[x*2 for x in raw['imag']])
    pol=candidate.derive_policy(raw,STATE,T,Q)
    assert pol['input_value_sha256']==POLICY['input_value_sha256']
    assert pol['raw_input_sha256']!=POLICY['raw_input_sha256']
    return need_reject(lambda:verify(raw=raw))


check("equivalent_value_cannot_replace_exact_original_grid",common_grid_not_substitutable)


def moderate_aggregate_budget():
    # A safe 4.8 MB instance demonstrates the aggregate rule without a DoS test.
    value={'malformed':['x'*1200000]*4}
    return need_reject(lambda:candidate.canonical_bytes(value))


check("reject_aggregate_serialized_object_above_budget",moderate_aggregate_budget)


result={"candidate_filename":SOURCE.name,"candidate_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "independent_oracle_sha256":hashlib.sha256((HERE/'independent_oracle.py').read_bytes()).hexdigest(),
        "test_count":len(RESULTS),"passed":sum(x["pass"] for x in RESULTS),
        "failed":sum(not x["pass"] for x in RESULTS),"tests":RESULTS,
        "historical_code_executed":False,"producer_executed":False,"external_writes":False}
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'tests'},indent=2))
for x in RESULTS:
    if not x['pass']:
        print('FAIL',x['name'],x['error'])
