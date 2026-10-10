"""Independent rank-one quasiseparable UNITARY positive control.

A single adjacent-Givens chain is unitary, qsep order one, and O(N) gates.
Its mixing entropy is too small to be a complete Fourier transform. This
checks a known Ailon-model argument, not a new lower bound on nonunitary FFTs.
"""
import math,json
from exact_scan_macro import P,rank_mod


def entropy(matrix):
    return -sum((v*v)*math.log2(v*v) for row in matrix for v in row if abs(v)>1e-15)


def run(ns=(4,8,16,32)):
    report=[]
    p=P
    inv5=pow(5,-1,p)
    cm=3*inv5%p;sm=4*inv5%p
    for n in ns:
        exact=[[int(i==j) for j in range(n)] for i in range(n)]
        approx=[[float(i==j) for j in range(n)] for i in range(n)]
        entropies=[entropy(approx)]
        for idx in range(n-1):
            a,b=exact[idx][:],exact[idx+1][:]
            exact[idx]=[(cm*x+sm*y)%p for x,y in zip(a,b)]
            exact[idx+1]=[(-sm*x+cm*y)%p for x,y in zip(a,b)]
            a,b=approx[idx][:],approx[idx+1][:]
            approx[idx]=[(3*x+4*y)/5 for x,y in zip(a,b)]
            approx[idx+1]=[(-4*x+3*y)/5 for x,y in zip(a,b)]
            entropies.append(entropy(approx))
        max_cutrank=0
        for s in range(1,n):
            ru=rank_mod([row[s:] for row in exact[:s]])
            rd=rank_mod([row[:s] for row in exact[s:]])
            max_cutrank=max(max_cutrank,ru,rd)
        # Exact orthogonality over finite field: because (3/5)^2+(4/5)^2=1.
        for i in range(n):
            for j in range(n):
                assert sum(exact[k][i]*exact[k][j] for k in range(n))%p==int(i==j)
        assert max_cutrank==1
        differences=[entropies[i+1]-entropies[i] for i in range(n-1)]
        assert max(differences)<=2+1e-10
        report.append({'n':n,'unitary_givens_gates':n-1,
                       'maximum_quasiseparable_offdiagonal_rank':max_cutrank,
                       'final_entropy_bits':entropies[-1],
                       'target_fourier_entropy_bits':n*math.log2(n),
                       'maximum_entropy_increase_per_gate':max(differences)})
    return report

if __name__=='__main__':print(json.dumps(run(),indent=2))
