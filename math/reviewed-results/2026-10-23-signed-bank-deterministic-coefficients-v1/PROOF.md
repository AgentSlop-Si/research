# Fast original-axis testing in the improved signed-bank range

23 October 2026 UTC. Separate domain-composition candidate. No frozen theorem, review, bank dictionary, or accepted packet is relabeled or modified. Independent scoped acceptance is required before publication.

## 1. Exact result and sources

Let N be odd, d>=4, N>=6d-2, and m=N-d. The coefficient field K contains a supplied primitive Nth root q and has characteristic not dividing N. Use exactly the original E, U=E^perp, U0, and ordinary coefficient pairing from the accepted new-range pencil addendum. The defining denominator and envelope ranges are unchanged:

    D(z)=product_(i=2)^(d-1)(1-q^i z),
    rho=q^(2^-1 mod N), C_j=q^((4^-1 mod N)j^2),
    E={((C_j P(rho^j)+R(q^j))/D(q^j))_(j=0)^m:
       deg P<=3d-7, deg R<=d-2}.

Given an explicitly represented list of 2N distinct elements of K, the same two-pencil generator, with the accepted exact reciprocal-gcd axis test, returns a monic degree-m g in this SAME U with g(0)!=0, gcd(g,g')=1, and full row rank of the ORIGINAL X_N(g). Its complete deterministic coefficient stage costs O(N^4) field additions/multiplications, O(N^3) inversions, and O(N^2) live field elements. Every failed scalar trial and both coprime-combination loops are included.

This composes two separately accepted, byte-pinned inputs:

- The improved-range pencil addendum `signed_bank_pencil_new_range_addendum_20261023_v1/ADDENDUM.md`, SHA-256 da880d924870bc312dd8eff5ce57c5937104f1ffc7174dc191a4ddb458e190be, with independent acceptance in `signed_bank_pencil_new_range_independent_20261023`. It supplies the required exact original-U facts and constructs the actual two pencils on N>=6d-2, but its accepted coefficient bound was O(N^5).
- The fast-axis theorem `signed_bank_fast_axis_guard_20261023_v1/THEOREM.md`, SHA-256 54a19739c708ea5d0e38e9fd18408ff7bf50ccfb5849f800ece67ac9829959dc, and its independent review SHA-256 6e10976c19f56b2480b4dc278e4e2250db4caacb4c4d1fa299890acb595fd863. Its original acceptance scope was only N>=8d-10. The extension of THAT result is proved here, not inferred from the old pencil's compatibility.

SOURCE_PINS.json records the manifests, all bound members, accepted verdicts, and unchanged first-order physical-bank ledger. All were verified as inert files. No author/historical scientific program was imported or executed.

## 2. Inherited objects on the new domain

The accepted improved-range addendum and its first-order sources establish, on N>=6d-2 and after algebraic closure,

    gcd(U)=t-1, gcd(U0)=t(t-1),
    c0,c1,cm jointly independent on U.

All D(q^j) are nonzero, and this U implies every required original whole-left recurrence. No smaller coefficient class is introduced. The available dimension bound is dim U>=N-5d+8>=d+6, not the old 3d-2 bound; only the O(N) upper dimension is used in operation counts.

Set n=m-1 and r=m-2. The first pencil constructs an actual monic f of degree r in V0=U0/[t(t-1)] with f(0)!=0 and gcd(f,rev_r f)=1. The second constructs

    h0=t f,
    W={h in U/(t-1): coefficient_n(h)=0},
    h1 in W, gcd(h0,h1)=1,
    h_Z=h0+Z h1, g_Z=(t-1)h_Z.

In particular h1(0)!=0, every h_Z is monic of degree n, and every g_Z belongs to the original monic degree-m slice of U. The accepted separability argument remains valid in characteristic two: h_Z is irreducible over K(Z), its derivative has nonzero constant coefficient as a polynomial in Z because h0'=f+t f' has constant f(0)!=0, and h0(1)=f(1)!=0. Thus the degree-m discriminant is not identically zero. These are supplied proved facts, not assumptions inferred from finite controls.

## 3. Exact axis reduction and complete gcd locus

For any such monic h, a row relation on the ORIGINAL axis matrix corresponds exactly to nonzero b with deg b<=d-1 and

    t v b = c b_(d-1) H_N (mod h),
    v=rev_n(h), c=h(0), H_N=1+t+...+t^(N-1).             (1)

This follows directly from A=(t-1)h a, b=rev_(d-1)a, and the cyclic reversal formula

    J_N A=(t-1)[c b_(d-1)H_N-t v b].

The identities n+(d-1)=N-2 and n+d=N-1 hold exactly, independently of a support-range inequality. The condition A(1)=0 is automatic. Thus this equivalence requires no old N>=8d-10 premise and includes c=0 and repeated factors.

For a legal candidate c!=0, set K0=(h-c)/t, D0=gcd(h,v), hbar=h/D0, vbar=v/D0, and ell=deg hbar. To avoid confusing the fixed envelope polynomial D(z) with this gcd, this addendum names the latter D0. The original nonzero-constant guard gives gcd(K0,h)=1 and makes (1) equivalent to

    v b = -K0 H_N b_(d-1) (mod h).

The accepted complete decision is therefore unchanged:

- ell<=d-2: a nonzero homogeneous relation b=hbar exists, so rank drops.
- ell>=d-1 and D0 does not divide H_N: no normalized relation exists, so the axis has full row rank.
- Otherwise compute b0=[vbar^(-1)(-K0(H_N/D0))] mod hbar. If ell=d-1, b0+hbar is a relation. If ell>d-1, rank drops exactly when b0 is monic of degree d-1.

All multiplicities are retained. No reciprocal-gcd locus is excluded. The inverse exists because gcd(hbar,vbar)=1. The original fast routine is never invoked at c=0; the division-free matrix below covers the auxiliary witness. The only degree comparison used in the reciprocal-coprime subcase is n>d-1, checked explicitly in Section 5.

## 4. The new affine minor proof, checked on the larger domain

Write (1) without division:

    t rev_n(h)b - c b_(d-1)H_N - h u = 0.

The degree-(N-1) coefficient cancels identically, since it is c b_(d-1) in each of the first two terms. The remaining degree is at most N-2, and h is monic of degree n, so deg u<=d-1. Thus the coefficient map in (b,u), both of degree less than d, is an (N-1)-by-2d matrix M(h). Every entry is linear in h and hence affine in Z. A kernel vector with b=0 also has u=0. Full column rank of M(h) is exactly full row rank of the ORIGINAL X_N((t-1)h), also at c=0.

At the actual second-pencil base point h0=t f, its equation cancels a factor t and becomes

    rev_r(f)b = f u.

The supplied reciprocal coprimality forces f|b. The new domain still has r>d-1, so b=u=0. Hence M(h0) has full column rank, with enough rows as independently checked below. Some 2d-row minor is nonzero there, and its restriction to the pencil is a nonzero polynomial of degree at most 2d.

The optional safe reciprocal continuation also survives: rev_n(h0)=rev_r(f) has constant 1, so gcd(h0,rev_n(h0))=1. The residue [-K0 H_N rev_n(h)^(-1)] mod h at Z=0 equals -f because f(H_N-rev_r f) is divisible by t f. This uses only their common constant 1. No inverse of t is taken at the singular boundary. The coefficient of degree n-1 is -1, nonzero in characteristic two. The primary minor proof needs no resultant exclusion or rational continuation.

Multiplying the degree-2d minor, the nonzero linear constant guard, and the nonzero monic degree-m discriminant gives the complete degree bound

    H_fast=2d+1+(2m-2)=2N-1.

Therefore 2N distinct scalars guarantee a successful final candidate on this new domain. Every candidate is tested by its actual nonzero constant, ordinary squarefreeness, and exact all-gcd-locus axis criterion, not by a genericity assumption or a smaller bank matrix.

## 5. Complete new-domain inequality and list audit

From N>=6d-2, d>=4, and N odd, N>=23. The fast-axis proof uses precisely these size statements:

- Matrix row margin: (N-1)-2d=N-2d-1>=4d-3>0, so the 2d-column minors exist.
- Auxiliary degree margin: r-(d-1)=N-2d-1>=4d-3>0, so f|b forces b=0.
- Coprime residue margin: n-(d-1)=N-2d>=4d-2>0, so the inverse residue uniqueness argument retains the needed degree separation.
- The inherited original-X witness also has (2m-2)-(N-1)=N-2d-1>0; its original proof remains valid.
- All h, reversed polynomials, gcds and Euclidean operands have degree O(N), and the largest product K0 H_N has degree at most n+N-2=O(N). No matrix dimension or operand degree grows as a hidden function of the old gate.

The common scalar list is now 2N elements, not the previous H+1 list. Check every earlier construction separately:

- First coprime-combination loop: a=f0 has maximum degree r, and preserving its nonzero endpoint functional requires at most r+2=m=N-d<2N distinct values per direction.
- Second loop: a=h0 has degree n and needs at most n+1=m=N-d<2N values per direction. Every basis member of W has degree at most n-1.
- Reciprocal pencil: at most 2r+3=2m-1=2N-2d-1<2N tests suffice, including its endpoint guards.
- Final pencil: H_fast+1=2N values suffice.

The supplied finite-field representation is unchanged. If the base is F_Q containing q then Q>=N+1, so the same E0=F_(Q^2) has more than 2N elements. Its O(Q^3) preparation remains separately paid. Enumerating the shorter list costs O(N) field-element writes plus representation/counter costs. In characteristic zero the usual integers supply the list; arbitrary positive-characteristic infinite fields still require the effective distinct-element interface. None of this treats field construction or bit growth as free.

## 6. Whole cost and physical-bank boundary

All basis dimensions remain O(N), with the full original spaces retained. Dense envelope/nullspace preparation is O(N^3). Each of the TWO coprime-combination loops has O(N) directions and O(N) scalar trials per direction, with degree-O(N) Euclid costing O(N^2) arithmetic and O(N) inversions per trial. These loops still dominate the coefficient stage at O(N^4) arithmetic and O(N^3) inversions. The reciprocal pencil and the final 2N-trial stage each cost O(N^3) arithmetic and O(N^2) inversions. Streamed candidates and the envelope data require O(N^2) live elements. All failures, reads, writes, candidate formation, gcds, reductions, and final coefficient output are included.

This replaces only the coefficient-selection part of the accepted first-order physical-bank ledger, SHA-256 abc2f7bedcd39c630069a3f2764bf81972690ca51c5fd086a1a151963bdb72bf. Genuine splitting-field construction and actual root recovery remain fully charged, including the enormous finite m!-overfield recipe if used. Vandermonde moments, axis amplitudes, raw weights, original branch denominators/inverses, every output coordinate, storage, and base-coordinate expansion remain unchanged. Literal application is still 2BN^2 multiplications and 2BN^2-BN-N additions, B<=2m+2, over the actual root field.

Choosing d=floor((N+2)/6) uses the already accepted 5N/3+O(1) bank count with the improved deterministic coefficient stage; it is not a new bank-count result. The pre-existing expected O(N^3) Las Vegas coefficient bound is not improved. No end-to-end polynomial-time compiler, efficient root field, FFT speedup, historical novelty, or broader-owner closure is asserted.

## 7. Fresh controls strictly outside the old scope

The separate standalone `fresh_controls.py` specializes arithmetic helpers authored during the current fast-axis task, without importing or executing any accepted/historical scientific program. It reconstructs the ORIGINAL E/U and both pencils rather than relabeling old outputs. Its checks remain active under Python optimization; normal and optimized outputs are byte-identical.

Every fixture satisfies 6d-2<=N<8d-10:

- N29,d5 over F233, primitive q=2: 58 dense-X/affine-M comparisons and 57 complete fast tests.
- N35,d6 over F211, primitive q=5: 70 dense/affine comparisons and 69 fast tests; odd composite N, including a nontrivial reciprocal-gcd specialization.
- N51,d8 over GF(2^8), represented by x^8+x^4+x^3+x^2+1, primitive q=3: 102 dense/affine comparisons and 101 fast tests; characteristic two and composite N, also including a nontrivial reciprocal-gcd specialization.
- N63,d10 over GF(2^12), represented by x^12+x^6+x^4+x+1, primitive q=131: 126 dense/affine comparisons and 125 fast tests; characteristic two and composite N. The program verifies the 64-element Frobenius-fixed subfield containing q, so this is an actual quadratic coefficient field over an input field containing the required root.

In total the new-range fixtures compare 356 ORIGINAL dense axis matrices with the affine matrix and perform 352 exact fast tests. Every candidate in every 2N-element list is checked for original-U membership, nonzero constant, squarefreeness, and actual axis rank. Each zero-constant witness also passes its original dense rank comparison and safe continuation check. The entire spaces' fixed-divisor and endpoint properties, operand-degree bounds and field/root representation are verified in the controls. No root-bank arrays or huge splitting field are constructed.

The run records 937,507 explicit checks, including 163,515 small integer parameter pairs with odd N<2000 for the displayed inequalities. These finite checks are transcription evidence, not the uniform proof. All four fixtures happen to pass the final guards at scalar 1; this is not a two-trial guarantee. The all-parameter result is supplied by Sections 2–6.
