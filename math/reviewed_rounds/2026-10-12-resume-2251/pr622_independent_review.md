# Review of the PR622 profile-comparison supplement

12 October 2026 UTC. ACCEPT at the bounded profile-comparison scope; not a full algorithm or owner-map audit.

The comparison argument in pr622_comparison_audit.md is logically sufficient. For nonnegative profiles supported on 1<=r<73, the moment function is continuous and strictly increasing. The recorded rank mass gives Phi(0)=520704/523264<1, and the positive exponential terms imply a unique threshold. A negative moment sign for PR623 above the candidate's strict upper bracket proves the first ordering. A positive PR624 moment sign at the candidate's strict lower bracket proves the second. This correctly compares thresholds, not merely their feasible lower bounds.

The rational error formulas were checked algebraically: the positive log-atanh tail after 90 terms is bounded by 2*z^181/(181*(1-z^2)); after exponential degree 25 the positive tail is bounded by (t^26/26!)/(1-t/27) for the stated nonnegative t<1/100. Outward rounding preserves enclosures. The recorded profile difference 1-4*3+2*16-21=0 preserves rank mass. Exact pin/source matching and eight rational interval evaluations are recorded by the fresh checker; this independent review checks the mathematical comparison and bounds rather than claiming a second independent numerical reconstruction.

Accept only the pinned-source/profile ordering PR623 > candidate > PR624 in the specified native-complex moment model. Author source replay statements are not independent proof of owner-map legality or complete all-size transfer. Original input files remain unchanged; the author's correction withdrawing novelty/current-best implications remains controlling. No practical FFT or integer-multiplication breakthrough is established.
