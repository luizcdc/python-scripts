#include <stdio.h>
#define min(a,b) (a < b ? a : b)

int cost_to_all(char c, char * string,  int size){
  int count = 0;
  for (size_t i = 0; i < size; i++)
    if (string[i] != c)
      count++;

  return count;
}

int cgood(char c, char * string, int size){
  if (size == 1)
    return (int)(string[0] != c);
  return min(cgood((char)(((int)c)+1),string+size/2,size/2) + cost_to_all(c,string,size/2),
             cgood((char)(((int)c)+1),string,size/2) + cost_to_all(c,string+size/2,size/2));
}

int main(int argc, char const *argv[]) {
  int ncases, size;
  scanf("%d",&ncases);
  int ;

  for (size_t i = 0; i < ncases; i++) {
    scanf("%d",&size);
    scanf("%s\n",string);
    printf("%d\n",cgood('a',string,size));
  }
  return 0;
}
