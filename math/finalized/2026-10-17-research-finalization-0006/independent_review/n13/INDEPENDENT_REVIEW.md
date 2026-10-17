# Independent acceptance: N13 quadratic and cubic sixteen-bank minima

17 October 2026 UTC. **ACCEPT within the original free-cross-singleton bank grammar.** This is an assistant's independent exact-arithmetic review, not independent human review or formal verification.

## Accepted result

For N=13, q=16 and characteristic 53, let B(K) count physical signed resolvent banks, with parameters and raw weights in K and exactly one effective alpha node in each cross orientation, at independently free locations. Then

- B(F_(53^2))=B(F_(53^3))=B(F_(53^4))=16.
- The least positive finite extension degree attaining sixteen is 2.
- Equality holds whenever the extension degree is divisible by 2 or 3. The earlier accepted quintic witness additionally covers multiples of 5.

This is a sufficient divisibility condition, not a complete field classification. The prior B(F53)=18 remains unchanged. No unrestricted-cross optimum, other-q or characteristic statement, novelty or priority conclusion, arithmetic speedup, or all-length FFT improvement follows.

The author report at SHA256 `6801e87679da1b71c327827becd9ac2bb85d3345446883eb651afac703cc9a9c` has the correct scope. Its discovery equations and displayed base-field factorizations also pass separate fresh checks. The selected eleven-file author manifest was checked for byte integrity; mathematical acceptance attaches specifically to the frozen literal certificates below, not to untested search exhaustiveness.

## Exact original operator

Indices are modulo 13. The literal target is F[k,t]=16^(-kt), with S e_t=e_(t+1) and T e_t=16^t e_t. Each physical bank is

    (1/13) sum_(j=0)^12 w_j
      (I-alpha S^epsilon-beta 16^(epsilon delta j) T^delta)^(-1),
    Delta=1-alpha^13-beta^13 != 0.

The signs epsilon and delta independently belong to {+1,-1}. There is no target conjugation, pre/post map, new generator, product of banks, derivative node, singular limit, infinite node, trace-valued replacement bank, or implicit extension beyond the stated coefficient field.

The accepted lower theorem permits arbitrary legal beta, repeated physical banks and cancellations. The two new upper witnesses choose beta=1, which is a witness specialization rather than a restriction on competing lower-bound representations. Nodes may coincide across different orientations; within each same-sign orientation all seven are distinct and nonzero. Each bank has a nonzero full sector-amplitude vector and a nonzero literal matrix. Physical and effective allocations are both (7,1,1,7).

## Field and literal certificate verification

The quadratic field is F53[u]/(u²−2); the cubic is F53[v]/(v³+40v²+25v+11). The verifier checks that 53 is prime, that 16 has exact order 13, and that neither modulus has a root among the 53 base-field residues. For degrees two and three, absence of a base-field root proves irreducibility. Consequently these are fields rather than possibly reducible quotient rings.

The verifier independently evaluates every supplied support root, checks seven distinct nonzero roots on each side, and checks the field encodings and all nonzero inverse guards. Monicity and the seven distinct roots identify each displayed degree-seven annihilator exactly.

Frozen accepted author certificate hashes:

- QUADRATIC_LITERAL_CERTIFICATE.json: `a68775988c19040d2a1ca53bde75ed68ead00d2f369d95da4f47ab59680c515c`.
- CUBIC_LITERAL_CERTIFICATE.json: `0b4e2d1087c5191469d97a50a5103920501426ec9b1b3c6917ce419073bfb3eb`.

The main reviewer `fresh_raw_certificate_review.py` treats the certificates as inert field parameters and raw weights. It does not import or execute producer or historical programs, nor trust supplied inverse matrices or aggregate entries. It solves the original cyclic branch equations by affine recurrence, independently of the author's Gauss–Jordan route:

    d_r x_r-alpha x_(r-epsilon)=b_r,
    d_r=1-beta 16^(epsilon delta j+delta r).

