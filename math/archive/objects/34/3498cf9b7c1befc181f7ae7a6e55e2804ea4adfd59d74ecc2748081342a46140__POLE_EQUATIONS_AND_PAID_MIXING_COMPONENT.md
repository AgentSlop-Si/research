# A bounded pole-family gate and an explicit paid mixing component

## Outcomes

Changing the original pole schedule does change the sector frames. Equal poles on the H0-minus and H0-plus routes create an exact plus-sector dependence. This produces a legitimate two-Green high-x mixing component, with all inverse guards stated.

However, the one tested family of 256 schedules tau_j in {+1/2,-1/2} does not permit a commuting or anticommuting prefix to realize F64 through the eight-term outer layer. This is a finite-family result, not an exclusion of arbitrary pole schedules or genuinely mixing lifts.

The explicit component supplies only one mixing direction and no Fourier coefficient lift. Right endpoint permutations, projectors, additional orders, and changed seed poles are not counted as free operations.

## 1. Pole equations from the target characters

Keep the eight N64 nested route permutations fixed, but allow complex scalar poles tau_0,...,tau_7. Require

    1-tau_j^64 != 0.

If nonzero edge weights are part of the declared branch, also require tau_j != 0. All schedules and the component below satisfy both guards.

Each route obeys P_j^32=X, where X shifts indices by 32. Let d_j(i,k) in {0,...,63} be the directed distance from k to i along P_j, and put

    q_j(i,k)=d_j(i,k) mod 32,
    e_j(i,k)=floor(d_j(i,k)/32).

The exact projected row frame is

    V_i^sigma[j,k]
      = G_j(tau_j)[i,k]+sigma G_j(tau_j)[i,k+32]
      = sigma^(e_j(i,k)) tau_j^(q_j(i,k))
          / (1-sigma tau_j^32), 0<=k<32.

The denominator is nonzero under the original inverse guard, because 1-tau_j^64=(1-tau_j^32)(1+tau_j^32). Thus a candidate pure-character outer row must satisfy explicit polynomial determinant conditions on its forbidden sector:

    det[ sigma^(e_j(i,k)) tau_j^(q_j(i,k)) ]_(j=0..7,k in K)=0

for every eight-column set K, together with the rank and coefficient guards below. These determinants have degree at most 248; each row depends on just one pole. `SIGNED_POLE_FAMILY_CERTIFICATE.json` supplies the complete exponent/sign tables for rows 0 and 1, so the equations are explicit without expanding millions of determinants.

For a commuting prefix, Fourier row 0 requires annihilating the minus frame and row 1 requires annihilating the plus frame. For an anticommuting prefix these signs reverse. These are target-only necessary pole conditions: they do not depend on the accepted seed's numerical center or on unknown inner coefficients within the signed-prefix class.

### Rank deficiency alone is insufficient

Let R_i be the full 8-by-64 Green row frame. A nonzero pure wanted-character row exists exactly when

    rank R_i > rank V_i^(forbidden).

This says that the forbidden-sector kernel contains a coefficient vector that does not annihilate the whole row. If all eight physical outer coefficients must be nonzero, that kernel must additionally not be contained in any coordinate hyperplane. These conditions are sufficient for one full-support pure-character row over characteristic zero: avoid the finite union of the forbidden full-row kernel and coordinate hyperplanes. They are not sufficient for the entire Fourier product.

For example, setting every pole to zero makes all Greens equal I. Every eight-by-eight projected determinant vanishes, but both the full and projected row frames have rank one; no nonzero coordinate row becomes a pure X character. The rank comparison prevents this false positive.

## 2. Exact finite test: all signed half-poles

Test exactly the 256 schedules

    tau_j=s_j/2, s_j in {+1,-1}.

Every Green denominator is the same nonzero rational 1-2^-64. At the verified prime p=998244353, 2 and 2^64-1 remain nonzero. The verifier checks each schedule using exact modular arithmetic on fixed rational matrices.

For every schedule:

- the row-0 minus-sector frame has rank eight;
- the row-1 minus-sector frame has rank eight;
- the full row-0 frame therefore has rank eight.

Each rank claim comes with an explicit eight-column minor and nonzero determinant, so it is a characteristic-zero statement, not merely a finite-field observation. Row 0 rules out every commuting prefix. Row 1 rules out every anticommuting prefix. Singular prefixes are separately impossible because Fourier is invertible.

