# Two case normalization and guard sheet

Companion to MANUSCRIPT.md, 10 October 2026 UTC. This is a theorem-use checklist, not an unconditional simplicity claim.

## Common conventions

$H_n(z;q)=\sum_k{n\brack k}_qz^k$, $D_n=\operatorname{Disc}_zH_n$, with the ordinary derivative, monic $H_n$, $\operatorname{Disc}1=1$, and $\operatorname{Res}(F,1)=1$. Use monic probabilists’ $\operatorname{He}_A$ and $P_A=\prod_{j=1}^Aj^j$.

Fix odd $d$, primitive complex $\omega$, $A\ge1$, $0\le b<d$, $n=Ad+b$, $F=z^d+1$, and $G=H_b(z;\omega)$. The formal path is $q(\varepsilon)=\omega(1+\varepsilon^2)^{1/d}$. Exactly $q^d-1=\varepsilon^2$. The factorization at $\varepsilon=0$ is $F^AG$.

For a nonmonic degree-$e$ polynomial $f=a\prod_i(z-\rho_i)$, $\operatorname{Disc}f=a^{2e-2}\prod_{i<j}(\rho_i-\rho_j)^2$. Every global polynomial in the formulas below is monic. Local initial forms may have a prefactor; do not take their discriminant as though they were monic without accounting for that prefactor. The manuscript instead uses their root displacements directly.

## Case S separated clusters

- Domain: odd $d\ge1$; $d=1$ is the classical endpoint
- Required guards: $\Delta=\operatorname{Disc}G\ne0$ and $R=\operatorname{Res}(F,G)\ne0$
- Cluster count: $A$ roots near each of the $d$ roots of $F$, and $b$ simple residual roots
- Nonzero initial form at $\alpha^d=-1$:

$$
H_n(\alpha+\varepsilon x;q(\varepsilon))
=\varepsilon^A(-1)^Ad^{A/2}G(\alpha)
\operatorname{He}_A(\sqrt d\,x/\alpha)+O(\varepsilon^{A+1}).
$$

- First displacements: $\alpha h_j/\sqrt d$, with $h_j$ the Hermite roots
- Leading $x$ coefficient of the initial form: $(-d/\alpha)^AG(\alpha)$
- Exact exponent: $K=dA(A-1)/2$
- Nonzero coefficient in $q^d-1$:

$$
C_{\rm sep}=(-1)^{A(d-1)/2}d^{dA(A+1)/2}P_A^d\Delta R^{2A}.
$$

Then $D_n(q(\varepsilon))=\varepsilon^{2K}(C_{\rm sep}+O(\varepsilon^2))$.

Odd $b$ forces $G(-1)=0$ and $R=0$, so it does not satisfy this case. The formal identity for the $\varepsilon^A$ coefficient remains true with a zero coefficient at a shared root; it is not a nonzero leading form there.

## Case O one simple shared root at minus one

- Domain: odd $d\ge3$, odd $1\le b<d$
- Deflate first: $G=(z+1)U$, with monic $U$
- Check $R_U=\operatorname{Res}(F,U)\ne0$ first; it implies $g=U(-1)=G'(-1)\ne0$
- Define $W=(\omega;\omega)_b/(\omega^2;\omega^2)_{(b+d)/2}$ and $\tau=dW/g$
- The Pochhammer denominator is nonzero since $(b+d)/2<d$ and $\omega^2$ has order $d$
- Remaining guards: $\Delta_U=\operatorname{Disc}U\ne0$ and $S_A(\tau)=\operatorname{Disc}J_{A+1}\ne0$
- Local monic polynomial:

$$
J_{A+1}(y;\tau)=y\operatorname{He}_A(y)-\tau\operatorname{He}'_A(y)
=\operatorname{He}_{A+1}(y)+A(1-\tau)\operatorname{He}_{A-1}(y).
$$

- Shared initial form:

$$
H_n(-1+\varepsilon x;q(\varepsilon))
=\varepsilon^{A+1}(-1)^{A+1}d^{(A-1)/2}g
J_{A+1}(-\sqrt d\,x;\tau)+O(\varepsilon^{A+2}).
$$

- Shared first displacements: $-j_k/\sqrt d$, with $j_k$ the roots of $J$
- Leading $x$ coefficient: $gd^A$
- Cluster count: $A+1$ at $-1$, $A$ at each other root of $F$, and $b-1$ simple residual roots
- Exact exponent: $L=dA(A-1)/2+A=K+A$
- Nonzero coefficient in $q^d-1$:

$$
C_{\rm ov}=(-1)^{A(d-1)/2}d^{dA(A+1)/2+A}P_A^{d-1}
S_A(\tau)\Delta_U R_U^{2A}g^2.
$$

Then $D_n(q(\varepsilon))=\varepsilon^{2L}(C_{\rm ov}+O(\varepsilon^2))$. The separated coefficient is zero here and cannot be relabeled as the first nonzero coefficient. The unmodified $\operatorname{He}_{A+1}$ is generally the wrong shared model.

## Three normalizations

Put $(M,C)=(K,C_{\rm sep})$ or $(L,C_{\rm ov})$, and $Q_d=(q^d-1)/\Phi_d$.

