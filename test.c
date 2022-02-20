
int jiet(int b){
	int a = 7;
	int i,j,s;
	s = 0;
	for (i=0;i<5;i+=1){
		s += i;
		j=5;
		while (j>0){
			s += j;
			j -= 1;
		}
	}
	return s;
}
int jxx=5;
int foo(int a,int b){
	int i=0,s = 0,j=0;
	s = jiet(a);
	s += jxx;
	jxx += 10;
	s += jxx;
	return s;
}
