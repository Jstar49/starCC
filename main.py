import sys

from starcc.lexer import Lexer
from starcc.parse import Parse

file_name = ""

source_stream = ""



def parse():
	lexer = Lexer(source_stream)
	lexer.lexer()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))
	parse = Parse(lexer.tokens)
	parse.main()
	parse.drawTree()

def lexer():
	lexer = Lexer(source_stream)
	lexer.lexer()
	for i in lexer.tokens:
		print("(%s, %s)" % (i.type,i.value))



if __name__ == '__main__':
	for opt in sys.argv[1:]:
		if opt == "-f":
			file_name = sys.argv[sys.argv.index(opt)+1]
			# print(file_name)
			source_file = open(file_name,"r")
			source_stream = source_file.read()
			print(source_stream)
			# print(len(source_stream))
		elif opt == "-l":
			lexer()
		elif opt == "-p":
			parse()