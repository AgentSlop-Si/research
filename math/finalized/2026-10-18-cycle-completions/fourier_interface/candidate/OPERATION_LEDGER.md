# Operation ledger

The unit model is literal scalar real arithmetic on exact coefficient lanes.
One add/subtract of complex values has two real adds; subtraction also charges
two signs. Multiplication by i or -i swaps real/imaginary positions and charges
one sign. A left shift and a division by 2^k each count as one operation per
real word, regardless of k. These are word counts, not constant bit costs.

## One main-interface pair, after its twiddle

- U(-2): 2 real adds, 2 negations, 2 left shifts.
- Q on the second coordinate: 1 negation and a component swap.
- Literal R30 rho=3: 8 real adds, 6 negations, 4 left shifts, 4 divisions by 8.
  Its 6 signs are 2 from the routing phases and 4 from output negation.
- Q^-1 on the second coordinate: 1 negation and a component swap.
- L(+1): 2 real adds.
- diag(-8,-2): 4 negations and 4 left shifts (two by 3 and two by 1).
- Total: 12 adds, 14 negations, 10 left shifts, 4 binary divides.

Both data outputs are required. No identity cancellation, constant folding
across R30, or data-dependent shortcut is applied. Zero-valued inputs still
execute the same operations. Separate pointer/index work, reads/writes, and
coefficient-lane routes are accounted below rather than described as free.

## Abstract complex-field Fourier implementation

Let N=2^D and T=ND/2-3N/2+2 be the standard number of general complex twiddle
multiplications after removing twiddles 1 and i. A general twiddle multiply
uses 4 real multiplications, 2 real additions, and 1 negation. There are N/2-1
i-twiddles, each charged one negation/component swap.

Our pairwise adapter construction therefore has:

- Real additions: 6ND+2T.
- General real multiplications: 4T.
- Real negations: 7ND+(N/2-1)+T.
- Left shifts: 5ND.
- Exact binary divisions: 2ND.
- O(ND) data/index work and O(N) field-coordinate storage, assuming the field
  operations and coefficients are available.

The baseline has 2ND+2T real additions and the same 4T real multiplications.
At N=256 this is 13,572 versus 5,380 real additions, with the same 2,568 real
multiplications. The adapter also has 15,105 negations, 10,240 left shifts,
and 4,096 exact divisions. This field accounting is not a claim that arbitrary
roots are natively supported by R30's Gaussian-dyadic fixed grid.

## Explicit Gaussian-dyadic coefficient lanes

Let ell=max(1,N/4). Put P=ND*ell/2, the number of actual scalar pair calls.
The matrix adapters and R30 consume:

- 12P=6ND*ell real additions.
- 14P=7ND*ell real negations, plus twiddle signs below.
- 10P=5ND*ell left shifts.
- 4P=2ND*ell exact binary divisions.
- No general coefficient multiplication: twiddles are lane permutations/phases.

A twiddle e=jN/2^m sends h to (h+e) mod ell and contributes i^floor((h+e)/ell).
For N>=4, each stage twiddle has 0<=e<2ell. Its total real sign count over all
ell lanes is exactly e: phases i^0,i^1,i^2 use 0,1,2 signs, respectively.
Summing the e's over the DIT program gives

    Qsign = N^2(D-2)/8 + N/4.

The same formula gives zero at N=2. Total negations are 7ND*ell+Qsign.
The code computes these signs through each executed phase, independently of
this formula.

At N=256, D=8, ell=64, P=65,536:

- 786,432 real additions.
- 966,720 real negations, including 49,216 twiddle signs.
- 655,360 left shifts.
- 262,144 exact binary divisions.
- 16,384 resident Gaussian coefficient positions, each containing two real
  numerators; additional buffers change only the constant factor.

The same lifted ordinary radix-two program uses 262,144 real additions and
180,288 real negations. Thus even in this expanded representation the adapter
program has triple the butterfly additions, plus shifts and divisions.

## Representation, I/O, width, and preprocessing

- An exact field value is ell Gaussian-dyadic coefficients and the fixed
  relation z^ell=i. It is never treated as one constant-size numeric word.
- For lane-zero input, allocate/initialize N*ell lanes and place N inputs.
  For general K_N inputs, all N*ell lanes must be read.
- A literal bit reversal copies N*ell lanes and constructs N D-bit indices.
- There are ND/2 twiddles; each routes ell lanes. The kernel visits ND*ell/2
  pairs. The implementations therefore perform O(ND*ell) lane reads, writes,
  phase routes, and O(log N)-bit index operations. The verifier uses explicit
  Python lists and temporary buffers; its wall clock is not a benchmark claim.
- Exponents e are prepared by stage-index arithmetic, with O(ND) exponent
  computations and O(1) resident stage coefficients. No numerical root table
  or root evaluation is hidden. Output is an exact coefficient array.
- There are O(N*ell) resident coefficient positions; the verifier's separate
  direct-DFT oracle costs O(N^2*ell) and is validation work, not the algorithm.
- If input real numerators have bound M0 and are multiples of 8, choose signed
  b with 2^(b-1)>5NM0. The pairwise algorithm stays exact on that grid. Its
  direct scalar bit-work upper bound is O(ND*ell*b), plus index work. The three
  reserve bits may be supplied by scaling the initial encoded numerators by 8
  and recording that common denominator; this initial representation step and
  final denominator metadata are charged, not a numerical approximation.
- Producing decimal/IEEE complex outputs would additionally require a precision
  contract and evaluating the root basis; it is not part of this exact-output
  construction and is not declared free.
