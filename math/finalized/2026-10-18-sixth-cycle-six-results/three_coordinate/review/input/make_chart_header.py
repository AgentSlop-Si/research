import json
from pathlib import Path
p=Path(__file__).resolve().parent
c=json.loads((p/'sources/CHART.json').read_text())
def arr(a):return '{'+','.join(arr(x)if isinstance(x,list)else str(x)for x in a)+'}'
(p/'chart_data.hpp').write_text('// Fresh data transcription from the pinned JSON, not historical executable code.\nint cycles[2][3][8]='+arr([x['cycles']for x in c['stages']])+';\nint pairs[2][17][2]='+arr([x['gaussian_pairs']for x in c['stages']])+';\n')
