# Independent review: cubic generator in the refined signed-bank space

23 October 2026. **SCOPED PASS. No author repair required.** This is a separate domain-and-space composition, not a silent extension of the old enlarged-envelope generator.

## Bound statement and scope

Accept the construction in candidate THEOREM.md, SHA-256 `6e550a85328df2b852014fb68fd856e303e047c403c8f57c99610aaf6447c690`, under precisely: odd N, d>=4, N>=6d-5, m=N-d, effectively represented coefficient field K, certified primitive Nth root q, char(K) not dividing N, and a supplied represented list of 2N distinct scalars. The output is a monic degree-m polynomial in the **refined** U, with nonzero constant, ordinary squarefreeness and full row rank of the actual original X_N.

The full deterministic coefficient stage has O(N^3) additions/multiplications, O(N^2) inversions and O(N^2) live field elements with schoolbook polynomial arithmetic. It matches the preceding expected cubic coefficient arithmetic and uses the already accepted 2(N-d)+2 bank count. It gives no further bank-count saving, new leading constant, root-finding improvement, total bit bound, end-to-end compiler gain, FFT speedup, practical advantage, owner closure or novelty clearance.

Crucially, E_ref retains both t^2 divisibility of the chirp numerator and the common formal-endpoint numerator constraint. Thus E_ref is smaller and U_ref is larger than the earlier unconstrained-envelope U. Earlier cubic acceptance did **not** itself establish this theorem. The review below reconstructs the interfaces for this exact new space. No frozen predecessor was modified.

## 1. Refined space, fixed divisors and endpoints

Only actual indices 0<=j<=m are divided by D(q^j); these denominators are units. At J=m+1, D(q^J)=0 and the condition is exclusively C_J P(rho^J)+R(q^J)=0. Eliminating the constant coefficient of R gives precisely 4d-10 spanning rows. The functional is nonzero on (0,1), so dim(U_ref)>=N-5d+11>=d+6. Modular half/quarter exponents are inverses modulo odd N, not divisions by 2 or 4 in K.

I checked the candidate's quoted interfaces against the accepted structural-endpoint theorem and independent review. The original Gaussian rows have the required t^2 factor, upper degrees and formal numerator cancellation, hence lie in E_ref. The accepted support proof uses the formal J equality and the t^2 factor together: after L_x and d constant factors, Q/t^2 has degree at most 4d-6 and N-2d distinct nonzero evaluation zeros. At N>=6d-5, that count is at least 4d-5. The variable-coefficient recurrence is not propagated backwards across a potentially zero factor; the later **constant** recurrence is used only after P=0. The derivative-functional exclusion likewise retains ordinary derivatives in every allowed characteristic. Sparse endpoint independence has its separate strict bound N-2d-1>4d-10.

Consequently the exact source contracts remain valid at this threshold over the algebraic closure: gcd(U_ref)=t-1, gcd(U_ref,0)=t(t-1), including multiplicities, and c0,c1,cm are jointly independent on U_ref. These imply gcd(V0)=gcd(V1)=1 for the actual quotient spaces V0=U_ref,0/[t(t-1)] and V1=U_ref/(t-1). V0 has independent constant and degree-(m-2) maps, namely -c1 and cm. No old-U dimension estimate, empirical rank saturation, perfectness or auxiliary squarefreeness is substituted.

## 2. Both deterministic selections and the reciprocal pencil

The reverse-gcd lemma is genuinely envelope-independent. At each unwind step, failed gcds are pairwise coprime and coprime to the retained divisor D, so D times their product divides A with full multiplicities. The sum of failed degrees is bounded by deg(A)-deg(D). Strict drops telescope and the optional one-time functional repair preserves phi exactly. Its v+2-element list and full arithmetic/inversion/storage contract therefore apply to the newly reconstructed spaces without altering the lemma.

For the first substitution, endpoint independence solves f0(0)=lead_r(f0)=1, r=m-2. The functional phi(f)=lead_r(f)-f(0) is nonzero on V0. The lemma returns f1 in the SAME scalar span V0, coprime to f0 and with phi(f1)!=0. There are no polynomial-coefficient combinations masquerading as vector-space membership.

