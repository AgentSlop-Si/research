# Extending the signed-bank dictionary: general odd length and an exact N=13 gate

14 October 2026. **Candidate mathematical result, subject to independent review.**

## Result first

The original signed-resolvent identities and the forced-window method extend to every odd length N over a field K containing a primitive Nth root q. The accepted N=11 minima do not extend automatically.

For the next odd size, with N=13 and q=16 in F53, the fresh exact computation establishes:

- Over every extension K/F53, the free-cross-singleton architecture requires at least seven nonzero effective nodes in each same-sign orientation, hence at least sixteen physical banks.
- Over F53 itself, it requires at least eight such nodes per side, hence at least eighteen physical banks.
- A legal original-grammar witness with allocation (11,1,1,11) gives twenty-four nonzero physical banks over F53.

Consequently, for this fixed N=13, q=16 dictionary,

    16 <= b(K) <= 24 for every extension K/F53,
    18 <= b(F53) <= 24.

The upper bound persists after scalar extension because its raw certificate lies in F53. No exact N=13 minimum is claimed. These bounds concern exactly one effective alpha node in each cross-sign orientation. They do not concern unrestricted orientations or other primitive thirteenth roots.

**There is no FFT improvement here.** A physical bank is an operator containing N inverse branches. Its count is not its arithmetic cost. The standard odd-length chirp identity already reduces the DFT itself to one cyclic convolution. A bank-based speed claim must beat that paid baseline, including input/output, constant generation and coefficient-field arithmetic.

## 1. Source boundary

Read-only historical inputs are bound by exact size and SHA-256 in outputs/SOURCE_BINDINGS.json:

1. singleton_minimum_synthesis_0149/RESEARCH_NOTE.md: the accepted/dependency-matched N=11 minima 14, 13 and 12 over F23, F23^3 and F23^5.
2. review_cubic_thirteen_0145/REVIEW.md: accepted literal original-bank grammar, thirteen-bank witness, and exact scope.
3. parameter_annihilator_gate_0131/CONTRACT.md and REPORT.md: the fixed-N=11 degree-five parameter gate and its limitations.
4. review_twelve_independent_2212/PRIOR_ACCEPTED_GRAMMAR.md: original-bank expansion, grouping rules, zero/repeated nodes, reflection and lower-bound necessity.

Historical programs were never executed, imported, or compiled. The new programs are fresh_n13_gate.py and check_certificates.py. This report does not reinterpret the accepted N=11 result or claim independent acceptance for its own computation.

The field change is deliberate and explicit. F53 contains primitive thirteenth roots already in its prime field; 16^13=1 and 16!=1, so 16 has exact order thirteen. This is a new admissible instance of the same grammar, not a lift of q=13 in F23. Keeping characteristic 23 at N=13 would instead require at least a degree-six extension to contain a primitive thirteenth root, because the order of 23 modulo 13 is six. That instance was not tested.

## 2. The general dictionary

Let N>=3 be odd, let K be a field with characteristic not dividing N, and let q in K have exact order N. Indices are in Z/NZ. Set

    S e_t = e_(t+1),        T e_t = q^t e_t,
    F[k,t] = q^(-kt).

One counted physical bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/N) sum_(j=0)^(N-1) w_j
          (I-alpha S^epsilon-beta q^(epsilon delta j)T^delta)^(-1),
    Delta = 1-alpha^N-beta^N != 0,
    epsilon,delta in {+1,-1}.

All parameters and all raw weights lie in K. No target transformation, pre/post map, bank product, derivative atom, singular limit, infinite node or trace-bank primitive is inserted into the grammar. The analysis below permits beta=0 and alpha=0 whenever Delta is nonzero.

Group banks with the same orientation and alpha by their whole sector-amplitude vectors. An effective node is a group with nonzero vector. This grouping only supplies necessary conditions; physical-bank counting continues to count the actual original summands. Exactly one effective node y is required in (-,+), and exactly one effective node z in (+,-). They are independently free.

## 3. Identities that generalize without an N=11 accident

### 3.1 Finite inverse and Gaussian support

For U=S^epsilon, V=T^delta and omega=q^(epsilon delta), we have VU=omega UV. Let D_omega(r,l) be the coefficient of U^r V^l in (U+V)^(r+l). Right multiplication gives

    D(r,l) = omega^l D(r-1,l) + D(r,l-1),  D(0,0)=1.

For r+l<N, the Gaussian product formula has only nonzero numerator and denominator factors. Thus D(r,l)!=0 there. At total degree N, each mixed coefficient contains 1-omega^N in its numerator, while its denominator factors are nonzero; hence

    (alpha U+eta V)^N = (alpha^N+eta^N)I.

