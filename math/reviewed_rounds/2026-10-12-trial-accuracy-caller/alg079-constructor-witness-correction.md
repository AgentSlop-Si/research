Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; scientific claims, exact source/cost boundaries and limitations are retained. Original source-report SHA-256: 2de12be58e164385e793ee409db7e387b9e199c9becacfc06d490682ee352543.

Review date: 12 October 2026 UTC.

Read with the [independent caller-migration review](alg079-historical-caller.md).

# Required constructor-witness correction

The original candidate REPORT.md is preserved byte-for-byte. Its sentence naming (N,p,omega)=(64,193,125) as a zero-diagonal refusal is incorrect.

Use this corrected replacement sentence in a reviewed derivative:

“The original RecurrenceGreen constructor raises ValueError('zero diagonal entry') at (N,p,omega)=(16,1201,473) and (32,353,294), using default green=(7,2,1) and generator arguments 11 and 3, respectively. At (64,193,125), generator argument 5, the original constructor succeeds and two unchanged-original-caller direct-DFT baselines pass. The new cold migration returns exact outputs on all three parameterized domains.”

The zero entries occur at L diagonal indices 14 and 25 in the two refusal cases. These are distinct parameterized witnesses; do not turn this correction into a general statement about every length-32 or length-64 constructor. The source-pinned migration acceptance is unchanged. See output/CORRECTED_WITNESSES.json for fresh observations and REPORT.md for the independently accepted scope.
