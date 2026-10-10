/* Binary-input FFT microbenchmark. All public execution methods are single-threaded.
 * Build: gcc -O3 -march=native -DNDEBUG -fno-math-errno -ffp-contract=fast \
 *        -std=c11 -Wall -Wextra -fPIC -shared leaf_fft.c -lm -o libleaf_fft.so
 * Inputs are uint8_t values in {0,1}. Outputs are unnormalized complex128 DFTs.
 */
#define _POSIX_C_SOURCE 200809L
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct { double r, i; } cx;
typedef struct {
    size_t n;
    uint32_t *perm;
    cx *twiddle; /* stage m occupies [m/2, m), total n complex slots */
} plan;

static void *amalloc(size_t bytes) {
    void *p = NULL;
    if (posix_memalign(&p, 64, bytes) != 0) return NULL;
    return p;
}

plan *fft_plan_create(size_t n) {
    if (n < 16 || (n & (n-1)) || n > UINT32_MAX) return NULL;
    plan *p = calloc(1, sizeof(*p));
    if (!p) return NULL;
    p->n=n; p->perm=amalloc(n*sizeof(uint32_t)); p->twiddle=amalloc(n*sizeof(cx));
    if (!p->perm || !p->twiddle) { free(p->perm); free(p->twiddle); free(p); return NULL; }
    unsigned bits=0; for (size_t q=n;q>1;q>>=1) ++bits;
    for(size_t j=0;j<n;++j) {
        uint32_t v=(uint32_t)j, r=0;
        for(unsigned b=0;b<bits;++b) { r=(r<<1)|(v&1); v>>=1; }
        p->perm[j]=r;
    }
    const double tau=6.283185307179586476925286766559;
    for(size_t m=2;m<=n;m<<=1) {
        for(size_t j=0;j<m/2;++j) {
            double a=-tau*(double)j/(double)m;
            p->twiddle[m/2+j]=(cx){cos(a), sin(a)};
        }
    }
    return p;
}
void fft_plan_destroy(plan *p) { if(p) {free(p->perm);free(p->twiddle);free(p);} }

/* Same optimized iterative DIT merge code is used after every leaf type. */
static void merge_stages(const plan *p, cx *restrict y, size_t first_m) {
    const size_t n=p->n;
    if(first_m==4) {
        for(size_t b=0;b<n;b+=4) {
            cx a=y[b], c=y[b+2], d=y[b+1], e=y[b+3];
            y[b]=(cx){a.r+c.r,a.i+c.i}; y[b+2]=(cx){a.r-c.r,a.i-c.i};
            y[b+1]=(cx){d.r+e.i,d.i-e.r}; y[b+3]=(cx){d.r-e.i,d.i+e.r};
        }
        first_m=8;
    }
    for(size_t m=first_m;m<=n;m<<=1) {
        const size_t h=m/2;
        const cx *restrict w=p->twiddle+h;
        for(size_t b=0;b<n;b+=m) {
            cx *restrict a=y+b, *restrict z=y+b+h;
            for(size_t j=0;j<h;++j) {
                const double zr=z[j].r, zi=z[j].i;
                const double tr=zr*w[j].r-zi*w[j].i;
                const double ti=zr*w[j].i+zi*w[j].r;
                const double ar=a[j].r, ai=a[j].i;
                a[j]=(cx){ar+tr,ai+ti}; z[j]=(cx){ar-tr,ai-ti};
            }
        }
    }
}

/* Inputs below are in the bit-reversed order needed by iterative DIT. */
static inline void real4(double x0,double x1,double x2,double x3,cx *y) {
    double a=x0+x1,b=x0-x1,c=x2+x3,d=x2-x3;
    y[0]=(cx){a+c,0}; y[1]=(cx){b,-d};
    y[2]=(cx){a-c,0}; y[3]=(cx){b,d};
}
static inline void real8(const double *x,cx *y) {
    const double s=0.70710678118654752440084436210485;
    double a=x[0]+x[1],b=x[0]-x[1],c=x[2]+x[3],d=x[2]-x[3];
    double e=x[4]+x[5],f=x[4]-x[5],g=x[6]+x[7],h=x[6]-x[7];
    double er0=a+c,er2=a-c,or0=e+g,or2=e-g;
    double tr=s*(f-h),ti=-s*(f+h);
    y[0]=(cx){er0+or0,0}; y[4]=(cx){er0-or0,0};
    y[1]=(cx){b+tr,-d+ti}; y[5]=(cx){b-tr,-d-ti};
    y[2]=(cx){er2,-or2}; y[6]=(cx){er2,or2};
    y[3]=(cx){b-tr,d+ti}; y[7]=(cx){b+tr,d-ti};
}
static inline void real16(const double *x,cx *y) {
    cx e[8], o[8]; real8(x,e); real8(x+8,o);
    static const double wr[8]={1,0.92387953251128675613,0.70710678118654752440,0.38268343236508977173,0,-0.38268343236508977173,-0.70710678118654752440,-0.92387953251128675613};
    static const double wi[8]={0,-0.38268343236508977173,-0.70710678118654752440,-0.92387953251128675613,-1,-0.92387953251128675613,-0.70710678118654752440,-0.38268343236508977173};
    for(unsigned j=0;j<8;++j) {
        double tr=o[j].r*wr[j]-o[j].i*wi[j],ti=o[j].r*wi[j]+o[j].i*wr[j];
        y[j]=(cx){e[j].r+tr,e[j].i+ti}; y[j+8]=(cx){e[j].r-tr,e[j].i-ti};
    }
}

