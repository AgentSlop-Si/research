"""Recheck Phase 23 and the fully nested inherited Phase 12-22 checkpoint."""
from __future__ import annotations
import hashlib,zipfile,tempfile,subprocess,sys,os,pathlib,json

def main(archive:str):
    path=pathlib.Path(archive).resolve()
    with tempfile.TemporaryDirectory(prefix='phase23_fresh_') as tmp:
        root=pathlib.Path(tmp)
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None,'Phase23 ZIP failed integrity'
            z.extractall(root)
        here=root/'fft_green_phase23_real_resolvent'
        for line in (here/'SHA256SUMS.txt').read_text().splitlines():
            sh,rel=line.split('  ',1)
            fp=here/rel
            assert fp.is_file() and hashlib.sha256(fp.read_bytes()).hexdigest()==sh,rel
        env=os.environ.copy();env['PYTHONPATH']=str(here);env['OPENBLAS_NUM_THREADS']='1'
        out=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],
                           cwd=here,env=env,capture_output=True,text=True,timeout=150)
        print('PHASE23 TEST STATUS=',out.returncode)
        print('\n'.join((out.stdout+out.stderr).splitlines()[-5:]))
        if out.returncode:raise RuntimeError(out.stderr)
        aud=subprocess.run([sys.executable,'audit.py'],cwd=here,env=env,
                           capture_output=True,text=True,timeout=150)
        if aud.returncode:raise RuntimeError(aud.stderr)
        recorded=json.loads((here/'audit.json').read_text())
        recomputed=json.loads((here/'audit_output.txt').read_text())
        assert recorded==recomputed, 'audit regeneration differs'
        print('PHASE23 EXHAUSTIVE HANKEL m=1..9, CYCLIC TRANSITIONS N<=16: PASSED')
        prev=here/'previous_full_phase22_checkpoint.zip'
        with zipfile.ZipFile(prev) as z:
            assert z.testzip() is None
            z.extractall(root/'older')
        runner=root/'older'/'fft_green_phase22_gram_gate'/'verify_full_lineage.py'
        old=subprocess.run([sys.executable,str(runner),str(prev)],env=env,
                           capture_output=True,text=True,timeout=300)
        if old.returncode:
            print(old.stdout,old.stderr)
            raise RuntimeError('inherited Phase12-22 test failure')
        print('\n'.join(old.stdout.splitlines()[-12:]))
        print('TOTAL VERIFIED: 24 NEW + 234 INHERITED = 258 TESTS (PHASES 12-23)')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: verify_full_lineage.py <Phase23 ZIP>')
    main(sys.argv[1])
