#!/usr/bin/python

import os
import glob
import time
import shutil

SHARE = "/media/share/cctv"

def check_drive():
	return os.path.exists("/mnt/share/cctv/DO_NOT_DELETE")

def free_space():
	drive = os.statvfs(SHARE)
	return drive.f_bavail * drive.f_frsize / 1024 / 1024

def folder_listing(path):
	old_path = os.getcwd()
	os.chdir(path)
	folders = sorted(glob.glob('????-??-??'))
	os.chdir(old_path)
	return folders

while True:
	if check_drive():	
		if(free_space() < 5000):
			#NAS is low on space, delete a day
			folders = folder_listing(SHARE)
			if len(folders) > 0:
				shutil.rmtree(SHARE + "/" + store_folders[0])
				shutil.rmtree("/media/share/trashbox/cctv")
	time.sleep(60)