# Independent review of parity ranks and affine scan depth

## Result

The exact complex parity-block rank formula and the heterogeneous GF(2)-affine quasiseparable depth theorem are valid. The two uploaded variants are byte-identical, so they provide one source checkpoint, not two independent confirmations. Their common SHA256 is 187469b7ae06bb3758da7c5642c889cf44ed3ba32e7deb0249052da7b7db1c06.

All saved finite witnesses and all 250 seeded mixer trials reproduce independently. The previously rank-feasible N256 layout remains unrejected by this parity search; the separately generated N512 and N1024 layouts fail, with capacities 246<256 and 449<512.

One source-code correction is required: the uniform witness helper accepts r>1 but returns an unweighted boundary sum as its capacity. Multiply each stage boundary by r before reporting capacity and gap. The mathematical theorem is unaffected, every saved uniform witness has r=1, and the heterogeneous helper correctly applies its stage weights.

An independent simplification strengthens the endpoint scope: the all-size depth theorem needs only the universal lower bound rank(F_N[R,C])>=N/4 for balanced R,C. It therefore remains valid with arbitrary invertible monomial gates at the two external endpoints, while retaining GF(2)-affine intermediate routing. The sharper exact parity formula is useful for the finite witnesses but is not necessary for that depth proof.

These statements concern factors that are quasiseparable in their declared layouts. They do not exclude the accepted N16 384-endpoint solution or the separately constructed nonlinear eight-order hierarchy. A sum of eight differently ordered Green operators has not been shown to be one fixed-order quasiseparable stage, and arbitrary relative route permutations need not be GF(2)-affine.

## 1 Sources and imported theorem

Both direct archives are 752310 bytes and pass ZIP integrity checking. Their nested prior_checkpoint_full.zip is byte-identical to the previously reviewed moving-partition archive, SHA256 7ba6c02ad9e5d47232119d618d8971199aa262c686494144d8c8be46a14b0026. SOURCE_PROVENANCE.json records both original identities and the exact nested match. Uploaded programs are preserved as inert source material and are neither executed nor imported.

The source's exact rank proof imports the prime-power universal-sampling criterion. I verified its precise statement in Theorem 4 of Osgood, Siripuram, and Wu: residue-class counts differing by at most one at every prime-power modulus characterize universal sampling sets. Universality means the corresponding square Fourier restrictions are nonsingular for every complementary index choice of the same cardinality. Fourier symmetry transfers this row-set statement to fixed column sets. This is an attributed imported theorem, not a new proof of arbitrary Fourier full spark. [Primary paper, Theorem 4](https://arxiv.org/html/1204.0992v1#S4.SS2).

The supplied authors are credited for their parity-rank application and depth argument. No publication-priority claim is made. The review's separate Frobenius-norm route below avoids needing that imported theorem for the all-size depth obstruction.

## 2 Exact parity-block Fourier ranks

Let N=2^k with k>=2 and let a,b be nonzero k-bit masks. Columns are the parity coset C_(a,s) and rows are R_(b,t), with either parity sign s,t. Put u=msb(a), v=msb(b). Then over C,

    rank F_N[R_(b,t),C_(a,s)]
      =N/4 when u+v<=k-2,
      =N/2 when u+v>=k-1.

Here Fourier matrices use compatible primitive complex roots; either exponent orientation gives the same ranks. These are not claimed to be all-field rank formulas.

To audit the proof, set h=2^(u+1) and d=N/h. The column parity coset is periodic modulo h. Its representative set E in [0,h) has h/2 elements, precisely one from each pair e,e+h/2. Thus it is a complete residue system modulo h/2. At all smaller power-of-two moduli its residue counts are equal; at modulus h they are zero or one. Hence E is universal by the imported criterion.

Write columns as e+hj and rows as rho+d ell. The Fourier entry factors as

    omega^(rho e) omega_h^(ell e) omega_d^(rho j).

For each fixed e, an invertible length-d Fourier transform on the j columns separates the rho residues. The matrix becomes a direct sum of d blocks. Each block has columns E, a nonzero column scaling, and those ell rows admitted by the output parity condition.

If v<log_2 d, the output parity depends only on rho: d/2 blocks contain every row and the other d/2 are absent. Each present block has column rank h/2, giving N/4. Otherwise, for each rho the parity predicate on ell is nonzero, so exactly h/2 rows survive. Universality makes each square block nonsingular, giving N/2. This also proves independence of both parity signs.

