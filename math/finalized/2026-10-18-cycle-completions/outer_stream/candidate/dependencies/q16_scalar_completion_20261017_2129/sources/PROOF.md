# Candidate proof: exact incidences and finite coefficient preparation

## 1. Incidence equivalence, half-open endpoints and uniqueness

A row ell retains k iff k = floor(ell*M/N)+j (mod M) for some integer -h<=j<=h+1. Put r=ell+vN. Since floor(r*M/N)=floor(ell*M/N)+vM, there is such a lift with

    k-h-1 <= floor(r*M/N) <= k+h.

For integer endpoints this is equivalent to

    N*(k-h-1)/M <= r < N*(k+h+1)/M.

Integers in this half-open interval are exactly r0,...,r1-1 as specified. Its length is N*t/M < N, so two distinct integers in it cannot differ by a nonzero multiple of N. Reduction modulo N is therefore injective, and its image is precisely the retained rows for k. An interval of length x contains at most ceil(x) integers. This proves E_k<=ceil(N*t/M), without a duplicate-removal or retention-filter charge. Across distinct k the ordered pairs are different. For a fixed row the retained residues are t consecutive distinct residues since t<M, so at most t supported pairs enter that row.

This proof also identifies the boundary defect in replacing the upper ceiling by floor: a noninteger upper endpoint can contain its floor and would be dropped. Replacing the strict endpoint with a closed endpoint introduces an extra incidence when that endpoint is an integer. Negative lower endpoints require signed floor semantics.

## 2. Elementary analytic bounds

For an integer j>=0, |D_j(u)|<=2j+1 by the triangle inequality for its defining exponential sum. Thus

    |F|=|D_L(u)/M| <= (M/2+1)/M < 1,
    |R|=|D_q(u)/(2q+1)| <= 1.

The kernel identity D_j(u)=sin((2j+1)*pi*u)/sin(pi*u) holds when u is nonintegral and has exact limiting value 2j+1 at integral u. Integer-order D_j is one-periodic. We use these elementary identities; the centered interpolation identity and Schur-tail bound remain inherited P05 premises and are not reproved by this component.

For 0<n_u<Q, the distance of n_u/Q to an integer is >=1/Q. Concavity of sine on [0,pi/2] gives b=sin(pi*n_u/Q)>=2/Q. Because 4N<=M<8N, Q=NM<=M^2/4. Also sqrt(M/N)<sqrt(8)<3.

## 3. Explicit scalar recurrence and fixed bit budget

The recurrence below was checked against the pinned Scalar source as inert text, not imported or run. Its mathematical enclosure argument is reconstructed here rather than inferred from an earlier test receipt. The source-specific future wrapper still needs independent review.

Let U=2^K, n=K+8. Enclose atan(1/v), v=5,239, with exactly n terms of

    sum_{j=0}^{n-1} (-1)^j / ((2j+1)*v^(2j+1)),

rounding each rational term outward to the K-grid and adding the alternating next-term remainder on its correct side. Each rounded term has width at most delta, and the next-term magnitude is less than delta because v>=5 and n=K+8. Each arctangent interval therefore has width at most (n+1)*delta. The Machin identity gives pi=16*atan(1/5)-4*atan(1/239), with total width at most 20(n+1)*delta. Its exact value lies between 31/10 and 16/5: the lower bound follows already from 16*(1/5-1/(3*5^3))-4/239>31/10, and the upper bound from atan(1/5)<1/5 and atan(1/239)>0. For K>=16, 20*(K+9)/2^K<=500/65536<1/100, since this expression decreases with K. Hence the returned endpoints are strictly between 3 and 4 as required.

For sin(pi*p/q), q>0, reduce p modulo 2q, fold exactly to [0,q/2] and retain the sign. Return exact 0 or +/-1 at the exact endpoints. Otherwise multiply the pi interval by the folded rational, round its endpoints outward, choose their K-grid midpoint x, and retain an integer radius enclosing the angle. Then 0<=x<=2. Starting T0=x, obtain each nonnegative Taylor term interval by

    Tj = outward_K(T_(j-1) * x^2 / ((2j)*(2j+1)))

for j=1,...,n-1. Add with alternating signs. The term multiplier is at most 2/3 and thereafter smaller. Each outward multiplication/division adds at most 2*delta to width, so induction gives term width <=6*delta and sum width <=6n*delta. Compute (2n+1)! by its fixed product loop and widen by ceil(U*2^(2n+1)/(2n+1)!)/U for the Taylor remainder. For n=K+8>=24, (2n+1)!>=n^(n+1)>=2^(4n+4)>2^(3n-7)=U*2^(2n+1), so that ceiling is at most one. The Taylor theorem is applied through degree 2n, whose even coefficient is zero; thus the stated remainder is valid despite the displayed polynomial having degree 2n-1.

