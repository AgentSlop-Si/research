#!/usr/bin/env python3
"""Rebuild degree-17 sources from byte-bound local predecessor snapshots."""
from pathlib import Path
out=Path(__file__).resolve().parent
src=out/'sources'
s=(src/'DEGREE13_search_degree13.cpp').read_text()
s=s.replace('constexpr int P=53,D=13;','constexpr int P=53,D=17;')
s=s.replace('constexpr Big ORDER=Big(26036721925606486ULL)*1000000+195973;','constexpr Big ORDER=[]() constexpr {Big r=1;for(int i=0;i<D;i++)r*=P;return r;}();')
s=s.replace('c[i-D]-=c[i];c[i-D+1]-=c[i];','c[i-D]-=6*c[i];c[i-D+1]-=c[i];')
s=s.replace('202610181140ULL','202610181239ULL').replace('splitting in degree 13','splitting in degree 17')
(out/'search_degree17.cpp').write_text(s)
s=(src/'DEGREE13_verify_literal.cpp').read_text().replace('search_degree13.cpp','search_degree17.cpp').replace('DEGREE13','DEGREE17').replace('degree 13','degree 17')
s=s.replace('[1,1,0,0,0,0,0,0,0,0,0,0,0,1]','[6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]').replace('degree\\\":13','degree\\\":17')
(out/'verify_literal.cpp').write_text(s)
s=(src/'DEGREE13_independent_literal_check.py').read_text()
s=s.replace('P=53;D=13;MOD=[1,1]+[0]*11+[1]','P=53;D=17;MOD=[6,1]+[0]*15+[1]')
s=s.replace("data['degree']==13","data['degree']==17").replace("'prime_degree':13","'prime_degree':17").replace('frobenius13','frobenius17').replace('DEGREE13','DEGREE17').replace('Since 13 is prime','Since 17 is prime').replace('degree 1 or 13','degree 1 or 17').replace('total degree 13','total degree 17')
(out/'independent_literal_check.py').write_text(s)
