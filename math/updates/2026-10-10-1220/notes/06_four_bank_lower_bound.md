# Characteristic zero exclusion of four signed magnetic banks at N equals 5

Version 2026-10-10. This is the N=5 continuation of the accepted signed-magnetic bank model. The proof uses exact cyclotomic identities and holds over every characteristic-zero extension containing a primitive fifth root. The four alpha parameters are unrestricted nonzero elements of that extension. The accepted original source hash and current lower-bound dependency are recorded in PROOF_STATUS.json at the packet root.

## Result

**Theorem.** Let q be any primitive fifth root of unity in a characteristic-zero field. The negative Fourier matrix F[k,t]=q^(-kt) cannot be represented by four signed magnetic banks, with one legal parameter pair in each orientation (epsilon,delta) in {+1,-1}², arbitrary phase weights, and the guard Delta=1-alpha^5-beta^5 nonzero in every bank.

The obstruction persists in the larger class where all five sector amplitudes in each bank are independent. Therefore no choice of beta, Delta, or raw phase weights can evade it. Together with the inherited support gate, this raises the N=5 bank-count lower bound from four to **at least five**. By itself, the exclusion does not determine the minimum beyond that lower bound; the construction in this update supplies the matching upper bound.

The earlier non-unit necessary row ideal at N=5 is not treated as a realization. The new step is to enforce the two actual Fourier coefficients at (a,b)=(0,2) and (0,3), after the exclusive and outer coefficients have fixed the relevant amplitudes. Those additional equations rule out every row-compatible case. The b=0 coefficients never need to be tested.

## 1. Model, normalization, and forced amplitudes

The inherited bank expansion is

R_(epsilon,delta) = sum_(ell=0)^4 h_(epsilon,delta,ell)
  sum_(r=0)^(4-ell) alpha_(epsilon,delta)^r
  [r+ell choose ell]_(q^(epsilon delta)) W_(epsilon r,delta ell),

where W_(a,b)=S^a T^b, S e_i=e_(i+1), and T e_i=q^i e_i. All indices are modulo 5. The Gaussian coefficient uses the indicated root.

The Fourier Weyl coefficients are C q^(4(a+b)²), where C is nonzero. Divide all amplitudes by C. Henceforth the target coefficient is

f(a,b)=q^(4(a+b)²).

The exponent is reduced modulo 5. Put

x=alpha_(++),  y=alpha_(-+),  u=alpha_(--),  v=alpha_(+-),
c=q+q^4,  d=1+q^4.

Each alpha is nonzero, because the corresponding exclusive coefficient at (epsilon,delta) is nonzero. This conclusion holds for every legal bank, including possible degeneracies elsewhere. The primitive-root Gaussian factors used below are also nonzero. In particular c(c+1)=1.

The exclusive points (epsilon,delta) and (2 epsilon,2 delta) force, for any orientation with alpha=a,

h_1=(q³+q+1)/a,
h_2=q²/a².

The amplitudes here have already been divided by C. The certificate obtains these values directly from the Gaussian coefficient formula for each of the four orientations.

## 2. The exact row solutions split into two types

At b=1, the coefficients a=2 and a=3 receive no contribution from delta=-1 banks. Substituting the forced h_1 values gives precisely

x=c y²-q²,
y=c x²-q².                                             (1)

Indeed, the two coefficient residuals are respectively -q^4 times x-c y²+q² and -q² times y-c x²+q². Simultaneous reflection (a,b) to (-a,-b) preserves f and gives

u=c v²-q²,
v=c u²-q².                                             (2)

Subtracting the two equations in either pair gives

(x-y)(1+c(x+y))=0.

Thus each pair is of one of the following types:

- Diagonal: x=y=t, with B(t)=c t²-t-q²=0.
- Nondiagonal: x≠y, with fixed sum s=x+y=-1/c and fixed product p=xy=1/c²-q²/c.

For the nondiagonal type, reduction modulo Phi_5(q)=1+q+q²+q³+q^4 gives

s=q³+q²,
p=1-q-2q²-2q³,
s²-4p=-3+4q+7q²+7q³.

These quantities are nonzero. There are only two diagonal candidates and two ordered nondiagonal candidates over an algebraic closure. The proof below excludes all cases algebraically; it does not search or approximate these roots.

## 3. The missing axis coefficients couple the two row pairs

At b=2, the outer coefficients a=1 and a=4 each receive one h_2 and one h_3 contribution. They force

h_(+,-,3)=-(1+d/x)/v,
h_(-,-,3)=-(1+d/y)/u.

Reflection gives the other two h_3 values. Now the actual coefficients at (0,2) and (0,3) require

q²(x^(-2)+y^(-2))-u^(-1)-v^(-1)
  -d[(xv)^(-1)+(yu)^(-1)] = q,                        (3)

q²(u^(-2)+v^(-2))-x^(-1)-y^(-1)
  -d[(xv)^(-1)+(yu)^(-1)] = q.                        (4)

There is no remaining amplitude that can change these two coefficients without disturbing already forced coefficients. Sectors ell=4 affect b=±1, not these rows; sectors ell=0 affect b=0.

For a row-compatible pair define

