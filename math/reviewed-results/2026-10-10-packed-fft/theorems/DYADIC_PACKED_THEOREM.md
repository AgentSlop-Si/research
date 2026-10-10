# A cold packed finite-state radix-2 Fourier executor

10 October 2026. New derivation, independent of the earlier unpacked executor's runtime.

## Status and scope

The construction below closes the proposed dyadic layout and catalogue gates at the proof level. It is a deterministic, finite-word, all-input relative-Euclidean approximation theorem. It is not an exact arbitrary-complex FFT theorem, a practical speed claim, a production implementation, or a historical-novelty claim. General integer lengths are not treated here. Fresh exact controls are recorded separately and do not replace the proofs.

The accepted comparison manuscript was read as mathematical background, not executed: `research_cycle_0958/algorithms/FINAL_THEOREM_AND_PROOF.md`, SHA256 `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`. Its quantizer conventions are retained. Its materialization charges and runtime are not used to establish the new executor's runtime.

## 1. Precise theorem

Fix an input-format constant c. Let N=2^v, v>=1, and supply an integer 2<=t<=v+1. Each real and imaginary input component is a dyadic with O(c(v+1)) description bits and polynomial dynamic range: for example, a*2^e with |a|<=N^c and |e|<=c(v+1). Shared or individual exponents are allowed. Put epsilon=2^-t.

There is one uniform deterministic algorithm on an address-capable word RAM with word width w=C(c)(v+1), for a sufficiently large fixed constant C(c), that explicitly writes N dyadic mantissa/exponent outputs y such that

    ||y-U_N x||_2 <= epsilon ||x||_2,
    (U_N)[k,j] = N^-1/2 exp(-2 pi i k j/N).

Its cold running time is

    O_c(N (t+log2(v+1))),

and its space is O_c(N) words, uniformly over this finite-precision domain. Integer addition, subtraction, multiplication, division, comparisons, shifts, Boolean operations, and random access are charged RAM instructions. A fixed number of words can be used for any O_c(v)-bit integer, with a fixed number of these instructions. No SIMD instruction, free permutation, coefficient oracle, or unbounded-word multiplication is assumed. Polynomial-bit certificate calculations are charged separately.

For fixed epsilon this is O_epsilon(N log log N), asymptotically. For every supplied t=o(v), the packed branch is eventually selected. If t=Theta(v), the theorem gives only O(Nv), and the scalar fallback is sufficient. N=1 is an exact copy. Accuracy-target parsing is separately charged if an integer t is not supplied.

The broad uniform statement uses an efficient scalar fallback, not the comparison manuscript's quadratic correctness fallback. This distinction is essential.

## 2. Normalize, encode, and define every table response

Scan the input and, unless it is zero, choose a power of two R so that the maximum absolute real or imaginary component of a=x/R belongs to [1/2,1). Then

    1/2 <= ||a||_2 <= sqrt(2N).

The zero case writes N zeros and stops. All subsequent normalization and scale restoration are exact dyadic operations.

Set

    p = t+10+ceil(log2(v+1)),   u=2^-p,
    e_min = -v-p,             e_max=v+4,
    tau=2^e_min=u/N,
    E=2v+p+5,                k=ceil(log2(E+1)),
    b=2(p+k+1).

A real finite state is sign*(2^p+f)*2^(e-p), with 0<=f<2^p and e_min<=e<=e_max. Its code has a sign bit, k exponent bits, and p fraction bits. Exponent fields 1,...,E encode the valid exponents. Exponent field 0 and every field larger than E decode to zero, independently of their other bits. Zero is encoded canonically as all-zero bits. A complex state concatenates two real codes, hence occupies b bits.

The total real quantizer q truncates the mantissa toward zero, sends magnitudes below tau to zero, and clips magnitudes at or above 2^(e_max+1)=32N to the signed largest finite value. This defines every table output, even on malformed/padded codes or unreachable large states. Clipping does not satisfy the usual small-error inequality; Section 6 proves that reachable execution never clips.

Before upper clipping, the componentwise complex quantizer obeys

    ||q(z)-z||_2 <= u||z||_2+sqrt(2N)tau.                 (1)

