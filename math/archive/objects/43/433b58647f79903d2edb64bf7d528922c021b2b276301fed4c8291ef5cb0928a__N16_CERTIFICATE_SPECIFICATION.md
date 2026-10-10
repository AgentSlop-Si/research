# Proposed bounded exact coefficient gate at N=16

This is a proposed restricted seed model and certificate, not a successful Fourier construction. It is separate from the frozen Hamiltonian geometry milestone.

## 1. Fix the model before any search

Take N=16, m=q=4. Use the deterministic cycle arrays from the geometry constructor in its fixed label order H0-,H0+,H1-,H1+,V0-,V0+,V1-,V1+. Set the corresponding fixed rational poles tau_j=1/(j+2), j=0,...,7. Define

    G_j=(I-tau_j P_j)^(-1).

Their denominators 1-tau_j^16 are nonzero over characteristic zero. Distinct poles avoid collapsing equal small-size cycle arrays into duplicate matrices.

Let B=diag(F4,F4,I4,I4), using the unnormalized F4 with i=ζ16^4. This fixes the half-active bank J={0,1} and its placement. Write

    H_l=sum_(j=0)^7 diag(a_(l,j))G_j,  l=1,2,3,
    C=H3 H2 B H1.

There are exactly24 Green occurrences and24*16=384 endpoint entries. The right endpoints are fixed identities, edge weights are fixed poles, cycle orders and bank are fixed, and the384 left entries are the only searched coefficients. Require each left entry to be nonzero for this first branch. No layer or parameter is omitted from the ledger. A valid identity automatically makes each H_l invertible because B and F16 are invertible.

This is deliberately narrower than allowing arbitrary edge weights or two independent endpoint diagonals. Failure here would reject only this branch. It cannot exclude the general eight-order architecture.

## 2. Minimal direct exact certificate

Work in K=Q[z]/(z^8+1), with z=ζ16, and check all256 entries of

    C[i,j]=z^(ij), 0<=i,j<16.

They are cubic equations in the384 endpoint entries. The pole denominators are fixed rational units. Require all384 supplied values nonzero; a polynomial system may encode this by saturation or one inverse witness for their product. If a search finds values outside K, supply an explicit algebraic extension with a minimal polynomial and an isolating embedding, or an exact field specification adequate to verify every equality. Decimal residuals alone do not certify a seed.

Equivalently check the16 seed entries C e0=1 and240 successor entries

    C[i,j+1]=z^i C[i,j], 0<=j<15.

These256 conditions are sufficient; the wrap relation follows from z^16=1. The seed must not be dropped. This is a complete global certificate rather than a cut, spectral, or local-rank test.

## 3. Eliminate the outer128 coefficients exactly

For fixed inner parameters define X=H2 B H1. For each output row i form an8-by16 matrix T_i whose jth row is row_i(G_j X). The outer row equation is

    a_(3,:,i)^T T_i = row_i(F16).

Choose an8-column pivot set K_i for which det(T_i[:,K_i]) is nonzero. Solve the8 pivot equations exactly, then check the remaining8 entries. Across all16 rows this eliminates128 outer variables and leaves128 full compatibility residuals in256 inner parameters. Keep every pivot guard and every reconstructed outer nonzero guard.

The choice of a pivot chart must be recorded. If the selected chart is singular, try another verified chart or report that chart's failure; do not treat it as nonexistence. A rank-deficient T_i must be handled with its actual exact rank and corresponding consistency equations. For invertible X, the template rank control below ensures rank(T_i)=8. Directly checking all256 entries remains the simplest final verifier regardless of how parameters were found.

Keeping all384 variables yields cubic equations. Clearing the rational outer solve generically yields degree16 equations in the256 inner variables: T_i entries are quadratic, and an8-by8 determinant has degree16. Thus variable elimination does not automatically make solving easier. The degree increase must not be hidden.

## 4. Why start at16 rather than4 or8

Fresh exact controls over F998244353 find full row-template rank N at N4 andN8 for these distinct poles, and rank8 in every row at N16,32,64. Pole denominators were checked nonzero. A full-rank modular minor implies the corresponding rational minor is nonzero in characteristic zero. Thus N4 andN8 already let one row-masked eight-term layer span an arbitrary row if zero coefficients are allowed. Such a tiny seed gives little structural evidence for this model.

N16 is the first dyadic size with eight fixed row templates for sixteen target entries. Its geometry has only six distinct cycle arrays but eight distinct Green templates because the poles differ. The seed still has more parameters than Fourier entries and is not expected to prove an asymptotic recursion by itself. The preserved `check_n16_outer_gate.py` regenerates these controls in `N16_OUTER_GATE_RESULTS.json`; `TEMPLATE_DIAGNOSTIC.json` is the earlier matching diagnostic.

## 5. Bounded first test and controls

Before numerical fitting, implement the exact full-entry verifier and outer-row consistency gate. Test it on a product generated from supplied admissible coefficients, which must pass, and on a changed target entry, which should fail whenever outside the row span. Test a wrong or missing seed separately.

A narrowly bounded initial rejection test can fix the256 inner coefficients to1 and leave all128 outer coefficients free. A nonzero9-by9 augmented minor of [T_i;row_i(F16)] proves impossibility for that fixed inner prefix. A finite-field nonzero minor proves characteristic-zero nonvanishing when denominators and the cyclotomic specialization are valid; it must come with the actual minor and exact modular determinant. Such a result would not reject any other inner coefficients.

The implemented checker performs these exact finite-field verifier controls and supplies a characteristic-zero negative certificate for the fixed all-ones inner prefix, using explicit nonzero augmented minors. It is not an acceptance verifier for arbitrary characteristic-zero algebraic candidates. Such a candidate would still need the exact field arithmetic specified in section2.

Do not begin an unbounded floating-point search. A subsequent search should state its finite parameter family or polynomial system, exact guards, allotted search domain, and stopping condition. A successful finite seed would still need a size-lifting rule preserving all entry equations and the active-bank budget, plus a charged uniform coefficient generator.
