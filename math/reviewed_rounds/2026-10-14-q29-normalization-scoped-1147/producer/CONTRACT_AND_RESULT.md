# Q29 exact carry-basis conversion and guarded normalization

Date: 2026-10-14 UTC. Producer result, with separately produced byte-comparison evidence.

## Result and strict scope

The accepted R843 coefficient file has been converted exactly from the canonical z power basis to the canonical alpha/pi carry-ring basis. It then yields all 200 raw coefficients of U1687(-1-v;q) through v^199, modulo pi^200, and the entire shared-center normalized polynomial

    F(Y) = pi^(-60) U1687(-1-pi Y;q)

modulo pi^140. The numerator has exact coefficientwise content valuation 60. Every division passed its divisibility guard and multiplication-back check. The chosen root, sign, coordinate order and carry relation are fixed explicitly below.

The 360,000-byte canonical F output agrees byte-for-byte with a separately authored review computation. Its SHA-256 is

    fb09f4ff9f535a864adf3f24ebe00593b3d604777110d08728625a0992c9bc19.

That equality is comparison evidence; this producer report does not issue the independent reviewer's verdict. No discriminant value or nonvanishing, terminal repeated-branch result, all-primary-center coverage, asymptotic claim, FFT comparison, novelty claim, or external publication is made.

## 1. Exact inputs and root conventions

The accepted input is R843(w;z) modulo (25,Phi3375(z),w^100), with 180,000 canonical byte residues and SHA-256

    ebf51150ffbed6e87f3e08875451176963670801c59ffd9128336a02c43ca38c.

Its offset 1800*k+e is the coefficient of w^k z^e. The source SHA-256 is checked before execution. The independent full-kernel acceptance, earlier ring/precision contracts, all small reference inputs and all old raw arrays are bound in INPUT_BINDINGS.json.

Keep q=z as the coefficient root. The polynomial variable is x, not z. Fix

    alpha=z^1000, beta=z^2376, pi=beta-1, z=alpha*beta.

The exact coefficient ring is

    B2=(Z/25Z)[alpha,pi]/(alpha^18+alpha^9+1,f(pi)),
    f(T)=Phi125(1+T)=sum(r=0..4)(1+T)^(25r).

It identifies with the local integer ring modulo pi^200. The degree-100 monic f is Eisenstein and v_pi(5)=100. In the stored array the coefficient of alpha^a*pi^b is at 18*b+a, where 0<=a<18 and 0<=b<100. A jet coefficient of variable degree j starts at 1800*j. Coordinates are integer residues in 0,...,24; no characteristic-5 replacement is made above its valid threshold.

The full mod-25 relation is retained:

    pi^100=-5(1+2pi^25+2pi^50+pi^75+4pi^80+3pi^85+3pi^90+4pi^95).

The valuation of a nonzero canonical vector c is min(b+100*v5(c[b,a])); zero gives only the lower bound 200. This follows because the powers pi^b have distinct valuations modulo 100 and the alpha basis is an unramified integral basis. These are the already accepted local-ring conventions, now used on the accepted large output.

## 2. Integral conversion and its inverse

For each z^e, write z^e=alpha^(e mod27)*beta^(e mod125). Reduce alpha^a with alpha^18=-alpha^9-1, and reduce beta^b for b>=100 using

    beta^b=-beta^(b-25)-beta^(b-50)-beta^(b-75)-beta^(b-100).

Then substitute beta^b=(1+pi)^b with ordinary integer binomial coefficients reduced modulo 25. This gives the forward map. For its inverse substitute pi^j=(beta-1)^j, then alpha^a*beta^b=z^((1000a+2376b) mod3375), reduced by the monic Phi3375 polynomial. Both maps have integral coefficients; neither loses any precision.

The new source independently builds monomial z remainders by multiplication by z followed by direct monic reduction. It does not import a producer shift table or any predecessor code. All 1800 input basis vectors pass a forward/backward round trip. Each of the 100 full R coefficients also passes an exact byte round trip. The separately authored reviewer instead expands (1+pi)^e and reduces f directly without the alpha/beta intermediate; all full converted R bytes agree.

All scalar accumulators are signed int. Before canonical reduction, forward beta conversion is bounded by 100*24*24=57,600 per coordinate; the raw-U sum by 100*24*24=57,600; the alpha/beta scatter by the coarse bound 1800*24*8=345,600. These are well below signed 32-bit range. Pi multiplication and division use smaller mod-25 representatives. No uint8 intermediate arithmetic is used.

## 3. Exact raw-U transfer and the discarded tail

