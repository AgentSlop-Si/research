# Fresh exact coefficient audit (17 October 2026)

These scripts were written independently for this audit. No Python code from the uploaded ZIP archive was executed or imported.

## What is computed

`check_exact.py d A b` uses the Rogers–Szegő recurrence

H_(k+1) = (1+z) H_k - z(1-q^k) H_(k-1), H_0=1, H_1=1+z,

at q = w(1+t), in the exact field Q(w) with w represented modulo Phi_d and with formal power series retained modulo t^(M+1). Here M is the claimed order. It then computes the actual ordinary discriminant independently of the claimed coefficient formula:

- If n=2m, write H_n(z;q)=z^m R(z+z^(-1);q). The identity used is Disc_z(H_n)=R(2) R(-2) Disc_x(R)^2.
- If n=2m+1, first divide exactly by z+1, then write H_n/(z+1)=z^m R(z+z^(-1);q). The identity used is Disc_z(H_n)=R(2) R(-2)^3 Disc_x(R)^2.
- Disc_x(R) is computed as the determinant of the ordinary Bezout matrix of R and its ordinary derivative R'. After the boundary valuations v_+=ord_t R(2) and v_-=ord_t R(-2) are actually computed, the determinant precision is reduced to k+1, where k=(M-v_+-e v_-)/2 and e=1 or 3 according to parity. Its actual first nonzero coefficient must occur at k; otherwise the test fails. This calculates exactly the only determinant coefficient needed for the leading term of its square.
- Gaussian elimination uses a pivot of minimum t-valuation in the remaining matrix, allowing row and column swaps. Division is in Q(w)((t)). Because every entry in the remaining block has valuation at least that of the pivot, each Schur update is valid at the original absolute t-precision: the precision loss in division is recovered by multiplying by an entry of at least the pivot's valuation. All pivots have nonnegative valuation. Thus the determinant and final discriminant are correct modulo t^(M+1).
- The script asserts that the first nonzero coefficient is exactly at t^M. It compares that coefficient with C*d^M, where C is evaluated separately from report (22) or (23), including the sign, every power of d, P_A, g^2, Disc(J), Disc(U), and resultant.
- Since q=w(1+t), Phi_d(q) has leading coefficient w*Phi_d'(w). The script divides the independently computed leading coefficient by [w*Phi_d'(w)]^M and checks exact equality with C*(w^(d/p)-1)^M. The tested d are prime powers.

This is an exact local ordinary-discriminant calculation, not a root approximation or an evaluation of the claimed leading coefficient alone. Choosing the precision from the proposed M does not force the result: lower order would be detected, and higher order would make the asserted nonzero coefficient fail.

## Independent full-polynomial controls

`check_full_small.py` computes the entire ordinary discriminant in Z[q] directly using SymPy for seven cases (degrees 3 through 8). It factors out Phi_d by exact polynomial division, verifies its exact multiplicity, and checks the remainder at w. It also compares the entire local Taylor vector through degree M with the reciprocal/Bezout engine. All seven controls pass:

(d,A,b;n,M) = (3,1,0;3,0), (3,1,1;4,1), (3,1,2;5,0), (3,2,0;6,3), (3,2,1;7,5), (3,2,2;8,3), (5,1,1;6,1).

The convention Disc(1)=1 is handled explicitly in the expected report formulas. SymPy's low-level polynomial discriminant reports zero on constants, so using its default there would be an implementation error; the ordinary discriminants of positive-degree H_n and R are unaffected.

## Exact local controls

Each `case_d*_A*_b*.json` contains the exact full reduced coefficient in Q(w), the Phi_d quotient value, auxiliary g/tau/Disc(J), pivot valuations, and elapsed time. These files are generated only after all assertions pass. Relevant cases include residual b=5 with both A=1 and A=2, prime-power d=9 with b=1,2 and A=2, even-residual controls, and A=3 controls.

The source and local outputs are reproducible with Python 3 and SymPy. No floating-point arithmetic is used.

## Short exact examples

In all examples below w is a primitive root of the indicated order and C is the coefficient in (q^d-1)^M, not the coefficient after dividing by Phi_d^M.

- (d,A,b)=(7,2,5), M=9:
  C=2^14*7^34*(136154010969*w^5+333768717734*w^4+444036217221*w^3+383922831985*w^2+198695166061*w+27833431601).
- (d,A,b)=(9,2,1), M=11:
  C=2^18*3^58*(-18*w^5-108*w^4-216*w^3-18*w^2-108*w-215).
- (d,A,b)=(3,3,0), M=9: C=-2^6*3^27. This is a direct check on the negative sign and P_3=108 in the separated formula.
- (d,A,b)=(3,3,1), M=12: C=2^8*3^31*(122*w+109). This checks the quartic J_4 discriminant as well as P_3 in the overlap formula.

For d=7, the actual Phi_7 quotient is checked against C*(w-1)^M. For d=9, it is checked against C*(w^3-1)^M, which is a materially different conversion.

## Scope limit

An optional (d,A,b)=(7,3,5), n=26, M=24 computation was started, then stopped at the reviewer's request because the requested coverage had already been established and this extra exact computation was slower. It was not completed. No coefficient, multiplicity result, or pass is claimed for that optional case. Its partial logs are retained for transparency. The completed A=3 controls are (3,3,0) and (3,3,1).
