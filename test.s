foo:
	addi	sp,sp,-48
	sw	s0,44(sp)
	addi	s0,sp,48
	sw	a0,-48(s0)
	sw	a1,-44(s0)
	li	a2,4
	sw	a2,-40(s0)
	li	a3,1
	sw	a3,-32(s0)
	li	a4,1
	sw	a4,-28(s0)
	sw	a0,-48(s0)
	li	a0,1
	sw	a0,-24(s0)
	sw	a1,-44(s0)
	li	a1,1
	sw	a1,-20(s0)
	sw	a2,-40(s0)
	li	a2,2
	sw	a2,-16(s0)
	sw	a3,-32(s0)
	ret
