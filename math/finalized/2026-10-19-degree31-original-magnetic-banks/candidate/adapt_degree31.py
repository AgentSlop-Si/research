"""Reviewed source adaptation; original sources are inert bytes and never executed."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;S=R/'sources';F=json.loads((R/'FIELD_IRREDUCIBILITY.json').read_text());assert F['verdict']=='PASS';D=31;C=11;A=2;Q=53**31
assert F['modulus_ascending']==[C,A]+[0]*29+[1]
repl={'D=29':'D=31','degree29':'degree31','DEGREE29':'DEGREE31','degree 29':'degree 31','degree-29':'degree-31','prime_degree\':29':'prime_degree\':31','frobenius29':'frobenius31',"==29":"==31",'167':'178','202610181745':'202610192024','MOD=[8,1]+[0]*27+[1]':'MOD=[11,2]+[0]*29+[1]','100925339366770615067826870974905413660631238363333':str(Q)}
def base(name):
 s=(S/name).read_text()
 for a,b in repl.items():s=s.replace(a,b)
 return s
s=base('search_degree29.cpp');s=s.replace('c[i-D]-=8*c[i];c[i-D+1]-=c[i];','c[i-D]-=11*c[i];c[i-D+1]-=2*c[i];')
s=s[:s.index('int main(int argc,char**argv)')]+r'''int main(int argc,char**argv){
 setup();int limit=argc>1?stoi(argv[1]):100000;if(limit<0||limit>100000)return 9;
 ofstream ledger("PREFIX_LEDGER.jsonl");uint64_t candidates=0,zero_draws=0;auto start=chrono::steady_clock::now();
 for(int trial=0;trial<limit;trial++){
  uint64_t before=rng;F y=randomF();if(y.zero()){ledger<<"{\"zero_draw\":true,\"rng_before\":"<<before<<",\"rng_after\":"<<rng<<"}\n";zero_draws++;trial--;continue;}
  array<F,14>yp;yp[0]=1;for(int j=1;j<14;j++)yp[j]=yp[j-1]*y;Poly c,n;
  if(!line(yp,c,n)){ledger<<"{\"trial\":"<<trial<<",\"chart_failure\":true,\"y\":"<<y<<"}\n";cerr<<"unexpected chart failure\n";return 3;}
  auto q=gate(yp,c,n);auto ls=roots2(q);ledger<<"{\"trial\":"<<trial<<",\"rng_before\":"<<before<<",\"rng_after\":"<<rng<<",\"y\":"<<y<<",\"gate_roots\":[";
  bool hit=false;Poly chosen;F chosenlam;
  for(size_t li=0;li<ls.size();li++){F lam=ls[li];Poly h(8);for(int j=0;j<8;j++)h[j]=c[j]+lam*n[j];bool nonzero=!h[0].zero();bool splits=false;if(nonzero){candidates++;splits=split(h);}
   if(li)ledger<<',';ledger<<"{\"lambda\":"<<lam<<",\"H\":[";for(int j=0;j<8;j++){if(j)ledger<<',';ledger<<h[j];}ledger<<"],\"nonzero_constant\":"<<(nonzero?"true":"false")<<",\"fully_splits\":"<<(splits?"true":"false")<<'}';
   if(splits){hit=true;chosen=h;chosenlam=lam;break;}
  }
  ledger<<"],\"cumulative_candidates\":"<<candidates<<",\"hit\":"<<(hit?"true":"false")<<"}\n";
  if(hit){ledger.flush();cout<<"{\"trial\":"<<trial<<",\"candidates\":"<<candidates<<",\"nonzero_nodes\":"<<trial+1<<",\"zero_draws\":"<<zero_draws<<",\"coefficient_draws\":"<<(trial+1+zero_draws)*D<<",\"y\":"<<y<<",\"lambda\":"<<chosenlam<<",\"H\":[";for(int j=0;j<8;j++){if(j)cout<<',';cout<<chosen[j];}cout<<"]}\n";return 0;}
  if(trial%100==0){double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();cerr<<"trial "<<trial<<" candidates "<<candidates<<" seconds "<<seconds<<'\n';}
 }
 ledger.flush();cerr<<"NO_SPLIT declared trials="<<limit<<" candidates="<<candidates<<'\n';return 1;
}
'''
(R/'search_degree31.cpp').write_text(s)
s=base('verify_literal.cpp');old='[8,1,'+','.join(['0']*27)+',1]';new='[11,2,'+','.join(['0']*29)+',1]';s=s.replace(old,new).replace('degree\\\":29','degree\\\":31');(R/'verify_literal.cpp').write_text(s)
s=base('independent_literal_check.py');s=s.replace('# Since 29 is prime','# Since 31 is prime').replace('1 or 29','1 or 31').replace('degree 29','degree 31')
# Check all full sectors directly from supplied amplitudes, independent of discovery.
needle='    wrong_sign=omitted13=perturbed=0'
extra='''    sector_checks=0
    def gaussian(e,d,a,b):
        r=e*a%13;l=d*b%13
        if r+l>=13:return 0
        w=pow(16,e*d%13,P);v=1
        for i in range(1,l+1):v=v*(1-pow(w,r+i,P))*pow((1-pow(w,i,P))%P,-1,P)%P
        return v
    for b in range(13):
        for a in range(13):
            v=ZERO
            for bank in banks:
                e,d=bank['epsilon'],bank['delta']
                v=add(v,scale(mul(tuple(bank['amplitudes'][b]),power(tuple(bank['alpha']),e*a%13)),gaussian(e,d,a,b)))
            assert v==scalar(pow(16,10*(a+b)**2%13,P));sector_checks+=1
'''
s=s.replace(needle,extra+needle).replace("'banks':16,'nonbase", "'full_sector_equalities':sector_checks,'banks':16,'nonbase")
s=s.replace('    start=time.time()','    start=time.time()\n    assert all(P%d for d in range(2,8)) and all(D%d for d in range(2,6))')
(R/'independent_literal_check.py').write_text(s)
(R/'arithmetic_probe.cpp').write_text(base('arithmetic_probe.cpp'))
(R/'check_arithmetic.py').write_text(base('check_arithmetic.py'))
s=base('check_convolution_boundary.py');s=s.replace('c[k-D+1]-=c[k];c[k-D]-=8*c[k]','c[k-D+1]-=2*c[k];c[k-D]-=11*c[k]').replace('==78416','==83824').replace('[24,25,29]','[24,25,31]').replace('(1+1+8)','(1+2+11)');(R/'check_convolution_boundary.py').write_text(s)
print('Adapted reviewed sources to',Q)
