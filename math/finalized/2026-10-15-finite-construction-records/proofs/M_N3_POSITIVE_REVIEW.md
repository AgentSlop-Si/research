# Independent N=3 complex positive certificate

10 October 2026 UTC. Verdict: accepted as a constant-size algebraic control. The quadratic-root operation is explicit; this is not an asymptotic FFT construction or a modular-to-complex existence inference.

Let w be either primitive complex cube root, F[i,j]=w^(ij), A=diag(1,w^2,w^2), and B=(A+F^(-1))^(-1). Direct exact inversion in Q(w), w^2+w+1=0, gives

    B = [[a,b,b],[b,d,e],[b,e,d]],
    d=(-1+9w)/14=(-17-16w)/(4+26w),
    e=(-3-w)/14=(1-4w)/(4+26w),
    a=w^2 d, b=w e.

In particular d and e are nonzero and e/d=(3+4w)/13. Choose either root

    t=(-1 +/- sqrt(1+8e/d))/2,

so t^2+t=2e/d, and put kappa=d(1-t^3)/2 and D=diag(w,1,1). For a 3-cycle permutation matrix P, the inverse identities give

    (I-tP)^(-1)+(I-tP^(-1))^(-1)
      = [2I+(t+t^2)(P+P^2)]/(1-t^3).

Therefore

    B = kappa D [(I-tP)^(-1)+(I-tP^(-1))^(-1)] D.

Each term is an allowed Hamiltonian weighted-permutation Green term with nonsingular diagonal endpoints. To check the Green guards, t^3=1 would force t=1 or a primitive cube root. These alternatives give t+t^2=2 or -1, hence e/d=1 or -1/2, respectively. The displayed e/d has neither value for primitive complex w. Thus both roots satisfy 1-t^3!=0, kappa!=0, and D is invertible. Also e!=0 ensures t is nonzero. No zero-mask or singular branch is needed.

The independently authored checker reconstructs the target by matrix inversion over Q(w), verifies all nine entries, and works in the formal quadratic algebra with t^2+t=2e/d. It verifies the nonzero norm of 1-t^3, namely (7860+4344w)/2197, certifying the guard for both algebraic roots without numerical approximation. Four supplementary numerical controls cover both roots of w and both roots of t. Only reviewer-authored code was executed.

This certificate was supplied by the root research worker as an algebraic candidate and was independently derived and verified here. It does not extend to the unrelated fixed-order N=13 exclusion or establish a scalable family.
