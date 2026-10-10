# Exact F5 reconstruction and honest Green-work accounting

## Result and scope

The accepted B5 positive certificate has THREE allowed Hamiltonian Green summands. Its third weighted cycle has every edge zero, so its Green kernel is I and that summand is simply a diagonal correction. Evaluating B5 therefore uses TWO nontrivial cyclic Green solves plus ONE diagonal correction, with the endpoint diagonal work also charged.

The same B5 reconstructs the unnormalized Fourier matrix by the exact identity

    F5=(1+c)B+(1−2c)BAB+(1+c)BABAB,   c=5g,           (1)
    g=1+2(ζ²+ζ³), A=diag(ζ^(3j²)).

Three reused sequential B applications suffice. With the explicit three-term factorization, this means SIX nontrivial cyclic Green solves, THREE diagonal-correction applications, and TWO chirp-A applications, plus the endpoint diagonal multiplications and final linear combination.

This is an exact fixed-size positive control and an explicit connection to Fourier evaluation. It supplies no all-length family, speedup, asymptotic advantage, or free algebraic-root generation assumption. The minimum-three result concerns the permitted summand grammar; it is not a claim that three nontrivial Green solves are necessary or performed.

## 1. Orientation and scalar derivation

Keep the unnormalized positive Fourier convention F[i,j]=ζ^(ij). The source target is

    B=(F^(-1)+A)^(-1).

Define M=AF and K=AB. The established positive-chirp scalar-cubic identity for FA transfers to AF by conjugation with A; alternatively it follows directly by completion of the square. Thus

    M³=cI,   c=5g.

The factor order is explicit:

    F^(-1)+A=(I+AF)F^(-1),
    B=F(I+M)^(-1),
    K=M(I+M)^(-1),
    I−K=(I+M)^(-1),
    F=B(I−K)^(-1).                                  (2)

Here 1+c≠0 because g²=5, so (1+c)(1−c)=1−125≠0. No normalized Fourier substitution is made.

The inverse Möbius relation M=K(I−K)^(-1) gives

    μ(K)=0,
    μ(z)=z³−c(1−z)³
        =(1+c)z³−3cz²+3cz−c.

Let

    Q(z)=(1+c)z²+(1−2c)z+(1+c).

Direct scalar multiplication yields (1−z)Q(z)=1−μ(z). Hence Q(K) is the two-sided inverse of I−K. Substituting in (2), while retaining the order of factors, gives

    F=B Q(AB)
     =(1+c)B+(1−2c)BAB+(1+c)BABAB,

which proves (1). The two alternative conventions K=AB and K=BA give equivalent final words if applied on the correct side; this addendum uses AB throughout.

## 2. A reused sequential evaluation plan

For an input x, compute

    y0=B x,
    y1=B(A y0),
    y2=B(A y1),
    F x=(1+c)y0+(1−2c)y1+(1+c)y2.                    (3)

There are three B calls, not a separate re-evaluation of each expanded product. Each B call uses the accepted factors

    (1−t)Du (I−W_t)^(-1) Dv
      +(t−1)Dv (I−W_(1/t))^(-1) Du
      +Δ,

where the two nonzero weighted cycles have weights(1,1,1,1,t) and(1,1,1,1,t^(-1)); Δ is the stored diagonal correction. Their respective Green denominators 1−t and1−t^(-1) are nonzero. The third grammar summand is Δ(I−0)^(-1)I=Δ and needs no cyclic solve.

In addition to the six nontrivial Green solves, (3) includes the endpoint diagonal actions in each branch, three Δ multiplications, two A multiplications, and the final three scalar-vector products and two vector additions. Nonzero coefficients and inverse closure scalars may be prepared and reused, but preparing the exact field/root data and every stored endpoint is part of setup. Nothing here establishes an advantageous asymptotic setup or application cost.

For clarity, a cyclic solve can be carried out without a dense matrix. For row action y_i−w_i y_(i+1)=x_i on the natural cycle, first compute

    y0=[x0+w0*x1+w0*w1*x2+⋯+(w0⋯w3)*x4]
         /(1−w0*w1*w2*w3*w4).

Then recover y4,y3,y2,y1 backwards from y_i=x_i+w_i*y_(i+1), taking y5=y0. This is a cyclic scan, not a stored dense inverse. The checker evaluates the factors through this scan.

## 3. Exact verification

The new standalone standard-library checker reads the frozen factor JSON as inert data. Its exact field arithmetic was copied from our own new constructor helpers; it does not import or execute the constructor or uploaded programs. It independently obtains B by Gaussian inversion of F^(-1)+A in Q(ζ), and compares it to the saved target.

It then verifies every entry of:

- (AF)³=cI and μ(AB)=0;
- (I−AB)Q(AB)=Q(AB)(I−AB)=I;
- BQ(AB)=F and the expanded identity(1).

Finally, it applies the actual factored B scan plan in (3) to all five basis vectors and two additional exact vectors, checking35 output entries. The seven runs invoke21 B calls,42 nontrivial Green solves,21 diagonal corrections and14 A calls, exactly the stated per-transform counts. Every scan separately checks its five defining recurrence equations. The output lies in Q(ζ) even though the factor evaluation temporarily uses the quadratic extension from the three-Green certificate.

The deterministic results, source checksum, isolated replay and file seal are included. Independent acceptance is a separate review artifact. The original three-Green constructor and its independent review remain unchanged.
