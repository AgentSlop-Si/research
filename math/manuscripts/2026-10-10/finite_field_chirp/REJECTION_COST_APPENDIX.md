# Exact rejection and cost contract

Appendix A to [A nonvanishing phase eliminant for exact finite field chirp recognition](MANUSCRIPT.md). The ledger specifies all charge categories; its formulas are uniform asymptotic envelopes, not exact instruction counts or measured timings.

## A1 Input and terminal states

Required data are the complete canonical-residue vector \(x\in\mathbb F_p^N\), integers \(N\ge3\) and \(1\le r\le\lfloor N/3\rfloor\), a supplied certified prime \(p\) with \(N\mid p-1\), and a supplied element \(\omega\) of exact order \(N\). The dyadic implementation additionally requires \(N\) to be a power of two. A separate sparse-first cap, if used, satisfies \(1\le t\le N/2\). Missing field/root discovery is not an assumed free subroutine.

| State | Exact meaning | Output obligation |
|---|---|---|
| ACCEPT | The full input has a representation within the applicable cap and family | Field/root identifiers, canonical phase, distinct frequency indices, nonzero amplitudes, branch label if dispatching, and all \(N\) positive-sign unnormalized DFT values |
| REJECT | All necessary complete paths establish nonmembership in \(\mathcal C_r\), or in \(\mathcal S_t\cup\mathcal C_r\) when that union is the chosen contract | Decision only; no arbitrary-input DFT and no promised succinct negative witness |
| INVALID_CONTRACT | Size/cap/encoding assumptions fail, the established prime-field premise is absent, or the supplied root fails validation | Identification of the invalid condition; no assertion of family nonmembership over some other field or grid |
| UNKNOWN | An explicitly budget-limited wrapper stopped before membership was decided | No negative membership claim; a separately paid DFT backend may still run |

A field-certificate verification whose validity has not been established cannot be treated as a successful field premise. The stated complete decision theorem concerns valid-contract inputs; budget or resource failure is not mathematical rejection.

Zero is accepted with an empty representation only after the complete raw-vector zero scan. Its dense output consists of \(N\) zeros. The accepted representation is not certified to use the globally smallest number of terms across phases.

## A2 Validation and shared preparation

1. Read the declared length, caps, field/root data, and all raw coefficients. Check the vector length and canonical residue conditions. Reading \(N\) field elements is charged.
2. The theorem accepts an established prime-field premise. If primality or an untrusted primality certificate is to be verified, add the actual certification cost \(C_{\rm field}(p)\) and its storage. Neither prime search nor primitive-root discovery is included.
3. Without factoring \(N\), compute \(1,\omega,\ldots,\omega^N\). Require \(\omega\ne0\), \(\omega^N=1\), and \(\omega^j\ne1\) for \(1\le j<N\). This proves exact order and supplies the power table. Work, equality checks, and storage are \(O(N)\), including failure paths. An independently valid root certificate can replace the order test; constructing the table remains paid.
4. Use table indices for inverse powers. This step does not spend a scalar inverse on each root or dechirped coordinate.
5. Find the all-zero case and an interior nonzero center. A nonzero vector with no center in \([r,N-r-1]\) is a genuine early rejection by the no-consecutive-zeros proof.

Write \(G=O(N)\) for this shared field work and traffic, excluding optional field certification and the declared integer-arithmetic costs. It is already covered by the final \(+N\) terms of the stand-alone recognizer envelopes. In a dispatcher, charge shared preparation once.

## A3 Every rejection route

