# One exact Schur step preserves a compact two-run tree jet

## Result and scope

One parity Schur elimination of the previously sealed pole-free border is constructive: its pivot is a weighted all-ones tree, its border dimension drops from N/2+1 to N/4+1, and every new feedback action on a constant vector has an O(N)-work complete numerator jet with at most 6N scalar slots. The actual formal series through degree log2 N also has an O(N)-work quotient-state evaluator. Markers can be retained in the corresponding scalar contraction.

This is one proved stage. The next literal parity pivot is not generally another single weighted functional-graph inverse. A finite exact countercontrol establishes that limited failure of closure, not an impossibility of another cheap inverse or a general FFT lower bound.

This additive report preserves ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md and all earlier seals. It uses the same independently specified graph, Library provenance, and no-uploaded-code-execution boundary.

## 1. Dimensions, coordinate maps, and the regularized recurrence

Let N=2^n>=8, m=N/2, l=N/4. Retain

    A_b e_s=omega^(b s)e_(2s+b mod N),
    K(z)=sum_(t=0)^(n-1) z^t(A_0^t-e_0 1^T),
    H(z)=C K(z)J,
    B(z)=[[I_m-zH,-e_0],[-z 1_m^T,1-z]].

Here J injects into odd global coordinates and (Cx)_r=omega^r(x_r-x_(r+m)). Let E and O inject length-l vectors into the even and odd coordinates of the interface E^m. Write H_EE=E^T H E, etc. E and O in this report are coordinate injections, not the root projector denoted E in the predecessor.

An explicit polynomial recurrence is also available. If v=(v_L,v_R) is split into halves, then

    (H_N(z)v)_(2a)=z[H_(N/2)(z)(v_L+v_R)]_a
                    -delta_(a,0) sum_s v_s,
    (H_N(z)v)_(2a+1)=omega^(2a+1)(v_L[a]-v_R[a]),       (1)

with child root omega^2 and scalar base H_2=-2. This is the regularized version of the Haar recurrence: the old root poles cancel to the explicit negative mass term. It follows either from the branch paths or by subtracting e_0 1^T/(1-z) from the unregularized recurrence; both sides are polynomials.

## 2. The odd pivot is exactly one weighted tree

Define length-l maps

    T_1 e_j=(omega^4)^j e_(2j+1 mod l),
    T_0 e_j=(omega^4)^j e_(2j mod l).

Direct entry inspection of the odd rows in (1) gives

    H_OO=omega^3 T_1,
    R:=H_OE=omega T_0.                                 (2)

Thus

    D(z)=I_l-z omega^3 T_1,
    q(z)=1-z omega^(-1).                               (3)

The map omega^3 T_1 is a tree toward l-1, whose root loop has weight omega^(-1). Its determinant is q. Its application and guarded inverse at one scalar z take O(l), with exact guard q(z)!=0. As a formal series at zero, q is a unit, so this Schur pivot is legitimate without choosing a numerical parameter.

A global lift makes the interaction transparent. Define L:E^l -> E^N by L e_j=e_(4j+3). Then

    A_1 L=L omega^3 T_1,
    L D(z)^(-1)=(I-zA_1)^(-1)L.                        (4)

The coordinates congruent to 3 modulo 4 are invariant under the all-ones transition. This identity includes the weights, not only the graph topology.

## 3. The exact reduced border and marked inputs

For x, write f=C Kx, f_E=E^T f, f_O=O^T f, sigma=1^T x. In the unknown ordering (e,o,t), eliminate o=D^(-1)(f_O+zR e). The resulting (l+1)-dimensional system is

    S e-e_0 t = f_E+z H_EO D^(-1)f_O,
    [-z 1_l^T-z^2 1_l^T D^(-1)R]e+(1-z)t
                 =sigma+z 1_l^T D^(-1)f_O,             (5)

where

    S=I_l-z H_EE-z^2 H_EO D^(-1)R.                     (6)

The eliminated coordinates are recovered by their displayed tree solve. This is an exact Schur identity, with no commutation assumption. Its sole new scalar pivot guard is q!=0; the reduced system itself still needs to be invertible to solve a full vector problem. In the formal series ring, its constant matrix is invertible.

