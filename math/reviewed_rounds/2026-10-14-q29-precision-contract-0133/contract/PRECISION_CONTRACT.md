# Q29: exact mixed-characteristic precision contract

2026-10-14 UTC. Bounded next-gate design and fresh small controls only.

## Result and scope

The recovered characteristic-5 jet can be replaced by the exact finite ring

    B_M = (Z/5^M Z)[a,T] / (a^18+a^9+1, Phi125(1+T)).

This ring is the actual local cyclotomic integer ring modulo pi^(100M), under a -> alpha and T -> pi. M=2 supplies absolute precision 200. All arithmetic must retain integer coefficient carries and the full degree-100 ramified relation. The old characteristic-5 arrays do not determine their mod-25 lifts: recompute the original integral recurrence.

Raising coefficient precision while retaining v<100 is insufficient for improving the recovered F=pi^-60 U1687(-1-pi Y;q) beyond precision 40. A concrete next shared-center configuration is M=2, reciprocal w-degree <100 (equivalently a raw U jet v<200), which would certify F modulo pi^140. This contract does not execute that H1687/R843 computation, does not predict whether precision 140 resolves any repeated branch, and does not determine the value or nonvanishing of Disc R843.

Here “precision P” always means equality modulo pi^P: valuations strictly below P are exact; a zero at that precision means valuation at least P. The coefficient at pi^100 first becomes visible at precision 101, not at precision 100.

## 1. Exact local model and root choice

Put g(A)=A^18+A^9+1=Phi27(A). The finite order of 5 modulo 27 is 18: 5^18=1 modulo 27, while the proper-divisor exponents 1,2,3,6,9 give 5,25,17,19,26. The primitive 27th roots form one Frobenius orbit of length 18, so g is irreducible modulo 5. The fresh controls also check irreducibility independently by the Rabin criterion: A^(5^18)=A modulo g, with gcd(g,A^(5^9)-A)=gcd(g,A^(5^6)-A)=1.

Consequently

    O = Z_5[A]/g(A),    alpha=A mod g,
    k = F_5[A]/g(A)

is the unramified degree-18 integer ring. The residue identification is fixed by alpha mod 5 equal to the recovered eta. Because alpha^27=1 and 27 divides 5^18-1, alpha^(5^18)=alpha: alpha is the Teichmuller lift of eta. There is no extra arbitrary choice of a lift once this residue identification and exact 27th-root condition are imposed.

Define

    f(T)=Phi125(1+T)=sum_(r=0)^4 (1+T)^(25r)
        =T^100 + sum_(j=0)^99 f_j T^j,
    f_j=sum_(r=0)^4 binomial(25r,j).

The convention is binomial(n,j)=0 for j>n. This is an exact integer formula, not a binomial formula modulo 5. It gives f_0=5, f_100=1, and 5 divides f_j for every j<100. Thus f is Eisenstein over O and

    A = O[T]/f(T),    pi=T mod f

is a complete DVR, v_pi(pi)=1, v_pi(5)=100. Its fraction field has degree 100 over Frac(O) and degree 1800 over Q_5. The element xi=1+pi has exact order 125; q=alpha*xi has exact order 3375.

For a specified primitive 3375th root q, the compatible factors are exactly

    alpha=q^1000,    xi=q^2376,    q=alpha*xi.

Indeed 1000 is 1 modulo 27 and 0 modulo 125, 2376 is 0 modulo 27 and 1 modulo 125, and 1000+2376=1 modulo 3375. This identifies which primitive 125th root defines pi. Choosing another primitive root requires an explicit coordinate change; coefficient vectors are not silently identified.

