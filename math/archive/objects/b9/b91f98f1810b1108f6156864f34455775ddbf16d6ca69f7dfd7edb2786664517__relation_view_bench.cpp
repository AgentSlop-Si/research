#include <algorithm>
#include <chrono>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>

using cd = std::complex<double>;
using Clock = std::chrono::steady_clock;

struct Event {
    bool coeff;
    int key;
    cd delta;
};

static double ms_since(Clock::time_point t0) {
    return std::chrono::duration<double,std::milli>(Clock::now()-t0).count();
}

static cd randc(std::mt19937_64 &g, double scale=1.0) {
    std::normal_distribution<double> d(0.0, scale);
    return {d(g),d(g)};
}

struct Problem {
    int n, r, q, p, updates;
    std::vector<cd> basis;      // r*n
    std::vector<cd> coeff0;     // r
    std::vector<int> bins;      // q
    std::vector<int> positions; // p
    std::vector<cd> phase_q;    // p*q
    std::vector<cd> phase_full; // p*n
    std::vector<Event> events;
};

static Problem make_problem(int n=8192,int r=256,int q=64,int p=32,int updates=4096) {
    Problem z{n,r,q,p,updates};
    std::mt19937_64 g(0xA71D4F22ULL);
    z.basis.resize((size_t)r*n);
    for (auto &v:z.basis) v=randc(g);
    z.coeff0.resize(r); for(auto &v:z.coeff0) v=randc(g);
    std::vector<int> pool(n); std::iota(pool.begin(),pool.end(),0); std::shuffle(pool.begin(),pool.end(),g);
    z.bins.assign(pool.begin(),pool.begin()+q);
    std::sort(z.bins.begin(),z.bins.end());
    std::shuffle(pool.begin(),pool.end(),g);
    z.positions.assign(pool.begin(),pool.begin()+p);
    std::sort(z.positions.begin(),z.positions.end());

    const double tau=-2.0*std::acos(-1.0)/n;
    z.phase_q.resize((size_t)p*q);
    z.phase_full.resize((size_t)p*n);
    for(int a=0;a<p;a++) {
        int pos=z.positions[a];
        for(int b=0;b<q;b++) z.phase_q[(size_t)a*q+b]=std::exp(cd(0,tau*pos*z.bins[b]));
        for(int k=0;k<n;k++) z.phase_full[(size_t)a*n+k]=std::exp(cd(0,tau*pos*k));
    }
    std::uniform_real_distribution<double> u(0.0,1.0);
    std::uniform_int_distribution<int> ci(0,r-1), pi(0,p-1);
    z.events.reserve(updates);
    for(int t=0;t<updates;t++) {
        bool coeff=u(g)<0.72;
        z.events.push_back({coeff, coeff?ci(g):pi(g), randc(g,0.02)});
    }
    return z;
}

static std::vector<cd> initial_partial(const Problem& z) {
    std::vector<cd> y(z.q,cd(0,0));
    for(int i=0;i<z.r;i++) {
        cd c=z.coeff0[i];
        const cd* row=&z.basis[(size_t)i*z.n];
        for(int b=0;b<z.q;b++) y[b]+=c*row[z.bins[b]];
    }
    return y;
}

static double run_replay(const Problem& z,int H, cd &checksum, std::vector<cd>* final_out=nullptr) {
    auto y=initial_partial(z);
    std::vector<cd> coeff=z.coeff0;
    std::vector<cd> residual(z.p,cd(0,0));
    std::vector<Event> pending; pending.reserve(H+8);
    checksum=0;
    auto t0=Clock::now();
    for(int t=0;t<z.updates;t++) {
        const auto &e=z.events[t];
        if(e.coeff) coeff[e.key]+=e.delta; else residual[e.key]+=e.delta;
        pending.push_back(e);
        if((t+1)%H==0) {
            for(const auto &a:pending) {
                if(a.coeff) {
                    const cd* row=&z.basis[(size_t)a.key*z.n];
                    for(int b=0;b<z.q;b++) y[b]+=a.delta*row[z.bins[b]];
                } else {
                    const cd* ph=&z.phase_q[(size_t)a.key*z.q];
                    for(int b=0;b<z.q;b++) y[b]+=a.delta*ph[b];
                }
            }
            pending.clear();
            checksum += y[0];
        }
    }
    if(final_out) *final_out=y;
    return ms_since(t0);
}

