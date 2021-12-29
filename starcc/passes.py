"""
生成中间代码
"""

class Insn(object):
	def __init__(self):
		self.next = None
		self.prev = None
		self.insn_type = None


class Passes(object):
	"""docstring for Passes"""
	def __init__(self, check):
		super(Passes, self).__init__()
		self.parse_tree = check.parse.grammar_tree
		self.var_pool = check.var_pool
		self.fun_pool = check.fun_pool
		self.symbol_dict = {}
		self.fun_symbol_dict = {}

	# 用 insn 数据流保存中间代码

	# 验证符号池，禁止未声明的变量使用
	def FunSymbolInit(self,func_d):
		# print(func_d)
		self.fun_symbol_dict = {}
		for sym in func_d["args"]:
			func_sym = func_d["args"][sym]["arg_symbol"]
			func_sym_type = func_d["args"][sym]["arg_type"]
			self.fun_symbol_dict[func_sym] = {"symbol":func_sym,"type":func_sym_type,"index":0}
		for sym in func_d["var_pool"]:
			# print(sym)
			func_sym = sym
			func_sym_type = func_d["var_pool"][sym]["type"]
			self.fun_symbol_dict[func_sym] = {"symbol":func_sym,"type":func_sym_type,"index":0}
		print("fun_symbol_dict",self.fun_symbol_dict)


	# 符号迭代,传入符号 var_temp,返回该符号的下一次计数,var_temp_n
	# 从标号0开始,但标号0禁止使用

	# 返回符号index
	def Symbol(self,symbol):
		if symbol in self.symbol_dict:
			self.symbol_dict[symbol]["index"] += 1
			return symbol + str(self.symbol_dict[symbol]["index"])
		self.symbol_dict[symbol] = {"index":0}
		self.symbol_dict[symbol]["index"] += 1
		return symbol + str(self.symbol_dict[symbol]["index"])

	# 节点运算
	def OpNode(self,node,insn,root_symbol):
		"""
		# node：节点
		# insn：父insn
		# root_symbol：所属符号
		"""
		# print(node.key)
		if len(node.children):
			left = node.children[0].key
			right = node.children[1].key
			if len(node.children[0].children):
				left = self.OpNode(node.children[0],insn,root_symbol)
			if len(node.children[1].children):
				right = self.OpNode(node.children[1],insn,root_symbol)
			op_type = node.key
			symbol = self.Symbol(root_symbol)
			print(op_type,symbol,left,right)
			node.children = []
			node.key = symbol
		return node.key



	def Node_2_IR(self,root_node):
		for node in root_node.children:
			if node.key == "Assign":
				Assign_insn = Insn()
				symbol = node.children[0].children[0].key
				op_node = node.children[0].children[1]
				right = self.OpNode(op_node,Assign_insn,symbol)
				# self.Assign(node)
				symbol = self.Symbol(symbol)
				print("=",symbol,right)

	def FunIteration(self):
		for func in self.fun_pool:
			# print(self.fun_pool[func]["node"].key)
			self.FunSymbolInit(self.fun_pool[func])
			self.Node_2_IR(self.fun_pool[func]["node"].children[3])

	# 主函数
	def main(self):
		self.FunIteration()