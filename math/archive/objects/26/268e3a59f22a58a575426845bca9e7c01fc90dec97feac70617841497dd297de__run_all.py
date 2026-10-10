"""Self-contained unit tests + regression test of the previous full checkpoint."""
import io,os,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent

def run():
    print('Compiling exact modular arithmetic verifier',flush=True)
    subprocess.run(['g++','-O3','-std=c++17',str(HERE/'rankmod.cpp'),'-o',str(HERE/'rankmod')],check=True)
    print('Running new multi-stage exact tests',flush=True)
    completed=subprocess.run([sys.executable,'-m','unittest','-v','test_new_gate'],cwd=HERE)
    if completed.returncode:raise RuntimeError('New tests failed')
    print('Verifying preserved previous endpoint rank checkpoint',flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(HERE/'prior_checkpoint_full.zip') as f:
            assert f.testzip() is None
            f.extractall(tmp)
        tests=list(Path(tmp).rglob('test_exact_gate.py'))
        assert len(tests)==1,tests
        cp=subprocess.run([sys.executable,'-m','unittest','-v','test_exact_gate'],cwd=tests[0].parent)
        if cp.returncode:raise RuntimeError('Previous checkpoint test failed')
    print('PASS: 9 new + 9 previous test groups, across 2 independent verification generations',flush=True)

if __name__=='__main__':run()
