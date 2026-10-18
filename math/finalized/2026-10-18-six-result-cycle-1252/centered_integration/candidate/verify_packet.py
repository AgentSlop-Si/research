"""Check retained bytes, provenance, all original-target rows and exact totals.

No provider or outer execution is performed by this verification command.
"""
from pathlib import Path
from fractions import Fraction as F
from types import SimpleNamespace as NS
import hashlib,json,sys
from run_integration import target_checks
HERE=Path(__file__).resolve().parent
PINS={
'centered_source.py':'4aa9992ee0f9d588d88152e0b97bb2ea2973d979865491e99dabf9b36a7fae43',
'sparse_output.py':'92577edf07395237940aad94326a8d1e5c4a18b194a9162af84ada2d826edafa',
'outer_wrapper.py':'d26c4cfe6d6c1430ce59b682f24bf69e2560fae81e8de60c63fc435b69b0637e',
'production_scalar.py':'73b3bb0bebf41f7a810bf2470e9ae520bdc3e7593516850d8933dd307500091e',
'full_transfer.py':'40d90da471b62fc9ac268b78cbe9f080b149be3789253bb1dbbe43837d5c534a'}
def read(name):return json.loads((HERE/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for k,v in PINS.items():assert sha(HERE/'runtime'/k)==v
    assert sha(HERE/'retained_oracle.py')=='30e83fb47f0ae5497a88e5d58b0a011484954bc96c05ce5f6a0024dc4041f40d'
    bindings=read('SOURCE_BINDINGS.json')['local_sources']
    for f in bindings:
        p=HERE/f['snapshot_path'];assert len(p.read_bytes())==f['bytes'] and sha(p)==f['sha256']
    original=read('ORIGINAL.json');saved=read('OUTPUT.json');report=read('RESULTS.json')
    source=saved['source'];out=saved['output'];est=saved['estimates']
    assert original['kind']==source['input_kind']=='dense'
    assert original['m']==source['m']==11 and original['F']==source['F']==-36
    assert len(original['data'])==source['N']==512
    assert all(x==[source['real'],source['imag']]==[-3,5] for x in original['data'])
    assert source['h']-source['F']==source['scale']==out['scale_power']==44
    assert out['bits']==0 and out['normalized_bits']==25
    assert len(out['pairs'])==512 and out['incidences']==5733
    assert est['source']==source and est['exact_support_size']==1537 and len(est['pairs'])==13
    assert report['source_hashes']==PINS and report['source_hashes_unchanged']
    # Every delivered output is rechecked against the actual original target.
    checks=target_checks(NS(source=NS(**source),final=NS(**out)))
    assert checks==read('TARGET_CHECKS.json')
    relative=F(**checks['squared_relative_error_upper'])
    assert relative<=F(2213,100000)**2
    op=read('RETAINED_TARGET_CHECKS.json')
    assert op['all_rows_checked']==512 and op['independent_coefficient_calls']==5733
    assert sum(x['terms'] for x in op['rows'])==5733
    assert all(x['squared_endpoint_error']<=x['squared_allowed_error'] for x in op['rows'])
    receipts=report['receipts'];front=receipts['front_production'];replay=receipts['source_replay']['replay_production'];cmp=receipts['source_replay']['comparison'];outer=receipts['outer_transfer']['outer_and_scatter'];scalar=receipts['outer_transfer']['scalar']
    assert front['events']['dense_coordinate_visits']==replay['events']['dense_coordinate_visits']==512
    assert scalar['operations']['coefficient_call']==scalar['operations']['certificate_pass']==5733
    assert scalar['operations']['pi_setup']==scalar['operations']['sqrt_setup']==1
    costs=read('COST_TOTALS.json')
    assert costs['disjoint_production_work_upper_sum']==sum(x['arithmetic_bit_work_upper']+x['control_bit_work_upper'] for x in (front,replay,cmp))+outer['bit_work']+scalar['total_bit_work_upper']
    assert costs['disjoint_cumulative_produced_control_bits_upper_sum']==sum(x['cumulative_bits_upper'] for x in (front,replay,cmp))+outer['produced_bits']+scalar['cumulative_integer_and_control_storage_bits_upper']
    assert len(report['rejection_controls'])==4 and all(x['rejected'] for x in report['rejection_controls'])
    assert len(read('BOUNDARY_CONTROLS.json')['controls'])==5
    assert read('PROCESS_EXIT.json')['exit_code']==read('ORACLE_EXIT.json')['exit_code']==0
    assert (HERE/'RUN.stderr').stat().st_size==(HERE/'ORACLE.stderr').stat().st_size==(HERE/'BOUNDARY.stderr').stat().st_size==0
    n=None
    if (HERE/'MANIFEST.json').exists() and '--fresh' not in sys.argv:
        manifest=read('MANIFEST.json');n=0
        for f in manifest['files']:
            p=HERE/f['path'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256'];n+=1
        assert sha(HERE/'MANIFEST.json')==read('SEAL.json')['manifest_sha256']
    print(json.dumps({'verified':True,'accepted_runtime_sources':5,'local_source_bindings':len(bindings),
        'all_original_target_rows_rechecked':512,'all_retained_target_records_validated':512,
        'certified_relative_error_at_most':'0.02213','exact_cost_sums_verified':True,
        'all_nine_rejection_controls_recorded':True,'manifest_members_checked':n},indent=2))
if __name__=='__main__':main()
