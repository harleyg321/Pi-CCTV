#!/usr/bin/python

import os
import glob
import time
import shutil

RAW = "/home/pi/cctv/raw"
FINAL = "/mnt/share/cctv"

def check_drive():
	return os.path.exists("/mnt/share/cctv/DO_NOT_DELETE")
		#time.sleep(60)
		#subprocess.Popen("/usr/bin/sudo /sbin/shutdown -r now", shell=True)
		#sys.exit()
	#return

def pi_free_space():
	pi_drive = os.statvfs(RAW)
	return pi_drive.f_bavail * pi_drive.f_frsize / 1024 / 1024

def store_free_space():
	store_drive = os.statvfs(FINAL)
	return store_drive.f_bavail * store_drive.f_frsize / 1024 / 1024

def folder_listing(path):
	old_path = os.getcwd()
	os.chdir(path)
	folders = sorted(glob.glob('????-??-??'))
	os.chdir(old_path)
	return folders

while True:
	if(pi_free_space() < 5000):
		#pi is low on space (unlikely, means NAS is not accessible)
		pi_folders = folder_listing(RAW)
		if len(pi_folders) > 0:
			shutil.rmtree(RAW + "/" + pi_folders[0])

	if check_drive():	
		if(store_free_space() < 5000):
			#NAS is low on space, delete a day
			store_folders = folder_listing(FINAL)
			if len(store_folders) > 0:
				shutil.rmtree(FINAL + "/" + store_folders[0])
				shutil.rmtree("/mnt/share/trashbox/cctv")

	time.sleep(60)
