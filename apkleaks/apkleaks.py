#!/usr/bin/env python
from apk_parse.apk import APK
from colors import colors
from contextlib import closing
from distutils.spawn import find_executable
from urllib2 import urlopen
from zipfile import ZipFile
import io
import json
import numpy
import os
import re
import shutil
import stat
import tempfile
import threading

class apkleaks:
	def __init__(self, args):
		self.file = args.file
		self.prefix = "apkleaks-"
		self.main_dir = os.path.dirname(os.path.realpath(__file__))
		self.output = tempfile.mkstemp(suffix=".txt", prefix=self.prefix)[1] if args.output is None else args.output
		self.pattern = self.main_dir + "/../config/regexes.json" if args.pattern is None else args.pattern
		self.jadx = find_executable("jadx") if find_executable("jadx") is not None else self.main_dir + "/../jadx/bin/jadx%s" % (".bat" if os.name == "nt" else "")

	def apk_info(self):
		return APK(self.file)

	def dependencies(self):
		exter = "https://github.com/skylot/jadx/releases/download/v1.1.0/jadx-1.1.0.zip"
		with closing(urlopen(exter)) as jadx:
			with ZipFile(io.BytesIO(jadx.read())) as zfile:
				zfile.extractall(self.main_dir + "/../jadx")
		os.chmod(self.jadx, 33268)
		return

	def writeln(self, message, color):
		print("%s%s%s" % (color, message, colors.ENDC))

	def integrity(self):
		if os.path.exists(self.jadx) is False:
			self.writeln("Can't find jadx binary. Downloading...\n", colors.WARNING)
			self.dependencies()
		if os.path.isfile(self.file) is True:
			try:
				self.apk = self.apk_info()
			except Exception as e:
				exit(self.writeln(str(e), colors.WARNING))
			else:
				return self.apk
		else:
			exit(self.writeln("It's not a valid file!", colors.WARNING))

	def decompile(self):
		self.tempdir = tempfile.mkdtemp(prefix=self.prefix)
		self.writeln("** Decompiling APK...", colors.OKBLUE)
		with ZipFile(self.file) as zipped:
			try:
				dex = self.tempdir + "/" + self.apk.get_package() + ".dex"
				with open(dex, "wb") as classes:
					classes.write(zipped.read("classes.dex"))
			except Exception as e:
				exit(self.writeln(str(e), colors.WARNING))
		dec = "%s %s -ds %s" % (self.jadx, dex, self.tempdir)
		os.system(dec)
		return self.tempdir

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

	def extract(self, name, matches):
		output = open(self.output, "a+")
		if len(matches):
			stdout = ("[%s]" % (name))
			self.writeln("\n" + stdout, colors.OKGREEN)
			output.write(stdout + "\n")
			for secret in matches:
				if name == "LinkFinder" and re.match(r"^.(L[a-z]|application|audio|cordova|fonts|image|kotlin|layout|multipart|res|text|video).*\/.+", secret) is not None:
					continue
				stdout = ("- %s" % (secret))
				print(stdout)
				output.write(stdout + "\n")
			output.write("\n")
		output.close()

	def scanning(self):
		self.writeln("\n** Scanning against '%s'" % (self.apk.get_package()), colors.OKBLUE)
		with open(self.pattern) as regexes:
			regex = json.load(regexes)
			for name, pattern in regex.items():
				if isinstance(pattern, list):
					for pattern in pattern:
						thread = threading.Thread(target = self.extract, args = (name, self.finder(pattern, self.tempdir)))
						thread.start()
				else:
					thread = threading.Thread(target = self.extract, args = (name, self.finder(pattern, self.tempdir)))
					thread.start()
		print("%s\n** Results saved into '%s%s%s%s'%s" % (colors.OKBLUE, colors.ENDC, colors.OKGREEN, self.output, colors.OKBLUE, colors.ENDC))
		shutil.rmtree(self.tempdir)