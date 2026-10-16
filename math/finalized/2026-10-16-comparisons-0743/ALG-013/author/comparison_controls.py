"""New exact controls for comparison boundaries; no imported research code."""
from fractions import Fraction as F
import json
from pathlib import Path

def g(x, y=0): return (F(x), F(y))
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def power(a,n):
    out=g(1)
    for _ in range(n): out=mul(out,a)
    return out
def dft4(x,sign=1):
    root=g(0,sign)
    return [sumg(mul(g(x[j]),power(root,j*k)) for j in range(4)) for k in range(4)]
def sumg(seq):
    out=g(0)
    for a in seq: out=add(out,a)
    return out
def enc(z): return [str(z[0]),str(z[1])]

x=[1,2,3,6]
assert x==[a*b for b in (1,3) for a in (1,2)]
X=dft4(x)
assert X==[g(12),g(-2,-4),g(-4),g(-2,4)]
det=sub(mul(X[0],X[3]),mul(X[1],X[2]))
assert det==g(-32,32)
# A unitary negative transform differs by a sign permutation and sqrt(4)=2.
y=[mul(g(F(1,2)),z) for z in dft4(x,-1)]
assert X==[mul(g(2),y[(-k)%4]) for k in range(4)]
# Direct even/odd subproblem sharing, computed without any research implementation.
T=[g(1+3),g(1-3)]
shared=[mul(add(g(1),mul(g(2),power(g(0,1),k))),T[k%2]) for k in range(4)]
assert shared==X
recurrence_controls=[]
for d in range(1,9):
    N=2**d
    e=[int(j==N-1) for j in range(N)]
    tensor=[int(all((j>>l)&1 for l in range(d))) for j in range(N)]
    assert tensor==e
    # For each L<N the final recurrence row has zero predictors and target 1.
    assert all(e[N-1]==1 and all(e[N-1-i]==0 for i in range(1,L+1)) for L in range(N))
    recurrence_controls.append({'N':N,'shortest_finite_LFSR_length':N,'zero_predictor_obstruction_verified':True})

result={'scope':'Comparison-boundary controls only; not a new correctness acceptance or source-program replay',
        'rank_one_input':x,'positive_explicit_dft':[enc(z) for z in X],
        'output_QTT_unfolding_determinant':enc(det),'output_QTT_rank':2,
        'negative_unitary_sign_scale_mapping':True,'shared_even_odd_subproblem_identity':True,
        'dense_input_terms':len(x),'all_outputs_nonzero':all(z!=g(0) for z in X),
        'finite_recurrence_separators':recurrence_controls,'passed':True}
Path(__file__).with_name('COMPARISON_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
