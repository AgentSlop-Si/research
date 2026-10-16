"""Fresh finite controls for the ALG-011 comparison; no inherited program imports."""
import itertools
import json
from pathlib import Path

p, n, q = 5, 4, 2
E = [[0] * n for _ in range(n)]
F = [[pow(q, i*j, p) for j in range(n)] for i in range(n)]
J = [[0] * n for _ in range(n)]
for i in range(n):
    E[i][i] = -pow(q, i, p) % p
    if i + 1 < n:
        E[i][i+1] = -pow(q, i, p)*(pow(q, i+1, p)-1) % p
    J[i][(i+1) % n] = (pow(q, -i-1, p)-1) % p
    J[i][(i+2) % n] = -pow(q, -i-1, p) % p

def mv(A, x):
    return [sum(a*b for a,b in zip(row,x)) % p for row in A]

def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(n)) % p
             for j in range(n)] for i in range(n)]

def min_recurrence(x):
    for L in range(len(x)+1):
        for c in itertools.product(range(p), repeat=L):
            if all((x[j]+sum(c[i-1]*x[j-i] for i in range(1,L+1))) % p == 0
                   for j in range(L,len(x))):
                return L, [1,*c]

assert mm(F,E) == mm(J,F)
results = {"field":5,"N":4,"q":2,"FE_equals_JF":True,"fixtures":[]}
for name,x,lam,expected_y in [
    ("exceptional_zero_defect",[1,3,1,0],1,[0,1,4,4]),
    ("dense_zero_defect",[1,2,2,1],2,[1,1,0,2])
]:
    ex=mv(E,x); residual=[(a-lam*b)%p for a,b in zip(ex,x)]
    y=mv(F,x)
    assert residual == [0]*n and y == expected_y
    L,c=min_recurrence(x)
    assert L==2
    out=dict(name=name,x=x,shift=lam,Ex=ex,residual=residual,
             DFT=y,input_support=sum(a!=0 for a in x),defect_cap=0,
             finite_input_minimal_LFSR_order=L,connection=c)
    if name == "exceptional_zero_defect":
        h=[0,1]
        for i in range(n-1):
            h.append(((1-pow(q,i+1,p))*h[i+1]-lam*pow(q,i+1,p)*h[i])%p)
        closure=[h[n],(1+lam*h[n-1])%p]
        t=next(t for t in range(n) if (-pow(q,t,p))%p==lam)
        sep=sum(pow(q,-i*t,p)*h[i] for i in range(n))%p
        assert closure == [0,0] and sep != 0 and sep == n*x[t]%p
        out.update(h=h,closure_coefficients=closure,eigenindex=t,
                   actual_input_coordinate=x[t],separating_sum=sep,
                   both_zero_and_x_have_same_forcing_and_y0=True)
    results["fixtures"].append(out)

# Derived ledger arithmetic, not runtime or inherited-code verification.
for N in [4,8,128,8192,131072]:
    R=N-1; d=1
    zero=(6*N-4)+2*R+(2*N-1)*d+(4*N-3)
    ordinary=(6*N-4)+2*R+2+2*N+(2*N-1)*d+(13*N-5)
    assert zero==14*N-10 and ordinary==25*N-10
results["derived_dense_one_defect_ledger_identities"]="PASS: zero 14N-10; ordinary 25N-10"
results["execution_scope"]="Only this newly authored finite mathematical control was run. No supplied implementation was executed."
Path(__file__).with_name("MATH_CONTROL_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
