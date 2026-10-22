# Version 2 empty input accounting correction

21 October 2026 UTC. The independent reviewer identified a genuine cost-ledger omission: with N=M=0, version 1's displayed leading terms vanished even though its text included fixed input setup, storage and a decision bit.

Version 1 is preserved byte-for-byte at the directory named in V1_REFERENCE.json. No authoritative predecessor source snapshot was changed. Version 2 is a separately pinned candidate, not an accepted result.

The corrected decision bound is

D = O((N+M+1)(b^2+ell) + M b^3 + M log2(M+1)(b+ell)).

The corrected storage bound is O((N+M+1)(b+ell)) bits, including the fixed field descriptor and working registers. The separately displayed extraction ledger is S_B^bit + O((N+1)ell+b+M E_B^bit+M b^2). Its fixed overhead is absorbed by the corrected D in the combined extraction-plus-decision formula.

The O(Nb) row-coordinate payload remains correct, but is now distinguished from the O((N+1)b) complete output including the field descriptor and decision bit. The field and input-domain freeze states explicitly that valid endpoint indices imply M=0 whenever N=0.

No mathematical theorem, domain algorithm, root routine, control code, recorded control result, source byte, or root-complexity claim changed. The +1 gives a conservative O(b^2+1) decision/setup upper bound for an empty selected system; it is not an optimal empty-input claim. V2_DIFF.patch records the exact report and candidate-metadata changes.

Acceptance remains pending until the independent reviewer checks the corrected bytes and their source and control bindings.
