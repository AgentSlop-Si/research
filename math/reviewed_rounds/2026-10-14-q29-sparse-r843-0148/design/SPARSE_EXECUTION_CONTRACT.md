# Q29: bounded sparse cyclotomic execution contract

2026-10-14 UTC. Exact implementation design and fresh small controls only.

## Result

The accepted mod-25 carry contract admits a substantially smaller arithmetic design than generic degree-1,800 coefficient multiplication. Use

    C_2 = (Z/25 Z)[z] / Phi3375(z),
    Phi3375(z) = Phi15(z^225)
               = z^1800-z^1575+z^1125-z^900+z^675-z^225+1.

This is exactly the accepted ring B_2, not an approximation. Under the fixed root convention,

    q=z, alpha=z^1000, beta=z^2376, pi=beta-1.

Every q multiplier in the reciprocal recurrence becomes a monomial shift with a small, exact, signed reduction table. A fused reciprocal step uses two variable monomial shifts and one particularly cheap multiplication by z. It has no general coefficient-ring products and no divisions. A separate paired even/odd recurrence computes the odd-factor-free polynomial directly, avoiding the extra raw v coefficient required when dividing a truncated H by v.

For the proposed m=843, w-degree <100 run, the specified canonical-basis kernel has a budget of 849,703,500 signed shift-scatter updates, at most 857,334,600 other coordinate additions/subtractions, and at most 142,830,000 scalar doublings. A simple stagewise implementation additionally performs at most 856,798,200 coordinate modular reductions. The arithmetic-update subtotal is 1,849,868,100. These are declared algorithm-specific operation counts, not measured full-run timings. They replace the earlier generic multiplication baseline; they do not constitute a like-for-like wall-clock speedup factor.

The full R843/H1687 computation was **not run**. No old scientific program was imported or executed. No external files, repositories, tables, or rankings were changed. This is a bounded implementation route for the existing Q29 contract, not a new FFT algorithm or a novelty claim.

## 1. Exact ring isomorphism and root binding

Let

    B_Z = Z[a,b] / (Phi27(a), Phi125(b)).

Both factors are monic; B_Z is free of rank 18*100=1,800 over Z. For complex primitive roots a and b of orders 27 and 125, their product has order 3,375. Consequently Phi3375(ab)=0 in B_Z: this can be checked in all complex embeddings, and B_Z injects into its rational tensor algebra because it is free over Z.

The maps

    Z[z]/Phi3375(z) -> B_Z, z -> ab,
    B_Z -> Z[z]/Phi3375(z), a -> z^1000, b -> z^2376

are inverse. Indeed

- 1000 is 1 modulo 27 and 0 modulo 125;
- 2376 is 0 modulo 27 and 1 modulo 125;
- 1000+2376=3376 is 1 modulo 3375.

Thus (ab)^1000=a, (ab)^2376=b, and z^1000*z^2376=z. The cyclotomic relations of the images hold over Z, not merely modulo 5. Equivalently, the first map is surjective between free Z modules of equal rank and hence is an isomorphism. Reducing modulo 25 and making the triangular integral substitution b=1+T gives

    C_2 ~= (Z/25)[a,T]/(Phi27(a),Phi125(1+T)) = B_2.

The identity Phi3375(z)=Phi15(z^225) follows by checking roots: if z^225 has exact order 15, the 3- and 5-adic parts of the order of z must both be cubed, so z has exact order 3375. The degrees agree. No division is used in the finite-ring implementation.

The accepted contract already fixes the reduction of alpha to eta in F_(5^18). The new representation must retain that identification. Selecting another primitive z, or replacing pi by a different primitive-125-root minus 1, is an explicit coordinate change, not permission to compare arrays without conversion.

Fresh controls verify all 1,800 basis vectors in each direction for the integral z <-> alpha,beta maps, giving 3,600 exact integer inverse checks. They also check the root-order guards and ten dense mod-25 round trips through the alpha,pi basis.

## 2. The sparse shift kernel

Write y=z^225. Reduce y^b modulo

    Phi15(y)=y^8-y^7+y^5-y^4+y^3-y+1.

For b=0,...,7 the remainder is y^b. The remaining seven rows are

    y^8  =  y^7-y^5+y^4-y^3+y-1
    y^9  =  y^7-y^6-y^3+y^2-1
    y^10 = -y^5-1
    y^11 = -y^6-y
    y^12 = -y^7-y^2
    y^13 = -y^7+y^5-y^4-y+1
    y^14 = -y^7+y^6+y^4-y^3-y^2+1.

