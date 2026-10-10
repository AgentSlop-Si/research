# Exact combinatorial certificate for the scaled-projector theorem

This file records an independent, integer/rational check of the finite identities behind Theorem 5.1. It is not a proof-assistant formalization, but it does not use floating-point covariance matrices.

Let

\[
N=p^L=KM,\qquad M=p^\mu,\qquad K=p^{L-\mu},\qquad K\ge M.
\]

For a fixed local coordinate `u` and valuation shell `v=0,...,mu-1`, the admissible nonzero displacements satisfy

\[
\#\{d\in D_u:\nu_p(|d|)=v\}
=
\frac{(p-1)M}{p^{v+1}}.
\]

The corresponding projector on the block Fourier modes has rank

\[
\frac{(p-1)K}{p^{v+1}}
\]

and its nonzero eigenvalue before the outer `1/N` normalization is

\[
\frac{p^{v+1}}{p-1}.
\]

Multiplying the shell count, shell eigenvalue and `1/N` gives exactly

\[
\frac{(p-1)M}{p^{v+1}}
\frac{p^{v+1}}{p-1}
\frac1N
=
\frac MN.
\]

The shell projectors are mutually orthogonal. Their rank per local coordinate telescopes to

\[
\sum_{v=0}^{\mu-1}\frac{(p-1)K}{p^{v+1}}
=K-\frac KM.
\]

Across all `M` local coordinates, the rank is

\[
M\left(K-\frac KM\right)=N-K,
\]

and the trace is

\[
(N-K)\frac MN=M-1.
\]

`projector_certificate.py` checks these identities with exact Python integers and `Fraction` arithmetic. The saved run covers 141 parameter triples with primes up to 13, exponents up to 10, and `M<=10000`; for every local coordinate it independently checks the displacement-shell count.

Run:

```bash
python projector_certificate.py --output projector_certificate_results.json
```

Expected terminal result:

```text
PASS: 141 exact prime-power parameter cases
```
