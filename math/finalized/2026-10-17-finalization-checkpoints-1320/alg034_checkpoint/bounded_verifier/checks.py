"""Fresh standard-library controls for the bounded binding contract.

Only the newly authored sibling verifier is imported. Numerical producer
execution is deliberately absent. All inputs and payloads here are synthetic.
"""
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import random
import binding_verifier as v


def run():
    results = []

    def test(name, condition, details=None):
        if not condition:
            raise AssertionError(name)
        result = {"name": name, "pass": True}
        if details is not None:
            result["details"] = details
        results.append(result)

    def denied(name, call, code=None):
        try:
            call()
        except v.Rejection as error:
            test(name, code is None or code == error.code, {"rejection": error.code})
        else:
            raise AssertionError(name + " was not rejected")

    n = 4
    raw = {"F": 5, "real": [3, -2, 0, 4], "imag": [0, 1, -1, 0]}
    state = {"N": n, "B": 3, "a": 1, "beta": 0}
    t, q = 2, 4
    policy = v.derive_policy(raw, state, t, q)
    payload = {"kappa": policy["plan"]["kappa"], "real": [2, -3, 4, 7], "imag": [1, 0, -2, 1]}
    record = v.make_record(raw, state, t, q, payload)
    verdict = v.verify(raw, state, t, q, record, expected_payload=payload)
    test("valid synthetic binding matches exact external payload", verdict["exact_payload_matches_external_reference"] is True)
    test("valid binding never promotes to producer, provenance or numerical acceptance",
         all(verdict[key] is False for key in ("authenticated_provenance", "producer_execution_verified",
             "numerical_error_certificate_verified", "adapter_invoked", "downstream_integration_verified")))
    test("canonical JSON round trip", v.strict_loads(v.canonical_bytes(record).decode()) == record)
    test("domain-separated digests", v.digest("raw-input", raw) != v.digest("payload-grid", raw))

    changed = deepcopy(raw); changed["real"][0] += 1
    denied("wrong raw coordinate", lambda: v.verify(changed, state, t, q, record), "POLICY_MISMATCH")
    changed_f = deepcopy(raw); changed_f["F"] += 1
    denied("wrong raw exponent", lambda: v.verify(changed_f, state, t, q, record), "POLICY_MISMATCH")
    changed_state = dict(state, beta=1)
    denied("wrong state beta", lambda: v.verify(raw, changed_state, t, q, record), "POLICY_MISMATCH")
    changed_order_state = dict(state, a=3)
    denied("wrong state frequency cycle", lambda: v.verify(raw, changed_order_state, t, q, record), "POLICY_MISMATCH")
    denied("wrong caller t", lambda: v.verify(raw, state, t+1, q, record), "POLICY_MISMATCH")
    denied("wrong caller q", lambda: v.verify(raw, state, t, q+1, record), "POLICY_MISMATCH")
    denied("wrong caller actual p", lambda: v.verify(raw, state, t, q, record, p=policy["p"]+1), "POLICY_MISMATCH")
    denied("insufficient actual p", lambda: v.derive_policy(raw, state, t, q, p=policy["p"]-1), "PRECISION")

    for field in ("A", "G", "C", "kappa", "p_min", "I"):
        fake = deepcopy(record)
        fake["policy"]["plan"][field] += 1
        fake = v.assemble_record(fake["policy"], fake["payload"])
        denied("rehashed wrong policy " + field,
               lambda fake=fake: v.verify(raw, state, t, q, fake), "POLICY_MISMATCH")
    fake = deepcopy(record); fake["policy"]["prepass"]["blocks"][0]["g"][0] += 1
    fake = v.assemble_record(fake["policy"], fake["payload"])
    denied("rehashed wrong exact prepass", lambda: v.verify(raw, state, t, q, fake), "POLICY_MISMATCH")
    fake = deepcopy(record); fake["payload"]["real"][0] += 1
    denied("changed payload with stale commitment", lambda: v.verify(raw, state, t, q, fake), "BINDING_MISMATCH")
    fake = deepcopy(record); fake["payload"]["kappa"] += 1
    denied("wrong payload scale", lambda: v.verify(raw, state, t, q, fake), "SCALE")
    for field in ("policy_sha256", "payload_grid_sha256", "payload_value_sha256", "binding_sha256"):
        fake = deepcopy(record); fake[field] = "0" * 64
        denied("wrong " + field, lambda fake=fake: v.verify(raw, state, t, q, fake), "BINDING_MISMATCH")

    # Critical negative control: rehashing a fabricated payload is cheap. A
    # correct consistency verifier must not turn that into numerical acceptance.
    forged = deepcopy(payload); forged["real"][2] = 123456789
    forged_record = v.make_record(raw, state, t, q, forged)
    forged_verdict = v.verify(raw, state, t, q, forged_record)
    test("self-consistent forged payload remains semantically unverified",
         forged_verdict["status"] == "BINDING_CONSISTENT_PRODUCER_UNVERIFIED"
         and not forged_verdict["numerical_error_certificate_verified"])
    denied("forged rehashed payload fails independent exact reference",
           lambda: v.verify(raw, state, t, q, forged_record, expected_payload=payload), "PAYLOAD_REFERENCE_MISMATCH")
    for field in ("authenticated", "genuine_producer", "numerically_certified", "producer_execution_verified"):
        fake = deepcopy(record); fake[field] = True
        denied("self-asserted flag " + field, lambda fake=fake: v.verify(raw, state, t, q, fake), "GRAMMAR")

    equivalent = {"F": raw["F"] + 7,
                  "real": [x << 7 for x in raw["real"]], "imag": [x << 7 for x in raw["imag"]]}
    equivalent_policy = v.derive_policy(equivalent, state, t, q)
    test("regridding preserves dyadic value identity", equivalent_policy["input_value_sha256"] == policy["input_value_sha256"])
    test("regridding does not preserve original representation identity", equivalent_policy["raw_input_sha256"] != policy["raw_input_sha256"])
    denied("equivalent regridding cannot impersonate original raw receipt",
           lambda: v.verify(equivalent, state, t, q, record), "POLICY_MISMATCH")
    equiv_payload = {"kappa": payload["kappa"]-1,
                     "real": [2*x for x in payload["real"]], "imag": [2*x for x in payload["imag"]]}
    test("equivalent payload has equal exact dyadic value",
         v.dyadic_value(equiv_payload, equiv_payload["kappa"]) == v.dyadic_value(payload, payload["kappa"]))
    test("equivalent payload has different grid identity", v.digest("payload-grid", payload) != v.digest("payload-grid", equiv_payload))
    denied("equivalent payload cannot replace actual p-grid representation",
           lambda: v.make_record(raw, state, t, q, equiv_payload), "SCALE")

    zero = {"F": -(1 << 100), "real": [0]*4, "imag": [0]*4}
    zero_record = v.make_record(zero, state, t, q)
    test("all-zero input branch", zero_record["policy"]["outcome"] == "EXACT_INPUT_ZERO")
    test("all-zero canonical exponent", v.dyadic_value(zero, -zero["F"])["scale"] == 0)
    other_zero = dict(zero, F=11)
    test("all-zero values ignore original exponent",
         v.derive_policy(other_zero,state,t,q)["input_value_sha256"] == zero_record["policy"]["input_value_sha256"])
    test("all-zero original representations retain original exponent",
         v.derive_policy(other_zero,state,t,q)["raw_input_sha256"] != zero_record["policy"]["raw_input_sha256"])
    denied("input-zero branch cannot declare producer p", lambda: v.make_record(zero,state,t,q,p=100), "DOMAIN")
    denied("input-zero branch cannot carry forged payload", lambda: v.make_record(zero,state,t,q,payload), "ZERO_BRANCH")
    project_raw = {"F":0,"real":[1,-1,0,0,0,0],"imag":[0]*6}
    project_state = {"N":6,"B":3,"a":1,"beta":0}
    project_record = v.make_record(project_raw,project_state,0,3)
    test("nonzero original projected-zero branch", project_record["policy"]["outcome"] == "EXACT_PROJECTED_ZERO" and project_record["policy"]["W"] == 1)
    test("projected-zero result invokes no adapter", v.verify(project_raw,project_state,0,3,project_record)["adapter_invoked"] is False)
    approximation_zero = {"kappa":payload["kappa"],"real":[0]*4,"imag":[0]*4}
    denied("zero approximation is not original/projected zero", lambda: v.make_record(raw,state,t,q,approximation_zero), "ZERO_APPROXIMATION")
    odd_raw = {"F":0,"real":[1,-1]+[0]*7,"imag":[0]*9}
    odd_state = {"N":9,"B":3,"a":1,"beta":0}
    test("odd parity witness is nonzero", v.derive_policy(odd_raw,odd_state,0,4)["outcome"] == "NONZERO_PLAN")
    test("Phi_12 is not a binomial shortcut", v.cyclotomic(12) == (1,0,-1,0,1))

    for k in (1,2,8,64,512):
        near = {"F":k,"real":[1<<k,-((1<<k)-1)]+[0]*4,"imag":[0]*6}
        plan = v.derive_policy(near,project_state,0,3)
        test(f"near-kernel exact input k={k}", plan["plan"]["A"] == 1 and plan["plan"]["G"] == k+1)

    large_p = 70000
    large_policy = v.derive_policy(raw,state,t,q,p=large_p)
    small_payload = {"kappa":large_policy["plan"]["kappa"],"real":[1,0,0,0],"imag":[0]*4}
    large_record = v.make_record(raw,state,t,q,small_payload,p=large_p)
    test("failed sufficient width bound is not actual overwidth",
         large_record["policy"]["plan"]["sufficient_65536_bit_width_bound"] is False
         and v.exact_payload_width(small_payload) == 1
         and not v.verify(raw,state,t,q,large_record,p=large_p)["adapter_invoked"])

    for case in (True, 1.0, "3"):
        bad = deepcopy(raw); bad["real"][0] = case
        denied("reject raw noninteger " + repr(case), lambda bad=bad: v.derive_policy(bad,state,t,q), "GRAMMAR")
    bad = deepcopy(raw); bad["real"].pop()
    denied("reject truncated raw", lambda: v.derive_policy(bad,state,t,q), "GRAMMAR")
    bad = deepcopy(raw); bad["real"][0] = 1 << 1024
    denied("raw width cap is resource rejection", lambda: v.derive_policy(bad,state,t,q), "RESOURCE_LIMIT")
    bad_state = dict(state, N=65)
    denied("length cap is resource rejection", lambda: v.derive_policy(raw,bad_state,t,q), "RESOURCE_LIMIT")
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1.0}', '{"x":1e3}', '\ud800'):
        denied("reject malformed JSON " + ascii(text), lambda text=text: v.strict_loads(text), "GRAMMAR")
    fake = deepcopy(record); fake["policy"]["prepass"]["modulus"] = tuple(fake["policy"]["prepass"]["modulus"])
    denied("reject tuple substitution inside policy", lambda: v.verify(raw,state,t,q,fake), "GRAMMAR")
    fake = deepcopy(record); fake["policy"]["unexpected"] = float("nan")
    denied("reject nonfinite nested direct-API value", lambda: v.verify(raw,state,t,q,fake), "GRAMMAR")
    cycle = []; cycle.append(cycle)
    denied("cyclic direct-API structure is bounded rejection", lambda: v.canonical_bytes(cycle), "RESOURCE_LIMIT")
    denied("aggregate serialization budget rejects repeated large strings",
           lambda: v.canonical_bytes(["x" * 300000] * 1000), "RESOURCE_LIMIT")
    huge_meta_raw = {"F":-((1<<128)-1),"real":[1,0,0],"imag":[0,0,0]}
    huge_meta_state = {"N":3,"B":3,"a":1,"beta":0}
    denied("derived actual p obeys the same metadata cap as explicit p",
           lambda: v.derive_policy(huge_meta_raw,huge_meta_state,(1<<128)-1,2), "RESOURCE_LIMIT")
    denied("JSON intake applies the structural depth cap",
           lambda: v.strict_loads("[" * 40 + "0" + "]" * 40), "RESOURCE_LIMIT")

    # Independent rational semantics check for canonicalization at modest scales.
    rng = random.Random(3401252)
    for case in range(300):
        count = rng.randrange(1,12)
        nums = {"real":[rng.randrange(-10000,10001) for _ in range(count)],
                "imag":[rng.randrange(-10000,10001) for _ in range(count)]}
        scale = rng.randrange(-30,31)
        normalized = v.dyadic_value(nums,scale)
        multiplier = Fraction(2)**scale
        canonical_multiplier = Fraction(2)**normalized["scale"]
        assert all(Fraction(x)*multiplier == Fraction(y)*canonical_multiplier
                   for part in ("real","imag") for x,y in zip(nums[part],normalized[part]))
        shift = rng.randrange(0,20)
        regrid = {part:[x<<shift for x in nums[part]] for part in ("real","imag")}
        assert v.dyadic_value(regrid,scale-shift) == normalized
    test("300 exact rational canonicalization and regridding controls", True)

    output = {"schema":1,"status":"PASS_BOUNDED_BINDING_CONTROLS",
              "checks":len(results),"randomized_exact_dyadic_cases":300,
              "producer_executed":False,"archived_or_candidate_modules_executed":False,
              "numerical_acceptance_claimed":False,"results":results}
    here = Path(__file__).resolve().parent
    (here/"CHECK_RESULTS.json").write_text(json.dumps(output,indent=2)+"\n")
    (here/"SYNTHETIC_EXAMPLE.json").write_text(json.dumps({"raw":raw,"state":state,"t":t,"q":q,
        "record":record,"verdict":verdict,"warning":"Synthetic payload: no producer generated it."},indent=2)+"\n")
    print(json.dumps({key:output[key] for key in ("status","checks","randomized_exact_dyadic_cases")},sort_keys=True))


if __name__ == "__main__":
    run()
