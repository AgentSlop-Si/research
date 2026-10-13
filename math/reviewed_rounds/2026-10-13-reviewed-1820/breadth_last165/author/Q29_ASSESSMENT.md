# Q29 small ramified normalization calibration: candidate only

## Useful result

For q a primitive 27th root, n=13, U(z;q)=H13(z;q)/(z+1), and the ordinary z-discriminant D(q), fresh exact field arithmetic gives

    v_pi(D(q))=174,  pi=q-1,  v_pi(3)=18.

The exact characteristic-zero polynomial multiplicity at q=1 is 66. Thus the intrinsic normalized element Delta(q)=D(q)/(q-1)^66 has

    v_pi(Delta(q))=108.

Both D(q) and Delta(q) are nonzero; neither normalized element is a local unit at the stated exponent until its full intrinsic power is removed. This is a t=1,p=3,e=3 finite calibration, pending independent review. It does not establish the open t=27,p=5,e>=3 normalization, any all-layer squarefreeness, global unitness, an algorithmic improvement or historical novelty.

## Source boundary

The accepted Q29 split review allows t any positive odd integer, p odd with p not dividing t, and e>r>=1. It explicitly distinguishes ordinary polynomial normalization, actual higher-root specialization, and intrinsic DVR valuation. Its t=1,p=3,e=3 use is an exact quotient-parity countercontrol, not an exact ordinary-discriminant valuation. The current parent asks for newly justified higher-layer normalization or a precise obstruction. This small slice is a calibration of that interface, not a substitute for the still-open main tower.

The accepted order675 values 2862 and1080 are not used or replayed. The accepted obstruction that the old order675 normalization vanishes at higher t27,p5 layers remains closed. No purported transfer of those coefficients is made.

## Exact calculation

A new q-Pascal implementation constructs the full H13 polynomial directly in Q[q]/(q^18+q^9+1). Exact division by z+1 has zero remainder. U is monic of degree12. Its ordinary derivative resultant equals its discriminant because (-1)^(12*11/2)=1.

`Q29_RAMIFIED27_RESULT.json` preserves the complete 18 coordinates of D in the q basis and in the pi=q-1 basis. Phi27(1+pi) is Eisenstein at3, so Z3[q] has uniformizer pi and ramification18. If D=sum_(i=0)^17 a_i pi^i with integer a_i, its nonzero summand valuations are 18v3(a_i)+i. Distinct i have distinct residues mod18, so a unique minimum cannot cancel. The minimum is174, at i=12 with v3(a_12)=9. The next minimum is175. This establishes the reported intrinsic valuation of the computed element.

## Exact ordinary normalization exponent

Use the classical degree recurrence

    H_n=(1+z)H_(n-1)-z(1-q^(n-1))H_(n-2).

Set q=1+u² and z=-1+uY. Induction on the recurrence gives

    u^(-n)H_n(-1+uY;1+u²) → He_n(Y),

where He_n=Y He_(n-1)-(n-1)He_(n-2). For n13 the persistent factor z+1=uY is exact, so the normalized U tends to L(Y)=He13(Y)/Y. Its polynomial is

    Y^12-78Y^10+2145Y^8-25740Y^6+135135Y^4-270270Y²+135135.

Its ordinary discriminant is nonzero (complete integer in the control JSON). Scaling twelve roots by u multiplies their discriminant by u^132, exactly (q-1)^66. Therefore ord_(q-1)D=66, with leading coefficient Disc(L), and exact monic polynomial division yields an integral quotient in Z[q]. Specializing at the actual primitive27 root subtracts66 from174, giving108.

The leading coefficient has v3=33. Multiplying that content by ramification and adding the ordinary exponent would predict660, which is wrong. The actual value174 supplies a small explicit calibration of the source's warning that later polynomial coefficients can dominate the intrinsic valuation. This illustrates the distinction; it is not a new general obstruction method.

## Alternate controls

- H13 is also constructed by the degree recurrence modulo three primes (109,163,271), for all18 primitive27 roots in each:54 ordinary discriminant controls match the saved field vector.
- An independent multiplication-matrix determinant of that field vector computes its exact rational norm, with v3(norm)=174, agreeing with the unique-prime DVR calculation.
- Exact Hermite recursion verifies the degree12 initial form, its nonzero discriminant, and leading-coefficient v3=33.

These are alternate calculations by the same worker, not independent review. No historical scientific script was executed. The exact field vector, norm, modular controls and scripts are included for a separate reviewer.

## Exact next task and stop

Independently reconstruct U13 and its ordinary resultant, check the unique 3-adic component and Eisenstein basis valuation, and verify the exact Phi1 multiplicity66 by the recurrence scaling argument. Stop at scoped acceptance or an exact mismatch. Preserve the distinction between this t1 calibration and the main t27,p5 higher-layer problem. Q29 and its shared NEXT-RS-AUGMENTED parent remain OPEN54 with no score increase.
