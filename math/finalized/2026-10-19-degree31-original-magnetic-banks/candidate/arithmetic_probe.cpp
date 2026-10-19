#define main discovery_main_not_run
#include "search_degree31.cpp"
#undef main
#include <cassert>
void emitpoly(const Poly&p){cout<<'[';for(size_t i=0;i<p.size();i++){if(i)cout<<',';cout<<p[i];}cout<<']';}
int main(){
 const Big B=Big(1)<<128, mask=B-1;
 assert(ORDER==Big("283499278281258657725525680568509306972713148562602397"));
 assert(ORDER>B && mpz_sizeinbase(ORDER.get_mpz_t(),2)==178);
 vector<Big> exponents={B-1,B,B+1,(Big(1)<<127)-1,Big(1)<<127,ORDER-2,ORDER-1,ORDER,(ORDER+3)/8,(ORDER-1)/2};
 F a;a.a[1]=1;F b;for(int i=0;i<D;i++)b.a[i]=(i*i+3)%53;
 Poly h={F(1)};for(int j=1;j<=7;j++){F root=a+F(j);Poly v(h.size()+1);for(size_t k=0;k<h.size();k++){v[k]=v[k]-root*h[k];v[k+1]=v[k+1]+h[k];}h=v;}
 Big wrap_order=ORDER&mask;Big truncated_inv=(ORDER-2)&mask;Big truncated_sqrt=((ORDER+3)/8)&mask;Big truncated_factor=((ORDER-1)/2)&mask;
 cout<<"{\"order\":\""<<ORDER<<"\",\"bits\":"<<mpz_sizeinbase(ORDER.get_mpz_t(),2)<<",\"gmp_version\":\""<<gmp_version<<"\",\"a\":"<<a<<",\"b\":"<<b<<",\"a_times_b\":"<<a*b<<",\"inverse\":"<<a.inverse()<<",\"power_cases\":[";
 for(size_t i=0;i<exponents.size();i++){if(i)cout<<',';cout<<"{\"exponent\":\""<<exponents[i]<<"\",\"value\":"<<a.power(exponents[i])<<'}';}
 cout<<"],\"split_polynomial\":";emitpoly(h);cout<<",\"exact_split\":";emitpoly(powmod({F(0),F(1)},ORDER,h));cout<<",\"wrapped_split\":";emitpoly(powmod({F(0),F(1)},wrap_order,h));
 cout<<",\"factor_base\":";emitpoly({a,b});cout<<",\"exact_factor_power\":";emitpoly(powmod({a,b},(ORDER-1)/2,h));cout<<",\"truncated_factor_power\":";emitpoly(powmod({a,b},truncated_factor,h));
 F d=a*a,s=d.power((ORDER+3)/8);if(s*s!=d)s=s*F(23);assert(s*s==d);F ts=d.power(truncated_sqrt);if(ts*ts!=d)ts=ts*F(23);
 cout<<",\"square\":"<<d<<",\"exact_sqrt\":"<<s<<",\"truncated_sqrt\":"<<ts<<",\"truncated_inverse\":"<<a.power(truncated_inv)<<",\"wrapped_order\":\""<<wrap_order<<"\",\"exponent_low128\":{\"inverse\":\""<<truncated_inv<<"\",\"sqrt\":\""<<truncated_sqrt<<"\",\"factor\":\""<<truncated_factor<<"\"}}\n";
}