For eta=beta q^(epsilon delta j), eta^N=beta^N. Telescoping therefore gives the original literal branch inverse

    (I-X_j)^(-1) = (I+X_j+...+X_j^(N-1))/Delta.

This proof works for composite odd N as well as prime N. Oddness is needed later for the square completion, not for this inverse identity itself.

Put r=[epsilon a]_N and l=[delta b]_N. Define G_(epsilon,delta)(a,b)=D(r,l) when r+l<N, and zero otherwise. The Weyl coefficient of the bank at S^a T^b is

    alpha^r G_(epsilon,delta)(a,b)
       beta^l/(N Delta) sum_j w_j q^(epsilon b j).

There is no division by alpha or beta in this identity.

### 3.2 Literal Fourier coefficients and the nonzero normalization

For any matrix M, its Weyl coefficients are

    c_M(a,b) = (1/N) sum_t M[(t+a) mod N,t] q^(-bt).

Let h be the inverse of 4 modulo N and gamma=(1/N)sum_t q^(-t^2). Completing the square modulo N gives

    c_F(a,b) = gamma q^(h(a+b)^2).

The scalar gamma is nonzero in every permitted field. Indeed, writing G_-=sum q^(-t^2) and G_+=sum q^(s^2), the invertible change of variables (s,t)->(s-t,s+t) modulo odd N proves

    G_- G_+ = sum_(u,v) q^(uv) = N != 0.

Thus normalization by gamma is legal, including in characteristic two when such an odd-order root exists. This is coefficient bookkeeping; it does not modify the target operator.

Write f(a,b)=q^(h(a+b)^2). A bank contributes normalized coefficient

    A_b alpha^r G_(epsilon,delta)(a,b),
    A_b=beta^l/(N Delta gamma) sum_j w_j q^(epsilon b j).

### 3.3 Forced windows and the general recurrence gate

Let n=(N-1)/2. For b=1,...,n, only (-,+) supports the coordinate (N-b,b). Its normalized target coefficient is one. Therefore y!=0 and its grouped amplitude is forced:

    T_b(y)=1/[y^b G_-+(N-b,b)].

For b<=a<=N-b-1, the two negative-delta orientations vanish, and G_++(a,b)!=0. Every legal representation consequently satisfies

    v_b(a;y)
      = [f(a,b)-T_b(y)y^(N-a)G_-+(a,b)]/G_++(a,b)
      = u_(b,a)-d_(b,a)y^(N-a-b)
      = sum_(x in X) A_(b,x) x^a,

where X is the distinct nonzero effective ++ support. Zero nodes contribute nothing to these positive-exponent windows. Repeated ordinary nodes only add amplitudes; they do not create derivatives. Arbitrary beta choices and cancellations are already covered.

The consecutive windows s_(b,j)=v_b(b+j;y) have lengths

    L_b=N-2b,       b=1,...,(N-1)/2.

Any m-node support gives a monic annihilator H(t)=product_(x in X)(t-x), and therefore

    sum_(k=0)^m H_k s_(b,j+k)=0

for every available window. For 0<=m<=N-1 the number of these equations is

    R_N(m)=sum_b max(N-2b-m,0)
          = floor((N-m-1)^2/4).

If a smaller support exists, multiplying its annihilator by a power of t gives a monic degree-m annihilator. This is algebraic padding for a necessary condition, not an added bank or a squarefree-root claim.

Reflection (a,b,epsilon,delta)->(-a,-b,-epsilon,-delta) preserves both f and G. It gives the same necessary bound for -- with the independent parameter z. No equality y=z is assumed.

The equation count explains a key size change: N=11,m=5 gives six equations in five unknown monic coefficients, while N=13,m=6 gives nine equations in six unknowns. Dimension counting alone is not a nonexistence proof. The exact minors below supply that proof for the chosen N=13 instance.

## 4. Exact N=13 extension obstruction

Here p=53, q=16, h=10 modulo thirteen and gamma=7. The fresh program directly checks every one of the 169 Fourier Weyl coefficients, derives the Gaussian table by noncommutative multiplication, and verifies the mixed degree-thirteen coefficients vanish.

The six forced window lengths are 11,9,7,5,3,1. The degree-six augmented recurrence matrix E(y) has nine rows and seven columns, with row labels

    (1,0),(1,1),(1,2),(1,3),(1,4),
    (2,0),(2,1),(2,2),(3,0).

Columns are the seven consecutive moments, so a monic sextic would supply a nonzero vector (h0,...,h5,1) in its kernel.

Take the two maximal minors on zero-based row sets

    I={0,1,2,3,4,5,6},    J={0,1,2,3,4,5,7}.

