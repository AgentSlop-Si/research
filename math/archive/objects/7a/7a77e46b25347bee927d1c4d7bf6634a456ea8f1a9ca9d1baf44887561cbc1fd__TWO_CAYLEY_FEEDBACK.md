# A constructive quadratic feedback family and its exact Fourier obstruction

## Result

There is an explicit, uniform family inside the four-plan paired-Green architecture with a genuinely quadratic loop minimal polynomial, including choices where both maps are dense and every nontrivial cycle weight is nonzero. Its Fourier covariance fails structurally for every even N>9, hence every dyadic N>=16. A degenerate one-Cayley specialization can pass the Fourier seed exactly at all even lengths, yet fails covariance for N>4. This closes one concrete construction branch; it is not an obstruction to independent-cycle paired-Green feedback or a faster FFT.

No uploaded program was executed. The supplied package was read as source; the controls in this folder are newly authored.

## Source provenance

Source Library identity: [private-id].
Resolved filename: fft_annihilator_closed_feedback_2026-10-10.zip.
Underlying file ID: [private-id].
Size: 115,988 bytes; created 2026-10-09T23:24:20.272285Z.
ZIP SHA-256: 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9.
Read member: fft_annihilator_closed_feedback/THEORY.md.
Member SHA-256: 4e3bb89d715175ae2e57271228aabf4db4f45895a1e879ade826bab4fe21ff7c.

The source supplies the general feedback certificate, annihilator evaluator, paired-Green class, pure-Green obstruction, and generic degree-N statement. The Cayley family and scoped obstruction below are deductions for this investigation. No external novelty claim is made. The source's dense-Fourier positive controls are not constructive examples for the claimed fast algorithm, and its random degree-N controls are not rerun or counted here.

## 1. Definitions and guards

Work over a field E with char(E) not dividing N and with a specified primitive Nth root omega. Let N>=2 be even. This implies char(E) != 2. Fourier conventions are F[i,j]=omega^(ij), S e_j=e_(j+1), and D=diag(omega^i), so F S=D F.

Choose any Hamiltonian cycle pi on N coordinates. Use the row-action convention

    (W x)[i] = w[i] x[pi(i)],   W=diag(w) P_pi.

Zero edge weights are allowed. Write rho=product_i w[i], so W^N=rho I. Choose a parity diagonal E=diag(e[i]) with e[i] in {+1,-1} alternating along pi. Because the cycle has even length, E exists and satisfies E^2=I and E W E=-W. Both parity classes are nonempty.

For a scalar c satisfying 1-c^N rho != 0, define

    C_c=(I+cW)(I-cW)^(-1)=2(I-cW)^(-1)-I.

For even N, det(I+cW)=det(I-cW)=1-c^N rho, so C_c is invertible. Moreover

    E C_c E=C_c^(-1)=C_(-c).

Choose a,b,lambda with

    1-a^N rho != 0,
    1-b^N rho != 0,
    lambda != 0,
    lambda^2 != 1.

These are the complete algebraic guards used below. Define

    A=C_a,
    B=lambda C_b E.

Each is a sum of exactly two allowed Green plans:

    A=2(I-aW)^(-1)-I,
    B=2lambda(I-bW)^(-1)E-lambda E.

The second term is a valid zero-edge-weight Hamiltonian Green plan with diagonal endpoint factors. The endpoints displayed here are nonsingular because char != 2 and lambda != 0. All four plans can use the same cycle order. The general proposal permits independent orders, so this same-order family is a legitimate, narrower subclass.

## 2. Exact quadratic closure

All rational functions of W used here commute with each other. They do not generally commute with E. Put R=C_b C_a^(-1). Then

    BA=lambda C_b E C_a=lambda C_b C_a^(-1)E=lambda R E.

Because E R E=R^(-1),

    (BA)^2=lambda^2 R E R E=lambda^2 I.

The loop is not scalar. If lambda R E were scalar, then R would be a nonzero scalar multiple of E. Since R commutes with W, E would commute with W; combined with E W=-W E and char != 2, this forces W=0. But W=0 gives R=I and BA=lambda E, which is not scalar because both parity classes are nonempty. Thus the minimal polynomial is exactly

    mu(z)=z^2-lambda^2.

Its value at 1 is 1-lambda^2 != 0. Hence H=I-BA is invertible, as is B. The transfer T=H^(-1)B is invertible and

    T=(B+BAB)/(1-lambda^2)
     =[lambda C_b E+lambda^2 C_a^(-1)]/(1-lambda^2).       (1)

The orientation in this calculation matters:

    BAB=lambda^2 C_b C_a^(-1) E C_b E=lambda^2 C_a^(-1).

We have not commuted E through a Cayley factor without replacing that factor by its inverse. Nor is B p(BA) substituted for p(BA) B.

## 3. Uniform cost and concrete non-oracle instance

A weighted Hamiltonian Green inverse is applied by a constant number of scans, including when individual edge weights vanish. Therefore each A and B application costs O(N), and their four plans need O(N) setup and storage from supplied weights and cycle order. The quadratic annihilator is available from lambda alone; there is no Krylov discovery or dense elimination. The feedback output uses one initial B application, then A and B, followed by a vector combination, so its cold cost is O(N) whenever all parameter and cycle generation costs are O(N).

For an explicit characteristic-zero family for every even N, choose the natural cycle, every w[i]=1, a=2, b=3, and lambda=2. Both guards 1-2^N and 1-3^N are nonzero. Both maps have nonzero off-diagonal entries, are dense, and are uniformly generated from fixed constants in O(N) work. This is a genuine linear-time non-Fourier operator family with exact quadratic closure; it contains no Fourier oracle.