| Object | Exact order | Leading value |
|---|---:|---|
| Formal series in $\varepsilon$ | $2M$ | $C$ |
| Local series in $q^d-1$ | $M$ | $C$ |
| Local series in $q-\omega$ | $M$ | $(d\omega^{d-1})^MC$ |
| Integral quotient $E=D_n/\Phi_d^M$ at $\omega$ | Nonzero value | $Q_d(\omega)^MC$ |

Do not omit $Q_d(\omega)^M$ in a cyclotomic-quotient check. Do not omit $(d\omega^{d-1})^M$ when using a $q-\omega$ Taylor coefficient. The sign $(-1)^{A(d-1)/2}$ is part of the ordinary discriminant and is not an absolute-value convention.

## Arithmetic checklist

To use the bridge to $n=(dp-1)/2$, perform these steps in this order:

1. Verify that $p$ is an odd prime and $p\nmid d$; set $A=(p-1)/2$, $b=(d-1)/2$.
2. Work in one specified field factor of $\mathbb F_p[q]/(\Phi_d)$. Exact order $d$, squarefreeness of $\Phi_d\bmod p$, and the unit property of $Q_d$ depend on $p\nmid d$.
3. In Case S, check both $\Delta$ and $R$ in that same component. In Case O, check $\Delta_U,R_U,S_A$, and define $\tau$ only after $g\ne0$ is verified.
4. For inverse-pair selection at $d\equiv3\pmod4$, check $\Gamma_d(\omega)\Gamma_d(\omega^{-1})\ne0$ in one common component, where $\Gamma_d=\Delta_U R_U$.
5. If $p\equiv1\pmod4$, also check $\delta_d=2g-dW\ne0$ there. The precise simultaneous-pair exception is $\tau=\tau'=2$; each $J$ then has a triple root at zero. For $p\equiv3\pmod4$, that exception cannot occur.
6. After selecting the good member of an inverse pair, use the appropriate characteristic-zero order to divide **exactly in $\mathbb Z[q]$**: $D_n=\Phi_d^M E$.
7. Evaluate $E(\omega)=Q_d(\omega)^MC$ in the selected component. All factors are units; $A<p$ makes $P_A$ a unit.
8. Only then reduce $\Phi_{dp}\equiv\Phi_d^{p-1}\pmod p$ to obtain the contradiction if $D_n(\zeta_{dp})=0$.

There is no condition $M<p-1$. Canonical reduced coefficient content selects one good component; a norm or an everywhere-unit condition is different. Reduction before the full integral division is not this proof.

## Characteristic zero guard reduction

Only when $d\equiv3\pmod4$ and $b=(d-1)/2$, squarefreeness of $H_b$ implies the residual resonance and local-$J$ guards for every $A\ge1$. Appendix A proves the half-order resonance and $|1-\tau|=1$ disk argument. This does not remove general-$b$ guards, prove composite squarefreeness, or establish finite-characteristic same-component conditions.

## Historical and current arithmetic collections remain distinct

The following is contextual scope reconciliation from R03 §6, not a newly attached or replayed certificate appendix:

| Collection | Lower bases | Prime hypothesis in the uniform bridge | Separately attributed exceptions or exclusions |
|---|---|---|---|
| Six historical separated bases | $5,9,13,17,21,25$ | Every odd prime $p\nmid s$ | Original three $p\equiv1\bmod4$ families have separate certificates at targets $25,169$. Do not silently include $27,289,63,147,125$ through this bridge. |
| Five historical paired overlap bases | $3,7,11,15,19$ | $p\equiv3\bmod4$, $p\nmid s$ | Historical certificates separately cover targets $9,49,121,45,361$. |
| Six current augmented overlap bases | $3,7,11,15,19,23$ | $p\equiv1\bmod4$, $p\nmid s$ | At $s=15$, exclude $p=5$; target $75$ is outside this bridge. Base $23$ comes from its later accepted package, not the older five-base manuscript. |

“Eleven historical families” means six separated plus five paired-overlap families. It does not mean eleven augmented bases or a common prime-congruence theorem. Current augmented targets are $3\bmod4$ and retain the forbidden resonant scalar node; they do not yield the smaller scalar-bank minimum.

The accepted valuation

$$
v_p(c_{sp}^{\rm sep})=\left\lfloor\frac{3s(p-1)}8\right\rfloor
$$

requires positive $s\equiv1\pmod4$, prime $p\equiv1\pmod4$, $c_s^{\rm sep}\ne0$, and $p\nmid s c_s^{\rm sep}$. It is a separately proved **separated-content** statement, not a formula for paired or augmented content and not an unconditional support assertion. Its intermediate content-product order $3sA^2/2$ is different from both $K$ and $L$. The full proof is not redeveloped in the local-discriminant manuscript; see R03 §7 and its exact source pins.

## Stopping boundary

Repeated-prime lifting, universal lower-content support, and arbitrary-composite half-degree simplicity remain open extensions in the project. Isolated certificates do not remove these gaps. No proof lemma is missing inside the guarded local theorem as stated.
