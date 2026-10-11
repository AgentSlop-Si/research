# Publication adaptation of reviewer-authored checker.
# Original SHA-256: f0598a6327a98b152d1f52922b8b51a1cbb2d7511d0680ad14aa6c904349560d
# Changes: Extracted unchanged exact exponent/proof-control portion; omitted workspace-specific source metadata generation.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
# Integer congruences prove the phase identities exactly. No floating arithmetic or source code import.
n=8;m=16
chirp=[((-r*r+(r-j)**2-j*j)-(-2*r*j))%m for r in range(n) for j in range(n)]
period=[((t+n)**2-t*t)%m for t in range(n)]
a=[(-t*t)%m for t in range(n)]
# p* leading exponent is 0; p leading exponent is 15, so p*=zeta*p if all roots are unit.
lam=(-a[-1])%m
lhs=(-a[n-2])%m
rhs=(lam+a[1])%m
assert all(x==0 for x in chirp+period)
assert a[0]==0 and a[-1]==15 and lam==1 and lhs==4 and rhs==0
assert lhs!=rhs
checks=dict(status='passed exact integer exponent checks',coefficient_field='Q(zeta), zeta a primitive 16th root',N=n,
 chirp_identity_checks=len(chirp),all_chirp_exponent_differences_zero_mod_16=all(x==0 for x in chirp),
 periodicity_checks=len(period),all_periodicity_differences_zero_mod_16=all(x==0 for x in period),
 p_coefficient_exponents_mod_16=a,
 self_reciprocal_test=dict(forced_scalar_exponent=lam,z_coefficient_of_p_star_exponent=lhs,z_coefficient_of_zeta_p_exponent=rhs,contradiction='zeta^4 = i differs from zeta^0 = 1'),
 nonzero_weights_proof='p has degree seven and nonzero constant coefficient; its seven roots are finite and nonzero, and alpha is their reciprocal.',
 guards_proof='C=D^{-1} F8 D^{-1} is invertible, so p(P)=8 C^{-1} is invertible. Factoring p(P) into seven square factors forces every I-alpha P invertible, equivalently alpha^8 != 1.',
 limitations='These checks validate the elementary comparison exponents only. They do not replay the Phase44 interval proof, compute polynomial roots, or certify a new architecture.')
(OUT/'EXACT_COMPARISON_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Exact comparison exponent controls passed. No interval replay or source-corpus scan performed.')
