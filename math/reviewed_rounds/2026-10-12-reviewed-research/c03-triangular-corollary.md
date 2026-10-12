Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: ab24054d4b3e819897a624632f79413dac4321556c8cf0f3e54d1cb712f92e07

---

Independent review of the C03 triangular corollary and source comparison
11 October 2026

Verdict

ACCEPT at the stated scope. The submitted triangular specialization, every-characteristic endpoint and multiplicity formulas, coefficient-only construction, and complete finite paired-pencil solution sets on a supplied certified cyclic subgroup are correct. The submitted arithmetic upper bounds are valid. No mathematical correction is required in the reviewed corollary.

The source comparison is accepted as a bounded comparison with explicit hypotheses. It establishes classical component antecedents, including the exact geometric-series trace recurrence, but does not establish an earlier printed match to the entire arbitrary-matrix C03 family or historical novelty. Treat this as a reviewed extension of C03/Q17. NEW-06 remains a view of the same result, not a separate discovery. No new candidate row, discovery count or ranking promotion is warranted by this packet. The specific-priority and general sparse-recovery obligations remain open.

This review binds the exact submitted bytes in REVIEWED_INPUTS.json. The producer packet is frozen with its original 'independent review pending' language; this separate review supplies the subsequent acceptance. Original research programs and the producer's control script were neither imported nor executed. Only the fresh independent_controls.py in this review packet was executed. No external service was modified.

1 Exact result and normalization

Use m>=1, a commutative ring S with identity, and A,B triangular in the displayed coordinate order, with upper/lower choices independent. Write c=det(A)det(B), D(w)=diag(1,w,...,w^(m-1)), and keep the fixed formal degree-(m,m) resultant R of det(A-aDAD) and det(B-awDBD). The reviewed residual V is the one in the already accepted identity

R=w^v(w-1)^(m^2)w^b V(w+w^(-1)),
v=m(m-1)(4m+1)/6, b=m(m-1)(2m-1)/6.

Triangularity gives the scalar products det(A) product_i(1-a w^(2i)) and det(B) product_j(1-a w^(2j+1)). With the standard resultant order, Res_a(1-au,1-av)=v-u. Thus coefficient homogeneity and factor multiplicativity give

R=c^m product_(0<=i,j<m)(w^(2j+1)-w^(2i)).

This includes singular inputs because it is an integral polynomial identity, not an argument that cancels determinants or assumes actual degree m. In particular, a zero determinant makes one complete scalar pencil zero in this triangular subclass. This is not true for arbitrary singular, nontriangular A,B, and no such broader statement is approved.

There are m(m-1)/2 negative oriented differences (i>j). For every d from 0 to m-1 the absolute difference 2d+1 has multiplicity n_d=2m-2d-1, while the sum of all lower powers is v. Therefore

R=epsilon c^m w^v product_d(w^(2d+1)-1)^n_d,
epsilon=(-1)^(m(m-1)/2).

The n_d sum to m^2 and sum d n_d=b. For C_0=1, C_1=x+1, C_d=x C_(d-1)-C_(d-2), induction in the Laurent ring gives

sum_(k=0)^(2d) w^k=w^d C_d(w+w^(-1)).

Consequently V=epsilon c^m product_(d=1)^(m-1) C_d(x)^n_d. The only cancellation is of monic polynomial factors and Laurent units; this is valid in the presence of zero divisors. The trace substitution is injective on this bounded-degree space, seen from each distinct highest w-power. This proves the exact residual identity rather than merely its agreement at test points.

Every C_d is monic of degree d. Hence V=0 if and only if c^m=0, and otherwise V has degree exactly b even over a ring with zero divisors. The stronger field simplification V=0 iff c=0 is approved only over a field (or another explicitly justified reduced setting). The empty product gives m=1 correctly.

2 Endpoints and multiplicities in every characteristic

Recurrence gives C_d(2)=2d+1 and C_d(-2)=(-1)^d. Since b and m(m-1)/2 have the same parity, V(-2)=c^m with the reviewed sign convention. The stated product for V(2) follows immediately.

Assume a field and c!=0 for finite multiplicity claims. In characteristic zero each binomial w^(2d+1)-1 has a simple root at 1, so ord_1 R=m^2. In characteristic p, its exact multiplicity is h_p(2d+1), the largest p-power dividing 2d+1. Thus

