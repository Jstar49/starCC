import sys
import re
import graphviz
'''
# author : jxx
# how to use:
# > python3.6 thisScriptName.py large_hcc.txt large_armgcc.txt large.csv
# argv[1] : input file. hcc 的汇编代码文件或者反汇编的指令文件
# argv[2] : input file. armgcc 的汇编代码文件或者反汇编的指令文件
# argv[3] : output file. 结果保存文件,唯一格式 .csv
'''

dot = graphviz.Digraph(comment='root')

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

def printdot(fun_info):
	# print(fun_info['name'])
	fun_block = fun_info['name']+"\n"
	fun_block_name = fun_info['name']+"\n"
	# dot.node(fun_info['name'],fun_info['name'])
	for line in fun_info["api_stmt"]:
		if len(re.findall(r'<(.*)>:',line)):
			print(re.findall(r'<(.*)>:',line)[0])
			fun_block = line
			continue
		fun_block += line

def get_api_diff(file1_result):
	# list for store api
	file1_api_list = {}

	# print(file1_result)

	for i in file1_result:
		if re.search(r'<(.*)>:', i) and '.L' not in i:
			api_index = file1_result.index(i)
			api_addr_begin = re.findall(r'(.*) <',i)[0]
			api_name = re.findall(r'<(.*)>',i)[0]
			api_addr_end = 0
			api_stmt = []
			for j in range(api_index+1, len(file1_result)):
				if re.search(r'<(.*)>:', file1_result[j]) and '<.L' not in file1_result[j] :
					templine = j-1
					while api_addr_end == 0:
						if len(file1_result[templine].split("\t")) >= 3:
							api_addr_end = str.lstrip(re.findall(r' (.*):',file1_result[templine])[0])
							
						else:
							templine = templine - 1
					break
				api_stmt.append(file1_result[j])
			templine = j-1
			while api_addr_end == 0:
				if len(file1_result[templine].split("\t")) >= 3:
					api_addr_end = str.lstrip(re.findall(r' (.*):',file1_result[templine])[0])
				else:
					templine = templine - 1
			# print(api_addr_begin)
			# print(api_addr_end)
			api_length = int(api_addr_end,16) - int(api_addr_begin,16) + 2
			file1_api_list[api_name] = {'name': api_name, \
										'addr_begin': api_addr_begin, \
										'addr_end': api_addr_end,\
										'api_length': api_length,
										'api_stmt':api_stmt}
			# print(api_name)
			# for i in api_stmt:
			# 	print(i)
			printdot(file1_api_list[api_name])
	# print(file1_api_list)



if __name__ =='__main__':
	# print(sys.argv[1])
	f= open(sys.argv[1],'r')
	f_stream = f.readlines()
	f.close()
	get_api_diff(f_stream)