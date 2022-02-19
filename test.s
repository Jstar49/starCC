	.file	"test.c"
	.option	nopic
	.text
	.align	1
	.global	jiet
	.type	jiet, @function
jiet:
	addi	sp,sp,-24
	sw	ra,0(sp)
	sw	a0,20(sp)		 #b
	li	a1,7
	sw	a1,16(sp)		 #a
.L1:
	lw	a1,16(sp)		 #a Ret_reg_by_sym
	mv	a2,a1		 #['=', 'func ret_1', 'a_0']
	sw	a2,12(sp)		 #func ret assign
	sw	a0,20(sp)		 #b
	lw	ra,0(sp)
	addi	sp,sp,24
	mv	a0,a2
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
.L2:
	lw	a0,44(sp)		 #a Ret_reg_by_sym
	mv	a5,a0		 #['=', 'args temp0_1', 'a_0']
	sw	a5,16(sp)		 #args temp0 assign
	sw	a0,44(sp)		 #a
	lw	a5,16(sp)		 #args temp0 Ret_reg_by_sym
	mv	a0,a5
	call	jiet
	lw	a3,32(sp)		 #s Ret_reg_by_sym
	mv	a3,a0		 #['=', 's_1', 'fun ret']
	sw	a3,32(sp)		 #s assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym
	lw	a3,32(sp)		 #s Ret_reg_by_sym
	lui	a6,%hi(jxx)
	lw	a6,%lo(jxx)(a6)
	sw	a6,4(sp)		 #jxx assign
	add	a3,a3,a6		 #['+', 's_2', 's_1', 'jxx_0']
	sw	a3,32(sp)		 #s assign
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym
	li	a7,1
	add	a6,a6,a7		 #['+', 'jxx_1', 'jxx_0', '1']
	sw	a6,4(sp)		 #jxx assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym
	lw	a3,32(sp)		 #s Ret_reg_by_sym
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym
	add	a3,a3,a6		 #['+', 's_3', 's_2', 'jxx_1']
	sw	a3,32(sp)		 #s assign
	lw	a3,32(sp)		 #s Ret_reg_by_sym
	sw	a1,40(sp)		 #b
	lw	a1,24(sp)		 #func ret
	mv	a1,a3		 #['=', 'func ret_1', 's_3']
	sw	a1,24(sp)		 #func ret assign
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