Every decoded state lies on the common lattice 2^(-v-2p) Z[i], and its integer numerator has at most 2v+2p+O(1) bits. Exact addition and multiplication by the dyadic coefficients used below therefore require O(v+p) bits, including arbitrary valid but unreachable states. Table preparation decodes, evaluates, quantizes, and re-encodes explicitly. It never assumes a response vector is a scalar before packing it.

A leading-bit instruction is not needed. Prepare the bit-length table on h-bit chunks, h=max(1,floor(v/8)); its entries are obtained by L[0]=0 and L[j]=1+L[floor(j/2)] for j>0. It costs O(2^h) operations and words. Any O_c(v)-bit integer has only O_c(1) such chunks, so its leading bit is found in O_c(1) operations. For the finitely many v<8, use direct bit scanning. This handles input normalization/quantization and scalar fallback quantization. Input components can first be aligned to an O_c(v)-bit common dyadic lattice, so all scans and conversions cost O_c(N).

## 3. Certified coefficient grid and its exact local map

Let

    g=p+10,   Q=2^g.

For q=0,...,Q-1, prepare a complex dyadic c_q whose components lie on the p+10-fractional-bit lattice and are each within u/1024 of the corresponding component of exp(-2 pi i q/Q). Certified interval midpoints followed by rational nearest-grid rounding achieve this without deciding exact transcendental rounding ties. Thus

    |c_q-exp(-2 pi i q/Q)| <= sqrt(2)u/1024.

Prepare a real dyadic s_hat with |s_hat-1/sqrt(2)|<=u/1024. For the butterfly at phase j/L, use q=floor(Qj/L). The angular displacement and coefficient approximation give

    |c_q-exp(-2 pi i j/L)|
       <= (2pi+sqrt(2))u/1024 < u/128.                  (2)

For any such phase define the exact dyadic prequantization map

    A_q(a,b) = (s_hat*(a+c_q b), s_hat*(a-c_q b)).

If B_j/L is the ideal normalized butterfly, then, using the factorization through the Hadamard matrix,

    ||A_q-B_j/L||_2
       <= sqrt(2)|s_hat-1/sqrt(2)|
          +sqrt(2)|s_hat| |c_q-exp(-2 pi i j/L)|
       < u/32.                                         (3)

The deliberately loose bound holds for u<=1/4. Each local table response applies A_q exactly in dyadic arithmetic, followed by q independently to its real components. For malformed input codes, first use the total decoder from Section 2.

A uniform elementary coefficient generator suffices. Machin's identity and alternating arctangent sums enclose pi; rational Taylor sums with factorial remainders enclose sine and cosine on a bounded argument. A degree O(p+v+1), with a sufficiently large fixed constant, suffices. Integer square roots enclose 1/sqrt(2). Naive exact rational arithmetic has polynomially many bits and polynomially many operations. Output dyadics can be certified by continuing the interval computation until a dyadic within the required error has been selected; no exact rounding-to-nearest decision is necessary. Hence there is a fixed computable polynomial bounding work and scratch space per coefficient. All of it is included below.

## 4. Packed representation and the complete Q-1 catalogue

For the packed branch, choose the largest power of two P=2^d satisfying

    2bP <= v/8,

equivalently P<=v/(16b). Branch selection below ensures such a P exists. Pack P consecutive complex states per word, low lane first. The word length is bP<=v/16; a pair key and response each have 2bP<=v/8 bits.

First bit-reverse the input positions and quantize/pack them. A direct O(N) method initializes N/P zero words, then sends input i to the lane for rev_v(i) using one mask, one shift, and one OR. The bit-reversed index can be maintained incrementally: after position i, flip its leading run of one bits and the next zero bit, beginning at N/2. Across all N indices fewer than 2N bit flips occur. Thus bit reversal costs O(N) total, with no free permutation and no O(v) charge per input.

Now use literal in-place iterative normalized radix-2 DIT. At stage ell, L=2^ell. Its butterflies pair positions j and j+L/2 inside each aligned length-L span, using phase exp(-2 pi i j/L). The bit-reversed input convention yields outputs in ordinary frequency order.

### 4.1 Small spans, ell<=d

