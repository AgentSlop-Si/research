# Cubic split does not yield the proposed twelve-bank representation

14 October 2026. Author certificate, pending independent review.

## Result

The fixed twelve-bank construction fails over E=F23[u]/(u^3+13u^2+13u+13), with N=11 and q=13. Both cross-sign nodes are 15, and the proposed five-node support for each same-sign orientation is

    X={3,21,u,13+20u+14u^2,20+2u+9u^2}.

The last three nodes are u,u^23,u^529. All five nodes are distinct and nonzero. Their product polynomial is

    h(t)=t^5+12t^4+17t^3+14t^2+t+14
        =(t-3)(t-21)(t^3+13t^2+13t+13).

The full original coefficient systems are inconsistent in sectors b=3 and b=8. In b=3, the coefficient matrix has rank 10 and its augmented matrix has rank 11. Passing the five central moment-window tests therefore does not suffice for full-bank attainment.

More strongly, the b=3 obstruction is independent of every -- node and its bank count. With the ++ support contained in X and the two cross nodes fixed at 15, adding or changing -- banks cannot repair the failure. Arbitrary legal beta choices cannot repair it either. This is a support-specific obstruction, not an extension-field minimum theorem. It does not rule out different cross nodes, different ++ support, or an unrestricted orientation allocation.

## Original grammar

The only permitted summands are

    B_(e,d)(alpha,beta;w)
      =(1/11) sum_(j=0)^10 w_j
        (I-alpha S^e-beta*13^(edj)T^d)^(-1),
    Delta=1-alpha^11-beta^11 != 0,

where S e_t=e_(t+1 mod 11), T e_t=13^t e_t, and F[k,t]=13^(-kt). The literal branch test uses beta=1, so Delta=-alpha^11 is nonzero for every listed node. No new generators, coordinate transformations, pre/post maps, or products are introduced.

All code executed for this task is newly authored in fresh_cubic_gate.py. Historical programs were read only as inert evidence and were never executed, imported, or compiled. No external service was written.

## Exact obstruction

The Weyl coefficient of a matrix M is

    c_M(a,b)=(1/11) sum_(t=0)^10 M[(t+a) mod 11,t]*13^(-bt).

Direct extraction from the literal target gives c_F(a,b)=18 f(a,b), where f(a,b)=13^(3(a+b)^2). Word enumeration independently reconstructs the Gaussian factors G_(e,d)(a,b) and the vanishing of every mixed coefficient at word length eleven.

For b=3, take the prime-field vector, indexed by a=0,...,10,

    lambda=(0,1,12,18,8,12,2,12,1,0,0).

It satisfies lambda^T M_3=0 for all twelve proposed coefficient columns, but

    lambda^T f_3=11 != 0 in F23.

Equivalently define the literal-matrix functional

    L(M)=(1/11) sum_(a=0)^10 lambda_a
                    sum_(t=0)^10 M[(t+a) mod 11,t]*13^(-3t).

Then L(F)=18*11=14 != 0, while L vanishes on every one of the 132 literal inverse branches. Since a bank sum is a linear combination of those inverse branches, no choice of the 132 raw weights can produce F. This is an exact inconsistency certificate, not a failed numerical solve.

## Precisely what the obstruction depends on

Define the orientation polynomial

    P_(e,d)(x)=sum_a lambda_a G_(e,d)(a,3) x^([ea]_11).

Fresh exact arithmetic gives, with coefficients interpreted modulo 23,

    P_++(x)=h(x)*(9x+21x^2),
    P_-+(x)=4x^3+10x^4+19x^5+13x^6+21x^7,
    P_+-(x)=2x+6x^2=6x(x-15),
    P_--(x)=0.

Both cross polynomials vanish at x=15. P_++ vanishes at every node in X. For --, G_--(a,3) is supported only at a=0,9,10, and lambda is zero at those three coordinates. Therefore P_-- vanishes identically, independently of the chosen -- nodes or how many occur.

For arbitrary legal beta, the b=3 branch coefficient contains the scalar beta^[d*3]_11/Delta, the phase scalar 13^(e*3*j), and the same polynomial P_(e,d)(alpha). No division by beta is used. Thus the above annihilation remains valid for arbitrary legal beta and arbitrary raw weights. Repeated same-node physical banks and canceled amplitudes do not escape it. The proof remains a necessity argument for the declared alpha supports, and does not establish any minimum in a larger domain.

## Exact verification coverage

- The cubic has no root in F23, hence is irreducible; the quotient is a field of size 12167.
- All three Frobenius conjugates and all five quintic roots were checked exactly.
- All 121 target Weyl coefficients were extracted from the literal target matrix.
- Noncommutative words through length 11 were directly enumerated in each orientation.
- All eleven full coefficient systems were tested, with ranks

      (11,7,9,10,11,11,11,11,10,9,7).

  Exactly sectors 3 and 8 were inconsistent.
- All 132 original 11-by-11 literal inverse branches were separately constructed and inverted.
- All 264 left/right inverse-product identities were checked.
- The displayed functional was evaluated directly on every inverse matrix, giving zero 132 times, and directly on the target, giving 14.
- A second polynomial long-reduction implementation checked 182 distinct field elements occurring in support and inverse entries, including multiplicative inverses.
- Six mutation controls were rejected: perturb lambda; use zero lambda; corrupt an inverse entry; substitute support node 3 by 1; admit alpha 0 with beta 1; change the cubic modulus constant term.
- A cold replay reproduced RESULTS.json, FAILURE.json, BRANCHES.json, and MUTATION_CONTROLS.json byte for byte.

No raw weights were recovered, no twelve nonzero bank sum was constructed, and no aggregate-entry witness comparison was claimed. Those stages are impossible for these inputs because the full raw-weight span is already excluded by L.

## Scope and lower-bound sources

The current parameter-gate source reports an extension-field rank-five obstruction and classifies degree-five window annihilators. This task uses only its proposed y=15 support, then independently checks that support and the full-bank failure. It does not independently establish that source's all-parameter theorem or combine it into a minimum claim. The accepted free-singleton F23 minimum 14 is a separate base-field result and cannot simply be transferred to E.

No claim is made about characteristic-zero lifting, historical novelty, asymptotic runtime, FFT speed, or other allocation minima. A new independent reviewer must approve the parameter classification and this full-sector certificate before any stronger combined inference is accepted.

## Reproduction and timing

Run only the fresh program:

    python3 -I cubic_twelve_failure_candidate/fresh_cubic_gate.py --out cubic_twelve_failure_candidate/reproduced

The candidate code imports only Python standard-library modules. Input records, matrices, exact certificates, controls, source hashes, UTC timing, and cold-replay comparisons are included. The initial exploratory run correctly found b=3 inconsistency; the completed run checked all eleven sectors and all literal branches. No computational exception or failed assertion occurred. Model token usage is unavailable.

Task started at 2026-10-14 01:36:58 UTC. Arithmetic-run timings are in outputs/TIMING.json and cold_replay/TIMING.json. The complete final run took about 0.56 seconds; that is arithmetic wall time, not total reasoning time.