These exact-arithmetic claims do not assert good numerical conditioning. They do not establish the Fourier certificate.

## 4. Fourier support-product lemma over the stated fields

For every nonzero vector x, put s=|supp(x)| and t=|supp(F x)|. Then s t >= N.

Proof. Let M be the circulant matrix whose columns are cyclic shifts of x. Fourier diagonalization over the given splitting field shows rank(M)=t. Choose t columns forming a column-space basis. Every column has exactly s nonzero entries. Every row of M has at least one nonzero entry because x != 0. Therefore every row must be covered by the supports of those t basis columns: if all basis columns vanished in one row, every column would vanish in that row. Their support union has size at most st, so N<=st. This proof uses only invertibility of F, supplied by char(E) not dividing N and a primitive root. It does not use complex absolute values or a complex-only uncertainty theorem. QED.

The same lemma applies to a nonzero row vector x and x F, because F is symmetric.

## 5. Structural covariance obstruction

Set

    P=(I-bW)(I+aW).

P is invertible. Each row of P has support at most three: its own coordinate, pi(i), and pi^2(i). Multiplying (1) on the left by P, with the parity diagonal kept on the right, gives

    P T=[lambda(I+aW)(I+bW)E
         +lambda^2(I-bW)(I-aW)]/(1-lambda^2).            (2)

Thus every row of PT also has support at most three, since multiplication on the right by a diagonal does not change support. Cancellations or coincident positions can only lower these bounds.

Suppose Fourier covariance D T=T S held. From its columns,

    T[:,j]=D^j T[:,0],

so T=L F for a diagonal L. Since T is invertible, every diagonal entry of L is nonzero. Consequently PL is invertible, and every row x of PL is nonzero with support at most three. By (2), x F is a row of PT with support at most three. The support-product lemma forces

    N <= |supp(x)| |supp(x F)| <= 9.

Therefore Fourier covariance is impossible for all even N>=10, including every dyadic N>=16. The source's cubic certificate C1 is equivalent to covariance under the established feedback-invertibility guards, so it fails too. This obstruction does not need the seed condition.

If a=0 or b=0, the denominator can be chosen with degree one in W, and the same reasoning gives N<=4. In particular, the one-Cayley specialization fails already at every even N>=6.

This proof excludes all choices of weights, parity choice, cycle order, a,b,lambda in this family satisfying the guards, including zero weights and all cancellation branches. It does not exclude two independently ordered noncommuting Cayley factors, arbitrary sums of independently ordered Green maps, or any general exact arithmetic Fourier algorithm.

## 6. Seed-passing negative control at every even length

Over characteristic zero take a=0, b=1, lambda=2 and the natural row cycle pi(i)=i+1 mod N, with E[0,0]=1. Define

    g[0]=-5/4,    g[i]=-3/4 for i != 0,
    w[0]=3,      w[N-1]=3/5,
    w[i]=1 for 1<=i<N-1.

For N=2 the middle range is empty; the same two distinct endpoint weights apply. Directly, (I-W)g=e0 and rho=9/5, so the Green guard is 1-rho=-4/5 != 0. Since A=I,

    T=-(2/3)(C_1 E+2I).

As E e0=e0 and C_1 e0=2g-e0, the zeroth output entry is

    -(2/3)(2(-5/4)+1)=1,

and each remaining entry is

    -(2/3) 2(-3/4)=1.

Thus T e0=ones exactly. Equivalently H ones=B e0, so the source's seed C2 passes. Nevertheless C1 fails for N>4 by the theorem. This is a uniform, all-nonzero-weight counterexample to treating exact quadratic closure plus the correct seed as enough for Fourier correctness.

The same control works over finite fields where 2,3,5 are invertible, the chosen length is nonzero, and a primitive Nth root exists; specifically p=65537 at the tested dyadic lengths.

## 7. Own exact controls and acceptance status

The newly authored check_two_cayley.py tests the formulas over F65537 at dyadic N=2,4,8,16,32,64, with natural and reverse-index cycle lists and deterministic variable nonzero weights. It compares each independently implemented scan on every basis vector with direct inverse matrices, verifies quadratic closure and non-scalar loops, checks the oriented transfer identity and sparse multiplied identity, and checks covariance rejection at the proved sizes. A separate fixed family verifies the seed-passing negative control.

The test script constructs dense matrices only as verification oracles for this theorem. They are not the parameter generator or the proposed O(N) evaluator. Uploaded source code is neither imported nor executed. The completed run passed all 18 cases: 12 two-Cayley cases and six seed-passing controls; 378 basis vectors; 49,140 A/B/T output entries; 18 exact quadratic/non-scalar checks; 18 sparse multiplied identities; and 18 cubic residual identities. Actual per-case data and terminal status PASS are recorded in TWO_CAYLEY_RESULTS.json.

Acceptance status: constructive quadratic-closure family supplied; uniform generation supplied; correct operator orientation proved; Fourier compatibility disproved within this family. This is a scoped negative research result, not a positive FFT construction.

## 8. What a next construction must change

The obstacle is the common weighted-cycle rational algebra: a bounded-degree sparse denominator remains after closure, and Fourier covariance cannot fit its sparse numerator. Merely tuning its weights, alternating signs, or Cayley parameters cannot fix it. A candidate must leave this particular common-cycle rational form, for example through genuinely independent noncommuting orders or a map family without this low-row-support denominator/numerator certificate. Such a change removes this proof's premise only; it does not supply Fourier phases or a low-degree annihilator.
