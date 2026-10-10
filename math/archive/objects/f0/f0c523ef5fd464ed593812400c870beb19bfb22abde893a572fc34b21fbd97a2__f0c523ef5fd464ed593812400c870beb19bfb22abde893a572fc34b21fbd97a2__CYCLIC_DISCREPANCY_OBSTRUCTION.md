# A cyclic-window discrepancy obstruction for every three-stage layout

Research date: 9 October 2026 UTC. Independently derived from the previously audited local-annihilator rank lemma. The new ingredient is cyclic-window averaging and its connection to planar discrepancy. No uploaded program was executed.

## Result

Let F_N[i,j] = omega^(ij), with omega a primitive Nth root in a field. Suppose

F_N = S3 P2 S2 P1 S1,

where the three square stages have upper and lower quasiseparable cut ranks at most r3, r2, r1, respectively, in their individual natural stage coordinates. The internal permutations P1,P2 are completely arbitrary and may depend on N. They need not be equal, involutions, affine, or mutually inverse.

Let the permutation action on coordinate sets be the action of its permutation matrix. Define the grid discrepancy

D_grid(pi) = max_{0 <= W,t <= N} | #{i < W : pi(i) < t} - Wt/N |.

Then necessarily

D_grid(P2^{-1}) <= 2r1 + r2 + r3,
D_grid(P1)      <= r1 + r2 + 2r3.                 (A)

Here P2^{-1} denotes its map from output coordinates to middle-stage row coordinates; P1 maps input coordinates to middle-stage column coordinates. Replacing either permutation by its inverse leaves grid discrepancy unchanged, so a different consistent permutation-matrix convention does not alter either bound.

The classical two-dimensional Schmidt discrepancy theorem consequently gives an absolute c>0 such that

2r1+r2+r3 >= c log N - 2,
r1+r2+2r3 >= c log N - 2.                       (B)

In particular r1+r2+r3 = Omega(log N). There is no family of such three-stage factorizations of all growing sizes with all three orders bounded by a fixed constant. This is a representation obstruction for exactly this architecture and endpoint hypothesis. It is not an unrestricted Fourier arithmetic lower bound.

## 1. Cyclic localization costs at most two cut ranks

A cyclic interval J of width W is either an ordinary interval or the disjoint union of a prefix and a suffix. For an ordinary interval, S1[J^c,J] consists of an upper exterior block and a lower exterior block, of rank at most r1 each. For a wrapped interval, J^c is one central interval and S1[J^c,J] is the horizontal concatenation of a lower-left cut subblock and an upper-right cut subblock. Its rank is again at most 2r1.

Hence a full-column-rank right projection X from a space of dimension at least W-2r1 into the W input coordinates can be chosen so that S1[:,J]X is supported only on J. This conclusion uses rank-nullity and permits zero generators, vanishing transitions, and singular stages.

For the output prefix I={0,...,W-1}, S3[I,I^c] has rank at most r3. A full-row-rank left projection Y of rank at least W-r3 makes Y S3[I,:] supported only on I.

Thus for M=S3 P2 S2 P1 S1, R=P2^{-1}(I), C=P1(J),

rank M[I,J] <= 2r1+r3 + rank S2[R,C].           (1)

One way to verify (1) is to use rank M[I,J] <= rank(Y M[I,J] X) + (W-rank Y)+(W-rank X), then bound the compressed middle matrix by S2[R,C]. If either stated projection dimension is nonpositive, the final inequalities below are automatic because W is at most the outside budget.

## 2. A separator turns a count discrepancy into a middle rank bound

Fix a middle threshold t and write

a=|R intersect [0,t)|,   b=|C intersect [0,t)|.

If a>=b, delete the W-a rows of R at/above t and the b columns of C below t. The retained block is strictly upper-right across cut t, with rank at most r2. Restoring the deleted rows/columns increases rank by at most W-a+b. If b>=a, retain the lower-left block instead. Therefore

rank S2[R,C] <= r2 + W - |a-b|.                (2)

Equations (1)-(2) imply

rank M[I,J] <= 2r1+r3+r2+W-|a-b|.             (3)

For M=F_N, the left side is exactly W: prefix row exponents 0,...,W-1 evaluated at the W distinct nodes omega^j, j in J, form a Vandermonde matrix. This holds for any W distinct columns, including wrapped cyclic intervals, over every field with the stated primitive root. Consequently

|a-b| <= 2r1+r2+r3.                            (4)

## 3. Averaging eliminates the unknown first permutation

