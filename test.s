foo:
	addi	sp,sp,-28
	sw	s0,24(sp)
	addi	s0,sp,28
	sw	a0,-28(s0)		 #a
	sw	a1,-24(s0)		 #b
	li	a2,0
	sw	a2,-20(s0)		 #d
.L1
.L2
	sw	a1,-24(s0)		 #b
	li	a1,10
	sgt	a3,a0,a1
	xori	a3,a3,1
	andi	a3,a3,0xff		 #['<=', 'if condi_1', 'a_0', '10']
	beqz	a3,.L3		 #['beqz', 'if condi_1', 'func block 3']
	sw	a2,-20(s0)		 #d
	li	a2,1
	sub	a0,a0,a2		 #['-', 'a_1', 'a_0', '1']
	j	.L2
.L3
	mv	a4,a2		 #['=', 'func ret_1', 'd_0']
	sw	a0,-28(s0)		 #a
	mv	a0,a4
	ret
boo:
	addi	sp,sp,-20
	sw	s0,16(sp)
	addi	s0,sp,20
	li	a0,10
	sw	a0,-20(s0)		 #a
	li	a1,20
	sw	a1,-16(s0)		 #c
.L4
	add	a2,a0,a1		 #['+', 'func ret_1', 'a_0', 'c_0']
	sw	a0,-20(s0)		 #a
	mv	a0,a2
	ret
