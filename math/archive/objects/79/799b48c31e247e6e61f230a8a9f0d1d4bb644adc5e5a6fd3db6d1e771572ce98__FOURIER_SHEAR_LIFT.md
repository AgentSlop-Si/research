# Exact Fourier coefficient gate for full-coverage Green shears

## Result

Full cross-rank is insufficient in two distinct, precisely stated ways.

1. In the natural half-shift sectors, all four blocks of the full Fourier matrix have rank N/4 for N divisible by four. Invertible sector-preserving normalizations cannot change these ranks. They cannot make the lower-right block the identity or match a full-rank two-shear correction.
2. After paying the even/odd output permutation, the rank obstruction disappears, but a stronger coefficient invariant remains. Any external block-diagonal normalization of the two-shear product must satisfy **AB = -I/2**. The original full-coverage same-kernel family fails this for every legal pole at every N divisible by four with N >= 8. This holds even if those external block normalizations are arbitrary invertible matrices, rather than only inexpensive ones.

There is a constructive minimal escape in this second, specified architecture: keep A=C and replace the reverse kernel by **B=-C^{-1}/2**. The required inverse is a sparse two-shift operator. Explicitly paid normalizations then give the entire Fourier matrix, for every input, with two independent half-size Fourier calls. The resulting recurrence is Theta(N log N), not a new sub-N-log-N FFT. A chirp-convolution extension covers every positive integer size, also at O(N log N).

No impossibility is claimed for arbitrary interleaved non-sector-preserving diagonals, permutations, or Green layers, or for a variable unrelated prefix. Those are outside the invariant's scope and still require their own coefficient identities.

## 1. Source, convention, and scope

The reviewed source is:

- research_round_0101/review_paid_bidirectional_shears/INDEPENDENT_REVIEW.md
- research_round_2156/construct_expanding_cycle_orders/bidirectional_shear_milestone.zip
- Archive SHA256: 44b6f626933e70c78959e4a3bdd85feb52b173d50de6855bf1577726a5cf7f06

Source programs were read as inert text, never executed or imported. All controls in this directory were newly authored with standard-library exact arithmetic.

Use the unnormalized forward transform F_N[r,j]=omega_N^(r j), omega_N=exp(2 pi i/N). Write N=2n, X e_j=e_(j+n mod N), and

    E = [[I,I],[I,-I]],     E^{-1}=E/2.

E's columns give plus-first X-sector coordinates. Work in characteristic zero, or a field of characteristic different from two containing the specified roots and nonvanishing denominators.

The audited full-coverage construction uses a Hamiltonian P with P^n=X, n even, and the second Hamiltonian route XP. On minus, T=P|_- is a signed n-cycle, T^n=-I. For t != 0 and t^(2n) != 1,

    C = (I-tT)^{-1} - (I+tT)^{-1}
      = 2t T (I-t^2 T^2)^{-1}.

The original two odd masks give

    A=diag(a) C,       B=C diag(b),
    S=U(A)L(B)=[[I+AB,A],[B,I]].

A transpose reverse instead has B=C^T diag(b). All these statements concern actual coefficients, not just ranks.

## 2. Natural-sector rank obstruction

For signs a,b in {+1,-1}, the block from input sector b to output sector a is

    (E^{-1} F_N E)_{a,b}[i,j]
      = (omega_N^(ij)/2) (1+a(-1)^j)(1+b(-1)^i),

when n is even. Thus only n/2 rows and n/2 columns can be nonzero. On those rows and columns the matrix is a nonzero diagonal scaling of F_(n/2), with primitive root omega_N^4. Its rank is exactly n/2.

Consequently each of the four sector blocks has rank n/2, while S_--=I has rank n. Multiplication on either side by invertible block-diagonal matrices preserves the rank of each block. In particular this obstruction survives any combination of:

- invertible diagonals commuting with X (the two entries of each sheet pair agree);
- permutations commuting with X;
- guarded Green operators on routes commuting with X;
- arbitrary invertible products of these operators.

It does not cover an arbitrary physical diagonal that mixes the sectors, or a permutation that changes their pairing. One of the latter is the escape in the next section. Adding a correction to the obstructed lower-right block would require rank at least n/2; this is only a necessary rank bound, not a coefficient solution.

For a fixed prefix C0, the relevant target remains W=F_N C0^{-1}. The statements here apply directly when C0 and any additional external factors preserve these sectors. They do not assert the same ranks for an arbitrary C0.

## 3. Paid parity permutation and coefficient invariant

Let Q reorder the physical outputs as even indices first, then odd indices, and let D=diag(omega_N^j), 0 <= j < n. The exact identity is

    W := E^{-1} Q F_N E
       = [[F_n, F_n D],[F_n,-F_n D]]
       = H diag(F_n,F_n D),

    H = [[I,I],[I,-I]].

