Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery details are omitted; mathematical source identity, assumptions, costs and limitations are preserved. Original source-report SHA-256: 7cb68185e98e6e24696fcdfb8b348ab61aaac5bca7e16bbe116df9aed0458634.

# Independent review of the C03 general Bezoutian and Hankel bridge
12 October 2026

Verdict

ACCEPT the bridge and its bounded source comparison at the stated scope. No correction to C03, its structural supplement, its singular-safe supplied-node evaluator, or the submitted field-chart formulas is needed. The signed Bezoutian identity is universal at fixed homogeneous degree. The normalized Barnett construction is correct on its explicitly stated field chart. This review supplies an explicit localization clarification so that the chart is not incorrectly transferred to a general ring.

This closes the missing coefficient-level identification with a classical rational-function Hankel matrix. It does not close C03::specific-priority, demonstrate an earlier printed statement of the complete diagonal-pencil family, establish firstness, or produce a general sparse-reconstruction theorem. NEW-06 remains another view of C03. No new theorem count, ranking promotion, or correctness downgrade follows.

The input is C03_General_Hankel_Bezoutian_Priority_Bridge_CANDIDATE_2026-10-12.zip, SHA256 8b6b6e0db1df98414334aa40efd8de8f56db161e238cd5e5ce096aa961aa5a50. All 16 entries in its manifest were independently hashed and verified. Its executable was neither read to construct the controls nor imported or executed. Only the newly written independent_controls.py was run.

1 Fixed degree and exact Bezoutian sign

Fix m>=1 and a commutative ring S with identity. Let D=diag(1,w,...,w^(m-1)), f(a)=det(A-aDAD), and g(a)=det(B-awDBD). The resultant is always the degree-(m,m) Sylvester determinant, with both arrays padded through degree m. Its specialization must not be replaced by a resultant computed at the new actual degrees.

For arbitrary padded coefficients f_j,g_j define Z through

  (f(a)g(c)-f(c)g(a))/(a-c)=sum_(0<=i,j<m) Z_ij a^i c^j.

Exact polynomial division gives

  Z_ij=sum_(k=0..min(i,j)) (f_(i+j+1-k)g_k-f_k g_(i+j+1-k)),

where coefficients above m vanish. This agrees with the submitted indexing and source convention. Put epsilon_m=(-1)^(m(m-1)/2). Then

  Res_(m,m)(f,g)=epsilon_m det Z.                         (1)

Independent sign proof: for generic f with leading coefficient alpha and distinct roots r_i, the Vandermonde evaluation matrix W has entries r_i^j and WZW^t has diagonal entries f'(r_i)g(r_i). The product of derivatives is epsilon_m alpha^m det(W)^2. Hence det Z=epsilon_m alpha^m product_i g(r_i). Both sides of (1) are integer coefficient polynomials, so generic equality proves equality in the universal integer ring. Every ring specialization follows, including characteristic 2, zero divisors, vanished leading coefficients, one zero polynomial, and both zero polynomials.

The correct resultant convention matters already for m=1: for f=2a+1 and g=3, the padded degree-(1,1) resultant is 6, while the actual-degree resultant is 3. The fresh controls include this explicit negative control.

Combining (1) with the accepted C03 identity, without any new division, gives

  det Z=epsilon_m w^(v+b)(w-1)^(m^2)V(w+w^(-1)),
  v=m(m-1)(4m+1)/6, b=m(m-1)(2m-1)/6,
  v+b=m^2(m-1).

Z is the ordinary Bezoutian of the two scalar determinant polynomials. It is generally neither a raw input moment matrix nor the accepted m^2-square divided-difference matrix. The substitution is now explicit; simply saying that both constructions involve Hankel matrices would not have sufficed.

2 Barnett normalization and precise ring scope

On the submitted field chart w!=0 and det A!=0, set

  alpha=(-1)^m w^(m(m-1))det A,
  beta =(-1)^m w^(m^2)det B,
  u=f/alpha, h=g-beta u.

Then u is monic of formal and actual degree m; deg h<m, with h=0 allowed. Define c_k by the formal expansion h(a)/u(a)=sum_(k>=1)c_k a^(-k), and H_ij=c_(i+j+1). No root selection, convergence, coprimality, or assumption that h has degree m-1 is needed. If T=Bez_m(u,1), Barnett's identity is

  Bez_m(u,h)=THT.