Fresh polynomial Bareiss elimination gives polynomials d_I,d_J of degree 39. Their exact ascending coefficients and two degree-38 Bezout polynomials U,V are saved in GATE.json and obey the directly checked identity

    U(y)d_I(y)+V(y)d_J(y)=1 in F53[y].

Thus no algebraic value y can make both minors vanish. E(y) has column rank seven for every y over every extension of F53. It has no nonzero kernel, hence no monic degree-six or smaller common annihilator. A full legal singleton-bank representation therefore needs at least seven nonzero effective ++ nodes. Reflection gives seven -- nodes, and the two effective cross groups require two further physical banks: B>=16 over every extension.

This is stronger than a sweep of 52 base-field values. It also excludes the naive N+1=14-bank extrapolation of the N=11 degree-five-field construction throughout this characteristic-53/q=16 family. It does not rule out a different q or characteristic.

As a concrete specialization, y=1 gives degree-six coefficient rank six and augmented rank seven. The obstruction is exact, not numerical.

## 5. Base-field strengthening to eighteen banks

For monic degree seven there are six recurrence equations in seven unknown coefficients. For every y in F53*, the coefficient rank is exactly six, and the system is consistent. Each solution set is therefore an affine line with exactly 53 members.

The code explicitly enumerates all 52*53=2,756 monic polynomials and evaluates each at all 52 nonzero F53 residues. Every member has fewer than seven distinct nonzero roots; the maximum is six. Each polynomial and its complete nonzero-root list is retained in GATE.json.

For example, at y=1 the entire affine family is

    H_lambda(t)=t^7+lambda t^6+(50+22lambda)t^5
       +(48+15lambda)t^4+(27+10lambda)t^3
       +(19+11lambda)t^2+(50+25lambda)t+(16+31lambda),
    lambda in F53.

No member of this family, or of any other y family, splits into seven distinct nonzero base-field nodes. Since the all-extension argument already excludes six or fewer, a base-field representation requires at least eight ++ nodes. Reflection independently requires eight -- nodes. Therefore B>=18 over F53.

This is a base-field splitting obstruction. It is not promoted to the same eighteen-bank lower bound over extensions, where a degree-seven annihilator might split.

## 6. Literal twenty-four-bank upper certificate

The declared coarse baseline uses

    ++ support = -- support = {1,2,...,11},
    y=z=1,    beta=1 for every bank,
    allocation (11,1,1,11).

All twenty-four orientation/alpha pairs are distinct. Every Delta=-alpha^13 is nonzero. For each sector b=0,...,12, the complete 13-by-24 coefficient system has rank thirteen and is consistent. A deterministic solution is recovered into raw original phase weights by

    w_(i,j)=Delta_i gamma sum_b A_(i,b)q^(-epsilon_i b j).

The fresh code constructs and independently inverts each literal original 13-by-13 branch matrix, applies the original 1/13 factor, and checks:

- 312 literal inverse matrices, with 624 left/right inverse identities.
- Every one of the 312 forward/raw character-transform identities.
- Every one of the 24*169 extracted bank Weyl coefficients.
- All twenty-four banks nonzero, including the two cross banks.
- All 169 aggregate entries equal the direct literal Fourier target.

The complete matrices and raw weights are in BASELINE.json. This witness is intentionally a bounded existence baseline; it is not asserted optimal or competitive. No degree-seven split supports survived, so none of the conditional small-support full-sector tests were run.

## 7. Arithmetic accounting and the FFT comparison

### Physical count is not a cost model

Each physical bank contains N weighted inverse branches. A literal inverse branch is a cyclic bidiagonal solve. With alpha!=0 it can be solved in O(N) field operations even when one diagonal entry is zero: solve the row equation backward by division by alpha, then close the cycle using Delta!=0. With alpha=0 the legal branch is diagonal and also costs O(N).

One explicit paid implementation for alpha!=0, with constants precomputed, is as follows. Order the cycle by t_(s+1)=t_s-epsilon and write

    x_(t_(s+1)) = a_s x_(t_s)+b_s,
    a_s=(1-beta q^(epsilon delta j+delta t_s))/alpha,
    b_s=-v_(t_s)/alpha.

Precompute the closure multiplier. The b_s are shared by the N branches of one bank and cost N scalar multiplications. For each branch, forming its affine closure costs N-1 multiplications and N-1 additions; solving the starting value costs one multiplication; propagating the other N-1 values costs N-1 multiplications and N-1 additions. Weighting and summing the N branch outputs costs another N^2 multiplications and N(N-1) additions. This is a valid, unoptimized per-bank upper budget of

    3N^2 multiplications and 3N^2-3N additions,

after constant preprocessing. All zero/one scalar simplifications are deliberately omitted from this upper budget. It is not a lower bound, and evaluating branches independently is not claimed best possible.

