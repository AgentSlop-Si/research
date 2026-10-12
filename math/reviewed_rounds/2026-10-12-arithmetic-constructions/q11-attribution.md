Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, limitations and review method are retained. Original source-report SHA-256: e04fed374a719b50e20141ea81e47acc9a7948ae6d4b7d686b0f3a03a18c47f1.

# Q11 attribution addendum: independent model and cost review

Date: 2026-10-12 UTC. Verdict: **ACCEPT the bounded attribution comparison, with historical priority unresolved.** This addendum does not replace or modify the accepted mathematical proof packet.

The weighted-cycle inverse, state-space compression/correction methodology, and low-rank spectral-assignment mechanism have identifiable prior antecedents. The inspected results do not, without an additional model-preserving argument, establish Q11's complete three-scalar-resolvent arithmetic-family contract. This is a bounded comparison, not evidence of firstness or publication significance.

## 1. Immutable mathematical result preserved

The accepted mathematical archive remains SHA-256 `cbf39369d76caa729479ce2adbd090ce393ff8754eec6dd798d1fec5fe72ebed`. Its candidate remains SHA-256 `1a428177a230cbf1ce6c32bdb7de1b11431c49dc5cd5a8eff1dca519c7cc4b42`. Both were rechecked without alteration. The comparison-report version reviewed here is separately bound in INPUT_BINDINGS.json and preserved as an inert snapshot.

The accepted result remains the original five-dimensional C_q for q positive odd, coprime to 5, and 1 modulo 241, over K=Q(eta). It has three diagonal-ended cycle resolvents with distinct Hamiltonian structural permutations. Zero weights are allowed; the third effective graph is one edge. The accepted two-term lower supplies minimality. No full growing-B_N, all-size, negative-sign upper, stability, FFT-speed, or priority claim is added.

## 2. Exact individual-branch antecedent

