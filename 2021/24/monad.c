#include "stdio.h"

int monad(int *d) {
  int v4 = (((((d[0] * 26) + d[1]) * 26) + d[2]) + 5628);
  int v9 = ((((v4 % 26) + -8) == d[3]) == 0);
  int v21 = (((((((v4 / 26) * ((25 * v9) + 1)) + ((d[3] + 10) * v9)) * 26) + (d[4] + 2)) * 26) + (d[5] + 8));
  int v26 = ((((v21 % 26) + -11) == d[6]) == 0);
  int v35 = (((((v21 / 26) * ((25 * v26) + 1)) + ((d[6] + 4) * v26)) * 26) + (d[7] + 9));
  int v40 = ((((v35 % 26) + -3) == d[8]) == 0);
  int v49 = (((((v35 / 26) * ((25 * v40) + 1)) + ((d[8] + 10) * v40)) * 26) + (d[9] + 3));
  int v54 = ((((v49 % 26) + -3) == d[10]) == 0);
  int v60 = (((v49 / 26) * ((25 * v54) + 1)) + ((d[10] + 7) * v54));
  int v65 = ((((v60 % 26) + -1) == d[11]) == 0);
  int v71 = (((v60 / 26) * ((25 * v65) + 1)) + ((d[11] + 7) * v65));
  int v76 = ((((v71 % 26) + -10) == d[12]) == 0);
  int v82 = (((v71 / 26) * ((25 * v76) + 1)) + ((d[12] + 2) * v76));
  int v87 = ((((v82 % 26) + -16) == d[13]) == 0);
  return (((v82 / 26) * ((25 * v87) + 1)) + ((d[13] + 2) * v87));
}

int main() {
    int vals[14];
    for (int i = 0; i < 14; ++i) {
        vals[i] = 9;
    }
    
    int ii = 0;
    int evaled = 0;
    int finished = 0;
    while (!finished) {
        ii += 1;
        
        evaled = monad(vals);
        if (!evaled) {
            printf("solution! ");
            for (int i = 0; i < 14; ++i) {
                printf("%d", vals[i]);
            }
            printf("\n");
            break;
        }
        if (!(ii%1000000)) {
            for (int i = 0; i < 14; ++i) {
                printf("%d", vals[i]);
            }
            printf(" --> %d\n", evaled);
        }
        for (int i = 14-1; i >= 0; --i) {
            vals[i] -= 1;
            if (vals[i] == 0) {
                if (i == 0) {
                    finished = 1;
                }
                vals[i] = 9;
            } else {
                break;
            }
        }
    }
    return 0;
}
