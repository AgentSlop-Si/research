Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, limitations and review method are retained. Original source-report SHA-256: 45ac3ba533bb3573b98a164f428ddb2fc5b682a1513cdd7ea251b93cb05540c7.

Review date: 12 October 2026 UTC.

Independent review of degree eleven Rogers Szego overlap

ACCEPT October 2026 UTC

**Decision.** Accept the frozen candidate for all integer sizes $A\ge1$ and all odd orders $25\le d\le89$. The residue-field proof at $d=25$ is valid uniformly in $A$; the exact conjugate witnesses at $d=27$ cover complementary size ranges; and every odd $29\le d\le89$ has an exact outer-annulus witness. No mathematical repair is needed. With the precisely identified inherited results, this completes the degree-eleven family. The higher-degree overlap and ordinary residual gaps remain open.

# 1 Exact scope and original normalization

Let $k$ be any characteristic-zero field and let $q\in k$ have exact odd order $d>11$. Use the original definitions $$H_{11}(z;q)=\sum_{j=0}^{11}{11\brack j}_qz^j=(z+1)U(z),\qquad g=U(-1)=H'_{11}(-1),$$ $$W=\frac{(q;q)_{11}}{(q^2;q^2)_{(d+11)/2}},\qquad
 \tau=\frac{dW}{g},\qquad J_{A+1}(x;\tau)=x\operatorname{He}_A(x)-A\tau\operatorname{He}_{A-1}(x).$$ Here $(a;q)_n=\prod_{j=0}^{n-1}(1-aq^j)$ and $\operatorname{He}_0=1$, $\operatorname{He}_1=x$, $\operatorname{He}_{n+1}=x\operatorname{He}_n-n\operatorname{He}_{n-1}$. The freshly accepted statement is $$\boxed{\quad 25\le d\le89\text{ odd},\quad A\in\mathbb Z_{\ge1}
 \quad\Longrightarrow\quad \operatorname{Disc}_x J_{A+1}(x;\tau)\ne0.\quad}$$ Monicity makes nonzero discriminant equivalent to absence of a multiple root. This is the overlap discriminant, not the ordinary discriminant of $U$.

Set $h=(d-1)/2$, $E=(q^2;q^2)_h$, $s_j=(q;q^2)_j/(q^2;q^2)_j$, and $S_r=\sum_{j=0}^r s_j$. The imported identities $g=(q^2;q^2)_5S_5$, $W=(q^2;q^2)_5/E$, and $ES_h=d$ give $\tau=S_h/S_5=d/(ES_5)$. All product lengths are below $d$ and $q^2$ has exact order $d$. The accepted sector proof gives $S_5\ne0$ and nonreal $\tau$ in every primitive complex embedding.

The independent computation reconstructs $H_{11}$ from $$\prod_{j=0}^{10}(1+q^jz)
 =\sum_{j=0}^{11}q^{j(j-1)/2}{11\brack j}_qz^j.$$ It then differentiates at $-1$ and evaluates the *uncancelled* original $W$. This checks the parameter itself, including its sign, the factor $d$, and the Hermite normalization, at $d=25$ and at every interval witness.

**Frozen input.** The candidate ZIP is 10,517,391 bytes, with SHA-256

<div class="center">

`e0ecd3e0fb869f10f64a2f2598e46c86b4c905da303cd61c2fa76141cc510688`.

</div>

Its 33 entries pass CRC, safe-path and byte-identity checks against the immutable package. All 32 manifest-listed payloads and all seven source pins are verified.

# 2 The uniform local criterion

**Verified lemma.** Suppose $K$ is a number field, $\mathfrak p$ lies above $3$, and $\tau\in K$ is integral at $\mathfrak p$. If $\bar\tau\notin\mathbb F_3$, then $J_{A+1}(x;\tau)$ is squarefree for every integer $A\ge1$.

At zero, the exact parity evaluations of the Hermite polynomials imply that a multiple root requires $\tau=0$ when $A$ is odd, or $\tau=-1/A$ when $A$ is even. The first has prime-field residue. In the second case, $3\mid A$ makes $-1/A$ nonintegral at $\mathfrak p$; if $3\nmid A$, its residue is in $\mathbb F_3$. Both are excluded.

