from pathlib import Path
src=Path(__file__).resolve().parent/'adaptation_inputs'
out=Path(__file__).resolve().parent
s=(src/'search_nonstable.cpp').read_text()
s=s.replace('constexpr int P=53,D=11;','constexpr int P=53,D=13;\nusing Big=__uint128_t;')
s=s.replace('constexpr uint64_t ORDER=9269035929372191597ULL;','constexpr Big ORDER=Big(26036721925606486ULL)*1000000+195973;')
s=s.replace('int c[21]={}', 'int c[2*D-1]={}').replace('for(int i=20;i>=11;i--){c[i-11]-=3*c[i];c[i-10]-=c[i];}','for(int i=2*D-2;i>=D;i--){c[i-D]-=c[i];c[i-D+1]-=c[i];}')
s=s.replace('power(uint64_t e)','power(Big e)').replace('Poly x,uint64_t e','Poly x,Big e')
s=s.replace('202610181044ULL','202610181140ULL')
s=s.replace('bool split(const Poly&h){return powmod({F(0),F(1)},ORDER,h)==Poly({F(0),F(1)});}', '''bool split(const Poly&h){
 // Exact Frobenius splitting in degree 13, represented beyond uint64_t.
 return powmod({F(0),F(1)},ORDER,h)==Poly({F(0),F(1)});
}''')
s=s.replace('stoi(argv[1]):10000','stoi(argv[1]):100000')
(out/'search_degree13.cpp').write_text(s)
s=(src/'verify_literal.cpp').read_text().replace('search_nonstable.cpp','search_degree13.cpp').replace('j<11','j<D').replace('DEGREE11','DEGREE13').replace('degree 11','degree 13')
s=s.replace('[3,1,0,0,0,0,0,0,0,0,0,1]','[1,1,0,0,0,0,0,0,0,0,0,0,0,1]').replace('degree\\\":11','degree\\\":13')
(out/'verify_literal.cpp').write_text(s)
s=(src/'independent_literal_check.py').read_text()
s=s.replace('P=53;D=11;MOD=[3,1]+[0]*9+[1]','P=53;D=13;MOD=[1,1]+[0]*11+[1]')
s=s.replace('c=[0]*21','c=[0]*(2*D-1)').replace('range(20,10,-1)','range(2*D-2,D-1,-1)').replace('range(11)','range(D)').replace('==11','==13').replace("'prime_degree':11","'prime_degree':13").replace('frobenius11','frobenius13').replace('DEGREE11','DEGREE13').replace('Since 11 is prime','Since 13 is prime').replace('degree 1 or 11','degree 1 or 13').replace('total degree 11','total degree 13')
(out/'independent_literal_check.py').write_text(s)
