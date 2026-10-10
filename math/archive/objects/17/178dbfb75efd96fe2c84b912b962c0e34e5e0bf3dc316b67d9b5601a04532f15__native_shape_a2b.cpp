// Auto-generated OFFLINE from validated degree lists; no input values are embedded.
#include <cstdint>
#include <cmath>
extern "C" int fft10_shape_eval(
  int64_t n, const double* base, const double* dense,
  const int64_t* sparse_positions, const double* sparse_weights,
  int64_t pa, double alpha, int64_t pb, double beta,
  const int64_t* indices, int64_t q_count, double* out) {
  if(n<2 || q_count<0 || !base || !out || pa<0 || pa>=n || pb<0 || pb>=n)
    return 1;
  if(!std::isfinite(alpha) || !std::isfinite(beta)) return 2;
  if(!indices && q_count!=n) return 3;
  if(!dense) return 4;
  if(!sparse_positions || !sparse_weights) return 5;
  const int64_t shift0=static_cast<int64_t>((static_cast<__int128>(0)*pa+static_cast<__int128>(1)*pb)%n);
  const double scale0=beta;
  const int64_t shift1=static_cast<int64_t>((static_cast<__int128>(1)*pa+static_cast<__int128>(0)*pb)%n);
  const double scale1=alpha;
  const int64_t shift2=static_cast<int64_t>((static_cast<__int128>(1)*pa+static_cast<__int128>(1)*pb)%n);
  const double scale2=alpha*beta;
  const int64_t shift3=static_cast<int64_t>((static_cast<__int128>(2)*pa+static_cast<__int128>(0)*pb)%n);
  const double scale3=alpha*alpha;
  for(int64_t r=0;r<q_count;++r) {
    const int64_t q=indices?indices[r]:r;
    if(q<0||q>=n)return 6;
    int64_t j0=q-shift0; if(j0<0)j0+=n;
    int64_t j1=q-shift1; if(j1<0)j1+=n;
    int64_t j2=q-shift2; if(j2<0)j2+=n;
    int64_t j3=q-shift3; if(j3<0)j3+=n;
    out[r]=base[q]+scale0*dense[0*n+j0]+scale1*dense[1*n+j1]+scale2*dense[2*n+j2]+scale3*dense[3*n+j3];
  }
  const int64_t sp0=static_cast<int64_t>((static_cast<__int128>(sparse_positions[0])+static_cast<__int128>(0)*pa+static_cast<__int128>(2)*pb)%n);
  const double sv0=sparse_weights[0]*(beta*beta);
  if(!indices)out[sp0]+=sv0;
  else for(int64_t r=0;r<q_count;++r)if(indices[r]==sp0)out[r]+=sv0;
  const int64_t sp1=static_cast<int64_t>((static_cast<__int128>(sparse_positions[1])+static_cast<__int128>(2)*pa+static_cast<__int128>(1)*pb)%n);
  const double sv1=sparse_weights[1]*(alpha*alpha*beta);
  if(!indices)out[sp1]+=sv1;
  else for(int64_t r=0;r<q_count;++r)if(indices[r]==sp1)out[r]+=sv1;
  return 0;
}