All row coefficients are ±1, and every row has at most six terms. Since z^3375=1, an arbitrary monomial z^e is reduced by

    e <- e mod 3375,
    e = 225*b+r, 0<=r<225,
    z^e = z^r * remainder(y^b).

Define S_t(c)=z^t*c in C_2. For each input coordinate c_i, distribute it with the row signs to the output coordinates obtained from e=(i+t) mod 3375. This is exact multiplication, with integer carries retained modulo 25. It is not coefficient arithmetic in characteristic 5.

### Packed block implementation

Store a coefficient as eight contiguous blocks of length 225. Write t=225*b+s, 0<=s<225. For source block a, split its residue interval into r<225-s and r>=225-s. These two contiguous pieces use reduction rows (a+b) mod 15 and (a+b+1) mod 15 respectively, with the corresponding residue offsets. This needs at most sixteen input block slices and at most six signed output-slice updates per slice. It avoids per-coordinate division and remainder calculations in the hot loop.

If d_j is the number of nonzero terms in reduction row j, the exact signed-scatter count for one dense coefficient is

    C(t) = sum_(a=0)^7 [(225-s)d_((a+b) mod 15)
                       +s*d_((a+b+1) mod 15)].

The fresh enumeration gives C(1)=1,805 and max_t C(t)=6,525. Multiplication by z can also be implemented as a shift/copy plus reduction of the single outgoing top coefficient.

Every output row of every S_t has absolute row sum at most six. Therefore canonical inputs 0,...,24 give a signed intermediate of absolute value at most 144. This supports signed int16 for the individual, stage-normalized kernels, or int32 as a conservative production choice. Operands must be widened before additions; doing arithmetic in uint8 and converting afterward is wrong. Normalize modulo 25 after each stage described below. Storage in uint8 is safe only after normalization.

The current Python control code is a sparse reference kernel. It is not the packed block-slice production implementation, and its tiny timing is not a throughput measurement.

## 3. Removing the odd factor without a precision loss

The usual Rogers–Szego polynomial is H_n(x;q)=sum_k GaussianBinomial(n,k;q)x^k. Its standard recurrence is

    H_(n+1)=(1+x)H_n-x(1-q^n)H_(n-1),
    H_0=1, H_1=1+x.

This identity is classical; for example see Johann Cigler, *Some remarks and conjectures about Rogers–Szego polynomials*, equation (3):
https://homepage.univie.ac.at/johann.cigler/preprints/hankel-rs.pdf

The following paired implementation is an elementary regrouping of that identity, not a new polynomial family. Define

    E_m=H_(2m),
    O_m=H_(2m+1)/(1+x),
    E_0=O_0=1.

The quotient is an integral polynomial. Inductively, the recurrence gives

    E_m=(1+x)^2 O_(m-1)-x(1-q^(2m-1))E_(m-1),
    O_m=E_m-x(1-q^(2m))O_(m-1).

These two formulas can instead define E_m and O_m, and then establish H_(2m+1)=(1+x)O_m. Multiplication by the monic polynomial 1+x is injective even over a coefficient ring with zero divisors, so the quotient is unambiguous. No ring inverse, pi division, or evaluated division by 1+x is needed.

At x=-1-v, writing the same letters for substituted polynomials,

    E_m=v^2 O_(m-1)+(1+v)(1-z^(2m-1))E_(m-1),
    O_m=E_m+(1+v)(1-z^(2m))O_(m-1).

Thus O_843 is exactly U1687(-1-v;q), with the accepted sign convention

    U1687(-1-v;q) = -H1687(-1-v;q)/v.

Compute modulo v^200 throughout. Every multiplication has nonnegative v degree, so discarded terms never return to retained degrees. This paired recurrence directly supplies raw U modulo v^200 at coefficient precision 200. Unlike a truncated direct H route, it does not require retaining v^200 of H as an extra coefficient. There is no pi-precision digit loss from removing 1+x. The later pi^60 content normalization still loses the accepted 60 digits.

The paired route is useful as an independent production cross-check. Its planned main shift count is 317,200 coefficient shifts, with 1,413,798,000 signed scatter updates under this canonical kernel. The reciprocal route below retains half as many variable coefficients and has a lower shift budget.

## 4. Reciprocal recurrence and its fused sparse form

Eliminating E from the paired recurrence gives

    O_m=[(1+x)^2-x(2-q^(2m)-q^(2m-1))]O_(m-1)
        -x^2(1-q^(2m-1))(1-q^(2m-2))O_(m-2).