Q is a paid N-word permutation. E and E^{-1} are paid pairwise additions and scalings. All four blocks of W are now invertible.

For any block matrix M with the indicated inverse blocks, define

    R(M)=M_++ M_-+^{-1} M_-- M_+-^{-1}.

Under arbitrary invertible block-diagonal left and right multiplication, R changes only by conjugation with the plus left block. Direct substitution gives

    R(W)=-I,
    R(S)=I+(AB)^{-1}.

Therefore W can be externally block-diagonally equivalent to S only if

    AB=-I/2.

Conversely, this is sufficient for an invertible A and B: the explicit construction in Section 5 supplies the equivalence. Thus this is a complete coefficient test for the stated normalized two-shear problem. A determinant-one condition or two full cross-ranks does not substitute for it.

## 4. Original kernel fails the invariant

Since C is invertible,

    C^{-1}=(T^{-1}-t^2 T)/(2t),
    C^{-2}=(T^{-2}-2t^2 I+t^4 T^2)/(4t^2).

If AB=-I/2 for A=diag(a)C and B=Cdiag(b), both masks must be everywhere nonzero, and C^2 must be diagonal. Then its inverse C^{-2} would also be diagonal.

- If even n >= 6, the permutations underlying T^2 and T^{-2} have distinct, off-diagonal supports. Their nonzero coefficients cannot cancel.
- If n=4, T^{-2}=-T^2. The off-diagonal coefficient is (t^4-1)/(4t^2). Vanishing would force t^8=1, excluded by the original N=8 Green guard.
- If n=2, both squared shifts are diagonal, and this particular obstruction is absent.

Thus the same-kernel two-shear family cannot pass the coefficient invariant at any even n>=4, regardless of mask choices or arbitrary external block-diagonal normalizations. This is a uniform complex-field proof, not a conclusion extrapolated from modular examples.

For the ordinary-transpose alternative,

    (CC^T)^{-1}=[(1+t^4)I-t^2(T^2+T^{-2})]/(4t^2).

This is non-diagonal for even n>=6, so transpose reversal also fails there. There are genuine small exceptions: n=2 and n=4 have CC^T scalar. At n=4, T^{-2}=-T^2 makes their sum vanish. In the dyadic sequence the transpose obstruction starts at N=16; the same-kernel obstruction starts at N=8. Complex transpose here is not a Hermitian adjoint.

## 5. Minimal inverse-kernel escape

Within this externally block-diagonally normalized two-shear architecture, fixing the forward block A determines the reverse block uniquely:

    B=-A^{-1}/2.

For A=C, it can be implemented by the explicit sparse formula above. In physical coordinates, if Phi=G_P(t)-G_XP(t) and Pi_-=(I-X)/2, put

    J=Pi_- (P^{-1}-t^2 P) Pi_-/(2t).

Then Phi J=J Phi=Pi_-. With the source's odd character D0=diag(I,-I), the reverse mixer -J D0/2 has sector block B=-C^{-1}/2 and still squares to zero. This changes the reverse primitive openly: two signed route shifts and their scalar combination replace the original same-kernel reverse. P^{-1} is a separately declared inverse order, constructible in O(N) time and words; it is not silently assumed to belong to the original bank.

Define

    S*=U(C)L(-C^{-1}/2)
      = [[I/2,C],[-C^{-1}/2,I]],
    Lambda=diag(I,-C),
    Gamma=diag(2I,C^{-1}).

Multiplication verifies entrywise

    Lambda S* Gamma = H,
    E^{-1} Q F_N E = Lambda S* Gamma diag(F_n,F_n D),
    F_N = Q^{-1} E Lambda S* Gamma diag(F_n,F_n D) E^{-1}.

Both external normalizations are charged. C occurs twice, once in the forward shear and once in Lambda. C^{-1} also occurs twice, once in Gamma and once in the reverse shear. There is no free recurrence closure or reuse of one recursive output for two arbitrary input vectors.

One may retain an original C-based reverse and compose with the explicitly sparse C^{-2} normalization, but it algebraically reduces to this inverse-kernel reverse. The word “minimal” refers only to the forced single reverse-block replacement with A fixed in this architecture, not a global minimal arithmetic circuit theorem.

## 6. Explicit application ledger and dyadic recurrence

Take the legal fixed pole t=1/2 at every dyadic size N>=4. Use the canonical signed cycle T with one negative wrap edge. A signed-cycle Green (I-tT)^{-1} can be applied by two n-step affine recurrences and one multiplication by a precomputed inverse wrap denominator 1/(1+t^n). This costs at most 4n+1 scalar field operations. The (-t) Green is analogous for even n.

