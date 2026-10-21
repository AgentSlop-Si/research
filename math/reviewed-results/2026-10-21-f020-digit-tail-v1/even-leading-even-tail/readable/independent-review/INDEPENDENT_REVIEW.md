# Independent review: every even leading digit and positive even short tail

## Verdict and exact artifact binding

ACCEPTED WITHIN THE EXACT STATED SCOPE. The uniform proof is valid. No essential repair was supplied by this reviewer, and no candidate or dependency file was changed.

The immutable author candidate is `f020-even-leading-even-tail-candidate-20261021_v1`:

- Manifest SHA-256: `3e8b8d80451bc5a7d720d19e2870926d50473e64ffe26e2ecdcd31eeecdc5004`.
- REPORT.md SHA-256: `6bf682e4b51053e09ff64a9767ea559f1a99a1dcbff7a1b8532c8961dd068183`.
- Exact inventory: 271 manifest-bound files, plus the manifest and seal. Declared directory inventory is exact. There are no unlisted files or symlinks.
- All six copied dependency inventories match their immutable manifest pins and original source packages. All three accepting reviews bind the correct author candidate. Accepted dependency programs and control suites were not executed.

This is mathematical and candidate-artifact acceptance, not acceptance of a future public package, external publication, or delivery.

## Accepted theorem

Let p be an odd prime, c and d be even integers with 2 <= c,d < p, r >= 2, s > r, N=p^r, and q any characteristic-zero primitive p^s-th root. Let n=cN+d and m=d/2. Use precisely the original recurrence

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),

the original Gaussian polynomial H_n, ordinary characteristic-zero derivatives, and the algebraic-square Christoffel-Darboux kernel.

Both P_n and H_n are squarefree. The original algebraic-square kernel is nonzero at every P_n root. There is no exceptional prime, parameter pair, or unresolved root-lifting gate within this scope.

Normalize v(q-1)=1 and set

    B=r(p-1)p^(r-1)/2,
    K=cN/2+cB,
    E=(c-1)N/2+cB,
    D=(c+1)N/2+cB-p=N+E-p.

There are exactly d low roots of X-value 1/2; their derivative value is (n-1)/2. There are cN high roots: exactly cL boundary roots in each of the beta disjoint disks defined in the candidate, with beta=p^floor(r/2) and L=N/beta. At every high root the original derivative value is D+d/2. Each high disk has c distinct residual locations, with L roots counted with multiplicity above each before simplicity is established.

There is no zero root; v(P_n(0))=K+d/2. Corresponding H_n root derivatives have the same valuations, with multiplier residue

    i^(n-1)=(-1)^(c/2+d/2-1)i.

Both c=p-1 and d=p-1 are included, separately and simultaneously. The p=3,c=d=2 case and all accepted c=2 even tails are retained predecessors, as is c=4,d=2. No claim of historical novelty is made.

## 1. Actual general-c authority, not extrapolation

The essential source is the accepted general leading-digit calculation, not the c=2 or c=4 special cases. Its author manifest is `e19104be98018ea10de85dd648b3b2634664150ea24994300e28ac56fe889ec7`; its accepting review manifest is `a7990e625de81f3797ac13bbad7d7c817eb65aee195e5690f84de6ca7540c3c7`. The author report hash is `639b35b0b603fccc44a57c1f5321fc7efc5c9007510b0cd12d714eefc0d5820c`, and the accepting review report hash is `67dc7c923f4e0ace97b9246c9303a2fa3633eeaadea850449a22a9f62c0355f0`.

