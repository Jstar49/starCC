
"""
# 最困难的是寄存器分配，必须好好思量
"""
import copy
A_RRGISTER = ['a7','a6','a5','a4','a3','a2','a1','a0']

class Riscv(object):
	"""docstring for Assembly"""
	def __init__(self, passes):
		self.fun_pool = passes.fun_pool
		self.outputAss = []
		self.register = None
		self.a_register = None
		self.var_register = None
		self.register_var = None
		self.var_in_sp_off = None

	# 主函数
	def main(self):
		for func in self.fun_pool:
			# 初始的寄存器分配, 返回sp的偏移量
			sp_off = self.Reg_init(func)
			# 根据IR生成汇编代码
			ass = self.IR2Assemble(self.fun_pool[func]['insn'],sp_off)
			self.PrintAssemble(ass)

	# 函数寄存器分配--初始化
	def Reg_init(self,func):
		print("debug riscv 28", self.fun_pool[func]['fun_symbol_dict'])
		# 函数符号对象
		fun_sym = self.fun_pool[func]['fun_symbol_dict']
		# A系列寄存器备份
		self.a_register = copy.deepcopy(A_RRGISTER)
		self.var_register = {}
		self.register_var = {}
		# 变量在sp中的偏移
		self.var_in_sp_off = {}
		sp_off = 0
		for sym in fun_sym:
			self.var_in_sp_off[sym] = sp_off
			sp_off += 4
			# 函数参数
			if 'sym_type' in fun_sym[sym] and fun_sym[sym]['sym_type'] == 'fun_args':
				arg_reg = self.a_register.pop()
				self.var_register[sym] = arg_reg
				self.register_var[arg_reg] = sym
			# 函数内局部变量
			elif 'sym_type' in fun_sym[sym] and fun_sym[sym]['sym_type'] == 'fun_var':
				self.var_register[sym] = None

		print("debug riscv 51", sp_off)
		print("debug riscv 51", self.var_in_sp_off)
		return sp_off + 4

	def PrintAssemble(self, ass_list):
		for code in ass_list:
			print(code)


	def IR2Assemble(self, insn_stream, sp_off):
		func_assembly = []
		for insn in insn_stream:
			if insn.insn_type == 'func_head':
				func_assembly.append(insn.insn[0])
				# sp,s0寄存器初始化
				self.Fun_sp_init(func_assembly,sp_off)
			elif insn.insn_type == 'return':
				self.Ret_insn(insn, func_assembly)
			elif insn.insn_type == 'Operation':
				self.Op_insn(insn, func_assembly)
		return func_assembly

	# 函数sp寄存器初始化
	def Fun_sp_init(self,ass_list,sp_off):
		ass_list.append("\taddi\tsp,sp,-"+str(sp_off))
		ass_list.append("\tsw\ts0,"+str(sp_off-4)+"(sp)")
		ass_list.append("\taddi\ts0,sp,"+str(sp_off))

	def Ret_insn(self, insn,ass_list):
		ass_list.append("\tret")

	def Op_insn(self, insn, ass_list):
		print(insn.insn)
		print(insn.op0,insn.op1,insn.op2)