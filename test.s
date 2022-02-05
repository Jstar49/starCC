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
	sw	a0,-20(s0)		 #c
	lw	a1,-16(s0)		 #a
	li	a1,7
	sw	a1,-16(s0)		 #a
.L1:
	lw	a2,-12(s0)		 #func ret
	mv	a2,a1		 #['=', 'func ret_1', 'a_0']
	sw	a0,-20(s0)		 #c
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
	sw	a1,-28(s0)		 #b
	lw	a2,-24(s0)		 #s
	li	a2,9
	sw	a2,-24(s0)		 #s
.L2:
	lui	a3,%hi(5)
	lw	a3,%lo(5)(a3)
	li	a4,b
	sub	a2,b,a4		 #['-', 's_1', '5', 'b_0']
	lw	a5,-16(s0)		 #op temp
	li	a6,5
	sub	a5,a1,a6		 #['-', 'op temp_1', 'b_0', '5']
	lw	a7,-8(s0)		 #args temp
	mv	a7,a5		 #['=', 'args temp_0', 'op temp_2']
	sw	a0,-32(s0)		 #a
	call	jiet
	mv	a2,a0		 #['=', 's_3', 'fun ret']
	sw	a0,-12(s0)		 #fun ret
	li	a0,b
	sub	a5,b,a0		 #['-', 'op temp_3', '5', 'b_0']
	mv	a7,a5		 #['=', 'args temp_0', 'op temp_4']
	call	jiet
	mv	a2,a0		 #['=', 's_4', 'fun ret']
	lw	a4,-32(s0)		 #a
	add	a2,a2,a4		 #['+', 's_5', 's_4', 'a_0']
	lw	a6,-20(s0)		 #func ret
	mv	a6,a2		 #['=', 'func ret_1', 's_6']
	sw	a0,-12(s0)		 #fun ret
	lw	s0,28(sp)
	addi	sp,sp,32
	mv	a0,a6
	ret
	.size	foo, .-foo