The signed-sector scan is an explicit executor optimization, not an assertion that a source length-N Green is a free n-scan. Without it, each application of C can instead use two original length-N Green applications plus paid sector embedding/projection; the resulting recurrence is still 2 A(N/2)+4 G(N)+O(N).

Using the signed executor, with additions/subtractions and multiplications each counted as one field operation:

- C costs 2(4n+1)+n = 9n+2 operations, including its Green difference.
- C^{-1}, or -C^{-1}/2 with scalars absorbed, costs 3n operations and two signed permutation passes.
- E^{-1} costs 4n operations, including its half scalings.
- D costs n operations.
- The two recursive F_n calls are separately charged.
- Gamma's plus scaling costs n operations.
- The two shear residual additions cost 2n operations.
- E costs 2n operations.
- The minus sign in Lambda can be absorbed by reversing the Green difference.
- Q^{-1} costs N output placements; the two C^{-1} calls cost four n-word signed permutation passes. The Green scans' own route traversals are additionally included in their executor work.

Total, before optional cancellation:

    A(2)=2,
    A(N) <= 2 A(N/2)+17N+4,          N=4,8,16,...,
    A(N) <= 17N log2(N)-14N-4. 

For example, the declared application ledger is 76 operations at N=4. At full size N=64, one signed-sector scan has length n=32 and costs 129 field operations, rather than one scalar operation. Arithmetic counts use precomputed coefficients; setup is separately O(N) field operations/words across all dyadic levels: twiddle tables by multiplication, powers of t by squaring, and inverse wrap constants. Exact coefficient representation and bit complexity are not bounded by this unit-cost field model.

The two C and two C^{-1} appearances cancel through the factorization. Performing that proved cancellation gives the ordinary decimation-in-frequency evaluation:

    u_j=x_j+x_(j+n),
    v_j=omega_N^j (x_j-x_(j+n)),
    even outputs=F_n u,    odd outputs=F_n v.

Its elementary unspecialized ledger is

    A_fast(1)=0,
    A_fast(N)=2 A_fast(N/2)+3N/2
             =(3/2)N log2(N),

with N-word output interleaving per level. Special constant multipliers can be optimized, but the recurrence remains Theta(N log N). This construction demonstrates exact coefficient closure while making clear that it does not establish the requested asymptotic improvement.

## 7. Every positive integer size

For a non-dyadic N, let M be the least power of two with M>=2N-1, so M<4N, and let eta be a primitive 2N-th root. Form length-M vectors

    a_j=x_j eta^(j^2),                    0<=j<N,
    b_(r mod M)=eta^(-r^2),               -(N-1)<=r<=N-1,

with remaining entries zero. Then

    (F_N x)_k=eta^(k^2) (a * b)_k,        0<=k<N,

where convolution is cyclic of length M. This follows directly from 2kj=j^2+k^2-(k-j)^2; the chosen padding prevents interfering terms.

Charge both forward transforms, including the kernel spectrum, and the inverse transform. In the positive-exponent convention F_M^{-1}=J F_M/M, where J reverses nonzero indices. The fully paid bound is

    A_all(N) <= 3 A(M)+2M+2N,

besides O(M+N) data placement and coefficient setup. The 2M term includes pointwise products and inverse normalization; 2N includes both chirp masks. Kernel-spectrum preprocessing is not free in this bound. Replacing A by the simplified dyadic recurrence gives the familiar O(N log N) all-size bound. No sub-N-log-N conclusion follows.

## 8. Exact controls and limitations

Run:

    python3 check_fourier_shear_lift.py

The checker uses no uploaded or earlier constructor code. It verifies:

- All four natural Fourier block ranks, and every coefficient in the parity-shuffled identity.
- C's sparse inverse, the original-family C^2 obstruction, the transpose small-size exceptions, and the inverse-kernel normalized full Fourier identity.
- Sixty matrix instances: N=4,8,16,32,64; three signed-cycle routings/voltage choices; poles 1/2 and 1/3; two finite fields.
- A genuine signed-scan recursive executor on seeded vectors at N=1 through 256 in two fields, with the stated operation ledger.
- Nine non-dyadic chirp-convolution controls, charging all three transforms.

The all-size equalities and complex-pole exclusions are proved above. Finite-field controls are reproducibility checks, not standalone proofs for unspecified complex coefficient families. The scalar operation ledger counts multiplication by precomputed coefficients, not the Python interpreter's integer or index operations. The dense matrices in the verification harness are not part of the claimed execution algorithm.

What remains open is an explicitly specified richer coefficient architecture whose entire paid recurrence is genuinely below N log N. These results isolate why the rank-only milestone cannot certify that goal and supply an exact, conservatively charged fallback.
