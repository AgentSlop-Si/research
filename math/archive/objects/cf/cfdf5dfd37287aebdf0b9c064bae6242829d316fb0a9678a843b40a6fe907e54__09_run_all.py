"""Run new tests and independently extract & run all prior checkpoint tests."""
from __future__ import annotations
from pathlib import Path
import tempfile,zipfile,subprocess,sys
HERE=Path(__file__).resolve().parent

def run(cmd,cwd):
    print('\n$', ' '.join(map(str,cmd)),'in',cwd,flush=True)
    proc=subprocess.run(cmd,cwd=cwd,encoding='utf-8',capture_output=True)
    print(proc.stdout,flush=True)
    print(proc.stderr,flush=True)
    if proc.returncode:raise SystemExit(proc.returncode)
    return proc.stdout+proc.stderr

def main():
    new=run([sys.executable,'test_dual_gate.py'],HERE)
    with tempfile.TemporaryDirectory(prefix='fft_dual_prior_') as temp:
        with zipfile.ZipFile(HERE/'prior_checkpoint_full.zip') as z:
            if z.testzip() is not None:raise RuntimeError('ZIP checksum failure')
            z.extractall(temp)
        past=Path(temp)/'fft_inverse_quartic_gate_2026-10-09'
        old=run([sys.executable,'run_all.py'],past)
    assert 'Ran 8 tests' in new and 'ALL PASS: 10 new tests and 37 saved regression tests' in old
    print('FINAL: 55/55 passing tests: 8 new + 47 previous',flush=True)
    (HERE/'REGRESSION_LOG.txt').write_text(new+'\n'+old+'\nFINAL: 55/55 passing tests\n')

if __name__=='__main__':main()
