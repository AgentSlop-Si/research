# Original ranked theorem re-audit: C01 and F015

Date: 10 October 2026. Scope: the original exact-five-dimensional Green theorem and the complete original growing-fiber Fourier theorem. This is not a substitution of the newer S2 recognizer for F015.

## Result and precise closure

**C01 survives in its stated arithmetic five-dimensional grammar.** The decisive finite lower certificate has now been reconstructed from the equations by a freshly authored exact checker. Its 576 ordered cycle pairs, 4,320 nonsingular transition equations, 384 empty row domains, and 624 remaining branches are all accounted for. Every remaining branch has coefficient rank 10 and augmented rank 11. All 3,120 column constraints have rank one. The reconstruction includes infinity and vanishing base coordinates. The uniform upper construction's 27 guard residues and both quadratic-root reconstructions were freshly checked, and its two generic polynomial identities were independently expanded over the integers. The characteristic-zero and infinite-parameter conclusions follow from the uniform proofs below, not from extrapolating sample computations.

**F015 survives as a deterministic exact-field structured-input recognition and transform theorem.** The full per-fiber cap theorem, aggregate-budget extension, guarded Green variant, setup/output charges, growing-budget corollaries and coverage limits have been re-audited. A newly authored implementation supplies fresh controls: 615 cap cases, 1,750 aggregate cases, 2,981 charged heavy-fiber fallbacks, 36,848 checked explicit output coordinates, and 39 valid Green identities. These are controls of our own implementation, not historical execution claims.

An explicit guard counterexample sharpens the retained qualification: over F17 with N=16 and primitive root 3, L=7I+D+2S is invertible with determinant 16, but d_3=7+3^3=0. The declared divide-by-diagonal Green scan cannot run. The source correctly requires stronger local and closure guards; invertibility alone cannot replace them.

No substantive counterexample was found within either stated theorem. No supplied research program was executed, imported, compiled, or AST-parsed. All fresh programs in this package were authored from displayed mathematical statements and use the standard library, importing only another fresh checker where explicitly identified.

## 1. Provenance and evidence levels

SOURCE_MANIFEST.json identifies original statements and the exact historical dependencies by path, size and SHA-256. The central original texts are:

- C01 lower: N5_EXHAUSTIVE_DIAGONAL_ENDPOINT_EXCLUSION.md, with historical review hash aa91fdec5f08cc03e33652869d41be9f9a53bf3c37838c2d5f8d58532dd54586.
- C01 restriction: PRINCIPAL_RESTRICTION_AND_INFINITE_SUBFAMILY.md.
- C01 upper: THREE_GREEN_RESTRICTED_FAMILY.md, with historical review hash 985eab459973fab307ec4081560238fb604d80b9c5b7d14b6d16252d71bbc12b.
- F015 original THEORY.md: a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045; historical review: 77803ddc6aeb79ee42a1e22c6048090d00db98886db1aef3214c4a9240e70e2b.

Original statements and relevant reviews were read as text. The lower checker derives its own finite target, cycles, forests, quadratic domains and nonzero minors; it does not load the historical certificate. The upper checker recomputes its residues from the target and the displayed formulas. The F015 checker implements the cap and aggregate paths independently and compares against a direct DFT.

Historical characteristic-zero sample reconstructions, original software logs, source instruction traces, large operation profiles and hardware measurements were not replayed. In particular, the historical 7,516,160 versus 7,340,032 arithmetic comparison remains attributed evidence. None is a missing premise of the mathematical theorems proved below. External priority and external peer review remain unresolved.

## 2. C01: exact theorem and grammar

Let q be a positive odd integer, gcd(q,5)=1, q=1 modulo 241. Set N=5q², supply a primitive complex Nth root omega, and define

F_N[i,j]=omega^(ij), A_N[j,j]=omega^((N+1)j²/2), B_N=(F_N^(-1)+A_N)^(-1).

On S=(0,q²,2q²,3q²,4q²), put C_q=B_N[S,S] and eta=omega^(q⁴). Let K=Q(eta). The allowed five-dimensional summand is

L(I-W_sigma)^(-1)R,

where sigma is a Hamiltonian cycle of the fixed five coordinates, (W_sigma x)_i=w_i x_sigma(i), all w_i are arbitrary, 1-product(w_i) is nonzero, and L,R are diagonal, possibly singular. Zero edge weights are allowed. Unmatched row/column permutation endpoints and product architectures are not in this grammar.