| Stage | Failing condition | Scope of the failure | Cost paid before continuing or stopping |
|---|---|---|---|
| Contract validation | Invalid size, cap, residue, field premise, divisibility, or root order | INVALID_CONTRACT | Actual validation and table/read work already performed, plus any certification work |
| Zero handling | A later entry is nonzero after a zero prefix | No zero acceptance; continue appropriate nonzero path | Full scan or subsequent full verification; a zero prefix alone never accepts |
| Center search | Nonzero input has no allowed nonzero center | Final REJECT for \(\mathcal C_r\) | \(O(N)\) scan |
| Phase scan | No root of \(E\) on the canonical phase grid | Final REJECT for \(\mathcal C_r\) | Entire determinant construction and phase scan |
| Dyadic candidate BM | Prefix recurrence order exceeds cap, or final polynomial degree differs from recorded order | Reject this phase only | BM work up to failure, at most \(O(r^2)\) |
| Dyadic candidate roots | Fewer or more than the required distinct grid roots | Reject this phase only | Full necessary root scan within \(O(N\log(r+2))\) |
| Dyadic candidate amplitudes | Zero derivative denominator or zero listed amplitude | Reject this phase only | Polynomial work \(O(r^2)\), with actual scalar inversions charged |
| Dyadic candidate synthesis | Any synthesized coordinate differs from raw dechirped input | Reject this phase only | Full synthesis bound \(O(N\log(r+2))\), and comparisons up to failure |
| All-length prefix | Leading block at the computed positive rank is singular | Reject this phase only | Dense rank and solve budget \(O(r^3)\) |
| All-length roots | Monic recurrence does not have the required number of distinct grid roots | Reject this phase only | Blocked scan \(O(N(r+1)^{\kappa-1})\) |
| All-length residuals | Any of the \(N-s\) recurrence residuals is nonzero | Reject this phase only | Blocked full-residual budget \(O(N(r+1)^{\kappa-1})\) |
| Rank zero | Entire dechirped vector is not zero | Reject this phase only | Full scan \(O(N)\) |
| Candidate exhaustion | Every retained phase failed its complete necessary tests | Final REJECT for \(\mathcal C_r\) | Sum of every attempted phase cost, bounded by \(C_*\) candidate budgets |
| Sparse-first failure | Raw input is not in \(\mathcal S_t\) | Continue the common-chirp branch | Entire first-attempt cost \(A(N,t)\), even if the later branch also rejects |
| Budget exhaustion | An optional time/work cap is reached | UNKNOWN | Actual work already spent; backend cost is additional if requested |

For the all-length test, a successful Vandermonde solve may include zero weights; omit those weights. The checked recurrence and first samples still force full equality. For the dyadic test, the minimal-recurrence recovery explicitly rejects zero amplitudes. These equivalent acceptance mechanisms need not have identical intermediate rejection labels.

A derivative-zero guard is harmless even when the required distinct-root count already makes it impossible on a degree-\(s\) candidate. Failure of a polynomial-ring pivot would indicate a broken implementation or invalid arithmetic, not a legitimate family rejection: the nonzero-center proof guarantees those pivots are units.

## A4 Dyadic cost ledger

Let \(D=\binom{r+2}{3}\), \(L=N/2\), \(C_* =\min(D,L)\), \(\kappa=\log_2 3\), and \(T(r)=r^2(D+1)^\kappa\).

| Component | Additions and multiplications | Scalar inversions | Live field elements |
|---|---:|---:|---:|
| Shared raw reads, root table, zero and center checks | \(O(N)\) | 0 | \(O(N)\) |
| Toeplitz determinant in \(\mathbb F_p[z]/(z^{D+1})\) | \(O(T(r))\) | 1 cached inverse of \(x_c\) | \(O(r(D+1))\) |
| Coefficient reduction modulo \(z^L-1\) | \(O(D+L)\) | 0 | \(O(D+L)\), reusable |
| Phase-grid pruned transform | \(O(N\log(\min(D+1,L)+2))\) | 0 | \(O(N)\) |
| One candidate dechirp, BM, grid roots, amplitudes, and full synthesis | \(O(N\log(r+2)+r^2)\) | \(O(r)\) | \(O(N)\) |
| All candidate attempts | \(O(C_*[N\log(r+2)+r^2])\) | \(O(C_*r)\) | One candidate workspace at a time |
| Accepted Gauss row and all dense outputs | \(O(Ns+N)\subseteq O(Nr+N)\) | No additional field inversions | \(O(N)\) |

The sum is
\[
H=T(r)+D+N\log(\min(D+1,L)+2)
+C_*[N\log(r+2)+r^2]+Nr+N
\]
inside a uniform \(O(H)\) bound. On rejection the final output work is absent, but the same bound applies. Candidate dechirping is absorbed into its \(N\log(r+2)\) term. All equality checks, coefficient initialization, copying, zero-filling, and corresponding index/array traffic are covered at the stated elementary-operation scale.

The total scalar-inversion count is \(O(1+C_*r)\). BM may cache its nonzero discrepancy inverse whenever that discrepancy changes; there are only \(O(r)\) such events in a \(2r\)-sample run. Amplitude denominators add \(O(r)\). The Toeplitz series inverses all start from the same \(x_c^{-1}\); ring inversions are not counted as free scalar operations.

Peak storage is \(O(N+r(D+1))\), not the sum of candidate workspaces. Hence the simplified envelopes are
\[
O(Nr^3\log(r+2)+r^{2+3\kappa}),\quad
O(1+r^4)\text{ inversions},\quad O(N+r^4)\text{ field elements}.
\]

## A5 All length ledger

