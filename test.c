int star = 0;
int foo(int a,int b){
	return a + star + b;
}

int func(int a,int b,int c){
	int sum = 5,j,i;
	sum = 4;
	foo(sum+b,a);
	sum += foo(sum,b);
	return sum;
}