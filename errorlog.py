import logging
import argparse
import pathlib
import re
from range_key_dict import RangeKeyDict
from tabulate import tabulate


class Module:
	# WA 3.8.1
	WASegments = RangeKeyDict({
		(0x00400000, 0x00401000 - 1): '.HEADER',
		(0x00401000, 0x0061A000 - 1): '.text',
		(0x0061A000, 0x0061A744 - 1): '.idata',
		(0x0061A744, 0x00694000 - 1): '.rdata',
		(0x00694000, 0x006AFD00 - 1): '.data',
		(0x006AFD00, 0x006AFE60 - 1): '.idata',
		(0x006AFE60, 0x008C5000 - 1): '.data',
	})

	def __init__(self, path, base, size, info):
		self.path = path
		self.name = path.split('\\')[-1]
		self.base = base
		self.size = size
		self.end = self.base + self.size
		self.iswa = '.exe' in self.name.lower()
		self.loadingbase = 0x00400000 if self.iswa else 0x10000000
		self.info = info

	def __str__(self):
		return f'Module: {self.name} [0x{self.base:08x} - 0x{self.end:08x}]\n{self.info}'

	def rebase(self, addr):
		rebased = addr - self.base + self.loadingbase
		if not self.iswa:
			return rebased, None
		else:
			try:
				return rebased, Module.WASegments[rebased]
			except:
				return rebased, ".heap"


class ErrorLog:
	def __init__(self, file):
		with open(file, 'r') as f:
			self.contents = f.read().replace('\r\n', '\n')
			self.path = pathlib.Path(file)
		self.modules = []
		self.memory = None

	def rebase(self, addrstr):
		value = int(addrstr, 16)
		try:
			module = self.memory[value]
			rebased, segment = module.rebase(value)
			return f'0x{value:08x} [{module.name} 0x{rebased:08x}{segment if segment else ""}]'
		except:
			return f'0x{value:08x}'

	def parseModules(self):
		tmp = {}
		for match in re.finditer(r"Module(.|\n)*?\n\n", self.contents):
			data = match.group()
			splitlines = data.splitlines()
			path = splitlines[1]
			addrs = re.findall(r"Image Base: 0x([0-9a-fA-F]+).+Image Size: 0x([0-9a-fA-F]+)", data)
			base = int(addrs[0][0], 16)
			size = int(addrs[0][1], 16)
			module = Module(path, base, size, data)
			tmp[(base, base + size)] = module
			self.modules.append(module)
		self.memory = RangeKeyDict(tmp)

	def parseStack(self):
		lines = []
		for match in re.finditer(r"0[xX]([0-9a-fA-F]+): ([0-9a-fA-F]+) ([0-9a-fA-F]+) ([0-9a-fA-F]+) ([0-9a-fA-F]+)(.*)", self.contents):
			matches = list(match.groups())
			stackaddr = int(matches[0], 16)
			out = [f'0x{stackaddr:08x}:']
			for i, addr in enumerate(matches[1:-1]):
				out += [self.rebase(addr)]
			rest = matches[-1]
			out += [rest]
			lines.append(out)
		print(tabulate(lines))

	def parseInfo(self):
		data = self.contents[:self.contents.index("Stack:")]
		data = re.sub(r"0[xX]([0-9a-fA-F]+)", lambda m: self.rebase(m.group()), data)
		print(data)



if __name__ == "__main__":
	logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help="path to ERRORLOG.TXT file")
	args = parser.parse_args()

	errlog = ErrorLog(args.file)
	errlog.parseModules()
	errlog.parseInfo()
	errlog.parseStack()
	for module in errlog.modules:
		print(module)
