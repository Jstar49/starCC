
class Check(object):
	"""docstring for Check"""
	def __init__(self, parse):
		super(Check, self).__init__()
		self.parse = parse
		self.var_pool = {}



	def CheckVarDeclaration(self,root_node):
		print(root_node.key)
		for node in root_node.children:
			if node.key == 'VarDeclaration':
				print(node.key)
				root_node.children.remove(node)
				varDec_Node = node
				# print(varDec_Node.children[0].key)
				var_type = varDec_Node.children[0].key
				varDec_Node.children.remove(varDec_Node.children[0])
				print(varDec_Node.children[0].key)

	def main(self):
		# for node in self.parse.grammar_tree.children:
		self.CheckVarDeclaration(self.parse.grammar_tree)
		print(self.parse.grammar_tree.children)