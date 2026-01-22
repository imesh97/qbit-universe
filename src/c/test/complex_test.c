/* orig test */

#include <stdio.h>
#include <complex.h>

int main() {
    double complex a = 1.0 + (2.0 * I); // 1 + 2i
    double complex b = 1.0 - (2.0 * I); // 1 - 2i
    /*

    (1 + 2i)(1 - 2i)
    
    = 1*1 + 1*(-2i) + 2i*1 + 2i*(-2i)
    = 1 - 2i + 2i - 4i²
    = 1 - 4(-1)
    = 1 + 4 = 5

    */
    double complex result = a * b;
    
    printf("The result is %.1f + %.1fi\n", creal(result), cimag(result));
    return 0;
}