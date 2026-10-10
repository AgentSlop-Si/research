# N=5 is realizable with five signed magnetic banks

10 October 2026. An explicit characteristic-zero construction with exact certificates and independent acceptance at the source hash recorded in PROOF_STATUS.json.

## Result and status

**Theorem.** Let k be a characteristic-zero field containing a primitive fifth root q. The negative Fourier matrix F[k,t]=q^(−kt), with row and column indices 0,...,4, is the sum of five legal signed magnetic banks. All parameters and weights lie in Q(q). Combined with the accepted four-bank exclusion, **the minimum number of banks is exactly five** in this grammar.

The sufficiency statement is proved by the explicit witness below and exact coefficient substitution. The separate verifier checks the original inverse matrices as well. Independent review accepts the explicit witness, generic solvability lemma under its stated nonsingularity assumptions, and exact minimum in this grammar. The source proof and exported proof hashes are recorded separately in SOURCE_MANIFEST.json. This is neither a numerical search result nor a finite-field lifting claim.

## 1. Model and exact witness parameters

Use S e_i=e_(i+1 mod 5), T e_i=q^i e_i and W_(a,b)=S^a T^b. A bank with orientation (epsilon,delta) means

R = (1/5) sum_(j=0)^4 w_j [I−alpha S^epsilon−beta q^(epsilon delta j) T^delta]^(-1).

Its guard is Delta=1−alpha^5−beta^5 != 0. Put

c=q+q^4,
H=q/(1+q)=1+q+q^3,
z=−2−3q−3q^2−q^3,
t=1+q,
C=(1/5) sum_(j=0)^4 q^(−j^2)=(−1−2q^2−2q^3)/5.

Take these five banks, in the displayed order, with beta=1 throughout:

| Bank | epsilon | delta | alpha |
|---|---:|---:|---|
| 1 | +1 | +1 | 1 |
| 2 | +1 | +1 | z |
| 3 | −1 | +1 | q |
| 4 | +1 | −1 | t |
| 5 | −1 | −1 | t |

Thus only ++ is duplicated. Their guards are

Delta_1=Delta_3=−1,
Delta_2=269+760q+795q^2+325q^3,
Delta_4=Delta_5=3−5q^2−5q^3.

These identities follow by Delta=−alpha^5. The last two displayed polynomials are nonzero of degree less than four. Since Phi_5=1+q+q^2+q^3+q^4 is irreducible over Q, every guard is nonzero in every stated field. Also C != 0.

## 2. A tractable exact parameterization on a nonsingular set

This lemma explains the construction rather than treating the witness as a black box. It is not asserted to classify degenerate five-bank solutions.

Consider five banks ordered (++ with x), (++ with z), (−+ with y), (+− with v), (−− with u). Assume

- x,z,y,u,v are all nonzero;
- x != z;
- the matrices M_0 and M_2 below are nonsingular.

Fix beta=1 in every bank throughout this lemma. Let

M(y)=c y^2−q^2,  N(y)=(y+q^2)/c,
G=1+q+q^2,  P=1+q^4+q^3.

**Generic solvability lemma.** Under these assumptions, the five banks realize Fourier with some phase weights if and only if

u=c v^2−q^2,
v=c u^2−q^2,
N(y)=(x+z)M(y)−xz.                                    (1)


For clarity the row-b matrices have rows a=0,...,4 and the same five bank columns as above. Each column uses ell=[delta b]_5. In particular

M_0 =
[ 1    1    1    1    1   ]
[ x    z    y^4  v    u^4 ]
[ x^2  z^2  y^3  v^2  u^3 ]
[ x^3  z^3  y^2  v^3  u^2 ]
[ x^4  z^4  y    v^4  u   ],

M_2 =
[ 1       1       1       1     1      ]
[ Gx      Gz      0       −qv   0      ]
[ q^2x^2  q^2z^2  0       0     0      ]
[ 0       0       q^3y^2   0     0      ]
[ 0       0       Py      0     −q^4u  ].

For nonzero y,u,v and x != z, M_2 is nonsingular precisely when

x+z+(G/(qv))xz != 0.                                  (2)

The third square matrix, M_3, is