Keep W,t,I fixed and run J through all N cyclic intervals of length W. Each input coordinate belongs to exactly W of these intervals. Since P1 is a permutation, exactly t coordinates map into [0,t). Thus

(1/N) sum_J |P1(J) intersect [0,t)| = Wt/N.

Averaging (4), using the triangle inequality, gives

| |P2^{-1}(I) intersect [0,t)| - Wt/N | <= 2r1+r2+r3.

Taking the maximum over W,t proves the first inequality in (A). Apply the same argument to the transpose factorization, which exchanges the outside orders and inverts the internal permutation maps, to obtain the second.

The cyclic averaging step is essential. The average over only nonwrapping intervals need not equal Wt/N; using that incorrect average would leave a genuine gap.

## 4. Passage to standard planar discrepancy

For any permutation pi consider the N-point set

A_pi = {(i/N, pi(i)/N) : 0<=i<N} subset [0,1)^2.

At a grid rectangle [0,W/N) x [0,t/N), its unnormalized discrepancy is exactly the expression defining D_grid(pi).

For arbitrary real x,y in [0,1], let W=ceil(Nx), t=ceil(Ny). The point count in [0,x) x [0,y) equals the grid count with these W,t (including the equality cases). Moreover

|Wt/N-Nxy| <= 2.

It follows that the continuous unnormalized star discrepancy obeys

||D_{A_pi}||_infinity <= D_grid(pi)+2.

Schmidt's theorem says ||D_A||_infinity >= c log N for every N-point set in the square, for an absolute positive c. This proves (B). No explicit numerical cutoff is claimed from the unspecified constant.

Primary-source verification: W. M. Schmidt, “Irregularities of distribution, VII,” Acta Arithmetica 21 (1972), 45-50, DOI 10.4064/aa-21-1-45-50. The publisher's metadata was checked at https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/21/0/98185/irregularities-of-distribution-vii ; the original PDF was unavailable to this browser. The exact all-point-set formulation and unnormalized convention are also explicitly stated as equation (1.2), page 2, in the primary research paper by Bilyk, Lacey, Parissis and Vagharshakyan, https://arxiv.org/pdf/0810.5544 . This argument imports the established Schmidt theorem; it does not claim a new proof of that theorem or publication priority for the present application.

## 5. Scope, operation charges, and constructive consequence

- The result includes the complete quasiseparable family, not only the separated-generator chart. It does not divide by stage generators and therefore covers degenerate branches.
- Fourier invertibility would force all square factors to be invertible, but the localization proof does not need this fact.
- Invertible endpoint diagonals can be absorbed into the stages. Independent affine coprime-stride Fourier endpoint orders also retain the Vandermonde property after phase/root changes.
- In fact the first inequality alone permits an arbitrary input endpoint permutation, provided the output endpoint is affine with coprime stride: its prefix rows are consecutive powers evaluated at ANY distinct column nodes. The transposed second inequality permits arbitrary output endpoint permutation when the input endpoint is affine. Therefore either one affine endpoint suffices for the asymptotic fixed-order exclusion.
- Two arbitrary non-affine endpoint permutations are not covered in general: the required Fourier submatrix rank can drop at composite N. At prime N over characteristic zero, the separately established full-spark theorem would restore that rank hypothesis, but this note does not reprove full spark or assert it over arbitrary finite fields.
- The result concerns three stages, not all constant depths or general linear circuits. It does not establish a lower bound for every possible algorithm that happens to apply a matrix of growing quasiseparable order.
- In the explicitly charged separated rank-r scan executor that pays Theta(Nr) for its r scalar channels, (B) prevents an asymptotically sub-N-log-N implementation with only these three stages. General transition-generator setup, inverses, coefficient synthesis, root preparation, data motion, and all outputs must still be charged separately. A representation-rank bound by itself is not an operation lower bound for an optimized or different executor.
- Dense inverse-global factors are included only when their actual inverses/stages meet the stated quasiseparable ranks. Calling a dense matrix an inverse does not create the rank hypothesis.

Therefore simply replacing bit reversal by a different internal permutation pair cannot rescue three constant-order quasiseparable scans with the stated Fourier endpoints. A constructive continuation should change a hypothesis deliberately: investigate a fourth independently ordered stage, a different cheap global family, or a non-affine endpoint layout whose actual Fourier minors are tracked rather than presumed full rank. Raising the rank to Theta(log N) is compatible with this obstruction but does not on its own produce a faster-than-FFT charged executor.
