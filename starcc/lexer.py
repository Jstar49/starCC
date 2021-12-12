
file_name = ""

# self.source_stream = ""

# 操作符
operatorList = ['+','-','*','/','=','&','|','>','<','>=','<=','++','--','!=','==']
# 特殊符号
specialChar = [	'(',')','[',']','{','}',',',';','\"']
# 关键字
keyWords = [
	'int','double','float','char','void','for','while','if','else','do','return','include'
]

# 关键字,操作符 Token
keyWords_Token = {
	'int':'T_int',
	'char':'T_char',
	'void':'T_void',
	'for':'T_for',
	'while':'T_while',
	'if':'T_if',
	'else':'T_else',
	'do':'T_do',
	'return':'T_return',
	'include':'T_include',
	'+':'T_add',
	'-':'T_sub',
	'*':'T_mul',
	'/':'T_div',
	'=':'T_assign',
	'&':'T_and',
	'|':'T_or',
	'>':'T_gt',
	'<':'T_lt',
	'>=':'T_ge',
	'<=':'T_le',
	'++':'T_addadd',
	'--':'T_subsub',
	'!=':'T_notequal',
	'==':'T_equal',
	'#':'T_sharp',
	'(':'T_l1_bracket',
	')':'T_r1_bracket',
	'[':'T_l2_bracket',
	']':'T_r2_bracket',
	'{':'T_l3_braket',
	'}':'T_r3_braket',
	',':'T_comma',
	';':'T_semicolon',
	'\"':'T_quote'
}
# 其他Token
other_Token = {
	'identifier':'T_identifier',#标识符
	'constant':'T_constant',#常数
	'string':'T_string',#字符串
}


class Token(object):
	'''Token分类'''
	def __init__(self,type_key,value):
		self.value = value
		if type_key in keyWords_Token:
			self.type = keyWords_Token[type_key]
		elif type_key in other_Token:
			self.type = other_Token[type_key]

class Lexer(object):
	'''词法分析'''
	def __init__(self,stream):
		# print("init")
		self.tokens = []
		self.source_stream = stream
		# print(self.source_stream)

	# 跳过一些不需要分析的词法，比如空白字符 & /**/注释
	def If_skip_word(self,index):
		# print("If_skip_word",self.source_stream[index],self.source_stream[index+1])
		# 空白字符
		if self.source_stream[index] == '\n' or self.source_stream[index] == '\t' or \
			self.source_stream[index] == ' ' or self.source_stream[index] == '\r':
			# print("skip",self.source_stream[index])
			index += 1
		# 注释 ,识别 /* */
		if index < len(self.source_stream) and self.source_stream[index] == '/' and self.source_stream[index+1] == '*':
			index_temp = index
			while index_temp < len(self.source_stream):
				if self.source_stream[index_temp] == '*' and self.source_stream[index_temp+1] == '/':
					index_temp += 2
					break
				index_temp +=1
			# print(self.source_stream[index:index_temp])
			# print(self.source_stream[index_temp])
			return index_temp
		return index

	def lexer(self):
		# print("lexer")
		# print(self.source_stream)
		word_num = 0
		while word_num < len(self.source_stream):
			# print(self.source_stream[word_num],self.source_stream[word_num+1])
			# 判断是否为注释或者不需要分析的词法
			word_num = self.If_skip_word(word_num)
			if word_num >= len(self.source_stream):
				break;
			# print(word_num)
			# 是否为引入头文件
			if self.source_stream[word_num] == "#":
				# word_num += 1
				tk_str = self.source_stream[word_num]
				# 收纳 '#'
				self.tokens.append(Token(tk_str,tk_str))
				word_num += 1
				# 匹配 'include'
				if self.source_stream[word_num:word_num+7] == "include":
					tk_str = self.source_stream[word_num:word_num+7]
					self.tokens.append(Token(tk_str,tk_str))
					word_num += 7
					word_num = self.If_skip_word(word_num)
					# 匹配 '\"' 和 '<'
					if self.source_stream[word_num] == '\"' or self.source_stream[word_num] == '<':
						end_char = '\"' if self.source_stream[word_num]=='\"' else '>'
						tk_str = self.source_stream[word_num]
						self.tokens.append(Token(tk_str,tk_str))
						word_num += 1
						tk_str = ''
						while word_num < len(self.source_stream):
							if self.source_stream[word_num] == end_char:
								break
							tk_str += self.source_stream[word_num]
							word_num += 1
						self.tokens.append(Token("identifier",tk_str))
						word_num = self.If_skip_word(word_num)
				else:
					print("Error :'#' must used with 'include'.")
					exit()
			# 是下划线或者字母
			elif self.source_stream[word_num] == "_" or self.source_stream[word_num].isalpha():
				tk_str = ""
				while word_num < len(self.source_stream) and \
					(self.source_stream[word_num].isalpha() or \
					self.source_stream[word_num].isdigit() or \
					self.source_stream[word_num] == '_'):
					tk_str += self.source_stream[word_num]
					word_num += 1
				# print(tk_str)
				if tk_str in keyWords:
					# 识别为关键字,如 int, double ...
					self.tokens.append(Token(tk_str,tk_str))
				else:
					# 识别为标识符,如变量名等
					self.tokens.append(Token("identifier",tk_str))
			# 是数字
			elif self.source_stream[word_num].isdigit():
				tk_str = ''
				while word_num < len(self.source_stream) and self.source_stream[word_num].isdigit():
					tk_str += self.source_stream[word_num]
					word_num += 1
				# 识别为整型常量
				self.tokens.append(Token("constant",tk_str))
			# 是运算符
			elif self.source_stream[word_num] in operatorList:
				# word_num = self.If_skip_word(word_num)
				tk_str = ''
				# ++ | --
				if (self.source_stream[word_num] == '+' or self.source_stream[word_num] == '-') and \
					self.source_stream[word_num] == self.source_stream[word_num+1]:
					tk_str += self.source_stream[word_num]
					tk_str += self.source_stream[word_num+1]
					word_num += 2
					self.tokens.append(Token(tk_str,tk_str))
				# >= | <= 
				elif (self.source_stream[word_num] == '>' or self.source_stream[word_num] == '<') and \
					self.source_stream[word_num+1] == '=':
					tk_str += self.source_stream[word_num]
					tk_str += self.source_stream[word_num+1]
					word_num += 2
					self.tokens.append(Token(tk_str,tk_str))
				else:
					tk_str += self.source_stream[word_num]
					self.tokens.append(Token(tk_str,tk_str))
					word_num +=1
			# 是特殊符号
			elif self.source_stream[word_num] in specialChar:
				# print(self.source_stream[word_num],self.source_stream[word_num+1])
				tk_str = self.source_stream[word_num]
				self.tokens.append(Token(tk_str,tk_str))
				word_num += 1
				# 遇到 '\"' ,匹配字符串
				if self.source_stream[word_num-1] == '\"':
					tk_str = ''
					while word_num < len(self.source_stream):
						if self.source_stream[word_num] == '\"':
							break
						tk_str += self.source_stream[word_num]
						word_num += 1
					self.tokens.append(Token("string",tk_str))
					tk_str = self.source_stream[word_num]
					self.tokens.append(Token(tk_str,tk_str))
					word_num += 1
				word_num = self.If_skip_word(word_num)
			# word_num += 1