[ 1       1       1       1       1      ]
[ −q^4x   −q^4z   0       Pv      0      ]
[ 0       0       0       q^3v^2   0      ]
[ 0       0       0       0       q^2u^2  ]
[ 0       0       −qy     0       Gu     ].

M_3 is automatically nonsingular under the nonzero/distinct assumptions. Rows a=2,3,4 determine three amplitudes, and the remaining two columns on rows a=0,1 have determinant q^4(x−z).

### Proof of the lemma

Normalize all sector amplitudes by C. The desired Weyl coefficient is then f(a,b)=q^(4(a+b)^2).

At b=1, the two delta=−1 banks contribute only at a=0. The a=4 coefficient fixes h_(−+,1)=H/y. The three remaining nonaxis equations are exactly

h_(x,1)x+h_(z,1)z=H,
h_(x,1)x^2+h_(z,1)z^2=H M(y),
h_(x,1)x^3+h_(z,1)z^3=H N(y).

The first two solve to

h_(x,1)=H(z−M(y))/(x(z−x)),
h_(z,1)=H(M(y)−x)/(z(z−x)).

Their third moment equals (x+z) times the second minus xz times the first. Thus the last equation in (1) is necessary and sufficient for this row's nonaxis entries.

At b=4, simultaneous reflection (a,b) -> (−a,−b) preserves f. Only the two delta=−1 ell=1 sectors contribute at nonzero a. Their endpoint amplitudes are H/u and H/v; their remaining two conditions are precisely the first two equations in (1).

For each of these two rows, an opposite-delta ell=4 sector affects only a=0, so the axis entry can be set freely after the nonaxis entries. For b=0,2,3, solve the five-by-five systems M_b h_b=f_b. They are nonsingular under the stated hypotheses. The amplitudes for distinct b use distinct ell in every bank; solving one row never changes another. This proves sufficiency. Necessity follows from the nonaxis row equations already derived. Finally beta=1 and Delta=−alpha^5 make every chosen amplitude legal via the phase-weight conversion in section 4.

No claim is made about solutions with a zero alpha, x=z, det M_0=0, or det M_2=0. Such cases are unnecessary for the exhibited realization.

## 3. Specializing the lemma to the witness

Choose y=q and x=1. Then

M(q)=q−q^2+q^3,
N(q)=1+2q+2q^2+q^3,
z=(N(q)−M(q))/(M(q)−1)=−2−3q−3q^2−q^3.

This enforces the third equation in (1). Choose u=v=t=1+q. Direct reduction modulo Phi_5 gives c t^2−t−q^2=0, enforcing the first two equations.

The exact square-row determinants in the stated row and column orders are

det M_0=−1093−5351q−6894q^2−3592q^3,
det M_2=31+21q−17q^2−30q^3,
det M_3=6+19q+21q^2+9q^3.

Each is a nonzero polynomial of degree less than four, and therefore cannot vanish at a primitive fifth root in characteristic zero. The simpler factor in (2) is −3−6q−4q^2−q^3, also nonzero. All remaining denominators and nonzero/distinct assumptions of the lemma are satisfied. This proves existence without an approximate root or parameter search.

The full five-row coefficient systems have ranks 5,4,5,5,3 for b=0,1,2,3,4, respectively. The three amplitude freedoms are axis-only ell=4 choices, and are fixed in the following explicit witness.

## 4. Complete amplitudes and original branch weights

For an integer four-tuple A=(A_0,A_1,A_2,A_3), write [A]/d=(A_0+A_1q+A_2q^2+A_3q^3)/d. The following table specifies every normalized amplitude h_(bank,ell). The actual sector amplitudes are C times these entries.