A(x,y)=q²(x^(-2)+y^(-2))+x^(-1)+y^(-1).

Equations (1) imply the exact identity

A(x,y)=2c-(x+y)(x-y)²/(x²y²).                          (5)

Subtracting (4) from (3) requires A(x,y)=A(u,v). A diagonal pair has A=2c. A nondiagonal pair has x+y=-1/c≠0 and x-y≠0, hence A≠2c. Therefore **mixed diagonal/nondiagonal types are impossible**.

It remains to exclude two diagonal pairs and two nondiagonal pairs.

## 4. Two diagonal pairs are impossible

Write x=y=t and u=v=w. Both B(t)=B(w)=0. After using B(t)=0, equation (3) is equivalent to

D(t,w)=(2c-q)tw-2(t+w)-2d=0.                          (6)

All denominators are nonzero. The certificate also verifies the unreduced identity

(axis residual in (3)) tw = D(t,w)-2(w/t)B(t).

### Distinct diagonal roots

If t≠w, the quadratic B implies t+w=1/c and tw=-q²/c. Consequently (6) forces

c D(t,w)=-(2c-q)q²-2-2cd
        =-2-2q+2q²-q³=0.                            (7)

The displayed polynomial is nonzero and has degree less than 4, so cannot vanish at a primitive fifth root in characteristic zero.

### The same diagonal root

If t=w, set a=2c-q and

l_1=2q³+2q²-q+2,
l_0=q³+2q²+2q.

Direct expansion gives

L(t)=c D(t,t)-a B(t)=l_1 t+l_0.

There is an explicit polynomial Bezout certificate:

l_1² B(t) - (c l_1 t-c l_0-l_1)L(t)
 = c l_0²+l_0 l_1-q² l_1²
 = 1+4q-11q²+6q³.                                   (8)

If B(t)=D(t,t)=0, the left side is zero. The right side is a nonzero polynomial of degree less than 4, again impossible. This argument does not divide by l_1 and does not omit a possible degenerate elimination case.

## 5. Two nondiagonal pairs are impossible

Both pairs now have the same sum s and product p from section 2. Therefore their unordered entries agree. There are only two possibilities:

- (u,v)=(x,y), giving (xv)^(-1)+(yu)^(-1)=2/p.
- (u,v)=(y,x), giving (xv)^(-1)+(yu)^(-1)=(s²-2p)/p².

Multiply the residual in (3) by p². In the first case it is

q²(s²-2p)-sp-2dp-qp² = -5-5q+5q³.                    (9)

In the second case it is

q²(s²-2p)-sp-d(s²-2p)-qp²
 = -9-19q-17q²-5q³.                                  (10)

Both are nonzero polynomials of degree less than 4. These are contradictions in characteristic zero. Equations (7)-(10), together with the mixed-type separation (5), exhaust all cases.

## 6. Why the nonzero residues are exact contradictions

Phi_5 is irreducible over Q: Phi_5(z+1)=z^4+5z³+10z²+10z+5 is Eisenstein at 5. Hence every primitive fifth root has degree 4 over Q. No nonzero rational polynomial of degree at most 3 can vanish at such a root.

This applies to every primitive fifth root and every characteristic-zero extension field. In particular the four alphas are not restricted to the cyclotomic field; they may be arbitrary nonzero complex numbers. Only the displayed coefficient certificates lie in Q(q).

No conclusion is taken from the earlier F_11 failure, and no finite-field-to-complex lifting step appears in the proof.


## Certificate and scope

The original standard-library checker verifies 95 exact identities. Its full source and mathematical output are included. The original independent literal-matrix and elimination review accepted this proof and all four exhaustive cases; its source hash is recorded in PROOF_STATUS.json. Neither finite-field failure nor approximate parameter search is used to infer the characteristic-zero result.

This exclusion supplies the lower bound of at least five banks. The independently accepted [five-bank construction](05_n5_five_bank_construction.md) attains it. Together with the prior N=3 construction, accepted N=7 characteristic-zero computational exclusion, and odd N>=9 exclusions, this closes the four-bank characteristic-zero question for odd N>=3 in this exact signed grammar: N=3 is feasible and odd N>=5 is not. The N=7 conclusion retains its exact computer-algebra certificate qualification. No all-positive-characteristic extension, enlarged endpoint/product grammar, new FFT algorithm or historical-priority claim follows.

## Support gate and the exact minimum at N equals 5

For orientation (ε,δ), a bank has Weyl support only where [εa]_5+[δb]_5≤4. For each t=1,2, the point (a,b)=(εt,δt) belongs to that orientation alone: flipping one sign changes the sum to 5 and flipping both gives 10−2t>4. The negative Fourier matrix has coefficients C q^(4(a+b)^2), with C≠0. Therefore every orientation is necessary. A sum of at most four banks must have exactly one of each orientation; the accepted four-bank exclusion rules it out. Together with the explicit five-bank witness, the minimum is five.

The bracket [r]_5 denotes the residue in {0,1,2,3,4}. This support follows from the root-of-unity binomial expansion of the legal inverse, as in the signed-bank comparison. The displayed coefficient normalization is the same as in the five-bank construction.