The leading coefficient of u is 1, so T has antidiagonal 1 and zero entries beyond that antidiagonal. Therefore det T=epsilon_m and (det T)^2=1. Bilinearity and cancellation of the u,u term yield Z=alpha Bez_m(u,h). Consequently

  R=epsilon_m alpha^m det H.                             (2)

For w!=1, C03 and v+b=m^2(m-1) give exactly

  V(w+w^(-1))=(-1)^(m(m+1)/2)(det A)^m det H/(w-1)^(m^2). (3)

There is no omitted power of w, leading coefficient, or determinant. The parity reduction in (3) is correct.

Explicit arbitrary-ring clarification: the same construction and identities hold in

  S[(det A)^(-1)][w,w^(-1)].

Equivalently, at a fixed ring element w, both w and det A must be units. Merely requiring det A to be nonzero is insufficient over a ring with zero divisors or other nonunits. The field version in the candidate is correctly restricted; this note prevents an invalid all-ring reading. If det A is nilpotent, the localization can be the zero ring and supplies no information about an original nonzero ring. We do not descend identities through a possibly noninjective localization. The universal identity (1) and the accepted C03 identity are proved before specialization.

Barnett's identity extends to this ring chart without appealing to ranks or roots: expand the inverse of the monic reversed denominator as a formal power series, multiply out the divided-difference kernel, and compare coefficients. This uses additions and multiplications only after alpha has been made a unit.

The useful undivided version is

  (det A)^m det H=(-1)^(m(m+1)/2)(w-1)^(m^2)V(w+w^(-1)). (4)

Thus det H contains the forced endpoint factor in the Laurent ring. Multiplication by w-1 is injective there, even if S has zero divisors. The exact quotient can be formed symbolically and then specialized at w=1; a literal numerical 0/0 in (3) is not permitted. In particular the vanished determinant of H at w=1 is not the residual value V(2).

If only det B is nonzero over a field, reverse (f,g), use the B chart, and restore the factor (-1)^(m^2) from resultant swapping. If both matrix determinants vanish, both formal leading coefficients vanish and both constant coefficients vanish. The padded resultant is zero; neither normalized chart is available. This does not mean that one singular arbitrary matrix forces the resultant to be zero. The fresh symbolic example A=[[1,1],[1,1]], B=I has V=1 and a nonzero resultant.

3 Endpoint compatibility

The bridge preserves the accepted structural formulas. It supplies an alternative expression on an invertible chart, rather than a replacement for the division-free residual determinant.

With S_k(w)=(w^k-1)/(w-1) interpreted as a Laurent polynomial for every integer k, the residual matrix is

  N_((i,k),(j,l))=A_ij B_kl S_(1+k-i+l-j)(w).

Entrywise extraction from A tensor (wDBD)-(DAD) tensor B yields the exact factors w^(m^2(m-1))(w-1)^(m^2), and hence det N=V(w+w^(-1)). At w=1 the identity S_k(1)=k gives the tangent determinant and its fixed-degree resultant. At w=-1, S_k(-1) is 1 for odd k and 0 for even k, giving the two parity blocks. These endpoint evaluations are valid in arbitrary commutative rings. In characteristic 2 the two endpoints coincide; they cannot be treated as two independent tests.

The symbolic controls reconstruct V from the literal padded Sylvester determinant for seven arbitrary-matrix pairs, including singular inputs, the zero resultant, a constant nonzero V, a degree-one V vanishing at each endpoint in separate examples, and a nontriangular m=3 pair. They check the prescribed top coefficient, tangent determinant and tangent resultant, parity blocks, and five complete rational-function Hankel factor identities in symbolic w. They confirm the signs and endpoint factors without interpreting division at a specialized zero denominator.

4 Nullity and the exact recovery obstruction

Over any field, for a pair not both zero, write q=max(deg f,deg g) and d=deg gcd(f,g). Then

  nullity Bez_m(f,g)=nullity Syl_(m,m)(f,g)=m-q+d.         (5)

This is a field statement. The Sylvester kernel consists of pairs (-g/delta,f/delta)r, where delta is a gcd and deg r<m-q+d. The unpadded degree-q Bezoutian has nullity d; padding adds a zero block of size m-q. Both arguments use only polynomial arithmetic over a field and therefore remain valid in positive characteristic. They do not need complex roots. The printed Curgus-Dijksma theorem is formulated over C; the all-field extension here is justified by its algebraic proof, not falsely attributed to broader printed hypotheses.