ord_1 R=sum_d n_d h_p(2d+1),
mult_2 V=(sum_d n_d (h_p(2d+1)-1))/2.

The division by 2 is an integer count. The substitution x-2=(w-1)^2/w explains the factor of two without dividing by 2 in the field. For p=2 all odd exponents have h_p=1, the two endpoints coincide, and V(0)=c^m!=0. For odd p, base order holds precisely when p>2m-1: if p is smaller, d=(p-1)/2 provides a positive excess term.

The examples V=-x-1 for m=2 and V=-(x+1)^3(x^2+x-1) for m=3 are correct. In characteristic 3 the first has full residual degree but R=-w^3(w-1)^6. For every m>=3, C_1=x+1 occurs at least cubically in nonzero triangular V, proving failure of squarefreeness in every characteristic. These are exact countercontrols to unsupported implications from full degree; none weakens the accepted arbitrary-matrix identity.

3 Complete supplied-subgroup solutions

The approved input contract is an exact field, nonsingular triangular A,B, and an element zeta whose order N is supplied and certified. No algorithm for discovering, certifying or extending that field/root data is claimed. A field element of finite order N forces characteristic not to divide N.

For nonidentity w=zeta^k, a common root requires w^(2j+1-2i)=1 for some indices. All possible absolute differences are exactly 1,3,...,2m-1. Difference 1 produces only w=1. Therefore the nonidentity labels are exactly the union over 1<=d<m of the nonzero multiples rN/gcd(N,2d+1), with 1<=r<gcd(N,2d+1). This is elementary cyclic-group arithmetic and involves no discrete logarithm.

For each such w, let u_i=w^(2i) and v_j=w^(2j+1). The distinct common a-values are precisely u_i^(-1) for those u_i appearing among the v_j. Direct factor inspection proves both inclusion directions and includes repeated-factor situations. The identity endpoint contributes exactly a=1. Since w and both determinants are nonzero, each pencil has a nonzero degree-m coefficient and a nonzero constant, so neither a missing affine candidate nor an infinity root needs an additional gate under this contract.

This is complete recovery of the finite (w,a) solutions of these two equations in the supplied subgroup. It is not sparse-rational reconstruction from samples, global denominator certification, a full cyclic Fourier identity, or arbitrary-matrix recovery. Those distinctions are essential to the acceptance.

4 Cost audit

The coefficient construction uses O(m^2) operations for all C_d via the recurrence, with only O(m) coefficients held if streamed. Multiplying each repeated factor into the accumulator by ordinary convolution costs at most O(b^2+m^2), since the total multiplied degree is b. The live accumulator and recurrence use O(b+m) ring entries besides the input. Diagonal determinant products cost O(m); binary powering for c^m costs O(log(m+1)). The stated O(m^2) read/triangularity checks dominate input handling. No interpolation, extension, inverse or sampling node is needed for this coefficient-only construction.

For subgroup recovery, each gcd is at most 2d+1; the total number of pre-deduplication nonidentity labels is at most m(m-1). O(m) binary root powerings plus the consecutive subgroup powers cost O(m log(N+1)+m^2) field operations. Sorting O(m^2) integer labels requires O(m^2 log(m+1)) comparisons, with bit-index gcd and label work separately charged. Each complete u/v matching and a deduplication takes O(m^2) comparisons/field operations, for O(m^4+m log(N+1)) total. Candidate/label storage O(m^2) and solution storage O(m^3) are valid upper bounds; streaming still charges output writes. Add the separate coefficient cost if that output is requested. These are exact arithmetic bounds, not bit complexity, numerical stability, or an implementation performance claim.

5 Independent controls

All fresh controls passed:
- 40 sizes for signed exponent counts, valuation v and trace degree b
- All coefficients of the full pairwise product and trace reconstruction through m=10
- 192 literal padded Sylvester determinants at integer w, including 96 singular-input cases and 32 w=0 fixed-grade cases
- 6 complete symbolic padded Sylvester identities for independently chosen upper/lower triangular matrices
- 72 exact positive-characteristic endpoint/multiplicity cases using repeated polynomial division, with p in {2,3,5,7,11,13,17,19}
- 273 ring-with-zero-divisors coefficient cases modulo 4,6,8,9,12, including 40 with c nonzero and c^m zero
- 440 exhaustive subgroup solution cases across prime fields and F_4, F_8, F_16; 64 cases use characteristic-two extension fields
- 70,272 individual (w,a) tests of the two scalar pencil equations and 2,874 output solutions checked

