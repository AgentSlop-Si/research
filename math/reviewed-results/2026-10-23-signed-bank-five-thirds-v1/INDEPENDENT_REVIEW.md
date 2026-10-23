# Independent scientific review: first-order signed-bank support improvement

23 October 2026 UTC. Verdict: ACCEPT the original-bank representation bound, with the exact field, grammar and cost limits below. No author or historical scientific program was imported or executed, and no external state was changed.

## 1. Accepted delta, not a renamed old bound

For odd N, d>=4, N>=6d-2, and a field k containing a supplied primitive Nth root q with characteristic not dividing N, the literal negative unnormalized Fourier matrix is a sum of at most 2(N-d)+2 original individual signed phase-weighted resolvent banks over a genuine algebraic splitting extension. The same-sign groups use the distinct nonzero roots of one degree-m polynomial, m=N-d; both cross-sign singleton nodes are 1; every beta is 1. Raw weights may vanish. No derivative atom, zero-node bank, trace-bank replacement, new generator, product of banks or external endpoint map is counted.

Thus d=floor((N+2)/6) gives at most 2N-2floor((N+2)/6)+2=5N/3+O(1) banks for every odd N>=23. The accepted baseline is N>=8d-10, with 7N/4+O(1). This is an actual improvement to the sufficient count in the unchanged original bank dictionary, not an invented subclass, unchanged asymptotic statement, or restatement of the coefficient-field extension theorem.

It is not a matching lower bound, minimum, support classification, base-field attainment, historical novelty certification, whole-owner closure, or faster FFT. The actual literal schedule remains cubic in field operations and can use an enormous splitting field. For finite k=F_Q, coefficients may lie in F_(Q^2), but the physical roots still require a genuine splitting extension of degree at most m! over that coefficient field. For infinite k, coefficients may lie in k, not necessarily all roots.

## 2. Baseline and original-model scope

I read the accepted all-characteristic theorem, its operation ledger, and its independent review as inert text, checked the used assertions and their prior range, and compared every changed range requirement. The original enlarged envelope, whole-left Gaussian row identity, generic separability argument, auxiliary zero-node axis degeneration, and literal bank reconstruction remain inherited. They are not credited as new here. Their accepted source hashes are included in BINDINGS.json.

The envelope is exactly E={(C_j P(rho^j)+R(q^j))/D(q^j)}_(j=0)^m, with D(z)=product_(r=2)^(d-1)(1-q^r z), deg P<=3d-7, deg R<=d-2, rho=q^(2^-1 mod N), and C_j=q^((4^-1 mod N)j^2). Exponent halves/quarters are modulo odd N, not coefficient-field division by two or four. Every D(q^j) is nonzero on this interval. The Gaussian row identity places all actual recurrence windows in E; the new proof does not replace them by a smaller artificial row family or assume rank saturation.

There are at most 4d-7 generators, so dim U>=N-5d+8>=d+6 for U=E^perp. The old stronger estimate 3d-2 is correctly removed. Joint sparse-functional independence, not this dimension estimate alone, supplies the coefficient guards.

## 3. Independently derived first-order improvement

The exact consecutive-factor identity is

(1-q^2 z)D(qz)=(1-q^d z)D(z).

Consequently L_x y(j)=(1-q^(j+2))y(j+1)-x(1-q^(j+d))y(j) annihilates x^j D(q^j). It sends an ordinary R(q^j) of degree at most d-2 to an ordinary polynomial of degree at most d-1. Applied to a chirp it gives C_j Phi_x(P)(rho^j), where

Phi_x(P)(t)=q^h t(1-q^2t^2)P(rho t)-x(1-q^dt^2)P(t).

For a nonzero degree-a polynomial P, the first summand has unique degree a+3 coefficient -q^(h+2)rho^a lead(P); the second has degree at most a+2. Therefore Phi_x is injective and raises degree exactly three in every admissible characteristic, including two. No cancellation of that highest coefficient is possible.

The constant operator M_+=product_(r=0)^(d-1)(S-q^r), of order d, kills the ordinary image. Each factor sends a chirp polynomial to q^h tP(rho t)-q^r P(t), gaining exactly one degree and remaining injective. Thus a nonzero surviving chirp after M_+ L_x has degree at most 4d-4.

