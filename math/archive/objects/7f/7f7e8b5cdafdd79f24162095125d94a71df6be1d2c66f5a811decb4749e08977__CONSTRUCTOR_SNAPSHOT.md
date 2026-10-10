# Necessary resolvent tests for the forced odd-chirp B

## Result

The odd-chirp construction fixes B exactly; a low-degree loop alone does not give its implementation. Two additional necessary tests are proved here:

1. A product of L single weighted-permutation Green inverses, even with arbitrary monomial endpoints and independent cycle orders, needs L>=ceil(log2 N). Thus no bounded-length pure product represents this B for growing N.
2. Across every complementary coordinate cut, B has exactly the inverse-Fourier cut rank. Therefore a bounded sum or product must supply enough crossing rank through its cycle and endpoint routing. A sum of two diagonal-ended Green terms needs at least floor(N/2) combined cycle crossings across every cyclic contiguous half interval.

The second condition does not exclude general independently ordered paired-Green sums. No admissible positive family for B is supplied; the remaining task is an exact coefficient factorization with a uniform cost certificate.

## 1. Fixed target and guards

Let N>=3 be odd, h=(N+1)/2 modulo N, and F[i,j]=omega^(ij) be unnormalized Fourier. The field contains a primitive Nth root omega and has characteristic not dividing 2N. Define

    A=diag(omega^(h j^2)),
    G=sum_j omega^(h j^2),
    c=N G,
    B=(F^(-1)+A)^(-1).

Require 1+c!=0. The odd-chirp report proves (FA)^3=cI, the displayed inverse exists under that guard, the Fourier transfer equals (I-BA)^(-1)B, and the loop has a cubic annihilator. Over C the guard is automatic because |c|=N^(3/2)>1. Over finite fields it must be checked explicitly.

This B is an arbitrary-input operator, not an input-dependent approximation. Its inverse is the particularly simple specified matrix

    X=B^(-1)=A+F^(-1),
    F^(-1)[i,j]=N^(-1)omega^(-ij).                    (1)

The source package is ACFF, Library [private-id], ZIP SHA-256 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9. The constructive chirp formulas are proved separately in ODD_CHIRP_CUBIC_GATE.md. These are new scoped deductions, not an external novelty claim. No uploaded code is executed.

## 2. Every field under the guards has at least one full inverse row

All off-diagonal entries of X are nonzero. Over C, every diagonal entry is also nonzero: A[i,i] has modulus one while F^(-1)[i,i] has modulus 1/N. Hence X is entrywise dense over C.

In allowed finite fields a diagonal entry may cancel, but at least one does not. Suppose all diagonal entries vanished. The zeroth diagonal would give 1+N^(-1)=0, or N=-1 as a field element. The first diagonal would then give omega^h-omega^(-1)=0, so omega^(h+1)=1. Since h+1=(N+3)/2, primitiveness forces N to divide 3. With N>=3 odd this gives N=3, and N=-1 in the field would force characteristic two, contrary to the guard. This contradiction proves that at least one row of X has exactly N nonzeros over every allowed field.

Do not strengthen this to all finite-field entries being nonzero. For example, over F521 at N=5 and omega=104, the guard is valid (c=47), but diagonal entries of X are [418,24,0,0,24]. Its maximum row support is still five.

## 3. No bounded pure product of Green resolvents

Suppose

    B=G_L ... G_1,
    G_l=L_l (I-W_l)^(-1) R_l,

where W_l is a weighted permutation matrix and L_l,R_l are monomial endpoints. All square factors must be invertible because B is invertible. Thus

    G_l^(-1)=R_l^(-1)(I-W_l)L_l^(-1)

has at most two nonzeros per row, irrespective of permutation order. Monomial multiplication preserves row-support bounds. Row support is submultiplicative under matrix multiplication, giving

    max_row_support(B^(-1))<=2^L.

Section 2 therefore implies

    2^L>=N,   L>=ceil(log2 N).                         (2)

This is valid for arbitrary independent cycles, arbitrary nonzero edge weights or allowed zero weights, and arbitrary monomial endpoint routing. It is not restricted to the natural cycle or parity-compatible cycles.

