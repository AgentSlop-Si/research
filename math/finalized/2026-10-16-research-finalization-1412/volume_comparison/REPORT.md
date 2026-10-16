# ALG-057 rectangular-volume comparison

Date: 2026-10-16. Scope: the exact independent arbitrary-jet, exposed-output, bounded-linear-gate interface in the supplied Young-feedback obstruction.

## Result

**The sharpening A >= JS/2 is a direct application of established rectangular row-volume machinery.** It removes an avoidable loss from the repository proof, but supplies no new asymptotic obstruction or demonstrated historical novelty. The named comparison can be closed without closing different input or gate models.

## Exact classical statement and provenance

For M in C^(a x d), let M_I contain an r-subset of its rows. Bürgisser and Lotz, *Lower Bounds on the Bounded Coefficient Complexity of Bilinear Maps*, [arXiv:cs/0301016v1](https://arxiv.org/pdf/cs/0301016v1), §3, printed p.7, equation (2), state

    vol_r(M) = max_(|I|=r) sqrt(det(M_I M_I*)),
    C(M) >= log_2 vol_r(M).

They attribute this extension of Morgenstern's determinant argument to Raz (2002). Their §2.1, printed pp.3–4, uses addition/subtraction and scalar multiplication with modulus at most 2, charging every instruction. For a matrix with exactly r independent output rows, the displayed volume is sqrt(det(M M*)). This is the required rectangular statement, rather than a maximum individual square minor or the later mean-square-volume proposition.

Version matters: the [2002 FOCS draft](https://www3.math.tu-berlin.de/algebra/work/bc.pdf), §3, uses a maximum-square-minor definition under the same symbol. Cite the pinned 2003 manuscript for the row-Gram formula above. The published article is JACM 51(3), 464–482 (2004), [DOI](https://doi.org/10.1145/990308.990311); equation numbering here is explicitly manuscript numbering.

[Raz's original ECCC TR02-012](https://eccc.weizmann.ac.il/report/2002/012/) was located, but this check did not obtain usable theorem text from its PDF. Direct verification therefore rests on the readable Bürgisser–Lotz statement; Raz attribution is reported as their attribution, not a separately checked theorem-number claim.

## Model specialization and application

The supplied ALG-057 model allows free copies/permutations and scalar multipliers of modulus at most 1, and charges binary additions/subtractions. An all-gate complexity bound alone would not justify its additions-only claim; the elementary potential proof does.

Fix q. Take the maximum exterior-product norm of q coefficient rows among all input and computed forms. Initially it is 1. A unit-bounded scalar gate does not increase it. Substituting a new sum into any selected q-tuple splits its exterior product into two terms, each bounded by the previous maximum. Thus each paid binary addition multiplies the potential by at most 2. Copies, permutations and subtraction obey the same bounds. Keeping all earlier forms only strengthens this lower-bound analysis.

The source proves BB* = diag(2^(b+t), with multiplicities m_t), defines S = sum_t(b+t)m_t, and exposes J independent complete copies of B. Their combined target matrix T has

    det(T T*) = 2^(JS),
    q = J sum_t m_t <= r(n+1).

Applying the potential directly to its q rows yields

    2^A >= sqrt(det(T T*)) = 2^(JS/2),
    A >= JS/2.

No column-minor selection or complementary coordinate padding is needed. The old subtraction (J/2) log_2 binom(r,m) arose from choosing a single square minor; it is not intrinsic to the rectangular theorem. The existing estimate S/2 >= rL/64 and identity rL=N/2 give A >= JN/128, improving the former JN/256 while retaining the same Omega(Nn) order.

## Optional exact refinement

The same argument also includes partial terminal banks: age t is exposed for j=0,...,n-b-t. Orthogonality within each jet block and independence across blocks give

    A >= (1/2) sum_t (n-b-t+1)(b+t)m_t >= JS/2.

This refinement was independently checked in the current review. It does not change the asymptotic conclusion or classical-method attribution; JS/2 should not be described as an optimal exact constant.

## Disposition

Record this as **classical-method sharpening of the existing component proof**, with the marker-word packet construction credited to its supplied source. Do not label the volume lemma new, or infer publication novelty merely from finding no matching packet application. Independent jets, actual scalar outputs and the gate bound remain essential. Constrained source-generated jets, fused source/solve outputs, unrestricted multipliers/nonlinear operations, and finite-field constructions are outside this comparison.
