#include<stdio.h>
extern int foo(int a,int b);
extern int jxx;
int main(){
    int a = 5;
    int b = 10;
    int c = foo(a,b);
    printf("c = %d\n",c); 
    printf("jxx = %d\n",jxx);
    return 0;
}