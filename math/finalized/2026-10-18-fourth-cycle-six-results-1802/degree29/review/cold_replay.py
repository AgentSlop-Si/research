#!/usr/bin/env python3
"""Isolated independent certificate replay and separate fresh candidate GMP probe."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
steps=[]
with tempfile.TemporaryDirectory(prefix='degree29-independent-') as td:
 p=Path(td);(p/'inputs').mkdir()
 shutil.copyfile(R/'review_check.py',p/'review_check.py')
 shutil.copyfile(R/'inputs/DEGREE29_LITERAL_CERTIFICATE.json',p/'inputs/DEGREE29_LITERAL_CERTIFICATE.json')
 r=subprocess.run([sys.executable,'-I','review_check.py'],cwd=p,capture_output=True,text=True)
 (R/'COLD_LITERAL.log').write_text(r.stdout+r.stderr);assert r.returncode==0
 assert (p/'ARITHMETIC.json').read_bytes()==(R/'ARITHMETIC.json').read_bytes()
 steps.append({'step':'isolated_inert_certificate_check','exit_code':r.returncode,'arithmetic_byte_identical':True,'arithmetic_sha256':sha(p/'ARITHMETIC.json')})
 for n in ['arithmetic_probe.cpp','search_degree29.cpp']:shutil.copyfile(R.parent/'candidate'/n,p/n)
 cmd=['g++','-O2','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all','arithmetic_probe.cpp','-lgmpxx','-lgmp','-o','arithmetic_probe']
 r=subprocess.run(cmd,cwd=p,capture_output=True,text=True)
 (R/'GMP_COMPILE.log').write_text(r.stdout+r.stderr);assert r.returncode==0
 r=subprocess.run(['./arithmetic_probe'],cwd=p,capture_output=True,text=True)
 (R/'FRESH_GMP_PROBE.json').write_text(r.stdout);(R/'GMP_RUN.stderr').write_text(r.stderr)
 assert r.returncode==0 and not r.stderr
 assert r.stdout.encode()==(R/'inputs/ARITHMETIC_PROBE.json').read_bytes()
 steps.append({'step':'fresh_GMP_implementation_probe','compile_command':cmd,'exit_code':r.returncode,'undefined_behavior_sanitizer':'PASS','output_byte_identical':True,'probe_sha256':sha(R/'FRESH_GMP_PROBE.json')})
 # An unchanged 16-bit degree-23 carry guard must stop before any literal inverse.
 bad=(R/'review_check.py').read_text().replace('assert 2**16 <= D*52**2 < 2**17','assert D*52**2 < 2**16')
 (p/'unsafe16_check.py').write_text(bad)
 r=subprocess.run([sys.executable,'-I','unsafe16_check.py'],cwd=p,capture_output=True,text=True)
 (R/'UNSAFE16_GUARD.log').write_text(r.stdout+r.stderr)
 assert r.returncode!=0 and 'AssertionError' in r.stderr and 'bank ' not in r.stdout
 steps.append({'step':'unmodified_16bit_carry_guard_negative_control','nonzero_exit_observed':True,'rejected_before_literal_bank_checks':True})
 # Bypassing the carry guard while retaining 16-bit slots must still fail the
 # ordinary-convolution differential, before mathematical certificate acceptance.
 bad=(R/'review_check.py').read_text().replace('<<(17*i)','<<(16*i)').replace('>>(17*i))&131071','>>(16*i))&65535')
 (p/'unsafe16_check.py').write_text(bad)
 r=subprocess.run([sys.executable,'-I','unsafe16_check.py'],cwd=p,capture_output=True,text=True)
 (R/'UNSAFE16_DIFFERENTIAL.log').write_text(r.stdout+r.stderr)
 assert r.returncode!=0 and 'AssertionError' in r.stderr and 'bank ' not in r.stdout
 steps.append({'step':'unsafe_16bit_differential_negative_control','nonzero_exit_observed':True,'rejected_before_literal_bank_checks':True})
out={'verdict':'PASS','certificate_sha256':sha(R/'inputs/DEGREE29_LITERAL_CERTIFICATE.json'),'steps':steps,'candidate_discovery_or_literal_verifier_executed':False,'candidate_code_execution_scope':'Only the separate small GMP implementation probe was freshly built and run under UBSan. Main mathematical replay imports no candidate program.'}
(R/'COLD_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
