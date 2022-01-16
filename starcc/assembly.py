
from .riscv import Riscv

class Assembly(object):
	"""docstring for Assembly"""
	def __init__(self, passes):
		self.fun_pool = passes.fun_pool
		self.passes = passes

	def main(self):
		riscv = Riscv(self.passes)
		riscv.main()

	def PrintIR(self):
		pass