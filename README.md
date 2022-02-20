# starcc

A simple C syntax risCV instruction compiler

## 简介

一个简单C语法的riscv指令编译器，由python3 编写。
该项目的目的主要为了学习编译原理。通过自制编译器的实战方式，能够对从编译到链接的过程有一个大致的了解。因为主要是为了学习，所以并没有支持所有的C语法，仅仅支持比较简单的语法以及操作。

支持的C语法：

- if-else, for, while 控制语句，可嵌套使用；
- int , char, short 类型变量，仅支持整型数据，不支持浮点数据；
- 函数调用
- 全局变量引用与修改

一些C语法要求：

- 所有的控制语句后必须接代码块符号 '{}'。就是说即使 if 后只有一条语句也必须使用代码块标记符。这仅仅是为了我的开发方便。
- 虽说支持 int , char , short 数据类型，但是在操作上都是默认 32 位 int 类型数据进行处理。
- 所有的变量声明必须在函数开头完成，不接受在 for 、while、if 控制块中声明局部变量，且函数声明时只接受不赋值或者赋值常量形式，不允许通过变量进行赋值声明（如 int a = b;）。

## 食用方式

### 环境要求  

 - Python version >= 3.6.9, 要求安装 graphviz 库（用于生成语法树图）。
 - riscv-gnu toolchain. 安装 [RISCV-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain) 环境。选择32位linux版本，包括riscv-gdb、riscv-run 工具。

### 使用方式  

仅支持命令行参数传入形式  

1、传入 C 代码文件。指定需要进行分析的C原程序。
```shell
python3 main.py -f test.c 
```

2、词法分析。分析 C 文件的关键字，形成C语法的 token 流，将会直接输出到控制台，带有简单的弱语法检查。
```shell
python3 main.py -f test.c -l
```

3、语法分析。根据 C 语法的 token 数据流，形成 C 程序的语法树，输出到与 C 文件同名的 .gv.png 文件中。带有基础的弱语法检查。

```shell
python3 main.py -f test.c -p
```

4、语义分析。根据 C 代码的语法树，进行简单的语义分析，生成中间代码，将直接输出到控制台。
```shell
python3 main.py -f test.c -r
```

5、代码生成。将生成的中间代码翻译成 riscv 指令的汇编代码, 结果输出到 C 文件同名的 .s 文件中。
```shell
python3 main.py -f test.c -s
```

## 案例测试  

### 案例1  

hello.c:  
```c
int jiet(int a){
	return a;
}
int jxx;
int foo(int a,int b){
	int s = 0;
	s = a + b + jiet(a);
	return s;
}
```

**词法分析  :**  

```shell
# python3 main.py -f test.c -l
(T_int, int)
(T_identifier, jiet)
(T_l1_bracket, ()
(T_int, int)
(T_identifier, a)
(T_r1_bracket, ))
(T_l3_braket, {)
(T_return, return)
(T_identifier, a)
(T_semicolon, ;)
(T_r3_braket, })
(T_int, int)
(T_identifier, jxx)
(T_semicolon, ;)
(T_int, int)
(T_identifier, foo)
(T_l1_bracket, ()
(T_int, int)
(T_identifier, a)
(T_comma, ,)
(T_int, int)
(T_identifier, b)
(T_r1_bracket, ))
(T_l3_braket, {)
(T_int, int)
(T_identifier, s)
(T_assign, =)
(T_constant, 0)
(T_semicolon, ;)
(T_identifier, s)
(T_assign, =)
(T_identifier, a)
(T_add, +)
(T_identifier, b)
(T_add, +)
(T_identifier, jiet)
(T_l1_bracket, ()
(T_identifier, a)
(T_r1_bracket, ))
(T_semicolon, ;)
(T_return, return)
(T_identifier, s)
(T_semicolon, ;)
(T_r3_braket, })
```

**语法分析**  生成语法树。  

```shell
# python3 main.py -f hello.c -p
```

生成的语法树：  

