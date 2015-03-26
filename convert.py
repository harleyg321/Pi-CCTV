#!/usr/bin/python

import os
import sys
import glob
import errno
import time
import string
import shutil
import subprocess

RAW = "/home/pi/cctv/raw"
FINAL = "/mnt/share/cctv"

def create_folder(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	return

def check_drive():
	while not os.path.exists(FINAL + "/DO_NOT_DELETE"):
		time.sleep(60)
		#subprocess.Popen("/usr/bin/sudo /sbin/shutdown -r now", shell=True)
		#sys.exit()
	return

def folder_listing(path):
	old_path = os.getcwd()
	os.chdir(path)
	folders = sorted(glob.glob('????-??-??'))
	os.chdir(old_path)
	return folders

def file_listing(path):
	old_path = os.getcwd()
	os.chdir(path)
	files = sorted(glob.glob('??-??-??.h264'))
	os.chdir(old_path)
	return files

def hour_listing(files):
	hours = []
	for x in range(0, len(files)):
		hours += [files[x][0:2]]
	return sorted(set(hours))

def convert(folder, files, hour):
	old_path = os.getcwd()
	os.chdir(RAW + "/" + folder)
	create_folder(FINAL + "/" + folder)
	convert_files = sorted(glob.glob(hour + '-??-??.h264'))
	output,error = subprocess.Popen("/usr/bin/MP4Box -fps 30 -tmp " + RAW + " -add " + string.join(convert_files, " -cat " ) + " " + FINAL + "/{}/{}.mp4".format(folder,files[0][0:8]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	for x in range (0, len(convert_files)):
		os.remove(convert_files[x]);
	os.chdir(old_path)
	return

while True:
	check_drive()
	raw_folders = folder_listing(RAW)
	if raw_folders:
		raw_files = file_listing(RAW + "/" + raw_folders[0])
		raw_hours = hour_listing(raw_files)
		if len(raw_hours) == 0:
			os.rmdir(RAW + "/" + raw_folders[0])
			#shutil.rmtree("/mnt/share/trashbox/raw")
		elif len(raw_hours) == 1 and len(raw_folders) > 1:
			convert(raw_folders[0], raw_files, raw_hours[0])
			os.rmdir(RAW + "/" + raw_folders[0])
			#shutil.rmtree("/mnt/share/trashbox/raw")
		elif len(raw_hours) == 1 and len(raw_folders) == 1:
			pass
		elif len(raw_hours) > 1:
			convert(raw_folders[0], raw_files, raw_hours[0])
			#shutil.rmtree("/mnt/share/trashbox/raw")
	time.sleep(60)