The integral reciprocal identity, before any quotient-ring arithmetic, is

    U1687(x;q)=sum(k=0..843) r[k](q) x^(843-k)(1+x)^(2k).

Putting x=-1-v gives

    U1687(-1-v;q)=sum(k=0..843)(-1)^(843+k)r[k](q)v^(2k)(1+v)^(843-k).

Every discarded k>=100 summand begins at v^200. Thus the accepted w<100 coefficients determine exactly the raw v<200 jet J, with

    U1687(-1-v;q)-J(v) in (pi^200,v^200).

The implementation evaluates this transfer with ordinary mod-25 Pascal coefficients, retaining j<200. It does not apply characteristic-5 Frobenius. The sign is the fixed convention U=-H/v at x=-1-v.

All available prior shared-center raw arrays were compared as inert data: the recovered primary array, the independent reciprocal array, and the independent normalization-review array. Every one of their 180,000 coordinates agrees with J reduced modulo 5, including zero coordinates. These three comparisons overlap; they are not 540,000 distinct coefficients. The canonical raw reduction SHA-256 for each comparison is in CONTROLS.json. Other primary centers were not compared or reconstructed from this jet.

## 4. Content proof and guarded quotient

Write J(v)=sum(j=0..199)u[j]v^j. In B2, the fresh calculation checks that v_pi(u[j])+j>=60 for each j and finds equality. The coefficients at degrees 10,30,50 attain it. For j>=200, integrality alone gives substituted valuation at least j>=200. Errors in the retained coefficients have valuation at least 200+j. Hence the exact full numerator U1687(-1-piY;q), not only its representative, is integral and divisible coefficientwise by pi^60. Its content valuation is exactly 60.

For x=sum c[j]pi^j, one division by pi is allowed precisely when every alpha coordinate of c[0] is divisible by 5. Using canonical residues, set

    d[99]=-c[0]/5,
    d[j-1]=c[j]+f[j]*d[99] for 1<=j<=99.

Then pi*d=x in B2. The source verifies this equality after every single guarded division. A quotient of an input known modulo pi^P is known modulo pi^(P-1); the full-capacity array does not override this loss.

Two routes were materialized and compared:

1. Form every numerator coefficient pi^j*u[j] in B2, then divide each 60 times. This performs 12,000 guards and multiply-back checks, yielding F modulo pi^140.
2. For j<60, divide u[j] only 60-j times. For j>=60, multiply u[j] by pi^(j-60). This performs 1,830 additional guards and multiply-back checks and retains stronger coefficientwise precision where justified.

Their canonical reductions modulo pi^140 agree for all 360,000 byte coordinates. A unit divided by pi is explicitly rejected. Additional fresh controls check pi^i valuations through i=200 and quotient recovery for exponents 1,25,60,99,100,125,199.

The common uniform error is

    min(200,200)-60=140.

This is sufficient and sharp for the supplied truncated information. Altering R by w^100 leaves all accepted bytes unchanged, preserves the top monic coefficient, and changes F by

    -pi^140 Y^200(1+piY)^743.

Its Y^200 coefficient has valuation exactly 140, first visible modulo pi^141. Thus neither a larger-capacity representative nor this basis conversion licenses uniform precision 141.

## 5. Exactly which jets and precision are recoverable

The materialized outputs certify:

- R coefficients w^0 through w^99 in B2; the rest remain absent.
- Raw U(-1-v) coefficients v^0 through v^199 in B2, each with coefficient precision 200. This is a jet modulo (pi^200,v^200), not an all-degree raw polynomial.
- The entire scaled numerator U(-1-piY) modulo pi^200; coefficients of degree >=200 vanish at this uniform precision by integrality.
- The entire F(Y) modulo pi^140; omitted coefficients of degree >=200 vanish at this uniform precision after division by pi^60.
- For retained 0<=j<200, a sharper coefficientwise class F_j modulo pi^(140+j). When j<60 this is represented by guarded division. When j>=60 it is represented without further information loss by the factored pair pi^(j-60) times the stored raw u[j] modulo pi^200. The materialized B2 version is truncated to precision min(200,140+j), as recorded in R843_precision.csv. It must not be read beyond that precision. For j>=200 only the generic bound v_pi(F_j)>=j-60 follows from these data, not a determined coefficient.

For any integral center c and integer b>=0, substitution Y=c+pi^b Z preserves the uniform precision 140. These data therefore recover translated shared-center F jets at the chosen integer centers 0,1,2,3,4, and at other explicitly specified integral centers, modulo pi^140. Each later certified division by pi^h lowers this to 140-h. Such translated jets were not materialized in this run. Integer centers and Teichmuller centers are distinct above the pi^100 boundary and cannot be silently exchanged.

