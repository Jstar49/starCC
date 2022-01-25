foo:
	addi	sp,sp,-28
	sw	s0,24(sp)
	addi	s0,sp,28
	sw	a0,-28(s0)		 #a
	sw	a1,-24(s0)		 #b
	li	a2,5
	sw	a2,-20(s0)		 #d
.L1
	sub	a2,a0,a1
	seqz	a2,a2
	andi	a2,a2,0xff		 #['==', 'd_1', 'a_0', 'b_0']
	sub	a2,a0,a1
	snez	a2,a2
	andi	a2,a2,0xff		 #['!=', 'd_3', 'a_0', 'b_0']
	slt	a2,a0,a1
	xori	a2,a2,1
	andi	a2,a2,0xff		 #['>=', 'd_5', 'a_0', 'b_0']
	sgt	a2,a0,a1
	xori	a2,a2,1
	andi	a2,a2,0xff		 #['<=', 'd_7', 'a_0', 'b_0']
	sgt	a2,a0,a1
	andi	a2,a2,0xff		 #['>', 'd_9', 'a_0', 'b_0']
	slt	a2,a0,a1
	andi	a2,a2,0xff		 #['<', 'd_11', 'a_0', 'b_0']
	beqz	a2,.L3		 #['beqz', 'd_12', 'func block 3']
	li	a2,10		 #['=', 'd_13', '10']
	j	.L2
.L3
	li	a2,20		 #['=', 'd_14', '20']
.L2
	mv	a3,a2		 #['=', 'func ret_1', 'd_14']
	sw	a0,-28(s0)		 #a
	mv	a0,a3
	ret