The folded rational is at most 1/2. Its K-grid angle bracket has width at most 10(n+1)*delta+2*delta. Choose x by rounding the bracket's integer midpoint down. Twice its enclosing radius is at most the angle-bracket width plus delta. Widening the polynomial enclosure by that radius and the Taylor tail thus gives total width <=6n*delta+10(n+1)*delta+5*delta=(16n+15)*delta<=64(n+1)*delta. The radius handles the tiny downward midpoint rounding. Since the angle bracket endpoints lie in [0,2] on the K-grid, so does x. Sine is 1-Lipschitz; clipping to [-1,1] preserves its true value. These arguments establish the complete fixed-loop scalar enclosure without any tolerance-driven refinement or experimental extrapolation.

For completeness the selected K satisfies the needed inequality universally, not merely in tested ranges. Set b=bit_length(J+1), so J<=2^b-2. Then

    K+9=J+2b+25 <= 2^b+2b+23.

For b>=1, 2b+23<=25*2^(b-1), hence K+9<=14*2^b. Therefore

    64*(K+9) <=896*2^b <=2^(2b+16) =2^(K-J).

Thus every sine interval has width at most epsilon=2^(-J). K>=16 and K>=p follow directly. This recurrence/proof use the accepted generic rational-argument Scalar subroutine but do not execute its historical source or inherit acceptance for a new calling wrapper.

The integer square-root bisection in CONTRACT.md gives floor(sqrt(Z)) exactly after K+2 iterations. Since Z=floor(M*U^2/N), floor(sqrt(Z))=floor(U*sqrt(M/N)); the specified enclosure follows. No approximation to N, M or their ratio is used.

## 4. Ratio bound: why only two additional m bits are needed

This is the essential improvement over a loose generic quotient bound. Let f=a/(c*b) be the true normalized quotient, where c=M for F or c=2q+1 for R. In either case |f|<=1 and c>=1. The sine intervals contain a,b and have width <=epsilon. Every corner (a',b') therefore obeys |a'-a|,|b'-b|<=epsilon. Our J has epsilon<1/Q; hence b'>=b-epsilon>=b/2>=1/Q and division is safe. Then

    |a'/(c*b') - f|
      <= |a'-a|/(c*b') + |f|*|b-b'|/b'
      <= Q*epsilon*(1/c+1) <=2Q*epsilon.

All four corner values lie within 2Q*epsilon of f. Their min/max interval has width <=4Q*epsilon. Outward rounding adds at most 2delta, so both F and R have width

    w0 <= 4Q*epsilon + 2delta.

Clipping to [-1,1] preserves the true quotient and cannot increase width. At n_u=0 their exact dyadic intervals have zero width. Using the raw numerator bound alone inside a generic derivative estimate would waste another factor Q and would not justify the proposed J; the normalization bound is doing real work here.

## 5. Signed power, products, phase and complex rounding

For positive integer s, x^s is s-Lipschitz on [-1,1], by the derivative bound and the mean-value theorem. For odd s it is monotone, and for even s the minimum is at zero if included, otherwise at the smaller absolute endpoint. Thus the specified signed endpoint-power recurrence is a genuine enclosure and its width after outward rounding is at most s*w0+2delta. It is valid for negative and zero-crossing intervals. The compact-window even_power API alone cannot supply it.

