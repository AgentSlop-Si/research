#!/usr/bin/env python3
"""Rebuild degree-19 sources from byte-bound degree-17 snapshots."""
from pathlib import Path
out=Path(__file__).resolve().parent;src=out/'sources'
s=(src/'DEGREE17_search_degree17.cpp').read_text()
s=s.replace('constexpr int P=53,D=17;','constexpr int P=53,D=19;')
s=s.replace('c[i-D]-=6*c[i]','c[i-D]-=12*c[i]')
s=s.replace('202610181239ULL','202610181330ULL').replace('splitting in degree 17','splitting in degree 19')
(out/'search_degree19.cpp').write_text(s)
s=(src/'DEGREE17_verify_literal.cpp').read_text().replace('search_degree17.cpp','search_degree19.cpp').replace('DEGREE17','DEGREE19').replace('degree 17','degree 19')
s=s.replace('[6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]','[12,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]').replace('degree\\\":17','degree\\\":19')
(out/'verify_literal.cpp').write_text(s)
s=(src/'DEGREE17_independent_literal_check.py').read_text()
s=s.replace('P=53;D=17;MOD=[6,1]+[0]*15+[1]','P=53;D=19;MOD=[12,1]+[0]*17+[1]')
s=s.replace("data['degree']==17","data['degree']==19").replace("'prime_degree':17","'prime_degree':19").replace('frobenius17','frobenius19').replace('DEGREE17','DEGREE19').replace('Since 17 is prime','Since 19 is prime').replace('degree 1 or 17','degree 1 or 19').replace('total degree 17','total degree 19')
(out/'independent_literal_check.py').write_text(s)
s=(src/'DEGREE17_field_verify.py').read_text().replace('D=17;MOD=[6,1]+[0]*15+[1]','D=19;MOD=[12,1]+[0]*17+[1]').replace('D=17','D=19').replace('degrees 1 or 17','degrees 1 or 19').replace('degree 17: X^(53^17)','degree 19: X^(53^19)').replace('u^17+u+6','u^19+u+12')
(out/'field_verify.py').write_text(s)