For F_Z=f0+Zf1, coprimality proves irreducibility over K(Z). Constant and leading coefficients are not identically zero. A common factor with the padded reversal would force the two equal-degree polynomials to be scalar multiples. Reversal twice makes that scalar +1 or -1, with only 1 in characteristic two. The specialization at Z=0 and the nonzero endpoint determinant exclude both possibilities. Thus the reciprocal resultant is a nonzero polynomial of degree at most 2r. Including both endpoints gives degree at most 2r+2, so 2r+3=2m-1 scalar values suffice. The selected monic f has nonzero constant and gcd(f,rev_r f)=1. In particular f(1)!=0, because a root at 1 would be shared with the reversal. No squarefreeness of f is needed.

For the second substitution, h0=t f belongs to the actual V1 and is monic of degree n=m-1. With W the exact zero-leading slice, V1=K h0 direct-sum W. Therefore gcd(h0,W)=gcd(V1)=1 with multiplicities. Reverse selection within W gives h1 of degree below n, coprime to h0, necessarily h1(0)!=0. This proves the second pencil premises rather than assuming that an old-U h1 still belongs to the new space.

## 3. Ordinary generic separability, including characteristic two

The polynomial h_Z=h0+Z h1 is irreducible over K(Z) by the same primitive linear-pencil argument. Its ordinary t derivative is not the zero polynomial: the coefficient of t in h0 is f(0)!=0, so the relevant coefficient of h_Z' is a nonzero polynomial in Z. This works in characteristic two and over imperfect coefficient fields. Thus h_Z is separable over K(Z).

Since h0(1)=f(1)!=0, h_Z(1) is not identically zero. Consequently g_Z=(t-1)h_Z is generically squarefree, its monic discriminant is a nonzero polynomial in Z of degree at most 2m-2, and g_Z(0)=-Z h1(0) is nonzero of degree one. These are generic polynomial nonvanishing proofs; the algorithm still checks each accepted specialization by an ordinary gcd test. Neither inseparability nor a specialization at Z=0 is incorrectly declared legal.

## 4. Actual original-axis identity and all reciprocal-gcd cases

The original axis rows are (p_a,1,p_(-a mod N)), where p_a is the remainder of t^a modulo g. A relation polynomial A of degree below N therefore satisfies g|A, A(1)=0, and g|J_N A, with J_N A=t^N A(1/t)+A(0)(1-t^N). For g=(t-1)h and A=(t-1)h a, padded reversal b=rev_(d-1)(a) gives exactly

    J_N A=(t-1)[c b_(d-1) H_N - t (rev_n h)b].

The scalar block condition is already satisfied. This establishes the actual original-axis correspondence, not a substitute Hankel or reciprocal sufficient test.

Introducing a quotient q0 of degree below d yields the affine coefficient system t v b-c b_(d-1)H_N-h q0=0. The coefficient at degree N-1 cancels identically; its remaining N-1 rows and 2d columns give a matrix linear in h. A kernel vector with b=0 has q0=0. Thus its nullity is exactly the original-axis row defect, including c=0.

At h0=t f, the equation reduces to (rev_r f)b=f q0. Reciprocal coprimality forces f|b, and r>d-1 forces b=q0=0. Hence some actual 2d-row minor is nonzero at Z=0 and has Z-degree at most 2d. This is an auxiliary **zero-constant** polynomial witness; it is never used as a physical zero-node bank or required to pass the final guards.

For actual candidates with c!=0, t is a unit modulo h and c/t=-(h-c)/t modulo h. The complete gcd-locus criterion follows by dividing v b=-K0 H_N b_top modulo h by D0=gcd(h,v):

- If deg(h/D0)<d-1, h/D0 itself gives a relation with top coefficient zero.
- Otherwise a possible nonzero relation has top coefficient one. Since gcd(K0,h)=1, the necessary divisibility is exactly D0|H_N, with full multiplicities.
- When divisibility holds, all solutions are b0 plus multiples of h/D0. At equal degree a unique monic lift exists; above degree d-1, a relation exists precisely when b0 already has that exact degree and is monic.

This derivation uses only actual h,N,d and survives the changed envelope. It does not reject nontrivial reciprocal gcds or assume tested points are generic. Extended Euclid, quotients and remainders have degree O(N), so the test is quadratic, not a hidden dense axis solve.