Huhtanen–Perämäki, Theorem 2.9 (author manuscript p.6), gives the inverse of I+DS as a sum of diagonally weighted powers of a cyclic shift. Substitution D=-diag(w), with the appropriate successor orientation, yields the Q11 branch identity. Zero weights are allowed by that identity. Theorem 2.10 (pp.6–7) normalizes nonzero weights using an nth root; that separate normalization cannot be imported as a root-free construction over K. Their multiplicative factorization theorem concerns a different architecture. Proposition 2.5 gives linear-operation sparse LU setup, not free dense inverse output. [Primary author manuscript](https://math.aalto.fi/~mhuhtane/manu.pdf).

Reviewer translation: if W=diag(w)P_sigma for any Hamiltonian successor cycle and h=product(w), then W^5=hI. Multiplying I-W by I+W+...+W^4 gives (1-h)I. Consequently the inverse formula is valid over any field with 1-h nonzero, without dividing by an individual edge. A simultaneous relabelling explains the comparison with the paper's canonical shift; no actual uncharged endpoint permutation or basis change is inserted into the Q11 construction. Diagonal endpoints multiply this same known branch identity. Inverting the complete branch as a sparse diagonal-plus-cycle matrix additionally requires invertible endpoints; the accepted witness has them, but the full source grammar need not.

## 3. Semiseparable correction precedent and exact model boundary

Chandrasekaran–Epperly–Govindarajan, §3.1, equations (3.3)–(3.5) and Algorithm 1, first replace corner blocks, construct an SSS representation, then restore the corner discrepancies through CSS generators. Equations (3.1)–(3.2) display separate diagonal and corner contributions. Their concluding discussion reports O(N^4) worst-case optimal-construction cost; fast multiplication presupposes a prepared compact representation. These are genuine method-level antecedents, not an immediate three-Green bound. [Version 3, pp.24–25 and 49–50](https://arxiv.org/pdf/1911.05858v3).

Reviewer model comparison: CSS state dimensions count generator sizes. Q11 counts scalar diagonal-ended Hamiltonian resolvents in one additive layer. The two Q11 modes couple their upper and lower rank-one generators through the same scalar monodromies. Ordinary independent upper/lower generators do not impose that coupling. A free CSS diagonal and corner correction must also be encoded within the permitted three branches, not counted for free. Reordering an entry to a corner may clarify an analogy; it is not a license to add unmatched endpoint permutations to the final identity.

The overlapping-block completion paper establishes simultaneous rank minimization by one missing block over an arbitrary field. Thus a supposed real-versus-cyclotomic field distinction alone would be inadequate to dismiss this antecedent. Its optimization objective still differs from forcing Q11's constrained monodromy to split while preserving the other guards. [Epperly–Govindarajan–Chandrasekaran, Theorem 1 and field convention, pp.1–3](https://arxiv.org/pdf/2106.11267).

The word “Green” also has a broader rank-structured meaning: Boito–Eidelman §2 uses off-diagonal rank conditions and band-inverse equivalences, followed by generator formulas. These rank orders are not counts of scalar cycle resolvents. The comparison correctly avoids identifying those two quantities. [Theorem 2.1 and equation (2.3)](https://arxiv.org/html/2308.02701).

## 4. Independent exact rank-one reformulation

This section is a new algebraic verification of the supplied Q11 formulas, not a claim that an external source states Q11.

Write p=c_41, z=c_02, t=c_42, v=c_43, u=c_03; let x0=c_01. Set

a=vz-ut, d(x)=pz-xt, b(x)=pu-xv,
Q(x)=[[0,1],[a/d(x),b(x)/d(x)]].

For d(x)d(x0) nonzero, direct subtraction gives

Q(x)-Q(x0)=[(x-x0)a/(d(x)d(x0))] e2 [t,-p].

The bottom-left numerator is a(d(x0)-d(x))=(x-x0)at. The bottom-right numerator is b(x)d(x0)-b(x0)d(x)=-(x-x0)ap. Both are exact polynomial identities. Thus, with P=Q4Q3Q2 and R=Q0 fixed,

M(x)=M(x0)+theta(x)(P e2)([t,-p]R),
theta(x)=(x-x0)a/(d(x)d(x0)).

This is a fixed-direction rank-one update with a fractional-linear parameter, on the guarded nonpole locus. For any square A, det(A+theta UV^T)=det(A)+theta V^T adj(A)U; in this 2-by-2 case the reviewer independently expands the identity over an integer polynomial ring. Taking A=M(x0)-rI shows why the characteristic equation is affine in theta. In Q11's physical entry x, clearing d(x) produces the displayed affine H(x). The characteristic slope, replacement-window divisor, nonzero second eigenvalue, distinctness, and Green denominators still need their separate guards. General spectral assignment does not supply them automatically.

Merzel–Mináč–Nguyen–Pasini prove base-field characteristic-polynomial assignment by rank-bounded perturbations, using rational canonical form. Their perturbation direction is unrestricted. [Theorem 1 and §3, pp.867,871–872](https://files.ele-math.com/articles/oam-17-58.pdf). Gernandt–Trunk distinguish parameter-restricted pencil updates and use the determinant identity; their adjustable vector and complex/real hypotheses differ from Q11's fixed rank-one direction. [§6, Proposition 6.1 and Theorem 6.3](https://arxiv.org/html/1604.06671). These comparisons support attribution of the mechanism without asserting an immediate specialization of their full existence theorems.

## 5. What is classical and what is separately certified here

The finite geometric-series inverse of a weighted cycle, low-rank state-space compression with corrections, determinant-based spectral assignment, reversal bookkeeping, and the nilpotent formula (I-eE_01)^(-1)=I+eE_01 are classical ingredients or elementary algebra. They should not be promoted individually as new general methods.

Q11's accepted certificate combines those ingredients for the exact arithmetic input: a one-entry change with nonzero affine slope, split base-field monodromy, legal forward/reverse branches, and a third source-legal branch containing both the entry correction and all five diagonal calibrations. Its local-ring proof establishes every required division and nonvanishing condition uniformly in the admitted q family. The construction uses rational functions of the matrix entries, not a requirement that the entries themselves be rational numbers. The recipe can apply to other inputs on its guard locus; the Fourier/chirp-specific certification is the proof that this entire stated family lies there.

Neither a sample success nor nonmatch to these named papers proves novelty. A broader predecessor need not mention C_q, 241, or this particular recipe to imply the result. It would need an explicit model-preserving specialization guaranteeing the original field, the exact additive branch grammar and count, and the complete admitted family. No such implication was identified in the inspected theorem portions. Citation chains and the noted cyclic-rank-completion lead remain unexhausted. Historical priority therefore stays unresolved.

## 6. Independent controls, cost boundary, and disposition

check_bridges.py is newly authored and imports only standard-library modules. It proves the two Q-difference numerators and the 2-by-2 adjugate determinant identity by exact symbolic polynomial expansion. It also verifies W^5=hI and the inverse numerator identity for all 24 directed structural cycles with formal edge weights. Because those are polynomial identities, zero-weight specializations remain included. A separate prime-field reconstruction verifies the rank-one formula for all 240 nonpole parameter values; the pole is 157, with x0=20, a=57, d(x0)=188. These controls test the reformulation and attribution mapping; they do not rerun or replace the accepted full arithmetic-family proof or lower certificate.

No literature operation count is transferred to Q11. Its accepted setup remains paid, its application is fixed dimension five, and its degree-four coefficient bit bounds do not hide ambient-root representation/conversion cost. Fast application of supplied generators is distinct from constructing them or writing a dense inverse. A branch formula or a low CSS state rank gives no full-B_N algorithm or FFT speedup.

Accept the comparison as a bounded attribution addendum. The accepted mathematical result and broader open obligations remain as stated. No novelty or priority conclusion follows. The original mathematical ZIP and seal are unchanged.
