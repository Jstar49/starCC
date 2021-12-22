import sys

from starcc.lexer import Lexer
from starcc.parse import Parse
from starcc.check import Check
from starcc.passes import Passes

file_name = ""

source_stream = ""



def parse():
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))
	parse = Parse(lexer.tokens)
	parse.main()
	parse.drawTree(parse.grammar_tree)

def lexer():
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))

def passes():
	lexer = Lexer(source_stream)
	lexer.main()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))
	parse = Parse(lexer.tokens)
	parse.main()
	# parse.drawTree(parse.grammar_tree)



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