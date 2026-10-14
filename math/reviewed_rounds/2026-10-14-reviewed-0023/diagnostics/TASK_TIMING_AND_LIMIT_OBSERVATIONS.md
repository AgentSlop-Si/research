# Research task timing and limit observations

All times are UTC. These are observed wall-clock intervals, not active compute time or billing telemetry. Actual model input, output and total token counters were unavailable and remain **unknown**. No token amount is inferred from duration, text size or tool-output estimates.

## Completed work

- Earlier GitHub research publication: 13 October 23:26:50 to 14 October 00:19:21, **52 minutes 31 seconds**, including substantial approval waits. The verified result is commit 48b7d68885705e79a0920a1b23edaf55d159fa30.
- Independent H16 bounded-exclusion review: 14 October 00:17:42 to 00:19:33, **1 minute 51 seconds** for the substantive audit. Packaging finished at 00:20:28. The bounded-family verdict is ACCEPT.
- Independent Q16 static contract review: 14 October 00:17:50 to 00:22:30, **4 minutes 40 seconds**. The verdict is ACCEPT_STATIC_CONTRACT_ONLY; production execution remains separate.
- Research-file inventory: 14 October 00:17:57 to 00:20:35, **2 minutes 38 seconds**.
- Usage-observability report: first measured time 14 October 00:17:34; report finalized at 00:19:06.541. This is a **1 minute 32.541 second measured interval**, not an exact whole-task lifetime.
- Conditional H16 admission/lift audit: completion was observed at 14 October 00:18:28. Its precise start and complete elapsed duration were not available in this observation set. It supplied no 31-call word.

All six tasks observed in progress at 00:17:57 had completion reports by 00:22:53. They did not necessarily start together. No preview-limit error was observed in that group. This does not establish a quota reset, bug, missing limit or runtime threshold.

## Errors and limits

An earlier task had the exact preview-limit message:

“You’ve hit the preview limit. Try again at Nov 12th, 2026 11:33 PM.”

Its actual failure time, prior elapsed runtime and token use were unavailable. The reset text did not supply a timezone or identify the exhausted allowance.

At 00:18:38, a separate attempt to create another task failed. The exact error excerpt was “agent thread limit reached”. No new task was created. This is a capacity observation, not evidence of token exhaustion.

The H16 independent review reported one truncated directory-listing output; subsequent bounded reads and all verification computations succeeded. No compiler, assertion, integrity, authorization or preview-limit error occurred in that review. The truncation warning's token estimate measures returned output only and is not model usage.

## Package preparation

The additive package was first assembled from 00:23:37, with pre-seal checks completed at 00:26:07 and manifest finalization observed by 00:26:29. A final editorial pass began at 00:30:03 and reached final checks at 00:32:02 before upload. This revision preserves the original scientific archives byte-for-byte, excludes unfinished new Q16 regression work, and does not claim a later successful spreadsheet application without a verified receipt.

The available observations do not expose provider billing or quota accounting.
