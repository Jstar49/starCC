
int jiet(int b){
	int a = 7;
	return a;
}

int foo(int a,int b){
	int i=0,s = 0;
	s = jiet(s);
	// s = i<=a;
	// for(i=0;i<3;i+=1){
	// 	s += i;
	// }
	// i=0;
	while (i<3){
		s += i;
		i = i+1;
	}
	return s;
}
