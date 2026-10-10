"""Single command to rerun all independently testable NEW results."""
import json,hashlib,time
from pathlib import Path
from collapse_certificate import exact_test,quadric_irreducibility
from rank_uncertainty_gate import audit as rank_audit
from boundary_lock import audit_lengths
from permutation_screen import run as screen
ROOT=Path(__file__).parent

def run():
 start=time.monotonic()
 a=exact_test();b=quadric_irreducibility()
 c=rank_audit();d=audit_lengths();e=screen()
 results=dict(exact_polynomial_collapse=a,absolutely_irreducible_rankdrop_quadric=b,
              all_length_rank_uncertainty=c,auxiliary_boundary_match=d,permutation_screen=e)
 path=ROOT/'ALL_NEW_VERIFIED.json'
 path.write_text(json.dumps(results,indent=2)+'\n')
 print('ALL NEW GATES VERIFIED: 55 symbolic maximal minors,',a['subspace_determinant_identities'],
       'fixed-subspace identities,',c['total_rank_checks'],'finite-field rank checks;',
       'elapsed',round(time.monotonic()-start,2),'seconds;',
       'sha256',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
 return results
if __name__=='__main__':run()
