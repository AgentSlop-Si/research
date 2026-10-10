from pathlib import Path
import hashlib,zipfile,tempfile,subprocess,sys
ROOT=Path(__file__).resolve().parent

def run(args,cwd):
    r=subprocess.run(args,cwd=cwd,text=True,capture_output=True,check=False)
    if r.stdout:print(r.stdout,flush=True)
    if r.stderr:print(r.stderr,flush=True)
    if r.returncode:raise RuntimeError(f'test returned {r.returncode}: {args}')

def main():
    print('Checking current seven regression groups:',flush=True)
    run([sys.executable,'-m','unittest','-v','test_new_gate'],str(ROOT))
    print('Checking previous checkpoint archive:',flush=True)
    p=ROOT/'prior_checkpoint_full.zip'
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        with tempfile.TemporaryDirectory() as tmp:
            z.extractall(tmp)
            prior=Path(tmp)/'fft_bitrev_multistage_geometry_2026-10-09'
            assert prior.exists()
            run(['g++','-O3','-std=c++17','rankmod.cpp','-o','rankmod'],str(prior))
            run([sys.executable,'-m','unittest','-v',
                 'test_new_gate.TestNewMultistageGate.test_dimension_bound',
                 'test_new_gate.TestNewMultistageGate.test_bitrev_n8_all_depths',
                 'test_new_gate.TestNewMultistageGate.test_saved_json_is_consistent'],str(prior))
    print(f'PASS 7 new groups, 3 previous smoke checks, prior archive SHA256={sha}',flush=True)

if __name__=='__main__':main()
