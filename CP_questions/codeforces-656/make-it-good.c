#include <stdio.h>
#include <unistd.h>
#define bool _Bool
#define true 1
#define false 0

bool still_good(int * array, int len, int len_curr){
    int counter = 1, last = 0;
    int comp = array[len - len_curr];
    for (int i = len - 1; i > len - len_curr; i--) {
        if (array[i] < last) {
            return false;
        }else{
            last = array[i];
        }

    }
    return true;
}
/* still_good(array, len_curr, len)
[1 2 3 4]
len = 4
len_curr = 4
counter = 1
last = 0
comp = 1

i = 3
last = 4
3 < 4 ?
*/
/*
[1 2 3 4]
len = 4
len_curr = 4
ret (int) ! still_good(array, len_curr, len)
*/

int how_good(int * array, int len , int len_curr) {
    if (len_curr == len) {
        if (array[0] <= array[1]){
            return 0;
        }else{
            return (int) !still_good(array,len_curr,len);
        }
    }
    if (len_curr == 1 || array[len - len_curr] <= array[len - len_curr + 1] || still_good(array,len,len_curr)){
        return how_good(array, len, len_curr + 1);
    }

    return len - len_curr + 1;
}



int main(int argc, char const *argv[]) {
    int ncases, size;
    scanf("%d",&ncases);
    int array[200000];
    for (size_t i = 0; i < ncases; i++) {
        scanf("%d",&size);
        for (size_t j = 0; j < size; j++) {
            scanf("%d", &array[j]);
        }
        printf("%d\n",how_good(array,size,1));
    }
    return 0;
}
