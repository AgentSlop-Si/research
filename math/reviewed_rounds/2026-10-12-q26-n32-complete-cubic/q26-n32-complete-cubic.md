# Fixed N=32 seven-Green family: complete cross-prime cubic exclusion

12 October 2026. Independent outcome: **ACCEPT_BOUNDED**.

For the exact seven-Green family defined below, no two invertible complex diagonal masks, two internal permutations, or nonzero homogeneous three-component pencil parameter can make the circuit equal to the unnormalized 32-point Fourier matrix. The result follows from an exhaustive cross-prime cover of all 856,135,680 induced mappings in each of the two fields.

Each prime has 856,135,679 rank-10 mappings and **one genuine rank-9 exception**. The two exceptional mappings are different. A concrete nonzero 10-by-10 minor in the other prime covers each one, and valid cyclotomic specialization proves the fixed characteristic-zero exclusion. Universal rank 10 in each individual prime is false.

This is the complete proof-documentation derivative of the accepted independent review, supplemented with the exact source convention, quotient scaling, numerical guards, exceptions, recorded full replay and bounded cold replay. It retains every substantive section of the independent proof. Evidence filenames in that proof identify members of the hash-bound accepted packet; they are not links to files distributed in this documentation collection. The sealed computational archives and original programs are not republished here. Consequently this collection is complete proof documentation, rather than a standalone executable replay distribution.

## 1. Exact source model and conventions

Let zeta=exp(2*pi*i/32), so the scalar imaginary unit is i=zeta^8. Indices range from 0 to 31. The target has entries F[j,k]=zeta^(j*k), with no normalization factor and positive exponent.

For each ordered cycle s below, define W_s e_(order[t])=e_(order[(t+1) mod 32]). Write pos_s(j) for the position of j in that list. Fix

    alpha_0=(1+i)/4, alpha_1=(2+i)/7, alpha_2=(1+2i)/8,
    alpha_3=(1-i)/5, alpha_4=(2+i)/9, alpha_5=(1+i)/6,
    alpha_6=(1+3i)/11.

The resolvents and outer operators are

    G_s=(I-alpha_s W_s)^(-1),
    G_s[j,k]=alpha_s^((pos_s(j)-pos_s(k)) mod 32)/(1-alpha_s^32),
    A=G_0+((1+i)/3) G_1,
    C=G_4+((1-i)/4) G_5,
    B(x)=x_0 G_2+x_1 G_3+x_2 G_6,
    T=A^(-1) F C^(-1).

The excluded equality is F=A D_1 P_1 B(x) P_2 D_2 C, where D_1,D_2 are arbitrary invertible complex diagonal matrices, P_1,P_2 are arbitrary 32-by-32 permutation matrices, and x is any nonzero triple in C^3. This includes x=(1,lambda,mu) for every finite complex pair (lambda,mu), and also the homogenized boundary x_0=0. All seven internal resolvent couplings and all cycles remain fixed.

The seven explicit directed cycles are:

- G_0: 0,24,15,26,28,17,8,10,5,6,29,7,13,22,20,12,30,18,27,1,16,2,14,4,31,11,9,3,25,19,23,21
- G_1: 0,15,6,24,20,25,29,26,8,16,18,1,7,27,4,3,12,21,30,13,23,5,2,31,17,22,9,11,14,10,28,19
- G_2: 0,5,4,25,15,11,12,9,31,20,14,8,7,29,26,24,21,18,10,22,2,23,19,27,6,3,17,16,28,1,30,13
- G_3: 0,4,20,26,22,18,7,13,8,21,28,12,29,24,16,14,30,19,2,27,9,1,23,31,11,15,6,25,10,5,17,3
- G_4: 0,11,21,17,30,27,1,26,16,15,4,3,9,8,28,25,18,19,24,22,5,20,14,29,12,23,10,2,6,7,31,13
- G_5: 0,9,30,25,3,23,4,14,5,17,13,26,10,22,15,31,18,21,29,7,19,11,6,2,8,20,27,1,16,12,28,24
- G_6: 0,29,7,6,13,16,31,28,3,15,24,5,4,20,17,23,26,8,21,19,18,27,22,9,14,25,1,11,10,2,30,12

Quadratic monomial order:

    x0^2, x0*x1, x0*x2, x1^2, x1*x2, x2^2.

