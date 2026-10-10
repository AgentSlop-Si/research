"""Windowed Fourier rank obstructions for two quasiseparable stages.

B = F[:, :] @ C[:, perm], where C invertible; F has a primitive Fourier root
and may have its output rows independently reordered. Input coordinates must
be in natural Fourier order. All indices zero based.

The `check_windows` routine uses only necessary inequalities. A pass is NOT a
factorization, and none of these results proves an FFT complexity bound.
"""
from __future__ import annotations
from collections import Counter
from itertools import permutations
from random import Random


def old_bilateral_required_rank_sum(perm):
    n = len(perm)
    return max((max(min(t, n-1-max(perm[-t:])),
                     min(t, min(perm[:t]))) for t in range(1, n)), default=0)


def inequalities_for_window(perm, u, v, C_up=1, C_down=1,
                            B_up=1, B_down=1):
    n = len(perm)
    assert sorted(perm) == list(range(n))
    assert 0 <= u <= v < n
    segment = perm[u:v+1]
    a, b = min(segment), max(segment)
    t = v-u+1
    bcost = (B_up if u>0 else 0) + (B_down if v<n-1 else 0)
    cup = C_up if a>0 else 0
    cdown = C_down if b<n-1 else 0
    return [
       {"type":"head", "required":min(t,a), "budget":bcost+cup,
        "u":u,"v":v,"a":a,"b":b},
       {"type":"tail", "required":min(t,n-1-b), "budget":bcost+cdown,
        "u":u,"v":v,"a":a,"b":b},
       {"type":"both", "required":min(t,n-1-(b-a)),
        "budget":bcost+cup+cdown,
        "u":u,"v":v,"a":a,"b":b},
    ]


def check_windows(perm, C_up=1, C_down=1, B_up=1, B_down=1):
    n=len(perm)
    assert sorted(perm)==list(range(n))
    violations=[]
    for u in range(n):
       a=n; b=-1
       for v in range(u,n):
          a=min(a,perm[v]);b=max(b,perm[v]);t=v-u+1
          bcost = (B_up if u>0 else 0) + (B_down if v<n-1 else 0)
          cup = C_up if a>0 else 0
          cdown = C_down if b<n-1 else 0
          gates=[('head',min(t,a),bcost+cup),
                 ('tail',min(t,n-1-b),bcost+cdown),
                 ('both',min(t,n-1-(b-a)),bcost+cup+cdown)]
          for name, required,budget in gates:
             if required>budget:
                violations.append({"type":name,"u":u,"v":v,
                  "a":a,"b":b,"required":required,"budget":budget})
    return violations


def combinatorial_ceiling(C_up, C_down, B_up, B_down):
    # Each interior window of length m needs an item from each extreme m-set.
    d_tail=C_down+B_up+B_down
    d_head=C_up+B_up+B_down
    m_tail=d_tail+1; m_head=d_head+1
    return {"head_markers":m_head,"tail_markers":m_tail,
        "maximum_length_by_head":m_head*m_head+m_head+1,
        "maximum_length_by_tail":m_tail*m_tail+m_tail+1,
        "necessary_maximum_n":min(m_head*m_head+m_head+1,
                                  m_tail*m_tail+m_tail+1)}


def enumerate_n8():
    totals=Counter()
    witnesses={}
    for p in permutations(range(8)):
        old_ok=old_bilateral_required_rank_sum(p)<=2
        violations=check_windows(p)
        new_ok=not violations
        totals[(old_ok,new_ok)] += 1
        if old_ok and not new_ok and 'new_rejection' not in witnesses:
            witnesses['new_rejection']={"perm":list(p), "violation":violations[0]}
    return {
        "number_of_permutations":40320,
        "old_only_survivors":totals[(True,True)]+totals[(True,False)],
        "window_survivors":totals[(True,True)]+totals[(False,True)],
        "survived_both":totals[(True,True)],
        "rejected_new_beyond_old":totals[(True,False)],
        "new_pass_old_fail":totals[(False,True)],
        "witnesses":witnesses,
    }


def random_screen(n=16, samples=2000, seed=20261009):
    rng=Random(seed)
    old=new=0
    for _ in range(samples):
        p=list(range(n));rng.shuffle(p)
        if old_bilateral_required_rank_sum(p)<=2:
            old+=1
            if not check_windows(p):new+=1
    return {"n":n,"samples":samples,"seed":seed,
            "old_survivors":old,"survive_both":new,
            "note":"Monte Carlo only; zero survivors is NOT a proof of emptiness."}


if __name__ == '__main__':
    import json
    print(json.dumps({"n8":enumerate_n8(),
         "rank_one_length_bound":combinatorial_ceiling(1,1,1,1),
         "rank_two_length_bound":combinatorial_ceiling(2,2,2,2),
         "n16_example":{
             "perm":[8,0,13,4,9,3,15,5,6,1,12,11,10,2,14,7],
             "passes":not check_windows([8,0,13,4,9,3,15,5,6,1,12,11,10,2,14,7])}},indent=2))
