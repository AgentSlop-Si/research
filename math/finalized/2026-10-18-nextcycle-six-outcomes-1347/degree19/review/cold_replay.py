#!/usr/bin/env python3
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='degree19-independent-review-') as td:
 p=Path(td);(p/'inputs').mkdir()
 shutil.copyfile(R/'review_check.py',p/'review_check.py')
 shutil.copyfile(R/'inputs'/'DEGREE19_LITERAL_CERTIFICATE.json',p/'inputs'/'DEGREE19_LITERAL_CERTIFICATE.json')
 proc=subprocess.run([sys.executable,'-I','review_check.py'],cwd=p,capture_output=True,text=True)
 (R/'COLD_RUN.log').write_text(proc.stdout+proc.stderr)
 assert proc.returncode==0,proc.stderr
 result=(p/'ARITHMETIC.json').read_bytes();assert result==(R/'ARITHMETIC.json').read_bytes()
 out={'verdict':'PASS','isolated_inputs':['review_check.py','inputs/DEGREE19_LITERAL_CERTIFICATE.json'],'process_returncode':proc.returncode,'byte_identical_arithmetic':True,'arithmetic_sha256':hashlib.sha256(result).hexdigest(),'review_checker_sha256':hashlib.sha256((R/'review_check.py').read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256((p/'inputs'/'DEGREE19_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest()}
 (R/'COLD_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