I read the actual general source Sections 2-5 and 7 and the accepting review's uniform audit. For A=P_(cN), M=P_(cN-1), their full-disk coefficientwise statements give weights K,E,D for A,M,A', respectively, and weight(M') >= E. Their initial polynomials are nonzero scalar multiples of M_c(Zbar), c M_(c-1)(Zbar), and c M_(c-1)(Zbar), with Zbar=alpha Y^L, alpha nonzero. These statements are unconditional for every even c<p, r>=2, s>r. The source's later adjacent-degree simplicity criterion is not a hypothesis of these statements.

The cap R(j)<=W(j)/2 has equality exactly at multiples of N on the required interval. The original ordinary derivative's unique maximizing increment is p^2. ALL equality pairs are retained:

    u=lN, k=lN+p^2, l=1,3,...,c-1.

Their complete normalized sum is c M_(c-1). At c=4 the two contributions are 12 Zbar and 4 Zbar^3; at general c there are c/2 contributions. At r=2 the final pair has k=cN, which is legal and included. At c=p-1 every needed factorial and block multiplier remains a residue unit.

The full M' lower bound covers every ordinary derivative term. Reflection and the cap leave only apparent excesses j=1,p, each at most 1/2. If the lower index is not a multiple of N, the cap is strict. Otherwise parity makes it lN with l even, and the N-level carry gives floor(2a/N)>2 floor(a/N). Half-integrality then removes the excess. This argument also covers p=3,c=2 and c=p-1.

The H/P conversion retains the prefactor derivative term. For A that error has weight at least re+K>D, where e=(p-1)p^(s-1). Hence the A' statement is valid off-root on the full disk, which is essential when evaluating at new tail roots. For M the analogous conversion preserves the lower bound E.

The integer Hermite recurrence and derivative identity give gcd(M_c,M_(c-1))=1 modulo p. The monic resultant product over j<c is correctly signed and is a unit because p>c. Thus the exact values E and D apply at every point of the residual locus M_c(Zbar)=0, not just roots of the earlier polynomial A. No missing general-c coefficientwise lemma remains.

## 2. Exact tail transfer and derivative witness

The original recurrence yields F=P_(cN+d)=T_d A-b_0 U_d M, where b_j=1-q^(cN+j). The associated polynomial starts with U_0=0,U_1=1; consequently U_2=X and U_4=X^3-(b_2+b_3)X. Replacing it by the ordinary tail starting at b_1 would be wrong.

Ordinary differentiation gives the exact fraction-free identity

    S_d=T_d F'-T_d'F
       =T_d^2 A'-b_0(U_d'T_d-U_d T_d')M-b_0 U_d T_d M'.

The square on T_d, both correction terms, and the subtraction of T_d'F are indispensable. All derivative integer factors are retained before reduction. The edges are independent of X.

The inequality n<pN<=p^s holds even at c=d=p-1, since pN-n >= N-(p-1)>0. Thus every recurrence edge and imported denominator is nonzero. The exact leading edge residues are b_0/t^N -> -c and b_j/t -> -j for 1<=j<d, with t=q-1.

## 3. Uniform high-disk estimates and complete high-root count

The matching degree shows that an X^(2k) coefficient of T_(2m) has value at least m-k and an X^(2k+1) coefficient of U_(2m) has value at least m-1-k. Cancellation can only improve these bounds. The unique constant matching gives

    T_d(0)/t^m -> C_m=(2m-1)!!.

Every factor of C_m is below p, including d=p-1. If x is the high-disk Gauss weight of X, then x>=1. Every nonconstant T term has weight at least m+k(2x-1)>m. Therefore T_d/t^m is an analytic unit throughout every high disk, not merely at a selected root.

The ordinary derivatives give weight(U_d)>=x+m-1, weight(T_d')>=x+m-1, weight(U_d')>=m-1, and weight(W_d)>=2m-1 for W_d=U_d'T_d-U_dT_d'. No U or W coefficient is assumed to be a unit.

The perturbation b_0 U_d M is strictly above K+m. Therefore F has the same normalized high residual as C_m A: a degree-cL residual with nonzero constant and higher coefficients of strictly greater weight. Newton-polygon or Weierstrass root counting gives exactly cL roots counted with multiplicity, all on the boundary. This is not simple-root Hensel lifting of the inseparable residual M_c(alpha Y^L).

M_c is separable with c nonzero roots, and Frobenius Y -> Y^L has one preimage per residue root over the algebraically closed residue field, of multiplicity L. Thus there are exactly c residual locations per disk. The beta disk centers have mutual distance valuation below rho, so the disks are disjoint. Their total high-root count is cN.

At each new high root the residual equation permits the source's exact M and A' values. The three witness terms have values

    D+2m,
    at least D+2m+(p-1),
    at least D+2m+(p+x-1).

The two corrections are strictly higher for every allowed parameter. Hence v(S_d)=D+2m. At a root, S_d=T_d F' exactly; division by the already proved tail unit gives v(F')=D+m. This proves simplicity of all cN high roots.

