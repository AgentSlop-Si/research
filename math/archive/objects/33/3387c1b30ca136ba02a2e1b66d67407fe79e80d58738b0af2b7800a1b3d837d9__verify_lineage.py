"""Verify the nested Phase 14 and 13 source/test lineage supplied in the archive."""
from pathlib import Path
import os,subprocess,sys,tempfile,zipfile
root=Path(__file__).resolve().parent
new_env=os.environ.copy();new_env['OPENBLAS_NUM_THREADS']='1'
with tempfile.TemporaryDirectory(prefix='hero0_phase15_') as path:
    base=Path(path)
    with zipfile.ZipFile(root/'prior_phase14_bundle.zip') as z:
        assert z.testzip() is None
        z.extractall(base)
    ph14=base/'fft_hero0_phase14_transverse_expander'
    assert (ph14/'test_phase14.py').exists()
    a=subprocess.run([sys.executable,'-m','unittest','-q','test_phase14'],cwd=ph14,env=new_env,capture_output=True,text=True)
    print('Phase 14:',a.stderr.strip())
    assert a.returncode==0,'Phase14 tests failed'
    with zipfile.ZipFile(ph14/'prior_phase13_bundle.zip') as z:
        assert z.testzip() is None
        z.extractall(base)
    ph13=base/'fft_hero0_phase13_cut_capacity'
    assert (ph13/'test_phase13.py').exists() and (ph13/'test_lifted.py').exists()
    b=subprocess.run([sys.executable,'-m','unittest','-q','test_phase13','test_lifted'],cwd=ph13,env=new_env,capture_output=True,text=True)
    print('Phase 13:',b.stderr.strip())
    assert b.returncode==0,'Phase13 tests failed'
print('Inherited lineage: PASS')
