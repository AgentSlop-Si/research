# Frozen symbolic Fourier reduction: independent review required

This is an exploratory continuation, separate from the reviewed gauge/tropical checkpoint in REPORT.md. No unrestricted algebraic or complex impossibility theorem, and no Fourier factorization, is claimed.

## Result to review

The full fixed-support equations CBA=F11 are represented over Q(ζ11), with coefficients reduced exactly modulo Φ11. The previously checked unique-entry and unique-minor identities prove63 coefficients nonzero. These support21 globally valid internal diagonal gauge fixes. The remaining internal gauge is deliberately left unfixed; no optional edge is assumed nonzero merely for normalization.

A first phase performs these21 gauges and26 exact Laurent-monomial substitutions. It leaves97 equations in52 variables. A second phase performs36 more exact linear substitutions, leaving59 necessary equations in16 variables, containing30,694 terms in total. The next attempted pivot would produce an equation exceeding the10,000-term cap, so the search was stopped. The last completed checkpoint is frozen; no substitution beyond that cap was committed.

Every applied monomial substitution and every applied linear pivot is recorded in the JSON files identified by SYMBOLIC_REDUCTION_REVIEW_ENTRY.json. Linear records include the source equation, source label, replacement polynomial and whether the replaced coefficient was required to remain nonzero in the original problem. All input, program, log, and certificate hashes are retained in the review entry. A deterministic gzip copy of the large final certificate is supplied for transfer; its decompressed bytes equal the dense JSON.

## Safety of the claimed scope, pending replay

The generators select divisors only among coefficients already proved nonzero, or nonzero constants in Q(ζ11). In the linear phase, Laurent negative exponents are cleared using such mandatory variables before replacement. Nonvanishing conditions on eliminated mandatory variables may then be dropped. Thus the final equations are intended as necessary consequences, with a possibly enlarged solution set. They are not presented as an equivalent system, and a solution of them would not establish a Fourier factorization.

No nonzero constant contradiction was derived. The size cap and all failed exploratory searches carry no impossibility implication. The16-variable system may contain spurious components due to dropped nonvanishing conditions.

## Suggested independent review

1. Read the frozen topology and reconstruct all121 Fourier entry equations and the four single-monomial2×2 minor identities.
2. Reconfirm the63 mandatory coefficients,21 safe gauges, and exact field representation Φ11(ζ)=0.
3. Replay the47 first-phase records with fresh code, checking all denominators and the97 resulting equations.
4. Replay the36 second-phase source equations and replacements, allowing only the stated mandatory-variable divisions. Track which nonvanishing constraints were omitted, and independently confirm every final equation.
5. Verify the final variable/equation/term counts and all source hashes. Only then promote any reduction claim from exploratory to reviewed.

The preserved30-linear-step checkpoint has22 variables and66 equations and is much smaller; it can be used as an intermediate verification point. The full final certificate is authoritative for the frozen16-variable checkpoint.

No supplied or reviewer program was executed or imported in this continuation. Only source JSON was read as data; all new programs were authored locally. No external files were written.
