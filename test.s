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
	lw	a1,12(sp)		 #a Ret_reg_by_sym
	mv	a2,a1		 #['=', 'func ret_1', 'a_0']
	sw	a2,8(sp)		 #func ret assign
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
	addi	sp,sp,-44
	sw	ra,0(sp)
	sw	a0,40(sp)		 #a
	sw	a1,36(sp)		 #b
	li	a2,0
	sw	a2,32(sp)		 #i
	li	a3,0
	sw	a3,28(sp)		 #s
.L2:
	lw	a3,28(sp)		 #s Ret_reg_by_sym
	mv	a4,a3		 #['=', 'args temp0_1', 's_0']
	sw	a4,16(sp)		 #args temp0 assign
	sw	a0,40(sp)		 #a
	lw	a4,16(sp)		 #args temp0 Ret_reg_by_sym
	mv	a0,a4
	call	jiet
	lw	a3,28(sp)		 #s Ret_reg_by_sym
	mv	a3,a0		 #['=', 's_1', 'fun ret']
	sw	a3,28(sp)		 #s assign
.L3:
	lw	a2,32(sp)		 #i Ret_reg_by_sym
	li	a6,3
	slt	a5,a2,a6
	andi	a5,a5,0xff		 #['<', 'if condi_1', 'i_0', '3']
	sw	a5,4(sp)		 #if condi assign
	lw	a5,4(sp)		 #if condi Ret_reg_by_sym
	beqz	a5,.L4		 #['beqz', 'if condi_1', 'func block 4']
	lw	a3,28(sp)		 #s Ret_reg_by_sym
	lw	a3,28(sp)		 #s Ret_reg_by_sym
	lw	a2,32(sp)		 #i Ret_reg_by_sym
	add	a3,a3,a2		 #['+', 's_2', 's_1', 'i_0']
	sw	a3,28(sp)		 #s assign
	lw	a2,32(sp)		 #i Ret_reg_by_sym
	lw	a2,32(sp)		 #i Ret_reg_by_sym
	li	a7,1
	add	a2,a2,a7		 #['+', 'i_1', 'i_0', '1']
	sw	a2,32(sp)		 #i assign
	j	.L3
.L4:
	lw	a3,28(sp)		 #s Ret_reg_by_sym
	sw	a0,12(sp)		 #fun ret
	lw	a0,24(sp)		 #func ret
	mv	a0,a3		 #['=', 'func ret_1', 's_2']
	sw	a0,24(sp)		 #func ret assign
	lw	ra,0(sp)
	addi	sp,sp,44
	ret
	.size	foo, .-foo
