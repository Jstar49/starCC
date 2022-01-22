foo:
	addi	sp,sp,-24
	sw	s0,20(sp)
	addi	s0,sp,24
	sw	a0,-24(s0)		 #a
	sw	a1,-20(s0)		 #b
	li	a2,5
	sw	a2,-16(s0)		 #d
	li	a2,2		 #['*', 'd_1', '1', '2']
	addi	a2,a2,2		 #['-', 'd_3', 'd_2', '2']
	addi	a2,a0,10		 #['/', 'd_5', 'a_0', '10']
	sub	a2,a0,a2		 #['-', 'd_7', 'a_0', 'd_6']
	mv	a3,a2		 #['=', 'func ret_1', 'd_8']
	sw	a0,-24(s0)		 #a
	mv	a0,a3
	ret
