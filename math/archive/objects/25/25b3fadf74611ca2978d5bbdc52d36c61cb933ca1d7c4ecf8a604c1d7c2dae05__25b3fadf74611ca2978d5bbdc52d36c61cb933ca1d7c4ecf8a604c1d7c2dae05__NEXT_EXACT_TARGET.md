# Next exact challenge — after testing compact operator compression

The exact FFT matrix is already representable with displacement rank one and O(N) symbolic state. The failed step is **materializing all N answers in fewer than N log N properly charged operations**. A new smaller representation, by itself, is insufficient.

## Disqualifiers (now explicitly certified)

1. A two-register unitary stage compiler cannot give O(N) arithmetic for arbitrary normalized DFT: total Shannon entropy must grow from 0 to N log2 N, by at most two bits per gate. This is the known Ailon-model obstruction, and is tight for radix-2.
2. A det<=2 two-register nonunitary compiler cannot give O(N) arithmetic for the unnormalized DFT: volume growth needs N log2 N/2 gates. This is a narrow easy determinant bound, related to Morgenstern's stronger old result.
3. Standard exact low-rank compression of contiguous large Fourier blocks is impossible: those blocks have maximal rank. This does not rule out displacement, permutations or nontraditional factorings.
4. A growing sub-FFT advertised as one O(1) macro is unacceptable unless it truly has an independently justified O(1) primitive cost in the selected model.

## One falsifiable candidate for future work

**Nonunitary, global multi-output representation with charged exact recovery.** Specify a constant-size dataflow primitive that maps an N-dimensional state through a **nonunitary** stage, and prove that the resulting intermediate representation has some exploitable composition law which can be evaluated with o(N log N) total ring/arithmetic operations. It must not simply be a DFT macro under another name or a table of all input possibilities. The coefficient size, inverse conditioning, data movement, and construction costs must be explicit. If its intermediate maps are uniformly well conditioned, check Ailon's conditioned-model restrictions first.

Concrete pre-code falsification checks:

- Does the purported primitive hide a large-determinant or high-entropy block operation? If yes, explain why its hardware/model cost is constant instead of pretending it is.
- Is there an O(N)-size exact symbolic expression but no O(N) materialization? If yes, this is the same displacement/pole-representation issue.
- Are input-dependent collisions required? If yes, random full-entropy controls from the checkpoint apply.
- Does the proof rely on finite precision, single-bin outputs, structured data, or amortized updates? Then it targets a different problem.
- Is the new construction merely an unrestricted-coefficient shared linear circuit? This is already the core direction of OpenAI #130; compare the **entire circuit and its costs** rather than presenting an isolated gate-count change as unrelated novelty.

Only build a new implementation after a mathematical candidate survives those tests. The current experiment therefore ends with a clear negative result under two natural exact-operation models, not another optimistic benchmark.
