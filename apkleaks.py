#!/usr/bin/env python
from apkleaks.apkleaks import apkleaks
from apkleaks.colors import colors
import argparse
import os
import shutil

def header():
	VERSION = open(os.path.dirname(os.path.realpath(__file__)) + "/VERSION", "r").read()
	return ("     _    ____  _  ___               _        \n    / \\  |  _ \\| |/ / |    ___  __ _| | _____ \n   / _ \\ | |_) | ' /| |   / _ \\/ _` | |/ / __|\n  / ___ \\|  __/| . \\| |__|  __/ (_| |   <\\__ \\\n /_/   \\_\\_|   |_|\\_\\_____\\___|\\__,_|_|\\_\\___/\n # {}\n --\n Scanning APK file for secrets\n (c) 2020, dwisiswant0\n".format(VERSION))

def argument():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", help="APK file to scanning", type=str, required=True)
	arg = parser.parse_args()
	return arg

if __name__ == "__main__":
	print(colors.HEADER)
	print(colors.HEADER + header() + colors.ENDC)
	arg = argument()
	init = apkleaks(arg.file)
	apk = init.integrity()
	out = init.decompile()
	init.scanning(out)
	shutil.rmtree(out)