**Theorem C01.** The minimum number of allowed summands for C_q is exactly three over an explicit genuine quadratic extension E_q/K. The lower bound holds even over C and with all endpoint masks; the displayed upper factors have nonsingular endpoints. A three-term upper bound over K alone is not proved. Only the dimension-five block is constructed. No upper representation for full B_N at q>1, no all-N theorem, and no FFT speedup follow.

### 2.1 Target formula without an inherited Gauss-sign premise

For odd N, write h=(N+1)/2 and G=sum_j omega^(hj²). Completing the square gives

(A_N F_N)²=G times Fbar_N A_N^(-1)=NG (A_N F_N)^(-1).

Thus (A_N F_N)³=cI, c=NG. Multiplying (I+A_N F_N) by I-A_N F_N+(A_N F_N)² gives (1+c)I. Consequently, whenever 1+c is nonzero,

B_N[i,j]=[omega^(ij)-G omega^(-h(i+j)²)+c omega^(-hi²) delta_ij]/(1+c).

For N=5q², the residue map x=q²u+5v, u modulo 5 and v modulo q², is bijective since gcd(5,q)=1. Its cross term in hx² is divisible by N. The quadratic sum factors into a fifth-root sum and a q²-root sum. In the latter, writing v=s+qt gives an inner sum of (xi^q)^(2a s t), where xi=omega^5 has exact order q² and a=5h is a unit modulo q. Because q is odd, only s=0 survives. This factor is exactly q, with no square-root convention or primality assumption on q.

Therefore G=qg, where g=1+2(eta²+eta³) and g²=5. Also eta has exact order five, since gcd(5q²,q⁴)=q². Restricting the target entry formula gives

C_q=(F-qgH+5q³gD)/(1+5q³g),

F_ij=eta^(ij), H_ij=eta^(-3(i+j)²), D_ij=eta^(-3i²)delta_ij.

The denominator is nonzero: its product with 1-5q³g is 1-125q⁶. This also proves that B_N is defined for this family. For q>1 the block is not B_5; both q and q³ must be retained.

### 2.2 A closed necessary system for every two-summand representation

First suppose both endpoint pairs are invertible. The inverse of the first branch has row support {i,pi(i)}; the inverse of the second has column support {j,tau^(-1)(j)}. Denote their independently projectivized row and column directions by u_i=(a_i,b_i), v_j=(c_j,d_j), and the resulting sparse matrices by U,V. Since B=G_1+G_2 implies G_1^(-1) B G_2^(-1)=G_2^(-1)+G_1^(-1), independent row/column rescaling gives some scalars x_i,y_j satisfying

(UBV)_ij=V_ij x_i+U_ij y_j.

Outside j in {i,pi(i),tau(i)}, the right side vanishes. Explicitly,

u_i^T M_ij v_j=0,

M_ij=[[B_i,j, B_i,tau^(-1)(j)], [B_pi(i),j, B_pi(i),tau^(-1)(j)]].

Let the augmented 25-by-11 matrix have coefficients V_ij in column x_i, U_ij in column y_j, and final column (UBV)_ij. Its 11-column maximal minors must all vanish.

These are closed equations on (P1)^10. To check the non-obvious assertion for a maximal minor, rescale u_i by lambda_i and v_j by mu_j. Each selected equation row acquires lambda_i mu_j; coefficient column x_i contributes lambda_i^(-1), and column y_j contributes mu_j^(-1). A minor using row set R scales by

product_i lambda_i^(n_i-1) product_j mu_j^(m_j-1),

where n_i and m_j count selected row and column indices. If some count is zero, the corresponding coefficient column is zero and the minor is identically zero. Otherwise all exponents are nonnegative. Each nonzero minor is multihomogeneous, of total degree six in row directions and six in column directions.

Singular endpoint masks do not invalidate necessity. Replace zero endpoint entries by a formal epsilon while keeping the legal Green weights fixed. The perturbed branches are invertible over C(epsilon), their sum specializes to the alleged target, and each inverse row/column pair can be divided by its lowest epsilon valuation. It then has a nonzero projective limit. The homogeneous equations pass to that limit. Scale variables need not remain finite. No base coordinate or open invertibility condition is being specialized. Zero edges require no division.