Cubic monomial order:

    x0^3, x0^2*x1, x0^2*x2, x0*x1^2, x0*x1*x2,
    x0*x2^2, x1^3, x1^2*x2, x1*x2^2, x2^3.

K3 has twelve rows: the x0,x1,x2 multiples of q01, then q02, then q03, then q12, with the four quadratics defined in the proof below. All row and column indices are zero-based mathematical indices.

## 2. Complete independent proof

The following proof reproduces all substantive sections of the accepted independent proof document. Its introductory status sentence is updated to reflect the completed exhaustive premises recorded in the final verdict; its mathematical argument is unchanged.

### Independent N=32 cubic certificate obligations

Scope: the exact fixed seven-Green family of the supplied Phase 39 theorem,
N=32, the homogeneous three-component pencil, and K3 from column pairs
(0,1), (0,2), (0,3), (1,2). This proof establishes the enumeration and Schur-complement certificate
scheme. Its exhaustive numerical premises are completed by the final verdict
and the independent full-run records summarized in Section 5 below.

### Source binding and reconstruction

The theorem SHA-256 is
dfad32c3ce3aadcdf04e535aee662de005cc274e25ad718133d9975f23de6908.
INPUT_GUARDS.json gives the two independently reconstructed instance hashes,
field roots, seven Green denominators and the two outer determinants.
SOURCE_BINDINGS.json binds the original archive and inert source members.
No historical or candidate source was imported or executed. The independent
program rebuild_and_check.py reads the mathematical cycle convention from
the original definitions and constructs each Green matrix by its closed
geometric formula, checking it against inversion of I-alpha W. It checks
both inverse directions, reconstructs A^-1 F C^-1, and obtains exact byte
equality with both supplied instance files. The seven explicit orders are
frozen in CYCLES_N32.json.

### Why every permutation is covered

For any pair of 32-by-32 permutation matrices, there are bijections rho and
kappa such that (P1 B P2)[j,k]=B[rho(j),kappa(k)]. Hence rows 0,1 and columns
0,1,2,3 induce an ordered pair r0!=r1 and an ordered four-tuple of distinct
columns c0,c1,c2,c3. Conversely, each such partial injection extends to a
permutation: independently biject the remaining 30 row labels and 28
column labels. Thus the induced mapping set is exactly the Cartesian
product of these two sets of ordered injections.

Its size is 32*31*32*31*30*29 = 856135680. Grouping by the row pair and first
three columns produces 32*31*32*31*30 = 29521920 groups, each with exactly
29 remaining column choices. No symmetry reduction is used. A group-level
elimination reused for the final 29 choices reduces arithmetic, not coverage.
There are 992 row-pair blocks with 863040 mappings each.

A canonical zero-based mapping index is obtained by mixed-radix digits
(r0, r1-[r0<r1], c0, c1-[c0<c1],
 c2-[c0<c2]-[c1<c2],
 c3-[c0<c3]-[c1<c3]-[c2<c3])
with radices (32,31,32,31,30,29). This is a bijection onto integers from
0 through 856135679: each compressed digit unpacks uniquely by selecting
the specified position in the sorted set of still-available labels.
An exhaustive ledger must reconcile these ranges without gaps or duplicates.
Merely reporting the correct total, or a digest of sampled mappings, is
not such a reconciliation.

### The necessary equations use no division by pencil entries

Write T[j,k]=d[j]*B[rho(j),kappa(k)]*e[k], with d[j],e[k] nonzero. Multiplying
two such equalities crosswise shows that every q_ab from the source theorem
vanishes at x=(1,lambda,mu). This implication is polynomial, including when
some B entries vanish. Testing all nonzero homogeneous x is stronger than
testing only x0=1. If K3 has rank10, its row span contains all degree-three
monomials. A nonzero common projective root would have x_i!=0 for some i,
contradicting that the cubic x_i^3 is in the vanishing span.

### Exact triangle/quotient factorization

For each mapped column a define the linear forms
U_a=T[1,a]*B[r0,c_a] and V_a=T[0,a]*B[r1,c_a]. Then
q_ab=V_a U_b-V_b U_a. For columns 0,1,2 there are the two polynomial
identities

U_0 q_12-U_1 q_02+U_2 q_01=0,
V_0 q_12-V_1 q_02+V_2 q_01=0.