![hello.png](https://cdn.jsdelivr.net/gh/mybules/cdn@1.6.5/mybules/2022-2-20/hello.gv.png) 


**语义分析**  生成中间代码。  

```shell
# python3 main.py -f hello.c -r
['jiet:']
['func block 1:']
         ['=', 'func ret_1', 'a_0']
         ['return', 'func ret_1']
['foo:']
['func block 2:']
         ['=', 'args temp0_1', 'a_0']
         ['call', 'jiet']
         ['+', 's_1', 'b_0', 'fun ret']
         ['+', 's_2', 'a_0', 's_1']
         ['=', 's_3', 's_2']
         ['=', 'func ret_1', 's_3']
         ['return', 'func ret_1']
```

**代码生成**，生成 riscv 的汇编代码。'#'符后为注释。

```shell
# python3 main.py -f hello.c -s
# cat hello.s
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
```



### 案例2  

test.c:  
```c
int jiet(int b){
	int a = 7;
	int i,j,s;
	s = 0;
	for (i=0;i<5;i+=1){
		s += i;
		j=5;
		while (j>0){
			s += j;
			j -= 1;
		}
	}
	return s;
}
int jxx=5;
int foo(int a,int b){
	int i=0,s = 0,j=0;
	s = jiet(a);
	s += jxx;
	jxx += 10;
	s += jxx;
	return s;
}
```
**词法分析  :**  

```shell
# python3 main.py -f test.c -l
(T_int, int)
(T_identifier, jiet)
(T_l1_bracket, ()
(T_int, int)
(T_identifier, b)
(T_r1_bracket, ))
(T_l3_braket, {)
(T_int, int)
(T_identifier, a)
(T_assign, =)
(T_constant, 7)
(T_semicolon, ;)
(T_int, int)
(T_identifier, i)
(T_comma, ,)
(T_identifier, j)
(T_comma, ,)
(T_identifier, s)
(T_semicolon, ;)
(T_identifier, s)
(T_assign, =)
(T_constant, 0)
(T_semicolon, ;)
(T_for, for)
(T_l1_bracket, ()
(T_identifier, i)
(T_assign, =)
(T_constant, 0)
(T_semicolon, ;)
(T_identifier, i)
(T_lt, <)
(T_constant, 5)
(T_semicolon, ;)
(T_identifier, i)
(T_add_assign, +=)
(T_constant, 1)
(T_r1_bracket, ))
(T_l3_braket, {)
(T_identifier, s)
(T_add_assign, +=)
(T_identifier, i)
(T_semicolon, ;)
(T_identifier, j)
(T_assign, =)
(T_constant, 5)
(T_semicolon, ;)
(T_while, while)
(T_l1_bracket, ()
(T_identifier, j)
(T_gt, >)
(T_constant, 0)
(T_r1_bracket, ))
(T_l3_braket, {)
(T_identifier, s)
(T_add_assign, +=)
(T_identifier, j)
(T_semicolon, ;)
(T_identifier, j)
(T_sub_assign, -=)
(T_constant, 1)
(T_semicolon, ;)
(T_r3_braket, })
(T_r3_braket, })
(T_return, return)
(T_identifier, s)
(T_semicolon, ;)
(T_r3_braket, })
(T_int, int)
(T_identifier, jxx)
(T_assign, =)
(T_constant, 5)
(T_semicolon, ;)
(T_int, int)
(T_identifier, foo)
(T_l1_bracket, ()
(T_int, int)
(T_identifier, a)
(T_comma, ,)
(T_int, int)
(T_identifier, b)
(T_r1_bracket, ))
(T_l3_braket, {)
(T_int, int)
(T_identifier, i)
(T_assign, =)
(T_constant, 0)
(T_comma, ,)
(T_identifier, s)
(T_assign, =)
(T_constant, 0)
(T_comma, ,)
(T_identifier, j)
(T_assign, =)
(T_constant, 0)
(T_semicolon, ;)
(T_identifier, s)
(T_assign, =)
(T_identifier, jiet)
(T_l1_bracket, ()
(T_identifier, a)
(T_r1_bracket, ))
(T_semicolon, ;)
(T_identifier, s)
(T_add_assign, +=)
(T_identifier, jxx)
(T_semicolon, ;)
(T_identifier, jxx)
(T_add_assign, +=)
(T_constant, 10)
(T_semicolon, ;)
(T_identifier, s)
(T_add_assign, +=)
(T_identifier, jxx)
(T_semicolon, ;)
(T_return, return)
(T_identifier, s)
(T_semicolon, ;)
(T_r3_braket, })
```

**语法分析**  生成语法树。  

```shell
# python3 main.py -f test.c -p
```
生成的语法树：  

![test.png](https://cdn.jsdelivr.net/gh/mybules/cdn@1.6.5/mybules/2022-2-20/test.gv.png)  


**语义分析**  生成中间代码。  
```shell
# python3 main.py -f test.c -p
['jiet:']
['func block 1:']
         ['=', 's_1', '0']
         ['=', 'i_1', '0']
['func block 2:']
         ['<', 'if condi_1', 'i_1', '5']
         ['beqz', 'if condi_1', 'func block 3']
         ['+', 's_2', 's_1', 'i_1']
         ['=', 'j_1', '5']
['func block 4:']
         ['>', 'if condi_2', 'j_1', '0']
         ['beqz', 'if condi_2', 'func block 5']
         ['+', 's_3', 's_2', 'j_1']
         ['-', 'j_2', 'j_1', '1']
         ['b', 'func block 4']
['func block 5:']
         ['+', 'i_2', 'i_1', '1']
         ['b', 'func block 2']
['func block 3:']
         ['=', 'func ret_1', 's_3']
         ['return', 'func ret_1']
['foo:']
['func block 6:']
         ['=', 'args temp0_1', 'a_0']
         ['call', 'jiet']
         ['=', 's_1', 'fun ret']
         ['+', 's_2', 's_1', 'jxx_0']
         ['+', 'jxx_1', 'jxx_0', '10']
         ['+', 's_3', 's_2', 'jxx_1']
         ['=', 'func ret_1', 's_3']
         ['return', 'func ret_1']
```

**代码生成**，生成 riscv 的汇编代码。'#'符后为注释。

```shell
# python3 main.py -f test.c -s
# cat test.s
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
	li	a2,0		 #['=', 's_1', '0']
	sw	a2,20(sp)		 #s assign
	li	a3,0		 #['=', 'i_1', '0']
	sw	a3,28(sp)		 #i assign
.L2:
	lw	a3,28(sp)		 #i Ret_reg_by_sym
	li	a5,5
	slt	a4,a3,a5
	andi	a4,a4,0xff		 #['<', 'if condi_1', 'i_1', '5']
	sw	a4,8(sp)		 #if condi assign
	lw	a4,8(sp)		 #if condi Ret_reg_by_sym
	beqz	a4,.L3		 #['beqz', 'if condi_1', 'func block 3']
	lw	a2,20(sp)		 #s Ret_reg_by_sym
	lw	a2,20(sp)		 #s Ret_reg_by_sym
	lw	a3,28(sp)		 #i Ret_reg_by_sym
	add	a2,a2,a3		 #['+', 's_2', 's_1', 'i_1']
	sw	a2,20(sp)		 #s assign
	li	a6,5		 #['=', 'j_1', '5']
	sw	a6,24(sp)		 #j assign
.L4:
	lw	a4,8(sp)		 #if condi Ret_reg_by_sym
	lw	a6,24(sp)		 #j Ret_reg_by_sym
	li	a7,0
	sgt	a4,a6,a7
	andi	a4,a4,0xff		 #['>', 'if condi_2', 'j_1', '0']
	sw	a4,8(sp)		 #if condi assign
	lw	a4,8(sp)		 #if condi Ret_reg_by_sym
	beqz	a4,.L5		 #['beqz', 'if condi_2', 'func block 5']
	lw	a2,20(sp)		 #s Ret_reg_by_sym
	lw	a2,20(sp)		 #s Ret_reg_by_sym
	lw	a6,24(sp)		 #j Ret_reg_by_sym
	add	a2,a2,a6		 #['+', 's_3', 's_2', 'j_1']
	sw	a2,20(sp)		 #s assign
	lw	a6,24(sp)		 #j Ret_reg_by_sym
	sw	a0,36(sp)		 #b
	lw	a6,24(sp)		 #j Ret_reg_by_sym
	li	a0,1
	sub	a6,a6,a0		 #['-', 'j_2', 'j_1', '1']
	sw	a6,24(sp)		 #j assign
	j	.L4
.L5:
	lw	a3,28(sp)		 #i Ret_reg_by_sym
	sw	a1,32(sp)		 #a
	lw	a3,28(sp)		 #i Ret_reg_by_sym
	li	a1,1
	add	a3,a3,a1		 #['+', 'i_2', 'i_1', '1']
	sw	a3,28(sp)		 #i assign
	j	.L2
.L3:
	lw	a2,20(sp)		 #s Ret_reg_by_sym
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
	li	a7,10
	add	a6,a6,a7		 #['+', 'jxx_1', 'jxx_0', '10']
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
	lw	a6,4(sp)		 #jxx Ret_reg_by_sym
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

```



### 正确性验证

由于目前尚不支持 printf/scanf I/O 操作，所以借助 main.c 来进行验证：

```c
#include<stdio.h>
extern int foo(int a,int b);
int main(){
    int a = 5;
    int b = 10;
    int c = foo(a,b);
    printf("c = %d\n",c); 
    return 0;
}
```

使用main.c 中主函数调用返回的形式判断正确性：

```shell
# 案例1
> python3 main.py -f hello.c -s
> riscv32-unknown-elf-gcc hello.s -c
> riscv32-unknown-elf-gcc main.s -c
> riscv32-unknown-elf-gcc hello.o main.o -o a.out
> riscv32-unknown-elf-run a.out
c = 20
jxx = 0

# 案例2
> python3 main.py -f test.c -s
> riscv32-unknown-elf-gcc test.s -c
> riscv32-unknown-elf-gcc main.s -c
> riscv32-unknown-elf-gcc test.o main.o -o a.out
> riscv32-unknown-elf-run a.out
c = 105
jxx = 15
```

由输出信息得知，计算结果与待测试C文件中预期结果一致。




## TODO

 - 目前的语法简单非常简单，需添加更加严格的语法检查；
 - 代码优化，目前有较多的冗余代码，code size 还有可压缩的空间；
 - 浮点数支持；
 - 生成 xx.o 的可重定位文件；
 - 链接；



