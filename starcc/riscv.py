
"""
# 最困难的是寄存器分配，必须好好思量
"""
import copy
A_RRGISTER = ['a7','a6','a5','a4','a3','a2','a1','a0']
# A_RRGISTER = ['a4','a3','a2','a1','a0']
ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y),"/": (lambda x,y: x/y), "*": (lambda x,y: x*y)}
OPERATOR = {'+':'add','-':'sub','*':'mul','/':'div'}
COMP = ['>','>=','<','<=','==','!=']

class Riscv(object):
	"""docstring for Assembly"""
	def __init__(self, passes):
		self.fun_pool = passes.fun_pool
		self.outputAss = []
		# 全局变量
		self.global_var_dict = passes.global_var_dict
		
		# 局部变量表
		self.fun_symbol_dict = None
		self.register = None
		self.a_register = None
		# 变量与寄存器的映射
		self.var_register = None
		# 寄存器与变量的映射
		self.register_var = None
		self.var_in_sp_off = None
		# 已使用的寄存器
		self.reg_used = None
		# 汇编代码
		self.func_assembly = []

	# 主函数
	def main(self,file_name):
		# 输出文件
		ass_file_name = file_name
		self.outFile = open(ass_file_name+".s","w")
		# 汇编文件头
		self.Assembly_head(ass_file_name)
		for func in self.fun_pool:
			# 函数局部变量
			self.fun_symbol_dict = self.fun_pool[func]['fun_symbol_dict']
			# func_assembly = []
			# 初始的寄存器分配, 返回sp的偏移量
			self.sp_off = self.Reg_init(func)
			# 函数头调试信息
			self.Func_head_debug(func)
			# 根据IR生成汇编代码
			self.IR2Assemble(self.fun_pool[func]['insn'],self.func_assembly,self.sp_off)
			self.Func_tail_debug(func)
			self.Func_end()
		# global varibal
		self.Global_assembly()
		self.PrintAssemble(self.func_assembly)
		# 关闭文件
		self.outFile.close()


	#global var
	def Global_assembly(self):
		for gvar in self.global_var_dict:
			if 'init_value' in self.global_var_dict[gvar]:
				self.func_assembly.append("\t.global\t"+gvar)
				self.func_assembly.append("\t.align\t2")
				self.func_assembly.append("\t.type\t"+gvar+", @object")
				self.func_assembly.append("\t.size\t"+gvar+", 4")
				self.func_assembly.append(gvar+":")
				self.func_assembly.append("\t.word\t"+self.global_var_dict[gvar]["init_value"])
			else:
				self.func_assembly.append("\t.comm\t"+gvar+",4,4")


	# 汇编文件头
	def Assembly_head(self,file_name):
		self.func_assembly.append("\t.file\t\""+file_name+".c\"")
		self.func_assembly.append("\t.option\tnopic")
		self.func_assembly.append("\t.text")

	# 函数结束后寄存器归位，为下一个函数做准备
	def Func_end(self):
		pass

	# 函数寄存器分配--初始化
	def Reg_init(self,func):
		
		# 函数符号对象
		fun_sym = self.fun_pool[func]['fun_symbol_dict']
		# 可用寄存器备份
		self.a_register = copy.deepcopy(A_RRGISTER)
		# 变量与寄存器的映射
		self.var_register = {}
		# 寄存器与变量的映射
		self.register_var = {}
		# 变量在sp中的偏移
		self.var_in_sp_off = {}
		# 已使用的寄存器
		self.reg_used = []
		sp_off = 0
		for sym in fun_sym:
			self.var_in_sp_off[sym] = sp_off
			sp_off += 4
			# 函数参数
			if 'sym_type' in fun_sym[sym] and fun_sym[sym]['sym_type'] == 'fun_args':
				arg_reg = self.a_register.pop()
				self.var_register[sym] = arg_reg
				self.register_var[arg_reg] = sym
				self.reg_used.append(arg_reg)
			# 函数内局部变量
			elif 'sym_type' in fun_sym[sym] and fun_sym[sym]['sym_type'] == 'fun_var':
				self.var_register[sym] = None
			else:
				self.var_register[sym] = None
		# 全局变量
		for sym in self.global_var_dict:
			self.var_in_sp_off[sym] = sp_off
			sp_off += 4

		return sp_off + 4

	# 输出
	def PrintAssemble(self, ass_list):
		for code in ass_list:
			# 
			self.outFile.write(code+"\n")


	def IR2Assemble(self, insn_stream, func_assembly,sp_off):
		for insn in insn_stream:
			# 遇到函数头
			if insn.insn_type == 'func_head':
				func_assembly.append(insn.insn[0])
				# sp 寄存器初始化
				self.Fun_sp_init(func_assembly,sp_off)
			elif insn.insn_type == 'code_block':
				self.Code_block(insn, func_assembly)
			elif insn.insn_type == 'return':
				self.Ret_insn(insn, func_assembly)
			elif insn.insn_type == 'Operation':
				self.Op_insn(insn, func_assembly)
			elif insn.insn_type == 'assign':
				self.Assign(insn, func_assembly)
			elif insn.insn_type == 'condi_jump':
				self.Condi_jump(insn, func_assembly)
			elif insn.insn_type == 'jump':
				self.NoCondi_jump(insn, func_assembly)
			elif insn.insn_type == 'FunctionCall':
				self.Call_func(insn, func_assembly)

	# 函数头调试信息
	def Func_head_debug(self,func_name):
		self.func_assembly.append("\t.align\t1")
		self.func_assembly.append("\t.global\t"+func_name+"")
		self.func_assembly.append("\t.type\t"+func_name+", @function")

	# 函数尾调试信息
	def Func_tail_debug(self,func_name):
		self.func_assembly.append("\t.size\t"+func_name+", .-"+func_name)

	# 函数sp寄存器初始化
	def Fun_sp_init(self,ass_list,sp_off):
		# print("debug riscv 157",self.var_in_sp_off)
		ass_list.append("\taddi\tsp,sp,-"+str(sp_off))
		# ass_list.append("\tsw\ts0,"+str(sp_off-4)+"(sp)")
		# ass_list.append("\taddi\ts0,sp,"+str(sp_off))
		ass_list.append("\tsw\tra,0(sp)")
		
		# 保存参数
		for fun_sym in self.fun_symbol_dict:
			# 函数参数
			if "sym_type" in self.fun_symbol_dict[fun_sym] and \
					self.fun_symbol_dict[fun_sym]['sym_type'] == 'fun_args':
				ass_code = "\tsw\t"+self.var_register[fun_sym]+","
				off_ = sp_off - self.var_in_sp_off[fun_sym]-4
				# ass_code += str(-off_)+"(s0)"
				ass_code += str(off_)+"(sp)"
				ass_code += "\t\t #"+fun_sym
				ass_list.append(ass_code)
			# 函数内有初始化的变量
			if "sym_type" in self.fun_symbol_dict[fun_sym] and \
					self.fun_symbol_dict[fun_sym]['sym_type'] == 'fun_var' and \
				'init_value' in self.fun_symbol_dict[fun_sym]:
				ass_code = "\tli\t"
				# reg = self.a_register.pop()
				reg = self.Get_alive_reg()
				ass_code += reg + ","+self.fun_symbol_dict[fun_sym]['init_value']
				ass_list.append(ass_code)
				ass_code = "\tsw\t"+reg+","
				off_ = sp_off - self.var_in_sp_off[fun_sym]-4
				# ass_code += str(-off_)+"(s0)"
				ass_code += str(off_)+"(sp)"
				ass_code += "\t\t #"+fun_sym
				ass_list.append(ass_code)
				self.var_register[fun_sym] = reg 
				self.register_var[reg] = fun_sym

	# 保存寄存器中的值
	def Save_reg(self,reg_num):
		if reg_num not in self.register_var:
			return
		if self.register_var[reg_num] == None:
			return
		ori_sym = self.register_var[reg_num]
		self.var_register[ori_sym] = None
		self.register_var[reg_num] = None
		ass_code = "\tsw\t"+reg_num+","
		off_ = self.sp_off - self.var_in_sp_off[ori_sym]-4
		# ass_code += str(-off_)+"(s0)"
		ass_code += str(off_)+"(sp)"
		ass_code += "\t\t #"+ori_sym
		self.func_assembly.append(ass_code)

	# 根据符号取出可用的寄存器
	def Ret_reg_by_sym(self,symbol):
		# 是否在var_register中 
		# print("debug riscv 216",symbol, self.var_register[symbol])
		if symbol in self.var_register:
			# 暂时没有映射关系
			if self.var_register[symbol] == None:
				reg = None
				# print("debug riscv 216",self.a_register)
				if len(self.a_register):
					reg = self.a_register.pop()
					self.var_register[symbol] = reg
					self.register_var[reg] = symbol
					self.reg_used.append(reg)
					# return reg
				else:
					reg = self.reg_used.pop(0)
					# 保存原来寄存器中の值
					self.Save_reg(reg)
				# print("debug riscv 225",reg)
				self.var_register[symbol] = reg
				self.register_var[reg] = symbol
				self.reg_used.append(reg)
				
				
				# 重新读取
				ass_code = "\tlw\t"+reg+","
				off_ = self.sp_off - self.var_in_sp_off[symbol]-4
				# ass_code += str(-off_)+"(s0)"
				ass_code += str(off_)+"(sp)"
				ass_code += "\t\t #"+symbol
				self.func_assembly.append(ass_code)
				return reg
			# 已存在映射关系
			else:
				# reg重新上色
				self.reg_used.remove(self.var_register[symbol])
				self.reg_used.append(self.var_register[symbol])
				reg = self.var_register[symbol]
				ass_code = "\tlw\t"+reg+","
				off_ = self.sp_off - self.var_in_sp_off[symbol]-4
				# ass_code += str(-off_)+"(s0)"
				ass_code += str(off_)+"(sp)"
				ass_code += "\t\t #"+symbol+" Ret_reg_by_sym "+symbol
				self.func_assembly.append(ass_code)
				return reg
		# 否则视为全局变量
		else:
			
			reg = None
			if len(self.a_register):
				reg = self.a_register.pop()
			else:
				# 
				reg = self.reg_used.pop(0)
				# 保存原来寄存器中の值
				self.Save_reg(reg)
			self.var_register[symbol] = reg
			self.register_var[reg] = symbol
			self.reg_used.append(reg)
			ass_code = '\tlui\t'+reg+",%hi("+symbol+")"
			self.func_assembly.append(ass_code)
			ass_code = "\tlw\t"+reg+",%lo("+symbol+")("+reg+")"
			self.func_assembly.append(ass_code)
			self.Save_var_in_sp(symbol)
			return reg

	# 保存变量值
	def Save_var_in_sp(self,symbol):
		# 所有的赋值操作后改变了变量的值，必须要在sp中进行保存
		# ass_code = "\tsw "+str(insn.insn)
		ass_code = "\tsw\t"+self.var_register[symbol]+","
		off_ = self.sp_off - self.var_in_sp_off[symbol]-4
		# ass_code += str(-off_)+"(s0)"
		ass_code += str(off_)+"(sp)"
		ass_code += "\t\t #"+symbol +" assign"
		self.func_assembly.append(ass_code)


	# 重置寄存器
	def Reset_reg(self,reg):
		symbol = self.register_var[reg]
		# 如果reg已被使用
		if symbol:
			self.Save_reg(reg)

	# 取出一个可用的寄存器
	def Get_alive_reg(self):
		reg = None
		if len(self.a_register):
			reg = self.a_register.pop()
		else:
			reg = self.reg_used.pop(0)
			self.Save_reg(reg)
		self.reg_used.append(reg)
		return reg

	# call 语句
	def Call_func(self, insn, ass_list):
		# 
		func_name = insn.insn[-1]
		
		self.Reset_reg('a0')
		for i in range(len(self.fun_pool[func_name]['args'])):
			self.Reset_reg('a'+str(i))
			reg = self.Ret_reg_by_sym("args temp"+str(i))
			ass_code = "\tmv\ta"+str(i)+","+reg
			ass_list.append(ass_code)
		ass_code = "\tcall\t"+insn.insn[-1]
		ass_list.append(ass_code)
		# 保存返回值
		# self.Save_var_in_sp("fun ret")
		self.Reset_reg('a0')
		self.var_register['fun ret'] = 'a0'
		self.register_var['a0'] = 'fun ret'
		self.Save_var_in_sp("fun ret")


	# 代码块
	def Code_block(self, insn, ass_list):
		
		code_block = insn.insn[0].split("func block ")[-1].split(":")[0]
		ass_code = ".L"+code_block + ":"
		ass_list.append(ass_code)

	# 无条件跳转
	def NoCondi_jump(self,insn, ass_list):
		
		# condi_reg = self.Ret_reg_by_sym(insn.op0)
		ass_code = "\tj\t"
		code_block = insn.insn[1].split("func block ")[-1]
		ass_code += ".L"+code_block
		# ass_code += "\t\t #"+ str(insn.insn)
		ass_list.append(ass_code)

	# 有条件跳转
	def Condi_jump(self,insn, ass_list):
		condi_reg = self.Ret_reg_by_sym(insn.op0)
		ass_code = "\tbeqz\t"+condi_reg+","
		code_block = insn.insn[2].split("func block ")[-1]
		ass_code += ".L"+code_block
		ass_code += "\t\t #"+ str(insn.insn)
		ass_list.append(ass_code)

	# Save global var
	def Save_global_var(self):
		for gvar in self.global_var_dict:
			if "has_edit" in self.global_var_dict[gvar]:
				
				reg = self.Ret_reg_by_sym(gvar)
				hi_reg = self.Get_alive_reg()
				ass_code = "\tlui\t"+hi_reg+",%hi("+gvar+")"
				self.func_assembly.append(ass_code)
				ass_code = "\tsw\t"+reg+",%lo("+gvar+")("+hi_reg+")"
				self.func_assembly.append(ass_code)
	
	def Save_sp(self):
		# self.sp_off - self.var_in_sp_off[ori_sym]
		# ass_code = "\tlw\ts0,"+ str(self.sp_off-4) +"(sp)"
		# self.func_assembly.append(ass_code)
		ass_code = "\tlw\tra,0(sp)"
		self.func_assembly.append(ass_code)
		ass_code = "\taddi\tsp,sp,"+ str(self.sp_off)
		self.func_assembly.append(ass_code)

	# 返回语句
	def Ret_insn(self, insn,ass_list):
		# print("debug riscv 350",insn.insn)
		# Save global var
		self.Save_global_var()
		if self.var_register['func ret'] == 'a0':
			self.Save_sp()
			ass_list.append("\tret")
			return
		self.Reset_reg('a0')
		# Save sp register
		self.Save_sp()
		# func ret 位置
		
		fun_ret_reg = self.var_register['func ret']
		ass_code = "\tmv\ta0,"+fun_ret_reg
		ass_list.append(ass_code)
		ass_list.append("\tret")

	# 操作指令
	def Op_insn(self, insn, ass_list):
		
		# op1_reg = self.Ret_reg_by_sym(insn.op1)
		# op2_reg = self.Ret_reg_by_sym(insn.op2)
		op1_reg = None
		op2_reg = None
		op0_reg = self.Ret_reg_by_sym(insn.op0)
		
		ass_code = "\t"
		if insn.insn[0] in OPERATOR:
			op = OPERATOR[insn.insn[0]]
			# 常数赋值
			if insn.insn[2].isdigit() and insn.insn[3].isdigit():
				op1_reg = insn.insn[2] + insn.insn[3]
				op1_reg = ops[insn.insn[0]](int(insn.insn[2]), int(insn.insn[3]))
				ass_code += "li" +"\t"+op0_reg+","+str(op1_reg)
			elif insn.insn[2].isdigit() or insn.insn[3].isdigit():
				if insn.insn[2].isdigit():
					op1_reg = insn.insn[2]
					constant_reg = self.Get_alive_reg()
					ass_code += "li\t"+constant_reg+","+op1_reg+"\n"
					op1_reg = constant_reg
					op2_reg = self.Ret_reg_by_sym(insn.op2)
				else:
					op2_reg = insn.insn[3]
					constant_reg = self.Get_alive_reg()
					ass_code += "li\t"+constant_reg+","+op2_reg+"\n"
					op2_reg = constant_reg
					op1_reg = self.Ret_reg_by_sym(insn.op1)
				# 
				ass_code += "\t"+op +"\t"+op0_reg+","+op1_reg+","+op2_reg
				
			else:
				# print("debug riscv 430",insn.op1,insn.op2)
				op1_reg = self.Ret_reg_by_sym(insn.op1)
				op2_reg = self.Ret_reg_by_sym(insn.op2)
				# print("debug riscv 433",op1_reg,op2_reg)
				ass_code += op +"\t"+op0_reg+","+op1_reg+","+op2_reg
			ass_code += "\t\t #"+ str(insn.insn)
			ass_list.append(ass_code)
			# 
		elif insn.insn[0] in COMP:
			
			op = insn.insn[0]
			if insn.insn[2].isdigit() or insn.insn[3].isdigit():
				if insn.insn[2].isdigit():
					op1_reg = insn.insn[2]
					constant_reg = self.Get_alive_reg()
					ass_code += "li\t"+constant_reg+","+op1_reg+"\n\t"
					op1_reg = constant_reg
					op2_reg = self.Ret_reg_by_sym(insn.op2)
				else:
					op2_reg = insn.insn[3]
					constant_reg = self.Get_alive_reg()
					ass_code += "li\t"+constant_reg+","+op2_reg+"\n\t"
					op2_reg = constant_reg
					op1_reg = self.Ret_reg_by_sym(insn.op1)
			else:
				op1_reg = self.Ret_reg_by_sym(insn.op1)
				op2_reg = self.Ret_reg_by_sym(insn.op2)
				# op0_reg = self.Ret_reg_by_sym(insn.op0)
			
			if op == '<':
				ass_code += "slt\t"+op0_reg+","+op1_reg+","+op2_reg+"\n"
			elif op == '<=':
				ass_code += "sgt\t"+op0_reg+","+op1_reg+","+op2_reg+"\n"
				ass_code += "\txori\t"+op0_reg + ","+op0_reg+",1"+"\n"
			elif op == '>':
				ass_code += "sgt\t"+op0_reg+","+op1_reg+","+op2_reg+"\n"
			elif op == '>=':
				ass_code += "slt\t"+op0_reg+","+op1_reg+","+op2_reg+"\n"
				ass_code += "\txori\t"+op0_reg + ","+op0_reg+",1"+"\n"
			elif op == '!=':
				ass_code += "sub\t"+op0_reg+","+op1_reg+","+op2_reg+"\n"
				ass_code += "\tsnez\t"+op0_reg + ","+op0_reg+"\n"
			elif op == '==':
				ass_code += "sub\t"+op0_reg+","+op1_reg+","+op2_reg+"\n"
				ass_code += "\tseqz\t"+op0_reg + ","+op0_reg+"\n"
			# ass_code += op +"\t"+op0_reg+","+op1_reg+","+op2_reg
			ass_code += "\tandi\t"+op0_reg+","+op0_reg+",0xff"
			ass_code += "\t\t #"+ str(insn.insn)
			ass_list.append(ass_code)
			# 
		# 保存变量值
		self.Save_var_in_sp(insn.op0)
		# 进行运算的是全局变量？需要记录
		if insn.op0 in self.global_var_dict:
			# print("debug riscv 508",insn.op0)
			self.global_var_dict[insn.op0]['has_edit'] = True

	# 赋值处理
	def Assign(self,insn,ass_list):
		# print("debug riscv 440",insn.insn)
		# print("debug riscv 440",insn.op0, insn.op1)
		# 
		op1 = insn.op1
		op0 = insn.op0
		# 操作数1和操作数2相同
		if op1 == op0:
			return
		# 函数返回值
		if insn.op1 == "fun ret":
			
			op0_reg = self.Ret_reg_by_sym(insn.op0)
			ass_code = ass_code = "\tmv\t"+op0_reg+",a0"
			self.var_register['fun ret'] = 'a0'
			self.register_var['a0'] = 'fun ret'
		# elif insn.op0 == 'args temp':
		# 	
		# 赋值的是数字
		elif insn.insn[2].isdigit():
			op1_reg = insn.insn[2]
			op0_reg = self.Ret_reg_by_sym(insn.op0)
			ass_code = "\tli\t"+op0_reg+","+op1_reg
		else:
			
			op1_reg = self.Ret_reg_by_sym(insn.op1)
			op0_reg = self.Ret_reg_by_sym(insn.op0)
			ass_code = "\tmv\t"+op0_reg+","+op1_reg
		ass_code += "\t\t #"+str(insn.insn)
		ass_list.append(ass_code)
		# 被赋值的是全局变量
		if op0 in self.global_var_dict:
			# print("debug riscv 508",op0)
			self.global_var_dict[op0]['has_edit'] = True
		# 保存被赋值变量的值
		self.Save_var_in_sp(op0)