They are two relations among the nine linear multiples of the three
triangle quadrics. If their two coefficient vectors are linearly dependent
over the ground field, the triples of forms U and V are proportional over
that field (or one is zero); then all three triangle quadrics are zero.
Otherwise the two relations are independent. Consequently the triangle
matrix H has rank at most7 in every case. Adding the three multiples of
q_03 gives rank(K3)<=rank(H)+3, so rank(H)=7 is necessary for rank(K3)=10.

When rank(H)=7, select seven original rows R and seven pivot columns C
forming an invertible 7-by-7 matrix A=H[R,C]. Let D be the remaining three
monomial columns, Q=H[R,D], and L the three coefficient rows of x_i*q_03.
The exact residual matrix is S=L[:,D]-L[:,C]*A^-1*Q. The ten original rows
consisting of R followed by the three q_03 rows have, after ordering columns
C then D, block matrix [[A,Q],[L[:,C],L[:,D]]]. Therefore

det(this ordered 10-by-10 matrix)=det(A)*det(S).

Changing back to source monomial or row order contributes only a recorded
sign. Thus nonzero det(A) and det(S) are an actual rank10 minor witness in
the original source-exact K3. They are not a surrogate numerical statistic.
Conversely, rank(K3)=7+rank(S), since the other triangle rows lie in the
selected seven-row span. This proves the factorized check is exactly
equivalent to full cubic rank, including all deficiencies.

To replay a witness independently, reconstruct the original K3 from the
source matrices, select R plus the three q_03 rows, and evaluate its
10-by-10 determinant by a different elimination routine. A zero residual
is not a Fourier witness. It can be checked in the other prime or in
characteristic zero; failing the cubic sufficient test does not prove a
factorization, nor does it exclude one.

### Characteristic-zero specialization

Fix K=Q(zeta), where zeta is the primitive complex 32nd root specified by
the positive-exponent Fourier convention, and i=zeta^8. Every matrix
coefficient lies in K. Begin with Z[zeta], invert the integer coupling and
outer-weight denominators 3,4,5,6,7,8,9,11, invert the seven 1-alpha_s^32,
and invert det(A),det(C). The resulting subring R of K contains the full
source matrices and every K3 entry by the adjugate inverse formula.

For either recorded prime p, the independently checked element z_p has
exact order32 and satisfies z_p^16+1=0, the defining cyclotomic relation.
Sending zeta to z_p thus defines a ring map Z[zeta] to F_p. The recorded
i_p=z_p^8 agrees with the Gaussian coupling convention. Every denominator
listed above maps to a nonzero element by INPUT_GUARDS.json, so the map
extends to R and its matrix specialization is exactly the supplied input.

If any selected 10-by-10 minor specializes to a nonzero field element,
the characteristic-zero determinant was nonzero: ring maps send zero to
zero. Its K3 has rank10 over K and over C, so no nonzero common projective
root exists over C. The row/column selector may differ for each mapping,
and the successful prime may also differ for each mapping, without
weakening this implication. In particular, exhaustive enumeration in both
primes together with disjoint sets of deficient mappings is a complete
cover equivalent for the characteristic-zero exclusion purpose. It is
not a statement of full rank in each individual prime. Each such
exception can be supplied with a concrete nonzero minor in the other
prime. A nonzero modular minor proves nonzero characteristic-zero rank;
a zero modular minor or deficient modular K3 is inconclusive.

### Acceptance boundary

The guards and the proof above are independently established. The local
controls include a planted common root of rank9 in both primes, an anchored
rank9 control, a zero target of rank0, and fresh sampled direct rank10
minor witnesses. These controls do not replace exhaustive coverage.

A bounded acceptance requires completed full-range ledgers, all exceptional
mappings accounted for, source-bound group/minor witness replay, and
independent enumeration/checker validation. Those obligations are now met:
VERDICT.json records 856135680 independently replayed mappings per prime,
all 1984 block streams matching the author, and the two disjoint rank9
exceptions repaired with explicit other-prime rank10 minors. The actual
minor determinant streams are also computed afresh. Thus the N=32 cubic
characteristic-zero gate closes by a complete cross-prime cover. Nothing
here closes N=64, all N, quartic K4, a production transform, or a
complexity/priority claim. Full rank at every mapping in each individual
prime is explicitly false.


## 3. Exact quotient scale and original-matrix minor

The accepted independent proof gives the general Schur-complement argument. The following source-exact details identify the scaled witness actually compared in all completed blocks.

