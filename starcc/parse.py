# from graphviz import Digraph
import graphviz
import os

# os.environ["PATH"] += os.pathsep + 'E:/Graphviz/bin'
# os.environ["PATH"] += os.pathsep + 'G:/Graphviz/bin'
dot = graphviz.Digraph(comment='root')

operator_priority = {
	'=':9,
	'T_add':10,
	'T_sub':10,
	'T_mul':20,
	'T_div':20,
}

def dot_exam():
	dot = graphviz.Digraph(comment='The Round Table')
	dot.node('A', 'King Arthur')
	dot.node('B', 'Sir Bedevere the Wise')
	dot.node('L', 'Sir Lancelot the Brave')
	dot.edges(['AB', 'AL'])
	dot.edge('B', 'L', constraint='false')
	print(dot.source)
	dot.render('round-table.gv', view=True)


class Tree(object):
	def __init__(self,key):
		self.key = key
		self.dot_num = None
		self.token = None
		self.children = []
		self.father = None
		# self.dot = None
		if self.key == 'Statement':
			self.type = None

	def add_child(self,node):
		self.children.append(node)
		node.father = self

	def dot_tree_in(self,gram_node,father_node):
		dot.node(str(gram_node.dot_num),gram_node.key)
		dot.edge(str(father_node.dot_num),str(gram_node.dot_num))
		for i in gram_node.children:
			self.dot_tree_in(i,gram_node)

	def Print_tree(self,gram_node):
		dot.node(str(gram_node.dot_num),gram_node.key)
		for i in gram_node.children:
			self.dot_tree_in(i,gram_node)
		# print(dot.source)
		# dot.render('round-table.gv', view=True)
		dot.render('round-table.gv')

