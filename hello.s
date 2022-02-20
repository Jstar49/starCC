	.file	"hello.c"
	.option	nopic
	.text
	.align	1
	.global	jiet
	.type	jiet, @function
jiet:
	addi	sp,sp,-20
	sw	ra,0(sp)
	sw	a0,16(sp)		 #a
.L1:
	lw	a0,16(sp)		 #a Ret_reg_by_sym a
	lw	a1,12(sp)		 #func ret
	mv	a1,a0		 #['=', 'func ret_1', 'a_0']
	sw	a1,12(sp)		 #func ret assign
	sw	a0,16(sp)		 #a
	lw	ra,0(sp)
	addi	sp,sp,20
	mv	a0,a1
	ret
	.size	jiet, .-jiet
	.align	1
	.global	foo
	.type	foo, @function
foo:
	addi	sp,sp,-40
	sw	ra,0(sp)
	sw	a0,36(sp)		 #a
	sw	a1,32(sp)		 #b
	li	a2,0
	sw	a2,28(sp)		 #s
.L2:
	lw	a0,36(sp)		 #a Ret_reg_by_sym a
	lw	a3,16(sp)		 #args temp0
	mv	a3,a0		 #['=', 'args temp0_1', 'a_0']
	sw	a3,16(sp)		 #args temp0 assign
	sw	a0,36(sp)		 #a
	lw	a3,16(sp)		 #args temp0 Ret_reg_by_sym args temp0
	mv	a0,a3
	call	jiet
	sw	a0,12(sp)		 #fun ret assign
	lw	a2,28(sp)		 #s Ret_reg_by_sym s
	lw	a1,32(sp)		 #b Ret_reg_by_sym b
	lw	a0,12(sp)		 #fun ret Ret_reg_by_sym fun ret
	add	a2,a1,a0		 #['+', 's_1', 'b_0', 'fun ret']
	sw	a2,28(sp)		 #s assign
	lw	a2,28(sp)		 #s Ret_reg_by_sym s
	lw	a4,36(sp)		 #a
	lw	a2,28(sp)		 #s Ret_reg_by_sym s
	add	a2,a4,a2		 #['+', 's_2', 'a_0', 's_1']
	sw	a2,28(sp)		 #s assign
	lw	a2,28(sp)		 #s Ret_reg_by_sym s
	lw	a5,24(sp)		 #func ret
	mv	a5,a2		 #['=', 'func ret_1', 's_3']
	sw	a5,24(sp)		 #func ret assign
	sw	a0,12(sp)		 #fun ret
	lw	ra,0(sp)
	addi	sp,sp,40
	mv	a0,a5
	ret
	.size	foo, .-foo
	.comm	jxx,4,4
