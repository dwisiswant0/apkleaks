#!/usr/bin/env python3
import io
import json
import logging.config
import os
import re
import shutil
import sys
import tempfile
import threading
import requests
from tqdm import tqdm

from contextlib import closing
from distutils.spawn import find_executable
from pathlib import Path
from pipes import quote
from urllib.request import urlopen
from zipfile import ZipFile

from pyaxmlparser import APK

from apkleaks.colors import color as col
from apkleaks.utils import util

class APKLeaks:
	def __init__(self, args):
		self.apk = None
		self.file = os.path.realpath(args.file)
		self.json = args.json
		self.disarg = args.args
		self.prefix = "apkleaks-"
		self.tempdir = tempfile.mkdtemp(prefix=self.prefix)
		self.main_dir = os.path.dirname(os.path.realpath(__file__))
		self.output = tempfile.mkstemp(suffix=".%s" % ("json" if self.json else "txt"), prefix=self.prefix)[1] if args.output is None else args.output
		self.fileout = open(self.output, "%s" % ("w" if self.json else "a"))
		self.pattern = os.path.join(str(Path(self.main_dir).parent), "config", "regexes.json") if args.pattern is None else args.pattern
		self.jadx = find_executable("jadx") if find_executable("jadx") is not None else os.path.join(str(Path(self.main_dir).parent), "jadx", "bin", "jadx%s" % (".bat" if os.name == "nt" else "")).replace("\\","/")
		self.out_json = {}
		self.scanned = False
		logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})

	def apk_info(self):
		return APK(self.file)

	def download_latest_jadx(self, root_dir):
		root_dir = "jadx"
		if not os.path.exists(root_dir):
			os.makedirs(root_dir)
		jadx_dir = os.path.join(root_dir, )
		version_file = os.path.join(root_dir, "latest_version.txt")

		url = "https://api.github.com/repos/skylot/jadx/releases/latest"
		response = requests.get(url)

		if response.status_code != 200:
			util.writeln(f"Error fetching latest release info: {response.status_code}", col.FAIL)
			return

		release_info = response.json()
		tag_name = release_info["tag_name"]

		if not os.path.exists(root_dir):
			os.makedirs(root_dir)

		if os.path.exists(version_file):
			with open(version_file, "r") as f:
				current_version = f.read().strip()
		else:
			current_version = ""

		if tag_name != current_version or not os.path.exists(jadx_dir):
			util.writeln(f"[+] Downloading and extracting jadx-{tag_name}...", col.OKBLUE)

			if not os.path.exists(jadx_dir):
				os.makedirs(jadx_dir)

			download_url = None
			for asset in release_info["assets"]:
				if asset["name"].endswith(".zip"):
					download_url = asset["browser_download_url"]
					break

			if not download_url:
				util.writeln(" Error: Download URL not found.", col.FAIL)
				return

			response = requests.get(download_url, stream=True)

			if response.status_code != 200:
				util.writeln(
					f"[-] Error downloading jadx-{tag_name}.zip: {response.status_code}", col.FAIL)
				return

			zip_path = os.path.join(jadx_dir, "{}.zip".format(tag_name))
			total_size = int(response.headers.get("content-length", 0))
			with open(zip_path, "wb") as f:
				for data in tqdm(response.iter_content(chunk_size=1024), total=total_size//1024, unit="KB"):
					f.write(data)

			with ZipFile(zip_path, "r") as zip_ref:
				zip_ref.extractall(jadx_dir)

			# Remove downloaded zip file
			os.remove(zip_path)

			# Update the latest_version.txt file
			with open(version_file, "w") as f:
				f.write(tag_name)

			util.writeln(f"[+] jadx-{tag_name} successfully downloaded and extracted.", col.OKGREEN)
		else:
			util.writeln(f"[+] jadx-{tag_name} is already up to date.", col.OKGREEN)

	def integrity(self):
		if os.path.exists(self.jadx) is False:
			util.writeln("Can't find jadx binary.", col.WARNING)
			util.writeln("\n** Updating to latest jadx...\n", col.OKBLUE)
			self.download_latest_jadx(self.jadx)
		else:
			version_file = os.path.join("jadx", "latest_version.txt")
			if os.path.exists(version_file):
				with open(version_file, "r") as f:
					current_version = f.read().strip()
			util.writeln("Jadx version: %s" % (current_version), col.OKBLUE)


		if os.path.isfile(self.file):
			try:
				self.apk = self.apk_info()
			except Exception as error:
				util.writeln(str(error), col.WARNING)
				sys.exit()
			else:
				return self.apk
		else:
			sys.exit(util.writeln("It's not a valid file!", col.WARNING))

	def decompile(self):
		util.writeln("** Decompiling APK...", col.OKBLUE)
		args = [self.jadx, self.file, "-d", self.tempdir]
		try:
			args.extend(re.split(r"\s|=", self.disarg))
		except Exception:
			pass
		comm = "%s" % (" ".join(quote(arg) for arg in args))
		comm = comm.replace("\'","\"")
		os.system(comm)

	def extract(self, name, matches):
		if len(matches):
			stdout = ("[%s]" % (name))
			util.writeln("\n" + stdout, col.OKGREEN)
			self.fileout.write("%s" % (stdout + "\n" if self.json is False else ""))
			for secret in matches:
				if name == "LinkFinder":
					if re.match(r"^.(L[a-z]|application|audio|fonts|image|kotlin|layout|multipart|plain|text|video).*\/.+", secret) is not None:
						continue
					secret = secret[len("'"):-len("'")]
				stdout = ("- %s" % (secret))
				print(stdout)
				self.fileout.write("%s" % (stdout + "\n" if self.json is False else ""))
			self.fileout.write("%s" % ("\n" if self.json is False else ""))
			self.out_json["results"].append({"name": name, "matches": matches})
			self.scanned = True

	def scanning(self):
		if self.apk is None:
			sys.exit(util.writeln("** Undefined package. Exit!", col.FAIL))
		util.writeln("\n** Scanning against '%s'" % (self.apk.package), col.OKBLUE)
		self.out_json["package"] = self.apk.package
		self.out_json["results"] = []
		with open(self.pattern) as regexes:
			regex = json.load(regexes)
			for name, pattern in regex.items():
				if isinstance(pattern, list):
					for p in pattern:
						try:
							thread = threading.Thread(target = self.extract, args = (name, util.finder(p, self.tempdir)))
							thread.start()
						except KeyboardInterrupt:
							sys.exit(util.writeln("\n** Interrupted. Aborting...", col.FAIL))
				else:
					try:
						thread = threading.Thread(target = self.extract, args = (name, util.finder(pattern, self.tempdir)))
						thread.start()
					except KeyboardInterrupt:
						sys.exit(util.writeln("\n** Interrupted. Aborting...", col.FAIL))

	def cleanup(self):
		shutil.rmtree(self.tempdir)
		if self.scanned:
			self.fileout.write("%s" % (json.dumps(self.out_json, indent=4) if self.json else ""))
			self.fileout.close()
			print("%s\n** Results saved into '%s%s%s%s'%s." % (col.HEADER, col.ENDC, col.OKGREEN, self.output, col.HEADER, col.ENDC))
		else:
			self.fileout.close()
			os.remove(self.output)
			util.writeln("\n** Done with nothing. ¯\\_(ツ)_/¯", col.WARNING)