An equality known for j=1,...,m remains valid after these forward operators for j=1,...,m-d-1. There are exactly N-2d-1 distinct rho-points. Under N>=6d-2, this is at least 4d-3, strictly greater than the degree bound; the degree itself is below N. Hence the transformed polynomial is zero, and injectivity forces P=0. This is the changed proof step that improves the bank constant.

For the ordinary derivative functional, L_1(jD(q^j))=(1-q^(j+d))D(q^j), an ordinary polynomial of degree d-1. It is not zero under L_1 alone, but M_+ kills it. The same strict degree/zero count therefore forces P=0 for this target too. The calculation uses (j+1)-j=1 in the field and is valid in small characteristic.

Crucially, the variable coefficients of L_x do vanish at some residue positions. No such coefficient is inverted and L_x is never used for recurrence propagation. Its only uses are an exact polynomial cancellation and a finite forward-interval calculation.

## 4. Fixed divisors and all retained range obligations

The old sparse-support argument uses the order-(d-1) ordinary annihilator. From support {0,1,m}, it gives N-2d-1 zeros for degree at most 4d-8; its weaker requirement N>=6d-6 is satisfied. Thus delta_0,delta_1,delta_m are jointly independent modulo E. In particular c_0,c_1,c_m are independent on U, and c_1,c_m remain independent on U_0={c_0=0}.

For a fixed nonzero root x of U_0, duality gives an envelope agreeing with x^jD(q^j) for j=1,...,m. The new cancellation first gives P=0. Only then use the old constant recurrence product_(r=0)^(d-2)(S-q^r)(S-xq^r), whose order is 2d-2 and whose leading and constant coefficients are nonzero. Since m>=2d-2, the known zero interval propagates in both directions. Positions 0 and N give x^N=1. For x=q^s, comparing coefficients modulo z^N-1 identifies R with z^sD. The nonzero two endpoint coefficients, together with 2(d-2)<N, force s=0.

For the derivative target after P=0, the constant operator M^2 propagates R(q^j)-jD(q^j). It kills j q^(rj) in every characteristic. Positions 0 and N would give 0=ND(1), impossible because the characteristic does not divide N. Endpoint independence handles the zero multiplicity. Hence gcd(U_0)=t(t-1) and gcd(U)=t-1, including multiplicities, also over an algebraic closure.

The source's generic guard arguments remain valid in this larger d range. The universal residual polynomial for U/(t-1) is irreducible because a parameter-degree-zero factor would divide every member of a gcd-one space. Its derivative is nonzero because the residual linear coefficient is the nonzero functional -c_0-c_1. Irreducibility plus nonzero derivative proves generic separability; merely having a linear coefficient would not suffice for arbitrary specialized polynomials.

For U_0/[t(t-1)], independent endpoint functionals exclude a universal reversal eigenvector. Generic reciprocal coprimality follows. The auxiliary g_0=t(t-1)f is used only to establish a nonzero quotient-axis minor, never as a legal physical bank. A row-dependence polynomial A would be divisible by t(t-1)f rev(f), of degree 2m-2>N-1. Thus it is zero. This inequality requires N>2d+1, which the new range satisfies. Nonzero endpoints and reciprocal coprimality also imply f(1) is nonzero, so the needed factors are coprime.

The constant, discriminant and axis-minor guards lie on the same nonempty irreducible monic affine slice. Their nonzero product supplies a legal g. The relevant moment count b<=(N-1)/2<=m and the disjoint axis-row ranges N>2d also remain valid. None of these steps reuses an inequality tied specifically to 8d-10.

## 5. Field and literal-bank completion

The unchanged remainder-degree bounds give axis-minor degree at most d(d+1); the total simultaneous guard degree is H=d(d+1)+2m-1. The new range still gives d<=N/4 and N>=23. Therefore H<Q^2/2 whenever F_Q contains q, since Q>=N+1. A quadratic coefficient extension suffices for finite fields, with exact uniform rejection probability below one half. This is not a deterministic two-trial guarantee, nor a splitting-field assertion.