Each entire length-L block is inside a packed word. The same arrangement repeats in every word. For each ell=1,...,d, prepare a table of 2^(bP) P-state responses. For each key, decode P states, perform all P/2 disjoint stage butterflies, quantize, and repack. One read/lookup/write updates a word. No phase identifier depends on the word's global index.

### 4.2 Large spans, ell>d

Put r=ell-d. A span contains 2^r words. A first-half word has index a=0,...,2^(r-1)-1 inside that span; it pairs with word a+2^(r-1). Its lanes use grid indices

    floor[Q(Pa+l)/(P2^r)],    l=0,...,P-1.               (4)

Prepare the following COMPLETE catalogue, including any patterns not reached at the current N:

    s=1,...,g,
    h=0,...,2^(s-1)-1,
    pattern(s,h)[l] = floor[Q(Ph+l)/(P2^s)].             (5)

Its number of entries is

    sum_{s=1}^g 2^(s-1) = Q-1.                          (6)

For an actual stage/word pair define

    s=min(r,g),
    h=a >> max(r-g,0),
    id=2^(s-1)-1+h.                                    (7)

If r<=g, (4) and (5) are identical. If r>g, write a=2^(r-g)h+c with 0<=c<2^(r-g). Then

    Q(Pa+l)/(P2^r) = h+(Pc+l)/(P2^(r-g)),
    0 <= Pc+l < P2^(r-g),

so (4) equals h for every lane. Catalogue row (g,h) is also constantly h, since (5) becomes floor(h+l/P). This proves (7) exactly, including all alignment and boundary cases. Long spans add no patterns. The proof does not require Q>=P, although that inequality holds in the selected parameter regime.

For each catalogue entry prepare EVERY 2P-state response. There are S=2^(2bP) keys. Low P lanes encode the first input word and high P lanes the second. Apply P independent exact A_q maps and total quantization, then pack all first outputs into the low bP bits and all second outputs into the high bP bits. Each entry occupies one word. The large table is flattened; entry address is

    (id << (2bP)) + key.                               (8)

There is no online pattern search, coefficient generation, directory traversal, scalar gathering, or scalar unpacking. Formula (7) uses one shift and an addition after stage constants have been prepared.

## 5. Explicit charged pseudocode

All arrays below contain one machine word per entry. Arithmetic in BUILD uses polynomially charged exact operations; EXECUTE's integers fit a fixed number of words. Here MASK=(1<<(bP))-1, S=1<<(2bP), and S0=1<<(bP).

    BUILD:
      Build the Q coefficients and s_hat with certificates.
      For s=1,...,g:
        For h=0,...,2^(s-1)-1:
          id=(1<<(s-1))-1+h
          For key=0,...,S-1:
            Decode 2P states from key.                         [O(P) work]
            For lane=0,...,P-1:
              q=floor(Q*(P*h+lane)/(P*(1<<s)))
              (out0[lane],out1[lane])=quantized A_q pair       [poly(v+p)]
            T[(id<<2bP)+key]=pack(out0,out1)                  [O(P) work]
      For ell=1,...,d:
        For key=0,...,S0-1:
          Decode P states.
          Apply all P/2 stage-ell butterflies, with
            q=floor(Q*j/(1<<ell)) for each local j.
          TS[(ell-1)*S0+key]=quantize_and_pack_outputs.

    EXECUTE:
      Scan/normalize input; initialize W[0,...,N/P-1]=0.
      For each input i, maintaining r=rev_v(i) amortized O(1):
        code=quantize(x[i]/R)
        W[r>>d] |= code << (b*(r & (P-1)))                  [O_c(1)]
      For ell=1,...,v:
        If ell<=d:
          off=(ell-1)*S0
          For z=0,...,N/P-1:
            W[z]=TS[off+W[z]]                              [O(1)]
        Else:
          r=ell-d; s=min(r,g); shift=max(r-g,0)
          base=(1<<(s-1))-1; span=1<<r; half=span>>1
          For block=0,span,2span,...,N/P-span:
            For a=0,...,half-1:
              id=base+(a>>shift)
              key=W[block+a] | (W[block+a+half] << bP)
              response=T[(id<<2bP)+key]
              W[block+a]=response & MASK
              W[block+a+half]=response >> bP              [O(1) pair]
      For k=0,...,N-1:
        Extract its b-bit state from W[k>>d].
        Decode it, add log2(R) to its exponent, write y[k]. [O_c(1)]

