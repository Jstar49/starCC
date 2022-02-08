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
	addi	sp,sp,-44
	sw	s0,40(sp)
	addi	s0,sp,44
	sw	a0,-44(s0)		 #a
	sw	a1,-40(s0)		 #b
	lw	a2,-36(s0)		 #s
	li	a2,9
	sw	a2,-36(s0)		 #s
.L2:
	li	a3,5
	sub	a2,a1,a3		 #['-', 's_1', '5', 'b_0']
	lw	a4,-28(s0)		 #op temp
	li	a5,5
	sub	a4,a1,a5		 #['-', 'op temp_1', 'b_0', '5']
	mv	a4,a0		 #['=', 'op temp_3', 'a_0']
	mv	a4,a1		 #['=', 'op temp_4', 'b_0']
	lw	a6,-24(s0)		 #args temp0
	mv	a6,a4		 #['=', 'args temp_0', 'op temp_2']
	lw	a7,-20(s0)		 #args temp1
	mv	a7,a4		 #['=', 'args temp_1', 'op temp_3']
	sw	a2,-36(s0)		 #s
	lw	a2,-16(s0)		 #args temp2
	mv	a2,a4		 #['=', 'args temp_2', 'op temp_4']
	sw	a0,-44(s0)		 #a
	mv	a0,a6
	sw	a1,-40(s0)		 #b
	mv	a1,a7
	sw	a2,-16(s0)		 #args temp2
	lw	a3,-16(s0)		 #args temp2
	mv	a2,a3
	call	jiet
	lw	a5,-36(s0)		 #s
	mv	a5,a0		 #['=', 's_3', 'fun ret']
	sw	a0,-12(s0)		 #fun ret
	lw	a0,-44(s0)		 #a
	add	a5,a5,a0		 #['+', 's_4', 's_3', 'a_0']
	lw	a1,-32(s0)		 #func ret
	mv	a1,a5		 #['=', 'func ret_1', 's_5']
	sw	a0,-44(s0)		 #a
	lw	s0,40(sp)
	addi	sp,sp,44
	mv	a0,a1
	ret
	.size	foo, .-foo