A squarefree degree-m polynomial has splitting degree at most m!. In finite fields the actual degree is the lcm of factor degrees; the enormous field F_(Q^(2m!)) is a sufficient paid overfield, not a claimed minimal or polynomial-degree extension. The compositum argument for arbitrary positive-characteristic input fields is unchanged.

Actual distinct nonzero roots give the original consecutive-power Vandermonde solves. The whole-left recurrence fills positive rows, the right moments fill their remaining supported intervals, reflection supplies negative rows, and the full quotient-axis rank supplies b=0. All sector assignments are disjoint. The original Gaussian factors used in divisions are nonzero on their supported triangles.

For each physical bank beta=1 and Delta=-alpha^N is nonzero. The primitive-root quantum-binomial identity gives the literal two-sided inverse as the finite geometric sum divided by Delta. Finite character inversion of all raw weights then recovers every Weyl coefficient of the negative unnormalized Fourier matrix. Thus the conclusion is an equality of original banks, not merely recurrence feasibility, moment matching, or a residual surrogate. The two cross banks are effective; ineffective same-sign banks may be omitted, hence an at-most count.

## 6. Cost audit

The revised ledger charges supplied-field and root-order requirements, quadratic-field search, envelope preparation, every failed coefficient test, splitting-overfield construction and root enumeration, amplitudes, raw weights, inversions, all output coordinates, storage and addressing. The field search is intentionally astronomical; no free factoring or root oracle is inserted.

With t=m!, the stated exhaustive splitting construction and schoolbook L/E arithmetic bounds are valid. Post-root preparation remains O(N^3) in the genuine root field with O(N^2) stored field elements. A warm literal bank uses N multiplications for the input scaling, N(N-1) for branch recurrences, and N^2 for output weights, totaling 2N^2 multiplications and 2N^2-2N additions. Summing B banks gives 2BN^2 multiplications and 2BN^2-BN-N additions, exactly as stated. Input/output and extension-coordinate costs are not silently suppressed.

Reducing B changes this particular cubic schedule's leading multiplication upper bound from about (7/2)N^3 to (10/3)N^3, but no arithmetic-order improvement follows, and ordinary dense base-field Fourier evaluation is already quadratic. No practical FFT, numerical stability or unqualified bit-complexity result is accepted.

## 7. Fresh independent controls and frozen objects

I wrote fresh_controls.py directly from the mathematical definitions, without importing or executing author or historical scientific code. Normal and python -O outputs are byte-identical, with 31,713 explicit checks. Fixtures are N=23,d=4 over F47; N=35,d=6 over F71; N=47,d=8 over F283; and N=63,d=10 over F64 in characteristic two. The last three include new-range cases beyond the old sufficient threshold, and include composite N. Each finite field is checked through all nonzero inverses and each chosen q through its exact order.

Checks include the new operator on actual chirp-plus-ordinary sequences, its unique highest coefficient, both target annihilations, 3,144 actual original whole-left Gaussian row identities, all original envelope denominators, joint endpoint-functional independence, the derivative-functional exclusion, retention of the forced root 1, sampled non-one exclusions, and every changed range margin. A modified first-order coefficient is rejected; explicit zero coefficients are retained without division; losing the strict zero-count inequality is identified as invalid. These are bounded transcription/falsification controls, not a proof by finite sampling. I did not instantiate the huge splitting fields or claim a full physical-bank array was computed.

Accepted author THEOREM.md SHA-256: f45e740543fab9d42001cd3ee4cbc78bd2eacf266fed81b2362a47e3d5a5bb1e. Accepted OPERATION_LEDGER.md: abc2f7bedcd39c630069a3f2764bf81972690ca51c5fd086a1a151963bdb72bf. All six frozen author manifest members and the three accepted baseline bindings were independently hash-checked. No mathematical repair was needed in this frozen packet.

The new acceptance is exactly the improved original signed-bank count under the stated extension and cost conditions. Broader owners, unrestricted optimality, base-field minima, novelty and runtime improvements remain unclaimed.