For intervals A,B contained in [-a,a],[-b,b], respectively, the diameter of their product range is at most b*width(A)+a*width(B). This follows by writing xy-x'y'=y(x-x')+x'(y-y'). Outward grid rounding adds at most 2delta. Analytic clipping retains the target.

Consequently the F*R^s interval, clipped to [-1,1], has width <=(s+1)*w0+4delta. Multiplying by the sqrt interval, whose width is delta and endpoints are clipped to [0,3], gives an amplitude interval within [-3,3] with width

    <=3*(s+1)*w0+15delta.

Each phase interval has width <=epsilon and lies in [-1,1]. After one final product/rounding, each Cartesian coefficient interval has width

    wC <=3*(s+1)*w0 +3epsilon+17delta
       <=12*(s+1)*Q*epsilon +3epsilon +(6*(s+1)+17)*delta
       <=[3*(s+1)*M^2 +6s+26]*epsilon
       <=4*(s+1)*M^2*epsilon.

The last inequality uses M>=4 and s>=1: 6s+26 <=16(s+1) <=M^2(s+1). With c_s=ceil(log2(s+1)), our J gives

    wC <= 4*(s+1)*2^(2m-J) <= eta/64.

Nearest-even rounding of the interval midpoint to p=A+3 adds at most eta/16 to its distance from the midpoint. The midpoint is at distance at most wC/2 from any true Cartesian coordinate. Thus each Cartesian error is <=eta/128+eta/16=9eta/128, and the complex error is <=9sqrt(2)*eta/128<eta. The squared-radius integer certificate in the contract is therefore always satisfied in the valid-domain exact recurrence. It avoids conflating a Cartesian error with complex modulus.

All bounds include odd s and exact zero limits. They do not require a successful sparse-recovery event, input amplitudes, estimate values, or the outer scale exponent.

## 6. Universal finite arithmetic and preparation charge

Here D is fixed, s=Dm, and J,K,n=O_D(m). Every rational argument product has O(m+log(s+1)) bits. Pi arctangent denominators v^(2j+1)(2j+1) have O(K) bits. The Taylor factorial has O(K log(K+2)) bits, and other scalar arithmetic has no larger than this bound. The signed-power integers and their binary denominator have O(s*K) bits. Thus a common successful-domain maximum integer-width envelope is

    H = O(m + K*log(K+2) + s*K + log(s+1)) = O_D(m^2).

There are O(K) operations in fixed Machin/Taylor/factorial loops, O(K) in sqrt bisection, O(log(s+1)) in each square-and-multiply endpoint power, and a constant number of interval products, quotients, clipping and exact final certificate operations. A conservative count per coefficient plus amortized one-time setup is O(K+log(s+1)+m)=O_D(m). Euclidean division, multiplication and shifts on H-bit integers can be charged O(H^2) by the stated schoolbook model; comparisons/additions are smaller and may be overcharged the same. Therefore

    bit work = O((K+log(s+1)+m)*H^2) = O_D(m^5),
    cumulative produced integer bits = O((K+log(s+1)+m)*H) = O_D(m^3).

These are valid deliberately loose bounds, not an assumption that polynomial time means m^5. Square-and-multiply performs O(log s) multiplies but intermediate values up to s*K bits, which must be counted. Factorial width is not incorrectly called O(m). Shift allocation and certificate/loop counters are included; their logarithmic widths are absorbed by H. Peak live arithmetic scratch can be O_D(m^2) with streamed scalar terms, while retained output certificates cost O(E*K) bits and are separately paid. A ledger may conservatively charge cumulative storage rather than peak memory; the two must not be confused.

Header/support validation and enumeration use O(S+E+1) operations on O(m+log(s+1)) bits, hence O_D((S+E+1)*m^2) bit work. The +1 covers header preparation and validation even at S=E=0. The scalar setup is incurred only when E>0. If E=0 the outer stage terminates after validation/endpoints. No loop has N iterations except downstream accumulator/output work excluded from this component. With the inherited support bound E<=S*t, all auxiliary work remains (S+1)*poly_D(m), which is absorbed by the recovered theorem's fixed positive exponent slack. That all-length argument, dense fallback, exact accumulation/scale-back and independent amplification remain separate dependencies/gates.

## 7. A concrete odd-power witness and its exact limitation

Take D=5, m=57, M=2^57, N=M/4-1, s=285, and k=6s=1710, ell=0. This is a retained incidence because k<=h+1. Here q=floor(M/(8s)) and

    1 < (2q+1)*k/M < 2.

Thus the normalized D_q ratio is negative. Also (2L+1)*k/M=855+k/M lies in (855,856), so F is negative. Since s is odd and phase=1, the exact coefficient is positive. Replacing R^s by |R|^s gives a negative exact target. The current historical even_power rejects exponent 285 instead, a direct interface obstruction.

This sign witness must not be oversold: its high power makes the coefficient very small, and a sign discrepancy alone need not exceed eta at final rounding. The decisive rejection control is the odd-exponent API failure; independent signed-power interval checks expose the incorrect substitution at the operator level. This packet does not claim an eta-violating final-output counterexample for the absolute-power mutant.

The same metadata satisfy all sparse/outer guards at beta=1/8 (with any fixed 0<alpha<1/8). The no-array witness is theorem-parameter compatible, but does not execute a theorem-sized sparse front end or create a length-N output.