More generally, if the lth inverse denominator is I minus a sum of g_l weighted permutations, the necessary bound is

    product_l (g_l+1)>=N.                              (3)

For a single denominator this gives g>=N-1. These bounds concern the number of sparse-denominator factors in the specified direct representation. They do not exclude sums of Green maps, products whose factors are themselves Green sums, auxiliary-variable Schur complements, or a different optimized circuit.

A literal sequential implementation with L separately applied linear-scan factors would consequently retain at least logarithmically many scans. Equation (2) is not a lower bound for every shared or otherwise reorganized arithmetic algorithm producing the same operator.

## 4. Exact complementary-cut rank inheritance

For any invertible square T and coordinate set I, let Ic be its complement. Then

    rank T[I,Ic]=rank T^(-1)[I,Ic].                    (4)

A short proof avoids assumptions on principal subblocks. Let Vc be the coordinate subspace supported on Ic. The nullity of the map Vc -> E^I induced by T is dim(Vc intersect T^(-1)Vc). Applying T identifies this space with TVc intersect Vc. That last dimension is the nullity of the analogous map induced by T^(-1). Both domains have dimension |Ic|, proving equal ranks.

Use (4) with T=B. Since A is diagonal, (1) gives

    rank B[I,Ic]=rank F^(-1)[I,Ic]                      (5)

for every I. In particular, if I consists of m=floor(N/2) cyclically consecutive coordinates, the Fourier rectangle has rank m: after a nonzero column scaling its first m distinct columns form a Vandermonde matrix in distinct Nth roots. Thus

    rank B[I,Ic]=m.                                   (6)

This survives the fact that B is close to the diagonal A^(-1) in complex operator norm. The full-rank correction carries exactly this cross-coordinate coupling; replacing it by zero loses the target.

## 5. Necessary routing budget for sums or products

For a weighted permutation W with row convention (Wx)[i]=w[i]x[pi(i)], define

    e_pi(I)=#{i in I : pi(i) in Ic}.

Its inverse Green action Q^(-1), Q=I-W, has off-diagonal cut rank at most e_pi(I): apply (4) to Q and note that Q[I,Ic] is a partial matching. Zero weights may lower its rank.

For any matrices U,V,

    rank (U+V)[I,Ic] <= rank U[I,Ic]+rank V[I,Ic],
    rank (UV)[I,Ic] <= rank U[I,Ic]+rank V[I,Ic].

The second inequality follows by splitting the intermediate coordinates into I and Ic. Thus a sum or product containing r Green terms with diagonal endpoints must satisfy, at every cyclic contiguous half interval,

    sum_(s=1)^r e_pi_s(I) >= floor(N/2).               (7)

The same condition holds for endpoints preserving that tested cut. With arbitrary monomial endpoints, add their own off-diagonal permutation crossing counts to the left side; endpoint routing cannot simply be omitted from the budget. More complicated sum/product expressions obey the corresponding bound counting Green and endpoint occurrences, but this count alone is not a DAG-sharing cost lower bound.

For the source's paired-Green B, the diagonal-ended r=2 case is a precise necessary synthesis test. Passing it is not sufficient: no Fourier phase or coefficient identity follows from crossing capacity alone.

For example, natural cycles each contribute one crossing to such an interval, so two diagonal-ended natural-cycle terms cannot realize B at odd N>=7. Conversely a Hamiltonian jump by m=(N-1)/2 crosses every half interval m times; it passes this cut test even as one term, but one term is excluded by the inverse-support result. This shows that the two tests detect different defects and that passing the routing gate is not a construction.

## 6. Average edge displacement required of diagonal-ended sums

Let I_t, t=0,...,N-1, be all cyclic intervals of length m=(N-1)/2. Define dist_N(i,j)=min((i-j) modN,(j-i) modN), which lies between zero and m. A fixed permutation edge from pi(i) to i is counted in e_pi(I_t) for exactly dist_N(i,pi(i)) of these intervals. Summing (7) yields

    sum_s sum_i dist_N(i,pi_s(i)) >= N m.              (8)