Select K3 rows R=(0,1,2,3,4,5,9). Split that seven-by-ten matrix into [A7 Q], where A7 consists of monomial columns 0 through 6 and Q consists of the remaining three columns. Let L be K3 rows (6,7,8), the three q03 multiples. The author uses division-free elimination and scaled backward substitution. The resulting ten-by-three kernel matrix is

    K=[-d A7^(-1) Q ; d I3],

where d is the product of the seven nonzero division-free pivot values. In particular, d is a scale factor and is **not** generally det(A7). The exact checks are [A7 Q]K=0 and the lower block K[7:10,:]=d I3. With delta=det(LK), the block determinant identity yields

    delta=d^3 det(M)/det(A7),
    M=K3[(0,1,2,3,4,5,9,6,7,8), all ten monomial columns].

Thus delta is nonzero if and only if this original ten-row minor is nonzero, on the checked invertible leading block. The grouping by the first three middle columns reuses A7,Q and d for all 29 remaining fourth-column choices; each of those 29 choices is still evaluated individually.

The independent verifier uses normalized Gaussian elimination with batch inversion over all 29,760 first-three-column choices in each ordered-row-pair block. It forms the unscaled Schur complement, tracks pivot-swap signs, and computes actual det(M) values afresh. It also recovers the author's division-free scale by the normalized-pivot recurrence d <- d^2 * pivot, starting from d=1. This permits exact comparison of every scaled residual word while separately recording actual original-minor streams.

Whenever the leading minor or the residual determinant vanishes, full twelve-by-ten modular elimination decides the actual rank. The completed runs have no rank-10 fallback mappings and no failed-kernel triples. Their only deficient mappings are the two rank-9 cases documented below. No deficiency is silently converted to a rank-10 witness.

Every stream word is an unsigned 32-bit little-endian integer. A genuine deficient mapping retains a zero word. The product and SHA-256 of each stream bind the complete ordered block; a digest alone is not a proof that a computation occurred. Here the bound exact inputs, complete loops, independent normalized checker, complete author/independent stream reconciliation, and direct minor replay collectively supply the computational evidence.

## 4. Source and reduction guards

The original source archive has SHA-256 8f90f6e5fc21fdaffa02fc6bd66cc2a4fb96d53d3efb360ec7443cba305002d4. The source theorem has SHA-256 dfad32c3ce3aadcdf04e535aee662de005cc274e25ad718133d9975f23de6908. The frozen mathematical-definition texts have these SHA-256 identities:

- phase37_curvature.py: 1ec5b193a5bb32639fbcd1079740219514851ebca8a3ce2bd38c86da3b3d2e5d
- phase38_joint_masks.py: 76831de46788aa2388ded69c7ca17f38a89c5191fca989cdbff22953e69a5b87
- phase39_bivariate.py: 3054524a0ee6589c21ca91255d0d8ff9ae89d7471139b3839512a8ca74852ac6

These hashes identify source provenance; their programs were read only as inert text during the independent review and are not included in this collection.

### Field p=998244353

- p-1=2^23 * 7^1 * 17^1; primitive generator g=3
- z_p=g^((p-1)/32)=452798380; i_p=z_p^8=911660635
- z_p^32=1, z_p^16=-1, i_p^2=-1; exact order 32 is checked
- Reduced alpha_0 through alpha_6: 227915159, 272843570, 352695703, 416614485, 434043744, 484691557, 430133692
- Green denominators 1-alpha_s^32: 249557549, 230734618, 452422754, 522387065, 585700600, 426465659, 260127399
- det(A)=962618726; det(C)=364690165; all are nonzero
- Source-exact serialized (T,G2,G3,G6) SHA-256: 4059d6bb807aabe64ce54312a25f4264f947f2b724f1e0901cde84c62cc993da

### Field p=2013265921

- p-1=2^27 * 3^1 * 5^1; primitive generator g=31
- z_p=g^((p-1)/32)=760005850; i_p=z_p^8=1728404513
- z_p^32=1, z_p^16=-1, i_p^2=-1; exact order 32 is checked
- Reduced alpha_0 through alpha_6: 1438734089, 534524348, 1690392329, 459625466, 639437373, 288067419, 1020455573
- Green denominators 1-alpha_s^32: 2013251522, 323817585, 1995741379, 1846272313, 817372966, 470609768, 205949800
- det(A)=440369554; det(C)=15719915; all are nonzero
- Source-exact serialized (T,G2,G3,G6) SHA-256: 3e201d74d44a29166f4656604b38c3874af2750b81750772aecff18c04ae995a