For the twenty-four-bank N=13 witness this literal schedule costs at most 12,168 multiplications and 11,531 additions, including summing its twenty-four bank outputs. It also needs preprocessing/storage for the branch constants. Direct dense application of the 13-by-13 target costs at most 169 multiplications and 156 additions with its coefficients precomputed. The literal bank schedule is therefore not a useful arithmetic improvement at this size.

### The fair fast baseline already uses convolution

Let h2=2^(-1) modulo odd N. The identity

    q^(-kt)=q^(-h2 k^2) q^(h2(k-t)^2) q^(-h2 t^2)

holds exactly. Thus the DFT itself is a diagonal scale, one cyclic convolution with kernel q^(h2 r^2), and another diagonal scale. If M_K(N) denotes a paid cyclic-convolution cost over the same field, this is M_K(N)+2N scalar multiplications, plus preprocessing.

An efficient structured evaluator for each bank can improve upon the literal quadratic schedule. That alone is insufficient: the comparison must be against the one-convolution target baseline, not against treating Fourier evaluation as a dense matrix. Summing B independently evaluated convolution-like bank terms ordinarily multiplies the convolution work by B. Only a proved joint sharing/cancellation algorithm, with a complete total operation count, could establish a different conclusion. No such algorithm is supplied here.

Extension-field multiplication is also not a prime-field multiplication. The accepted N=11 cubic and quintic minima must be charged for arithmetic in their respective fields before comparing them with a prime-field FFT or NTT. This N=13 witness avoids that issue by using F53 itself, but still has no speed advantage.

## 8. Which accepted minima are special, and the next gate

The general identities above do not transfer these N=11-specific facts: the six-by-six determinant, its degree-27 parameter polynomial, its characteristic-23 factor degrees 1,1,7,18, the quintics at y=4 and y=15, their degree-five/cubic splitting fields, the full-sector cubic obstruction, or the exact physical-bank minima 14/13/12. All depend on the particular N,q,coefficient field and full-sector equations. Even a compatible split annihilator remains only a necessary-window result until the remaining sector equations and literal raw banks are checked.

There are two precise, distinct next gates:

1. **Representation gate at the tested size.** Decide whether eight same-sign nodes per side can attain eighteen banks over F53, or tighten the current interval 18..24. At degree eight, the forced windows give four equations in eight coefficients, so a naive sweep over all y and all polynomial coefficients is much larger than this bounded test. A structural splitting/annihilator argument is preferable. Any surviving supports must pass every full sector and literal raw-weight reconstruction. This gate was not launched.
2. **Speed gate for any growing family.** Specify an explicit family of lengths/fields/roots, construct legal full-bank witnesses, and exhibit one algorithm for applying the entire bank sum to an arbitrary input. Charge field operations, coefficient construction, storage, input/output and field-extension costs. Compare its total with the paid chirp/convolution baseline on the same field and output contract. Merely reducing B, tensoring a fixed codelet, or assigning unit cost to a bank cannot establish sub-N-log-N work.

The first gate could improve a finite representation theorem. The second is indispensable for the user's FFT question. Neither is silently treated as solved by this packet.

## 9. Reproduction, checks, errors and stopping point

Run from a workspace containing the five bound historical text sources:

    python3 -I signed_bank_n13_extension_1310/fresh_n13_gate.py
    python3 -I signed_bank_n13_extension_1310/check_certificates.py signed_bank_n13_extension_1310/outputs

Only standard-library Python is required. The second checker uses direct Leibniz determinants at every one of the 53 base-field values (106 checks), separately verifies the polynomial Bezout identity, checks the complete degree-seven enumeration, and verifies stored inverse matrices against the original two-entry-per-column branch matrices before reconstructing the target. This second producer check is not an independent review.

An isolated cold workspace containing only these fresh programs and copies of the five bound text sources reproduces all six deterministic JSON files byte for byte. REPLAY_VERIFICATION.json retains exact hashes and sizes; timing files are excluded from byte equality. Timing records measure arithmetic wall time, not reasoning or review time.

One development error occurred in the second checker after its mathematical assertions had completed: an orientation variable shadowed the output-directory variable and prevented writing its result file. It was renamed and the complete checker and cold replay were rerun successfully. CHECK_DEVELOPMENT_ERROR.log preserves the original error. No preview/resource limit or mathematical assertion failure occurred. No replacement search, package install, network access, external write, or supplied historical-code execution occurred.

The declared experiment stopped after two maximal minors reached gcd one, all 2,756 degree-seven candidates were exhausted, and the single prescribed coarse baseline was literally certified. This packet is ready for separate review; it makes no novelty, exact-minimum, unrestricted-architecture, characteristic-zero, all-length-construction, or FFT-speed claim.
