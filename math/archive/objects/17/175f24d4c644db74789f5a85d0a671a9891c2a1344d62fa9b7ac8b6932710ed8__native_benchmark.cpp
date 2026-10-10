// Native C++20/FFTW validation and benchmark for the v9 unit-step chirp row.
// FFTW declarations are repeated locally because the runtime library is present
// in the execution environment while its development header is not.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <complex>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

extern "C" {
typedef double fftw_complex[2];
typedef struct fftw_plan_s *fftw_plan;
void *fftw_malloc(size_t n);
void fftw_free(void *p);
fftw_plan fftw_plan_dft_1d(int n, fftw_complex *in, fftw_complex *out,
                           int sign, unsigned flags);
void fftw_execute(const fftw_plan p);
void fftw_destroy_plan(fftw_plan p);
}

using cd = std::complex<double>;
using Clock = std::chrono::steady_clock;
constexpr int FFTW_FORWARD_LOCAL = -1;
constexpr unsigned FFTW_ESTIMATE_LOCAL = 1u << 6;
constexpr double PI = 3.141592653589793238462643383279502884;

static uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t mod) {
    return static_cast<uint64_t>((static_cast<unsigned __int128>(a) * b) % mod);
}

static uint64_t tri_mod(uint64_t x, uint64_t mod) {
    unsigned __int128 a = x;
    unsigned __int128 b = x - 1;
    if ((x & 1u) == 0) a >>= 1; else b >>= 1;
    return static_cast<uint64_t>((a * b) % mod);
}

static size_t next_pow2(size_t x) {
    size_t r = 1;
    while (r < x) r <<= 1;
    return r;
}

struct FFTPlan {
    int n;
    fftw_complex *in;
    fftw_complex *out;
    fftw_plan plan;
    explicit FFTPlan(int n_) : n(n_) {
        in = static_cast<fftw_complex*>(fftw_malloc(sizeof(fftw_complex) * n));
        out = static_cast<fftw_complex*>(fftw_malloc(sizeof(fftw_complex) * n));
        if (!in || !out) throw std::bad_alloc();
        plan = fftw_plan_dft_1d(n, in, out, FFTW_FORWARD_LOCAL, FFTW_ESTIMATE_LOCAL);
        if (!plan) throw std::runtime_error("FFTW plan creation failed");
    }
    ~FFTPlan() {
        if (plan) fftw_destroy_plan(plan);
        if (in) fftw_free(in);
        if (out) fftw_free(out);
    }
    std::vector<cd> execute(const std::vector<cd>& x) {
        if (static_cast<int>(x.size()) != n) throw std::invalid_argument("FFT size mismatch");
        for (int i = 0; i < n; ++i) { in[i][0] = x[i].real(); in[i][1] = x[i].imag(); }
        fftw_execute(plan);
        std::vector<cd> y(n);
        for (int i = 0; i < n; ++i) y[i] = cd(out[i][0], out[i][1]);
        return y;
    }
};

struct State { uint64_t a, beta; };

struct Engine {
    size_t N, M, K;
    std::vector<cd> root;
    FFTPlan fftK;
    std::vector<cd> d, D, terms, gauge, scan, row, projected;
    std::vector<size_t> idx;

    Engine(size_t n, size_t m)
        : N(n), M(m), K(n/m), root(n), fftK(static_cast<int>(K)),
          d(K), D(K), terms(N), gauge(N), scan(N), row(N), projected(N), idx(N) {
        if ((N & (N-1)) || (M & (M-1)) || N % M || K < M)
            throw std::invalid_argument("N,M must be dyadic, M|N, K>=M");
        for (size_t q = 0; q < N; ++q) {
            double angle = 2.0 * PI * static_cast<double>(q) / static_cast<double>(N);
            root[q] = cd(std::cos(angle), std::sin(angle));
        }
    }

    cd rpos(uint64_t q) const { return root[q % N]; }
    cd rneg(uint64_t q) const { return std::conj(root[q % N]); }

