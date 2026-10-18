#!/usr/bin/env python3
"""Exact, byte-replayable adaptation of accepted degree-19 sources."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'sources'
s=(S/'DEGREE19_search_degree19.cpp').read_text()
s=s.replace('#include <array>','#include <gmpxx.h>\n#include <array>')
s=s.replace('constexpr int P=53,D=19;','constexpr int P=53,D=23;')
s=s.replace('using Big=__uint128_t;','using Big=mpz_class; // Unbounded exact integers for every exponent and field order.')
s=s.replace('constexpr Big ORDER=[]() constexpr','const Big ORDER=[]()')
s=s.replace('if(e&1)','if(mpz_odd_p(e.get_mpz_t()))')
s=s.replace('c[i-D]-=12*c[i]','c[i-D]-=5*c[i]')
s=s.replace('202610181330ULL','202610181502ULL').replace('splitting in degree 19, represented beyond uint64_t','splitting in degree 23, with unbounded exact GMP exponents')
# pm operates only on tiny prime-field exponents, not Big; retain its integer bit test.
s=s.replace('int pm(int a,int e){int z=1;a=(a%P+P)%P;while(e){if(mpz_odd_p(e.get_mpz_t()))','int pm(int a,int e){int z=1;a=(a%P+P)%P;while(e){if(e&1)')
(R/'search_degree23.cpp').write_text(s)
s=(S/'DEGREE19_verify_literal.cpp').read_text().replace('search_degree19.cpp','search_degree23.cpp').replace('DEGREE19','DEGREE23').replace('degree 19','degree 23')
s=s.replace('[12,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]','[5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]').replace('degree\\\":19','degree\\\":23')
(R/'verify_literal.cpp').write_text(s)
s=(S/'DEGREE19_independent_literal_check.py').read_text()
s=s.replace('P=53;D=19;MOD=[12,1]+[0]*17+[1]','P=53;D=23;MOD=[5,1]+[0]*21+[1]')
s=s.replace("data['degree']==19","data['degree']==23").replace("'prime_degree':19","'prime_degree':23").replace('frobenius19','frobenius23').replace('DEGREE19','DEGREE23').replace('Since 19 is prime','Since 23 is prime').replace('degree 1 or 19','degree 1 or 23').replace('total degree 19','total degree 23')
(R/'independent_literal_check.py').write_text(s)
s=(S/'DEGREE19_field_verify.py').read_text().replace('D=19;MOD=[12,1]+[0]*17+[1]','D=23;MOD=[5,1]+[0]*21+[1]').replace('D=19','D=23').replace('degrees 1 or 19','degrees 1 or 23').replace('degree 19: X^(53^19)','degree 23: X^(53^23)').replace('u^19+u+12','u^23+u+5')
(R/'field_verify.py').write_text(s)
s=(S/'DEGREE19_search_field.py').read_text().replace('19','23').replace('[12,1]+[0]*17+[1]','[5,1]+[0]*21+[1]').replace('[c,1]+[0]*17+[1]','[c,1]+[0]*21+[1]').replace('assert c==12','assert c==5')
(R/'search_field.py').write_text(s)
