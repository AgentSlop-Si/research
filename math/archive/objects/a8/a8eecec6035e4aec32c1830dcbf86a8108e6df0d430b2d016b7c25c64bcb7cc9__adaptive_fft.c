/* Adaptive binary FFT API. Build this source alone; it includes the common FFT
 * implementation so calibration and selected execution use identical kernels. */
#include "leaf_fft.c"

typedef void (*fft_kernel)(const plan *,const uint8_t *,cx *,const cx *);
typedef struct {
    plan *base;
    cx *table4, *table8;
    fft_kernel kernel;
    const cx *selected_table;
    int method;
} adaptive_plan;

static void run_radix2(const plan *p,const uint8_t *x,cx *y,const cx *t) {(void)t;fft_radix2(p,x,y);}
static void run_codelet4(const plan *p,const uint8_t *x,cx *y,const cx *t) {(void)t;fft_codelet4(p,x,y);}
static void run_codelet8(const plan *p,const uint8_t *x,cx *y,const cx *t) {(void)t;fft_codelet8(p,x,y);}
static void run_codelet16(const plan *p,const uint8_t *x,cx *y,const cx *t) {(void)t;fft_codelet16(p,x,y);}
static fft_kernel candidates[6]={run_radix2,run_codelet4,run_codelet8,run_codelet16,fft_lookup4,fft_lookup8};

/* OR reduction is vectorizable. Reject invalid input before touching output or
 * computing a lookup address. No casts that could turn arbitrary data into bits. */
static int binary_valid(const uint8_t *x,size_t n) {
    unsigned invalid=0;
    for(size_t j=0;j<n;++j) invalid|=x[j];
    return (invalid & ~1u)==0;
}

adaptive_plan *fft_adaptive_create(size_t n) {
    adaptive_plan *a=calloc(1,sizeof(*a));
    if(!a)return NULL;
    a->base=fft_plan_create(n);a->table4=fft_table_create(4);a->table8=fft_table_create(8);
    if(!a->base||!a->table4||!a->table8) {
        fft_plan_destroy(a->base);fft_table_destroy(a->table4);fft_table_destroy(a->table8);free(a);return NULL;
    }
    a->method=0;a->kernel=candidates[0];return a;
}
void fft_adaptive_destroy(adaptive_plan *a) {
    if(a) {fft_plan_destroy(a->base);fft_table_destroy(a->table4);fft_table_destroy(a->table8);free(a);}
}
int fft_adaptive_select(adaptive_plan *a,int method) {
    if(!a || method<0 || method>=6)return -1;
    a->method=method;a->kernel=candidates[method];
    a->selected_table=method==4?a->table4:(method==5?a->table8:NULL);
    return 0;
}
int fft_adaptive_execute(const adaptive_plan *a,const uint8_t *x,cx *y) {
    if(!a || !x || !y)return -1;
    if(!binary_valid(x,a->base->n))return -2;
    /* A single function-pointer dispatch, no per-node map or retuning. */
    a->kernel(a->base,x,y,a->selected_table);return 0;
}
int fft_adaptive_execute_candidate(const adaptive_plan *a,int method,const uint8_t *x,cx *y) {
    if(!a || !x || !y || method<0 || method>=6)return -1;
    if(!binary_valid(x,a->base->n))return -2;
    const cx *t=method==4?a->table4:(method==5?a->table8:NULL);
    candidates[method](a->base,x,y,t);return 0;
}
double fft_adaptive_bench_candidate(const adaptive_plan *a,int method,const uint8_t *pool,unsigned pool_count,cx *y,unsigned repeats) {
    if(!a || !pool_count || !repeats || method<0 || method>=6)return -1;
    fft_kernel kernel=candidates[method];
    const cx *t=method==4?a->table4:(method==5?a->table8:NULL);
    double start=seconds();
    for(unsigned r=0;r<repeats;++r) {
        const uint8_t *x=pool+(size_t)(r%pool_count)*a->base->n;
        if(!binary_valid(x,a->base->n))return -2;
        kernel(a->base,x,y,t);
    }
    return (seconds()-start)/(double)repeats;
}
double fft_adaptive_bench_selected(const adaptive_plan *a,const uint8_t *pool,unsigned pool_count,cx *y,unsigned repeats) {
    if(!a || !pool_count || !repeats)return -1;
    double start=seconds();
    for(unsigned r=0;r<repeats;++r) {
        if(fft_adaptive_execute(a,pool+(size_t)(r%pool_count)*a->base->n,y))return -2;
    }
    return (seconds()-start)/(double)repeats;
}
