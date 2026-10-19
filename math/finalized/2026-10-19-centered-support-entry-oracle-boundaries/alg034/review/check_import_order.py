#!/usr/bin/env python3
from pathlib import Path
import importlib.util,sys,json
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('order_probe',D/'order_probe'/'check_obstruction.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert 'bounded_variation' not in sys.modules and 'interval_core' not in sys.modules
try:m.main()
except AssertionError:pass
else:raise AssertionError('Mismatch was accepted')
assert 'bounded_variation' not in sys.modules and 'interval_core' not in sys.modules
out={'status':'PASS_INDEPENDENT_REPAIRED_IMPORT_ORDER','module_import_did_not_import_recognition':True,'dependency_mismatch_rejected_before_recognition_import':True,'isolated_copy_only':True}
(D/'IMPORT_ORDER_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
