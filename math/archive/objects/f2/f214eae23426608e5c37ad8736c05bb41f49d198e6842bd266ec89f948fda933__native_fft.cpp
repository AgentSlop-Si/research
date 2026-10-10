#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <vector>

// No fast-math assumptions. This is floating-point code, not an exact field FFT.
struct C { double r, i; };
inline C add(C a,C b) { return {a.r+b.r,a.i+b.i}; }
inline C sub(C a,C b) { return {a.r-b.r,a.i-b.i}; }
inline C mul(C a,C b) { return {a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r}; }
inline double energy(C a) { return a.r*a.r+a.i*a.i; }
inline bool zero(C a) { return a.r==0.0 && a.i==0.0; }

struct Stats {
    std::uint64_t butterflies=0,visited_nodes=0,threshold_tests=0;
    std::uint64_t pruned_nodes=0,pruned_outputs=0,computed_outputs=0;
    std::uint64_t norm_value_volume=0,zero_value_tests=0,root_pairs=0;
    std::uint64_t full_output_writes=0,max_stack=0;
};

template<bool Count> void dit(std::vector<C>& a,const std::vector<C>& roots,Stats& s) {
    const std::size_t n=a.size();
    for(std::size_t i=1,j=0;i<n;i++) {
        std::size_t bit=n>>1;
        for(;j&bit;bit>>=1) j^=bit;
        j^=bit;
        if(i<j) std::swap(a[i],a[j]);
    }
    for(std::size_t len=2;len<=n;len<<=1) {
        const std::size_t half=len>>1,step=n/len;
        for(std::size_t start=0;start<n;start+=len) {
            for(std::size_t j=0;j<half;j++) {
                C x=a[start+j],y=mul(a[start+j+half],roots[j*step]);
                a[start+j]=add(x,y);a[start+j+half]=sub(x,y);
            }
        }
        if constexpr(Count) s.butterflies+=n/2;
    }
}

template<bool Count> void dif(std::vector<C>& a,const std::vector<C>& roots,Stats& s) {
    const std::size_t n=a.size();
    for(std::size_t len=n;len>=2;len>>=1) {
        const std::size_t half=len>>1,step=n/len;
        for(std::size_t start=0;start<n;start+=len) {
            for(std::size_t j=0;j<half;j++) {
                C x=a[start+j],y=a[start+j+half];
                a[start+j]=add(x,y);a[start+j+half]=mul(sub(x,y),roots[j*step]);
            }
        }
        if constexpr(Count) s.butterflies+=n/2;
    }
    for(std::size_t i=1,j=0;i<n;i++) {
        std::size_t bit=n>>1;
        for(;j&bit;bit>>=1) j^=bit;
        j^=bit;
        if(i<j) std::swap(a[i],a[j]);
    }
}

struct Node { std::size_t start,len,offset,stride;double energy;bool all_zero; };

template<bool Count,bool Approx>
void adaptive(std::vector<C>& a,const std::vector<C>& roots,double* output,
              double root_energy,double epsilon,double inverse_sqrt_n,double scale,Stats& s) {
    const std::size_t n=a.size();
    std::fill(output,output+2*n,0.0);
    if constexpr(Count) s.full_output_writes=n;
    std::vector<Node> stack;stack.reserve(64);
    stack.push_back({0,n,0,1,root_energy,false});
    const double threshold=epsilon*epsilon*root_energy;
    while(!stack.empty()) {
        if constexpr(Count) s.max_stack=std::max<std::uint64_t>(s.max_stack,stack.size());
        const Node node=stack.back();stack.pop_back();
        if constexpr(Count) {s.visited_nodes++;s.threshold_tests++;}
        bool prune;
        if constexpr(Approx) prune=node.energy <= threshold*double(node.stride);
        else prune=node.all_zero;
        if(prune) {
            if constexpr(Count) {s.pruned_nodes++;s.pruned_outputs+=node.len;}
            continue;
        }
        if(node.len==1) {
            const C value=a[node.start];
            output[2*node.offset]=(value.r*inverse_sqrt_n)*scale;
            output[2*node.offset+1]=(value.i*inverse_sqrt_n)*scale;
            if constexpr(Count) s.computed_outputs++;
            continue;
        }
        const std::size_t half=node.len/2,step=n/node.len;
        double left_energy=0,right_energy=0;
        bool left_zero=true,right_zero=true;
        for(std::size_t j=0;j<half;j++) {
            const C x=a[node.start+j],y=a[node.start+j+half];
            const C left=add(x,y),right=mul(sub(x,y),roots[j*step]);
            a[node.start+j]=left;a[node.start+j+half]=right;
            if constexpr(Approx) {left_energy+=energy(left);right_energy+=energy(right);}
            else {left_zero=zero(left)&&left_zero;right_zero=zero(right)&&right_zero;}
        }
        if constexpr(Count) {
            s.butterflies+=half;
            if constexpr(Approx) s.norm_value_volume+=node.len;
            else s.zero_value_tests+=node.len;
        }
        stack.push_back({node.start+half,half,node.offset+node.stride,node.stride*2,right_energy,right_zero});
        stack.push_back({node.start,half,node.offset,node.stride*2,left_energy,left_zero});
    }
}

