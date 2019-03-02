import sys
import os
import re

class LinesCounter:
	def __init__(self, main_directory):
		self.main_directory = self.getRootPath(main_directory)
		self.setWhatToBeIgnored()

	def getTotal(self, with_logging=False):
		self.with_logging = with_logging
		return self.getCountOfLinesInOneItem(self.main_directory, -1)

	def recursive(self, directory, level = 0):
		content = self.getContentOfDirectory(directory)
		total = 0
		for item in content:
			total += self.getCountOfLinesInOneItem(item, level)
		return total

	def getCountOfLinesInOneItem(self, item, level):
		if(self.toBeIgnored(item)):
			return 0
		if os.path.isfile(item):
			number = self.getCountOfLinesInOneFile(item)
			self.logger(level, item, number)
		else:
			self.logger(level, item)
			number = self.recursive(item, level+1)
		return number

	def setWhatToBeIgnored(self):
		self.readAndSetContentOfGitIgnoreIfExists()

	def toBeIgnored(self, item):
		try:
			for ignorant in self.to_be_ignored:
				if item == ignorant or item.endswith(ignorant):
					print(f'ignored: {item}')
					return True
		except:
			pass
		return False

	def getCountOfLinesInOneFile(self, file_path):
		lines = 0
		try:
			with open(file_path) as file:
				lines = sum( 1 for i, line in enumerate(file) )
		except:
			pass
		return lines	

	def logger(self, level, path, number=None):
		if not self.with_logging:
			return 
		if os.path.isfile(path):
			print("    "*level + self.getNameFromPath(path) + ": " + str(number))
		else:
			print("    "*level + self.getNameFromPath(path) + ": ")

	def getNameFromPath(self, path):
		return path[path.rfind('/'):]

	def getRootPath(self, path, parent=None):
		parent = os.getcwd() if not parent else parent
		return path if self.isRoot(path) else os.path.join(parent, path)

	def isRoot(self, path):
		return True if path[0] == '/' else False

	def getContentOfDirectory(self, directory):
		content = os.listdir(directory)
		return [ self.getRootPath(item, directory) for item in content ]

	def readAndSetContentOfGitIgnoreIfExists(self):
		if os.path.isfile(self.main_directory):
			return 

		dirContent = os.listdir(self.main_directory)
		if '.gitignore' not in dirContent:
			return

		content = list(open(os.path.join(self.main_directory, '.gitignore')))
		content.append('/.git\n')

		for i in range(len(content)):
			startIndex = 1 if content[i][0] == '/' else 0
			if content[i][0] == '*':
				content[i] = content[i][1:-1]
			else:
				content[i] = self.getRootPath(content[i][startIndex:-1], self.main_directory)
		self.to_be_ignored = content

if __name__ == '__main__':
	print(f'Counting lines for "{sys.argv[0]}" ')
	linesCounter = LinesCounter(sys.argv[1])
	print(f"Total: {linesCounter.getTotal(with_logging=False)}")