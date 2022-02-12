	.file	"test.c"
	.option	nopic
	.text
	.align	1
	.global	jiet
	.type	jiet, @function
jiet:
	addi	sp,sp,-24
	sw	s0,20(sp)
	addi	s0,sp,24
	sw	a0,-24(s0)		 #c
	lw	a2,-20(s0)		 #a
	li	a2,7
	sw	a2,-20(s0)		 #a
	sw	a1,-16(s0)		 #b
.L1:
	lw	a3,-12(s0)		 #func ret
	mv	a3,a2		 #['=', 'func ret_1', 'a_0']
	sw	a0,-24(s0)		 #c
	lw	s0,20(sp)
	addi	sp,sp,24
	mv	a0,a3
	ret
	.size	jiet, .-jiet
	.align	1
	.global	foo
	.type	foo, @function
foo:
	addi	sp,sp,-24
	sw	s0,20(sp)
	addi	s0,sp,24
	sw	a0,-24(s0)		 #a
	sw	a1,-20(s0)		 #b
	lw	a2,-16(s0)		 #s
	li	a2,9
	sw	a2,-16(s0)		 #s
.L2:
	sgt	a2,a2,a1
	andi	a2,a2,0xff		 #['>', 's_1', 's_0', 'b_0']
	lw	a3,-12(s0)		 #func ret
	mv	a3,a2		 #['=', 'func ret_1', 's_2']
	sw	a0,-24(s0)		 #a
	lw	s0,20(sp)
	addi	sp,sp,24
	mv	a0,a3
	ret
	.size	foo, .-foo
