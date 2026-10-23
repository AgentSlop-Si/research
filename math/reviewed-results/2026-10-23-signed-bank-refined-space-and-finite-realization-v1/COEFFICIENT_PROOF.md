# Cubic deterministic coefficient generation in the refined signed-bank space

23 October 2026 UTC. Separate author candidate for independent review. This packet does not amend, relabel, or delay any previously accepted packet. No external publication is performed. All scientific control code in this packet is new.

## 1. Exact statement and genuinely changed input space

Let N be odd, d>=4, N>=6d-5, and m=N-d. Let K be a supplied effectively represented coefficient field containing a certified primitive Nth root q, with char(K) not dividing N, and a supplied represented list of 2N distinct scalars. Exponent fractions below mean inverses modulo N, never field division by 2 or 4. Set

    h=4^(-1) mod N, e=2^(-1) mod N, rho=q^e,
    C_j=q^(h j^2), D(z)=product_(a=2)^(d-1)(1-q^a z), J=m+1.

The space used in THIS theorem is exactly

    Pairs_ref = {(P,R): t^2 | P, deg P<=3d-7, deg R<=d-2,
                        C_J P(rho^J)+R(q^J)=0},
    E_ref = {((C_j P(rho^j)+R(q^j))/D(q^j))_(j=0)^m:
               (P,R) in Pairs_ref},
    U_ref = E_ref^perp, U_ref,0 = {g in U_ref:g(0)=0}.

Only the ACTUAL columns 0<=j<=m are divided by D(q^j), which are nonzero. D(q^J)=0, and no quotient is evaluated at J. Coefficients of g identify it with a vector of length m+1. This E_ref is smaller than the older unconstrained envelope; U_ref is correspondingly larger. Neither earlier cubic theorem supplies this new-space theorem by terminology or by changing a displayed threshold.

