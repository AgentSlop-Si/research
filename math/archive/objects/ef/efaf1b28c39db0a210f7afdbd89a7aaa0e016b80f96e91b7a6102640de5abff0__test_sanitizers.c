/* Optional local memory/undefined-behavior check.
 * gcc -O1 -g -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer \
 *     test_sanitizers.c -lm -o test_sanitizers && ./test_sanitizers
 */
#include "leaf_fft.c"
#include <stdio.h>
int main(void) {
    cx *tables[3]={fft_table_create(4),fft_table_create(8),fft_table_create(16)};
    for(int i=0;i<3;++i) if(!tables[i]) return 2;
    double worst=0;
    for(size_t n=16;n<=1048576;n*=2) {
        plan *p=fft_plan_create(n);
        uint8_t *x=malloc(n);cx *reference=malloc(n*sizeof(cx)),*y=malloc(n*sizeof(cx));
        if(!p||!x||!reference||!y) return 2;
        uint32_t state=123456789;
        for(size_t j=0;j<n;++j) {state^=state<<13;state^=state>>17;state^=state<<5;x[j]=(uint8_t)(state&1);}
        fft_radix2(p,x,reference);
        for(int method=0;method<7;++method) {
            fft_execute(method,p,x,y,method>=4?tables[method-4]:NULL);
            for(size_t j=0;j<n;++j) {
                double err=hypot(y[j].r-reference[j].r,y[j].i-reference[j].i);
                if(err>worst) worst=err;
                if(err>1e-9) {fprintf(stderr,"Mismatch N=%zu method=%d bin=%zu error=%g\n",n,method,j,err);return 1;}
            }
        }
        free(x);free(reference);free(y);fft_plan_destroy(p);
    }
    for(int i=0;i<3;++i)fft_table_destroy(tables[i]);
    printf("Address/undefined-behavior sanitizer check passed; max method difference %.12g\n",worst);
    return 0;
}
