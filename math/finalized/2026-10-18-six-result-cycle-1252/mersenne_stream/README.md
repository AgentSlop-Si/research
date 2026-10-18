# Mersenne Stream: accepted scope and retained evidence

Read candidate/REPORT.md and the final independent review in review/. Mandatory qualifications are in ../REQUIRED_CLARIFICATIONS.md; reproduction and byte-binding changes are in ../REPRODUCTION.md and ../PORTABILITY.md. Historical candidate “pending” statements are retained. Root RELEASE_STATUS.json and SEAL.json determine release finality.

The final review corrects two interface qualifications: ambient m does not force actual W≥t for low-valued inputs; use q≤1+W/t=O(m/t) under the ambient condition or retain the unsimplified/paid-padding ledger. Reading an arbitrarily long encoded grouping parameter d incurs its bitlength cost. The accepted conversion bound is not a full multiplication or prime-supply result.