THEOREM. In the stated interface one can deterministically construct a monic degree-m g in this EXACT U_ref such that

    g(0)!=0, gcd(g,g')=1, rank X_N(g)=N,

where X_N is the original axis matrix defined in Section 5. The complete coefficient stage costs O(N^3) coefficient-field additions/multiplications, O(N^2) coefficient-field inversions, and O(N^2) live coefficient-field elements with schoolbook arithmetic. Failed trials, all intermediate coefficient vectors, dense space/endpoint preparation, and final coefficient output are included.

This composes the independently accepted reverse-gcd selection lemma with a separately checked reconstruction of both pencils in the refined space. The underlying bank theorem is the already accepted bound 2(N-d)+2 on N>=6d-5. Taking d=floor((N+5)/6) covers every odd N>=19. There is no further bank-count or leading-constant improvement here. The result matches the existing expected cubic coefficient work, now deterministically at this refined-space interface. Field/list setup, a genuine splitting extension, actual roots, physical banks, and all warm costs remain separate. No FFT, efficient full compiler, optimality, or historical novelty claim is made.

## 2. Exact refined-space facts, not old-U assumptions

The accepted structural-endpoint theorem and its independent review, pinned in SOURCE_BINDINGS.json, establish the following facts over K and its algebraic closure. Here are the specific proof interfaces and threshold checks used in this transfer.

Before the last constraint the numerator space has dimension (3d-8)+(d-1)=4d-9. The constraint is nonzero on (0,1); therefore

    dim E_ref<=4d-10,
    dim U_ref>=(m+1)-(4d-10)=N-5d+11>=d+6.

The pair (0,D) satisfies the constraint, so the all-ones vector lies in E_ref and every g in U_ref vanishes at 1. The original supported Gaussian recurrence rows belong to E_ref, not just to the older envelope. In the source notation s=a+b, their chirp numerator is Q_b q^(h s^2)t^s F_(a,b)(t^2), which has t^2 as a factor and degree <=3d-7; the ordinary numerator is -B_b R_(a,b)F_(a,b), of degree <=d-2. For s<d-1 the remaining factor of D makes both numerators vanish at J. For s=d-1 the two numerator values are both Q_b and cancel. This is an equality of polynomial numerators at the formal point, not division by D(q^J). Hence U_ref is contained in the actual original recurrence kernel in every admitted characteristic.

For completeness, the critical support argument retains both refinements. A nonzero x fixed by U_ref,0 gives, by finite-dimensional duality, an equality between an envelope numerator and x^jD(q^j) on j=1,...,m. The formal constraint extends this numerator equality to J, because the target is zero there. Apply

    (L_x y)_j=(1-q^(j+2))y_(j+1)-x(1-q^(j+d))y_j,
    M_+=product_(a=0)^(d-1)(S-q^a).

On the chirp polynomial L_x acts as

    Phi_x(P)=q^h t(1-q^2t^2)P(rho t)-x(1-q^dt^2)P(t).

For x!=0 it raises degree exactly three and preserves t-adic valuation; each subsequent constant factor raises degree exactly one and preserves valuation. The unique extreme coefficients are nonzero, so all these polynomial operators are injective. The resulting Q is divisible by t^2, with deg(Q/t^2)<=4d-6, and vanishes at N-2d distinct nonzero rho-points. At the new threshold

    N-2d>=4d-5>4d-6.

Thus Q=0 and P=0. The ordinary remainder satisfies a constant recurrence of order 2d-2 with nonzero endpoint coefficients. The m known zeros suffice to propagate both ways. Comparison at j=0,N gives x^N=1. The nonzero endpoint coefficients of D then force x=1: if x=q^s, both s and s+d-2 modulo N must lie in [0,d-2], and 2(d-2)<N.

For the derivative functional (j), the same proof uses L_1(jD(q^j))=(1-q^(j+d))D(q^j). The remainder obeys the square of the ordinary annihilator, also in characteristic two. Comparison at 0,N would give N D(1)=0, impossible. Consequently the fixed root 1 is not forced to have multiplicity two even on U_ref,0.

Sparse support on {0,1,m} gives the independent endpoint statement. After applying product_(a=0)^(d-2)(S-q^a), the chirp divided by t^2 has degree <=4d-10 but has N-2d-1 zeros. Since N-2d-1>=4d-6>4d-10, the chirp and then the ordinary part vanish. Therefore c0,c1,cm are jointly independent on U_ref, and c1,cm are independent on U_ref,0.

These results give EXACT fixed divisors, including multiplicities:

    gcd(U_ref)=t-1, gcd(U_ref,0)=t(t-1).

Indeed c0 independence excludes a universal zero root in U_ref, c1 independence makes zero simple in U_ref,0, the derivative exclusion makes 1 simple, and the support argument excludes every other nonzero algebraic root. No perfectness, squarefreeness of auxiliary polynomials, or rank-saturation hypothesis is needed.

Define the NEW residual spaces

    V0={g/[t(t-1)]:g in U_ref,0}, r=m-2,
    V1={g/(t-1):g in U_ref}, n=m-1.

Their gcds are exactly one. V0 has maximum degree r and independent constant and degree-r coefficient maps: these are -c1 and cm before division. V1 has maximum degree n. Both spaces have O(N) dimension and degree bounds. These facts, rather than any old-U fixture or old dimension estimate, are the inputs to both deterministic selections below.

## 3. The accepted reverse-gcd lemma and both exact substitutions

The separately accepted selection lemma is independent of N,d and envelopes. For a monic degree-v polynomial a and a basis b_1,...,b_s of W, of degrees <=L with L>=v and gcd(a,W)=1, it returns P in the SAME scalar span W with gcd(a,P)=1. With a nonzero coefficient functional phi it can also require phi(P)!=0. A list of v+2 distinct scalars suffices, and its complete schoolbook costs are

    O((s+v)L^2) additions/multiplications,
    O((s+v)L) inversions,
    O(sL+v^2+L) live field elements.

To specify the transferred algorithm exactly, scan the basis and record only strict decreases A_i=gcd(A_(i-1),p_i), starting with A_0=a and ending at 1. Initialize P=p_last, then unwind backward. At a level A=A_(i-1), D=A_i, p=p_i, maintain gcd(D,P)=1. Try p+lambda P for Delta+1 nonzero scalars, where Delta=deg A-deg D, accepting an exact gcd-one test. The failed monic gcds e_lambda are pairwise coprime and coprime to D, so

    D product_lambda e_lambda divides A

WITH ALL THEIR MULTIPLICITIES. Thus at most Delta fail. Degree drops telescope, giving at most 2v-1 unwind trials. If phi(P)=0, choose a basis member u with phi(u)!=0 and try u+lambda P. The same charge allows at most v-deg gcd(a,u)+1 trials while preserving the nonzero phi exactly. This single repair is not an unproved forward simultaneous-preservation induction. No factorization or root extraction is performed.

FIRST substitution. Solve in the actual V0 for f0(0)=coefficient_r(f0)=1. Endpoint independence makes the solve consistent. Apply the lemma to

    a=f0, W=V0, L=v=r,
    phi(f)=coefficient_r(f)-f(0).

Gcd(V0)=1 gives gcd(f0,V0)=1 and independent endpoints make phi nonzero. Thus the output f1 is in V0, gcd(f0,f1)=1, and phi(f1)!=0. The required list has r+2=m elements, within 2N.

Form F_Z=f0+Z f1. This polynomial is irreducible over K(Z): a factor independent of Z in a factorization of the primitive polynomial linear in Z would divide f0 and f1. Its constant and leading coefficients are nonzero over K(Z). If F_Z shared a factor with rev_r(F_Z), irreducibility and equal degrees would imply rev_r(F_Z)=lambda F_Z. Reversing twice gives lambda^2=1, so lambda is the constant +1 or -1 (only 1 in characteristic two). This contradicts the nonzero endpoint determinant phi(f1). Thus the reciprocal resultant is nonzero and has Z-degree <=2r. Including both endpoints gives a guard of degree <=2r+2. Test 2r+3=2m-1 distinct list elements using endpoint and ordinary gcd tests, then normalize to obtain monic f in V0 with

    f(0)!=0, gcd(f,rev_r f)=1, f(1)!=0.

No squarefreeness of f is claimed or required.

SECOND substitution. Put h0=t f in V1 and define the EXACT zero-leading slice

    W={h in V1:coefficient_n(h)=0}.

Because h0 is monic of degree n, every h in V1 has the unique decomposition coefficient_n(h) h0+w, w in W. Hence V1=K h0 direct-sum W, and gcd(h0,W)=gcd(V1)=1, including multiplicities. Apply the same lemma to a=h0, this W, and L=v=n, without a functional. Its output h1 is in the zero-leading slice, gcd(h0,h1)=1, and h1(0)!=0. The required list has n+2=m+1 elements, again within 2N. Polynomial multiples never replace scalar combinations, and no membership claim crosses between refined U and old U.

## 4. Generic separability on this actual second pencil

Let h_Z=h0+Z h1 and g_Z=(t-1)h_Z. Every specialization is monic degree m and belongs to U_ref. Coprimality of h0,h1 makes h_Z irreducible over K(Z). Its ordinary derivative is nonzero because the coefficient of t in h0 is f(0)!=0, so the corresponding coefficient of the derivative is a nonzero polynomial in Z. This remains true in characteristic two and over imperfect fields. Therefore h_Z is separable over K(Z).

Moreover h0(1)=f(1)!=0, so h_Z(1) is not identically zero. Thus g_Z is squarefree over K(Z), and its monic degree-m discriminant is a nonzero polynomial in Z of degree at most 2m-2. Finally g_Z(0)=-Z h1(0) is a nonzero linear polynomial. These are generic NONZERO POLYNOMIAL certificates; the algorithm still checks each accepted specialization exactly.

## 5. Actual original axis identity and the nonzero 2d minor

For monic g of degree m, let p_a be the coefficient vector of t^a mod g, 0<=a<N. The ORIGINAL matrix has row a

    X_N(g)[a]=(p_a, 1, p_[-a mod N]).

A left relation with A(t)=sum_(a=0)^(N-1) beta_a t^a is exactly

    g | A, A(1)=0, g | J_N A,
    J_N A=t^N A(1/t)+A(0)(1-t^N).

This follows directly by summing all three column blocks; it is not a substituted Hankel matrix or a claimed reciprocal sufficient condition.

Write g=(t-1)h, n=m-1, c=h(0), v=rev_n(h), s=d-1, and H_N=sum_(j=0)^(N-1)t^j. Any first-block relation has A=(t-1)h a with deg a<=s. Put b=rev_s(a), using padded reversal. Direct expansion gives

    J_N A=(t-1)[c b_s H_N-t v b].

Hence nonzero axis relations are equivalent to nonzero b of degree <=s such that

    t v b = c b_s H_N modulo h.                         (1)

The scalar-column condition is automatic because A has t-1 as a factor. The identity needs neither c!=0 nor genericity nor squarefreeness.

Rewrite (1) as the polynomial equality

    t v b-c b_s H_N-h q0=0, deg b<d, deg q0<d.          (2)

The nominal coefficient at degree N-1 cancels: both first terms have coefficient c b_s. Their difference therefore has degree <=N-2, and division by monic h bounds the quotient by d-1. Let M(h) be the (N-1)-by-2d coefficient matrix of (2). Its entries are linear in h. A kernel vector with b=0 forces q0=0; the original-axis correspondence gives

    dim ker M(h) = N-rank X_N((t-1)h).

In particular M has full column rank exactly when the ORIGINAL X_N has full row rank, including c=0.

At the actual auxiliary h0=t f, c=0 and v=rev_r f. Cancel t in (2) to get

    (rev_r f)b=f q0.

Reciprocal coprimality forces f|b. But r=N-d-2>d-1 under N>=6d-5,d>=4, so b=q0=0. Thus M(h0) has rank 2d and X_N(g0) has rank N for g0=t(t-1)f. This is an auxiliary polynomial specialization ONLY, never a physical zero-node bank. It also reproduces the older divisor witness because 2m-2>N-1.

Select for the proof any 2d-row minor of M(h0) that is nonzero. On h_Z its determinant A_axis(Z) is nonzero at zero and has degree <=2d. No symbolic minor is required by the implementation. The existence of that minor follows from the actual original-axis identity at this refined-U witness, not by importing an old-U rank statement.

## 6. The quadratic exact axis test on every reciprocal-gcd locus

For a candidate with c!=0, t is a unit modulo h. Put K0=(h-c)/t, D0=gcd(h,v), hbar=h/D0, vbar=v/D0, and ell=deg hbar. Since c/t=-K0 modulo h, (1) is equivalent to

    v b=(-K0 H_N)b_s modulo h.

The following complete test is the accepted fast-axis identity, which depends only on the displayed actual h, N and d and therefore applies unchanged after the explicit refined-space construction.

1. If ell<s, take b=hbar; its b_s=0 and it supplies a nonzero relation. Rank is deficient.
2. For ell>=s, no nonzero relation can have b_s=0. Normalize a possible relation to b_s=1.
3. Such a relation requires D0|H_N. Indeed gcd(K0,h)=1 because h=tK0+c and c!=0, so divisibility by D0 of -K0 H_N is equivalent to divisibility of H_N, with full multiplicities. If it fails, the axis has full row rank.
4. If D0|H_N, compute by extended Euclid

       b0=[vbar^(-1)(-K0(H_N/D0))] mod hbar.

   If ell=s, b0+hbar is a monic degree-s relation, so rank drops. If ell>s, rank drops exactly when b0 itself is monic of degree s. In every other case rank is full.

This is exhaustive. It never discards D0!=1 or assumes that a tested point is generic. When deficient, reversing the specified b produces the explicit original relation A=(t-1)h rev_s(b). All gcds, divisions, modular inversion and remainders have degree O(N), hence cost O(N^2) schoolbook field arithmetic and O(N) inversions per candidate. Test c!=0 first, as required for this algorithm.

The complete final guard is

    A_axis(Z) * g_Z(0) * Disc_t(g_Z),

nonzero of degree at most 2d+1+(2m-2)=2N-1. Therefore the supplied 2N distinct scalars include a successful final candidate. Test them in fixed order, constructing coefficients, checking nonzero constant and ordinary squarefreeness by gcd, and applying the complete axis test above. A candidate may pass even when the particular theoretical minor vanishes; the exact test still decides its real axis rank.

## 7. Full threshold, dimensions and list audit

All lower bounds hold uniformly at N>=6d-5, d>=4; oddness retains modular half/quarter exponents.

- N>=19; m>=5d-5; r=m-2 and n=m-1 are positive.
- dim U_ref>=N-5d+11>=d+6. Actual upper dimensions, not an old lower bound, are O(N).
- Refined fixed-root/derivative interpolation: N-2d>=4d-5>4d-6.
- Sparse endpoint interpolation: N-2d-1>=4d-6>4d-10.
- Ordinary propagation: m>=2d-2, and the sparse ordinary zero count m-2>d-2.
- Endpoint support interval: 2(d-2)<N.
- Truncated matrix has enough rows: N-1>=2d. Its witness margin r-(d-1)=N-2d-1>=4d-6>0.
- Original reciprocal divisor margin: (2m-2)-(N-1)=N-2d-1>0. The safe reciprocal-residue witness also has degree r>d-1.
- First selection requires m scalars; second requires m+1; reciprocal pencil requires 2m-1. Each is <=2N. Filtering zero still supplies the selection lemmas' v+1 nonzero candidates.
- Final product degree is EXACTLY bounded by 2N-1, so 2N values suffice.
- Original physical reconstruction still has m>=(N-1)/2 and N>2d+1.
- If F_Q contains q, N divides Q-1, so Q>=N+1; its quadratic extension has Q^2>2N and supplies the list. Also the older existence guard H=d(d+1)+2m-1 still satisfies 2H<(N+1)^2, though the new deterministic list no longer depends on H.

There is no hidden old N>=6d-2 or N>=8d-10 consumer left in the proof.

## 8. Complete cubic cost and unchanged physical obligations

Build the exact refined envelope by eliminating R's constant coefficient with the formal constraint, then compute U_ref, U_ref,0, V0,V1,W and the endpoint solve by dense elimination. This uses O(N^3) arithmetic, O(N) pivot inversions and O(N^2) live storage. The two reverse selections each have s,L,v=O(N), hence each costs O(N^3) arithmetic, O(N^2) inversions and O(N^2) storage. The first pencil has O(N) tests at O(N^2) arithmetic/O(N) inversions each. The final pencil has at most 2N tests at the same per-test costs. Summing these stages gives the theorem's complete cubic arithmetic and quadratic inversion bounds; no dense axis rank test is inserted into the runtime claim. Dense axis matrices occur only in fresh controls.

The source paid model is retained. Finite quadratic coefficient-field setup may cost O(Q^3) base operations and is NOT absorbed into coefficient-field work. The scalar list, its representation/counters, bit lengths and field-interface certification remain separate paid inputs. Infinite positive-characteristic fields need an effective supplied distinct-element interface; repeated addition of 1 does not supply it.

After g is obtained, construct a genuine splitting field and recover all m actual distinct nonzero roots. Neither a degree-two coefficient extension nor an auxiliary g0 supplies physical roots. Retain the conservative finite overfield of degree t=m! over R=Q^2 when using the explicit source recipe: O(t^2 R^(t+floor(t/2))) coefficient-field operations for the modulus, and O(m t^2 R^t) for exhaustive root recovery. These enormous bounds are not improved here.

All amplitudes, Vandermonde/axis solves, raw weights and branch inverses remain paid. Subsequent preparation is O(N^3) ACTUAL root-field arithmetic with O(N^2) root-field storage, plus stated inversions. For B=2m+2, the literal warm application retains 2BN^2 multiplications and 2BN^2-BN-N additions, as well as full input/output, indexing, storage and extension/base-coordinate costs. Its arithmetic order is cubic; direct dense Fourier evaluation already has quadratic base-field arithmetic. This coefficient theorem establishes neither a faster complete compiler nor a Fourier/FFT speedup.

## 9. New evidence and publication boundary

Fresh controls reconstruct E_ref by eliminating the formal endpoint, derive its nullspaces, check exact fixed divisors and original Gaussian rows, and run both selections and both pencils from scratch. They also compute the literal original axis, the truncated matrix and a nonzero specific 2d minor. All nine fixtures satisfy 6d-5<=N<6d-2. They include N=19,21 and prime/composite orders in characteristic two. Every selected coefficient vector is NOT in the old unconstrained U; these are not old-U fixtures relabelled as new evidence.

Additional fresh exhaustive axis controls cover all five branch outcomes, including reciprocal-gcd and repeated-factor cases, and compare every outcome with the literal original axis. Separate fresh reverse-selection stress controls exercise failed trials, functional repair and inseparable moduli. They are implementation/transcription checks, not substitutes for the uniform proof. No scientific author/historical program was imported or run. No root field, full physical bank array or bank application was constructed by these controls.

Independent verification is required before accepting or publishing this separate refined-space coefficient theorem. Previously accepted old-U cubic packages and the accepted refined bank-count theorem remain unmodified and independently scoped.
