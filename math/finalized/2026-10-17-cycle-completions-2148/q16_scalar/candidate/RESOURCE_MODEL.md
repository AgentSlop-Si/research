# Paid finite arithmetic and source bounds

This is a deliberately conservative schoolbook binary arithmetic model. It is not a measurement of Python object allocation, CPU instructions, JSON hashing/serialization or host RSS. Test-driver/report-file serialization is a finite external harness cost; it is not hidden inside the production coefficient complexity claim. Process caps separately bound the actual test.

## Primitive charges

Every addition, subtraction, negation, multiplication, floor/ceiling division, modulo reduction, bit-length query and binary shift passes through `Paid`. Exact built-in integer inputs are charged on read and copy. Square-and-multiply accounts for each multiplication, exponent update and parity reduction, retaining intermediate widths rather than counting a large power as a unit operation. Every shifted binary divisor is accounted for at its actual result width.

For one recorded primitive, let b be two plus the sum of signed operand/result bit lengths. The arithmetic work charge is `16*b*b`, and the produced-integer charge includes the signed result width. This overpays ordinary addition, comparison and bit-length operations and bounds schoolbook integer multiplication/division and the allocated result of a shift.

Each fixed-size validation, branch, loop iteration, analytic clipping, corner comparison, interval/record construction and copied output field also increments an explicit event count. The report adds a global control/copy/width envelope with `e=events+256`, `w=max_integer_bits+bit_length(e)+8`:

- control/copy/width work upper bound: `2048*e*w*w`
- cumulative control/copy/integer storage upper bound: `produced_integer_bits+2048*e*w`

Each production helper has a bounded number of untraced fixed-control actions per event; the only variable-sized helper loop is over recorded operands (at most three for current arithmetic calls). The envelope covers ledger counter arithmetic, bounded tuple construction, type guards, interval/record fields, loop controls, abs/min/max/comparisons and width-accounting operations themselves. The report is a charged event. The declared work/storage totals are conservative bounds in this model, not exact operation counts or peak-memory measurements.

The companion wrapper must account for its own header parsing, accepted sparse fields, support validation/canonicalization, incidence endpoints, stream records and association checks. No uncharged front-end sorting or support hash is claimed by the numerical kernel.

## Growth bound

For fixed D, `s=Dm`, and `K,n=O_D(m)`. Kernel argument numerators have O(m) bits. Maintained Machin powers have O(K) bits. The Taylor factorial has O(K log(K+2)) bits. Signed-power endpoints/divisor have O(sK) bits. A successful-domain integer-width envelope is therefore

`H=O(m+K log(K+2)+sK+log(s+1))=O_D(m^2)`.

A coefficient uses at most five sine calls, each O(K) primitive/control operations, plus O(log(s+1)) endpoint-power steps and constant many products/quotients/certificate operations. One-time pi and root setup also use O(K) operations. Thus per-coefficient and one-time setup work is O_D(m^5), with O_D(m^3) cumulative produced integer bits. The control envelope retains these bounds because its event and width growth have the same orders. D-uniform m^5 is not claimed.

Header validation plus companion support/enumeration work has O(S+E+1) O_D(m)-bit operations. For a valid support S<=M and E<=St, counter widths remain O_D(m). With lazy setup this yields

`O_D((S+1)m^2 + 1_{E>0}m^5 + E*m^5)`.

An empty engine pays header work but does not construct U=2^K, pi, root or Taylor terms. Nonempty repeated preparation never resets the ledger and never adds a new pi/root setup. The kernel stores no N/M-sized objects or phase table. Any downstream retained E-record storage and N accumulator/output work must be paid by their own stage.

## Concrete receipt

For the three selected numerical evaluations plus the actual signed-power sentinel and a repeated preparation check, the author run reports 12 sine calls, 1,262 atan terms, 625 root bisections, 5,040 Taylor recurrence iterations, and 10,096 factorial multiplications. `max_integer_bits=177557` includes a sign bit; the corresponding unsigned-width convention would report 177556. Ledger totals and their recomputation formula are in `RESULTS.json`; they do not imply a measured speedup.
