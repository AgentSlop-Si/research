# Executed constant-centered-original composition

18 October 2026 UTC. New integration result; independent review pending.

## Result

The accepted restricted centered-source provider has now actually executed through the accepted complete outer transfer. The fresh run starts with a supplied 512-entry dense original, recognizes every entry, creates its normalized centered-spectrum approximation, freshly replays that source computation, produces and replays its actual one-row Cartesian median, evaluates all 5,733 retained coefficients, and writes all 512 rounded, exactly scaled final outputs.

Every final output was checked twice by exact arithmetic: against an independent interval evaluation of the retained operator, and against the actual original vector's negative unitary N-point DFT. No original/source/target switch occurs. The run's error satisfies

    ||Y - U_N u0||_infinity / ||u0||_2 <= 0.02213.

This decimal upper bound is certified by an exact rational inequality, rather than a floating tolerance. It is a finite observation for this fixture; it does not strengthen the accepted general theorem.

This completes the previously absent **executed integration gate for the restricted constant-original family**. It does not close ALG-034, supply a general sparse-recovery algorithm, establish an all-length executable, or demonstrate a useful speedup. The old singleton/recovery bridge and impossible sixteen-support exact centered interface were not used.

## Frozen dependencies and source association

The `runtime/` directory contains byte-identical accepted sources:

- centered_source.py: `4aa9992ee0f9d588d88152e0b97bb2ea2973d979865491e99dabf9b36a7fae43`
- sparse_output.py: `92577edf07395237940aad94326a8d1e5c4a18b194a9162af84ada2d826edafa`
- outer_wrapper.py: `d26c4cfe6d6c1430ce59b682f24bf69e2560fae81e8de60c63fc435b69b0637e`
- production_scalar.py: `73b3bb0bebf41f7a810bf2470e9ae520bdc3e7593516850d8933dd307500091e`
- full_transfer.py: `40d90da471b62fc9ac268b78cbe9f080b149be3789253bb1dbbe43837d5c534a`

The accepted provider proof/review, outer theorem/review, and mandatory dependency cost erratum are retained under `sources/`; SOURCE_BINDINGS.json identifies their original local paths and exact hashes. The scalar was absent from the supplied interface packet and was retrieved read-only from the immutable public preservation commit `d1c6910aa9fc4ef861981358e8bf3e0c71585689`, at `math/finalized/2026-10-18-cycle-completions/outer_stream/candidate/production_scalar.py`. Its exact SHA-256 matches the accepted outer theorem pin. The separate preserved Horner oracle was retrieved from that same directory and also matches its recorded source hash. All five numerical runtime hashes were checked before and after the complete execution.

The new integrated_centered.py adapter accepts only an actual original in the provider grammar. It does not accept caller-supplied estimates, output rows, coefficient records, or a numerical callback. It obtains the immutable accepted Source and Estimates by calling the provider itself. The Source retains m,N,F,c,h,scale and the original representation consumed. For the admitted constant family, those fields fully specify the mathematical original even when the caller's original representation was dense.

The adapter creates the candidate tuple and single immutable median row from the actual Estimates, paying all their copies on the same cumulative outer ledger. It calls produce_medians, constructs Outer (which pays its mandatory median replay), checks exact equality to the provider's pairs, and creates FullTransfer with TransferConfig(1,4,source.scale,4). Its run method actually calls FullTransfer.run. The returned immutable SourceBoundOutput retains the same Source, Estimates and exact transfer output; the latter retains the identical Outer binding and median origin. In-process owner/identity validation rejects substituted output objects.

These are trusted-program source associations, not hostile-runtime security or external historical attestation. A post-run mutation of the caller's original list cannot change the retained mathematical source. Semantic source replay is distinct from median replay: the former was explicitly requested and freshly performed in this run.

## Mathematical composition and scope

The accepted family is a nonzero canonical Gaussian-dyadic constant original u0_j=c 2^-F, N=M/4, M=2^m, within the provider's documented finite reference ceilings. Let

    E=N|c|^2, h=ceil(log2 sqrt(E)), u_j=c 2^-h,
    sigma=h-F, R=||u||_2, lambda=2^sigma.

Then 1/2<R<=1 and u0=lambda u. The actual centered source is J_N u with center floor((N-1)/2), and the exact spectral target is z=U_M J_N u. Its nonzero spectrum has exactly 3N+1 coordinates, whereas the provider returns a certified approximant on S=1+3*2^ceil(m/4)/2 coordinates. The retained half-sample phase remains exp(-pi i k/M). Three nonzero residue fibers are not three coordinates.