For a nonzero multiple root $x$, consecutive Hermite polynomials cannot vanish together: their recurrence in characteristic zero descends to $\operatorname{He}_0=1$. Since $A\tau x\ne0$, the equation $J=0$ therefore forces both $\operatorname{He}_A(x)$ and $\operatorname{He}_{A-1}(x)$ to be nonzero. Differentiating and using the recurrence gives $$J'=(1+A\tau)\operatorname{He}_A+Ax(1-\tau)\operatorname{He}_{A-1}.$$ The two common-root equations imply $$x^2=\frac{\tau(A\tau+1)}{\tau-1}=y.$$ Every division is justified: $\tau\ne0,1$, $x\ne0$, and the two Hermite values are nonzero. Since $A$ has residue in $\mathbb F_3$ whereas $\bar\tau$ does not, $\tau$, $\tau-1$, and $A\tau+1$ are local units in every residue class of $A$. Thus $y$ is a unit.

Extend the local valuation to the number field $K(x)$. The equations $x^2=y$ and $(x^{-1})^2=y^{-1}$ show that $x$ and $x^{-1}$ are integral there. Hence $\bar x$ exists and is nonzero, and reduction of $J=J'=0$ is legitimate. The residue extension cannot turn the nonzero elements already identified into zero.

For every $t\ge0$, the recurrence modulo $3$ proves by induction in blocks of three that $$\operatorname{He}_{3t}=x^{3t},\qquad \operatorname{He}_{3t+1}=x^{3t+1},\qquad
 \operatorname{He}_{3t+2}=x^{3t}(x^2-1).$$ In the next block the recurrence coefficients are $0,1,2$, and the last step gives the next factor $x^3$. Writing $A=3t+r$ gives $$\bar J=x^{3t}P_r(x),\qquad \overline{J'}=x^{3t}P'_r(x),$$ $$P_0=x,\qquad P_1=x^2-\bar\tau,\qquad
 P_2=x^3-(1+2\bar\tau)x.$$ For $r=0$, $P_0(\bar x)\ne0$. For $r=1$, $P'_1(\bar x)=2\bar x\ne0$. For $r=2$, $P'_2=\bar\tau-1\ne0$. These exhaust all integers $A\ge1$ and contradict a reduced common root. The proof does not assume that the full reduction of $J$ is squarefree: its power of $x$ can be large, but the characteristic-zero multiple root has been proved to reduce to a unit.

Finite checks through index 60 corroborate the recurrence identity. The induction, unit argument and residue-class exhaustion provide the all-$A$ proof; those finite checks are not used as an extrapolation.

# 3 Exact order twenty five reconstruction

Use $K=\mathbb Q(\zeta_{25})$ and $$f(X)=\Phi_{25}(X)=X^{20}+X^{15}+X^{10}+X^5+1.$$ The checker independently verifies $X^{3^{20}}=X$ modulo $f$, and the supplied *unreduced* polynomial Bezout identities showing $$\gcd(f,X^{3^4}-X)=\gcd(f,X^{3^{10}}-X)=1
 \quad\text{over }\mathbb F_3.$$ Since $4=20/5$ and $10=20/2$, these are the complete Rabin irreducibility conditions. Equivalently, $3$ has exact multiplicative order $20$ modulo $25$. The quotient is the field $\mathbb F_{3^{20}}$; the class $Q$ has order $25$, checked by $Q^{25}=1$ and $Q^5\ne1$.

All 12 even denominator factors $1-Q^{2j}$ are reconstructed and their recorded inverses multiplied out. Computing $E,S_5,D=ES_5$ and an independent extended-Euclidean inverse gives $$E=-Q^3,$$ $$\begin{aligned}
 \bar\tau={}&-Q^{18}-Q^{17}-Q^{16}+Q^{15}+Q^{14}-Q^{11}-Q^{10}+Q^9\\
 &-Q^8+Q^6-Q^4-Q^3+Q^2+Q-1.
\end{aligned}$$ The coefficient vector in ascending order is $$(2,1,1,2,2,0,1,0,2,1,2,2,0,0,1,1,2,2,2).$$ It has degree $18<20$ and is nonconstant, so it is not in $\mathbb F_3$. The identities $D\bar\tau=25=1$ and $ES_h=25=1$ are checked independently. The recorded nonzero $\bar\tau^3-\bar\tau$ and its inverse also multiply to one.

The finite Euler product independently gives all 12 original Gaussian coefficients, their reciprocity, $H_{11}(-1)=0$, and the derivative $g$. Computing the numerator of $W$ through exponent $11$ and its original denominator through even exponent $36$ produces exactly the same $25W/g$. None of those even exponents is divisible by $25$. The resulting $g$ is nonzero; its inverse and the denominator inverse exist. Thus reduction of the original rational parameter is justified, rather than inferred from a formally cancelled expression.

The residue-field calculation proves that $ES_5$ is a local unit. Therefore $\tau$ is integral at the prime above $3$ and has the displayed residue. Each of the three recorded values of $A\bar\tau+1$ and $\bar y=\bar\tau(A\bar\tau+1)/(\bar\tau-1)$ is reconstructed and the recorded $\bar y$ inverse is checked. The lemma on the preceding page proves the conclusion for *every* $A\ge1$ at $d=25$.

**Negative controls.** Separate mutations of the residue of $\tau$, a denominator inverse, and an irreducibility Bezout coefficient are all rejected by the mathematical checker. Further controls reject a missing order-89 row, a false norm endpoint, and treating the order-27 inner witness as an outer witness. The latter guards against an incorrect all-$A$ interpretation of one conjugate.

# 4 Exact conjugate witnesses and all size coverage

For a nonreal multiple-root parameter and $A\ge3$, the accepted critical-parameter argument gives $$1+\frac1A<\rho:=|\tau-1|^2\le2+\frac2A\le\frac83.$$ Its rank-one parity matrix has nonzero real off-diagonals and a last-diagonal shift $A(\tau-1)$. A repeated eigenvalue has a Jordan chain; complex symmetry gives $u^Tu=0$ and hence $0<|u_r|^2/\|u\|^2\le1/2$. The Hermitian identity and the formula for $x^2$ then give the displayed annulus. The inner endpoint is strict; the outer endpoint is included. No diagonalizability assumption is made.

For $d=27$, the exact witnesses are $$\rho_{13}\in[1033,1034]/1000<7/6,\qquad
 \rho_{11}\in[2339,2340]/1000>7/3.$$ The first excludes $3\le A\le6$, because $1+1/A\ge7/6$. The second excludes $A\ge6$, because $2+2/A\le7/3$. The overlap at $A=6$ is harmless and there is no uncovered size. For every remaining order the following exact closed intervals have lower endpoint greater than $3>8/3$.

<div class="center">

| $d$ | $k$ | $1000\rho$ lower | upper | $d$ | $k$ | $1000\rho$ lower | upper |
|----:|----:|-----------------:|------:|----:|----:|-----------------:|------:|
|  29 |   3 |             3267 |  3268 |  61 |   1 |             4835 |  4836 |
|  31 |  11 |             3043 |  3044 |  63 |   1 |             5048 |  5049 |
|  33 |   2 |             3584 |  3585 |  65 |   1 |             5262 |  5263 |
|  35 |   3 |             4241 |  4242 |  67 |   1 |             5476 |  5477 |
|  37 |   2 |             4283 |  4284 |  69 |   1 |             5691 |  5692 |
|  39 |   4 |             6577 |  6578 |  71 |   1 |             5907 |  5908 |
|  41 |   2 |             4948 |  4949 |  73 |   1 |             6123 |  6124 |
|  43 |   3 |             7608 |  7609 |  75 |   1 |             6340 |  6341 |
|  45 |   1 |             3165 |  3166 |  77 |   1 |             6558 |  6559 |
|  47 |   1 |             3370 |  3371 |  79 |   1 |             6776 |  6777 |
|  49 |   1 |             3577 |  3578 |  81 |   1 |             6995 |  6996 |
|  51 |   1 |             3784 |  3785 |  83 |   1 |             7215 |  7216 |
|  53 |   1 |             3992 |  3993 |  85 |   1 |             7435 |  7436 |
|  55 |   1 |             4202 |  4203 |  87 |   1 |             7655 |  7656 |
|  57 |   1 |             4412 |  4413 |  89 |   1 |             7876 |  7877 |
|  59 |   1 |             4623 |  4624 |     |     |                  |       |

</div>

These are 31 distinct odd orders, plus the two order-27 rows, hence 33 interval rows. Together with the separate order-25 field argument they cover 33 distinct odd orders. Every listed $k$ is coprime to $d$.

The small sizes have $J_2=x^2-\tau$ and $J_3=x(x^2-1-2\tau)$, so their only exceptional parameters are $0$ and $-1/2$. Nonreality excludes both. For fixed $A$, $\operatorname{Disc}_xJ_{A+1}(x;T)\in\mathbb Q[T]$. Vanishing would hold under every cyclotomic embedding, contradicting a witness outside the annulus. Only algebraic vanishing is transported; norms and signs of imaginary parts are not transported between conjugates.

# 5 Independent arithmetic replay and retained boundaries

The fresh checker uses only the Python standard library, with exact integers and rational fractions. Its dyadic interval scale is $2^{512}$, distinct from the candidate’s $2^{256}$. It bounds $$\pi=4\bigl(\arctan(1/2)+\arctan(1/3)\bigr)$$ using 300 alternating terms per arctangent and the next term as the exact remainder bracket. The tangent addition formula and the angle range identify this sum as $\pi/4$. Separate cosine and sine polynomials of degrees 200 and 201 enclose $q=e^{2\pi i k/d}$ with Taylor–Lagrange errors $\theta_{\max}^{201}/201!$ and $\theta_{\max}^{202}/202!$.

All products and reciprocals round outward; zero-crossing squares have lower endpoint zero; every complex denominator has a proved positive squared-norm lower bound. Binary powers reconstruct $E$, the prefix sums, and the original finite Euler product. At every row, each new interval for $q,E,S_5,S_h,\tau$ and $\rho$ lies inside its recorded candidate enclosure. A third route using the original uncancelled $W/g$ lies inside the saved product-route intervals too. The checker also verifies $q^d=1$, $|E|^2=d$, $ES_h=d$, nonreality at each witness, and every displayed rational norm bound. Full independent endpoints are in `RESULTS.json`.

All **1,801** exact checks pass. The immutable archive is extracted into a separate directory and the new checker alone is run there with Python isolated mode. Fresh and cold result files are byte-identical, with SHA-256

<div class="center">

`bd46db710d2d1f84fd5ca59c11fe84acfb5cd42ec57f26684304d5ecc385ca18`.

</div>

No candidate, predecessor, or uploaded research program is executed or imported. The three inherited review archives pass CRC, and the cited proof files are byte-identical to their respective archived copies. Those prior accepted results are inherited with their stated scopes; this audit does not claim to freshly redo every predecessor computation.

**Exact integration.** The accepted lower strip is $11<d\le23$, the new middle strip is $25\le d\le89$, and the accepted general tail is $d\ge15(11+1)/2=90$, whose first admissible odd order is $91$. Thus all odd $d>11$ are covered without a boundary gap. The inherited ordinary theorem covers $b=11$ because it covers every odd $b\le25$ and all odd $d>b$. Together with inherited $g\ne0$ and $\operatorname{Res}_z(1+z^d,U)\ne0$, all four guards hold for the degree-eleven family.

Any characteristic-zero field containing a primitive order-$d$ root receives an injective map from $\mathbb Q(\zeta_d)$. The proved nonzero discriminants remain nonzero. No embedding of the entire base field into $\mathbb C$ is needed.

**Scope and remaining work.** The completed families are b=1,3,5,7,9,11; the general remaining-guard problem stays open. Remaining overlap is odd $b\ge13$ with $2b+1<d<15(b+1)/2$, except separately proved instances. Remaining ordinary squarefreeness is odd $b\ge27$ with $b<d<4b^2$, except separately proved instances. The next degree-13 middle strip is odd $29\le d\le103$.

No conclusion is added for even orders, nonprimitive roots, $A=0$, positive characteristic, quantitative conditioning, or historical priority. The verdict is mathematical acceptance at the stated scope, without a novelty or historical-priority conclusion.
