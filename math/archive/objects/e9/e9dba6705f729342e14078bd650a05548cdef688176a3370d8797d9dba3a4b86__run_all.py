from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import zipfile

ROOT=os.path.dirname(os.path.abspath(__file__))

def run(*args):
    print("$",*args,flush=True)
    subprocess.run(args,cwd=ROOT,check=True)

def main():
    run(sys.executable,"generate_results.py")
    run(sys.executable,"-m","unittest","-v","test_checkpoint")
    run(sys.executable,"independent_verifier.py")
    prior=os.path.join(ROOT,"PRIOR_v26_COMPLETE.zip")
    assert zipfile.ZipFile(prior).testzip() is None
    print("PRIOR ZIP CRC OK")
    print("ALL CHECKS PASSED")

if __name__=="__main__":main()