The proof correctly avoids claiming weight(F')=D+m on the entire disk. Away from roots, T_d'F can have lower weight; the fraction-free witness removes it identically.

## 4. Actual central units and harmless cancellations

For r=2, B=p^2-p, mu^2=t^p and epsilon=(-1)^((p-1)/2). The source's actual block units give w_N -> -1, Q_((N-1)/2) -> -1, a_(cN) -> -c, and N_N -> -i^p Y^p under the stated scalings. The Q sign follows from Wilson's identity. The square-root choices cancel because c is even.

The neighbor's original-P scalar is epsilon, not c times epsilon: its factor c cancels with the factor c in a_(cN). The exact derivative-to-neighbor scalar ratio, including the H/P coordinate ratio, gives

    A'(mu Y)/[t^((c+1)B)mu^((c-1)p)]
       -> -c epsilon M_(c-1)(Y^p).

Multiplication by the tail constant in the rootwise witness therefore yields the claimed actual F' unit

    -c C_m epsilon M_(c-1)(Y^p).

Both scalar factors are units; coprimality excludes vanishing at the entire M_c root locus. The c=2 scalar cannot simply be copied to other c. There is no Y^2+1 correction factor here. The adjacent +1 obstruction at M_c(i)=0, including (c,p)=(8,11),(10,19),(16,17), is therefore irrelevant to this even-tail theorem.

The associated Hermite linear coefficient b_m^* satisfies b_m^*=(2m-2)!!+(2m-1)b_(m-1)^*, b_0^*=0. The displayed initial values and cancellations at (d,p)=(6,11),(12,13) are correct. If p divides b_m^*, the first possible U and W coefficients disappear and their lower bounds improve. Further cancellation is harmless for the same reason. Only C_m must be a unit, and it is uniformly so for d<p. The proof does not turn these auxiliary cancellations into exceptional primes or omit them.

## 5. Low roots, endpoint cases, and total exhaustion

With tau^2=t, scale the original polynomial and its ordinary derivative separately. Their integral recurrences reduce to M_j and M_j', respectively, because -(1-q^j)/t reduces to j modulo p, including zero at multiples of p. The integer identity M_p=Z^p modulo p and the zero coefficient at each multiple of p give

    M_(ap+b)=Z^(ap)M_b, 0<=b<p.

For n=cN+d this yields the exact low initial pair

    Q_n -> Z^(cN)M_d(Z),
    R_n -> d Z^(cN)M_(d-1)(Z).

Since d<p, the Hermite recurrence, derivative relation and nonzero constant prove that M_d has d distinct nonzero roots. The resultant and discriminant formulas stated by the author have the correct signs; all possible prime divisors are <=d. Thus d=p-1 is fully covered. Simple-root Hensel lifting is used only at these simple nonzero low residue roots and gives exactly d simple low roots of X-value 1/2 and derivative value (n-1)/2.

These low roots lie outside the high disks, where X-values are at least 1. The counts cN+d=n exhaust the degree. The remaining zero residue at the low scale has therefore been completely accounted for by the high disks; it is not an unexamined cluster.

U_d is odd, so F(0)=T_d(0)A(0), of exact value K+m. There is no omitted or factored-out zero root.

The p=3,c=d=2 specialization is consistent without any new exception: N=9, B=6 at r=2, giving 18 high roots of derivative value 47/2, two low roots of derivative value 19/2, and constant value 22. Its low derivative unit at Z^2=-1 is -2Z, whereas c=4,d=2 gives +2Z. The unsimplified general formula retains the correct sign in both cases. These are proof specializations, not reruns of accepted predecessor controls.

## 6. Original H, all primitive phases, and the kernel

The exact identity H_n(v0^2)=v0^n P_n(v0+v0^(-1)) and its ordinary derivative retain the nP_n/2 term. At a root that term vanishes exactly. All P roots have positive valuation, so none equals +/-2. On the branch near i both coordinate derivatives are units, and the analytic inverse maps the n distinct P roots to n distinct H roots. Degree n exhausts H_n.

The derivative multiplier residue is i^(n-1)=(-1)^(c/2+m-1)i. In particular it is -i for c=2,d=2 but +i for c=4,d=2; a fixed c=2 sign would be incorrect. Valuations agree, not necessarily normalized units.

Every original recurrence edge is nonzero. A common root of consecutive P polynomials would propagate backwards to P_0=1. At a P_n root the original diagonal Christoffel-Darboux identity therefore has nonzero right side P_n' P_(n-1)/w_(n-1). This is the algebraic-square kernel, not an absolute-value-square or positivity argument.

Every valuation statement uses the mixed-characteristic lattice e=(p-1)p^(s-1), retaining integer p-divisibility before residue reduction. Choosing an algebraic p-adic embedding for any primitive phase and using injectivity, or Galois conjugacy, transfers nonvanishing to every characteristic-zero primitive p^s-th root. There is no unsupported auxiliary finite-characteristic simplicity claim.

## 7. Independent controls and immutable evidence

The uniform proof above and the accepted coefficientwise inputs establish the theorem. Finite controls only detect transcription and implementation errors.

The newly written independent control program imports no author or dependency program. It uses exact rational 2-by-2 transition-matrix products, direct recurrence propagation and polynomial differentiation to check tail transfer and the complete witness at d=4,6,10. It rejects omissions of either correction, the missing T square, and omission of T_d'F.

Independent factorial-formula Hermite checks retain all derivative pivots for c=4,6,8,12,16,20. New combined c,d low-residue fixtures cover (p,c,d,r)=(7,4,4,2),(11,10,8,2),(13,10,12,2),(17,16,14,2),(7,6,6,3),(5,4,4,4). The original polynomial and ordinary derivative residues are evolved as separate recurrence states. These checks include both endpoint types and r=2,3,4. They are not high-degree cyclotomic or all-phase scans. Auxiliary-cancellation checks preserve a nonzero decisive C_m at p=11,13,17.

Both the author's NEW control program and the independent program cold-replayed byte-for-byte under normal and optimized Python. Each run was capped at 30 CPU seconds, 45 wall seconds, 512 MiB address space and 16 MiB file size. The independent result hash is `a67dccf860c313a52b44a023e2bb8f4516351f32031e569ec99396ef33b0752c`; the new author result hash is `ec424f537282e774f86c650eef1b01f891f32d1152d86682c38c00aaac373ecb`.

The independently written exact-inventory verifier rejected eight disposable-copy mutations in both Python modes: proof edit, missing file, extra file, bad seal, symlink, fully rehashed replacement under a changed manifest, extra directory, and changed dependency verdict. The original candidate and all dependency packages remained unchanged.

## Scope and remaining gates

No mathematical exception or missing lemma remains for even 2<=c,d<p, r>=2, s>r and odd prime p. This acceptance does not cover odd c or d, c>=p or d>=p, r=1, s<=r, p=2, composite orders, arbitrary/intermediate base-p digit strings, arbitrary n, unrelated finite-characteristic simplicity, global F020/F023 closure, FFT or algorithmic-cost improvement, or historical novelty.

Any public-package transformation or external delivery requires its own exact-byte publication audit. This review performed no external write.
