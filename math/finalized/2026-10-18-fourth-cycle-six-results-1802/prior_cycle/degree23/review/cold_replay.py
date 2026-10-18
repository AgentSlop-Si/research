#!/usr/bin/env python3
"""Isolated independent certificate replay and sanitized candidate GMP implementation probe."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='degree23-independent-review-') as td:
 p=Path(td);(p/'inputs').mkdir()
 shutil.copyfile(R/'review_check.py',p/'review_check.py')
 shutil.copyfile(R/'inputs'/'DEGREE23_LITERAL_CERTIFICATE.json',p/'inputs'/'DEGREE23_LITERAL_CERTIFICATE.json')
 proc=subprocess.run([sys.executable,'-I','review_check.py'],cwd=p,capture_output=True,text=True)
 (R/'COLD_RUN.log').write_text(proc.stdout+proc.stderr)
 assert proc.returncode==0,proc.stderr
 result=(p/'ARITHMETIC.json').read_bytes();assert result==(R/'ARITHMETIC.json').read_bytes()
 out={'verdict':'PASS','isolated_inputs':['review_check.py','inputs/DEGREE23_LITERAL_CERTIFICATE.json'],'process_returncode':proc.returncode,'byte_identical_arithmetic':True,'arithmetic_sha256':hashlib.sha256(result).hexdigest(),'review_checker_sha256':hashlib.sha256((R/'review_check.py').read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256((p/'inputs'/'DEGREE23_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest()}
# Separate process; the literal review above never imports or executes candidate code.
with tempfile.TemporaryDirectory(prefix='degree23-GMP-probe-') as td:
 p=Path(td)
 for name in ['search_degree23.cpp','arithmetic_probe.cpp']:
  shutil.copyfile(R.parent/'candidate'/name,p/name)
 command=['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all','arithmetic_probe.cpp','-lgmpxx','-lgmp','-o','arithmetic_probe']
 compiled=subprocess.run(command,cwd=p,capture_output=True,text=True)
 assert compiled.returncode==0,compiled.stderr
 proc=subprocess.run([str(p/'arithmetic_probe')],cwd=p,capture_output=True)
 (R/'GMP_PROBE_RUN.log').write_bytes(compiled.stdout.encode()+compiled.stderr.encode()+proc.stderr)
 assert proc.returncode==0,proc.stderr
 assert not proc.stderr
 assert proc.stdout==(R/'inputs/ARITHMETIC_PROBE.json').read_bytes()
 (R/'FRESH_GMP_PROBE.json').write_bytes(proc.stdout)
 out.update({'fresh_candidate_GMP_probe_compilation':command,'fresh_candidate_GMP_probe_exit_code':proc.returncode,'fresh_candidate_GMP_probe_byte_identical':True,'GMP_probe_undefined_behavior_sanitizer':'PASS','candidate_discovery_or_literal_program_executed':False})
(R/'COLD_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
