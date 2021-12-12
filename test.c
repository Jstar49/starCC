//#include<stdio.h>

/* 你好 */
int a = 10,b=0,c;
//char ch='s';

int main(){
	int i,j;
	int sum=0;
	for(i=0;i<=100;i++){
		sum = sum + i;
	}
	printf("sum = %d\n",sum);
	if (sum >= 4950){
		printf("sum >= 4950\n");
	}
	return 0;
}
