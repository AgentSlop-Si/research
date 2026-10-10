"""Independent fresh-prior extraction + 9 new tests + exhaustive GF(17) audit."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent

def run(cmd, cwd):
    print('\n$', ' '.join(map(str,cmd)), 'in', str(cwd), flush=True)
    result=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,check=False)
    print(result.stdout, flush=True)
    print(result.stderr, flush=True)
    if result.returncode:
        raise RuntimeError(f'command exited {result.returncode}: {cmd}')
    return result.stdout+'\n'+result.stderr

def main():
    new=run([sys.executable,'test_new_gate.py'],HERE)
    assert 'Ran 9 tests' in new and 'OK' in new
    with tempfile.TemporaryDirectory(prefix='fft_spectral_prior_') as temp:
        zpath=HERE/'previous_research_checkpoint.zip'
        with zipfile.ZipFile(zpath) as z:
            corrupt=z.testzip()
            if corrupt is not None:raise RuntimeError(f'Archive member corrupt: {corrupt}')
            z.extractall(temp)
        past=Path(temp)/'fft_dual_support_gate_2026-10-09'
        assert (past/'run_all.py').is_file()
        old=run([sys.executable,'run_all.py'],past)
        assert 'FINAL: 55/55 passing tests' in old
    from exhaust_smallfield import go
    measured=go(17)
    expected=json.loads((HERE/'exhaustive_GF17_chart.json').read_text())
    for key in ('h_checked','tail_linear_exception','t_zero','tail_plus_quartic',
                'upper_necessary_gamma_pairs','eight_param_exception','invertible_candidate','full_B_success'):
        assert measured['counts'][key]==expected['counts'][key],(key,measured['counts'][key],expected['counts'][key])
    print('\nFINAL: 64/64 passing tests: 9 new + 55 previous; exhaustive GF(17) regular-patch audit reproduced',flush=True)
    return new,old

if __name__=='__main__':main()