There are 2^u masks of highest bit u. The number of deficient ordered nonzero mask pairs is therefore

    sum_(u+v<=k-2) 2^(u+v)=(k-2)2^(k-1)+1.

The formula is O(1) per pair in a machine-word model supporting most-significant-bit extraction. It is an oracle for this structured family of index sets, not for arbitrary Fourier submatrices. Arbitrary-precision bit work must still be charged.

## 3 Moving boundaries and the affine depth theorem

Represent each interface permutation by pi: old coordinate pi(j) enters new coordinate j. Transport membership by A_next=pi^(-1)(A). For a quasiseparable stage of upper and lower contiguous cut rank at most r,

    rank S[A^c,A]<=r d(A),

where d(A) counts membership changes along adjacent natural indices. One proof splits A^c into runs; each adjacent left/right A contribution is a submatrix of a contiguous cut block of rank at most r. There is one such contribution per boundary. Telescoping a product while moving the sets gives

    rank M[A_t^c,A_1]<=sum_j r_j d(A_j).

Neither invertible stages nor nonsingular generator charts are needed. This retains the previous moving-set theorem; it does not replace moving sets by a single common subset.

For pi(x)=Lx+b over GF(2), a parity mask pulls back by L^T, while b may flip its parity sign. The linear map on masks is invertible. If the lowest q bits of a nonzero mask vanish, membership is constant on each block of length 2^q, so d(A)<=N/2^q-1.

Choose stage quotas q_j>=1 with sum_j r_j 2^(-q_j)<=1/4. If sum_j q_j<k, imposing the low-q_j zero conditions on all transported masks gives fewer than k homogeneous binary equations in the k bits of the initial mask. A nonzero solution exists. Every stage mask stays nonzero. Its moving rank capacity is bounded by

    sum_j r_j (N 2^(-q_j)-1)
      <=N/4-sum_j r_j <N/4.

Both endpoint sets are parity halfsets, whose Fourier rank is at least N/4 by the exact formula. This contradiction proves the necessary condition

    sum_j q_j>=k.

For uniform order r, take q=ceil(log_2(4rt)) to obtain

    k<=t ceil(log_2(4rt)).

For fixed r this gives t=Omega(k/log k). It excludes every fixed t eventually, but does not by itself exclude sub-N log N algorithms: for example, a depth of order log N/log log N is not ruled out by this inequality. An arithmetic lower bound also requires a separately stated per-stage execution/charging model.

For r=1 the stated sufficient no-go thresholds reproduce: t=2 at k>=7, t=3 at k>=13, t=4 at k>=17, and t=5 at k>=26. These are sufficient thresholds, not asserted sharp.

## 4 A simpler lower bound and stronger external-endpoint scope

For any balanced subsets R,C of complex Fourier rows and columns, let A=F_N[R,C]. Every entry has modulus one, so ||A||_F^2=N^2/4. Row/column restriction cannot increase operator norm, and ||F_N||_2^2=N. Therefore

    rank(A)>=||A||_F^2/||A||_2^2>=N/4.

The normalized Fourier convention gives the same rank inequality. Diagonal scalings and permutations preserve the relevant submatrix ranks. Consequently the depth proof in section 3 works without the exact parity-rank theorem: its low-boundary nullspace witness still has balanced input and output sets.

It also permits arbitrary invertible monomial matrices at the two external endpoints. Pulling those external maps into the Fourier target turns the chosen parity halfsets into possibly non-parity balanced sets, to which this N/4 bound still applies. Only the interstage maps used to impose linear low-bit constraints must remain GF(2)-affine. This extension does not allow arbitrary nonlinear intermediate routing.

The sharp N/4-versus-N/2 oracle still matters for testing particular layouts. Replacing its value by the universal N/4 lower bound can miss some finite obstructions.

## 5 Finite witnesses and implementation correction

The legacy seeded generator uses a different random walk at every k. It is not a proved compatible infinite hierarchy. Independent regeneration of its basis images and exhaustive parity-mask optimization gives:

- N256: selected rank 128, capacity 167, no contradiction;
- N512: selected rank 256, capacity 246;
- N1024: selected rank 512, capacity 449;
- N2048: selected rank 1024, capacity 390;
- N4096: selected rank 2048, capacity 887.