The determinant relation is det B=q det B_reduced. Clearing the shared denominator by multiplying every reduced row by q changes the determinant to q^l det B. That known factor must be retained if determinant coefficients are used.

The odd right input is constant in z:

    (f_O)_j=omega^(2j+1)(x_(2j+1)-x_(2j+1+m)).           (7)

Both R e for constant e and f_O can therefore be formed in O(N). Using (4), the new vector feedback is exactly

    H_EO D^(-1)v=E^T C K(z)(I-z A_1)^(-1)Lv.            (8)

For a marker h, the pre-elimination scalar resolvent representation has coefficients

    a_E=z h^T KJ E,   a_O=z h^T KJ O,   a_t=h_0.

After eliminating o, its marked constant term gains a_O D^(-1) f_O, and its coefficient on e becomes a_E+z a_O D^(-1)R. Consequently each newly introduced marked contraction is also an instance of the same two-tree primitive (8). Markers remain variables throughout; specializing them to zero first would discard the requested answer.

## 4. A fully charged O(N) two-run primitive

Put lambda=omega^(-1), so A_1^(n+1)=lambda A_1^n, and define

    Ghat_1(z)=(1-lambda z)(I-z A_1)^(-1)
       =(1-lambda z) sum_(a=0)^(n-1) z^a A_1^a
          +z^n A_1^n.                                 (9)

For an arbitrary constant vector v, the complete polynomial

    K(z) Ghat_1(z) v                                   (10)

has degree at most 2n-1 and can be produced with O(N) scalar arithmetic, storage, and word addressing. Its at most 6N slots include all degrees, not only one selected coefficient.

### Explicit quotient-state algorithm

Generate w_a=A_1^a v for a=0,...,n. For each a, propagate that vector under A_0 for b=0,...,n-1. The potential support of

    Y_(a,b)=A_0^b A_1^a v

is an affine coset with exactly

    max(N/2^(a+b),1)                                   (11)

positions. This follows from the endpoint map

    s -> 2^(a+b)s+2^b(2^a-1) modulo N.

Each transition combines at most two current states, using its actual supplied edge weight. Weights are not discarded when states merge. The root-power table costs O(N); each edge weight is then an O(1) lookup. Cosets can be stored as deterministic arrays indexed by their high bits, with the low-bit prefix supplied by (11); no expected-time hashing is required by the cost claim.

For each (a,b), accumulate Y_(a,b)-e_0(1^T w_a) at degree a+b, with the coefficients and one-degree shift prescribed by (9). This is exactly (10). The aggregate state count is

    sum_(a=0)^n sum_(b=0)^(n-1) max(N/2^(a+b),1)
       <4N+n^2 <=6N.                                  (12)

The scalar root-projector updates cost O(n^2), also O(N). All input mass sums and initial A_1 propagation cost O(N). The algorithm never creates N entries for every time pair: it processes only the quotient-state arrays in (11).

### Output-slot bound

For nonzero output index r, write t=v_2(r), then let h be the length of the run of ones immediately above its t trailing zeros. Unless r=N-2^t, the degree in (10) is at most t+h+1. For each k=t+h<n, there are k*2^(n-k-1) such indices, and their slot bound is k+2.

The n exceptional indices r=N-2^t have degree at most n+t. The root coordinate has at most 2n slots. Therefore the total capacity is bounded by

    sum_(k=1)^(n-1) k(k+2)2^(n-k-1)
       +sum_(t=0)^(n-1)(n+t+1)+2n
       =5N+(n^2-3n-10)/2 <=6N.                         (13)

This also explains the compression: paths have one run of ones followed by one run of zeros. Typical coordinates admit only short runs; the few long-run exceptions do not create an N-times-log-N array.

### Actual formal truncation, not a free division

The actual series K(z)(I-zA_1)^(-1)v through degree d=n is computed directly by the same quotient arrays, retaining only a+b<=n. At those degrees the resolvent coefficient is exactly A_1^a; no generic series inversion is needed. The O(n^2) root updates and all coefficient additions remain charged. Equivalently, the numerator in (10) satisfies

    numerator[d]=series[d]-lambda*series[d-1]

through degree n. The verifier checks this coefficient identity individually. A blanket N-times-n division pass is neither required nor counted as free.