/* Baseline already fuses the input permutation with arithmetic length-2 leaves. */
void fft_radix2(const plan *p,const uint8_t *restrict x,cx *restrict y) {
    for(size_t b=0;b<p->n;b+=2) {
        double a=x[p->perm[b]],c=x[p->perm[b+1]];
        y[b]=(cx){a+c,0}; y[b+1]=(cx){a-c,0};
    }
    merge_stages(p,y,4);
}
void fft_codelet4(const plan *p,const uint8_t *restrict x,cx *restrict y) {
    for(size_t b=0;b<p->n;b+=4)
        real4(x[p->perm[b]],x[p->perm[b+1]],x[p->perm[b+2]],x[p->perm[b+3]],y+b);
    merge_stages(p,y,8);
}
void fft_codelet8(const plan *p,const uint8_t *restrict x,cx *restrict y) {
    for(size_t b=0;b<p->n;b+=8) {
        double v[8]; for(unsigned j=0;j<8;++j) v[j]=x[p->perm[b+j]];
        real8(v,y+b);
    }
    merge_stages(p,y,16);
}
void fft_codelet16(const plan *p,const uint8_t *restrict x,cx *restrict y) {
    for(size_t b=0;b<p->n;b+=16) {
        double v[16]; for(unsigned j=0;j<16;++j) v[j]=x[p->perm[b+j]];
        real16(v,y+b);
    }
    merge_stages(p,y,32);
}

/* Each row stores a complete complex-double spectrum. Key bit j is leaf slot j
 * in global bit-reversed input layout. This is deliberately NOT contiguous
 * natural input order; the permutation preserves the radix-2 decimation. */
void *fft_table_create(unsigned leaf) {
    if(leaf!=4 && leaf!=8 && leaf!=16) return NULL;
    size_t rows=(size_t)1<<leaf;
    cx *t=amalloc(rows*leaf*sizeof(cx));
    if(!t) return NULL;
    for(size_t k=0;k<rows;++k) {
        double x[16]; for(unsigned j=0;j<leaf;++j) x[j]=(double)((k>>j)&1);
        if(leaf==4) real4(x[0],x[1],x[2],x[3],t+k*leaf);
        else if(leaf==8) real8(x,t+k*leaf);
        else real16(x,t+k*leaf);
    }
    return t;
}
void fft_table_destroy(void *t) {free(t);}

#define DEFINE_LOOKUP(L) \
void fft_lookup##L(const plan *p,const uint8_t *restrict x,cx *restrict y,const cx *restrict t) { \
    for(size_t b=0;b<p->n;b+=L) { \
        unsigned key=0; \
        for(unsigned j=0;j<L;++j) key |= (unsigned)x[p->perm[b+j]]<<j; \
        memcpy(y+b,t+(size_t)key*L,L*sizeof(cx)); \
    } \
    merge_stages(p,y,2*L); \
}
DEFINE_LOOKUP(4)
DEFINE_LOOKUP(8)
DEFINE_LOOKUP(16)

/* Dispatch is outside per-transform loops. Timed batches include key packing,
 * permutation/gathers, output copies, all merge stages, and C function calls.
 * They exclude plan/table creation, input generation, and buffer allocation. */
void fft_execute(int method,const plan *p,const uint8_t *x,cx *y,const cx *t) {
    switch(method) {
      case 0: fft_radix2(p,x,y); break;
      case 1: fft_codelet4(p,x,y); break;
      case 2: fft_codelet8(p,x,y); break;
      case 3: fft_codelet16(p,x,y); break;
      case 4: fft_lookup4(p,x,y,t); break;
      case 5: fft_lookup8(p,x,y,t); break;
      case 6: fft_lookup16(p,x,y,t); break;
    }
}
static double seconds(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return (double)t.tv_sec+1e-9*(double)t.tv_nsec;
}
double fft_bench(int method,const plan *p,const uint8_t *pool,unsigned pool_count,cx *y,const cx *t,unsigned repeats) {
    double start=seconds();
    for(unsigned r=0;r<repeats;++r)
        fft_execute(method,p,pool+(size_t)(r%pool_count)*p->n,y,t);
    return (seconds()-start)/(double)repeats;
}
/* Microbenchmark gather+compute/copy only, optional diagnostic after full FFT. */
