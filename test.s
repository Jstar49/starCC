	.file	"test.c"
	.option	nopic
	.text
	.align	1
	.global	jiet
	.type	jiet, @function
jiet:
	addi	sp,sp,-40
	sw	ra,0(sp)
	sw	a0,36(sp)		 #b
	li	a1,7
	sw	a1,32(sp)		 #a
.L1:
	lw	a2,20(sp)		 #s
	li	a2,0		 #['=', 's_1', '0']
	sw	a2,20(sp)		 #s assign
	lw	a3,28(sp)		 #i
	li	a3,0		 #['=', 'i_1', '0']
	sw	a3,28(sp)		 #i assign
.L2:
	lw	a4,8(sp)		 #if condi
	lw	a3,28(sp)		 #i Ret_reg_by_sym i
	li	a5,5
	slt	a4,a3,a5
	andi	a4,a4,0xff		 #['<', 'if condi_1', 'i_1', '5']
	sw	a4,8(sp)		 #if condi assign
	lw	a4,8(sp)		 #if condi Ret_reg_by_sym if condi
	beqz	a4,.L3		 #['beqz', 'if condi_1', 'func block 3']
	lw	a2,20(sp)		 #s Ret_reg_by_sym s
	lw	a2,20(sp)		 #s Ret_reg_by_sym s
	lw	a3,28(sp)		 #i Ret_reg_by_sym i
	add	a2,a2,a3		 #['+', 's_2', 's_1', 'i_1']
	sw	a2,20(sp)		 #s assign
	lw	a6,24(sp)		 #j
	li	a6,5		 #['=', 'j_1', '5']
	sw	a6,24(sp)		 #j assign
.L4:
	lw	a4,8(sp)		 #if condi Ret_reg_by_sym if condi
	lw	a6,24(sp)		 #j Ret_reg_by_sym j
	li	a7,0
	sgt	a4,a6,a7
	andi	a4,a4,0xff		 #['>', 'if condi_2', 'j_1', '0']
	sw	a4,8(sp)		 #if condi assign
	lw	a4,8(sp)		 #if condi Ret_reg_by_sym if condi
	beqz	a4,.L5		 #['beqz', 'if condi_2', 'func block 5']
	lw	a2,20(sp)		 #s Ret_reg_by_sym s
	lw	a2,20(sp)		 #s Ret_reg_by_sym s
	lw	a6,24(sp)		 #j Ret_reg_by_sym j
	add	a2,a2,a6		 #['+', 's_3', 's_2', 'j_1']
	sw	a2,20(sp)		 #s assign
	lw	a6,24(sp)		 #j Ret_reg_by_sym j
	sw	a0,36(sp)		 #b
	lw	a6,24(sp)		 #j Ret_reg_by_sym j
	li	a0,1
	sub	a6,a6,a0		 #['-', 'j_2', 'j_1', '1']
	sw	a6,24(sp)		 #j assign
	j	.L4
.L5:
	lw	a3,28(sp)		 #i Ret_reg_by_sym i
	sw	a1,32(sp)		 #a
	lw	a3,28(sp)		 #i Ret_reg_by_sym i
	li	a1,1
	add	a3,a3,a1		 #['+', 'i_2', 'i_1', '1']
	sw	a3,28(sp)		 #i assign
	j	.L2
.L3:
	lw	a2,20(sp)		 #s Ret_reg_by_sym s
	lw	a5,16(sp)		 #func ret
	mv	a5,a2		 #['=', 'func ret_1', 's_3']
	sw	a5,16(sp)		 #func ret assign
	lw	ra,0(sp)
	addi	sp,sp,40
	mv	a0,a5
	ret
	.size	jiet, .-jiet
	.align	1
	.global	foo
	.type	foo, @function
foo:
	addi	sp,sp,-48
	sw	ra,0(sp)
	sw	a0,44(sp)		 #a
	sw	a1,40(sp)		 #b
	li	a2,0
	sw	a2,36(sp)		 #i
	li	a3,0
	sw	a3,32(sp)		 #s
	li	a4,0
	sw	a4,28(sp)		 #j
.L6:
	lw	a0,44(sp)		 #a Ret_reg_by_sym a
	lw	a5,16(sp)		 #args temp0
	mv	a5,a0		 #['=', 'args temp0_1', 'a_0']
	sw	a5,16(sp)		 #args temp0 assign
	sw	a0,44(sp)		 #a
	lw	a5,16(sp)		 #args temp0 Ret_reg_by_sym args temp0
	mv	a0,a5
	call	jiet
	sw	a0,12(sp)		 #fun ret assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym s
	mv	a3,a0		 #['=', 's_1', 'fun ret']
	sw	a3,32(sp)		 #s assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym s
	lw	a3,32(sp)		 #s Ret_reg_by_sym s
	lui	a6,%hi(jxx)
	lw	a6,%lo(jxx)(a6)
	sw	a6,4(sp)		 #jxx assign
	add	a3,a3,a6		 #['+', 's_2', 's_1', 'jxx_0']
	sw	a3,32(sp)		 #s assign
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym jxx
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym jxx
	li	a7,10
	add	a6,a6,a7		 #['+', 'jxx_1', 'jxx_0', '10']
	sw	a6,4(sp)		 #jxx assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym s
	lw	a3,32(sp)		 #s Ret_reg_by_sym s
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym jxx
	add	a3,a3,a6		 #['+', 's_3', 's_2', 'jxx_1']
	sw	a3,32(sp)		 #s assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym s
	sw	a1,40(sp)		 #b
	lw	a1,24(sp)		 #func ret
	mv	a1,a3		 #['=', 'func ret_1', 's_3']
	sw	a1,24(sp)		 #func ret assign
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym jxx
	sw	a2,36(sp)		 #i
	lui	a2,%hi(jxx)
	sw	a6,%lo(jxx)(a2)
	sw	a0,12(sp)		 #fun ret
	lw	ra,0(sp)
	addi	sp,sp,48
	mv	a0,a1
	ret
	.size	foo, .-foo
	.global	jxx
	.align	2
	.type	jxx, @object
	.size	jxx, 4
jxx:
	.word	5