The N512 mask path is 380,272,344,156 with boundaries 86,30,38,92. The N1024 path is 544,620,740,752 with boundaries 30,145,233,41. Full exact modular ranks of both selected half-blocks reproduce over both 12289 and 65537, in addition to the characteristic-zero theorem.

All five stored uniform threshold witnesses, including N=2^31, and the heterogeneous k29 witness reproduce directly from their compact basis images. The heterogeneous stage orders are 1,2,1,3, quotas 5,6,5,7, and weighted capacity 31645454. These large witnesses use binary masks and exact integers; no huge Fourier matrix is allocated or implicitly claimed to have been numerically ranked.

The source helper gf2_depth_certificate.construct_witness(k,...,r) obtains its reported capacity from an unweighted trace_witness. For r>1 that field, its per-stage capacity labels, and its gap need the rank weights. For identity routing with k=9,t=2,r=2,q=4, the valid low-bit mask 16 has boundaries 31,31: the source-style unweighted value is 62, whereas the correct rank capacity is 124. The quota argument still proves 124<128, so the mathematical guarantee survives; the numeric ledger is the problem. All saved uniform witnesses have r=1 and are unaffected. The heterogeneous helper already weights correctly. Fresh review controls include r=2 and r=3 and always report weighted capacities.

## 6 Finite-field warning and empirical scope

The source's universal-column example at N16 has columns 0,1,2,3,4,13,6,7 and rows 0,1,2,3,4,6,7,12. Its complex rank is eight because the columns are a complete residue set modulo eight. Independent specialization reproduces rank seven over 12289 and rank eight over 65537. Thus a valid Fourier root in a finite field does not guarantee that every nonzero complex determinant remains nonzero after reduction. Nonzero modular minors certify complex nonvanishing; zero modular minors do not certify complex vanishing.

This particular example concerns a general universal set, not a parity-by-parity half-block. It does not establish a finite-field failure of the specific parity formula. That formula is accepted here as a characteristic-zero statement with a primary theorem proof, not by extrapolating from its successful modular controls.

All 250 source mixer trials reproduce, including every saved example record: rejection counts are 21/50, 40/50, 49/50, 50/50, 50/50 at N256,512,1024,2048,4096. These are results for the specified elementary-row-operation random walk and a particular necessary parity-cut test. They are not probabilities for uniform random GL(k,2), arbitrary permutations, or optimized designs. Surviving the test does not supply coefficients.

## 7 Scope relative to other reviewed models

The fixed-GF(2)-affine-bank obstruction reviewed earlier chose a common bank-compatible parity subset and charged every Green occurrence. This theorem instead constrains products of quasiseparable stages with moving affine layouts and no uncharged dense internal bank. The different assumptions and quantities should not be merged without proving the required model conversion.

The accepted N16 construction has three sums of eight independently ordered Green terms and a specified block-Fourier bank, with an exact 384-endpoint coefficient solution. The present theorem neither identifies those sums as constant-order quasiseparable stages in one affine-linked layout nor excludes the finite N16 scale. It does not contradict that seed.

Likewise, the expanding hierarchical route family uses modular carries, nonlinear relative orderings, and separate channel bases. Passing the earlier common-subset incoming-edge budget remains only that necessary-capacity result. The present affine-stage no-go does not certify or exclude all separators or Fourier coefficient feasibility for the eight-order nonlinear architecture. The full recursive coefficient and cost question remains separate.

## 8 Independent controls and seal

The fresh checker executes only review-authored Python and the standard library. It verifies:

- 12124 full parity-submatrix ranks over two fields, exhaustive through N64 for the basic parity signs and all four signs through N16;
- exact deficient-pair counts through N64;
- 2046 residue-balanced representative sets through ambient size 1024;
- the bad-prime universal-set example;
- all five legacy-seed and all five uniform-depth records, plus the heterogeneous record;
- four full N512/N1024 modular rank corroborations;
- all 250 seeded mixer trials and seven independently synthesized weighted nullspace witnesses.

Run `python3 independent_checks.py`. It reads only the two source JSON records and imports only exact_utils.py. PORTABLE_REPLAY.json records isolated replay and byte-identical VERIFIED_RESULTS.json. The original source programs are kept inert. The proof relies on the clearly attributed sampling theorem only where indicated; the simpler all-size depth proof is also supplied independently.
