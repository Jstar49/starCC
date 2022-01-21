foo:
	addi	sp,sp,-24
	sw	s0,20(sp)
	addi	s0,sp,24
	sw	a0,-24(s0)		 #a
	sw	a1,-20(s0)		 #b
	li	a2,5
	sw	a2,-16(s0)		 #d
	li	a2,12		 #['+', 'd_1', '1', '2']
	addi	a2,a2,2		 #['+', 'd_3', 'd_2', '2']
	addi	a2,a2,2		 #['-', 'd_5', 'd_4', '2']
	mul	a2,a0,a1		 #['*', 'd_6', 'a_0', 'b_0']
	sw	a0,-24(s0)		 #a
	ret
