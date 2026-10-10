"""Self-contained Phase18 exact audit and optional immutable Phase17 replay."""
from __future__ import annotations
import argparse,os,subprocess,sys, tempfile, zipfile, pathlib

HERE=pathlib.Path(__file__).resolve().parent

def run(args,cwd,log):
    print('RUN',args,'in',cwd,flush=True)
    with open(HERE/log,'w',encoding='utf-8') as out:
        result=subprocess.run(args,cwd=cwd,stdout=out,stderr=subprocess.STDOUT)
    if result.returncode:
        print('FAILED',log, 'tail:')
        print('\n'.join((HERE/log).read_text(errors='replace').splitlines()[-40:]))
        raise SystemExit(result.returncode)
    print('PASSED',log,flush=True)

def safe_extract(z,where):
    target=pathlib.Path(where).resolve()
    for info in z.infolist():
        file=(target/info.filename).resolve()
        if not file.is_relative_to(target):raise ValueError('unsafe zip path')
    z.extractall(target)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--prior',action='store_true',help='fresh Phase17 unittest replay from its original archive')
    cfg=parser.parse_args()
    run([sys.executable,'-m','unittest','-v','test_phase18'],HERE,'TEST_RUN.log')
    run([sys.executable,'exact_basis_audit.py'],HERE,'BASIS_AUDIT.log')
    run([sys.executable,'union_audit.py'],HERE,'UNION_AUDIT.log')
    run([sys.executable,'union_benchmark.py'],HERE,'UNION_BENCHMARK.log')
    run([sys.executable,'generic_gate.py'],HERE,'GENERIC_GATE.log')
    run([sys.executable,'operation_benchmark.py'],HERE,'BENCHMARK.log')
    run([sys.executable,'precision_gate.py'],HERE,'PRECISION_GATE.log')
    if cfg.prior:
        with tempfile.TemporaryDirectory(prefix='phase18_prior_') as tmp:
            with zipfile.ZipFile(HERE/'PRIOR_PHASE17_COMPLETE.zip') as z:safe_extract(z,tmp)
            old=pathlib.Path(tmp)/'fft_hero1_phase17'
            if not (old/'test_phase17.py').exists():raise ValueError('missing prior Phase17 suite')
            run([sys.executable,'-m','unittest','-v','test_phase17'],old,'PRIOR_PHASE17_REGRESSION.log')
    print('ALL REQUESTED PHASE18 AUDITS PASSED')

if __name__=='__main__':main()
