#!/usr/bin/env python3
from apkleaks.colors import clr
from contextlib import closing
from distutils.spawn import find_executable
from pipes import quote
from pyaxmlparser import APK
from urllib.request import urlopen
from zipfile import ZipFile
import io
import json
import logging.config
import mimetypes
import numpy
import os
import re
import shutil
import sys
import tempfile
import threading

class APKLeaks:
	def __init__(self, args):
		self.file = args.file
		self.prefix = "apkleaks-"
		self.tempdir = tempfile.mkdtemp(prefix=self.prefix)
		self.main_dir = os.path.dirname(os.path.realpath(__file__))
		self.output = tempfile.mkstemp(suffix=".txt", prefix=self.prefix)[1] if args.output is None else args.output
		self.pattern = self.main_dir + "/../config/regexes.json" if args.pattern is None else args.pattern
		self.jadx = find_executable("jadx") if find_executable("jadx") is not None else self.main_dir + "/../jadx/bin/jadx%s" % (".bat" if os.name == "nt" else "")
		logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})

	def apk_info(self):
		return APK(self.file)

	def dependencies(self):
		exter = "https://github.com/skylot/jadx/releases/download/v1.2.0/jadx-1.2.0.zip"
		with closing(urlopen(exter)) as jadx:
			with ZipFile(io.BytesIO(jadx.read())) as zfile:
				zfile.extractall(self.main_dir + "/../jadx")
		os.chmod(self.jadx, 33268)

	def write(self, message, color):
		sys.stdout.write("%s%s%s" % (color, message, clr.ENDC))

	def writeln(self, message, color):
		self.write(message + "\n", color)

	def integrity(self):
		if os.path.exists(self.jadx) is False:
			self.writeln("Can't find jadx binary.", clr.WARNING)
			valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
			while True:
				self.write("Do you want to download jadx? (Y/n) ", clr.OKBLUE)
				choice = input().lower()
				if choice == "":
					choice = valid["y"]
					break
				elif choice in valid:
					choice = valid[choice]
					break
				else:
					self.writeln("\nPlease respond with 'yes' or 'no' (or 'y' or 'n').", clr.WARNING)
			if choice:
				self.writeln("** Downloading jadx...\n", clr.OKBLUE)
				self.dependencies()
			else:
				sys.exit(self.writeln("Aborted.", clr.FAIL))

		if os.path.isfile(self.file) is True:
			try:
				self.apk = self.apk_info()
			except Exception as e:
				sys.exit(self.writeln(str(e), clr.WARNING))
			else:
				return self.apk
		else:
			sys.exit(self.writeln("It's not a valid file!", clr.WARNING))

	def decompile(self):
		self.writeln("** Decompiling APK...", clr.OKBLUE)
		with ZipFile(self.file) as zipped:
			try:
				dex = self.tempdir + "/" + self.apk.package + ".dex"
				with open(dex, "wb") as classes:
					classes.write(zipped.read("classes.dex"))
			except Exception as e:
				sys.exit(self.writeln(str(e), clr.WARNING))
		args = [self.jadx, dex, "-d", self.tempdir, "--deobf"]
		comm = "%s" % (" ".join(quote(arg) for arg in args))
		os.system(comm)
		return self.tempdir

	def unique(self, list): 
		x = numpy.array(list) 
		return (numpy.unique(x))

	def finder(self, pattern, path):
		matcher = re.compile(pattern)
		found = []
		for path, _, files in os.walk(path):
			for fn in files:
				filepath = os.path.join(path, fn)
				if mimetypes.guess_type(filepath)[0] is None:
					continue
				with open(filepath) as handle:
					for lineno, line in enumerate(handle):
						mo = matcher.search(line)
						if mo:
							found.append(mo.group())
		return self.unique(found)

	def extract(self, name, matches):
		output = open(self.output, "a+")
		if matches:
			stdout = ("[%s]" % (name))
			self.writeln("\n" + stdout, clr.OKGREEN)
			output.write(stdout + "\n")
			for secret in matches:
				if name == "LinkFinder" and re.match(r"^.(L[a-z]|application|audio|fonts|image|layout|multipart|plain|text|video).*\/.+", secret) is not None:
					continue
				stdout = ("- %s" % (secret))
				print(stdout)
				output.write(stdout + "\n")
			output.write("\n")
		output.close()

	def scanning(self):
		self.writeln("\n** Scanning against '%s'" % (self.apk.package), clr.OKBLUE)
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

	def __del__(self):
		print("%s\n** Results saved into '%s%s%s%s'%s" % (clr.OKBLUE, clr.ENDC, clr.OKGREEN, self.output, clr.OKBLUE, clr.ENDC))
		try:
			shutil.rmtree(self.tempdir)
		except Exception:
			return