### 2.3 Fresh complete geometric special-fiber exclusion

Use p=241 and eta=91. Fresh arithmetic verifies order(91)=5, g=103, c=33 and denominator 34; the target is

161 20 102 102 20
20 182 62 26 92
102 62 236 28 26
102 26 28 236 62
20 92 26 62 182.

The checker also obtains this target by direct inversion of F_5^(-1)+A_5, independently of the displayed entry formula.

All 24 cycles are obtained once by starting their traversal at 0. For every ordered pair and every column j, eliminate its shared nonzero v_j between each pair of eligible rows. The equation is u_i^T C_ikj u_k=0 with C_ikj=M_ij J M_kj^T and J=[[0,1],[-1,0]]. Every one of the 4,320 C matrices is nonsingular. In particular each defines an invertible projective transition.

A spanning forest expresses every row direction as an invertible linear transform of one projective root per component. Every remaining edge yields a homogeneous quadratic in that component's root. No component is unconstrained. To determine its domain, the checker takes one nonzero quadratic, enumerates its at most two projective roots, includes infinity when appropriate, and tests every remaining quadratic.

All coefficients lie in F241 and all quadratic roots lie in F241(theta), theta²=7: 7 is a nonsquare, and a square discriminant has a base-field square root while a nonsquare discriminant divided by 7 is a square. The quadratic routine includes linear, double-root, and constant cases. Thus this is an algebraic-closure-complete enumeration, not a finite rational-point search.

Results freshly established:

- 384 pairs have an empty row domain.
- 72 pairs have one component with two directions.
- 120 pairs have two components, each with two directions.
- Exactly 624 row branches remain.
- All 3,120 joint two-column constraint matrices have rank one, so each column direction is unique; there is no omitted continuum.
- For every branch the coefficient matrix has rank 10 and the augmented matrix rank 11. The checker selects 11 equation rows and recomputes their nonzero determinant separately.
- 240 branches have a zero row base, 240 a zero column base, and 144 neither. None is discarded on a base-coordinate or Green-denominator guard.

GREEN_FRESH_CERTIFICATE.json records all cycles, forest indices, component quadratics, projective root domains, directions, selected equation rows, nonzero determinants and minor multidegrees. Its data and the fresh checker together give a reproducible finite certificate.

Twelve newly constructed legal two-Green targets pass the same off-support and augmented-rank necessity tests. Eight have singular endpoint masks, all twelve include zero edges, and one branch has every edge zero. Their projective limits are computed by retaining the lowest epsilon-valuation coefficients. These positive controls check the boundary interpretation and indexing independently of the excluded target; they are not additional lower-bound premises.

### 2.4 Uniform characteristic-zero lower bound

