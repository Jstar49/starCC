import sys
import re
import graphviz
'''
# author : jxx
# how to use: python test.py hello.txt
# > python3.6 thisScriptName.py large_hcc.txt large_armgcc.txt large.csv
# argv[1] : input file. hcc 的汇编代码文件或者反汇编的指令文件
# argv[2] : input file. armgcc 的汇编代码文件或者反汇编的指令文件
# argv[3] : output file. 结果保存文件,唯一格式 .csv
'''


dot_num = 0

def gratest(funs):
	global dot_num
	g = graphviz.Digraph('G', filename='cluster_edge.gv',format='png',node_attr={'color': 'lightblue2', 'style': 'filled'})
	g.attr(compound='true')
	g.attr('node', shape='box')

	for fun_info in funs:
		# with g.subgraph(name='cluster1') as c:
		# 	c.edges(['eg', 'ef'])
		block_list = []
		fun_block = funs[fun_info]['name']+"\n"
		fun_block_name = funs[fun_info]['name']+"\n"
		jump_in_fun = []
		for line in funs[fun_info]["api_stmt"]:
			print(line,end='')
		for line in funs[fun_info]["api_stmt"]:
			if len(re.findall(r'<(.*)>:',line)):
				# print(re.findall(r'<(.*)>:',line)[0])
				block_node = Tree(fun_block_name)
				block_node.dot_num = str(dot_num)
				dot_num += 1
				block_node.block_code = fun_block
				block_list.append(block_node)
				# update 
				fun_block = line
				fun_block_name = re.findall(r'<(.*)>:',line)[0]
				continue
			# if len(re.findall(r'<(.*)>',line)):
			# 	jump_in_fun.append([fun_block_name,re.findall(r'<(.*)>',line)[0]])
			fun_block += line
		print(jump_in_fun)
		fun_suck = []
		print(block_list[0].block_code)
		g.node(str(block_list[0].dot_num),block_list[0].block_code)
		for node_index in range(1,len(block_list)):
			g.node(block_list[node_index].dot_num,block_list[node_index].block_code)
			fun_suck.append((block_list[node_index-1].dot_num,block_list[node_index].dot_num))
		for i in jump_in_fun:
				for j in block_list:
					if i[0] == j.key:
						begin = j.dot_num
					if i[1] == j.key:
						end = j.dot_num
				fun_suck.append((begin,end))
		print(fun_suck)
		with g.subgraph(name='cluster'+funs[fun_info]['name']) as d:
			d.edges(fun_suck)
	# dot.render('test.gv')
	# print(funs[fun_info]['name'])
	# with g.subgraph(name='cluster1HAL_WDG_Start') as c:
	# 	c.edges([('eg', 'ef'),('sf','ll')])
	# with g.subgraph(name=str(funs[fun_info]['name'])+'1') as c:
	# 	c.edges([('op','sdf'),('sf','ll')])
	g.render()

class Tree(object):
	def __init__(self,key):
		self.key = key
		self.dot_num = None
		self.block_code = None

def printdot(funs):
	dot = graphviz.Digraph(comment='root')
	dot.attr(compound='true')
	dot.attr('node', shape='box')
	global dot_num
	for fun_info in funs:
		block_list = []
		fun_block = funs[fun_info]['name']+"\n"
		fun_block_name = funs[fun_info]['name']+"\n"
		jump_in_fun = []
		for line in funs[fun_info]["api_stmt"]:
			print(line,end='')
		for line in funs[fun_info]["api_stmt"]:
			if len(re.findall(r'<(.*)>:',line)):
				print(re.findall(r'<(.*)>:',line)[0])
				block_node = Tree(fun_block_name)
				block_node.dot_num = str(dot_num)
				dot_num += 1
				block_node.block_code = fun_block
				block_list.append(block_node)
				# update 
				fun_block = line
				fun_block_name = re.findall(r'<(.*)>:',line)[0]
				continue
			if len(re.findall(r'<(.*)>',line)):
				jump_in_fun.append([fun_block_name,re.findall(r'<(.*)>',line)[0]])
			fun_block += line
		print(jump_in_fun)
		fun_suck = []
		dot.node(str(block_list[0].dot_num),block_list[0].block_code)
		for node_index in range(1,len(block_list)):
			dot.node(block_list[node_index].dot_num,block_list[node_index].block_code)
			fun_suck.append((block_list[node_index-1].dot_num,block_list[node_index].dot_num))
		for i in jump_in_fun:
				for j in block_list:
					if i[0] == j.key:
						begin = j.dot_num
					if i[1] == j.key:
						end = j.dot_num
				fun_suck.append((begin,end))
		print(fun_suck)
		with dot.subgraph(name=funs[fun_info]['name']) as d:
			d.edges(fun_suck)
	# dot.render('test.gv')
	dot.edge('1','11')
	dot.render('test.gv')


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
			for i in api_stmt:
				print(i)
	gratest(file1_api_list)
	# print(file1_api_list)



if __name__ =='__main__':
	# print(sys.argv[1])
	f= open(sys.argv[1],'r')
	f_stream = f.readlines()
	f.close()
	get_api_diff(f_stream)
	
	# gratest()