    void compress(const std::vector<cd>& x, State s) {
        for (size_t r = 0; r < K; ++r) {
            uint64_t c = (mul_mod(mul_mod(s.a, M, N), r, N) + s.beta) % N;
            cd acc(0,0);
            for (size_t t = 0; t < M; ++t) {
                uint64_t ph = (mul_mod(s.a, tri_mod(t, N), N) + mul_mod(c, t, N)) % N;
                acc += rpos(ph) * x[r*M+t];
            }
            d[r] = acc;
        }
    }


    cd blelloch_scan() {
        scan = terms;
        for (size_t stride = 2; stride <= N; stride <<= 1) {
            for (size_t right = stride - 1; right < N; right += stride) {
                scan[right] += scan[right - stride/2];
            }
        }
        const cd total = scan[N-1];
        scan[N-1] = cd(0,0);
        for (size_t stride = N; stride >= 2; stride >>= 1) {
            for (size_t right = stride - 1; right < N; right += stride) {
                size_t left = right - stride/2;
                cd tmp = scan[left];
                scan[left] = scan[right];
                scan[right] += tmp;
            }
            if (stride == 2) break;
        }
        return total;
    }

    const std::vector<cd>& one_row(const std::vector<cd>& x, State s) {
        compress(x, s);
        D = fftK.execute(d);
        const uint64_t triM = tri_mod(M, N);
        for (size_t j = 0; j < N; ++j) {
            uint64_t mm = mul_mod(s.a, j, N);
            idx[j] = static_cast<size_t>(mm);
            uint64_t gph = (mul_mod(s.a, tri_mod(j, N), N) + mul_mod(s.beta, j, N)) % N;
            gauge[j] = rpos(gph);
            uint64_t bph = (mul_mod(M, (mm + s.beta) % N, N) + mul_mod(s.a, triM, N)) % N;
            cd boundary = rneg(bph);
            cd forcing = (D[mm % K] - boundary * D[(mm + mul_mod(s.a, M, K)) % K])
                         / std::sqrt(static_cast<double>(N));
            terms[j] = forcing * std::conj(gauge[j]);
        }
        // N is dyadic and a is odd, hence A_N=-1.  The cycle closure
        // determines the seed for free from the scan total: Y_0=sum(terms)/2.
        const cd y0 = blelloch_scan() / 2.0;
        for (size_t j = 0; j < N; ++j) row[idx[j]] = gauge[j] * (y0 - scan[j]);
        return row;
    }

    std::vector<cd> materialized_reference(const std::vector<cd>& x, State s, FFTPlan& fftN) {
        compress(x, s);
        for (size_t r = 0; r < K; ++r) {
            uint64_t c = (mul_mod(mul_mod(s.a, M, N), r, N) + s.beta) % N;
            for (size_t t = 0; t < M; ++t) {
                uint64_t ph = (mul_mod(s.a, tri_mod(t, N), N) + mul_mod(c, t, N)) % N;
                projected[r*M+t] = rneg(ph) * d[r];
            }
        }
        auto y = fftN.execute(projected);
        double inv = 1.0/std::sqrt(static_cast<double>(N));
        for (auto& z : y) z *= inv;
        return y;
    }
};

struct GridState {
    std::array<std::vector<int64_t>,3> candidate;
    std::array<std::vector<int32_t>,3> count;
    explicit GridState(size_t n) {
        for (int g=0; g<3; ++g) { candidate[g].assign(n,0); count[g].assign(n,0); }
    }
    void update(const std::vector<double>& values, double tau) {
        double W = 7.0*tau;
        double off[3] = {0.0, W/3.0, 2.0*W/3.0};
        for (int g=0; g<3; ++g) for (size_t i=0;i<values.size();++i) {
            int64_t id = static_cast<int64_t>(std::floor((values[i]-off[g])/W));
            if (count[g][i]==0) { candidate[g][i]=id; count[g][i]=1; }
            else if (candidate[g][i]==id) ++count[g][i];
            else --count[g][i];
        }
    }
    std::vector<double> finalize(double tau) const {
        double W=7.0*tau; double off[3]={0.0,W/3.0,2.0*W/3.0};
        size_t n=candidate[0].size(); std::vector<double> out(n);
        for(size_t i=0;i<n;++i){
            double c[3];
            for(int g=0;g<3;++g)c[g]=(static_cast<double>(candidate[g][i])+0.5)*W+off[g];
            std::sort(c,c+3); out[i]=c[1];
        }
        return out;
    }
};

