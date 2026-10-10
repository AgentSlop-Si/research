// Phase 10: AOT generic double-variable impulse-update evaluator.
// Compiled OFFLINE before importing Python; no JIT, no Python embedded.
// All arrays float64; circular convolution coefficient indexing.
#include <cstdint>
#include <vector>
#include <cmath>
#include <cstddef>

namespace {
inline int64_t mod_shift(int64_t a, int64_t b, int64_t n) {
    // a,b originate from bounded nonnegative indices & degrees. Signed safe for
    // practical array lengths; use __int128 for intermediate products.
    __int128 z=static_cast<__int128>(a)+static_cast<__int128>(b);
    int64_t r=static_cast<int64_t>(z % n);
    return r<0?r+n:r;
}
inline double pow_int(double x, int32_t d) {
    double v=1.;
    for(int32_t i=0;i<d;++i) v*=x;
    return v;
}
}
extern "C" {
int fft10_eval(
    int64_t n, const double* base, const double* dense,
    int64_t dense_count, const int32_t* d_a, const int32_t* d_b,
    int64_t sparse_count, const int32_t* s_a, const int32_t* s_b,
    const int64_t* sparse_positions, const double* sparse_weights,
    int64_t position_a, double delta_a, int64_t position_b, double delta_b,
    const int64_t* indices, int64_t output_count, double* output
) {
    if(n<2 || output_count<0 || dense_count<0 || sparse_count<0 || !base || !output
       || position_a<0 || position_a>=n || position_b<0 || position_b>=n
       || !std::isfinite(delta_a) || !std::isfinite(delta_b)) return 1;
    if(dense_count && (!dense || !d_a || !d_b)) return 2;
    if(sparse_count && (!s_a || !s_b || !sparse_positions || !sparse_weights)) return 3;
    if(indices && output_count<0) return 4;
    if(!indices && output_count!=n) return 5;
    std::vector<int64_t> shifts(static_cast<size_t>(dense_count));
    std::vector<double> scales(static_cast<size_t>(dense_count));
    for(int64_t h=0;h<dense_count;++h) {
        if(d_a[h]<0 || d_b[h]<0) return 6;
        __int128 z = static_cast<__int128>(d_a[h])*position_a + static_cast<__int128>(d_b[h])*position_b;
        shifts[h]=static_cast<int64_t>(z%n);
        scales[h]=pow_int(delta_a,d_a[h])*pow_int(delta_b,d_b[h]);
    }
    for(int64_t r=0;r<output_count;++r) {
        const int64_t q=indices ? indices[r] : r;
        if(q<0 || q>=n) return 7;
        double v=base[q];
        for(int64_t h=0;h<dense_count;++h) {
            const int64_t s=shifts[h];
            int64_t j=q-s; if(j<0)j+=n;
            v += scales[h]*dense[h*n+j];
        }
        output[r]=v;
    }
    for(int64_t h=0;h<sparse_count;++h) {
        if(s_a[h]<0 || s_b[h]<0) return 8;
        __int128 z=static_cast<__int128>(sparse_positions[h])+
             static_cast<__int128>(s_a[h])*position_a+
             static_cast<__int128>(s_b[h])*position_b;
        int64_t q=static_cast<int64_t>(z%n); if(q<0)q+=n;
        double inc=sparse_weights[h]*pow_int(delta_a,s_a[h])*pow_int(delta_b,s_b[h]);
        if(!indices)output[q]+=inc;
        else for(int64_t r=0;r<output_count;++r)if(indices[r]==q)output[r]+=inc;
    }
    return 0;
}
}

// Independent manually specialized comparator ONLY for the expression
// F(A,B,C,D)=A*A*B + A*B + B*B + C*D.
// Kernel order: K01,K10,K11,K20; coefficient impulses K02=K21=e0.
extern "C" int fft10_hand_example(
    int64_t n,const double *base,const double *k01,const double *k10,
    const double *k11,const double *k20,
    int64_t pa,double alpha,int64_t pb,double beta,double *out
) {
    if(n<2||!base||!k01||!k10||!k11||!k20||!out||
       pa<0||pa>=n||pb<0||pb>=n)return 1;
    const int64_t s01=pb;
    const int64_t s10=pa;
    const int64_t s11=static_cast<int64_t>((static_cast<__int128>(pa)+pb)%n);
    const int64_t s20=static_cast<int64_t>((static_cast<__int128>(2)*pa)%n);
    const double ab=alpha*beta;
    const double aa=alpha*alpha;
    for(int64_t q=0;q<n;++q) {
        int64_t i01=q-s01;if(i01<0)i01+=n;
        int64_t i10=q-s10;if(i10<0)i10+=n;
        int64_t i11=q-s11;if(i11<0)i11+=n;
        int64_t i20=q-s20;if(i20<0)i20+=n;
        out[q]=base[q]+beta*k01[i01]+alpha*k10[i10]
               +ab*k11[i11]+aa*k20[i20];
    }
    out[static_cast<int64_t>((static_cast<__int128>(2)*pb)%n)]+=beta*beta;
    out[static_cast<int64_t>((static_cast<__int128>(2)*pa+pb)%n)]+=aa*beta;
    return 0;
}