The byte-identical provider proves

    ||Z-z||_infinity <= M^-1/4 R.

Its grid is P=16m+16, its every-tape Cartesian cap is strict, and it checks |sigma|<=4m. The one-row median is exactly Z. With D=5, t=160m+4<M for every admitted m>=11, the accepted FullTransfer theorem therefore applies to this same original with beta=1/4 and d=4. Its accepted inherited bound is

    ||Y-U_N u0||_infinity <=
      [3t E_M + t eta(1+E_M) + 12*4^(-5m) + 2^(1-b)] ||u0||_2,
    E_M=4M^-1/4, eta=2^-8m, b=ceil(9m/4).

The original-target premise is supplied by the actual new provider execution and its accepted theorem. It is not inferred from median replay alone. The new adapter adds no approximation. FullTransfer performs the complete exact integer scatter, one final normalized rounding, and exact scale-back, including any required physical numerator shift.

The theorem remains restricted to the explicitly recognized constant original. It neither asserts exact sparse centered Fourier support nor supplies recovery from unknown measurements. Its proof carries all the provider's precision, original-width and finite-engineering limits. At the executed m value the inherited general bound is very loose; the sharper numerical error below is only a fresh finite certificate.

## Actual fresh execution

ORIGINAL.json retains every supplied input coordinate. The run uses

    m=11, M=2048, N=512, c=-3+5i, F=-36,
    E=17408, h=8, sigma=44,
    u0_j=(-3+5i)*2^36, u_j=(-3+5i)/256.

Thus the source's exact centered spectrum has 1,537 nonzero coordinates; only its approximation has 13. There are two fresh complete provider computations: production and full semantic replay, with 512 dense-coordinate visits each, 26 provider coefficient records in total, and a separately charged strict comparison.

The actual median row has 13 entries on grid P=192. The downstream header has D=5, t=1764, p=91. All 5,733 incidences are consumed in order; the scalar ledger records exactly 5,733 coefficient calls and 5,733 passing complex-radius certificates. Pi/root setup occurs once. The maximum actual row contains 13 terms. Every one of the 512 rows is written.

The normalized output grid is b=25. Since sigma=44, the final denominator exponent is zero and each rounded numerator is physically shifted by 19 bits. OUTPUT.json retains all 512 exact integer pairs, the original/source/estimate fields, and output metadata. RESULTS.json retains all disjoint numerical receipts and pre/post runtime hashes.

The complete source-bound driver exited zero with empty stderr, taking approximately 102.15 seconds and reporting a maximum RSS of 14,720 KiB on this host. These are process observations, not complexity claims. An earlier launcher attempt found `/usr/bin/time` unavailable and executed no Python; its stderr is retained separately. The successful driver uses Python's own monotonic/resource observations.

## Two exact all-output checks

### Actual original's transform

For any constant original, the geometric-series identity gives U_N u0 equal to sqrt(N)c2^-F at zero and exactly zero at every other coordinate. target_checks starts from that identity and the actual Source, obtains an independent 256-bit rational sqrt(N) enclosure by integer bisection, and checks every output after exact division by 2^sigma. No production trigonometric routine or Dirichlet ratio supplies its target.

All 512 exact rational squared-error checks satisfy a rational upper envelope for the accepted relative theorem. The maximum squared relative error is bounded by

    18295620993 / 37383395344384,

and occurs at row 510, where the exact target is zero. This is at most (2213/100000)^2, proving the reported relative error <=0.02213 (2.213%). The integer comparison is retained in VERIFICATION.json. TARGET_CHECKS.json retains the entire per-row error list, normalization, target intervals and theorem envelope. A simpler <=1/4 check is also directly asserted in the execution driver.

### Retained interpolation operator

check_retained_outputs.py independently traverses rows first and then the 13 input locations. It does not call the production iterator, endpoint table or coefficient kernel. For this N=M/4 fixture it selects the retained pairs by the equivalent unique circular difference -h-1<=4ell-k<h+1.

It evaluates every one of the same 5,733 retained coefficients using the preserved exact interval oracle: a different pi identity, interval Horner sine, exact integer square root, and separate row-first traversal. Every row's C Z interval is accumulated exactly on grid 2^-448, and its final output is checked by the accepted bound

    |2^-sigma Y_ell-(C Z)_ell| <=
       eta sum_(retained k)(|Re Z_k|+|Im Z_k|) + 2^-b.

