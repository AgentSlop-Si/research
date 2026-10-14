# Independent acceptance: fourteen original banks over F23²

14 October 2026. Verdict: **ACCEPT for the explicit witness and the precisely pinned minimum below.** This is an independent witness/proof audit, not acceptance of every claim in the candidate packet.

## Accepted result and limits

In the original signed-bank dictionary at N=11 and q=13, with exactly one effective cross-sign alpha node in each cross-sign orientation and both pinned to 4,

    b4(F23²) = 14.

The same witness embeds into every even-degree finite extension. The independently reviewed lower bound therefore gives

    b4(F23^d) = 14 whenever 2 divides d and 5 does not divide d.

This does not assert an exact value for d=3 or other odd degrees not divisible by five. The existing degree-five-subfield theorem is a separate dependency. There is no new unpinned or unrestricted optimum, characteristic-zero transfer, novelty verdict, asymptotic family, or arithmetic/FFT speedup. Counting resolvent banks does not count the scalar arithmetic required to evaluate them.

The candidate's full 529-polynomial factor census, its counts of quadratic/cubic-eligible supports, and its claim that the selected support was first in a search ordering are outside this audit. None is needed for the accepted explicit witness or minimum.

## Frozen inputs and independence

The raw witness is frozen at SHA-256

    5afef05b733e2838eed4b1a42ccb50ebaac3253a4bfa60b0b1aed995c26b7dc8

The complete candidate archive is retained as an inert source at SHA-256

    5b5c94301269a19c6f363b559e25df721029f07f683a7a26450c326d33ddde18

The accepted extension lower-bound proof report is frozen at SHA-256

    3031f45d467e0cd0e7860de9fc59beb49758033ea0e1765e084eb19c2f97ee19

Its exact reviewed fusion report has SHA-256

    404377f23eb474dca692575b6e531d866b32ac796d9fb0b69426468a4b157231

Only the new standard-library independent_check.py was executed for scientific calculations. No candidate or historical scientific program was executed, imported or compiled. Candidate reports, raw JSON and branch records were read as inert inputs. The code uses coordinate pairs for field arithmetic rather than the candidate's base-23 integer representation. Source lengths and hashes are checked and recorded before and after each run. There were no external writes.

## Field, legal grammar and support

Use K=F23[z]/(z²+1), with elements represented internally as ordered pairs (a,b) for a+bz. The checker evaluates z²+1 at every element of F23 and finds no root, proving irreducibility. It independently verifies the norm-based inverse of each of the 528 nonzero field elements. It verifies that q=13 has order eleven.

The target and generators are unchanged:

    S e_t = e_(t+1 mod 11), T e_t = 13^t e_t,
    F[k,t] = 13^(-kt), 0 <= k,t <= 10.

Every allowed bank is literally

    (1/11) sum_(j=0)^10 w_j
      (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1),

with signs epsilon,delta independently ±1 and legal denominator

    Delta = 1-alpha^11-beta^11 != 0.

There are fourteen actual banks, with orientation counts (6,1,1,6). Each same-sign group uses

    {5,6,8+3z,4+8z,4+15z,8+20z}.

Each cross-sign group uses alpha=4. Every beta equals one. Distinct nodes, all denominators, and every bank's nonzero status are independently checked. Exactly one actual bank occurs at each orientation/node pair, and all sector vectors are nonzero, so the fourteen listed nodes are effective.

Multiplying the six independently decoded linear factors gives

    h(t)=t^6+11t^5+6t^3+21t^2+15t+9
        =(t-5)(t-6)(t²+7t+4)(t²+15t+11).

The two quadratics are independently checked to have no F23 root. All six displayed elements are distinct nonzero roots. This proves the selected support facts without relying on the factor census.

## Literal matrix verification

For each bank and phase j, the checker constructs the original matrix directly from its entries, using the specified shift convention and original phase. It applies independent Gauss-Jordan inversion over the coordinate-pair field, without using the geometric inverse formula to construct the inverse. It verifies both products against the identity.

Results for the supplied witness:

- 154 independently constructed and inverted literal branches
- 308 two-sided inverse matrix identities
- 154 supplied raw weights checked and independently recovered
- 14 legal, nonzero bank matrices and nonzero sector vectors
- 1,694 bank entries compared with the supplied matrices
- 1,694 Weyl coefficients independently extracted and checked against the original coefficient formula
- 121 aggregate entries compared with the freshly generated negative Fourier target
- Zero target mismatches

The raw-weight recovery is independent of the candidate's sector solver. For every reconstructed literal bank, coefficient extraction at a=0 gives its sector vector H_b. Since beta=1, Fourier inversion recovers

    w_j = Delta sum_(b=0)^10 H_b 13^(-epsilon j b).

All 154 recovered values match the supplied raw weights exactly. The literal summation retains the original 1/11 factor throughout.

