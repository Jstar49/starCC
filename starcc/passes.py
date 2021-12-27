"""
生成中间代码
"""

class Passes(object):
	"""docstring for Passes"""
	def __init__(self, check):
		super(Passes, self).__init__()
		self.parse_tree = check.parse.grammar_tree
		self.var_pool = check.var_pool
		self.fun_pool = check.fun_pool

	# 用 insn 数据流保存中间代码

	# 验证符号池，禁止未声明的变量使用

	# 符号迭代,传入符号 var_temp,返回该符号的下一次计数,var_temp_n
	# 从标号0开始,但标号0禁止使用

	# 返回操作类型
	def GetOpType(self,node):
		# + 后端需要考虑 add/addi 两种情况，中间代码不需要
		if node.key == "+":
			return "+"
	# 赋值语句
	def Assign(self,node):
		# 3地址形式
		# 目的寄存器
		purpose_reg = node.children[0].children[0].key
		# 操作类型
		operation_type = self.GetOpType(node.children[0].children[1])
		# 操作寄存器1
		operator_reg_left = node.children[0].children[1].children[0].key
		# 操作寄存器2
		operator_reg_right = node.children[0].children[1].children[1].key
		# 操作
		print(purpose_reg,"=",operator_reg_left,operation_type,operator_reg_right)

	def main(self):
		for node in self.parse_tree.children:
			if node.key == "Assign":
				self.Assign(node)

		