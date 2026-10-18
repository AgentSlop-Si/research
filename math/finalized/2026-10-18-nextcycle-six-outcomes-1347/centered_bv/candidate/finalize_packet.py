"""Summarize disjoint receipts and seal a completed local packet."""
from pathlib import Path
import json,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent

def load(n):return json.loads((HERE/n).read_text())
def dump(n,x):(HERE/n).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    r=load('RESULTS.json');rec=r['receipts'];s=rec['outer_transfer']
    fronts=[rec['front_production'],rec['source_replay']['replay_production'],rec['source_replay']['comparison']]
    work=sum(x['arithmetic_bit_work_upper']+x['control_bit_work_upper'] for x in fronts)+s['outer_and_scatter']['bit_work']+s['scalar']['total_bit_work_upper']
    bits=sum(x['cumulative_bits_upper'] for x in fronts)+s['outer_and_scatter']['produced_bits']+s['scalar']['cumulative_integer_and_control_storage_bits_upper']
    totals={'disjoint_production_work_upper_sum':work,
        'disjoint_cumulative_produced_control_bits_upper_sum':bits,
        'includes':'front production; full source replay; strict replay comparison; cumulative adapter/median/outer/scatter ledger; cumulative scalar setup and coefficient ledger; output validation and four post-output controls',
        'excludes':'input fixture allocation, separate preliminary source recognition, imports/startup, independent direct-sum oracles, extra controls and complex examples, allocation-free plans, exports, hashes and packaging',
        'units':'conservative source-level bit-work/control and cumulative produced-bit envelopes, not runtime, actual instruction count, physical bytes, or peak resident storage',
        'history':'All numerical ledgers begin fresh here and remain cumulative. General prior-history H requirements remain mandatory.'}
    dump('COST_TOTALS.json',totals)
    a,b=r['relative_error_upper_rational'];pct=f'{100*a/b:.2f}'
    report=f'''# Executed nonconstant centered bounded-variation source

18 October 2026 UTC. New broader structured-family result, pending independent review.

## Result

The actual 512-entry three-block original was recognized, normalized, approximated, fully replayed, passed through the accepted one-row median and complete outer stream, and checked against its own unitary DFT. Every output's complex error is certified at most {a}/{b} = {pct}% of the actual original Euclidean norm. This is a finite fixture certificate, not an improvement to the universal outer theorem.

The original is 2^38 times 1 on [0,173), 2 on [173,384), and -1 on [384,512). Its exact raw energy is E=1145, zero-extended Cartesian jump variation is B=6, and checked variation factor is C=3. Normalization has h=6, ||u||_2^2=1145/4096 and scale sigma=44. It is genuinely nonconstant and has nonzero Fourier outputs away from zero.

Two complete provider executions read 1024 actual dense coordinates and write 98 certified P=192-grid records. Each list has cutoff K=24 and 49 locations. Working precision is Q=236. Full semantic source replay passes before median construction. The unchanged outer runtime then performs all 21609 retained coefficient evaluations and certificates and writes all 512 outputs, with normalized grid b=25 and exact physical scale-back to exponent zero. The source and row associations survive caller mutation; all four single-use/output-substitution controls reject.

## Independent exact checks

The centered-target oracle directly sums every raw original coordinate at every one of M=2048 frequencies, including the centering offset. All 49 retained errors satisfy the exact squared complex rho certificate; all 1999 omitted locations satisfy the beta=1/4 premise. This is 1048576 independently assembled direct-sum terms, with no production block formula or tail bound used as its numerical target.

The original-target oracle directly sums all 512 raw original coordinates at every one of 512 output frequencies, for 262144 direct-sum terms. All output checks use the actual original L2 denominator and complex modulus, not componentwise relative error or Cartesian maximum. TARGET_CHECKS.json contains every exact squared-error upper bound and the certified rational global ratio.

These oracles reuse the byte-identical independent reviewer sine construction, which differs from production in its pi identity, fixed-grid Taylor recurrence and interval arithmetic. Their inverse-root enclosures use independent integer bisection. The direct summation and all oracle/export costs are separate harness work, not hidden in the production theorem or receipts.

Eleven additional recognition controls pass, including zero, noncanonical input, Boolean, partition errors, oversized exponent, excessive scale/variation and a changed last dense value that exceeds the variation budget. Both dense late-failure controls pay all 512 visits. Additional accepted controls include dense/block representation equivalence, an eight-step monotone original, the C=8 budget boundary and seven independently checked coefficients from a complex three-block original. These seven evaluations are a partial extra example, not a second full outer execution.

There are also 44 allocation-free structural/precision plans through m=1024 and 12 exact affine-family energy/variation checks. They do not assert large-length numerical execution.

## Theorem and complete costs

PROOF.md establishes ||Z-U_M J_N u||_infinity <= M^(-1/4)||u||_2 using the zero-extended variation tail. The original class allows arbitrary block endpoints and unequal complex values, restricted by its verified variation-to-energy budget. The exact centered spectrum remains subject to the old support lower bound M-N+1; no constant-size exact centered support is asserted.

For raw-width parameter L=2+m+W+f, q blocks and S=2C*2^ceil(m/4)+1 candidates, the conservative front bounds are O(NL^6+qSL^7) for a supplied dense original and O(qL^6+qSL^7) for a supplied block descriptor. Full source replay adds that complete cost again and pays strict comparison separately. Median/adapter and outer work retain all actual history, address and counter widths. At fixed C and W,f=O(m), the complete dense path has the safe bound O(Nm^6+qM^(1/4)m^7). The q factor is never dropped. For fixed q it specializes to the old conservative form; for growing q it does not imply a fast transform.

The disjoint production work/control envelope sums to {work:,}; cumulative produced/control bits sum to {bits:,}. These are conservative source-model bounds, not actual operation counts or resident memory. COST_TOTALS.json names every included and excluded stage. The preliminary source recognition performed for the printed fixture, all independent oracles, auxiliary controls/plans, JSON, hashing and process costs remain additional finite harness work.

The complete main process, including its independent direct-sum checks and exports, observed approximately {r['observed_process_seconds']:.2f} seconds and reported maximum RSS {r['observed_process_maxrss_kib']} KiB on this host. These are observations, not asymptotic evidence or portable performance promises.

## Reproduction, source binding and boundary

SOURCE_BINDINGS.json pins the accepted copied interval primitives, all four accepted outer runtime modules, the independent oracle and the source manuscripts/review. The source primitives are reused explicitly and their work is charged; the old constant recognizer and provider are not invoked by the new path.

Run python run_example.py, python fresh_checks.py, python check_plans.py and python verify_packet.py --fresh in a copied directory for full regeneration. Plain python verify_packet.py checks the retained completed packet and its manifest seal without repeating its numerical production. Rerunning changes measured process times, so preserve the sealed directory when reproducing.

The finite provider retains m<=28, dense length<=4096, q<=64, C<=8 and bounded raw-width/scale restrictions. The theorem is parameterized more broadly, but neither these plans nor this fixture establish unrestricted executable coverage. No arbitrary-original recovery, general randomized amplification, all-length dispatcher, practical speedup, or closure of ALG-034 is claimed. No external write occurred.
'''
    (HERE/'REPORT.md').write_text(report)
    p=HERE/'README.md';text=p.read_text();text=text.replace('After the main run completes, RESULTS.json, TARGET_CHECKS.json, PROVIDER_CHECKS.json, REPORT.md and the sealed manifest give its final results. Read the final report rather than inferring completion from this reproduction description.',f'The completed main run produced 49 sparse records, evaluated all 21,609 retained outer coefficients and wrote all 512 outputs. Exact direct-sum checks certify error at most {pct}% of the actual original L2 norm for this fixture. RESULTS.json, TARGET_CHECKS.json, PROVIDER_CHECKS.json and REPORT.md retain the final evidence; independent review remains pending.')
    p.write_text(text)
    subprocess.run([sys.executable,str(HERE/'verify_packet.py'),'--fresh'],cwd=HERE,check=True,stdout=(HERE/'FRESH_VERIFICATION.stdout').open('w'),stderr=(HERE/'FRESH_VERIFICATION.stderr').open('w'))
    omit={'MANIFEST.json','SEAL.json','SEALED_VERIFICATION.stdout','SEALED_VERIFICATION.stderr'}
    manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in omit}
    dump('MANIFEST.json',manifest)
    dump('SEAL.json',{'manifest_sha256':sha(HERE/'MANIFEST.json'),'members':len(manifest),'status':'COMPLETED_BROADER_STRUCTURED_EXECUTION_PENDING_INDEPENDENT_REVIEW'})
    subprocess.run([sys.executable,str(HERE/'verify_packet.py')],cwd=HERE,check=True,stdout=(HERE/'SEALED_VERIFICATION.stdout').open('w'),stderr=(HERE/'SEALED_VERIFICATION.stderr').open('w'))
    print(json.dumps({'members':len(manifest),'fixture_relative_error_upper':r['relative_error_upper_rational'],'manifest_sha256':sha(HERE/'MANIFEST.json')}))
if __name__=='__main__':main()
