# from graphviz import Digraph
import graphviz
import os
# os.environ["PATH"] += os.pathsep + 'E:/Graphviz/bin'
os.environ["PATH"] += os.pathsep + 'G:/Graphviz/bin'
dot = graphviz.Digraph(comment='root')

def dot_exam():
	# g = Digraph('G',filename = 'hello.gv')
	dot = graphviz.Digraph(comment='The Round Table')
	dot.node('A', 'King Arthur')
	dot.node('B', 'Sir Bedevere the Wise')
	dot.node('L', 'Sir Lancelot the Brave')
	dot.edges(['AB', 'AL'])
	dot.edge('B', 'L', constraint='false')
	# g.view()
	print(dot.source)
	# doctest_mark_exe()
	# dot.render('doctest-output/round-table.gv').replace('\\', '/')
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
		print(dot.source)
		# dot.render('round-table.gv', view=True)
		dot.render('round-table.gv')

class Parse(object):
	def __init__(self,l_stream):
		self.tstack = []
		self.grammar_tree = Tree('root')
		self.tokens = l_stream
		self.dot_num = 0

	# 是变量声明语句
	def VarDeclaration(self,index):
		# VarDeclaration 节点
		state_tree = Tree('VarDeclaration')
		state_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.type = self.tokens[index].type
		self.grammar_tree.add_child(state_tree)
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
			if self.tokens[index].value == 'main':
				return index
			if self.tokens[index].type == 'T_semicolon':
				return index
			elif self.tokens[index].type == 'T_identifier':
				# 被声明的变量标识符节点，比如 a,ch[]
				var_name = self.tokens[index].value
				if self.tokens[index+1].type == 'T_l2_bracket':
					arr_var = ''
					while index < len(self.tokens) and self.tokens[index].type != 'T_r2_bracket':
						# print(self.tokens[index].value)
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
	def FuncDeclaration(self,index):
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
		self.grammar_tree.add_child(state_tree)
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
		# while index <len(self.tokens):
		# 	# 遇到了右括号 ')' 结束参数匹配
		# 	if self.tokens[index].type == 'T_r1_bracket':
		# 		break
		return index

	def retTokenType(self,index):
		# type 为类型关键字？很可能是变量声明或者函数声明
		if self.tokens[index].type == 'T_int' or self.tokens[index].type == 'T_char' or self.tokens[index].type == 'T_void':
			retType = 'VarDeclaration'
			index_tmp = index
			index_tmp += 1
			if self.tokens[index_tmp].type == 'T_identifier':
				if self.tokens[index_tmp+1].type == 'T_l1_bracket':
					retType = 'FuncDeclaration'
			return retType

	def parse(self):
		index = 0
		while index < len(self.tokens):
			# print(self.tokens[index].type,self.tokens[index].value)
			if self.tokens[index].value == 'main':
				return
			# 遇到了类型token，很可能是一个变量声明
			if self.retTokenType(index) == 'VarDeclaration':
				index = self.VarDeclaration(index)
			elif self.retTokenType(index) == 'FuncDeclaration':
				index = self.FuncDeclaration(index)
			# self.tstack.append(self.tokens[index])
			else:
				index += 1

	def drawTree(self):
		self.grammar_tree.Print_tree(self.grammar_tree)
		# dot(self.grammar_tree)

