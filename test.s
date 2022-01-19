foo:
	addi	sp,sp,-20
	sw	s0,16(sp)
	addi	s0,sp,20
	sw	a0,-20(s0)		 #a
	sw	a1,-16(s0)		 #b
	mul	a2,a0,a1		 #['*', 'func ret_1', 'a_0', 'b_0']
	ret
