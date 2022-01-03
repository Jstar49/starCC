"""
生成中间代码
"""

class Insn(object):
	def __init__(self,insn):
		self.next = None
		self.prev = None
		self.insn_type = None
		self.insn = insn

class Passes(object):
	"""docstring for Passes"""
	def __init__(self, check):
		super(Passes, self).__init__()
		self.parse_tree = check.parse.grammar_tree
		self.global_var_pool = check.global_var_pool
		self.global_var_dict = {}
		self.fun_pool = check.fun_pool
		self.symbol_dict = {}
		self.fun_symbol_dict = {}
		self.fun_insn_stream = []
		# 用于记录函数的代码块
		self.func_code_block_index = 0

	# 用 insn 数据流保存中间代码

	# 初始化全局变量
	def GlobalSymbolInit(self):
		for sym in self.global_var_pool:
			global_sym = sym
			global_sym_type = self.global_var_pool[sym]["type"]
			self.global_var_dict[global_sym] = {"symbol":global_sym,"type":global_sym_type,"index":0}
	# 初始化函数内定义的符号
	def FunSymbolInit(self,func_d):
		self.fun_symbol_dict = {}
		for sym in func_d["args"]:
			func_sym = func_d["args"][sym]["arg_symbol"]
			func_sym_type = func_d["args"][sym]["arg_type"]
			self.fun_symbol_dict[func_sym] = {"symbol":func_sym,"type":func_sym_type,"index":0}
		for sym in func_d["var_pool"]:
			func_sym = sym
			func_sym_type = func_d["var_pool"][sym]["type"]
			self.fun_symbol_dict[func_sym] = {"symbol":func_sym,"type":func_sym_type,"index":0}
		# print("fun_symbol_dict",self.fun_symbol_dict)

	# 检查未定义的symbol
	def CheckNode(self,node):
		for cnode in node.children:
			# print(cnode.key)
			self.CheckNode(cnode)
		if node.type == "identifier":
			# print(node.key)
			if node.key not in self.fun_symbol_dict:
				if node.key not in self.global_var_dict:
					exit("Symbol "+node.key+" Undefined!")

	# 检查未定义的symbol
	def UnDifinedSymbol(self,func_d):
		for node in func_d["node"].children[3].children:
			self.CheckNode(node)

	#　一些初始化
	def FunInit(self,func):
		# 函数 insn 流清零
		self.fun_insn_stream = []
		# 函数代码块清零
		self.func_code_block_index = 1
		# print(self.fun_pool[func]["type"])
		func_type = self.fun_pool[func]["type"]
		if func_type == "T_void":
			return
		func_ret_symbol = "func ret"
		self.fun_symbol_dict[func_ret_symbol] = {"symbol":func_ret_symbol,"type":func_type,"index":0}
		# 添加函数头
		func_head = [func + ":"]
		func_head_insn_temp = Insn(func_head)
		func_head_insn_temp.insn_type = "func_head"
		self.fun_insn_stream.append(func_head_insn_temp)
		# 第一个代码块
		func_first_code_bb = ["func block "+ str(self.func_code_block_index) + ":"]
		func_bb_insn_temp = Insn(func_first_code_bb)
		func_bb_insn_temp.insn_type = "code_block"
		self.fun_insn_stream.append(func_bb_insn_temp)

	# 输出 FUNC insn
	def Fun_insn_print(self):
		for insn in self.fun_insn_stream:
			if insn.insn_type in ["func_head","code_block"]:
				print(insn.insn)
			else:
				print("\t",insn.insn)

	# 符号迭代,传入符号 var_temp,返回该符号的下一次计数,var_temp_n
	# 从标号0开始,但标号0禁止使用

	# 返回符号index + 1
	def Symbol(self,symbol):
		if symbol in self.fun_symbol_dict:
			self.fun_symbol_dict[symbol]["index"] += 1
			return symbol+"_" + str(self.fun_symbol_dict[symbol]["index"])
		elif symbol in self.global_var_dict:
			self.global_var_dict[symbol]["index"] += 1
			return symbol+"_" + str(self.global_var_dict[symbol]["index"])

	# 返回符合 index
	def SymbolNow(self,symbol):
		if symbol in self.fun_symbol_dict:
			# self.fun_symbol_dict[symbol]["index"] += 1
			return symbol+"_" + str(self.fun_symbol_dict[symbol]["index"])
		elif symbol in self.global_var_dict:
			# self.global_var_dict[symbol]["index"] += 1
			return symbol+"_" + str(self.global_var_dict[symbol]["index"])
		elif symbol.isdigit():
			return symbol

	# 返回 block 的下一个index
	def Block_index(self):
		self.func_code_block_index += 1
		return "func block "+ str(self.func_code_block_index)

	# 节点运算
	def OpNode(self,node,insn,root_symbol):
		"""
		# node：节点
		# insn：父insn
		# root_symbol：所属符号
		"""
		# print(node.key)
		if len(node.children):
			left = self.OpNode(node.children[0],insn,root_symbol)
			# if len(node.children[1].children):
			right = self.OpNode(node.children[1],insn,root_symbol)
			op_type = node.key
			symbol = self.Symbol(root_symbol)
			insn_temp = [op_type,symbol,left,right]
			# print(insn_temp)
			Op_insn = Insn(insn_temp)
			self.fun_insn_stream.append(Op_insn)
			node.children = []
			node.key = symbol
			return node.key
		else:
			# print("node children",node.key)
			symbol = self.SymbolNow(node.key)
			return symbol

	# 处理 if 节点
	def Condi_Node(self,node):
		if 'if condi' not in self.fun_symbol_dict:
			self.fun_symbol_dict["if condi"] = {"symbol":"if condi","type":'T_int',"index":0}
		condi_sym = self.OpNode(node,None,"if condi")
		# print(condi_sym)
		return condi_sym

	def Node_2_IR(self,root_node):
		for node in root_node.children:
			# print(node.key)
			if node.trans_flag:
				continue
			if node.key == "Assign":
				# Assign_insn = Insn()
				Assign_insn = None
				symbol = node.children[0].children[0].key
				op_node = node.children[0].children[1]
				right = self.OpNode(op_node,Assign_insn,symbol)
				# self.Assign(node)
				symbol = self.Symbol(symbol)
				insn_temp = ["=",symbol,right]
				assign_insn = Insn(insn_temp)
				self.fun_insn_stream.append(assign_insn)
				# print(insn_temp)
				node.trans_flag = 1
			elif node.key == 'return':
				ret_node = node.children[0]
				ret_symbol_temp = self.OpNode(ret_node,None,"func ret")
				ret_symbol = self.Symbol("func ret")
				# print(ret_symbol)
				insn_temp = ["=",ret_symbol,ret_symbol_temp]
				ret_insn_temp = Insn(insn_temp)
				self.fun_insn_stream.append(ret_insn_temp)
				insn_temp = ["return",ret_symbol]
				ret_insn = Insn(insn_temp)
				self.fun_insn_stream.append(ret_insn)
				node.trans_flag = 1
			elif node.key == 'if':
				if_condi = self.Condi_Node(node.children[0].children[0])
				func_code_block_index = self.Block_index()
				has_else = False
				node_index = root_node.children.index(node)
				else_block = None
				# 存在 else 分支
				# print(root_node.key,len(root_node.children),node_index)
				if len(root_node.children) > node_index+1:
					if root_node.children[node_index + 1].key == "False":
						has_else = True
						else_block = self.Block_index()
				if node.children[-1].key == "True":
					# func_code_block_index = self.Block_index()
					insn_temp = ["beqz",if_condi,func_code_block_index]
					if has_else:
						insn_temp[2] = else_block
					j_insn_temp = Insn(insn_temp)
					j_insn_temp.insn_type = "condi_jump"
					self.fun_insn_stream.append(j_insn_temp)
					self.Node_2_IR(node.children[-1])
					# True 分支最后跳至if后的节点
					j_to_out = ["b",func_code_block_index]
					j_to_out_insn_temp = Insn(j_to_out)
					self.fun_insn_stream.append(j_to_out_insn_temp)
				node.trans_flag = 1
				if has_else:
					code_bb = [else_block + ":"]
					code_bb_insn_temp = Insn(code_bb) 
					code_bb_insn_temp.insn_type = "code_block"
					self.fun_insn_stream.append(code_bb_insn_temp)
					# print("False")
					node = root_node.children[node_index + 1]
					# print(node.key)
					self.Node_2_IR(node)
				code_bb = [func_code_block_index + ":"]
				code_bb_insn_temp = Insn(code_bb) 
				code_bb_insn_temp.insn_type = "code_block"
				self.fun_insn_stream.append(code_bb_insn_temp)

	def FunIteration(self):
		for func in self.fun_pool:
			print(func)
			# 函数符号初始化
			self.FunSymbolInit(self.fun_pool[func])
			print(self.fun_symbol_dict)
			# 检查函数是否用到了未定义的符号
			self.UnDifinedSymbol(self.fun_pool[func])
			# 一些初始化
			self.FunInit(func)
			self.Node_2_IR(self.fun_pool[func]["node"].children[3])
			self.Fun_insn_print()
			print("Func exit")

	# 主函数
	def main(self):
		# 全局符号
		self.GlobalSymbolInit()
		self.FunIteration()