For each field, the independent reconstruction checks the primality and primitive-generator factors, every rational denominator, all seven cycle permutations and Green denominator guards, the resolvent inverse identities in both multiplication orders, both outer inverse directions, A T C=F, and the positive-exponent Fourier/Weyl identities. The independently regenerated instance is byte-identical to its pinned source file. All entries of T are nonzero in both recorded fields. These checks establish valid specialization; a zero determinant in one reduction remains inconclusive about characteristic zero.

## 5. Completed exhaustive replay and two real exceptions

Both independent full runs completed before the accepted packet was sealed. Each covers the row-pair range [0,992), hence every mapping index in [0,856135680). All 992 blocks in each prime contain exactly 863,040 distinct mappings. There are 29,521,920 first-three-column groups per prime, each completed with its 29 remaining fourth-column choices.

### Completed field p=998244353

- Independently replayed mappings: 856,135,680
- Rank 10: 856,135,679; rank 9: 1; other ranks: zero
- All 992 author scaled-word streams match the independently computed streams
- Actual original-minor determinant streams are separately computed afresh
- Independent full-run time: 135.537 seconds
- Independent ledger SHA-256: ab3d9935cfe5a123ac55cfbaf3f8e38afbc372b098bd56d1de63b1f756128581
- Author ledger SHA-256: f00479c75d26940b44dee1e37e7e8683d57c6415b950a02e7bc73092890e48dd

### Completed field p=2013265921

- Independently replayed mappings: 856,135,680
- Rank 10: 856,135,679; rank 9: 1; other ranks: zero
- All 992 author scaled-word streams match the independently computed streams
- Actual original-minor determinant streams are separately computed afresh
- Independent full-run time: 178.057 seconds
- Independent ledger SHA-256: 330e2164b84127f66a809215308c9e0044fc0d3689cd6587805a28eb5bc02441
- Author ledger SHA-256: b348c421781f2c70f53df5f05465b13a31a19d8062f105fcb31f0f0321b71725

The accepted verifier was compiled with g++ (Debian 14.2.0-19) 14.2.0, using -O3 -std=c++17 -Wall -Wextra and libcrypto. Both complete runs exited with status zero. These are verification timings on the recorded environment, not production Fourier timings or a portable performance guarantee.

### Exception at p=998244353

The ordered middle rows are (15,2) and the ordered middle columns are (18,11,5,3), in row-pair block 467. Direct elimination gives rank 9 in p=998244353. Rows (0,1,2,3,4,5,6,7,9) and columns (0,1,2,3,4,5,6,7,8) give a nonzero nine-by-nine minor 66137296 in that field.

At exactly the same mapping in p=2013265921, direct elimination gives rank 10. Original K3 rows (0,1,2,3,4,5,6,7,8,9), with all ten columns, have determinant **307619848**, which is nonzero. This is the alternate-prime characteristic-zero witness.

### Exception at p=2013265921

The ordered middle rows are (20,7) and the ordered middle columns are (20,18,1,2), in row-pair block 627. Direct elimination gives rank 9 in p=2013265921. Rows (0,1,2,3,4,5,6,7,9) and columns (0,1,2,3,4,5,6,7,8) give a nonzero nine-by-nine minor 1459616786 in that field.

At exactly the same mapping in p=998244353, direct elimination gives rank 10. Original K3 rows (0,1,2,3,4,5,6,7,8,9), with all ten columns, have determinant **862908258**, which is nonzero. This is the other alternate-prime characteristic-zero witness.

The two deficiency sets have empty intersection. Assign p=998244353 to every mapping except its one exception and p=2013265921 to that exception. Every mapped K3 then has a nonzero characteristic-zero ten-by-ten minor. Repeating the argument in Section 2 excludes every proposed masked/permuted homogeneous factorization. Neither modular rank-9 case is a Fourier construction or a characteristic-zero counterexample.

### Separate direct witness replay

The first mapping in each of the 992 complete blocks in both primes supplies 1,984 recorded original-matrix rank-10 minors. Separate Python inverse/determinant arithmetic reconstructs K3 directly and checks each actual determinant, leading seven-by-seven determinant, scale d, kernel identity and exact residual-scaling identity. The accepted direct-witness record has SHA-256 16021da328fa43de727c90153318a71185394f5c2ccdcbca47dca5cd7add728e. The exceptional rank/minor record has SHA-256 b2fdf63d3aeb25f7baee9d83140dfb61ebf1e20cd03a0baecece9f6460607e16.

