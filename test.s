	.file	"test.c"
	.option	nopic
	.text
	.align	1
	.global	jiet
	.type	jiet, @function
jiet:
	addi	sp,sp,-20
	sw	ra,0(sp)
	sw	a0,16(sp)		 #b
	li	a1,7
	sw	a1,12(sp)		 #a
.L1:
	mv	a2,a1		 #['=', 'func ret_1', 'a_0']
	sw	a0,16(sp)		 #b
	lw	ra,0(sp)
	addi	sp,sp,20
	mv	a0,a2
	ret
	.size	jiet, .-jiet
	.align	1
	.global	foo
	.type	foo, @function
foo:
	addi	sp,sp,-40
	sw	ra,0(sp)
	sw	a0,36(sp)		 #a
	li	a1,0
	sw	a1,28(sp)		 #s
.L2:
	mv	a2,a1		 #['=', 'args temp0_1', 's_0']
	sw	a0,36(sp)		 #a
	mv	a0,a2
	call	jiet
	mv	a1,a0		 #['=', 's_1', 'fun ret']
	li	a3,0		 #['=', 'i_1', '0']
.L3:
	li	a5,10
	sgt	a4,a3,a5
	xori	a4,a4,1
	andi	a4,a4,0xff		 #['<=', 'if condi_1', 'i_1', '10']
	beqz	a4,.L4		 #['beqz', 'if condi_1', 'func block 4']
	add	a1,a1,a3		 #['+', 's_2', 's_1', 'i_1']
	li	a6,5
	sgt	a4,a3,a6
	xori	a4,a4,1
	andi	a4,a4,0xff		 #['<=', 'if condi_2', 'i_1', '5']
	beqz	a4,.L5		 #['beqz', 'if condi_2', 'func block 5']
	j	.L4
	j	.L5
.L5:
	li	a7,1
	add	a3,a3,a7		 #['+', 'i_2', 'i_1', '1']
	j	.L3
.L4:
	sw	a0,12(sp)		 #fun ret
	lw	a0,24(sp)		 #func ret
	mv	a0,a1		 #['=', 'func ret_1', 's_2']
	.size	foo, .-foo
