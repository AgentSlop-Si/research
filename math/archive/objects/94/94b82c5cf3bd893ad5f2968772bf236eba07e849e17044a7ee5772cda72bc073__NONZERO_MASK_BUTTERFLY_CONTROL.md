# Additive control: nonzero Green masks for the sixteen-point butterfly layers

10 October 2026. This does not change the earlier sealed construction or extend it to growing sizes.

The two butterfly layers in the explicit N=16 construction can use nonzero Green edges. Choose any scalar alpha not in {0,1,-1}; a primitive fourth root is valid under the dyadic field contract. Let E_12 and E_21 be the usual two-by-two elementary matrices. Then

    F_2 = alpha (I-alpha^-1 E_12)^-1
          + diag(1-alpha,-1-alpha)
              (I-(-1-alpha)^-1 E_21)^-1.          (1)

Both endpoint matrices are nonsingular. Since E_12^2=E_21^2=0, the inverses are exactly I+alpha^-1 E_12 and I+(-1-alpha)^-1 E_21. The first term contributes diagonal alpha and upper-right entry 1; the second contributes diagonal (1-alpha,-1-alpha) and lower-left entry 1. Their sum is [[1,1],[1,-1]].

For a global butterfly with disjoint ordered pairs (a_i,b_i), put the E_12 edges b_i -> a_i in one Green denominator and the E_21 edges a_i -> b_i in the other. The first Hamiltonian cycle may use the order

    b_0,a_0,b_1,a_1,...;

the second may use

    a_0,b_0,a_1,b_1,... .

Set the weights on the displayed matching edges to alpha^-1 and (-1-alpha)^-1, respectively, and every other cycle weight to zero. Each cycle is Hamiltonian, the matching edges are nonzero, each denominator's nonidentity part squares to zero, and the full cycle-weight product is zero. Thus every Green guard is exactly 1.

Use alpha I as the first left endpoint. The second left endpoint is diagonal, with 1-alpha on the a_i coordinates and -1-alpha on the b_i coordinates. Both right endpoints can be I. Equation (1) then holds independently on every pair. Any outside monomial prefactor or postfactor is absorbed into the corresponding endpoints.

This replaces the zero-mask realizations of the two actual butterfly cores inside H_1 and H_2 of `CHANGING_INTERFACE_CONSTRUCTIONS.md`. It leaves H_1,H_2, Q, and the exact F_16 product unchanged, while making both Green terms in those two layers use N/2 nonzero edges. The padded monomial H_3,H_4 may remain as originally specified. Every route, endpoint, and mask has an O(N) generator; applying the matching Green inverses costs O(N) because their nilpotent parts have square zero.

This is a literal nonzero-mask admissible control, still implementing the familiar small FFT. It does not compress additional butterfly stages or contradict the earlier obstruction to extrapolating the zero-mask family. No all-nonzero Hamiltonian cycle, large-size Green factorization, or new Fourier speedup is claimed.

`verify_nonzero_butterfly.py` checks the Hamiltonian routes, legal nonzero endpoints, nonzero matching masks, nilpotent inverse identities, and exact butterfly sums over F_65537. The controls are newly authored and execute no uploaded code.
