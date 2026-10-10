from pathlib import Path
import tempfile,shutil,subprocess,sys
here=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as d:
 shutil.copy2(here/'check_green_and_flow.py',d)
 subprocess.run([sys.executable,'check_green_and_flow.py'],cwd=d,stdout=subprocess.DEVNULL,check=True)
 assert (Path(d)/'INDEPENDENT_RESULTS.json').read_bytes()==(here/'INDEPENDENT_RESULTS.json').read_bytes()
print('ISOLATED REPLAY PASS')
