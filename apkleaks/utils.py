import os
import re
import sys
from apkleaks.colors import Color as col


class Util:
	@staticmethod
	def write(message, color):
		sys.stdout.write("%s%s%s" % (color, message, col.ENDC))

	@staticmethod
	def writeln(message, color):
		Util.write(message + "\n", color)

	@staticmethod
	def finder(pattern, path):
		matcher = re.compile(pattern)
		found = []
		for fp, _, files in os.walk(path):
			for fn in files:
				filepath = os.path.join(fp, fn)
				with open(filepath) as handle:
					try:
						for line in handle.readlines():
							mo = matcher.search(line)
							if mo:
								found.append(mo.group())
					except Exception:
						pass
		return sorted(list(set(found)))
