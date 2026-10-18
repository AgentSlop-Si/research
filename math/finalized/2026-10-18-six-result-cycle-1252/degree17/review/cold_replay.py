#!/usr/bin/env python3
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='degree17-independent-cold-') as t:
 p=Path(t);(p/'inputs').mkdir();shutil.copyfile(R/'review_check.py',p/'review_check.py');shutil.copyfile(R/'inputs/DEGREE17_LITERAL_CERTIFICATE.json',p/'inputs/DEGREE17_LITERAL_CERTIFICATE.json')
 result=subprocess.run(['python','-I',str(p/'review_check.py'),str(p/'inputs'),str(p)],capture_output=True,text=True)
 (R/'COLD_RUN.log').write_text(result.stdout+result.stderr);assert result.returncode==0
 replay=(p/'ARITHMETIC.json').read_bytes();original=(R/'ARITHMETIC.json').read_bytes();assert original==replay
 receipt={'verdict':'PASS','exit_code':result.returncode,'isolated_inputs':['review_check.py','inputs/DEGREE17_LITERAL_CERTIFICATE.json'],'candidate_code_executed':False,'arithmetic_byte_identical':True,'arithmetic_sha256':hashlib.sha256(original).hexdigest(),'checker_sha256':hashlib.sha256((R/'review_check.py').read_bytes()).hexdigest()}
 (R/'COLD_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