For exactly 128 schedules, s_0=s_1 and the row-0 plus frame has rank seven. Its unique kernel is span((1,-1,0,0,0,0,0,0)); an exact seven-minor certifies rank at least seven and the equal-row identity certifies rank at most seven. Hence the corresponding pure-minus row forces six outer coefficients to zero. In the other 128 schedules the plus frame has rank eight.

Thus the pole change creates a genuine sector dependence but not a full-support Fourier escape in this family. The row-1 certificate also rules out the anticommuting-prefix route even if zero outer coefficients were permitted.

## 3. Why the H0 pair acquires a common sector

Let P_a and P_b be the H0-minus and H0-plus N64 routes. Their quotient permutations on the X-plus sector are equal. Before merging, horizontal steps x-2y and x+2y have the same x coordinate modulo four. Their small N16 covers and splices agree, so the same lifted low-coordinate correction is applied; the deterministic merge is also the same. Direct successor-array checks verify the equality independently.

Consequently, for any common legal pole t,

    G_a(t) Pi_+ = G_b(t) Pi_+.

The two full route permutations are different. Their relative permutation P_a^(-1) P_b consists of 16 two-cycles and 32 fixed points. Therefore

    rank(P_a-P_b)=16

over characteristic zero. This combinatorial certificate is included explicitly.

For t != 0 and t^64 != 1, the resolvent identity gives

    K(t)=G_a(t)-G_b(t)
        =t G_a(t)(P_a-P_b)G_b(t),
    rank K(t)=16.

Each Green commutes with X and their difference annihilates the plus sector. Thus

    K(t)=Pi_- K(t) Pi_-.

This is a genuine rank-16 sector-supported operator, not a full rank-32 projector. The guards are essential: t=0 would collapse the difference to zero, while t^64=1 would invalidate a Green inverse.

## 4. An allowed two-term mixing operator

Let chi_x be +1 on physical indices 0,...,31 and -1 on 32,...,63. Its diagonal anticommutes with X. Then

    M(t)=diag(chi_x)(G_a(t)-G_b(t))
        =Pi_+ M(t) Pi_-,
    rank M(t)=16.

This maps the minus sector into the plus sector. It uses exactly two allowed Green occurrences with a common legal pole and left masks chi_x and -chi_x. Both masks are everywhere nonzero. For instance, t=1/2 is an explicit guarded schedule. No new route or endpoint permutation has been introduced.

Application costs two length-64 Green scans, one vector subtraction and one character-mask application. Written in the original term grammar, these are two paid masked Green terms. Folding the component into existing terms is permitted only when the orders and poles really coincide; all remaining coefficients and guards must still be charged.

The opposite mixing direction is not supplied by this identity. Multiplying on the right by a character would change the fixed-right-endpoint grammar and cannot be silently inserted. Nor may a projected block be used as a free primitive merely because its mathematical support has been identified.

As a standalone component only two of eight possible labels are used. It does not satisfy a requirement that all eight outer row coefficients be nonzero. Adding it to a larger layer would require checking that layer's complete coefficients, both mixing directions, bank compatibility and every Fourier entry.

Finally, equalizing the H0 pair poles changes the accepted N16 seed's original distinct schedule (1/2,1/3,...,1/9). This component therefore does not automatically descend to the accepted seed operator or preserve its coefficient law. That bridge remains an explicit obligation.

## 5. What remains open

This single bounded family test supplies exact necessary pole equations, a finite negative classification, and one explicit paid mixing component. It does not rule out other legal pole schedules. It does not construct a full N64 Fourier factorization or an all-size lift.

A next positive construction would have to combine legal components into the required genuinely mixing coefficient law, account for any changed poles or endpoint grammar, and verify the full target system. In particular, the existence of one rank-16 directed mixing component is not a substitute for the two-direction conditions proved for the original outer schedule.

## 6. Reproduction

Run `python check_signed_poles.py`. The freshly authored verifier regenerates all routes, checks the pole formula, certifies all 256 schedules, verifies the relative permutation cycles, and checks the component's rank and sector support at t=1/2. The all-legal-t rank statement follows from the displayed resolvent identity and fixed permutation rank. No uploaded source or numerical coefficient fitting is executed.
