"""Fresh-extraction verification of Phase 22 and inherited Phase 12-21 suites."""
from __future__ import annotations
import pathlib,hashlib,zipfile,tempfile,subprocess,sys,os

def main(path):
    path=pathlib.Path(path).resolve()
    with tempfile.TemporaryDirectory(prefix='phase22_fresh_') as d:
        root=pathlib.Path(d)
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None,'Phase22 corrupt zip'
            z.extractall(root)
        here=root/'fft_green_phase22_gram_gate'
        for line in (here/'SHA256SUMS.txt').read_text().splitlines():
            h,rel=line.split('  ',1)
            p=here/rel
            assert p.is_file(),rel
            assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
        env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['PYTHONPATH']=str(here)
        result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],
                              cwd=here,env=env,text=True,capture_output=True,timeout=180)
        print('PHASE 22 TESTS: status=',result.returncode)
        print('\n'.join((result.stdout+result.stderr).splitlines()[-5:]))
        if result.returncode:
            print(result.stdout,result.stderr)
            raise RuntimeError('Phase22 regression failed')
        aud=subprocess.run([sys.executable,'audit.py'],cwd=here,env=env,
                           capture_output=True,text=True,timeout=180)
        assert aud.returncode==0,aud.stderr
        print(aud.stdout)
        previous=here/'previous_full_phase21_checkpoint.zip'
        with zipfile.ZipFile(previous) as z:
            assert z.testzip() is None,'Phase21 corrupted'
            z.extractall(root/'prev')
        runner=root/'prev'/'fft_green_phase21_weyl_resolvent'/'verify_full_lineage.py'
        assert runner.is_file()
        r=subprocess.run([sys.executable,str(runner),str(previous)],env=env,
                         capture_output=True,text=True,timeout=240)
        print(r.stdout)
        if r.returncode:
            print(r.stderr)
            raise RuntimeError('Phase12-21 inherited validation failed')
        print('TOTAL VERIFIED: 12 NEW + 222 PRIOR = 234 TESTS (PHASES 12-22)')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: verify_full_lineage.py /path/phase22.zip')
    main(sys.argv[1])