More generally a scale v=pi^s Y gives the sufficient uniform bound min(200,200s)-h after a justified integral normalization pi^-h, using an explicitly constructed extension when s is fractional. This is a transfer bound, not a performed branch computation. A sharper coefficientwise or branch bound needs its own proof.

At the other primary centers x=-alpha^ell, with ell=1,...,26, w=(1+x)^2/x has nonzero residue and hence is a unit. The omitted w^100 term can then affect constant coefficients at valuation zero. The present w-adic truncation therefore does not reconstruct those primary-center jets. Similar first polygons or an integer translation within the shared Y disk do not establish all-primary-center symmetry.

## 6. Residue consistency

The reconstructed F residue is exactly

    A Y^10 (Y^4-1)^10,

where A in the alpha power basis is

    (1,1,0,4,4,1,2,3,2,3,0,0,4,2,2,3,2,1).

Only Y degrees 10,30,50 occur, with coefficients A,3A,A. This reproduces the previously accepted nonzero content witness. The previously accepted selected raw Newton vertices (0,75),(10,50),(50,10),(60,1),(62,0) are reproduced. No new terminal residual factor or derivative-unit assertion follows; the displayed residue remains inseparable.

## 7. Fresh controls, execution order, and resources

Only newly authored convert.cpp, run.py and check_outputs.py were compiled or executed. The predecessor programs and historical Q16 uploads were neither imported nor run. References were read as inert bytes. There were no network requests or external writes.

Before the full run, the controller pinned the input hash, compiled the fresh source, ran all 1800 basis round trips, nilpotence/valuation/guard controls, produced fresh converted small cases m=0,...,8 at q=z and q=z^1001, and measured a small m=192,w<48 conversion. The controller admitted the full computation only after the recorded estimate fit both remaining budgets. After the full run, an independently formulated exact Gaussian-binomial construction and integral odd-factor division checked every one of the 18 small U arrays, and all full legacy-coordinate/residue controls passed. The ordering is intentional and recorded; the independent small Gaussian comparison is a post-run verification, whereas basis and division controls precede admission.

The exact small Gaussian checks use new Python code and direct binomial expansion with f reduction, distinct from the production alpha/beta route and reciprocal transfer. They are implementation-diverse checks by this producer; separate reviewer authorship is recorded only for the independent full comparison.

Admission estimate: 10.72470976 seconds for both wall and charged CPU; available at admission 178.479171853 wall and 118.474524 CPU seconds. The estimate is heuristic with an eightfold cushion, not a timing theorem. Runtime limits were 180 wall seconds, 120 charged-CPU admission seconds and 512 MiB per-process address space.

Observed full executable interval: 0.395888682 seconds including launch; internal initialization, conversion, verification, normalization and writing: 0.391295 seconds. The entire compilation/control/admission/full/post-check workflow took 2.224801522 wall seconds and 2.229561 charged parent-plus-child CPU seconds. Peak child RSS was 108,084 KiB, including compilation; parent peak RSS was 10,752 KiB. There were no compiler failures or test failures. Times are finite machine observations; per-process address-space limits and child maximum RSS are not an aggregate cgroup-memory guarantee.

EXECUTION_RECEIPT.json contains all subprocess commands, their return codes and timings, bounds, output hashes and counts. Full input/output sizes are recorded in the manifest. The three independently produced R, U and uniform-F arrays agree in all 900,000 bytes; INDEPENDENT_BYTE_COMPARISON.json binds the exact paths and hashes.

## 8. Output decoding and reproduction

All .bin outputs consist solely of canonical unsigned one-byte residues, in jet-degree-major, pi-degree-next, alpha-degree-minor order:

    offset = 1800*jet_degree + 18*pi_degree + alpha_degree.

R843_R_ap.bin is 180,000 bytes. Each U, numerator, uniform F and coefficientwise F file is 360,000 bytes. The modulo-pi^140 canonical representative uses modulus 25 on pi degrees 0,...,39 and modulus 5 on pi degrees 40,...,99. The coefficientwise file uses the staggered modulus appropriate to each precision in its CSV.

Run python3 run.py from this directory to rebuild and reproduce against the bound sibling inputs. Timing JSON changes between runs; scientific output bytes must not. The reusable archive also contains the accepted full input, all small input arrays and the three historical comparison arrays under inputs/, with a portable reproduction option described in README.txt. The manifest hashes every delivered payload file without self-reference.

The next mathematical gate is a separately scoped continuation of repeated branches with explicit center lifts, variable scales, guards and remaining precision. This successful shared-center lift does not determine Disc R843 or the other 26 primary-center contributions.
