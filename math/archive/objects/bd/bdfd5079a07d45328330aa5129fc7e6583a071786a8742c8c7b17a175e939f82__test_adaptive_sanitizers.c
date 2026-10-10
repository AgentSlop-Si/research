/* gcc -O1 -g -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer \
 * test_adaptive_sanitizers.c -lm -o test_adaptive_sanitizers
 * ASAN_OPTIONS=detect_leaks=0 ./test_adaptive_sanitizers
 * LeakSanitizer cannot run under the execution sandbox's tracing. */
#include "adaptive_fft.c"
#include <stdio.h>
int main(void) {
    double worst=0;
    for(size_t n=16;n<=1048576;n*=2) {
        adaptive_plan *p=fft_adaptive_create(n);if(!p)return 2;
        uint8_t *x=malloc(n);cx *reference=malloc(n*sizeof(cx)),*y=malloc(n*sizeof(cx));
        if(!x||!reference||!y)return 2;
        uint32_t state=71236789;
        for(size_t j=0;j<n;++j){state^=state<<13;state^=state>>17;state^=state<<5;x[j]=state&1;}
        fft_radix2(p->base,x,reference);
        for(int method=0;method<6;++method) {
            if(fft_adaptive_select(p,method)||fft_adaptive_execute(p,x,y))return 1;
            for(size_t j=0;j<n;++j) {
                double error=hypot(y[j].r-reference[j].r,y[j].i-reference[j].i);
                if(error>worst)worst=error;if(error>1e-9)return 1;
            }
        }
        x[n-1]=255;y[0]=(cx){123,456};
        if(fft_adaptive_execute(p,x,y)!=-2 || y[0].r!=123 || y[0].i!=456)return 1;
        if(fft_adaptive_select(p,6)!=-1)return 1;
        fft_adaptive_destroy(p);free(x);free(y);free(reference);
    }
    printf("Adaptive API ASan/UBSan passed; maximum method error %.12g. Leak detection disabled for sandbox compatibility.\n",worst);
    return 0;
}
