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
	def __init__(self, args):
		self.file = args.file
		self.prefix = "apkleaks-"
		self.main_dir = os.path.dirname(os.path.realpath(__file__))
		self.output = tempfile.mkstemp(suffix=".txt", prefix=self.prefix)[1] if args.output is None else args.output
		self.pattern = self.main_dir + "/../config/regexes.json" if args.pattern is None else args.pattern

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
			exit(colors.WARNING + "It's not a valid file!" + colors.ENDC)

	def decompile(self):
		out = tempfile.mkdtemp(prefix=self.prefix)
		print("%s** Decompiling APK...%s" % (colors.OKBLUE, colors.ENDC))
		os.system("apktool d %s  -fro %s" % (self.file, out))
		return out

	def unique(self, list): 
	    x = numpy.array(list) 
	    return (numpy.unique(x))

	def finder(self, pattern, path):
		TEXTCHARS = "".join(map(chr, [7,8,9,10,12,13,27] + range(0x20, 0x100)))
		is_binary_string = lambda bytes: bool(bytes.translate(None, TEXTCHARS))
		matcher = re.compile(pattern)
		found = []
		for path, _, files in os.walk(path):
			for fn in files:
				filepath = os.path.join(path, fn)
				if is_binary_string(open(filepath).read(4098)):
					continue
				with open(filepath) as handle:
					for lineno, line in enumerate(handle):
						mo = matcher.search(line)
						if mo:
							found.append(mo.group())
		return self.unique(found)

	def scanning(self, path):
		print("%s\n** Scanning against '%s' (v%s)%s" % (colors.OKBLUE, apk.get_package(), apk.get_androidversion_name(), colors.ENDC))
		with open(self.pattern) as regexes:
			regex = json.load(regexes)
			for name, pattern in regex.items():
				found = self.finder(pattern, path)
				output = open(self.output, "a+")
				if len(found):
					stdout = ("[%s]" % (name))
					print("%s\n%s%s" % (colors.OKGREEN, stdout, colors.ENDC))
					output.write(stdout + "\n")
					for secret in found:
						if name == "LinkFinder" and re.match(r"^.L[a-z].+\/.+", secret) is not None:
							continue
						stdout = ("- %s" % (secret))
						print(stdout)
						output.write(stdout + "\n")
					output.write("\n")
				output.close()
		print("%s\n** Results saved into '%s%s%s%s'%s" % (colors.OKBLUE, colors.ENDC, colors.OKGREEN, self.output, colors.OKBLUE, colors.ENDC))