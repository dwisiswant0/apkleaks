#!/usr/bin/env python3
import os
import re
import sys
from apkleaks.colors import color as col

class util:
	@staticmethod
	def write(message, color):
		sys.stdout.write("%s%s%s" % (color, message, col.ENDC))

	@staticmethod
	def writeln(message, color):
		util.write(message + "\n", color)

	@staticmethod
	def finder(pattern, files_to_scan):
		matcher = re.compile(pattern)
		found = []
		
		for file in files_to_scan:
			with open(file) as handle:
				try:
					for line in handle.readlines():
						mo = matcher.search(line)
						if mo:
							found.append(mo.group())
				except Exception:
					pass

		return sorted(list(set(found)))
