# E25 on the accepted generic fixed-F11 chart

Status: author-side exact candidate. Independent acceptance is required.

## Bounded result

On the accepted regular H != 0, A != 0 piece, original retained residual E25 is equivalent to the explicit necessary polynomial N2(b,e) = 0 stored in CERTIFICATE.json. N2 has 370 nonzero terms and multidegree (19,39). It admits the checked identity

    N2(b,e) = b^10 e^3 H(e) core(b,e).

The three removed factors are already nonzero on this piece: b is an accepted additional guard, e=x83 is an original guard, and H is an explicit branch condition. Thus E25 is also equivalent there to core(b,e)=0. The core has 340 terms and multidegree (9,33).

This is an additional explicit necessary equation in the accepted two-input piece. It is not a new global two-input theorem, a dimension theorem, a feasibility certificate, or a nonzero-constant contradiction. All 50 original residuals, all 19 original guards, every accepted extra condition, and every prior cancellation exclusion remain compulsory. The A=B=0 exceptional piece is retained unchanged, as are the separate H=0 and other accepted atlas conclusions outside this calculation.

The direct core is not affine in either b or e. The bounded attempt produced no further guarded linear solve or contradiction. No irreducibility, absence of linear factors, or impossibility of another elimination is claimed.

## Trust boundary and source selection

Use K=Q[zeta]/(1+zeta+...+zeta^10), or any field extension, and b=x11, c=x34, q=x41, e=x83. The accepted affine-q packet is research_cycle_2304/regular_hnonzero_analysis/CANDIDATE.json, independently accepted by research_cycle_2310/hnonzero_continuation_review/RECEIPT.json with SHA-256

    22e0babbd1d637a38a355bed333317fb1f38c98057403715374fcdd066880d9e.

The four pinned input files and their digests are in CERTIFICATE.json. The accepted historical chart/reconstruction theorem and the accepted prior rational-coordinate identities are the explicit trust boundary. No historical program was executed or imported.

E25 is a still-retained residual, distinct from the E5, E22, E35 and E41 relations used for the present chart. Its source polynomial is read directly from the pinned original guarded-reduction certificate, at content address

    ce2413e7d1b9e31c5372467e1d12115510d1385a73052fbb0e9c005b1d7ca841.

It has 55 terms and support {x11,x22,x25,x34,x39,x41,x49,x65,x83,x88}. The source content address is recomputed from its actual coefficient rows. The exact accepted bindings x22=1 and x49=zeta-c are used. For x25,x39,x65,x88, the already independently accepted four-variable rational-coordinate ledger is used. E25 uses neither x0 nor x92, so this calculation makes no representative replacement or assumption that x0=0.

## Exact construction

For each coordinate v used by E25, write its accepted value as n_v/d_v. If m_v is the largest exponent of v in the original E25, form the completely uncancelled pair

    D_raw = product_v d_v^m_v,
    N_raw = sum_terms coefficient * product_v n_v^exponent(v) d_v^(m_v-exponent(v)).

Fresh arithmetic gives 391 terms in N_raw, with multidegree (7,4,4,5), and 54 terms in D_raw, with multidegree (5,2,3,4), in the order (b,c,q,e). The polynomial certificate supplies N4,D4,T with exact identities

    N_raw = N4*T,
    D_raw = D4*T.

N4 has 118 terms and multidegree (5,4,2,3); D4 has six terms and multidegree (3,2,1,2); T has twelve terms and multidegree (2,0,2,2). Nothing depends on these being maximally reduced or on a gcd claim. Both multiplication identities are independently recalculated by the fresh checker.

The accepted c substitution is c=cn/cd with cd=b*H. The accepted q substitution on the present piece is q=-B/A. The polynomials cn,cd,A,B are taken unchanged from the accepted packet. Define

    N3(b,q,e) = cd^4 * N4(b,cn/cd,q,e),
    N2(b,e)   = A^2 * N3(b,-B/A,e).

Four and two are the exact respective c- and q-degrees; the checker verifies them. N3 has 207 terms and multidegree (9,0,2,15). N2 has the stated 370 terms. Every coefficient of both clearing identities is checked exactly. The data keep the uniform four-exponent encoding (b,c,q,e); the checker requires every N2/core c- and q-exponent to be zero.

On the guarded chart, the full rational identity is therefore

    E25 = N2 / [A^2 * cd^4 * D4(b,cn/cd,-B/A,e)].

No factor is silently deleted from N2. The further identity N2=b^10*e^3*H*core is checked by multiplication and stripped only using existing nonzero conditions.

## Denominator and exception ledger

Every coordinate denominator used in D_raw is nonzero by the accepted affine-q packet and its existing cancellation ledger. Their product D_raw is consequently nonzero after reconstruction. Since D_raw=D4*T in a field, both D4 and T are nonzero at every admissible assignment. This preserves the new cancellation exclusion without requiring a separate feasibility assumption.

The c clearing uses cd=b*H, protected by b!=0 and H!=0. The q clearing uses A only on the explicit A!=0 piece. No division by B is made. Original q!=0 remains mandatory: A!=0,B=0 produces q=0 and is rejected by that original guard. The d!=0 and F_M!=0 regular conditions and the accepted Q_a,F_A,F_B nonzero guards remain unchanged. This calculation does not permit evaluating a cleared polynomial at a forbidden denominator and treating the result as a solution.

The complete accepted generic branch and the complete accepted A=0 exceptional branch are copied as inert records into the certificate and compared exactly by the checker. Adding N2=0 or core=0 to the generic circuit does not remove an admissible solution because E25 was already required; conversely, these necessary equations do not replace any retained test or certify a solution by themselves.

## Bounded search and limits

A direct four-variable multivariate gcd attempt was stopped without using its result. A successful replacement performs exact divisions by explicitly available small denominator factors and certifies only the two resulting multiplication identities. An initial q-clearing implementation was stopped for redundant repeated power computation; the successful run caches those powers. These implementation stops have no mathematical consequence.

A full factorization attempt on N4 was stopped without a result. A separate optional factorization of the guarded core was limited to 180 seconds; no successful factorization is assumed in the theorem. A small exact univariate-content check of A and B found only e as their shared coefficient content, but this exploration is not required or used by the certificate. No numerical roots, finite-field feasibility inference, Groebner basis, resultant, external write, or ranking change was used.

The bounded continuation ends here. The core need not be the best or smallest available equation; the remaining residual feasibility problem and the retained A=B=0 exception are unresolved.

## Reproduction

From the workspace root:

    python research_cycle_2325/f11_generic_residual/check_fresh.py

The checker uses newly written standard-library integer/rational ten-coordinate arithmetic and sparse polynomial operations, with exact cyclic convolution followed by reduction modulo Phi11. It reads only inert historical JSON. Deliberate coefficient, clearing-power, source, branch, guard, exception, cancellation, and unsupported-claim corruptions are rejected without a candidate-hash gate. CHECK_RECEIPT.json records the checks and negative controls. SHA256SUMS.txt and SEAL.json bind this packet; they are not substitutes for independent mathematical acceptance.