Each small stage does N/P word updates; each large stage does N/(2P) pair updates. Block/loop controls and all addresses take constant work per update; there are no more blocks than updates. Stage constants take O(v) total work. Thus execution costs

    O_c(N+Nv/P)=O_c(Nb),                                (9)

because P>v/(32b). The scalar output materialization occurs only once, at the end, and costs O(N).

All raw table keys and responses fit within v/8 bits. The preparation cap bounds the number of entries by N. Actual addresses therefore need only v+O(1) bits. The table offset in (8) and the packed input/output shifts cannot overflow the chosen RAM word. No multiplication by a many-word address is hidden.

## 6. All-input error and exclusion of reachable clipping

Every ideal stage is a unitary direct sum of normalized butterflies, up to the initial bit reversal. By (3), the corresponding exact dyadic prequantization stage has operator error below u/32. Combining with (1) gives, whenever the stage does not upper-clip,

    ||computed(z)-ideal(z)||_2
       <=3u||z||_2+sqrt(2N)tau.                         (10)

This holds also for each small-span table: all its butterflies are disjoint, not sequential within that stage. Initial quantization satisfies (10) with the identity as its ideal stage. There are J=v+1 rounded stages including that initial quantization.

Let e_j be the distance to the exact ideal program after j such stages. Then

    e_(j+1) <= (1+3u)e_j+3u||a||_2+sqrt(2N)tau.

Since 3uJ<1/2, the product factor is at most 2. Using ||a||_2>=1/2 and sqrt(2N)<=2N yields

    e_J/||a||_2
      <=6uJ+4J sqrt(2N)tau
      <=6uJ+8JN tau
      =14uJ
      <=14 epsilon/1024 < epsilon.                    (11)

The same bound applies to every prefix. To avoid circularity, assume a first stage whose table response clips. Every preceding stage obeys the recurrence, so its stored vector has norm at most (1+epsilon)||a||_2. By (3), the first hypothetical clipping stage's entire prequantized vector has norm at most

    (1+u/32)(1+epsilon)sqrt(2N) < 2sqrt(2N) < 32N.

No real component can reach the clipping threshold 32N, a contradiction. Initial quantization is already below magnitude 1. Thus all reachable responses avoid upper clipping, despite the tables being total on every key. Restoring R multiplies both the error and ||a|| by R, proving the required relative-l2 contract for every represented input, including cancellation-heavy and extremely small inputs. The zero input is exact.

## 7. Fully charged preparation and uniform branch selection

The exact number of response entries is

    (Q-1) 2^(2bP) + d 2^(bP).                           (12)

Each is constructed in P poly(v+p) charged operations; that factor includes decoding, the O(P) coefficient-index computations, exact dyadic arithmetic, total quantization, and packing. Add Q poly(v+p) coefficient construction, the leading-bit table, loop constants, and polynomial scratch work.

The preparation algorithm is uniform without consulting an unspecified asymptotic constant. Its branch rule is an actual bounded computation:

    If b>v/64, select the scalar fallback immediately.
    Otherwise choose maximal P as above.
    Attempt BUILD with an N-instruction and N-word preparation budget.
    Count every elementary RAM step of the coefficient routines,
      table construction, indexing, and allocation.
    If either budget would be exceeded before completion, abort BUILD,
      discard/reuse its scratch and table storage, and use the fallback.
    Otherwise use the completed tables.                          (13)

Bookkeeping for the step counter increases work by only a fixed factor. The memory cap applies to all preparation storage, including exact-rational scratch; increment/check allocation before using the slot. Table sizes can be checked first using arithmetic saturated at N+1. Even before a budget abort, proposed response-table offsets have at most g+2bP+O(1)<=17v/128+O(1) bits in the low-b branch, so computing them does not exceed the word model. The build need not allocate an oversized array and cannot hide work in a single arbitrary-precision instruction. Aborting a build never exposes a partial table to execution. Storage can be reclaimed by resetting an arena; even explicitly clearing at most N slots would cost only O(N).

