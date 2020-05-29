#!/usr/bin/env python
from apk_parse.apk import APK
from colors import colors
from distutils.spawn import find_executable
import json
import numpy
import os
import re
import tempfile

class apkleaks:
	def __init__(self, file):
		self.file = file
		self.current = os.path.dirname(os.path.realpath(__file__))

	def apk_info(self):
		return APK(self.file)

	def integrity(self):
		if find_executable("apktool") is None:
			exit(colors.WARNING + "Can't find 'apktool'. Please see https://ibotpeaches.github.io/Apktool/install/" + colors.ENDC)

		if os.path.isfile(self.file) is True:
			try:
				global apk
				apk = self.apk_info()
			except Exception as e:
				exit(colors.WARNING + str(e) + colors.ENDC)
			else:
				return apk
		else:
			exit(colors.WARNING + "It's not a file!" + colors.ENDC)

	def decompile(self):
		out = tempfile.mkdtemp(prefix="apkleaks-")
		print("%s** Decompiling APK...%s" % (colors.OKBLUE, colors.ENDC))
		os.system("apktool d %s  -fro %s" % (self.file, out))
		return out

	def unique(self, list): 
	    x = numpy.array(list) 
	    return (numpy.unique(x))

	def finder(self, pattern, path):
		TEXTCHARS = ''.join(map(chr, [7,8,9,10,12,13,27] + range(0x20, 0x100)))
		is_binary_string = lambda bytes: bool(bytes.translate(None, TEXTCHARS))
		matcher = re.compile(pattern)
		found = []
		for path, _, files in os.walk(path):
			for fn in files:
				filepath = os.path.join(path, fn)
				if is_binary_string(open(filepath).read(1024)):
					continue
				with open(filepath) as handle:
					for lineno, line in enumerate(handle):
						mo = matcher.search(line)
						if mo:
							found.append(mo.group())
		return self.unique(found)

	def scanning(self, path):
		print("%s\n** Scanning against '%s' (v%s)%s" % (colors.OKBLUE, apk.get_package(), apk.get_androidversion_name(), colors.ENDC))
		with open(self.current + "/../config/regexes.json") as regexes:
			regex = json.load(regexes)
			for name, pattern in regex.items():
				found = self.finder(pattern, path)
				if len(found):
					print("%s\n[%s]%s" % (colors.OKGREEN, name, colors.ENDC))
					for secret in found:
						if name == "LinkFinder" and re.match(r"^.L[a-z].+\/.+", secret) is not None:
							continue
						print("- %s" % (secret))