Let R=Z[eta] localized at (241,eta-91). For q=1 modulo 241, q and q³ both reduce to 1 and 1+5q³g reduces to 34. Hence every C_q has the same regular special fiber just excluded. Its closed necessary system is a closed subscheme of the projective R-scheme (P1_R)^10. It is proper over R. A nonempty geometric generic fiber would put the generic point in the closed image of this proper morphism and therefore also put the closed point in that image. This contradicts geometric special-fiber emptiness. The projective/proper fact is the classical [Stacks Project, Lemma 29.44.5](https://stacks.math.columbia.edu/tag/01WC); the concrete equations and emptiness certificate are established above.

This excludes two allowed terms for every stated q, under every primitive fifth-root embedding, even with singular endpoint masks. It does not lift a failure of an affine solve or a vanished open guard.

For completeness, principal restriction preserves the allowed grammar: effective cycle weights are products over arcs between retained vertices. Their total product is the original holonomy, and each Green entry is its unique path product divided by 1-holonomy. This proves restriction without dividing by any edge. Therefore full B_N inherits a lower bound of three for these arithmetic N. It does not inherit the block's upper bound.

### 2.5 Constructive upper bound and its uniform guards

Symmetry and reversal partition C_q's off-diagonal entries as

C01=C04=a, C02=C03=b, C12=C34=c, C13=C24=e, C14=f, C23=h0.

Define alpha=c/(ab), beta=e/(ab), gamma=f/a², epsilon=h0/b²,

L=beta²-gamma epsilon,
M=-2alpha beta+alpha gamma+alpha epsilon+beta gamma+beta epsilon-2gamma epsilon,
J=(beta-gamma)².

Let d be either root of Ld²+Md+J=0, and set

T=gamma(d+2)-alpha-beta,
t=[gamma d+(alpha+beta)d²]/T,
kappa=(t+d²)/gamma, x=(t-d)/kappa,
(r1,r2,r3,r4)=(x,(alpha-x)/d,(beta-x)/d,(gamma-x)/d),
z=kappa/(1+t), u0=1, ui=C_q[0,i]ri,
v0=z/t, vi=C_q[0,i]-zui.

For i,j positive, the normalized expression ui vj+t vi uj equals ri+t rj-kappa ri rj. The pairs involving index 1 follow from t-kappa x=d. Also kappa r4=1+d, so the difference of the (2,4) and (3,4) equations is automatic. The (3,4) equation follows directly from the definition of t. The final (2,3) residual is (Ld²+Md+J)/(dT). Its numerator identity is

(beta-gamma)[beta d²+(beta-alpha)d+beta-gamma]
 -(epsilon-beta)d[gamma d+2gamma-alpha-beta]=Ld²+Md+J.

The fresh integer-polynomial checker expands this identity. The four pairs involving 0 follow directly from the definitions of u0,v0,vi. Thus C_q[i,j]=ui vj+t vi uj for i<j.

Let W_s have successor weights (1,1,1,1,s) and W_0 have all five weights zero. With Delta_i=C_q[i,i]-(1+t)ui vi,

C_q=(1-t)diag(u)(I-W_t)^(-1)diag(v)
 +(t-1)diag(v)(I-W_(1/t))^(-1)diag(u)
 +diag(Delta)(I-W_0)^(-1)I.

Indeed (I-W_s)^(-1) has numerator 1 on/above the diagonal and s below it, and denominator 1-s. The upper entries are the proved identities, the lower entries follow by symmetry, and Delta corrects the diagonal.

Every denominator and endpoint is uniformly legal. At the same local ring R, the base guard residues (a,b,gamma,beta-gamma,L,discriminant) are (20,102,234,89,163,163). The monic quadratic reduces to d²+30d+124; discriminant 163 is a nonsquare in F241. A K-rational root would be integral over the integrally closed local ring R and reduce to an impossible residue-field root. Hence E_q=K[d] is a genuine quadratic field.

For an element A+Bd in its rank-two local algebra, Norm=A²-p1AB+p0B², where p1=M/L and p0=J/L. The fresh guard computation gives

Norm(d,T,kappa,t,1+t,1-t)=(124,139,53,1,160,85) modulo 241;
Norm(u)=(1,44,153,153,44);
Norm(v)=(41,117,7,7,117);
Norm(Delta)=(72,113,64,64,113).

Each inverse is a unit before the next expression is formed. Reduction therefore commutes with every division and the same residues persist for all q=1 modulo 241. Nonzero norms ensure all guards at both roots and under all embeddings. These 27 residues, both complete 25-entry reconstructions, and the irreducibility discriminant were freshly verified.

Writing s=alpha+beta, the second freshly expanded generic identity is

J(gamma²L-gamma sM+s²J)
=gamma²JL-gamma(2gamma-s)ML+(2gamma-s)²L².

It equates the numerator and denominator norms of t, giving Norm(t)=1 and conjugate(t)=1/t. This proves the reciprocal-root statement as well as reciprocal branch weights.

The upper and lower bounds now match. Coefficients are rational functions of q of bounded degree in a fixed degree-four field and one quadratic extension, so their exact-coordinate heights are O(log q) and preparation is polynomial in log q in a bit model. If only omega is supplied, forming eta=omega^(q⁴) costs O(log q) field multiplications. Application of this fixed five-dimensional representation takes a fixed number of field operations. Neither statement provides an ambient-size executor or a floating-point stability bound.

## 3. F015: complete original theorem audit

### 3.1 Model and input/output contract

N=2^k at least 4, Q=2^floor(k/2), M=N/Q, and a public integer cap 1<=b<=M/2. The input is all N raw field entries; no mode positions, amplitudes, recurrence, sparse transform, or certificate is supplied. The field E and a primitive Nth root w are supplied, with characteristic not dividing N. A field operation or inverse costs one algebraic operation; exact equality tests and O(log N)-bit indices cost word operations. Building all N powers of w costs O(N). In the dyadic setting primitivity may also be checked by w^N=1 and w^(N/2)!=1, within that budget.

Set eta=w^Q, theta=w^M, and y_t[u]=x[t+Qu]. Accept exactly when each fiber has an expansion

y_t[u]=sum_(h in H_t) a_t,h eta^(-hu), with nonzero a_t,h and r_t=|H_t|<=b.

On acceptance emit all N unnormalized outputs F_w x. On violation reject within the stated budget. This is exact membership recognition plus a complete output vector, not an assumed-input-only transform. A dense raw input, dense final spectrum, or full reshaped rank is consistent with this intermediate-fiber promise and does not remove it.

### 3.2 Three classical pruning uses

A dyadic transform of length L with s known nonzero input positions can produce every output in O(L[1+log(s+1)]) field/word operations. At depth d of parity recursion, at most min(2^d,s) nodes are active, each of length L/2^d. Summing their combine work gives the bound. Sparse-list partitioning is bounded by O(s log L), within the same envelope for s<=L; empty outputs and all copies are charged. Depth-first buffers need O(L) live space. Supplied full-length root powers permit all smaller twiddles by indexing.

For each fiber:

1. Run ordinary quadratic Berlekamp–Massey on the first 2b samples, producing C(z)=1+c1z+...+crz^r. Reject if its nominal degree exceeds b.
2. If r=0, test all M original entries for zero. Otherwise evaluate C at every eta^h using an input-pruned transform of its at most r+1 nonzero coefficients. Require exactly r distinct grid zeros.
3. Set A(z)=C(z)(sum_(u=0)^(r-1) y[u]z^u) modulo z^r. At each zero z_h=eta^h, lambda_h=z_h^(-1), recover a_h=-lambda_h A(z_h)/C'(z_h). Require nonzero derivative and nonzero amplitude. Forming A and these Horner evaluations costs O(r²).
4. Synthesize every candidate sample by a pruned inverse-root transform and compare all M entries exactly. Accept that fiber only on a complete match.

For a true r-mode fiber, C(z)=product_h(1-lambda_h z). The r-by-r Hankel matrix y[i+j] is V diag(a_h) V^T and is invertible, because the nodes are distinct and amplitudes nonzero. Thus 2r samples determine the unique minimal recurrence even when early samples cancel. Berlekamp–Massey on 2b samples recovers it in O(b²). Distinct roots make C'(z_h) nonzero. The amplitude formula follows by evaluating the numerator of sum_h a_h/(1-lambda_h z)=A(z)/C(z) at each pole. This proves completeness. The final full reconstruction proves soundness for arbitrary unpromised inputs, regardless of misleading prefixes. A trailing-zero nominal recurrence cannot pass the degree/root-count check.

### 3.3 Full output synthesis, including sharing and writing

Writing k=h+Mv and substituting the fiber expansion into the original DFT gives

(F_w x)[h+Mv]=M sum_t a_t,h w^(ht) theta^(vt).

The sum over u vanishes unless its two residue labels agree; this verifies the sign and factor M. For each h, collect B_h[t]=a_t,h w^(ht) and perform one pruned length-Q transform. If kappa_h fibers contain label h, that transform has kappa_h nonzero inputs. Define K=sum_t r_t=sum_h kappa_h. All synthesis, including absent-label zeros, costs

O(N+K+Q sum_h log(1+kappa_h)) <= O(N+K+N log(1+K/M)).

This uses Jensen's inequality over all M labels. It is important to fuse equal labels before synthesis; streaming each mode to Q outputs would give a different O(QK) charge. Bucketing by the integer labels and twiddle-table lookup costs O(N+K), with no hidden sorting or discrete logarithm.

Adding setup, Q recurrence computations, root-grid evaluation, amplitude recovery, full-fiber verification and output synthesis gives

O(N+Qb²+N log(2+K/Q)+N log(1+K/M))
 <= O(N log(b+2)+Qb²).

On rejection each attempted recurrence has degree at most b before its root-grid work; the algorithm stops at its first failed fiber. Thus the same cap bounds rejection. Input/output storage, root table, one live fiber workspace and at most Qb<=N/2 mode records fit O(N) space. No arbitrary algebraic root-finding or field-discovery oracle is used.

The optional successful-prefix refinement is also valid: on a true r-mode sequence every prefix has a recurrence of degree at most r, so the ordinary discrepancy/update implementation uses O(b(r+1)) work across 2b samples. Summing gives O(Qb+bK). The headline bound deliberately keeps O(Qb²), including arbitrary failed attempts, and needs no refinement.

For b=ceil(log^c N), fixed c>0, Qb²=o(N) and the bound is O_c(N log log N). Finite exceptional lengths can use the ordinary FFT with a c-dependent constant. More generally b=N^o(1) gives Qb²=N^(1/2+o(1)) and log b=o(log N), hence o(N log N) on the recognized class. Fixed b gives O_b(N). Ordinary FFT fallback after rejection provides all-input correctness but restores O(N log N) worst-case work for these schedules.

### 3.4 Aggregate budget, including the rejecting heavy fiber

For a public K0 in [0,N], let ell=log2 M, a=max(1,ceil(K0/Q)), B=min(M/2,a ell). Use the complete cap-B recognizer on each fiber. If it rejects, compute that fiber's ordinary full M-point DFT and divide by M. Completeness of the cap recognizer certifies its true support is greater than B. Accumulate the actual discovered support and stop immediately when it exceeds K0.

On acceptance the number of heavy fibers is at most floor(K0/(B+1)); on rejection there can be one extra final heavy fiber. The latter +1 is essential even for K0=0. Consequently the all-input success-or-rejection bound is

O(N log(B+2)+QB²+M ell(1+K0/B)+N log(1+K0/M)).

In the eventual unsaturated regime B=a ell, K0<=aQ makes the heavy term at most O(N+M ell)=O(N). The bound simplifies to O(N log(a ell+2)+Qa²ell²). For K0=O(Q log^c N), fixed c>=0, it is O_c(N log log N). The finite saturated regime retains the unsimplified bound. Individual fibers may have all M modes. The algorithm accepts exactly total support <=K0; it never assumes that supplied K0 is the actual rank.

The aggregate and uniform-cap classes are different. The former admits exceptional heavy fibers; the cap-only theorem alone does not. The older constant-average O(N) algorithm can still be better at K0=O(Q), so the growing-budget result is not a claim to improve every parameter point.

The preserved earlier theorem and Hero17 report were checked at their actual complexity ledgers: O(N+MK0+QK0+K0²) for the prior aggregate method, and O(rN+Qr²+rQ²+N) for the prior cap method. At K=Qb with b=log N in the balanced layout, those documented mode-by-mode terms are N b-scale, while F015 replaces them by N log b plus Qb². This compares specific upper-bound constructions; it is not a lower bound against all algorithms implementing the older ideas. The earlier reports are included as inert sources for this comparison, not re-certified in their unrelated theorem families here.

### 3.5 Green residual path and its exact domain

Let S e_j=e_(j+1), D=diag(w^j), P=7I+S+2D^(-1), and L=7I+D+2S. Direct index substitution gives F_w S=D F_w and F_w D^(-1)=S F_w, hence F_w P=L F_w. Compute residual r=Px in O(N), apply the certified algorithm to r, and solve Ly=F_w r in O(N). Then y=F_w x.

The declared scan writes d_j y_j+2y_(j-1)=z_j as y_j=a_j y_(j-1)+b_j, a_j=-2/d_j, b_j=z_j/d_j, and composes the cyclic affine recurrence. It requires every d_j=7+w^j nonzero and 1-product(a_j) nonzero. Both guards are checked and charged. They imply L invertible; mere invertibility does not imply those local guards.

Fresh counterexample to removing the guards: p=17, N=16, w=3. Its order is 16, d_3=0, and det(L)=product_j d_j-2^16=-1=16 modulo 17. Thus L is invertible but the stipulated scan is undefined. An invalid Green parameter is a domain error, not evidence that the residual violated a sparsity promise. Even a fallback-enabled source entrypoint may reject that invalid configuration. The raw-input theorem has no such Green restriction.

Over C, the perturbations of 7I in P,L have operator norm at most 3, so their singular values lie in [4,10] and condition numbers at most 2.5. These endpoint facts do not prove stability of exact Prony recognition. Generating x=P^(-1)r for test inputs is separate from transforming a fresh x and is never supplied as an uncharged representation.

### 3.6 Dense examples, coverage, and computational model

For square N=M² over C, choose H_t={t,...,t+b-1} modulo M with amplitude 2b at h=t and 1 elsewhere. The coefficient matrix is 2bI plus b-1 permutation matrices and hence invertible. Each raw coordinate has magnitude at least b+1; each final output has magnitude at least M(b+1). Thus the raw data and final spectrum are dense, and the Q-by-M reshaping has full rank. This norm argument is not valid over arbitrary finite fields and is not used there.

For any fixed support pattern the accepted set has at most Qb complex degrees of freedom. A finite union of such proper subspaces, even after finitely many fixed invertible preconditioners, cannot cover C^N when Qb<N. The aggregate version replaces Qb by K0; adding a fixed d-dimensional correction raises the dimension by at most d. This is a restriction on those fixed linear families, not a circuit lower bound or a claim about all nonlinear input-dependent constructions.

The theorem counts algebraic primitives plus indexing words. It does not show that an arbitrary field element fits an O(log N)-bit word. A growing finite field requires its own representation and arithmetic costs; exact complex/cyclotomic coefficients require height/extension analysis. Field construction, primitive-root discovery, arbitrary-precision bit work, floating-point zero tests, numerical stability and hardware timing are not free conclusions. Root-table preparation, mode identification and every explicit output write are included within the stated algebraic model.

## 4. Primary antecedents, inspected beyond abstracts

These comparisons establish relevant scope differences, not worldwide priority.

- [FFTW authors, Pruned FFTs](https://fftw.org/pruned.html): the opening discussion and first-K-output construction establish the O(N log K) arithmetic principle, its input/output duality, and the distinction between saved operations and practical speed. F015's three pruning uses are classical. That page does not state the original blind per-fiber membership/rejection interface or its aggregate budget theorem.
- [Briani, Cuyt and Lee, A hybrid Fourier-Prony method](https://arxiv.org/pdf/1706.04520), Sections 2–5 and equations (9)–(16): the input has a sparse global Fourier spectrum; shifted undersampled transforms and small Prony problems resolve alias collisions. Hankel structure and amplitude recovery are close antecedents. The inspected construction does not provide F015's exact supplied-grid scan, complete raw-input validation, or the stated all-size rejecting-input ledger. Fourier/Prony hybridization and discovering unknown modes cannot be advertised as new ideas here.
- [Bringmann et al., Traversing the FFT Computation Tree for Dimension-Independent Sparse Fourier Transforms](https://arxiv.org/html/2107.07347), Section 2, Theorem 1 and the tree-recovery setup: the exact result assumes oracle access and a globally k-sparse final Fourier transform, in unit-cost exact complex arithmetic. Its deterministic recovery time is soft-O(k² times 2^(8 sqrt(log k log log N))), with the paper's soft-O hiding polynomial logarithms of N. F015 instead reads and validates all data and can have a dense final spectrum with sparse intermediate fibers. Applying a sparse recovery theorem fiber-by-fiber is a comparator, not by itself the stated N log b+Qb² algorithm. The paper's conditional lower bounds for general non-equispaced transforms and sparse multipoint evaluation do not prohibit F015's full regular-grid pruning.

The defensible candidate increment is the complete charged intermediate-fiber interface and aggregate rejection accounting, built from established ingredients. Novelty of that exact combination remains unresolved. No measured practical speed advantage is established by this audit.

## 5. Reproduction, closure and remaining limits

Run only the three fresh scripts in this package:

- rebuild_green_certificate.py: independently regenerates the geometric finite lower witness.
- rebuild_upper_guards.py: regenerates both-root upper checks, 27 residues and two integer polynomial identities; imports only the first fresh checker for field arithmetic.
- rebuild_fiber_controls.py: regenerates the cap/aggregate/Green controls and the explicit invalid-local-guard example.

The JSON artifacts give exact results and the complete lower certificate. The certificate's field encoding is a+241*b for a+b*theta, theta²=7. SHA256SUMS.json seals all final package files except itself.

Meaningful closure: C01's decisive finite witness is no longer merely inherited in this cycle; its uniform upper/lower proof is explicitly audited. F015's original complete cap and aggregate algorithms are explicitly proved and freshly controlled, with every model and Green-domain qualification retained. A second reviewer should separately sign the exact sealed package before integration calls this new pass independently reviewed. Historical software execution, large operation profiles, numerical stability, finite-bit complexity and external publication priority remain distinct unverified claims; they are not silently promoted by the successful mathematical audit.
