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
		self.fun_pool = {}

	def Print(self,root_node):
		for node in root_node.children:
			print(node.key)
			self.Print(node)

	def CheckVarDeclaration(self,root_node,root_key):
		# print(root_node.key)
		varDec_list = []
		for node in root_node.children:
			if node.key == 'VarDeclaration':
				# print(node.key)
				# root_node.children.remove(node)
				varDec_list.append(node)
				varDec_Node = node
				# print(varDec_Node.children[0].key)
				var_type = varDec_Node.children[0].key
				varDec_Node.children.remove(varDec_Node.children[0])
				# print(varDec_Node.children[0].key)
				# 遍历 Identifier 节点
				for iden_node in varDec_Node.children[0].children:
					# print(iden_node.key)
					# 设置变量类型
					iden = iden_node.key
					if iden_node.key == 'Assign':
						iden = iden_node.children[0].children[0].key
					self.var_pool[iden] = {"type":var_type}
					# 是不是有初始值
					if iden_node.key == 'Assign':
						self.var_pool[iden]["init_value"] = iden_node.children[0].children[1].key
					# 设置变量生存范围
					self.var_pool[iden]["SurvivalRange"] = root_key
					if root_key == 'root':
						self.var_pool[iden]["SurvivalRange"] = "global"
				continue
			# self.CheckVarDeclaration(node)
		for node in varDec_list:
			root_node.children.remove(node)

	def CheckFunction(self,root_node):
		for node in root_node.children:
			if node.key == "FuncDeclaration":
				# 函数类型
				func_type = node.children[0].key
				# 函数符合名
				func_name = node.children[1].children[0].key
				# 检查是否有参数
				func_args = {}
				if len(node.children[2].children):
					for arg_node in node.children[2].children:
						arg_name = "arg" + str(node.children[2].children.index(arg_node))
						func_args[arg_name] = {}
						func_args[arg_name]["arg_type"] = arg_node.children[0].key
						func_args[arg_name]["arg_symbol"] = arg_node.children[1].key
				# 将函数加入函数池
				self.fun_pool[func_name] = {"type":func_type,"args":func_args}
				if len(node.children[3].children):
					self.CheckVarDeclaration(node.children[3],func_name)

	def main(self):
		# for node in self.parse.grammar_tree.children:
		# 首先检查全局变量
		self.CheckVarDeclaration(self.parse.grammar_tree,"root")
		# self.Print(self.parse.grammar_tree)
		self.CheckFunction(self.parse.grammar_tree)
		print(self.var_pool)
		print(self.fun_pool)