The comparison is an exact squared complex-endpoint inequality, not separate Cartesian tolerances. All 512 rows pass; the independent coefficient count agrees exactly with production. RETAINED_TARGET_CHECKS.json retains every row interval, exact squared error and allowed bound. This oracle is a separately executed checking program; its work/storage is not hidden in production receipts.

## Boundary controls

Four actual post-run controls reject a second integrated run, a copied integrated output, a copied output with a changed original-source field, and a copied FullTransfer output. Their paid ledger prefixes remain in RESULTS.json. The original caller array was altered after execution and cannot change the immutable associated original.

Five additional calls through the integrated entry reject zero, an out-of-contract scale, too-small m, a Boolean component, and a changed last dense coordinate. The final case pays all 512 visits before rejecting. Their separate fresh prefix receipts are retained in BOUNDARY_CONTROLS.json; no downstream numerical preparation is reached. The adapter's fixed initial type/control check costs an additional O(1), rather than being claimed as a separately measured front receipt.

## Honest complete costs and storage

Keep the accepted frontend definition L=2+m+W+f, including raw original component width W and exponent encoding width f. One frontend costs O(N L^6+S L^7) for supplied dense originals, or O(L^3+S L^7) for a supplied constant descriptor. These intentionally conservative bounds include its exact rational intermediate widths and global control envelope. The actual source replay adds another full such cost and its separately paid strict comparison.

The adapter adds O((S+1)H^2) copying/association work and O((S+1)H) records. The one-row median production and mandatory replay have that same order, separately charged, where H contains actual data/header/address widths and cumulative counter widths. The same outer ledger continues through all these steps, FullTransfer initialization, all validation, exact products/scatter, all N output writes, scale-back, and the listed output-substitution controls. No old receipt is reset or omitted.

The accepted numerical outer stage contributes

    O(N m^2 + S m^6)

for fixed D=5, beta=1/4, d=4 and O(m)-bounded original/history widths, since it evaluates E_outer<=S t coefficients and each accepted scalar coefficient costs O(m^5). For arbitrary histories use the actual H-dependent control bound and prior receipts. The scalar numerical ledger remains separately cumulative; its one setup and every coefficient are included.

With W,f=O(m), including the optional full source replay changes constants only. The complete restricted dense-original integration is conservatively

    O(N m^6 + M^1/4 m^7) binary work.

A compressed original replaces the dense recognition term by its actual compressed-input bound. No linear-bit or practical-fast-transform claim follows. Constant originals already have a closed-form DFT, so this is an interface/execution witness rather than a competitive algorithm.

COST_TOTALS.json sums only disjoint source-level receipts: frontend production, frontend replay, replay comparison, the single cumulative adapter/median/outer ledger, and the scalar ledger. Its conservative work sum is 86007892714819542569341088; cumulative produced/control-bit sum is 1509313675658178. These huge upper envelopes are not actual instruction counts, bytes resident, or time estimates. The separately run five front rejection prefixes, input fixture construction, imports/process startup, both oracles, exports, hashes and packaging remain additional finite harness work with separate files/process observations.

Peak production data obey the accepted O(Nm+Sm+L^2) new-stage bound under the same bounded metadata conventions, plus any caller-retained dense original's actual O(N(W+m)) bits. All median rows and origins, endpoint records, N accumulators/counts, N output records, source/estimate associations and scalar temporaries are included. The production stores no E_outer-sized coefficient table. This packet deliberately retains N-row outputs and two N-row audit tables, and the independent oracle performs its own work: their serialization and disk/storage costs are additional. Cumulative ledger bits must not be confused with peak storage.

## Reproduction and stopping boundary

From this directory, with Python 3.10 or newer and only the standard library:

    python run_integration.py
    python check_retained_outputs.py
    python check_boundary_controls.py
    python verify_packet.py --fresh

The first command performs the real complete numerical integration, not merely a constructor or an allocation-free parameter plan. Re-running writes fresh results/process observations and can change recorded times; keep the sealed packet intact and run in a copied directory if preserving these exact bytes. The --fresh flag validates regenerated results without requiring their new process timings to match the original manifest. Verification without rerunning production is available with `python verify_packet.py` against the retained manifest.

No GitHub, Sheet or other external write occurred. The executed new integration is ready for independent review. The general source-dependent supplier, arbitrary nonconstant originals, unknown-support recovery, independent-randomness/amplification obligations, general sparse/dense all-length dispatcher, and ALG-034 remain open. The exact centered support barrier remains unchanged.
