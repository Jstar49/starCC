"""
拿到语法树之后先进行符号切割；
切割成:
	全局变量符号, global a, b, c....
	函数符号, funa, funb, func....
对于有定义的函数进行分割:
	函数参数符号, funa:arg1, funa:arg2 ....
	函数局部变量, funa:x1, funa:x2, funa:x3 ....

分别保存到符号池和变量池中。
"""
class Check(object):
	"""docstring for Check"""
	def __init__(self, parse):
		super(Check, self).__init__()
		self.parse = parse
		self.var_pool = {}

	def Print(self,root_node):
		for node in root_node.children:
			print(node.key)
			self.Print(node)

	def CheckVarDeclaration(self,root_node):
		print(root_node.key)
		varDec_list = []
		for node in root_node.children:
			if node.key == 'VarDeclaration':
				print(node.key)
				# root_node.children.remove(node)
				varDec_list.append(node)
				varDec_Node = node
				# print(varDec_Node.children[0].key)
				var_type = varDec_Node.children[0].key
				varDec_Node.children.remove(varDec_Node.children[0])
				# print(varDec_Node.children[0].key)
				for iden_node in varDec_Node.children[0].children:
					print(iden_node.key)
					iden = iden_node.key
					if iden_node.key == 'Assign':
						iden = iden_node.children[0].children[0].key
					self.var_pool[iden] = {"type":var_type}
				continue
			self.CheckVarDeclaration(node)
		for node in varDec_list:
			root_node.children.remove(node)

	def main(self):
		# for node in self.parse.grammar_tree.children:
		self.CheckVarDeclaration(self.parse.grammar_tree)
		# self.Print(self.parse.grammar_tree)
		print(self.var_pool)