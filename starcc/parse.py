# from graphviz import Digraph
import graphviz
import os

# os.environ["PATH"] += os.pathsep + 'E:/Graphviz/bin'
# os.environ["PATH"] += os.pathsep + 'G:/Graphviz/bin'
dot = graphviz.Digraph(comment='root',format='png')

operator_priority = {
	'==':6,
	'!=':6,
	'&&':7,
	'||':7,
	'>':8,
	'>=':8,
	'<':8,
	'<=':8,
	'=':9,
	'&':10,
	'|':10,
	'+':10,
	'-':10,
	'*':20,
	'/':20,
}

class Tree(object):
	def __init__(self,key):
		self.key = key
		self.dot_num = None
		self.token = None
		self.children = []
		self.father = None
		# self.dot = None
		self.type = None
		self.trans_flag = 0

	def add_child(self,node):
		self.children.append(node)
		node.father = self

	def dot_tree_in(self,gram_node,father_node):
		dot.node(str(gram_node.dot_num),gram_node.key)
		dot.edge(str(father_node.dot_num),str(gram_node.dot_num))
		for i in gram_node.children:
			self.dot_tree_in(i,gram_node)

	def Print_tree(self,gram_node,file_name):

		dot.node(str(gram_node.dot_num),gram_node.key)
		for i in gram_node.children:
			self.dot_tree_in(i,gram_node)
		dot.render(file_name + '.gv')

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
			if self.tokens[index].type == 'T_semicolon':
				return index
			elif self.tokens[index].type == 'T_identifier':
				index = self.parse(index,iden_tree)
			elif self.tokens[index].type == 'T_comma':
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
					# 
					arr_var = ''
					while index < len(self.tokens) and self.tokens[index].type != 'T_r2_bracket':
						# 
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
			# 
			block_tree = Tree("Stmt")
			block_tree.dot_num = self.dot_num
			self.dot_num += 1
			state_tree.add_child(block_tree)
			# index += 1
			# 
			fun_braket = []
			fun_braket.append(self.tokens[index])
			index += 1
			while index < len(self.tokens):
				if self.tokens[index].type == 'T_r3_braket':
					fun_braket.pop()
					if len(fun_braket) == 0:
						break
				index = self.parse(index,block_tree)
		return index

	# 默认语句
	def Statemet(self,index,gram_root):
		stmt_list = []
		stmt_list_tree = []
		index_tmp = index
		while self.tokens[index_tmp].type != 'T_semicolon' and self.tokens[index_tmp].type != 'T_comma' \
			and self.tokens[index_tmp].type != 'T_r1_bracket'and index_tmp < len(self.tokens):
			if self.tokens[index_tmp+1].type == 'T_l1_bracket' and self.tokens[index_tmp].type == 'T_identifier':
				funcall_tree,index_tmp = self.FunctionCall(index_tmp)
				stmt_list_tree.append(funcall_tree)
			# '+|-|*|/(' 优先运算
			elif self.tokens[index_tmp].type == 'T_l1_bracket' and self.tokens[index_tmp-1].type != 'T_identifier':
				block_tree,index_tmp = self.Statemet(index_tmp+1,gram_root)
				stmt_list_tree.append(block_tree)
				while self.tokens[index_tmp].type != 'T_r1_bracket':
					index_tmp+=1
				index_tmp += 1
			else:
				stmt_list.append(self.tokens[index_tmp].value)
				stmts_tree = Tree(self.tokens[index_tmp].value)
				stmts_tree.dot_num = self.dot_num
				self.dot_num += 1
				stmt_list_tree.append(stmts_tree)
				if self.tokens[index_tmp].type == 'T_identifier':
					stmts_tree.type = 'identifier'
				index_tmp += 1
		while len(stmt_list_tree)>2:
			max_op = -2
			i = len(stmt_list_tree) - 2
			while i >0:
				if operator_priority[stmt_list_tree[i].key] > operator_priority[stmt_list_tree[max_op].key]:
					max_op = i
				i -= 2
			right_tree = stmt_list_tree[max_op+1]
			op_tree = stmt_list_tree[max_op]
			left_tree = stmt_list_tree[max_op-1]
			op_tree.add_child(left_tree)
			op_tree.add_child(right_tree)
			stmt_list_tree.remove(right_tree)
			stmt_list_tree.remove(left_tree)
		ret_node = stmt_list_tree.pop()
		return ret_node,index_tmp
	
	# 标识符
	def Identifier(self,index,gram_root):
		# 
		iden_tree = Tree(self.tokens[index].value)
		iden_tree.dot_num = self.dot_num
		self.dot_num += 1
		iden_tree.token = self.tokens[index]
		iden_tree.type = "identifier"
		gram_root.add_child(iden_tree)
		index += 1
		return index

	# 常数
	def Constant(self,index,gram_root):
		# 
		constant_tree = Tree(self.tokens[index].value)
		constant_tree.dot_num = self.dot_num
		self.dot_num += 1
		constant_tree.token = self.tokens[index]
		constant_tree.type = "constant"
		gram_root.add_child(constant_tree)
		index += 1
		return index

	# 字符串
	def IsString(self,index,gram_root):
		# string_node = Tree()
		# 
		string_value = self.tokens[index].value
		index += 1
		string_value += self.tokens[index].value
		index += 1
		string_value += self.tokens[index].value
		# 
		string_node = Tree(string_value)
		string_node.dot_num = self.dot_num
		string_node.type = "string"
		self.dot_num += 1
		gram_root.add_child(string_node)
		index += 1
		return index

	# Return 语句
	def Return(self,index,gram_root):
		ret_node = Tree(self.tokens[index].value)
		ret_node.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(ret_node)
		index_tmp = index + 1
		index = self.parse(index_tmp,ret_node)
		return index + 1

	# Break
	def Break(self,index,gram_root):
		break_node = Tree(self.tokens[index].value)
		break_node.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(break_node)
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
		iden_tree.type = "identifier"
		index += 1
		# '='节点
		assign_char_tree = Tree(self.tokens[index].value)
		assign_char_tree.dot_num = self.dot_num
		assign_char_tree.type = {'T_add_assign':'+','T_sub_assign':'-',\
		'T_mul_assign':'*','T_div_assign':'/','T_assign':'='}[self.tokens[index].type]
		self.dot_num += 1
		assign_tree.add_child(assign_char_tree)
		assign_char_tree.add_child(iden_tree)
		index += 1
		ret_node,index = self.Statemet(index,assign_char_tree)
		assign_char_tree.add_child(ret_node)
		return index

	# 函数调用
	def FunctionCall(self,index):
		# 函数调用节点
		funcall_tree = Tree("FunctionCall")
		funcall_tree.dot_num = self.dot_num
		funcall_tree.type = 'FunctionCall'
		self.dot_num += 1
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
		fun_braket = []
		fun_braket.append(self.tokens[index])
		index += 1
		while index < len(self.tokens):
			# 
			if self.tokens[index].type == 'T_l1_bracket':
				fun_braket.append(self.tokens[index])
			elif self.tokens[index].type == 'T_r1_bracket':
				fun_braket.pop()
				if len(fun_braket) == 0:
					index += 1
					break
			if self.tokens[index].type != 'T_comma':
				# 
				index = self.parse(index,func_arg_tree)
			else:
				index += 1
		return funcall_tree, index

	# If 语句
	def If(self,index,gram_root):
		if_tree = Tree(self.tokens[index].value)
		if_tree.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(if_tree)
		# 条件节点
		condition_node = Tree("Condition")
		condition_node.dot_num = self.dot_num
		self.dot_num += 1
		if_tree.add_child(condition_node)
		index+= 2
		index = self.parse(index,condition_node)
		index += 1
		if self.tokens[index].type == 'T_semicolon':
			return index+1
		if_braket = []
		if_braket.append(self.tokens[index])
		index += 1
		# 条件为True的节点
		if_true_node = Tree("True")
		if_true_node.dot_num = self.dot_num
		self.dot_num += 1
		if_tree.add_child(if_true_node)
		# 
		while index <len(self.tokens):
			if self.tokens[index].type == 'T_l3_braket':
				if_braket.append(self.tokens[index])
			elif self.tokens[index].type == 'T_r3_braket':
				if_braket.pop()
				if len(if_braket) == 0:
					index += 1
					break
			index = self.parse(index,if_true_node)
		# 
		if self.tokens[index].type == 'T_else' and self.tokens[index+1].type == 'T_if':
			while self.tokens[index].type == 'T_else' and self.tokens[index+1].type == 'T_if':
				else_if_node = Tree("Else_if")
				else_if_node.dot_num = self.dot_num
				self.dot_num += 1
				gram_root.add_child(else_if_node)
				condition_node = Tree("Condition")
				condition_node.dot_num = self.dot_num
				self.dot_num += 1
				else_if_node.add_child(condition_node)
				index+= 3
				index = self.parse(index,condition_node)
				index += 1
				if self.tokens[index].type == 'T_semicolon':
					return index+1
				if_braket = []
				if_braket.append(self.tokens[index])
				index += 1
				# 条件为True的节点
				if_true_node = Tree("True")
				if_true_node.dot_num = self.dot_num
				self.dot_num += 1
				else_if_node.add_child(if_true_node)
				while index <len(self.tokens):
					if self.tokens[index].type == 'T_l3_braket':
						if_braket.append(self.tokens[index])
					elif self.tokens[index].type == 'T_r3_braket':
						if_braket.pop()
						if len(if_braket) == 0:
							index += 1
							break
					index = self.parse(index,if_true_node)
		if self.tokens[index].type == 'T_else':
			if_false_node = Tree("False")
			if_false_node.dot_num = self.dot_num
			self.dot_num += 1
			gram_root.add_child(if_false_node)
			index += 1
			if_braket = []
			if_braket.append(self.tokens[index])
			index += 1
			while index <len(self.tokens):
				if self.tokens[index].type == 'T_l3_braket':
					if_braket.append(self.tokens[index])
				elif self.tokens[index].type == 'T_r3_braket':
					if_braket.pop()
					if len(if_braket) == 0:
						index += 1
						break
				index = self.parse(index,if_false_node)
		return index

	# while 节点
	def While(self,index,gram_root):
		while_node = Tree(self.tokens[index].value)
		while_node.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(while_node)
		# 条件节点
		condition_node = Tree("Condition")
		condition_node.dot_num = self.dot_num
		self.dot_num += 1
		while_node.add_child(condition_node)
		index += 2
		index = self.parse(index,condition_node)
		index += 1
		if self.tokens[index].type == 'T_semicolon':
			return index+1
		while_braket = []
		while_braket.append(self.tokens[index])
		index += 1
		# 条件为True的节点
		while_true_node = Tree("True")
		while_true_node.dot_num = self.dot_num
		self.dot_num += 1
		while_node.add_child(while_true_node)
		while index <len(self.tokens):
			if self.tokens[index].type == 'T_l3_braket':
				while_braket.append(self.tokens[index])
			elif self.tokens[index].type == 'T_r3_braket':
				while_braket.pop()
				if len(while_braket) == 0:
					index += 1
					break
			index = self.parse(index,while_true_node)
		return index

	# for节点
	def For(self,index,gram_root):
		# for节点
		for_node = Tree("For")
		for_node.dot_num = self.dot_num
		self.dot_num += 1
		gram_root.add_child(for_node)
		index+=2
		# for 的初始化
		for_init_node = Tree("for_init")
		for_init_node.dot_num = self.dot_num
		self.dot_num += 1
		for_node.add_child(for_init_node)
		while(self.tokens[index].type !='T_semicolon'):
			index = self.parse(index,for_init_node)
		index += 1
		# for 节点的条件Node
		condition_node = Tree("Condition")
		condition_node.dot_num = self.dot_num
		self.dot_num += 1
		for_node.add_child(condition_node)
		while(self.tokens[index].type !='T_semicolon'):
			index = self.parse(index,condition_node)
		index += 1
		# for增量Node
		add_node = Tree("For_add")
		add_node.dot_num = self.dot_num
		self.dot_num += 1
		for_node.add_child(add_node)
		while(self.tokens[index].type !='T_r1_bracket'):
			index = self.parse(index,add_node)
		index += 1
		# for 行为node
		stmt_node = Tree("Stmt")
		stmt_node.dot_num = self.dot_num
		self.dot_num += 1
		for_node.add_child(stmt_node)
		if self.tokens[index].type == 'T_semicolon':
			return index+1
		for_braket = []
		for_braket.append(self.tokens[index])
		index += 1
		while index <len(self.tokens):
			if self.tokens[index].type == 'T_l3_braket':
				for_braket.append(self.tokens[index])
			elif self.tokens[index].type == 'T_r3_braket':
				for_braket.pop()
				if len(for_braket) == 0:
					index += 1
					break
			index = self.parse(index,stmt_node)
		return index

	# 返回接下来的token句型
	def retTokenType(self,index):
		# type 为类型关键字？很可能是变量声明或者函数声明
		if self.tokens[index].type in ['T_int','T_char','T_void','T_short']:
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
				retType = 'Identifier'
			# 'iden = *',赋值语句
			elif self.tokens[index+1].type in ['T_assign','T_add_assign','T_sub_assign','T_mul_assign','T_div_assign']:
				retType = 'Assign'
			return retType
		# 常数
		elif self.tokens[index].type == 'T_constant':
			if self.tokens[index+1].value in operator_priority:
				return 'Stmt'
			return 'Constant'
		# if
		elif self.tokens[index].type == 'T_if':
			return 'If'
		# while
		elif self.tokens[index].type == 'T_while':
			return 'While'
		# break
		elif self.tokens[index].type == 'T_break':
			return 'Break'
		# for
		elif self.tokens[index].type == 'T_for':
			return 'For'
		elif self.tokens[index].type == 'T_return':
			return 'Return'
		elif self.tokens[index].type == 'T_quote':
			return 'String'

	def parse(self,index_init,gram_root):
		index = index_init
		if self.tokens[index].type == 'T_r3_braket':
			return index+1
		# 遇到了类型token，很可能是一个变量声明
		elif self.retTokenType(index) == 'VarDeclaration':
			index = self.VarDeclaration(index,gram_root)
		# 也有可能是函数定义捏
		elif self.retTokenType(index) == 'FuncDeclaration':
			index = self.FuncDeclaration(index,gram_root)
		# 修饰符开头？首先考虑是一条语句
		elif self.retTokenType(index) == 'Stmt':
			ret_node,index = self.Statemet(index,gram_root)
			gram_root.add_child(ret_node)
		# 也有可能是函数调用捏
		elif self.retTokenType(index) == 'FunctionCall':
			funcall_tree, index = self.FunctionCall(index)
			gram_root.add_child(funcall_tree)
		# 一个简单的修饰符罢了
		elif self.retTokenType(index) == 'Identifier':
			# 
			index = self.Identifier(index,gram_root)
		# 常数
		elif self.retTokenType(index) == 'Constant':
			# 
			index = self.Constant(index,gram_root)
		# 赋值语句
		elif self.retTokenType(index) == 'Assign':
			index = self.Assign(index,gram_root)
		elif self.retTokenType(index) == 'If':
			index = self.If(index,gram_root)
		elif self.retTokenType(index) == 'While':
			index = self.While(index,gram_root)
		elif self.retTokenType(index) == 'Break':
			index = self.Break(index,gram_root)
		elif self.retTokenType(index) == 'For':
			index = self.For(index,gram_root)
		elif self.retTokenType(index) == 'Return':
			index = self.Return(index,gram_root)
		elif self.retTokenType(index) == 'String':
			index = self.IsString(index,gram_root)
		else:
			index += 1
		return index

	def main(self):
		index = 0
		while index < len(self.tokens):
			index = self.parse(index,self.grammar_tree)

	def drawTree(self,gram_node,file_name):
		gram_node.Print_tree(gram_node,file_name)
		# dot(self.grammar_tree)