A second construction independently solves the full literal 121-by-154 linear system with the raw phase weights themselves as unknowns. This system has rank 113; setting its free variables to zero gives another explicit weight assignment. Rebuilding its banks again produces fourteen nonzero original banks and every target entry exactly. This second construction does not call the candidate's sector equations or consume its solution vectors.

Full branch matrices, inverses, bank matrices, recovered weights, the second raw-weight assignment and both sides of the target comparison are included as machine-readable outputs.

## Independent lower-bound reconstruction and proof review

The exact-minimum conclusion needs a lower bound, not merely the fourteen-bank construction. The referenced independent proof is accepted for the same pinned dictionary and all legal beta values, including beta=0. This audit both reviews that argument and reconstructs its numerical premises afresh.

For U=S^epsilon and V=T^delta, every binary word with r U's and ell V's contributes the scalar 13^(epsilon delta v), where v is its number of V-before-U pairs after ordering as U^r V^ell. The fresh checker sums these words directly. It checks all forty mixed degree-eleven coefficients vanish, so X_j^11=(alpha^11+beta^11)I. The legal inverse is consequently the finite geometric sum divided by Delta.

Each bank's Weyl coefficient has the form alpha^r G(a,b) H_b. The sector amplitude absorbs beta^ell, the raw character sum and 1/(11 Delta). This derivation never divides by beta, so it remains valid when beta=0. Equal-alpha banks only add ordinary sector amplitudes; repeated nodes do not produce derivatives.

Direct extraction from all 121 target entries gives

    c_F(a,b) = 18*13^(3(a+b)^2).

The pinned cross node forces normalized amplitudes T_1=22 and T_2=20. Subtracting the forced cross contribution on the legal positive-exponent windows gives

    b=1: 19,4,20,14,20,3,14,16,8;
    b=2: 21,15,14,11,13,22,19.

The four and two consecutive length-six windows form

    M = [19  4 20 14 20  3]
        [ 4 20 14 20  3 14]
        [20 14 20  3 14 16]
        [14 20  3 14 16  8]
        [21 15 14 11 13 22]
        [15 14 11 13 22 19].

The first five rows and columns have determinant 3, independently computed by all 120 permutation terms. Every row annihilates (6,4,18,1,8,1). Thus rank(M)=5 and the unique monic degree-five kernel polynomial over any extension field is

    g(t)=t^5+8t^4+t^3+18t^2+4t+6.

Fresh division by all 23 monic linear and 529 monic quadratic polynomials gives nonzero remainder. A reducible quintic has an irreducible factor of degree at most two; therefore g is irreducible over F23.

For any representation let X be its distinct nonzero effective ++ nodes, with m=|X|. If m<=5, the monic ordinary-node polynomial

    p(t)=t^(5-m) product_(x in X)(t-x)

annihilates every displayed moment window. It must therefore equal g. Because g(0)=6, m<5 is impossible. If m=5, g must split over the coefficient field. An irreducible degree-five polynomial over F23 can split in F23^d only if 5 divides d. Consequently six distinct nonzero ++ nodes are necessary when 5 does not divide d. Zero nodes vanish on these positive windows, and repeated or ineffective banks cannot evade the argument.

Reflection J e_t=e_(-t) fixes the Fourier target, reverses both generator signs, and preserves alpha, beta and the phase product epsilon delta. The checker verifies all 484 Gaussian reflection identities and all 121 target reflection entries. Applying the same argument after reflection forces six -- nodes. Each cross-sign group has a nonzero effective singleton and needs at least one actual bank. Thus b4(F23^d)>=6+1+1+6=14 whenever 5 does not divide d.

This is precisely the lower bound needed for d=2. Embedding F23² into F23^d for even d preserves the explicit bank identity, nonzero denominators and nonzero banks. Combining its upper bound with the lower bound proves the stated even-degree equality only when 5 does not divide d. If 5 divides d, this witness still gives an upper bound of fourteen but cannot establish optimality; the separate twelve-bank theorem applies.

## Controls and reproducibility

All 181 exact mutation controls detect a defect:

- Each of 154 raw weights separately increased by one
- Each of fourteen actual banks omitted
- One alpha changed, one beta changed to zero, and the phase sign reversed
- Original 1/11 normalization omitted
- Positive instead of negative Fourier target used
- One inverse entry changed, failing both product identities
- Each of six kernel polynomial coefficients changed
- Reducible modulus z²-1 substituted

The individual-weight controls use exact linearity and the independently rebuilt branch inverse; each resulting aggregate differs from the target. They are not full independent reruns of the complete witness per mutation.

A cold replay of the new checker reproduces every deterministic scientific output byte for byte. REPLAY_VERIFICATION.json binds both runs. Run from this directory with Python 3:

    python independent_check.py --out replay

The review completes its declared scope. The supplied witness, the alternative direct reconstruction, the pinned lower-bound argument and the even-degree embedding consequence are accepted. The candidate's separate census and all excluded broader claims remain outside this verdict.