static double run_rebuild(const Problem& z,int H, cd &checksum, std::vector<cd>* final_out=nullptr) {
    std::vector<cd> coeff=z.coeff0;
    std::vector<cd> residual(z.p,cd(0,0));
    std::vector<cd> y(z.q);
    checksum=0;
    auto t0=Clock::now();
    for(int t=0;t<z.updates;t++) {
        const auto &e=z.events[t];
        if(e.coeff) coeff[e.key]+=e.delta; else residual[e.key]+=e.delta;
        if((t+1)%H==0) {
            std::fill(y.begin(),y.end(),cd(0,0));
            for(int i=0;i<z.r;i++) {
                cd c=coeff[i];
                const cd* row=&z.basis[(size_t)i*z.n];
                for(int b=0;b<z.q;b++) y[b]+=c*row[z.bins[b]];
            }
            for(int a=0;a<z.p;a++) if(residual[a]!=cd(0,0)) {
                cd d=residual[a]; const cd* ph=&z.phase_q[(size_t)a*z.q];
                for(int b=0;b<z.q;b++) y[b]+=d*ph[b];
            }
            checksum += y[0];
        }
    }
    if(final_out) *final_out=y;
    return ms_since(t0);
}

static double run_eager(const Problem& z,int H, cd &checksum) {
    std::vector<cd> dense(z.n,cd(0,0));
    for(int i=0;i<z.r;i++) {
        cd c=z.coeff0[i]; const cd* row=&z.basis[(size_t)i*z.n];
        for(int k=0;k<z.n;k++) dense[k]+=c*row[k];
    }
    checksum=0;
    auto t0=Clock::now();
    for(int t=0;t<z.updates;t++) {
        const auto &e=z.events[t];
        if(e.coeff) {
            const cd* row=&z.basis[(size_t)e.key*z.n];
            for(int k=0;k<z.n;k++) dense[k]+=e.delta*row[k];
        } else {
            const cd* ph=&z.phase_full[(size_t)e.key*z.n];
            for(int k=0;k<z.n;k++) dense[k]+=e.delta*ph[k];
        }
        if((t+1)%H==0) checksum += dense[z.bins[0]];
    }
    return ms_since(t0);
}

template<class F> static double median3(F fn) {
    std::vector<double> t(3); for(auto &v:t) v=fn();
    std::sort(t.begin(),t.end()); return t[1];
}

int main(){
    Problem z=make_problem();
    std::cout<<std::setprecision(10);
    std::cout<<"N="<<z.n<<" r="<<z.r<<" q="<<z.q<<" prepared_points="<<z.p<<" updates="<<z.updates<<"\n";
    std::cout<<"H,replay_ms,rebuild_ms,eager_ms,replay_vs_rebuild,replay_vs_eager,max_error\n";
    cd eager_checksum; double eager_common=median3([&]{return run_eager(z,64,eager_checksum);});
    for(int H: {1,4,16,64,128,256,512,1024}) {
        cd ca,cb,cc; std::vector<cd> ya,yb;
        // correctness from one pass
        run_replay(z,H,ca,&ya); run_rebuild(z,H,cb,&yb);
        double err=0; for(int i=0;i<z.q;i++) err=std::max(err,std::abs(ya[i]-yb[i]));
        double tr=median3([&]{return run_replay(z,H,ca);});
        double tb=median3([&]{return run_rebuild(z,H,cb);});
        double te=eager_common;
        std::cout<<H<<","<<tr<<","<<tb<<","<<te<<","<<tb/tr<<","<<te/tr<<","<<err<<"\n";
    }
}