Traversing r=0,-epsilon,... expresses x_0 after one cycle as A x_0+B. The nonzero closure denominator gives x_0=B/(1−A), then all other coordinates. This is performed on each of the thirteen basis right-hand sides. Separate original sparse left and right products verify both inverse identities entrywise.

For each of the two frozen certificates, all of the following pass:

- 208 original 13×13 branch inverses;
- 416 independent left/right inverse-product identities;
- all 208 raw-weight/normalized-amplitude identities, with the original 1/13 factor and gamma=7;
- 2,704 independently extracted bank Weyl coefficients;
- all sixteen bank matrices and effective amplitude groups nonzero;
- exact orientation/alpha support and both cross-singleton constraints;
- all 169 entries of the aggregate equal to the original negative-sign Fourier matrix.

Thus the literal operator equality holds on every vector over the corresponding field. This is not merely quotient-sector consistency, a forced-window test, or a random-input sample.

Falsification controls reject omission of 1/13 (169 mismatches), reversal of the Fourier sign (144), perturbation of a raw branch weight (91), and deletion of any individual bank. The exact deletion counts are retained in the receipts.

Before seeing the author's raw quadratic weights, a separate fresh route in `fresh_literal_review.py` enumerated all roots in F53[u]/(u²−2), solved the actual 13×16 root-sector systems, derived its own raw weights, and directly inverted the original matrices by Gauss–Jordan elimination. Its independent witness also passes all original-matrix checks. Different free choices and root ordering give different valid raw weights; equality of those raw weights is neither asserted nor required.

## Matching lower bound and minimum degree

The accepted [base-field exact-eighteen review](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/finalized/2026-10-15-frontier-boundaries/n13_eighteen_independent_review_2034/INDEPENDENT_REVIEW.md), SHA256 `71351352c1840c41ec64ead3e2ece3fb36905518a5163c18662ea12194f85281`, explicitly uses this same original q=16 bank grammar, independently free cross-singleton nodes, and arbitrary legal beta. It binds the accepted universal lower review SHA256 `896200e3b4b12d56dd13ac1d87b5e6ea64ef3283e77887898bb595d1bf304b6f`.

I reread the original lower proof's arbitrary-beta expansion, effective-node bookkeeping and polynomial-minor conclusion. Its all-characteristic-53 lower bound requires at least seven nonzero effective nodes in each same-sign orientation, plus the two cross groups, hence sixteen physical banks. These statements are inherited accepted dependencies; their historical programs or complete censuses were not rerun in this review.

The literal upper certificates therefore match B(K)>=16 in exactly the same model. Degree 1 is excluded by B(F53)=18, while degree 2 is attained, proving the minimum degree 2. Standard finite-field embeddings carry the quadratic witness to every degree divisible by 2, including 4, and the cubic witness to degrees divisible by 3. The independent original inverse guards remain nonzero under an embedding. No claim that the quadratic field embeds into the cubic field is made.

The prior pinned y=z=1 field criterion is untouched: the quadratic witness has (y,z)=(14,43) and the cubic has (3,3). Neither is obtained by silently normalizing free cross nodes to one.

## Publication and table scope

The author's sixteen dated prefixes for existing overview G/J/P/Q cells on rows 10–13 are accepted, subject to replacing publication placeholders only by verified report/review URLs and immediate prewrite/readback guards. Independent native reads matched all sixteen exact preimages and the four stable IDs; every parent was TO RESEARCH at priority 56. Every proposed postimage preserves its complete previous text as a suffix.

Preserve rich text, chip offsets, notes and unrelated formatting. There is no new row, status, score, classification or census change. The four parent views remain open. The exact degree-2/3/4 and minimum-degree questions must no longer be presented as open, while remaining field classification, unrestricted allocations and paid shared evaluation remain separate.

No external write was performed by this reviewer. Only fresh reviewer programs were executed. Fresh finite checks establish this fixed explicit certificate; they do not establish a global search census or a new lower theorem.
