"""Exact-rational checks of the conservative proof constants."""
from fractions import Fraction as Q
from pathlib import Path
import json
O=Path(__file__).resolve().parent
rho=Q(1,1<<464);theta=Q(1,1<<400);eta=Q(3073,20**114)
eps=rho+6*eta
assert eta<Q(1,1<<480)
assert eps<2*rho
r=Q(1,1<<62);delta=Q(1,1<<162)
phase_deviation=2*r+r*r+delta*(1+r)**2
assert phase_deviation<Q(1,2)
assert eps+Q(1,1<<478)+rho<3*rho<4*rho
assert 8*theta+16*rho<9*theta
assert Q(120,16384)==Q(15,2048)
assert 1-Q(120,16384)==Q(2033,2048)
assert (5631+129)*2048+20000+6*16*8192==12602912<30_000_000
assert (1<<19)+6*(1<<20)+4096<8_000_000
assert 11*64*sum(range(28))+1000<1_000_000
assert Q(3073,1<<1024)<rho/4
# Every nearest bucket interval contains the entire normalizer interval.
for q in range(-1024,1025):assert q-1536<=-512 and q+1536>=512
# Bounds on legal public value widths: lambda<6, 0<=K<=3073.
assert (6*3073*(1<<464)+1).bit_length()<=480
assert (3073*(1<<560)+(1<<82)).bit_length()<=580
out={'status':'PASS_EXACT_RATIONAL_PROOF_MARGINS','nearest_passband_integer_points':2049,
     'success_probability':[2033,2048],'maximum_root_records_bound':11*64*sum(range(28))+1000,
     'six_call_numeric_operations_bound':12602912,'six_call_plus_windows_slots_bound':(1<<19)+6*(1<<20)+4096,
     'phase_relative_deviation_upper_numerator':phase_deviation.numerator,'phase_relative_deviation_upper_denominator':phase_deviation.denominator,
     'amplitude_bound_strictly_less_than_3rho':True,'final_norm_bound_strictly_less_than_9theta':True,
     'exact_support_indistinguishability_margin_valid':True}
(O/'EXACT_MARGIN_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