This targeted replay is additional to the full independent mapping scan. It is not substituted for the exhaustive premise.

## 6. Adverse controls and replay boundaries

The independently rebuilt controls in each field include:

- A planted masked/permuted factorization with common projective root (1:7:11), yielding rank 9. Its cubic evaluation vector is explicitly killed by the matrix, so the checker must not declare it impossible.
- The anchored-only star q01,q02,q03, yielding rank 9. The two linear anchor-entry forms have a common nonzero homogeneous zero; this is a spurious test root rather than a valid Fourier parameter.
- A zero target yielding rank 0.
- 130 direct full-rank sampled minor witnesses per prime, including two fixed boundary selections and 128 additional deterministic selections. These are explicitly sampled controls, not exhaustive certificates.
- Four rejected ledger corruptions: a missing block, a duplicated row-pair index, an altered determinant digest, and an altered mapping count.

The author-side controls separately compare 1,024 dispersed mappings per prime with direct twelve-by-ten elimination and check kernel invariants. Its first entire ordered-row-pair block in the first prime also receives 863,040 direct-rank cross-checks. These checks are separate from the independent complete enumeration.

The accepted seal records a fresh cold manifest verification, source reconstruction and adverse controls, all 1,984 direct witnesses, complete ledger reconciliation, and a fresh compile followed by one complete row-pair pilot in each prime. The **full independent exhaustive runs occurred before sealing**; the cold stage is not represented as another full exhaustive run.

During preparation of this publication derivative, newly authored local checking code rechecked the accepted archive's member integrity and both complete recorded block ledgers. It independently rebuilt both field instances byte-identically, recomputed all 1,984 direct first-mapping minors and their kernel/scaling identities, and checked all four exceptional rank/minor cases. It did not rerun the 856,135,680-mapping scans. No archived program was imported or executed during publication preparation. These preparation checks supplement, rather than relabel, the accepted independent replay.

## 7. Scope, costs and unproved extensions

The conclusion is for the exact fixed N=32 seven-Green family, arbitrary two invertible complex diagonal masks and two internal permutations, and the full nonzero homogeneous three-component pencil. The proof uses the cubic K3 certificate with pairs 01,02,03,12. It does not certify the N=32 quartic K4 test. N=64 and larger exhaustive certificates, any uniform all-N exclusion, independently varied cycle orders or resolvent couplings, four middle components, and additional noncommuting stages remain outside this result.

For supplied coefficients, cycles, masks and permutations, applying the candidate circuit uses seven cyclic Green recurrences, two diagonal passes and two permutation passes, with O(N) field arithmetic per vector and linear fixed-data preprocessing. This particular fixed candidate does not compute the Fourier transform under any of the permitted choices. Dense construction of T=A^(-1) F C^(-1) uses an O(N^3) reference procedure; exhaustive mapping enumeration has O(N^6) fixed-size field tests. Neither operation supplies a successful online Fourier algorithm. Exact finite-field arithmetic costs do not establish arbitrary-precision integer bit complexity, accuracy, coefficient-generation cost, memory traffic or a production speedup.

No production Fourier construction, asymptotic Fourier breakthrough, novelty claim or historical priority conclusion is made. Earlier accepted results at other sizes are not reclassified here.

## 8. Immutable provenance and publication boundary

- Accepted review archive: 645,473 bytes; SHA-256 f8ade45c0faeb68ab8984846193b3603f7a09ece83760368a569223873fdb565
- Reviewed candidate archive: 273,155 bytes; SHA-256 e523fd470bf2ff8711494ec992d65a6c91b76dd607508bb3fad088b559051407
- Accepted independent proof source: SHA-256 8c9ba6a07e0dd347c2aeb81d8859387f3745350e1aa92ca7f18fc69deab2d401
- Candidate proof source: SHA-256 3f2d02fba5b1470dac8b6940adbbca7386226a1510935a01aaee98905c3f5d9c
- Final independent verdict: SHA-256 44621965264ca3e35b96b23243df41a0fa8dcafab94d7bcaada23f9f38b352c2

The originals remain unchanged. This publication contains the complete proof-documentation derivative, a README, a minimal verification record and a file manifest. Private operational references, original executable source, complete archives and third-party full papers are outside the publication payload. Hashes bind the reported sources without granting access to omitted material.