Thus successful preparation, failed preparation, and its budget bookkeeping cost O(N), and attempted preparation uses O(N) words. A successful packed execution has cold cost O(Nb) by (9). All its input, output and working arrays, together with the table and scratch arena, occupy O(N) words. There is no simultaneous family of N-element stage arrays.

To establish eventual success, the specified elementary generator and table loops have a fixed polynomial work/space bound. Appendix A gives a concrete construction. In particular, some fixed constants C,K bound the *unbudgeted* preparation by

    C [(Q-1)2^(2bP)+d2^(bP)+Q
          +2^max(1,floor(v/8))+1] (v+p+1)^K.             (14)

These constants belong to the mathematical complexity analysis, not to a run-time oracle or an instance-dependent choice. When b<=v/64, p<=v/128, and

    log2(Q*2^(2bP)) <= p+10+v/8 <=17v/128+10.

The other terms in (14) are smaller up to fixed polynomial factors. Therefore some fixed C1,K1 bound the full unbudgeted preparation uniformly throughout this low-b regime by

    C1 2^(17v/128)(v+1)^K1 = o(2^v).                   (15)

Consequently every build beyond one absolute finite threshold V0 finishes within both literal budgets, uniformly over every permitted t with b<=v/64. In particular, for every supplied t=o(v), b=o(v), and the packed branch is eventually selected. Its cold preparation is o(N) in that regime. This proves uniform selection without needing to compute V0 or know a numeric asymptotic constant.

## 8. Scalar fallback and why the theorem is uniform

When the branch rule (13) selects the fallback, use the same normalized radix-2 DIT layout one scalar state per word, with the same p, total quantizer, and error budget. Prepare a full-circle coefficient array once, with guard precision

    K=p+v+20.

Certify omega_hat with |omega_hat-exp(-2 pi i/N)|<=2^-K. Set z_0=1 and

    z_(j+1)=R_K(z_j omega_hat),

where R_K truncates each real component to the 2^-K lattice. Writing e_j=|z_j-exp(-2 pi i j/N)| gives

    e_(j+1)<=(1+2^-K)e_j+(1+sqrt(2))2^-K.

For 0<=j<N, elementary geometric summation yields

    e_j<=6N2^-K < u/131072.

Each z_j stays bounded by 2. Exact products, truncations, and all indices have O(v+p) bits, so every recurrence step costs O(1) fixed-word instructions. The certified seed costs poly(v+p) work and scratch space; its full cost is included. The coefficient for stage ell and local position j is array entry j<<(v-ell). Multiply with a certified s_hat and quantize explicitly. The butterfly coefficient/operator bounds used in Section 6 are stronger than required, so that proof applies unchanged.

The scalar FFT costs O(Nv+poly(v+p)) work and O(N+poly(v+p)) words. Because t<=v+1, p=O(v+1), and every fixed polynomial in v is O(2^v), these are O(Nv) work and O(N) words with uniform constants. This observation includes the finitely many small v; it does not silently discard seed construction.

If b>v/64, then Nv<64Nb. Otherwise the fallback is selected only because the literal preparation budget is exhausted, and (15) implies v<V0. At those finitely bounded sizes Nv<=V0 Nb. Therefore in ALL cases fallback work is O(Nb), with one constant independent of v,t. Finally

    b=Theta(t+log2(v+1)),

which proves the uniform theorem in Section 1. The proof makes no assertion that its constants or crossover are useful in practice.

The theorem is limited to the stated finite precision domain 2<=t<=v+1. No arbitrary-t cost is claimed here. Higher precision would require separately charging the longer state arithmetic and leading-bit extraction.

## 9. Verification, remaining gates, and limitations

The fresh standalone `check_packed_identities.py` uses only exact Python integer arithmetic. It executes no uploaded/predecessor research program. It checks:

- 132,258 exact lane-index catalogue identities, including long-span boundaries;
- 21,844 exact symbolic DIT-to-DFT matrix entries at dyadic sizes through 128;
- all 197,952 responses of several complete small toy total tables;
- 1,696 exact packed-versus-scalar executions, including malformed toy codes;
- 32,766 incremental bit-reversal positions, with the less-than-2N flip bound.