If exactly one polynomial is zero, (5) gives nullity m for both matrices and is correct. If both are zero, Bezoutian nullity is m and Sylvester nullity is 2m; the candidate explicitly and correctly excludes this case from (5).

On a leading-coefficient chart q=m, Barnett congruence gives nullity H=d. For a nonzero field node w!=1 this identifies V(w+w^(-1))=0 with a common root over an algebraic closure. It does not provide a common root in the base field, and it does not imply an admissible sparse-rational reconstruction.

The submitted counterexample is exact. In F_3, set m=2, w=2=-1, A=B=[[1,1],[1,-1]]. Both determinants are 1 modulo 3. Direct calculation gives f=g=a^2+1. Its values at a=0,1,2 are respectively 1,2,2, so there is no base-field common root despite R=0. The structural residual is V=-4(x+2); at x=w+w^(-1)=1 it vanishes modulo 3. An extension-field/root computation or an appropriate usable-gcd condition remains necessary.

Even a base-field linear gcd supplies only a candidate a. It does not certify a legal grid, globally invertible denominator, complete cyclic identity, or reconstruction from data. The candidate correctly preserves these distinct obligations. Matrix determinant vanishing and gcd degree are also not an algebraic-geometric Jacobian/singular-locus classification of the parameter hypersurface.

5 Primary source comparison

The following theorem bodies and adjacent hypotheses were independently reopened, rather than relying on abstracts.

García-Armas, Ghorpade and Ram, arXiv:1011.1760v1, header dated 8 November 2010: Section 2 defines the exact Bezoutian convention; Proposition 2.2 is the full-degree field coprimality criterion. Lemma 3.2, Definition 3.3, and Proposition 3.4 give the rational-function expansion and Barnett congruence for all Padé pairs, including noncoprime pairs. Lemma 3.1 uses leading-term subtraction in the monic equal-degree setting. The candidate's rescaling/subtraction and determinant normalization are valid explicit substitutions. The dynamically rendered document date is not used as its historical publication date.
https://arxiv.org/html/1011.1760#S3

Curgus and Dijksma, arXiv:1208.2385v2: equations (6)-(9), pages 2-4, give the Bezoutian convention and Sylvester matrix connection. Section 5, equation (12), page 5, expressly gives the padded nullity and infinity-root contribution. Its coefficient field is C. The candidate distinguishes that printed scope from the independently justified universal determinant identity and all-field kernel statement.
https://arxiv.org/pdf/1208.2385

Baker, Reciprocity via Reciprocants, Appendix B, Proposition B.1 and Remark B.2: reciprocal trace representation is stated over a ring, and the recurrence C_0=2, C_1=x, C_(k+1)=xC_k-C_(k-1) is explicit. The fixed-grade extension with possible vanishing extreme coefficients follows directly from the coefficient argument. It does not divide by 2. Proposition 2.3 has reciprocal input hypotheses and must not be applied to the generally nonreciprocal a-polynomials merely because the eventual w-residual is reciprocal.
https://arxiv.org/html/2309.02512v2#A2

Busé and Mourrain, Explicit Factors of Some Iterated Resultants and Discriminants: Remark 2.1, pages 3-4, fixes expected degrees; equation (2.2), page 5, gives homogeneous composition over an arbitrary commutative ring. For two degree-m forms and a degree-one coordinate map, the resultant covariance exponent is m^2. The coordinate swap and collision substitution a=1+epsilon t, w=1+epsilon therefore have the precise weights used in C03. The cancellation establishing the collision factor is performed universally, not by dividing a zero divisor after specialization.
https://arxiv.org/pdf/cs/0612050

Sturmfels, On the Newton Polytope of the Resultant, Theorems 2.1 and 4.1, journal pages 213 and 220: primary extracted theorem text identifies generic initial monomials and general initial forms with mixed-decomposition data under essential-support hypotheses. The two univariate supports {0,...,m} satisfy the required essentiality. The C03 coefficient weights j(j-1) and j^2 give separated root slopes, hence no tie between the two root families. The source is a mechanism antecedent; the exact sign and closed principal-minor product remain justified by the accepted explicit telescoping calculation. Formula artwork was not independently image-audited: screenshot calls did not yield usable image content here, and direct PDF retrieval returned HTTP 403. No stronger page-image claim is made.
https://www.maths.tcd.ie/EMIS/journals/JACO/Volume3_2/m4496732732u7744.fulltext.pdf

