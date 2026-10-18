#!/usr/bin/env python3
import ast,hashlib,json,pathlib,sys,zipfile
HERE=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path(__file__).resolve().parent / '../candidate'
pins=json.loads((SRC/'SOURCE_PINS.json').read_text())
# Portable source I/O only: exact included members and public antecedent copies.
assert pins['archive_sha256']=='936bf7706643fc130c7cb1197848bf1c2bf193be533cdc01e6c3b265351c1581'
for member,expected in pins['source_members'].items():
 assert hashlib.sha256((SRC/'source'/member).read_bytes()).hexdigest()==expected
for label,expected in pins['accepted_documents'].items():
 assert hashlib.sha256((SRC/pins['public_accepted_document_paths'][label]).read_bytes()).hexdigest()==expected
sys.path.insert(0,str(SRC))
import shared_dispatcher as M
# A fixed default threshold does not guarantee that a shifted input's core
# enters the base case. This concrete control exercises the correct continuation.
C=(1<<2048)+1;A=C<<100003;B=C<<23019
D=M.Dispatcher();v=D.multiply(A,B);assert v==A*B
assert D.stats['base']==0 and D.stats['sparse_shared']==1 and D.stats['calls']==1
host=[]
for node in ast.walk(ast.parse((SRC/'shared_dispatcher.py').read_text())):
 if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Mult):host.append({'line':node.lineno,'expression':ast.unparse(node)})
result={'historical_archive_sha256':pins['archive_sha256'],'verified_historical_source_members':len(pins['source_members']),'verified_accepted_documents':2,'historical_programs_imported_or_executed':False,'threshold_crossing':{'input_bits':[A.bit_length(),B.bit_length()],'core_bits':C.bit_length(),**D.summary()},'host_multiplication_expressions':sorted(host,key=lambda z:z['line']),'all_passed':True}
(HERE/'PROVENANCE_AND_THRESHOLD_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'historical_pin_checks':8,'threshold_stats':dict(D.stats),'core_bits':C.bit_length(),'all_passed':True},indent=2))
