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
		# 记录循环中的break跳转代码块
		self.breakto = None

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
			self.fun_symbol_dict[func_sym]['sym_type'] = 'fun_args'
		for sym in func_d["var_pool"]:
			# print("debug Passes 45",func_d["var_pool"][sym])
			func_sym = sym
			func_sym_type = func_d["var_pool"][sym]["type"]
			self.fun_symbol_dict[func_sym] = {"symbol":func_sym,"type":func_sym_type,"index":0}
			self.fun_symbol_dict[func_sym]['sym_type'] = 'fun_var'
			if 'init_value' in func_d["var_pool"][sym]:
				self.fun_symbol_dict[func_sym]['init_value'] = func_d["var_pool"][sym]["init_value"]

	# 检查未定义的symbol
	def CheckNode(self,node):
		for cnode in node.children:
			self.CheckNode(cnode)
		if node.type == "identifier":
			if node.key not in self.fun_symbol_dict:
				if node.key not in self.global_var_dict:
					exit("Symbol "+node.key+" Undefined!")
		if node.type == 'FunctionCall':
			if(node.children[0].key not in self.fun_pool):
				exit("Function "+node.children[0].key+" Undefined!")

	# 检查未定义的symbol
	def UnDifinedSymbol(self,func_d):
		for node in func_d["node"].children[3].children:
			self.CheckNode(node)

	#　一些初始化
	def FunInit(self,func):
		# 循环中的break列表清空
		self.breakto = []
		# 函数 insn 流清零
		self.fun_insn_stream = []
		# 函数代码块清零
		self.func_code_block_index = 1 if self.func_code_block_index==0 else self.func_code_block_index+1
		# print(self.fun_pool[func]["type"])
		func_type = self.fun_pool[func]["type"]
		if func_type == "T_void":
			return
		func_ret_symbol = "func ret"
		self.fun_symbol_dict[func_ret_symbol] = {"symbol":func_ret_symbol,"type":func_type,"index":0}
		# 添加 temp符号
		func_ret_symbol = "op temp"
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
			return symbol+"_" + str(self.fun_symbol_dict[symbol]["index"])
		elif symbol in self.global_var_dict:
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
		if node.key == "FunctionCall":
			return self.Deal_functionCall(node)
		elif len(node.children):
			left = self.OpNode(node.children[0],insn,root_symbol)
			right = self.OpNode(node.children[1],insn,root_symbol)
			op_type = node.key
			symbol = self.Symbol(root_symbol)
			insn_temp = [op_type,symbol,left,right]
			Op_insn = Insn(insn_temp)
			Op_insn.insn_type = 'Operation'
			Op_insn.op0 = root_symbol
			Op_insn.op1 = left.split("_")[0]
			Op_insn.op2 = right.split("_")[0]

			self.fun_insn_stream.append(Op_insn)
			node.children = []
			node.key = symbol
			return node.key
		else:
			# print("node children",node.key)
			symbol = self.SymbolNow(node.key)
			return symbol


	# 赋值节点
	def Deal_Assign_node(self,node):
		Assign_insn = None
		symbol = node.children[0].children[0].key
		op_node = node.children[0].children[1]
		# print(node.children[0].key,node.children[0].type)

		right = self.OpNode(op_node,Assign_insn,symbol)
		symbol_1 = self.SymbolNow(symbol)
		symbol = self.Symbol(symbol)
		insn_temp = []
		assign_insn = None
		if node.children[0].type  != '=':
			insn_temp = [node.children[0].type,symbol,symbol_1,right]
			assign_insn = Insn(insn_temp)
			assign_insn.insn_type = "Operation"
			assign_insn.op1 = symbol_1.split("_")[0]
			assign_insn.op2 = right.split("_")[0]
			# print("Passes debug 181",insn_temp,node.children[0].children[0].key)
		else:
			insn_temp = ["=",symbol,right]
			assign_insn = Insn(insn_temp)
			assign_insn.insn_type = "assign"
			assign_insn.op1 = right.split("_")[0]
		# assign_insn = Insn(insn_temp)
		assign_insn.op0 = node.children[0].children[0].key

		self.fun_insn_stream.append(assign_insn)
		node.trans_flag = 1


	# 处理 条件 节点
	def Condi_Node(self,node):
		if 'if condi' not in self.fun_symbol_dict:
			self.fun_symbol_dict["if condi"] = {"symbol":"if condi","type":'T_int',"index":0}
		condi_sym = self.OpNode(node,None,"if condi")
		return condi_sym

	# For 节点
	def Deal_For(self, node):
		# for 代码块开始
		# for 的初始化处理
		self.Node_2_IR(node.children[0])
		# for 代码块
		for_block_index = self.Block_index()
		code_bb = [for_block_index + ":"]
		code_bb_insn_temp = Insn(code_bb) 
		code_bb_insn_temp.insn_type = "code_block"
		self.fun_insn_stream.append(code_bb_insn_temp)
		# 条件
		for_condi = self.Condi_Node(node.children[1].children[0])
		func_code_block_index = self.Block_index()
		# 添加循环出口代码块
		self.breakto.append(func_code_block_index)
		if len(node.children[3].children):
			insn_temp = ["beqz",for_condi,func_code_block_index]
			j_insn_temp = Insn(insn_temp)
			j_insn_temp.op0 = for_condi.split("_")[0]
			j_insn_temp.insn_type = "condi_jump"
			self.fun_insn_stream.append(j_insn_temp)
			# for 的行为语句
			self.Node_2_IR(node.children[-1])
			# for 的自增节点
			self.Node_2_IR(node.children[2])
			# for 代码块结束，跳至for代码块开头
			j_to_out = ["b",for_block_index]
			j_to_out_insn_temp = Insn(j_to_out)
			j_to_out_insn_temp.insn_type = "jump"
			self.fun_insn_stream.append(j_to_out_insn_temp)
		# 下一个代码块
		if func_code_block_index in self.breakto:
			self.breakto.remove(func_code_block_index)
		code_bb = [func_code_block_index + ":"]
		code_bb_insn_temp = Insn(code_bb) 
		code_bb_insn_temp.insn_type = "code_block"
		self.fun_insn_stream.append(code_bb_insn_temp)

	# while节点
	def Deal_while(self,node):
		# while 代码块开始
		while_block_index = self.Block_index()
		code_bb = [while_block_index + ":"]
		code_bb_insn_temp = Insn(code_bb) 
		code_bb_insn_temp.insn_type = "code_block"
		self.fun_insn_stream.append(code_bb_insn_temp)
		# 开始判断
		while_condi = self.Condi_Node(node.children[0].children[0])
		func_code_block_index = self.Block_index()
		# 添加循环出口代码块
		self.breakto.append(func_code_block_index)
		if node.children[-1].key == "True":
			insn_temp = ["beqz",while_condi,func_code_block_index]
			j_insn_temp = Insn(insn_temp)
			j_insn_temp.op0 = while_condi.split("_")[0]
			j_insn_temp.insn_type = "condi_jump"
			self.fun_insn_stream.append(j_insn_temp)
			self.Node_2_IR(node.children[-1])
			# while代码块结束，跳转至while代码块开头
			j_to_out = ["b",while_block_index]
			j_to_out_insn_temp = Insn(j_to_out)
			j_to_out_insn_temp.insn_type = "jump"
			self.fun_insn_stream.append(j_to_out_insn_temp)
		# 下一个代码块
		if func_code_block_index in self.breakto:
			self.breakto.remove(func_code_block_index)
		code_bb = [func_code_block_index + ":"]
		code_bb_insn_temp = Insn(code_bb) 
		code_bb_insn_temp.insn_type = "code_block"
		self.fun_insn_stream.append(code_bb_insn_temp)

	# if节点
	def Deal_if(self,node,root_node):
		if_condi = self.Condi_Node(node.children[0].children[0])
		func_code_block_index = self.Block_index()
		has_else = False
		has_else_if = False
		node_index = root_node.children.index(node)
		else_block = None
		# 存在 else 分支
		# print(root_node.key,len(root_node.children),node_index)
		if len(root_node.children) > node_index+1:
			if root_node.children[node_index + 1].key in ["False"]:
				has_else = True
				else_block = self.Block_index()
		# 存在 if-else 分支
		if len(root_node.children) > node_index+1:
			if root_node.children[node_index + 1].key in ["Else_if"]:
				has_else_if = True
				else_block = self.Block_index()
		if node.children[-1].key == "True":
			# func_code_block_index = self.Block_index()
			insn_temp = ["beqz",if_condi,func_code_block_index]
			if has_else or has_else_if:
				insn_temp[2] = else_block
			j_insn_temp = Insn(insn_temp)
			j_insn_temp.op0 = if_condi.split("_")[0]
			j_insn_temp.insn_type = "condi_jump"
			self.fun_insn_stream.append(j_insn_temp)
			self.Node_2_IR(node.children[-1])
			# True 分支最后跳至if后的节点
			j_to_out = ["b",func_code_block_index]
			j_to_out_insn_temp = Insn(j_to_out)
			j_to_out_insn_temp.insn_type = "jump"
			self.fun_insn_stream.append(j_to_out_insn_temp)
		node.trans_flag = 1
		while has_else_if:
			has_else_if = False
			node = root_node.children[node_index + 1]
			node_index += 1 
			# 代码块标号
			code_bb = [else_block + ":"]
			code_bb_insn_temp = Insn(code_bb) 
			code_bb_insn_temp.insn_type = "code_block"
			self.fun_insn_stream.append(code_bb_insn_temp)
			# 存在 else 分支
			if len(root_node.children) > node_index+1:
				if root_node.children[node_index + 1].key in ["False"]:
					has_else = True
					else_block = self.Block_index()
			# 存在 if-else 分支
			if len(root_node.children) > node_index+1:
				if root_node.children[node_index + 1].key in ["Else_if"]:
					has_else_if = True
					else_block = self.Block_index()
			# 条件节点
			if_condi = self.Condi_Node(node.children[0].children[0])
			insn_temp = ["beqz",if_condi,func_code_block_index]
			# 是否存在 else / else-if
			if has_else or has_else_if:
				insn_temp[2] = else_block
			j_insn_temp = Insn(insn_temp)
			j_insn_temp.op0 = if_condi.split("_")[0]
			j_insn_temp.insn_type = "condi_jump"
			self.fun_insn_stream.append(j_insn_temp)
			# 解析当前节点的语句
			self.Node_2_IR(node.children[-1])
			j_to_out = ["b",func_code_block_index]
			j_to_out_insn_temp = Insn(j_to_out)
			j_to_out_insn_temp.insn_type = "jump"
			self.fun_insn_stream.append(j_to_out_insn_temp)
		# 存在 else 吗？
		if has_else:
			code_bb = [else_block + ":"]
			code_bb_insn_temp = Insn(code_bb) 
			code_bb_insn_temp.insn_type = "code_block"
			self.fun_insn_stream.append(code_bb_insn_temp)
			node = root_node.children[node_index + 1]
			self.Node_2_IR(node)
		code_bb = [func_code_block_index + ":"]
		code_bb_insn_temp = Insn(code_bb) 
		code_bb_insn_temp.insn_type = "code_block"
		self.fun_insn_stream.append(code_bb_insn_temp)

	# 函数调用
	def Deal_functionCall(self,node):
		# 先验证参数个数
		func_name = node.children[0].key
		if len(node.children[1].children) != len(self.fun_pool[func_name]['args']):
			exit("Wrong number of function parameters")
		funars = []
		for args_node in node.children[1].children:
			# print(args_node.key)
			args_symbol_temp =self.OpNode(args_node,None,"op temp")
			# print(args_symbol_temp)
			args_symbol = self.Symbol("op temp")
			funars.append(args_symbol)
			insn_temp = ["=",args_symbol,args_symbol_temp]
			ret_insn_temp = Insn(insn_temp)
			ret_insn_temp.insn_type = "assign"
			self.fun_insn_stream.append(ret_insn_temp)
		for args_temp in funars:
			insn_temp = ["=","args temp_"+str(funars.index(args_temp)),args_temp]
			insn_temp = Insn(insn_temp)
			insn_temp.insn_type = "assign"
			self.fun_insn_stream.append(insn_temp)
		func_call = ["call",func_name]
		func_call_temp = Insn(func_call)
		func_call_temp.insn_type = "FunctionCall"
		self.fun_insn_stream.append(func_call_temp)
		if self.fun_pool[func_name]['type'] != 'T_void':
			# print("debug 279",self.fun_pool[func_name]['type'])
			return func_name+" ret"

	def Node_2_IR(self,root_node):
		for node in root_node.children:
			# print(node.key)
			# 当前节点已经翻译完毕
			if node.trans_flag:
				continue
			# 赋值节点
			if node.key == "Assign":
				self.Deal_Assign_node(node)
			# 遇到return节点
			elif node.key == 'return':
				ret_node = node.children[0]
				ret_symbol_temp = self.OpNode(ret_node,None,"func ret")
				ret_symbol = self.Symbol("func ret")
				insn_temp = ["=",ret_symbol,ret_symbol_temp]
				ret_insn_temp = Insn(insn_temp)
				ret_insn_temp.op0 = "func ret"
				ret_insn_temp.op1 = ret_symbol_temp.split("_")[0]
				ret_insn_temp.insn_type = "assign"
				self.fun_insn_stream.append(ret_insn_temp)
				insn_temp = ["return",ret_symbol]
				ret_insn = Insn(insn_temp)
				ret_insn.insn_type = "return"
				self.fun_insn_stream.append(ret_insn)
				node.trans_flag = 1
			# 遇到if节点
			elif node.key in ['if']:
				self.Deal_if(node,root_node)
			# 遇到while节点
			elif node.key == 'while':
				self.Deal_while(node)
			# 遇到break
			elif node.key == "break": 
				if len(self.breakto):
					breakout = self.breakto.pop()
					j_to_out = ["b",breakout]
					j_to_out_insn_temp = Insn(j_to_out)
					j_to_out_insn_temp.insn_type = "jump"
					self.fun_insn_stream.append(j_to_out_insn_temp)
				else:
					exit("'break' jump error!")
			# for 节点
			elif node.key == "For":
				self.Deal_For(node)
			elif node.key == "FunctionCall":
				self.Deal_functionCall(node)
				

	def FunIteration(self):
		for func in self.fun_pool:
			print(func)
			# 函数符号初始化
			self.FunSymbolInit(self.fun_pool[func])
			self.fun_pool[func]['fun_symbol_dict'] = self.fun_symbol_dict
			print(self.fun_pool[func])
			# 检查函数是否用到了未定义的符号
			# print(self.fun_pool[func]["node"].children[-1].key)
			if self.fun_pool[func]["node"].children[-1].key == 'Stmt':
				self.UnDifinedSymbol(self.fun_pool[func])
			# 一些初始化
			self.FunInit(func)
			if self.fun_pool[func]["node"].children[-1].key == 'Stmt':
				self.Node_2_IR(self.fun_pool[func]["node"].children[3])
			self.Fun_insn_print()
			self.fun_pool[func]["insn"] = self.fun_insn_stream           
			print("Func exit")
			# print(self.fun_pool[func])

	# 主函数
	def main(self):
		# 全局符号
		self.GlobalSymbolInit()
		self.FunIteration()