These claims start with constant v. Applying this primitive to an arbitrary already full polynomial-vector jet may need additional coefficient convolutions and does not inherit the same O(N) bound automatically.

## 5. The left marked jet: materialization versus a shared program

For odd j, the original left coefficient is

    (h^T K(z))_j=sum_(t=0)^(n-1) z^t(h_(2^t j mod N)-h_0).

Writing every column/degree value repeats m*n entries. At degree t there are only N/2^(t+1) different indexed h values across odd j, and their sum over t is N-1. Thus an O(N)-sized quotient-tree table represents the left jet; the expanded entry count is not a circuit lower bound.

The new two-run marked action has the same usable form: the quotient-state program in Section 4, followed by the h-weighted sum over its at most 6N output slots, computes every coefficient of h^T K Ghat_1 v in O(N) while retaining arbitrary h and constant v. This is an explicit bilinear arithmetic program, not a claim that the entire expanded marked row has been written out. It accounts for phases and weighted aggregation in the contraction, not merely the number of distinct h subscripts.

What is not proved is an O(N) contraction against the unknown polynomial vector e(z) produced by inverting the reduced feedback system. Feeding that jet into a constant-input program is an additional operation and may introduce many coefficient products.

## 6. Stage ledger and the limit of the proved recurrence

At this one stage:

- Interface dimension: m+1=N/2+1 before elimination, l+1=N/4+1 afterward.
- New inverse pivot: one weighted ones-tree, determinant q=1-z omega^(-1).
- New path word: one ones-run followed by one zeros-run, plus explicit root projections.
- Denominator representation: one shared degree-one factor q; root powers and addressing cost O(N).
- Full constant-input feedback numerator: degree at most 2n-1, at most 6N slots, O(N) work.
- Desired actual truncation: degree n, computed with the same O(N) bound and all updates charged.
- Marked representation: an O(N) arithmetic program for constant-input bilinear contractions, without materializing repeated marked-row entries.
- Remaining operation: invert the reduced bordered operator (5), whose even block is the coupled sum (6).

The implementation of this proved step uses a lift to the original N-coordinate trees. It does not establish that a second or rth elimination can be executed on a fresh N/2^r-coordinate tree with the same formula. Consequently a sum such as sum_r r N/2^r has not been justified.

Naively multiplying the two-run feedback repeatedly introduces more alternating runs and powers of the root denominator; that is not the same as proving a closed Schur recursion. No uniform bound for the subsequent run count, lifted state count, or coefficient contractions is claimed.

## 7. Countercontrol to literal single-tree closure

A weighted functional-graph map has at most one nonzero entry per column. Thus I-alpha T has at most one off-diagonal nonzero per column, even allowing arbitrary diagonal corrections.

For N=32, omega=3^2048 over GF(65537), z=1, the odd-odd block of the first reduced S in (6), in its natural next parity order, is exactly

    [    1,     0,     0,     0 ]
    [65535,   513,     2, 65025 ]
    [16384, 49153, 16385, 49153 ]
    [30151, 50827, 35386, 14711 ].

Its first column has three off-diagonal nonzeros. Every pivot used to produce this control is guarded in the verifier. Therefore this next pivot is not literally another single functional-tree matrix in those coordinates. This does not exclude a sum of tree maps, a low-rank correction, another routing, or a different cheap representation. Sparsity or a small local counterexample is not a general solve-cost lower bound.

## 8. Exact controls

The newly authored verifier runs 20 exact cases for N=8,16,32,64,128 and z=0,1,2,3 over GF(65537). It checks the weighted block identities (2), the first Schur recovery, the full-space lift (4), the complete compact numerator against independent dense resolvent oracles, marked contractions, and coefficient-by-coefficient formal truncation. Its largest observed structural slot ratio is 649/128, below the proved bound 6. The next-pivot countercontrol is recorded explicitly.

Dense matrices and solves are bounded verification oracles only. No source-uploaded code was executed. The all-size statements are the self-contained formulas and cost proofs above; the finite controls do not establish another fast inverse.

Companions: verify_one_schur_two_run_jet.py, ONE_SCHUR_TWO_RUN_CONTROLS.json, ONE_SCHUR_TWO_RUN_SHA256SUMS.txt.