All passed. The toy response maps deliberately use small rational real coefficients and a compact total alphabet so complete enumeration is feasible. They test layout and total-map agreement, not the theorem's transcendental approximation or quantitative floating error. The symbolic DFT control is exact and uses the relation -1=z^(N/2); it verifies the bit-reversal/sign convention independently of numerical trigonometry.

At the proof level, no missing packed-layout, catalogue-address, total-semantics, cold-preparation, normwise-error, or finite-size-fallback gate remains in the stated dyadic theorem. Remaining work is independent proof review, a full eager executor with implemented coefficient certificates, realistic cost studies, and a primary-source model-matched literature comparison before any novelty assertion. An all-length compiler needs its own independently charged composition proof; it is not included or presumed here.


## Appendix A. A uniform elementary polynomial-time coefficient routine

Let L=v+p+64. Every coarse-grid argument q/Q and the fallback root argument 1/N has O(L) bits. Compute each arctangent in Machin's identity using L terms of its alternating rational series. The pi enclosure has width less than 2^(-4L+6). Without fraction cancellation, the numerators and denominators have O(L^2) bits, because the sum of the term denominator bit lengths is O(L^2). Form the rational angle -2*pi_hat*q/Q, of magnitude below 7 and O(L^2)-bit rational description. Its certified uncertainty is less than 2^(-4L+10).

Evaluate sine and cosine using rational Taylor sums of degree at most 64L. A factorial remainder bound is much smaller than 2^(-4L): for m=64L, m!>=(m/2)^(m/2), hence 7^m/m!<=(98/m)^(m/2), and L>=64 supplies ample slack. Add the certified angle uncertainty using the Lipschitz bound for sine and cosine. This produces rational intervals with radius O(2^(-4L+10)), far smaller than every requested lattice spacing here, including the scalar fallback's K=p+v+20 guard precision.

Generate Taylor terms by multiplying by the rational angle and dividing by the next integer. Even without cancelling fractions, each term has O(L^3) bits; summing O(L) terms by numerator cross-multiplication uses O(L^4)-bit numerators and denominators. Grade-school integer addition, multiplication, division and comparison consequently give a fixed polynomial bit-time and scratch bound. Simulating them by ordinary RAM steps preserves a fixed polynomial bound; the budgeted implementation counts all these steps and all storage slots.

Choose each interval midpoint, then round that rational to the nearest desired dyadic grid using integer division. For the coarse grid, request interval width at most one quarter of the u/1024 grid spacing; component error is then strictly less than u/1024. For the fallback root, use grid spacing 2^(-K-4), giving complex error below 2^-K. No exact transcendental rounding-tie decision is required. The square-root constant uses floor(sqrt(floor(2^(2H)/2)))/2^H at H=p+10; integer binary search supplies the floor square root in polynomial time.

For a finite response, decoding P<=v states, evaluating dyadic butterflies on O(v+p)-bit integers, quantizing, and repacking also take a fixed polynomial amount of work per entry. Together these facts establish the fixed polynomial in (14) and therefore the uniform eventual-success bound (15). They do not assume a transcendental oracle or leave polynomial-bit work uncharged.

## Appendix B. Prior-art boundary

Chan, Jin, Vassilevska Williams and Xu, *Faster Algorithms for Text-to-Pattern Hamming Distances*, Appendix B, Lemmas B.6 and B.7, already describe compact FFT working-array representations, universal lookup tables across stages, and charged cold preprocessing: https://arxiv.org/html/2310.13174v2 . The packed-working-array mechanism must not be described as new here. The present proof question concerns its particular finite complex floating-state representation, all-input relative-l2 contract, dyadic coarse-phase catalogue, total semantics, and fully charged model. Establishing any novelty for that precise combination requires a model-matched literature comparison; none is asserted.

The bounded source comparison is recorded separately in `packed_fft_prior_art_1400/PRIOR_ART_AUDIT.md`. This manuscript does not transfer an integer-transform theorem to the complex relative-l2 setting by citation: Sections 2-8 prove the stated numerical and finite-word properties directly.
