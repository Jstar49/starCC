


class Assembly(object):
	"""docstring for Assembly"""
	def __init__(self, passes):
		self.fun_pool = passes.fun_pool

	def main(self):
		print(self.fun_pool)

	def PrintIR(self):
		pass