Multiplying the selected affine minor, nonzero constant and ordinary discriminant gives a nonzero polynomial of degree at most 2d+1+2m-2=2N-1. Therefore the supplied 2N scalars contain a fully legal point. The exact axis test can accept additional points where this particular minor vanishes without compromising soundness.

## 5. Every threshold and complete cost

At N>=6d-5,d>=4, the key margins are N-2d-1>=4d-6>0, r>d-1, N-1>=2d, and 2m-2>N-1. The ordinary propagation and original physical reconstruction inequalities remain valid. The list consumers are r+2=m, n+2=m+1, 2r+3=2m-1 and 2N, all covered by the supplied list. Filtering zero leaves enough distinct nonzero candidates. There is no residual N>=6d-2 or N>=8d-10 premise.

Dense construction of the exact constrained envelope, quotient spaces, endpoint solve and zero-leading slice is cubic arithmetic, linear pivot inversions and quadratic storage. Each reverse-gcd selection is cubic arithmetic and quadratic inversions, including basis scans, every failed trial, coefficient construction and the single optional repair. Each pencil has O(N) trials, with quadratic ordinary gcd/extended-Euclid work and O(N) inversions per trial. Streaming the candidates avoids cubic storage. No symbolic resultant, discriminant, axis minor or dense axis matrix is computed by the claimed runtime algorithm. Dense matrices in the controls are verification costs only.

The result is coefficient-field arithmetic, not a total bit or setup bound. The represented list and integer/field interface remain paid. Finite quadratic coefficient-field setup retains the separate O(Q^3) base-field bill. A degree-two coefficient extension is not a splitting field. The source's genuine splitting extension, actual root recovery, all raw weights/amplitudes, post-root preparations and literal cubic warm bank schedule are preserved and are not absorbed into the coefficient-stage improvement. Direct dense Fourier evaluation is already quadratic in the base field, so no end-to-end speedup is implied.

## 6. Independent controls and provenance

The fresh control driver reconstructs E_ref by eliminating the formal numerator constraint, computes its actual U/V0/V1 spaces, runs both selections and both pencils, and checks the literal original Gaussian rows at each selected output. It independently computes the dense original axis and a specific 2d-square auxiliary minor. No author or historical scientific program was executed or imported.

Field/polynomial arithmetic, the already independently tested reverse-selection routine, and the exact axis helper were deliberately reused from earlier **reviewer-owned** files. Their exact source paths and hashes are bound in BINDINGS.json. This is disclosed helper reuse, not mislabeled new authorship or author-control independence. The new envelope construction, nine full generator fixtures, original-row checks and composition assertions are fresh. Existing generic reverse/gcd-locus stress proofs and controls remain pinned dependencies rather than being endlessly repeated.

The normal and Python -O runs are byte-identical: 66,396 active assertions, including guarded arithmetic and 126 literal original Gaussian-row checks. The 18 composition selection calls need no failed trial or functional repair; those mechanisms are covered by the separately accepted generic reverse-selection proof and stress controls, not newly claimed here. All nine fixtures lie strictly below N>=6d-2: (N,d)=(19,4),(21,4),(25,5),(27,5),(31,6),(33,6),(39,7),(51,9),(63,11). The last two use characteristic-two fields of sizes 256 and 4096, with composite root orders 51 and 63. Every final g is explicitly outside old unconstrained U, satisfies the exact refined equations and literal original Gaussian recurrence rows, is monic/nonzero-constant/ordinary-squarefree, and has dense original-axis rank N. The auxiliary zero-constant witness, full affine matrix identity and nonzero specific minor are checked separately. Complete counts and coefficients are in CONTROL.json. No splitting field, actual root set, physical bank array or bank application was constructed.

All eight candidate manifest members and all 17 selected source bindings were independently hash/length checked. Source use is the exact new-space support theorem, the generic reverse-selection lemma, the actual axis algebra and their scoped reviews, not a broad historical audit.

## Disposition

Accept this separate refined-U deterministic cubic coefficient generator at N>=6d-5. Keep all predecessor packets independently scoped and unchanged. Preserve the original field/list, splitting, physical, warm-cost and attribution qualifications. No further bank reduction or FFT claim follows.