static double max_error(const std::vector<cd>& a, const std::vector<cd>& b) {
    double e=0; for(size_t i=0;i<a.size();++i)e=std::max(e,std::abs(a[i]-b[i])); return e;
}

static double median_ms(std::vector<double> v) {
    std::sort(v.begin(),v.end()); return v[v.size()/2];
}

int main(int argc, char** argv) {
    size_t maxN = (argc>1)?std::stoull(argv[1]):262144;
    int rows = (argc>2)?std::stoi(argv[2]):5;
    std::mt19937_64 rng(20261009);
    std::normal_distribution<double> normal(0.0,1.0);
    std::cout << "N,M,row_ms,rows_stream_ms,fftw_ms,row_over_fftw,stream_over_fftw,identity_error,approx_error,theory_radius,error_over_radius\n";
    for(size_t N=4096; N<=maxN; N<<=1){
        size_t M=next_pow2(static_cast<size_t>(std::ceil(std::log2(static_cast<double>(N)))));
        if (M<4) M=4;
        while ((N/M)<M) M>>=1;
        Engine eng(N,M); FFTPlan fftN(static_cast<int>(N));
        std::vector<cd> x(N); for(auto& z:x)z=cd(normal(rng),normal(rng));
        State state{static_cast<uint64_t>((rng()%(N/2))*2+1), static_cast<uint64_t>(rng()%N)};
        auto refrow=eng.materialized_reference(x,state,fftN);
        auto gotrow=eng.one_row(x,state);
        double iderr=max_error(refrow,gotrow);

        // Baseline exact unitary FFT.
        std::vector<double> baseTimes, rowTimes, streamTimes;
        std::vector<cd> exact;
        for(int rep=0;rep<5;++rep){
            auto t0=Clock::now(); auto y=fftN.execute(x); double inv=1.0/std::sqrt((double)N); for(auto&z:y)z*=inv;
            auto t1=Clock::now(); baseTimes.push_back(std::chrono::duration<double,std::milli>(t1-t0).count()); exact=std::move(y);
            t0=Clock::now(); eng.one_row(x,state); t1=Clock::now(); rowTimes.push_back(std::chrono::duration<double,std::milli>(t1-t0).count());
        }

        double norm=0; for(auto z:x)norm+=std::norm(z); norm=std::sqrt(norm);
        double g=4.0, tau=g*std::sqrt((double)M/(double)N)*norm;
        GridState gr(N),gi(N); std::vector<cd> estimate;
        for(int rep=0;rep<3;++rep){
            gr=GridState(N); gi=GridState(N);
            auto t0=Clock::now();
            for(int rr=0;rr<rows;++rr){
                State st{static_cast<uint64_t>((rng()%(N/2))*2+1), static_cast<uint64_t>(rng()%N)};
                const auto& y=eng.one_row(x,st); std::vector<double> re(N),im(N);
                for(size_t i=0;i<N;++i){re[i]=y[i].real();im[i]=y[i].imag();}
                gr.update(re,tau);gi.update(im,tau);
            }
            auto re=gr.finalize(tau), im=gi.finalize(tau); estimate.resize(N);
            for(size_t i=0;i<N;++i)estimate[i]=cd(re[i],im[i]);
            auto t1=Clock::now();streamTimes.push_back(std::chrono::duration<double,std::milli>(t1-t0).count());
        }
        double b=median_ms(baseTimes), r=median_ms(rowTimes), s=median_ms(streamTimes);
        double approx=max_error(estimate,exact);
        double radius=(5.0/std::sqrt(2.0))*g*std::sqrt((double)M/(double)N)*norm;
        std::cout<<N<<","<<M<<","<<r<<","<<s<<","<<b<<","<<r/b<<","<<s/b<<","<<iderr<<","<<approx<<","<<radius<<","<<approx/radius<<"\n";
    }
}
