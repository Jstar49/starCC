#include<stdio.h>
extern int foo(int a,int b);
int main(){
    int a = 5;
    int b = 10;
    int c = foo(a,b);
    printf("c = %d\n",c); 
    return 0;
}