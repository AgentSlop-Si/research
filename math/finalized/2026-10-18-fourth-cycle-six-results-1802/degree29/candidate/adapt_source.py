#!/usr/bin/env python3
"""Byte-replayable degree-29 adaptation from pinned accepted degree-23 sources."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'sources'
Q=53**29
s=(S/'DEGREE23_search_degree23.cpp').read_text()
s=s.replace('constexpr int P=53,D=23;','constexpr int P=53,D=29;').replace('c[i-D]-=5*c[i]','c[i-D]-=8*c[i]').replace('202610181502ULL','202610181745ULL').replace('splitting in degree 23','splitting in degree 29')
(R/'search_degree29.cpp').write_text(s)
s=(S/'DEGREE23_verify_literal.cpp').read_text().replace('search_degree23.cpp','search_degree29.cpp').replace('DEGREE23','DEGREE29').replace('degree 23','degree 29')
s=s.replace('[5,1,'+','.join(['0']*21)+',1]','[8,1,'+','.join(['0']*27)+',1]').replace('degree\\\":23','degree\\\":29')
(R/'verify_literal.cpp').write_text(s)
s=(S/'DEGREE23_independent_literal_check.py').read_text()
s=s.replace('P=53;D=23;MOD=[5,1]+[0]*21+[1]','P=53;D=29;MOD=[8,1]+[0]*27+[1]').replace("data['degree']==23","data['degree']==29").replace("'prime_degree':23","'prime_degree':29").replace('frobenius23','frobenius29').replace('DEGREE23','DEGREE29').replace('Since 23 is prime','Since 29 is prime').replace('degree 1 or 23','degree 1 or 29').replace('total degree 23','total degree 29')
(R/'independent_literal_check.py').write_text(s)
s=(S/'DEGREE23_field_verify.py').read_text().replace('D=23;MOD=[5,1]+[0]*21+[1]','D=29;MOD=[8,1]+[0]*27+[1]').replace('D=23','D=29').replace('degrees 1 or 23','degrees 1 or 29').replace('degree 23: X^(53^23)','degree 29: X^(53^29)').replace('u^23+u+5','u^29+u+8')
(R/'field_verify.py').write_text(s)
s=(S/'DEGREE23_search_field.py').read_text().replace('23','29').replace('[5,1]+[0]*21+[1]','[8,1]+[0]*27+[1]').replace('[c,1]+[0]*21+[1]','[c,1]+[0]*27+[1]').replace('assert c==5','assert c==8')
(R/'search_field.py').write_text(s)
s=(S/'DEGREE23_arithmetic_probe.cpp').read_text().replace('search_degree23.cpp','search_degree29.cpp').replace('4553496434179608203397220101976502751677',str(Q)).replace('==132','==167')
(R/'arithmetic_probe.cpp').write_text(s)
s=(S/'DEGREE23_check_arithmetic.py').read_text().replace('degree-23','degree-29').replace('D=23;Q=P**D;MOD=[5,1]+[0]*21+[1]','D=29;Q=P**D;MOD=[8,1]+[0]*27+[1]').replace('==132','==167')
(R/'check_arithmetic.py').write_text(s)
