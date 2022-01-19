
"""
# 最困难的是寄存器分配，必须好好思量
"""
import copy
# A_RRGISTER = ['a7','a6','a5','a4','a3','a2','a1','a0']
A_RRGISTER = ['a4','a3','a2','a1','a0']


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
	def main(self):
		# 输出文件
		self.outFile = open("test.s","w")
		for func in self.fun_pool:
			# 函数局部变量
			self.fun_symbol_dict = self.fun_pool[func]['fun_symbol_dict']
			# func_assembly = []
			# 初始的寄存器分配, 返回sp的偏移量
			self.sp_off = self.Reg_init(func)
			
			# 根据IR生成汇编代码
			self.IR2Assemble(self.fun_pool[func]['insn'],self.func_assembly,self.sp_off)
		
		self.PrintAssemble(self.func_assembly)
		# 关闭文件
		self.outFile.close()

	# 函数寄存器分配--初始化
	def Reg_init(self,func):
		print("debug riscv 28", self.fun_pool[func]['fun_symbol_dict'])
		# 函数符号对象
		fun_sym = self.fun_pool[func]['fun_symbol_dict']
		# A系列寄存器备份
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

		print("debug riscv 51", sp_off)
		print("debug riscv 51", self.var_in_sp_off)
		return sp_off + 4

	# 输出
	def PrintAssemble(self, ass_list):
		for code in ass_list:
			# print(code)
			self.outFile.write(code+"\n")


	def IR2Assemble(self, insn_stream, func_assembly,sp_off):
		for insn in insn_stream:
			# 遇到函数头
			if insn.insn_type == 'func_head':
				func_assembly.append(insn.insn[0])
				# sp,s0寄存器初始化
				self.Fun_sp_init(func_assembly,sp_off)
			elif insn.insn_type == 'return':
				self.Ret_insn(insn, func_assembly)
			elif insn.insn_type == 'Operation':
				self.Op_insn(insn, func_assembly)

	# 函数sp寄存器初始化
	def Fun_sp_init(self,ass_list,sp_off):
		ass_list.append("\taddi\tsp,sp,-"+str(sp_off))
		ass_list.append("\tsw\ts0,"+str(sp_off-4)+"(sp)")
		ass_list.append("\taddi\ts0,sp,"+str(sp_off))
		print("debug riscv 84",self.fun_symbol_dict)
		# 保存参数
		for fun_sym in self.fun_symbol_dict:
			# 函数参数
			if "sym_type" in self.fun_symbol_dict[fun_sym] and \
					self.fun_symbol_dict[fun_sym]['sym_type'] == 'fun_args':
				ass_code = "\tsw\t"+self.var_register[fun_sym]+","
				off_ = sp_off - self.var_in_sp_off[fun_sym]
				ass_code += str(-off_)+"(s0)"
				ass_code += "\t\t #"+fun_sym
				ass_list.append(ass_code)
				# reg = self.var_register[fun_sym]
				# self.register_var[reg] = None
				# self.var_register[fun_sym] = None
				# self.a_register.append(reg)
			# 函数内有初始化的变量
			if "sym_type" in self.fun_symbol_dict[fun_sym] and \
					self.fun_symbol_dict[fun_sym]['sym_type'] == 'fun_var' and \
				'init_value' in self.fun_symbol_dict[fun_sym]:
				ass_code = "\tli\t"
				# reg = self.a_register.pop()
				reg = self.Ret_reg_by_sym(fun_sym)
				ass_code += reg + ","+self.fun_symbol_dict[fun_sym]['init_value']
				ass_list.append(ass_code)
				
				ass_code = "\tsw\t"+reg+","
				off_ = sp_off - self.var_in_sp_off[fun_sym]
				ass_code += str(-off_)+"(s0)"
				ass_code += "\t\t #"+fun_sym
				ass_list.append(ass_code)
		print("debug riscv 103", self.a_register)

	# 保存寄存器中的值
	def Save_reg(self,reg_num):
		ori_sym = self.register_var[reg_num]
		ass_code = "\tsw\t"+reg_num+","
		off_ = self.sp_off - self.var_in_sp_off[ori_sym]
		ass_code += str(-off_)+"(s0)"
		ass_code += "\t\t #"+ori_sym
		self.func_assembly.append(ass_code)

	# 根据符号取出可用的寄存器
	def Ret_reg_by_sym(self,symbol):
		# print("debug riscv 137", symbol,self.var_register[symbol])
		# 是否在var_register中 
		if symbol in self.var_register:
			# 暂时没有映射关系
			if self.var_register[symbol] == None:
				# print("debug riscv 144", symbol)
				reg = None
				if len(self.a_register):
					reg = self.a_register.pop()
				else:
					print("debug riscv 147")
					reg = self.reg_used.pop(0)
					# 保存原来寄存器中の值
					self.Save_reg(reg)
				self.var_register[symbol] = reg
				self.register_var[reg] = symbol
				self.reg_used.append(reg)
				# exit(0)
				return reg
			# 已存在映射关系
			else:
				# reg重新上色
				print("debug riscv 167",self.reg_used,self.var_register[symbol])
				self.reg_used.remove(self.var_register[symbol])
				self.reg_used.append(self.var_register[symbol])
				return self.var_register[symbol]
		# 否则视为全局变量
		else:
			pass

	def Ret_insn(self, insn,ass_list):
		ass_list.append("\tret")



	# 操作指令
	def Op_insn(self, insn, ass_list):
		OPERATOR = {'+':'add','-':'sub','*':'mul','/':'div'}
		# print("debug riscv 124", self.a_register)
		# print("debug riscv 125", self.var_register)
		print("debug riscv 181", insn.insn, insn.op0, insn.op1, insn.op2)
		op1_reg = self.Ret_reg_by_sym(insn.op1)
		op2_reg = self.Ret_reg_by_sym(insn.op2)
		op0_reg = self.Ret_reg_by_sym(insn.op0)
		print("debug riscv 185", op1_reg, op2_reg, op0_reg)
		ass_code = "\t"
		op = OPERATOR[insn.insn[0]]
		ass_code += op +"\t"+op0_reg+","+op1_reg+","+op2_reg
		ass_code += "\t\t #"+ str(insn.insn)
		ass_list.append(ass_code)
		# print(insn.op0,insn.op1,insn.op2)