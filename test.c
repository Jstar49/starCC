
int jiet(int b){
	int a = 7;
	return a;
}

int foo(int a){
	int i,s = 0;
	s = jiet(s);
	for(i=0;i<=10;i+=1){
		s += i;
		if (i<=5){
			break;
		}
	}
	return s;
}
