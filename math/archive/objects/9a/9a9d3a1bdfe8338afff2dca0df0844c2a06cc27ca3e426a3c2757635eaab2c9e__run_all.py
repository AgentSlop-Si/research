"""Run the independent new+baseline tests, parameter study and N8 negative gate."""
import subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
for args in [
    [sys.executable,'-m','unittest','-v','test_centered','v11_test_checkpoint'],
    [sys.executable,'experiment.py'],
    [sys.executable,'rank_multicut_screen.py'],
]:
    print('RUN:', ' '.join(args), flush=True)
    subprocess.run(args,cwd=p,check=True)
print('ALL INCLUDED CHECKS PASS',flush=True)
