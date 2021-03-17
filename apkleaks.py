#!/usr/bin/env python3
from apkleaks.apkleaks import APKLeaks
from apkleaks.colors import clr
import argparse
import os

def header():
	VERSION = open(os.path.dirname(os.path.realpath(__file__)) + "/VERSION", "r").read()
	return ("     _    ____  _  ___               _        \n    / \\  |  _ \\| |/ / |    ___  __ _| | _____ \n   / _ \\ | |_) | ' /| |   / _ \\/ _` | |/ / __|\n  / ___ \\|  __/| . \\| |__|  __/ (_| |   <\\__ \\\n /_/   \\_\\_|   |_|\\_\\_____\\___|\\__,_|_|\\_\\___/\n {}\n --\n Scanning APK file for URIs, endpoints & secrets\n (c) 2020-2021, dwisiswant0\n".format(VERSION))

def argument():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", help="APK file to scanning", type=str, required=True)
	parser.add_argument("-o", "--output", help="Write to file results (random if not set)", type=str, required=False)
	parser.add_argument("-p", "--pattern", help="Path to custom patterns JSON", type=str, required=False)
	parser.add_argument("--json", help="Save as JSON format", required=False, action="store_true")
	arg = parser.parse_args()
	return arg

if __name__ == "__main__":
	print(clr.HEADER)
	print(clr.HEADER + header() + clr.ENDC)
	args = argument()
	init = APKLeaks(args)
	apk = init.integrity()
	init.decompile()
	init.scanning()