class Parse(object):
	def __init__(self,l_stream):
		self.tstack = []
		self.grammar_tree = Tree('root')
		self.tokens = l_stream
		self.dot_num = 0

	# 是变量声明语句
	def VarDeclaration(self,index,gram_root):
		# VarDeclaration 节点
		state_tree = Tree('VarDeclaration')
		state_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.type = self.tokens[index].type
		gram_root.add_child(state_tree)
		# VarDeclaration 节点的左孩子,一个 Type 节点, 记录声明的变量的类型
		type_tree = Tree(self.tokens[index].type)
		type_tree.token = self.tokens[index]
		type_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.add_child(type_tree)
		index += 1
		# VarDeclaration 节点的右孩子，标识符节点
		iden_tree = Tree("Identifier")
		iden_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.add_child(iden_tree)
		while index < len(self.tokens):
			# 遇到了 ';',声明终止
			if self.tokens[index].type == 'T_semicolon':
				return index
			elif self.tokens[index].type == 'T_identifier':
				# 被声明的变量标识符节点，比如 a,ch[]
				var_name = self.tokens[index].value
				if self.tokens[index+1].type == 'T_l2_bracket':
					arr_var = ''
					while index < len(self.tokens) and self.tokens[index].type != 'T_r2_bracket':
						arr_var += self.tokens[index].value
						index += 1
					arr_var += self.tokens[index].value
					var_name = arr_var
				var_tree = Tree(var_name)
				var_tree.dot_num = self.dot_num
				self.dot_num += 1
				iden_tree.add_child(var_tree)
				index += 1
				# 被声明的变量被赋予了初始值
				if self.tokens[index].type == "T_assign":
					index += 1
					if self.tokens[index].type == 'T_quote':
						index += 1
						value_tree = Tree(self.tokens[index].value)
						value_tree.dot_num = self.dot_num
						self.dot_num += 1
						var_tree.add_child(value_tree)
						index += 1
					else:
						# print(self.tokens[index].value)
						# 变量初值节点
						value_tree = Tree(self.tokens[index].value)
						value_tree.dot_num = self.dot_num
						self.dot_num += 1
						var_tree.add_child(value_tree)
						index += 1
			else:
				index += 1

	# 函数声明语句
	def FuncDeclaration(self,index,gram_root):
		'''
		# 两种类型的函数声明 :
		# Type identifier(args);
		# Type identifier(args){stmt;}
		'''
		# FuncDeclaration 节点
		state_tree = Tree('FuncDeclaration')
		state_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.type = self.tokens[index].type
		gram_root.add_child(state_tree)
		# FuncDeclaration 节点的左孩子,一个 Type 节点, 记录声明的变量的类型
		type_tree = Tree(self.tokens[index].type)
		type_tree.token = self.tokens[index]
		type_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.add_child(type_tree)
		index += 1
		# FuncDeclaration 节点的右孩子，标识符节点
		iden_tree = Tree("Identifier")
		iden_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.add_child(iden_tree)
		# 函数名节点
		iden_value_tree = Tree(self.tokens[index].value)
		iden_value_tree.dot_num = self.dot_num
		self.dot_num += 1
		iden_tree.add_child(iden_value_tree)
		# 添加参数节点 args
		args_tree = Tree("Args")
		args_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.add_child(args_tree)
		index += 1
		while index <len(self.tokens):
			# 遇到了右括号 ')' 结束参数匹配
			if self.tokens[index].type == 'T_r1_bracket':
				break
			elif self.tokens[index].type == 'T_int' or self.tokens[index].type == 'T_char':
				# 函数参数节点
				arg_tree = Tree("arg")
				arg_tree.dot_num = self.dot_num
				self.dot_num += 1
				args_tree.add_child(arg_tree)
				# 函数参数Type节点
				arg_type_tree = Tree(self.tokens[index].type)
				arg_type_tree.dot_num = self.dot_num
				self.dot_num += 1
				arg_tree.add_child(arg_type_tree)
				# 函数参数修饰符节点
				index += 1
				var_name = self.tokens[index].value
				# 参数是数组
				if self.tokens[index+1].type == 'T_l2_bracket':
					# print(self.tokens[index].value)
					arr_var = ''
					while index < len(self.tokens) and self.tokens[index].type != 'T_r2_bracket':
						# print(self.tokens[index].value)
						arr_var += self.tokens[index].value
						index += 1
					arr_var += self.tokens[index].value
					var_name = arr_var
				arg_iden_tree = Tree(var_name)
				arg_iden_tree.dot_num = self.dot_num
				self.dot_num += 1
				arg_tree.add_child(arg_iden_tree)
				index += 1
			else:
				index += 1
		index += 1
		# 遇到 '{' ,该函数声明有代码块
		if self.tokens[index].type == 'T_l3_braket':
			# print("block")
			block_tree = Tree("Stmt")
			block_tree.dot_num = self.dot_num
			self.dot_num += 1
			state_tree.add_child(block_tree)
			index = self.parse(index,block_tree)
		index += 1
		return index

	# 语句中的迭代
	def analyse_deeply(self,stmt_syntax_list,gram_root):
		print(stmt_syntax_list)
		stmt_list = stmt_syntax_list.pop(0)
		op_node = Tree(self.tokens[stmt_list[2]].value)
		op_node.dot_num = self.dot_num
		self.dot_num += 1
		iden_node = Tree(self.tokens[stmt_list[2]+1].value)
		iden_node.dot_num = self.dot_num
		self.dot_num += 1
		if operator_priority[stmt_list[0]] >= operator_priority[stmt_syntax_list[0][0]]:
			op_node.add_child(gram_root)
			op_node.add_child(iden_node)
			return op_node
		else:
			# stmt_syntax_list.pop(0)
			# op_node.add_child(gram_root)
			op_node.add_child(self.analyse_deeply(stmt_syntax_list,iden_node))
			if stmt_list[0] == '=':
				return op_node
			else:
				op_node.add_child(gram_root)
		return op_node
		
	# 语句
	def Statemet(self,index,gram_root):
		# 不是 iden | constant | ++ | -- ,语法错误
		if not (self.tokens[index].type == 'T_identifier' or self.tokens[index].type == 'T_constant' or\
			self.tokens[index].type == 'T_addadd' or self.tokens[index].type == 'T_subsub'):
			exit("Syntax error : '"+self.tokens[index-2].value+self.tokens[index-1].value+self.tokens[index].value+"'")
		# 这是一个函数调用
		if self.tokens[index].type == 'T_l1_bracket':
			pass
		stmt_syntax_list =[]
		tmp = ['=',self.tokens[index].type,index]
		stmt_syntax_list.append(tmp)
		index_tmp = index+1
		while self.tokens[index_tmp].type != 'T_semicolon' and self.tokens[index_tmp].type != 'T_comma' \
			and index_tmp < len(self.tokens):
			# print(self.tokens[index_tmp].value)
			tmp = [self.tokens[index_tmp].type,self.tokens[index_tmp+1].type,index_tmp]
			stmt_syntax_list.append(tmp)
			index_tmp += 2
		print(stmt_syntax_list)
		gram_root.add_child(self.analyse_deeply(stmt_syntax_list,gram_root))
		# state_tree = Tree("Statemet")
		# state_tree.dot_num = self.dot_num
		# self.dot_num += 1
		# gram_root.add_child(state_tree)
		return index+1

	# 标识符
	def Identifier(self,index,gram_root):
		iden_tree = Tree(self.tokens[index].value)
		iden_tree.dot_num = self.dot_num
		self.dot_num += 1
		iden_tree.token = self.tokens[index]
		gram_root.add_child(iden_tree)
		index += 1
		return index

	# 赋值语句
	def Assign(self,index,gram_root):
		# 赋值语句根节点
		assign_tree = Tree("Assign")
		assign_tree.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(assign_tree)
		# 被赋值符的节点
		iden_tree = Tree(self.tokens[index].value)
		iden_tree.dot_num = self.dot_num
		self.dot_num += 1
		iden_tree.token = self.tokens[index]
		index += 1
		# '='节点
		assign_char_tree = Tree(self.tokens[index].value)
		assign_char_tree.dot_num = self.dot_num
		self.dot_num += 1
		assign_tree.add_child(assign_char_tree)
		assign_char_tree.add_child(iden_tree)
		index += 1
		index = self.Statemet(index,assign_char_tree)
		return index

	# 函数调用
	def FunctionCall(self,index,gram_root):
		# 函数调用节点
		funcall_tree = Tree("FunctionCall")
		funcall_tree.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(funcall_tree)
		# 被调用的函数节点
		func_name_tree = Tree(self.tokens[index].value)
		func_name_tree.dot_num = self.dot_num
		self.dot_num += 1
		funcall_tree.add_child(func_name_tree)
		index += 1
		# 函数调用参数节点
		func_arg_tree = Tree("fun_call_arg")
		func_arg_tree.dot_num = self.dot_num
		self.dot_num += 1
		funcall_tree.add_child(func_arg_tree)
		# print(self.tokens[index].value)
		fun_braket = []
		fun_braket.append(self.tokens[index])
		index += 1
		while index < len(self.tokens):
			if self.tokens[index].type == 'T_l1_bracket':
				fun_braket.append(self.tokens[index])
			elif self.tokens[index].type == 'T_r1_bracket':
				# print("pop")
				fun_braket.pop()
				if len(fun_braket) == 0:
					# print("0")
					break
			if self.tokens[index].type == 'T_identifier':
				index = self.parse(index,func_arg_tree)
			else:
				index += 1
		index += 1
		return index

	# 返回接下来的token句型
	def retTokenType(self,index):
		# type 为类型关键字？很可能是变量声明或者函数声明
		if self.tokens[index].type == 'T_int' or self.tokens[index].type == 'T_char' or self.tokens[index].type == 'T_void':
			retType = 'VarDeclaration'
			index_tmp = index
			index_tmp += 1
			# 'Type inden'
			if self.tokens[index_tmp].type == 'T_identifier':
				# 'Type inden(' 大概率是函数
				if self.tokens[index_tmp+1].type == 'T_l1_bracket':
					retType = 'FuncDeclaration'
			return retType
		# type 为标识符,分为多种情况
		elif self.tokens[index].type == 'T_identifier':
			retType =  'Stmt'
			# 'iden(*' ,归为函数调用
			if self.tokens[index+1].type == 'T_l1_bracket':
				retType = 'FunctionCall'
			# 'iden,*' 归为普通的语句
			elif self.tokens[index+1].type == 'T_comma' or self.tokens[index+1].type == 'T_r1_bracket':
				# print('line 288',self.tokens[index+1].value)
				retType = 'Identifier'
			# 'iden = *',赋值语句
			elif self.tokens[index+1].type == 'T_assign':
				retType = 'Assign'
			return retType
		elif self.tokens[index].type == 'T_constant':
			return 'Constant'

	def parse(self,index_init,gram_root):
		index = index_init
		while index < len(self.tokens):
			# print(self.tokens[index].type,self.tokens[index].value)
			if self.tokens[index].type == 'T_r3_braket':
				return index
			# 遇到了类型token，很可能是一个变量声明
			if self.retTokenType(index) == 'VarDeclaration':
				index = self.VarDeclaration(index,gram_root)
			# 也有可能是函数定义捏
			elif self.retTokenType(index) == 'FuncDeclaration':
				index = self.FuncDeclaration(index,gram_root)
			# 修饰符开头？首先考虑是一条语句
			elif self.retTokenType(index) == 'Stmt':
				index = self.Statemet(index,gram_root)
			# 也有可能是函数调用捏
			elif self.retTokenType(index) == 'FunctionCall':
				index = self.FunctionCall(index,gram_root)
				# break
			# 一个简单的修饰符罢了
			elif self.retTokenType(index) == 'Identifier':
				index = self.Identifier(index,gram_root)
				break
			# 赋值语句
			elif self.retTokenType(index) == 'Assign':
				index = self.Assign(index,gram_root)
			else:
				index += 1
		return index

	def main(self):
		index = self.parse(0,self.grammar_tree)

	def printhello(self):
		print("hello world")

	def drawTree(self):
		self.grammar_tree.Print_tree(self.grammar_tree)
		# dot(self.grammar_tree)

