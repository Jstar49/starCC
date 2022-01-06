
int func(int a,int b,int c){
	int sum = 5;
	sum = sum + a;
	sum = sum -b*4+3;
	while(sum >8){
		sum = sum -1;
		if(sum == 10){
			break;
		}
	}
	return sum+2;
}