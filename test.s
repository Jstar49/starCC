	.file	"test.c"
	.option	nopic
	.text
	.align	1
	.global	jiet
	.type	jiet, @function
jiet:
	addi	sp,sp,-20
	sw	s0,16(sp)
	addi	s0,sp,20
	sw	a0,-20(s0)		 #b
	lw	a1,-16(s0)		 #a
	li	a1,+
	sw	a1,-16(s0)		 #a
.L1:
	lw	a2,-12(s0)		 #func ret
	mv	a2,a1		 #['=', 'func ret_1', 'a_0']
	sw	a0,-20(s0)		 #b
	lw	s0,16(sp)
	addi	sp,sp,20
	mv	a0,a2
	ret
	.size	jiet, .-jiet
	.align	1
	.global	foo
	.type	foo, @function
foo:
	addi	sp,sp,-32
	sw	s0,28(sp)
	addi	s0,sp,32
	sw	a0,-32(s0)		 #a
	lw	a1,-28(s0)		 #s
	li	a1,9
	sw	a1,-28(s0)		 #s
.L2:
	lw	a2,-16(s0)		 #args temp0
	mv	a2,a1		 #['=', 'args temp0_1', 's_0']
	sw	a0,-32(s0)		 #a
	mv	a0,a2
	call	jiet
	mv	a1,a0		 #['=', 's_1', 'fun ret']
	lw	a3,-24(s0)		 #func ret
	mv	a3,a1		 #['=', 'func ret_1', 's_1']
	sw	a0,-12(s0)		 #fun ret
	lw	s0,28(sp)
	addi	sp,sp,32
	mv	a0,a3
	ret
	.size	foo, .-foo