Replace the dyadic phase scan by \(O(N(D+1))\) Horner work. Replace each sparse candidate test by the dense prefix setup and two blocked kernels described in manuscript Section 7:
\[
O\!\left(N(r+1)^{\kappa-1}+r^3\right),
\quad O(r)\text{ inversions},\quad O(N+r^2)\text{ workspace}.
\]
Thus
\[
B=T(r)+N(D+1)+C_*[N(r+1)^{\kappa-1}+r^3]+Nr+N,
\quad L=N/\gcd(2,N).
\]
The \(O(r^6)\) total dense prefix term is absorbed by \(r^{2+3\kappa}\). The phase term \(Nr^3\) is absorbed by \(Nr^{2+\kappa}\), yielding Theorem 3. All scalar inversions and storage retain their prior bounds. This ledger uses Horner scanning deliberately; it does not require a fast transform at general length.

## A6 Sparse first overhead and optional fallback

Let \(A=N\log(t+2)+t^2\), and use \(K=\min(B,H)\) at dyadic lengths, \(K=B\) otherwise. The minimum is justified only because \(B\) and \(H\) decide the same \(\mathcal C_r\) contract. Equivalent integer size templates can choose between them without a real-logarithm oracle.

| Path | Field arithmetic | Scalar inversions | Storage |
|---|---:|---:|---:|
| Dyadic sparse-first acceptance | \(O(G+A+N)\) | \(O(t)\) | \(O(N)\) |
| Dyadic sparse rejection followed by chirp acceptance or rejection | \(O(G+A+K)\) | \(O(t+1+C_*r)\) | \(O(N+r^4)\) |
| Nondyadic complete decision | \(O(G+B)\) | \(O(1+C_*r)\) | \(O(N+r^4)\) |

For \(t=r\), the first attempt is absorbed in either chirp envelope, yet it is still performed and paid. For \(t\ne r\), retain its explicit charge and the union family \(\mathcal S_t\cup\mathcal C_r\). A failed sparse recognition does not by itself exclude a nonzero common phase.

On final rejection, an arbitrary-input transform wrapper adds all backend preparation, arithmetic, storage, and output work. The available same-field choices proved here are dyadic \(O(N\log N)\) radix-two evaluation or all-length \(O(N^\kappa)\) convolution. A separate backend of cost \(F(N,p)\) gives total \(O(G+A+K+F(N,p))\) when the sparse attempt exists; omit \(A\) otherwise. Peak memory is the maximum of sequential stages only if earlier workspaces are actually released. A backend-sized budget may abort recognition, but then membership remains UNKNOWN.

## A7 Integer word and bit costs

The main theorem counts exact field additions/multiplications and separately lists scalar inversions. The Gauss-row output also performs integer gcd and modular-inverse computations on \(O(\log N)\)-bit integers. Its inverses modulo \(m\) or \(q\) are not field inversions and must be paid separately. Powers such as \(aj^2\), binomial exponents, degree indices, and addresses need properly sized integer arithmetic; table lookups do not make their index computations free.

For a word-RAM interpretation, assume \(\log p=O(\log N)\), sufficiently wide address-capable words, and the stated cost for modular addition, multiplication, and reduction. With word inversion cost \(I_{\rm word}(p)\), a chirp path costs
\[
O(K+(1+C_*r)I_{\rm word}(p)+G_{\rm int}(N)+C_{\rm field}(p)),
\]
plus any preceding \(G+A\) work and \(O(t)\) inversions. The degree \(D=O(N^3)\) and maximum workspace addresses occupy \(O(\log N)\) bits with a suitable constant factor. If modular multiplication is not unit-cost on the target machine, its true cost multiplies the appropriate arithmetic count. For larger \(p\), each field element occupies multiple words.

For a conservative bit conversion, put \(b=\lceil\log_2p\rceil\), let \(M_{\rm mod}(b)\) upper-bound the relevant modular arithmetic cost, and let \(I_{\rm bit}(b)\) be inversion cost. A dispatcher path is bounded by
\[
O\!\left((G+A+K)M_{\rm mod}(b)
 +(t+1+C_*r)I_{\rm bit}(b)
 +G_{\rm index,int}(N)+C_{\rm field}(p)\right),
\]
with absent branches removed and the full actual index-operation total used in \(G_{\rm index,int}\). Include \(\Omega(Nb)\) input and accepted-output traffic. Storage is \(O((N+r^4)b)\) field-data bits, plus indices and certification workspace. This is a parameterized conversion, not an optimized bit-complexity theorem.

No scalar inversion, field certification, input decoding, root discovery, numerical tolerance, or fresh-vector operator application is concealed in the headline field-operation count.
