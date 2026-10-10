"""Extract the previous full checkpoint from a bundled ZIP when needed."""
from pathlib import Path
import sys,zipfile
ROOT=Path(__file__).resolve().parent
TARGET=ROOT/'_prior_extracted'/'fft_triple_intersection_gate_2026-10-09'

def activate():
    if not (TARGET/'exact_polynomial_gate.py').is_file():
        archive=ROOT/'prior_checkpoint_full.zip'
        if not archive.exists():
            raise FileNotFoundError(f'Package missing {archive}. Recreate from the full research ZIP.')
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            z.extractall(ROOT/'_prior_extracted')
    if str(TARGET) not in sys.path:sys.path.insert(0,str(TARGET))
    return TARGET