| Bank | ell | Numerator tuple A | Denominator d |
|---:|---:|---|---:|
| 1 | 0 | (−341,98,−3688,−3524) | 3355 |
| 1 | 1 | (−12,6,−10,−8) | 11 |
| 1 | 2 | (314,−212,137,356) | 1705 |
| 1 | 3 | (14,−62,−3,−9) | 55 |
| 1 | 4 | (−5,−1,−3,−3) | 1 |
| 2 | 0 | (78254,8168,42937,56276) | 104005 |
| 2 | 1 | (−27,−9,−11,−26) | 11 |
| 2 | 2 | (−94,−1218,578,−1236) | 1705 |
| 2 | 3 | (41,−48,58,9) | 55 |
| 2 | 4 | (0,0,0,0) | 1 |
| 3 | 0 | (−603,−341,−164,2583) | 3355 |
| 3 | 1 | (0,−1,0,−1) | 1 |
| 3 | 2 | (1,0,0,0) | 1 |
| 3 | 3 | (1,1,1,0) | 1 |
| 3 | 4 | (0,0,0,0) | 1 |
| 4 | 0 | (5206,−2731,6584,−7684) | 20801 |
| 4 | 1 | (2,0,1,1) | 1 |
| 4 | 2 | (−1,1,−1,0) | 1 |
| 4 | 3 | (−35,26,−13,16) | 31 |
| 4 | 4 | (28,3,10,34) | 11 |
| 5 | 0 | (187,84,281,73) | 671 |
| 5 | 1 | (2,0,1,1) | 1 |
| 5 | 2 | (−1,1,−1,0) | 1 |
| 5 | 3 | (0,1,0,0) | 1 |
| 5 | 4 | (0,0,0,0) | 1 |

For bank n, with orientation (epsilon_n,delta_n), the original phase weights are exactly

w_(n,j)=C Delta_n sum_(ell=0)^4 h_(n,ell) q^(−epsilon_n delta_n j ell), j=0,...,4.    (3)

No further scaling is implicit: the bank definition already has its 1/5 average. `../certificates/n5/WITNESS.json` contains every parameter, guard, normalized amplitude, and all 25 expanded raw phase weights, each as four rational coefficients in the basis 1,q,q^2,q^3. Equation (3) and the displayed table suffice to reproduce that file independently.

## 5. Exact controls

`verify_five_bank.py` is a newly authored, standard-library-only verifier that reads the literal `WITNESS.json` constants. Its field arithmetic uses rational coefficients modulo Phi_5; all requested field inverses are checked by multiplication. It does not import or execute any predecessor or supplied research program.

It checks:

1. Every target Weyl coefficient, independently extracted by the direct trace formula from F.
2. Every reconstructed normalized Weyl coefficient from the five banks and the Gaussian coefficient recurrence.
3. All five nonzero Delta guards and the conversion from normalized amplitudes to the supplied raw weights.
4. Each of the 25 original signed branch inverses, by multiplying on both the left and the right.
5. Every entry of the original Fourier matrix against the weighted sum of those 25 inverse matrices.

For the inverse checks it constructs X_j=alpha S^epsilon+q^(epsilon delta j)T^delta and the candidate inverse (I+X_j+...+X_j^4)/Delta, then checks both products with I−X_j exactly. Therefore the original-matrix check does not rely solely on the previously accepted bank coefficient formula.

See REPRODUCE.md at the packet root for a self-contained temporary working layout. The original literal witness checker and its exact result data are included. A separately written verifier uses literal Gaussian inversion and checks all four primitive-root conjugates. The independent acceptance also checks the previously accepted lower-bound source hashes.

## 6. Scope, lower-bound dependency, and remaining questions

The construction gives five-bank sufficiency in every characteristic-zero extension containing q; no extra algebraic extension is required. The exact minimum additionally uses the signed-support gate, which forces all four orientations, and [the accepted four-bank exclusion](06_four_bank_lower_bound.md), which excludes one bank in each orientation. Thus at most four banks are impossible and this five-bank construction attains the lower bound.

The nonsingular parameterization is a proved sufficient-and-necessary criterion only under its complete stated assumptions. Singular strata, positive-characteristic variants, and the classification of all five-bank solutions remain open here. The displayed rational denominators and determinant residues prevent an automatic all-characteristic conclusion.

This is a small exact realization in the stated bank grammar. It is not an FFT algorithm, a speedup, a lower bound on arithmetic runtime, or a historical-priority claim. Weight preparation, storage, literal inverse applications, and any possible cost sharing would require their own fully charged analysis. The algebraic mechanisms are classical Gaussian coefficients, moments, interpolation, and cyclotomic arithmetic.