Set w=(1+x)^2/x and write O_m=x^m R_m(w), understood as the polynomial identity

    O_m(x)=sum_(k=0)^m r_(m,k) x^(m-k)(1+x)^(2k).

There is no need to invert x in an implementation. The resulting accepted recurrence is

    R_m=(w-2+z^(2m)+z^(2m-1))R_(m-1)
        -(1-z^(2m-1))(1-z^(2m-2))R_(m-2),
    R_0=1, R_(-1)=0.

For P=R_(m-1), Q=R_(m-2), use the fused stages

    D=Q-S_(2m-2)(Q),
    T=P+S_1(P)+D,
    R_m=wP-2P-D+S_(2m-1)(T).

Expanding the last term gives S_(2m)P+S_(2m-1)P+S_(2m-1)D, exactly the accepted recurrence. The combination exploits linearity; it does not drop the product of the two nonunit factors in the original formula.

All stages can be computed modulo w^100. With arrays of length 100, the coefficient formula is

    d_k = q_k - S_(2m-2)(q_k),
    t_k = p_k + S_1(p_k) + d_k,
    r_k = p_(k-1) - 2p_k - d_k + S_(2m-1)(t_k),

where p_(-1)=0 and absent coefficients are zero. Q is absent at m=1. Terms w^100 and higher can be discarded immediately. No general product of two arbitrary 1,800-coordinate vectors occurs anywhere in this recurrence.

Recommended memory schedule: keep P and Q unchanged while streaming k. Store the output in a third slice, and retain only d_k,t_k and one shift scratch coefficient, rather than full D and T slices. Rotate Q,P,R after each completed m. Do not overwrite P before its p_(k-1) contribution has been consumed. Checkpoint only after the full step and its modular reductions are complete.

## 5. Exact coordinate conversion and precision handoff

Conversion back to the accepted alpha,pi basis is efficient and integral.

1. For each canonical z^e with 0<=e<1800, compute a=e mod 27 and b=e mod 125.
2. If a>=18, use alpha^a=-alpha^(a-9)-alpha^(a-18).
3. If b>=100, use beta^b=-beta^(b-25)-beta^(b-50)-beta^(b-75)-beta^(b-100).
4. The result has alpha degree <18 and beta degree <100. This stage has exactly 3,789 signed scatter updates per dense z coefficient in the unoptimized full layout.
5. For each alpha coordinate, use beta^b=(1+pi)^b. A direct triangular Pascal transform has at most 18*(100*101/2)=90,900 modular scalar multiply-accumulations per coefficient.

The inverse uses pi^j=(beta-1)^j followed by alpha^a beta^b=z^((1000a+2376b) mod 3375) and the same sparse reduction table. Both transforms have integer coefficients; neither loses precision. The basis is a power basis, not a normal basis.

Prefer converting the 100 retained R coefficients first, costing at most 9,090,000 triangular multiply-accumulations plus 378,900 signed scatters. Then form the raw U jet in the accepted basis using

    U1687(-1-v;q)
      = sum_(k=0)^99 (-1)^(843+k) r_(843,k)
        v^(2k)(1+v)^(843-k)       modulo v^200.

There are 10,100 scaled coefficient additions in this transform, or at most 18,180,000 coordinate multiply-accumulations, with integer binomial coefficients reduced modulo 25. No coefficient at w>=100 contributes below v^200.

At this handoff, the output is certified modulo (pi^200,v^200), exactly as in the accepted contract. Multiplication by pi and guarded division must use the full accepted relation, not a z-array index shift and not an inverse of pi. The accepted modulo-25 relation is automatically preserved by C_2; the fresh controls reproduce v_pi(5)=100, v_pi(5+pi^100)=125 and v_pi((1+pi)^5-1-pi^5)=101.

Before claiming a normalized result, certify the required pi^60 content of U1687(-1-pi Y;q) and apply the guarded divisions. The common guaranteed bound remains

    F(Y)=pi^-60 U1687(-1-pi Y;q) modulo pi^140.

The ring capacity is 200, but the post-normalization certified precision is only 140. Each later branch division further lowers that bound. No basis change, recurrence regrouping, or memory optimization promotes it back to 200. The content certification and all modulo-5 comparisons with recovered reference coordinates remain mandatory for a future full run.

## 6. Transparent operation and storage budget

For m=1,...,843 and L=100, define

    a_m=min(m,100), b_m=min(m-1,100), o_m=min(m+1,100).

These upper bounds include zero or special coefficients; they do not assume accidental sparsity. Their sums are A=79,350, B=79,250 and O=79,449.

Under the specified fused schedule:

- S_1(P): A coefficient shifts; 143,226,750 signed scatter updates.
- S_(2m-2)(Q): B coefficient shifts; 353,017,800 signed scatter updates.
- S_(2m-1)(T): A coefficient shifts; 353,458,950 signed scatter updates.
- All shifts: 237,950 coefficient shifts; 849,703,500 signed scatter updates.
- D subtraction, two T additions, and three output additions/subtractions: at most 1800*(B+2A+3O)=857,334,600 coordinate additions/subtractions.
- Scalar doubling of P: at most 1800*A=142,830,000 operations.
- Stagewise canonical reductions after each of the three shifts and after D,T,R: at most 1800*(3A+2B+O)=856,798,200 coordinate reductions modulo 25.

The counts for each shift use C(t), not the pessimistic 6,525 maximum. Copies, zero initialization, loop overhead, loads/stores, checkpoint hashes, source comparisons, serialization, the final basis and jet transforms, and normalization are not included in the arithmetic-update subtotal. They must be charged in any actual execution receipt. Shift signs require no nontrivial scalar multiplications. A production implementation may reduce some counts by fusing copies, exploiting zero/one coefficients, reducing modulo 25 less often with a proved safe bound, or vectorizing the contiguous block slices. None of those savings is presumed here.

Three uint8 rolling R slices use 3*100*1800=540,000 payload bytes. Three int32 scratch coefficients add 21,600 bytes. One converted R slice uses 180,000 bytes; one raw U jet uses 360,000 bytes. These can reuse recurrence storage. The fifteen-row reduction table is tiny, and no cache of all 3,375 dense q powers is required. These numbers exclude allocator/language overhead, source reference arrays, checkpoints and metadata. Keeping all rolling coefficients in int16 or int32 increases their payload proportionally.

The previous 513,864,000,000 schoolbook scalar product-accumulations concerned a different generic multiplication algorithm and excluded its monic reduction. It was an upper budget, not a lower bound. The present budget does not establish a benchmark ratio or a practical seconds estimate. A compiled packed kernel and an instrumented completed receipt are needed for a timing claim.

## 7. Fresh checks and exact scope

Only `fresh_sparse_controls.py` in this directory was executed for these controls. It is newly written, imports only Python standard-library modules, and neither imports nor executes predecessor code. The earlier precision-contract source was read as inert text and hashed for source binding.

`CONTROL_RESULT.json` records:

- all 3,375 monomial remainder comparisons against independent descending long division;
- all 3,600 exact integer unit-basis round trips between z and alpha,beta;
- ten dense mod-25 round trips through alpha,pi;
- 25 independent shift/long-division comparisons, including wrap and block boundaries;
- 16 sparse generic-product comparisons and shift-composition checks;
- root decomposition, primitive-order guards, all three carry valuations and the exact pi nilpotence index 200;
- full H3,...,H17 checks for q=z and q=z^1001, with the latter forcing nontrivial cyclotomic reductions while retaining primitive order 3375;
- independently constructed Gaussian-binomial coefficients, monic odd-factor removal, direct substitution, paired recurrence, fused reciprocal recurrence, and expanded original reciprocal recurrence;
- truncated jets at K=1,2,3,4,7,12 and reciprocal truncations L=ceil(K/2);
- exact operation-budget enumeration without computing any coefficients of H1687 or R843.

All checks passed, with empty stderr. Timing in the receipt describes these bounded controls only. The production packed kernel, full mod-25 jet, recovered-coordinate comparison, pi^60 content certification, continuation of repeated branches, and discriminant evaluation were not performed.

Input report hashes:

- Accepted precision contract: `e1d40ce00296465e93d8607d45e645fb040c403945bd6e2f1961373c13ee5149`.
- Independent precision-contract review: `54bd52a12dffe99079e7ce598d7cf1dac27b6982fe8e6ddd52acdf12d670cb5c`.

## 8. Next acceptance gate

1. Implement the packed, widened, stage-normalized block-slice shift kernel and independently test it against the fresh reference, including all shift boundaries and dense mod-25 inputs.
2. Test the compiled fused recurrence against fresh small Gaussian/paired controls; bind array order, sign and root convention in its manifest.
3. Only then execute the separately authorized full R843, w<100 computation with deterministic checkpoints, resource measurements and hashes.
4. Convert exactly, compare every available recovered raw coordinate modulo 5, verify the content/division guards, and report the actual certified precision.
5. Stop unresolved branches at their certified ceilings. A successful shared-center jet is not full center coverage, a derivative-unit result, squarefree residual certification, or a value/nonvanishing proof for Disc R843.