The controls corroborate the all-size proof above. They are not a proof by exhaustive small examples. The fresh script uses standard SymPy only for literal determinant algebra; coefficient, trace, multiplicity and finite-field controls are independently implemented. The submitted script was not read to construct these controls and was not run.

6 Exact primary comparisons and limitations

Baker, Reciprocity via Reciprocants, Appendix B, Proposition B.1 and Remarks B.2-B.3, especially equations (13)-(14), explicitly gives the trace construction, initial geometric-series traces 1 and x+1, and the exact recurrence used here. Thus that component is a direct printed antecedent. Proposition 2.3 concerns reciprocal input polynomials and cannot replace the earlier proof that C03's residual becomes reciprocal.
https://arxiv.org/html/2309.02512v2#A2

Busé and Mourrain, Remark 2.1 (printed pp.3-4) and equation (2.2) (printed p.5), explicitly retain expected degrees and give homogeneous composition/covariance. These are the appropriate fixed-grade component antecedents. They do not print the full C03 diagonal-deformation result in the inspected passages.
https://arxiv.org/pdf/cs/0612050

García-Armas, Ghorpade and Ram, Proposition 3.4, gives the Barnett factorization using Laurent coefficients of v/u, with u monic and deg v<deg u. Its statement does not require coprimality. These Hankel data differ from C03's raw adjacent moments and divided-difference matrix.
https://arxiv.org/html/1011.1760#S3

Ćurgus and Dijksma, section 5, equation (12), gives padded nullity n-max(deg f,deg g)+deg gcd(f,g) and its infinity-root interpretation in the paper's complex-polynomial setting. This substantiates the degree-drop qualification, not an independent all-ring proof.
https://arxiv.org/pdf/1208.2385

Uteshev and Baravy, Theorem 6.2, equations (6.6)-(6.7), uses weighted ratio-sample moments. Its factors retain signs, leading coefficients and sampled denominators; sample numerator/denominator values are nonzero. The proof initially assumes simple roots and expressly removes that extra assumption by algebraic specialization. The report's distinctions are correct.
https://arxiv.org/html/1603.08752#S6

Grigoriev, Karpinski and Singer, MPI/90-10, section 2 Lemma 2 and section 3 Lemma 7, employs an Ore prime-dilation operator over real quasirational functions and adds distinct-real-root constraints. It is substantive sparse-rational antecedent literature, not the ordinary C03 scalar-pencil family or an all-field certification shortcut.
https://archive.mpim-bonn.mpg.de/id/eprint/2068/1/preprint_1990_10.pdf

Yang, Conjugacy Classes of Torsion in GL_n(Z), ELA 30 (2015), p.484, expressly identifies the determinant of T -> AT-TB with the characteristic-polynomial resultant. The transpose in its Kronecker matrix reflects vectorization; it does not reverse the checked resultant convention. Its integer-coprime cokernel conclusions should not be transferred to arbitrary singular ring data. It supplies a component antecedent, not an earliest-priority finding.
https://journals.uwyo.edu/index.php/ela/article/download/1561/1561/1561

All seven passages above were independently reopened as primary full-text extraction/HTML, with exact formulas and adjacent hypotheses inspected. PDF screenshots for MPI/90-10 and Yang failed because the screenshot tool did not accept the content type; no page-image audit is claimed. The more detailed Sturmfels, Nart and fast-evaluator comparisons remain inherited evidence and were not independently page-audited in this review.

7 Publication treatment

Append a dated independent-acceptance note to the live-verified C03/Q17/NEW-06 rows and prior-work record; preserve previous text, accepted P02/R15 and supplements, source identities, and historical distinctions. Replace 'review pending' only as a new dated status, rather than rewriting the submitted sealed packet. The correct current label is 'independently accepted elementary triangular specialization; bounded primary comparison complete; exact full-family priority unresolved'.

No new candidate identifier or separate NEW-06 count is justified. The base proof already printed the A=B=I pairwise product as a sharpness example. Extending its determinant scale to triangular inputs and expanding the residual/cyclic solutions is useful and now verified, but does not by itself satisfy a novelty threshold or the intended general-recovery application gate. Keep C03::specific-priority open. No generic sparse-recovery or asymptotic Fourier promotion is approved.
