"""Independent finite controls, not execution of the research implementation."""
import hashlib, itertools, json, random
from pathlib import Path

P = 65537
G = 3
counts = {"factorization_cases": 0, "amplitude_checks": 0, "output_coordinates": 0,
          "heavy_profiles": 0, "final_heavy_needed": 0, "offgrid_coefficients": 0}
rng = random.Random(20261017)

for N in [4,8,16,32,64]:
    k = N.bit_length()-1
    Q = 2**(k//2)
    M = N//Q
    w = pow(G, (P-1)//N, P)
    assert pow(w,N,P)==1 and pow(w,N//2,P)!=1
    eta,theta=pow(w,Q,P),pow(w,M,P)
    for case in range(8):
        modes=[]
        x=[0]*N
        for t in range(Q):
            r = rng.randrange(M//2+1)
            labels = rng.sample(range(M),r)
            a={h:rng.randrange(1,P) for h in labels}
            modes.append(a)
            y=[sum(v*pow(eta,(-h*u)%M,P) for h,v in a.items())%P for u in range(M)]
            for u in range(M): x[t+Q*u]=y[u]
            C=[1]
            for h in labels:
                lam=pow(eta,(-h)%M,P)
                nxt=[0]*(len(C)+1)
                for j,c in enumerate(C):
                    nxt[j]=(nxt[j]+c)%P
                    nxt[j+1]=(nxt[j+1]-lam*c)%P
                C=nxt
            A=[sum(C[j]*y[d-j] for j in range(d+1))%P for d in range(r)]
            for h,v in a.items():
                z=pow(eta,h,P); lam=pow(eta,(-h)%M,P)
                az=sum(c*pow(z,j,P) for j,c in enumerate(A))%P
                cp=sum(j*C[j]*pow(z,j-1,P) for j in range(1,len(C)))%P
                assert cp and (-lam*az*pow(cp,-1,P))%P==v
                counts['amplitude_checks']+=1
        direct=[sum(v*pow(w,j*h,P) for j,v in enumerate(x))%P for h in range(N)]
        for h in range(M):
            for v in range(Q):
                joined=M*sum(modes[t].get(h,0)*pow(w,h*t,P)*pow(theta,v*t,P) for t in range(Q))%P
                assert joined==direct[h+M*v]
                counts['output_coordinates']+=1
        counts['factorization_cases']+=1

for Q,M in [(2,2),(2,4),(4,4),(4,8)]:
    for profile in itertools.product(range(M+1),repeat=Q):
        for K0 in range(Q*M+1):
            for B in range(1,M//2+1):
                total=heavy=0
                for r in profile:
                    heavy += r>B
                    total += r
                    if total>K0: break
                success=total<=K0
                bound=K0//(B+1)+(not success)
                assert heavy<=bound
                counts['heavy_profiles']+=1
                counts['final_heavy_needed'] += not success and heavy>K0//(B+1)

for M in [2,4,8,16,32]:
    eta=pow(G,(P-1)//M,P)
    z=next(v for v in range(2,P) if pow(v,M,P)!=1)
    for u in range(M):
        inner=sum(pow(z*pow(eta,u,P)%P,h,P) for h in range(M))%P
        closed=(1-pow(z,M,P))*pow((1-z*pow(eta,u,P))%P,-1,P)%P
        assert inner==closed and inner!=0
        counts['offgrid_coefficients']+=1

root=Path(__file__).parent
report={"status":"PASS", "scope":"Independent modular identity and integer-accounting controls only", "counts":counts,
        "not_tested":["original implementation", "Berlekamp-Massey implementation", "primary-source algorithm", "asymptotic proof by testing", "floating point", "performance"]}
(root/'CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
