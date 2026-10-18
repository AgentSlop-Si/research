# Mandatory cost clarification for the frozen outer-wrapper candidate

Date: 17 October 2026. This independent clarification is part of the acceptance condition and must accompany publication of the candidate.

## Exact scope and hash binding

This erratum applies to the candidate manifest SHA-256:

`f14e4bbd92c98063902e262ce699bfa58c6ba4333562bbbe683deb97714dff8f`

and specifically to:

- PROOF.md: `651d2c5f443a8aede073ef2ef3a536331728352ddc65fc4ec199524db4444b08`
- outer_wrapper.py: `d26c4cfe6d6c1430ce59b682f24bf69e2560fae81e8de60c63fc435b69b0637e`
- sparse_output.py: `92577edf07395237940aad94326a8d1e5c4a18b194a9162af84ada2d826edafa`

No runtime-source change is needed for this clarification. The bounded fixture and its receipts remain valid. The unrestricted producer asymptotic statement in PROOF.md section 5 is **not accepted as printed**.

## Address and cumulative-counter widths cannot be omitted

ReceiptLedger.charge, outer_wrapper.py lines 23–27, uses the larger of the reached integer widths and the bit length of the cumulative event counter. The merge sort also passes row counts, loop positions and merge widths to that ledger, sparse_output.py lines 64 and 76–78. Thus the numerical amplitude width alone does not control the charges for arbitrarily many rows or an arbitrarily large previously accumulated ledger.

For example, fix M=4, P=8, one candidate and all-zero amplitudes, and increase the odd row count R. All supplied integer values then have constant width, but the sorter has Theta(R log(R+1)) visited positions with Theta(log(R+1))-bit addresses/counters. Its conservative ledger therefore can grow as Theta(R log(R+1)^3), not O(R log(R+1)) with a constant numerical H_e. The experimental process caps do not prove an unrestricted asymptotic statement; they bound only this finite run.

A safe general statement is the following. Let:

- S be the number of candidates and R the positive odd number of rows;
- H_e bound the signed widths of all reached integer data/header fields, including M, P, indices and estimate components;
- E_0 be the event count already present on entry;
- H_0 bound the encoding widths of the ledger's existing counters if an incremental bound including their bookkeeping is wanted;
- T = O(1 + S + R + S R log(R+1)) be the total number of new charged events, with its constant chosen to dominate all parsing, sorting, output construction and replay-comparison events;
- H = max(1, H_e, H_0, ceil(log2(S+R+2)), ceil(log2(E_0+T+2))).

Then a producer call, and separately its paid replay plus comparison, have the safe conservative upper bounds O(T H^2) for bit work and O(T H) for cumulative produced/control bits. For a newly initialized ledger, H_0 is constant and E_0=0. For continuation on an existing ledger, its previous receipt is retained and added; it must not silently be reset or dropped. Counter accumulation is cumulative accounting, not an assertion that every later tiny operation on an arbitrarily old ledger has a cost depending only on its new numerical operands.

When R is fixed, all relevant data/address/counter widths are O(m), and the prior ledger prefix has O(m)-bit counters, this reduces to the stated bounded-input preparation cost. These conditions hold for the reviewed R=3, S=4, m=57 fixture. In a general caller-supplied-R interface they must be established, rather than inferred from fixed D.

Similarly, the outer-stage O((S+E+1)m^2) control bound assumes O(m)-bit reached metadata and cumulative counters, and the bounded number of validations in that stage. If a caller makes V additional validation calls, those calls are extra paid work. An unbounded previous event count or unbounded repeated API usage is not covered by the fixture's m-only shorthand.

## Stored context, outputs and observation boundary

The O(Sm) endpoint/prefix table is additional wrapper state. The ProducedMedians origin intentionally retains all original immutable input rows for semantic replay. Their storage, candidate/output records, and bounded merge-sort workspace must also be counted; a safe coarse data/address bound is O((SR+S+R+1)H), in addition to the scalar state. It is incorrect to quote O(Sm) as the complete retained producer-plus-wrapper memory bound for arbitrary R.

Every emitted incidence and coefficient is charged by the production stages. A caller that retains a full E-record list, serializes receipts or repeatedly snapshots the ledger adds caller-side work/storage. ReceiptLedger.report is an observational snapshot and does not itself increment the outer ledger. The independent driver and candidate launcher receipts/caps cover the finite test harness separately; unlimited reporting or JSON serialization is not a free operation included in the producer theorem.

## Acceptance consequence

Accept the local computed-median binding and bounded iterator/control subgate only together with this clarification. Do not accept or republish the unqualified H_e-only general producer bound. No claim of full sparse-pipeline provenance, full outer transform, Q16/STR-Q1 reopening, or completion of ALG-034/ALG-038 follows.