template<bool Count>
int transform(const double* input,double* output,std::size_t n,int algorithm,double epsilon,Stats& s) {
    if(n==0 || (n&(n-1)) || algorithm<0 || algorithm>2 || !std::isfinite(epsilon) || epsilon<0) return 1;
    double scale=0;
    for(std::size_t j=0;j<2*n;j++) {
        if(!std::isfinite(input[j])) return 2;
        scale=std::max(scale,std::abs(input[j]));
    }
    if(scale==0) {
        std::fill(output,output+2*n,0.0);
        if constexpr(Count) {s.full_output_writes=n;s.pruned_outputs=n;s.pruned_nodes=1;}
        return 0;
    }
    std::vector<C> a(n),roots(n/2);
    double root_energy=0;
    for(std::size_t j=0;j<n;j++) {
        a[j]={input[2*j]/scale,input[2*j+1]/scale};
        if(algorithm==2 && epsilon>0) root_energy+=energy(a[j]);
    }
    if constexpr(Count) if(algorithm==2 && epsilon>0) s.norm_value_volume+=n;
    const double angle=-2.0*std::acos(-1.0)/double(n);
    for(std::size_t j=0;j<n/2;j++) roots[j]={std::cos(angle*double(j)),std::sin(angle*double(j))};
    // Exactly representable special roots improve exact-zero recognition.
    if(n>=2) roots[0]={1,0};
    if(n>=4) roots[n/4]={0,-1};
    if constexpr(Count) s.root_pairs=n/2;
    // Normalize before restoring scale. Computing scale/sqrt(N) first can
    // underflow for subnormal inputs even when the true output is representable.
    const double inverse_sqrt_n=1.0/std::sqrt(double(n));
    if(algorithm==2) {
        if(epsilon>0) adaptive<Count,true>(a,roots,output,root_energy,epsilon,inverse_sqrt_n,scale,s);
        else adaptive<Count,false>(a,roots,output,root_energy,epsilon,inverse_sqrt_n,scale,s);
    } else {
        if(algorithm==0) dit<Count>(a,roots,s);else dif<Count>(a,roots,s);
        for(std::size_t j=0;j<n;j++) {
            output[2*j]=(a[j].r*inverse_sqrt_n)*scale;
            output[2*j+1]=(a[j].i*inverse_sqrt_n)*scale;
        }
        if constexpr(Count) {s.full_output_writes=n;s.computed_outputs=n;}
    }
    for(std::size_t j=0;j<2*n;j++) if(!std::isfinite(output[j])) return 3;
    return 0;
}

extern "C" int native_fft(const double* input,double* output,std::size_t n,
                          int algorithm,double epsilon,Stats* stats) {
    Stats local;
    int status=stats ? transform<true>(input,output,n,algorithm,epsilon,local)
                     : transform<false>(input,output,n,algorithm,epsilon,local);
    if(stats) *stats=local;
    return status;
}

extern "C" double consume(const double* data,std::size_t n) {
    // Every component is read. The checksum does not overflow on large values.
    double scale=0;
    for(std::size_t j=0;j<2*n;j++) scale=std::max(scale,std::abs(data[j]));
    if(scale==0) return 0;
    double sum=0;
    for(std::size_t j=0;j<2*n;j++) sum+=(data[j]/scale)*double(1+j%13);
    return sum;
}
