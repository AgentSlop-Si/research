"""Emit exact-width positive controls, no search or external dependency."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent/'results'
for n in [4,8,16]:
 word=[{'op':'h2','pair':[i,i^(1<<s)]} for s in range(n.bit_length()-1) for i in range(n) if i&(1<<s)==0]
 cert={'name':f'ordinary H{n} tensor schedule','width':n,'extra_registers':0,'word':word,'target':'H_n[i,j]=(-1)^popcount(i&j)','independent_arbitrary_inputs':True}
 (D/f'baseline_{n}.json').write_text(json.dumps(cert,indent=2))
shear={'name':'source-derived unit upper shear with three forward H2 calls','width':2,'extra_registers':0,'word':[
 {'op':'diagonal','values':['5/4','1']},{'op':'h2','pair':[0,1]},
 {'op':'diagonal','values':['-3','1']},{'op':'h2','pair':[0,1]},
 {'op':'diagonal','values':['2','1']},{'op':'h2','pair':[0,1]},
 {'op':'diagonal','values':['-1/10','-1/6']}],
 'source':'https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/local.tex'}
(D/'unit_shear.json').write_text(json.dumps(shear,indent=2))
