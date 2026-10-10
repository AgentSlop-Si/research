"""Run exact linear-work first-cross controls at much larger lengths."""
import json
from pathlib import Path
from phase35_balance import planted_control

def run():
    return {'large_exact_field_controls':[planted_control(n) for n in (8192,16384,65536)],
            'claim':'matches full first row/column only, NOT an FFT'}

if __name__=='__main__':
    out=run()
    Path('scale_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    for c in out['large_exact_field_controls']:
        print('N={} first-cross exact={} second Fourier column wrong at {} coordinates'.format(
            c['N'],c['first_row_and_column_exact'],c['second_column_mismatch_coordinates']))