The standard complete-DVR facts used here are the unramified construction from an irreducible separable residue polynomial and the Eisenstein uniformizer theorem. Primary references: Andrew Sutherland, [MIT 18.785 Lecture 10, Theorem 10.13 and Corollary 10.15](https://math.mit.edu/classes/18.785/2021fa/LectureNotes10.pdf), and [Lecture 11, Lemma 11.4 and Theorem 11.5](https://math.mit.edu/classes/18.785/2021fa/LectureNotes11.pdf). The instance-specific polynomials, congruences, and controls above are derived explicitly here.

## 2. Correctness lemma: exact finite representation

**Lemma.** For every integer M>=1, B_M is canonically A/(5^M)=A/(pi^(100M)). Every element has a unique array

    sum_(j=0)^99 sum_(i=0)^17 c_(i,j) alpha^i pi^j,
    c_(i,j) in Z/5^M Z.

For an exact nonzero lift x=sum_j b_j pi^j with b_j in O,

    v_pi(x)=min_(0<=j<100) [100*v_5(b_j)+j],
    v_5(b_j)=min_(0<=i<18) v_5(c_(i,j)).

For a nonzero element of B_M, the same formula using the canonical integer residues 0,...,5^M-1 gives its exact valuation, necessarily <100M. Zero gives only the lower bound >=100M.

For arbitrary 1<=N<=100M, let

    e_j(N)=max(0,ceil((N-j)/100)).

Then A/(pi^N) has the unique normal form obtained by reducing c_(i,j) modulo 5^e_j(N), with a coefficient omitted when e_j=0. Thus one may multiply in B_M, reduce both monic defining relations, and then apply these staggered moduli. This is an exact A/(pi^N) implementation, including N not divisible by 100.

**Proof.** Both defining polynomials are monic, giving the displayed free bases. Since f is Eisenstein, (5)=(pi^100), hence the two precision ideals agree. Reduction of the unramified basis modulo 5 proves the formula for v_5(b_j). Terms b_j*pi^j have valuations distinct modulo 100 for distinct j, so their minimum cannot cancel. The formula then proves both valuation detection and the staggered divisibility criterion. In particular, the additive coefficient count is sum_j e_j(N)=N and the quotient has 5^(18N) elements. Ring reduction before applying the staggered moduli is valid because these moduli describe the ideal (pi^N), not an arbitrary coefficient truncation. This proves the lemma.

### Implementation rules

1. Keep an 18 by 100 coefficient array over Z/5^M. Use exact integer arithmetic or modular operations that cannot overflow.
2. Multiply/convolve before monic reduction. Reduce alpha^18=-alpha^9-1; reduce pi^100=-sum_(j<100) f_j*pi^j. Repeat downward through all high powers. Coefficients f_j are retained modulo 5^M, never just modulo 5.
3. Reduce coefficients modulo 5^M. For requested precision N<100M, apply the staggered moduli only after ring reduction.
4. Store the precision separately from the representative. A representative in B_M can have a certified precision less than 100M after division or after importing uncertain data. Do not promote it back to 100M just because the array has that capacity.
5. q powers may use alpha^(n mod 27)*xi^(n mod 125), because these root orders are exact. Integer binomial expansion, repeated multiplication, or repeated squaring is valid. Characteristic-5 Frobenius factorization is not valid above its certified threshold.
6. Monic polynomial division is safe over this ring. Invert only proved units, or use explicitly tracked exact pi-division. A division-based resultant, gcd, or matrix algorithm must not treat every nonzero residue-ring element as invertible.

A unit inverse can be computed by lifting its inverse in k and applying x <- x(2-ux); the error squares in each step. Nonunit inversion requires changing the target operation and tracking all valuation/precision losses.

## 3. Carries and Teichmuller conventions

Let

    V(T)=sum_(j=0)^99 (f_j/5)T^j.

Then V(0)=1 and the exact relation is pi^100=-5 V(pi), equivalently 5=-pi^100 V(pi)^(-1). The initial unit is 5/pi^100=-1 modulo pi. Modulo 25 the complete relation is

    pi^100 = -5[1+2pi^25+2pi^50+pi^75
                  +4pi^80+3pi^85+3pi^90+4pi^95].

All coefficients in this display are interpreted modulo 25. In particular, replacing the polynomial by pi^100+5 is not an exact mixed-characteristic model.

Fresh negative controls certify:

- v_pi(5)=100. Treating coefficient addition 4+1 as zero loses a term first detectable modulo pi^101.
- v_pi(5+pi^100)=125. The shortened relation pi^100=-5 first fails modulo pi^126.
- v_pi((1+pi)^5-1-pi^5)=101, with quotient by pi^101 having residue 4. The characteristic-5 Frobenius shortcut first fails modulo pi^102.

Using ordinary coordinate digits 0,...,4 in the alpha basis is permitted, but that digit section k -> O is not additive or multiplicative. The ring operations above perform the necessary carries. Arbitrary sums of powers of alpha are generally not Teichmuller representatives.

For a general residue c in k, its Teichmuller lift is the unique root of X^(5^18)-X with residue c; its derivative is -1 modulo 5, so Hensel lifting is unambiguous. No such conversion is needed for the normal-basis arithmetic itself.

The recovered centers c=0,1,2,3,4 are ordinary integer lifts unless explicitly redefined. Their Teichmuller representatives modulo 25 are 0,1,7,18,24. For instance 2^4-1=15 has pi-valuation 100, while 7^4=1 modulo 25. Replacing an integer center by its Teichmuller lift changes it by a multiple of 5, hence at pi-valuation at least 100; previous below-40 faces are unaffected, but a higher continuation must preserve the selected convention or apply and record the exact coordinate translation.

## 4. Safe pi-division and normalization

For x=sum_(j=0)^99 c_j*pi^j, where c_j is in O/(5^M), division by pi is possible exactly when c_0 is divisible by 5 in O/(5^M). Choose the coordinate representatives 0,...,5^M-1 and put

    d_99=-c_0/5,
    d_(j-1)=c_j+f_j*d_99  for 1<=j<=99.

Then y=sum_j d_j*pi^j satisfies pi*y=x in B_M. A different choice in dividing c_0 changes y only modulo pi^(100M-1), which is exactly the lost precision. With an input certified modulo pi^P, 1<P<=100M, and proved divisible by pi, the output is certified modulo pi^(P-1). Iterate only while the divisibility guard passes and the remaining precision is positive. For h divisions, the output precision is P-h.

**Justification.** Multiplying y by pi and replacing pi^100 by -sum f_j*pi^j gives c_0=-5d_99 and c_j=d_(j-1)-f_j*d_99 for j>=1, exactly the formulas. If x and x' differ by pi^P, their quotients differ by pi^(P-1). This proves the error contract even when their full-capacity representatives differ. It also explains why division by pi is neither multiplication by an inverse in B_M nor a coefficient-index shift across the j=0 boundary.

Fresh controls divide a nontrivial element of pi^60*B_2 by pi^60 and check recovery to precision 140, divide pi^199 to recover 1 at precision 1, multiply back at every division step, and reject division of 1 by pi.

## 5. Jet-transfer lemma and a concrete next gate

**Lemma.** Let G(v) be an integral polynomial over A. Suppose an integral jet J(v) satisfies

    G-J in (pi^N,v^K).

In an extension where pi^s is defined, let s>0 and let h be a nonnegative allowed valuation exponent. Then

    pi^-h G(pi^s Y) - pi^-h J(pi^s Y)

has coefficientwise valuation at least min(N,sK)-h. If this lower bound is positive and all coefficients of the displayed normalized jet are integral, the true normalized polynomial is integral. Every integral translation Y=c+pi^b Z, b>=0, preserves the bound. Every further division by pi^r subtracts r from the bound. Formal differentiation in the current normalized variable preserves the bound; conversion to a previous variable may introduce inverse scales that must be subtracted explicitly.

**Proof.** A pi^N coefficient error stays divisible by pi^N under the integral substitution, and each omitted monomial v^j, j>=K, acquires pi-valuation at least sK. Division gives the stated bound. Integral translations and formal differentiation use only integral coefficients, proving the remaining statements.

For the recovered U1687 and F=pi^-60 U1687(-1-pi Y;q), this specializes to

    certified F precision = min(N,K)-60.

The exact R recurrence can be rerun in B_M[w]/(w^L):

    R_m=(w-2+q^(2m)+q^(2m-1))R_(m-1)
        -(1-q^(2m-1))(1-q^(2m-2))R_(m-2),
    R_0=1, R_(-1)=0.

It has no divisions and never decreases w-degree. The exact identity

    U1687(-1-v;q)=sum_(k=0)^843 (-1)^(843+k)
                 r_(843,k)(q) v^(2k)(1+v)^(843-k)

shows that retaining w<L determines the raw v<2L jet. Every binomial coefficient and sign in this transformation must be integral and evaluated in the mixed-characteristic ring.

A fully specified first continuation is:

- M=2, so coefficient precision N=200.
- Retain w<100 in the R recurrence through m=843.
- Transform to v<200. Equivalently, the direct H recurrence must retain v<201 before exact division -H/v to obtain U at v<200.
- Verify reduction modulo 5 against every available recovered raw coordinate, preserving the alpha basis and the sign -H/v.
- Normalize by v=pi Y and pi^-60 using guarded ring division. This yields F modulo pi^140, not a full discriminant.
- On each subsequent branch record its exact center lift, variable scale, content division, derivative conversion, and remaining precision. Any decisive term must have valuation strictly below that bound. Stop a branch at an unresolved ceiling and increase precision or prove a separate bound.

For a requested normalized precision P, sufficient parameters are 100M>=P+60 and 2L>=P+60, with the actual common raw precision min(100M,2L). These are sufficiency conditions, not a prediction of the precision needed for an eventual discriminant.

For fractional scales, a precise optional extension is rho^d=pi and

    A_d=O[rho]/f(rho^d).

The substituted polynomial is Eisenstein of degree 100d, so rho is a uniformizer, v_rho(5)=100d, and the same implementation works with ramified basis size 100d. The convention v_pi(rho)=1/d converts the error budget. A common d=10 accommodates the denominators 2 and 10 already seen. This extension construction is proved here but was not implemented by the bounded controls.

## 6. Fresh controls and provenance

Only fresh_exact_controls.py was executed for the mathematical checks in this task. It imports standard Python modules only and neither imports nor executes any predecessor scientific program. The predecessor archive was opened as inert bytes.

CONTROL_RESULT.json records:

- Exact integer construction of f and the identity ((1+T)^25-1)f(T)=(1+T)^125-1.
- Rabin irreducibility controls for g over F_5.
- Exact normal-form ring checks at M=1,2,3: cyclotomic relation, alpha's Teichmuller identity, primitive-3375 order guards, CRT root decomposition, v_pi(xi^5-1)=5, v_pi(xi^25-1)=25, and nilpotence index 100M.
- The three carry boundaries, guarded divisions, and staggered quotient checks for N=1,99,100,101,125,126,199,200.
- Independent small direct-H and reciprocal-R recurrence agreement for H3,H5,H7,H9,H11,H13 in B_2, using the complete small polynomials.
- Candidate archive CRC and all 36 manifest hashes, plus equality of the six selected local source members to their archived bytes.

The input archive SHA-256 is 29f2fd3524b7d7d2548b3d0480fbcb605768987a34b428814c22343bd4a44ce4. The recovered REPORT.md SHA-256 is 17057203aeab6f70f9cd03caacf9a25425fbdfb5c6831cb8a9b156d5fe1240dd. Full source paths, byte lengths, and hashes are in CONTROL_RESULT.json. The web references were read as primary background sources; no local byte hash of those web PDFs is claimed.

The source archive's earlier metadata-comparison replay failure is disclosed in its own AUDIT_RECEIPT.json and replay_history/INITIAL_REPLAY_FAILURE.stderr; that audit attributes the failure to nondeterministic elapsed-time-derived metadata and records a corrected replay. This task did not rerun that historical replay or independently validate its runtime claims. Our fresh controls completed successfully with empty stderr. Initial combined discovery/source output was truncated; focused subsequent reads recovered all decisive local source content. No mathematical test failure or compiler failure occurred in the fresh controls.

## 7. What remains unproved

This is an implementation-ready exact representation and precision lemma, supported by small exact controls. It is not an optimized all-degree engine, an H1687 mixed-characteristic lift, a new squarefree residual factor, a derivative-unit assertion, an all-center symmetry theorem, or a Disc R843 evaluation/nonvanishing proof. Those conclusions require separately executed and reviewed computations or mathematical arguments, with all scales and all relevant degrees accounted for. No external write, repository upload, table update, ranking change, or historical novelty claim was made.
