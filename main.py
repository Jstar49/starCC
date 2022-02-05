import sys

from starcc.lexer import Lexer
from starcc.parse import Parse
from starcc.check import Check
from starcc.passes import Passes
from starcc.assembly import Assembly

file_name = ""

source_stream = ""


# 语法分析
def parse():
	# 词法分析
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))
	parse = Parse(lexer.tokens)
	parse.main()
	parse.drawTree(parse.grammar_tree)

# 词法分析
def lexer():
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))

# 中间代码生成器
def passes():
	# 词法分析
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))
	# 语法分析
	parse = Parse(lexer.tokens)
	parse.main()
	parse.drawTree(parse.grammar_tree)
	# 符号检查
	check = Check(parse)
	check.main()
	# parse.drawTree(check.parse.grammar_tree)
	# 中间代码生成
	passes = Passes(check)
	passes.main()
	# parse.drawTree(passes.parse_tree)

def assembly():
	# 词法分析
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))
	# 语法分析
	parse = Parse(lexer.tokens)
	parse.main()
	parse.drawTree(parse.grammar_tree)
	# 符号检查
	check = Check(parse)
	check.main()
	# parse.drawTree(check.parse.grammar_tree)
	# 中间代码生成
	passes = Passes(check)
	passes.main()
	# 生成汇编代码
	assembly = Assembly(passes)
	assembly.main()

if __name__ == '__main__':
	for opt in sys.argv[1:]:
		if opt == "-f":
			file_name = sys.argv[sys.argv.index(opt)+1]
			# print(file_name)
			source_file = open(file_name,"r")
			source_stream = source_file.read()
			# print(source_stream)
			# print(len(source_stream))
		elif opt == "-l":
			lexer()
		elif opt == "-p":
			parse()
		elif opt == "-r":
			passes()
		elif opt == "-s":
			assembly()