For r terms the mean circular edge displacement must be at least m/r. In particular, two diagonal-ended Green terms require average displacement at least (N-1)/4 over their 2N edges. Bounded local steps cannot supply this at growing lengths. Independent global orders may pass, so this is a design requirement rather than a general two-Green no-go theorem.

## 7. Remaining exact factorization and cost obligation

For two candidate invertible diagonal-ended Green terms, one can state the remaining equation without a Fourier application algorithm. Write their sparse inverses as Q0 and Q1. Then

    B=Q0^(-1)+Q1^(-1)

is equivalent to

    Q0 B Q1=Q0+Q1.                                   (9)

The identity is oriented: Q0(Q0^(-1)+Q1^(-1))Q1=Q1+Q0. Since the factors and B are invertible, Q0+Q1 is invertible, and equivalently

    A+F^(-1)=Q1(Q0+Q1)^(-1)Q0.                       (10)

Equation (10), plus the diagonal-plus-weighted-permutation support of each Q_s and all guards, is a concrete synthesis target. A dense solve for Q_s or a dense inverse of their sum at each length is not a linear-time parameter generator. If a branch has singular endpoint scalings, (9)–(10) are not a valid parametrization of that branch; the cut tests remain valid, but this particular inverse representation must not silently remove it.

Any positive result must provide uniform formulas for the weights, endpoints and cycle arrays, prove the full coefficient identity (not only the rank tests), and count O(N) preparation/application for a bounded-sum representation. The present work supplies rejection and design tests only. No admissible positive B family is claimed.

## 8. Extension by the inherited inverse-rigidity lemma

The previously reviewed Fourier-versus-row-sparse lemma says that if F^(-1)=S+E, every row of S has at most d nonzeros, and rank(E)<=r, then

    r>=floor(N/(d+1)).

For completeness, choose r+1 consecutive Fourier rows. Their sparse supports together cover at most d(r+1) columns. If N>=(d+1)(r+1), at least r+1 columns remain untouched; the Fourier submatrix there is an invertible Vandermonde matrix, whereas E has rank at most r. This contradiction proves the inequality. The proof uses the supplied splitting field and Fourier convention, not complex positivity.

Apply this existing lemma to a proposed inverse representation B^(-1)=S+E with S of row degree d. Subtract the known diagonal A. Then F^(-1)=(S-A)+E, whose sparse baseline has row degree at most d+1. Consequently

    rank(E)>=floor(N/(d+2)).                           (11)

For a product B=G_L ... G_1 with G_i^(-1)=S_i+E_i, assume S_i has row degree at most d_i and rank(E_i)<=r_i. The inverse order is G_1^(-1)...G_L^(-1). Telescoping this against S_1...S_L gives

    B^(-1)-S_1...S_L
      =sum_i G_1^(-1)...G_(i-1)^(-1) E_i S_(i+1)...S_L.

Thus the error rank is at most sum_i r_i and the baseline row degree is at most D=product_i d_i. Equation (11) yields

    sum_i r_i >= floor(N/(D+2)).                       (12)

Monomial endpoints can be absorbed into the inverse factors without increasing row support or defect rank. Arbitrary dense endpoints cannot be treated that way without a separate support certificate. Bounded degree and bounded total inverse-defect rank therefore cannot evade the pure-product gate as N grows. The bound does not apply merely because the forward factors look structured: the actual inverse decomposition and all its guards must be supplied. Discovery of low-rank factors or sparse inverse baselines is not free preparation.

This is an application of the inherited rigidity lemma to the forced chirp inverse, not a new global Fourier lower bound.

## 9. Own exact controls

The newly authored check_chirp_resolvent_gates.py checks inverse supports, all cyclic half-cut ranks, the inverse cut-rank identity, crossing-count identities, and the circular-displacement sum at odd prime and composite lengths. It includes the F521 diagonal-cancellation example and deterministic product controls with monomial endpoints. Dense arithmetic is only a finite-instance verifier. The completed run passes eight target cases, 78 full half-cut tests, 234 Green inverse/cut checks, 24 circular displacement identities, 24 monomial-ended product inverse-support controls, and eight rank-two inverse-defect telescoping controls. Counts and terminal status appear in CHIRP_B_GATE_RESULTS.json.
