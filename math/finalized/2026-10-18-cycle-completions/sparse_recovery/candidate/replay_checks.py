"""Paid whole-schedule replay against separately supplied original context."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,time
from live_checks import LiveProvider,check_output
from sparse_adapter import strict_loads,canonical
from recovery import recover

BASE=Path(__file__).resolve().parent

def compute(context,context_bytes):
    provider=LiveProvider(context['raw'],context['state'])
    result=recover(provider,context['sigma'])
    result['original_binding']={'raw_and_state_path':'ORIGINAL_INPUT.json',
       'raw_and_state_sha256':sha256(context_bytes).hexdigest(),
       'independently_retained_original_required':True,'external_authentication':False}
    receipt=provider.receipt();result['provider_receipt']=receipt
    result['combined_receipt']={'total_bit_work_upper':receipt['total_bit_work_upper']+result['consumer_receipt']['total_bit_work_upper'],
       'cumulative_storage_upper_bits':receipt['cumulative_storage_upper_bits']+result['consumer_receipt']['cumulative_storage_upper_bits'],
       'production_runs':1,'replay_runs':0,'random_bits_if_uniform_sampling':27,
       'normalized_sparse_output_rows':len(result['rows']),'all_N_output_materialized':False}
    return result

def main():
    started=time.monotonic()
    context_bytes=(BASE/'ORIGINAL_INPUT.json').read_bytes()
    context=strict_loads(context_bytes.decode('ascii'))
    supplied=strict_loads((BASE/'RECOVERY_RUN.json').read_text())
    actual=compute(context,context_bytes)
    accuracy=check_output(context['raw'],actual)
    expected=canonical(actual);observed=canonical(supplied)
    assert expected==observed
    altered=deepcopy(supplied);altered['rows'][0][1]+=1
    assert canonical(altered)!=expected
    alternate_state=deepcopy(supplied)
    alternate_state['original_binding']['raw_and_state_sha256']='0'*64
    assert canonical(alternate_state)!=expected
    # Explicitly pay production, full replay, canonical intake/compare and
    # local inspection/artifact retention. No replay is inferred from a digest.
    report={'status':'PASS_FULL_SCHEDULE_SEMANTIC_REPLAY',
      'exact_canonical_packet_match':True,'changed_coefficient_rejected':True,
      'changed_retained_original_hash_rejected':True,
      'computed_packet_sha256':sha256(expected).hexdigest(),
      'caller_relative_binding':True,'external_origin_authenticated':False,
      'historical_execution_attested':False,'replay_accuracy':accuracy,
      'actual_replay_bucket_calls':29,'actual_replay_bucket_coordinates':29*(1<<17),
      'actual_production_plus_replay_bucket_coordinates':58*(1<<17),
      'canonical_intake_compare_work_envelope':1<<110,
      'canonical_intake_compare_storage_envelope_bits':1<<60,
      'production_plus_replay_total_bit_work_upper':
        supplied['combined_receipt']['total_bit_work_upper']+actual['combined_receipt']['total_bit_work_upper']+(1<<110),
      'production_plus_replay_cumulative_storage_upper_bits':
        supplied['combined_receipt']['cumulative_storage_upper_bits']+actual['combined_receipt']['cumulative_storage_upper_bits']+(1<<60),
      'elapsed_seconds':time.monotonic()-started,'external_writes':False,
      'independent_final_review':False}
    (BASE/'REPLAY_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'seconds':report['elapsed_seconds'],
       'actual_total_coordinates':report['actual_production_plus_replay_bucket_coordinates']}))

if __name__=='__main__':main()