Conrad, Universal Identities II, Theorem A.1, page 5: the primary full-text theorem identifies a Kronecker difference determinant with a characteristic-polynomial resultant over commutative rings. Generic invertibility and polynomial specialization yield the submitted generalized-pencil form. Its entrywise factorization then recovers N and the accepted endpoints. This is an undated exposition checkpoint, not evidence of the first historical occurrence.
https://kconrad.math.uconn.edu/blurbs/linmultialg/univid2old.pdf

No verdict relies on the body of Barnett's 1971 article, Barnett's 1972 note, Helmke-Fuhrmann's survey, Wimmer's history, or Jouanolou's original treatise: those bodies were not inspected in this independent pass. Bibliographic mention cannot close their exact-family priority comparison.

6 Which claims are classical and what remains open

The signed fixed-degree Bezoutian determinant, normalized rational-function Hankel congruence, field gcd/nullity criterion with infinity contribution, reciprocal trace recurrence, fixed-degree covariance, operator determinant identity, and weighted initial-form mechanism all have established classical antecedents. The bridge now gives the missing exact coefficient map for arbitrary C03 matrices. Thus determinant-zero/gcd and trace components should not remain advertised as unresolved conceptual novelty.

The node quotient w -> w+w^(-1) identifies exactly w and w^(-1) over a field because equality factors as (w-z)(wz-1)=0. For a supplied certified subgroup of order N there are (N+gcd(2,N))/2 quotient values. Excluding w=1 removes one value. This elementary orbit count does not find or certify the subgroup, does not make enough nodes exist, and does not remove interpolation or extension costs. The fresh controls cover prime-field subgroups, including characteristic 2.

What remains unresolved is the exact earlier printing or priority of the complete evaluated arbitrary-matrix package: the two specific diagonal deformations, closed v and b, prescribed signed principal-minor coefficient, division-free residual determinant and endpoint formulas, all at fixed homogeneous degree with specialization guards. The fact that its mechanisms are classical does not prove that this entire statement was previously printed. Conversely, failing to locate that full statement does not prove novelty or firstness.

A consequential general sparse-reconstruction application remains open independently. Nothing here upgrades a per-node O(m^3) evaluator into full O(m^3) coefficient or root recovery, supplies b+1 legal quotient nodes, proves general squarefreeness or irreducibility, or establishes an asymptotic Fourier improvement.

7 Distinction from the accepted triangular corollary

The frozen earlier independent review accepts the triangular specialization with independently upper/lower triangular A and B, explicit geometric-series trace factors, endpoint multiplicities, and complete paired-pencil solutions on a supplied certified cyclic subgroup. Its scalar product simplification uses triangularity, and a zero matrix determinant annihilates the entire corresponding pencil there.

This new bridge does not assume triangularity. It constructs a Bezoutian and a normalized Hankel matrix from the coefficients of the two general determinant polynomials. It closes a previously missing comparison step, but does not import the triangular closed factorization, coefficient-only construction, or subgroup solution algorithm into arbitrary matrices. The two accepted results must remain distinguishable in existing records. Neither creates a separate NEW-06 discovery.

8 Independent controls and scope

FRESH_RESULTS.json gives exact counts, seed, symbolic inputs, outputs and runtime. The original candidate checker was inert. The new controls use literal padded Sylvester matrices and exact bivariate divided-difference Bezoutians, rather than copying the candidate's coefficient routine. They include integer and composite-ring identities, small-characteristic nullity with the both-zero exception, full Barnett matrix congruences, general matrix substitutions, swapped charts, symbolic endpoint factors, the finite-field recovery counterexample, and quotient-node counts. These controls corroborate the proofs; they do not establish an all-size theorem or historical priority by examples.

Accepted conclusion:

  Independently accepted general C03 Bezoutian/Barnett-Hankel bridge. Exact signs, fixed-degree drops, field charts and arbitrary-ring localization checked. Determinant-zero/gcd and reciprocal-trace components have explicit classical reductions. Accepted C03/P02/R15, structural supplement and evaluator correctness are unchanged. This is distinct from the accepted triangular corollary. Exact full-family printed priority and general sparse reconstruction remain open; NEW-06 remains the same result view. No new discovery count or ranking change.

C03::specific-priority remains open. The exact full-family printed statement and general sparse reconstruction are unresolved, while the explicitly identified classical mechanisms retain their prior-work credit. Accepted mathematics and the distinct triangular corollary remain unchanged.
