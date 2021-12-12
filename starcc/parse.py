# from graphviz import Digraph
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'E:/Graphviz/bin'
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

	def statement(self,index):
		state_tree = Tree('Statement')
		state_tree.dot_num = self.dot_num
		self.dot_num += 1
		state_tree.type = self.tokens[index].type
		self.grammar_tree.add_child(state_tree)
		index += 1
		while index < len(self.tokens):
			if self.tokens[index].value == 'main':
				return index
			if self.tokens[index].type == 'T_semicolon':
				return index
			elif self.tokens[index].type == 'T_identifier':
				iden_tree = Tree(self.tokens[index].value)
				iden_tree.dot_num = self.dot_num
				self.dot_num += 1
				state_tree.add_child(iden_tree)
				index += 1
				if self.tokens[index].type == "T_assign":
					index += 1
					print(self.tokens[index].value)
					value_tree = Tree(self.tokens[index].value)
					value_tree.dot_num = self.dot_num
					self.dot_num += 1
					iden_tree.add_child(value_tree)
					index += 1
			else:
				index += 1


	def retTokenType(self,index):
		# type 为类型？很可能是变量声明或者函数声明
		if self.tokens[index].type == 'T_int' or self.tokens[index].type == 'T_char' or self.tokens[index].type == 'T_void':
			if self.tokens[index+1].type == 'T_identifier':
				return 'Statement'

	def parse(self):
		index = 0
		while index < len(self.tokens):
			# print(self.tokens[index].type,self.tokens[index].value)
			if self.tokens[index].value == 'main':
				return
			# 遇到了类型token，很可能是一个变量声明
			if self.retTokenType(index) == 'Statement':
				index = self.statement(index)
			# self.tstack.append(self.tokens[index])
			else:
				index += 1

	def drawTree(self):
		self.grammar_tree.Print_tree(self.grammar_tree)
		# dot(self.grammar_tree)

