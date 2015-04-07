#!/usr/bin/python

import picamera
import datetime
import subprocess
import errno
import sys
import os
import time
import threading
import Queue

def create_folder(time):
	check_drive()
	try:
		os.makedirs("/home/pi/cctv/raw/{}".format(time.strftime('%Y-%m-%d')))
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	return

def check_drive():
	while not os.path.exists("/mnt/share/cctv/DO_NOT_DELETE"):
		time.sleep(60)
	return
		#time.sleep(60)
		#subprocess.Popen("/usr/bin/sudo /sbin/shutdown -r now", shell=True)
		#sys.exit()
	#return

def capture_image(camera, capture):
	while True:
		cap = capture.get()
		if cap:
			camera.capture("/home/pi/cctv/public_html/cctv.jpg", use_video_port=True, splitter_port=2)
			capture.put(False)
		else:
			time.sleep(0.1)

if __name__ == '__main__':
	with picamera.PiCamera() as camera:
		capture = Queue.Queue()
		capture.put(False)
		t = threading.Thread(target=capture_image, args=(camera,capture))
		t.start()

		camera.resolution = (1920, 1080)
		camera.framerate = 30
		camera.annotate_text = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
		now = datetime.datetime.now()	
		create_folder(now)
		try:
			camera.start_recording('/home/pi/cctv/raw/{}/{}.h264'.format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')),bitrate=5000000)
			print("{}/{}".format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')))
		except:
			subprocess.Popen("/usr/bin/sudo /sbin/shutdown -r now", shell=True)
			sys.exit()
		while True:
			start = datetime.datetime.now()
			last = start
			while (datetime.datetime.now() - start).seconds < 598:
				dt = datetime.datetime.now()
				camera.annotate_text = dt.strftime('%H:%M:%S %d/%m/%Y')
				if (dt-last).seconds > 0:
					capture.put(True)
					last = dt
				else:
					camera.wait_recording(0.1)
			now = datetime.datetime.now()
			create_folder(now)
			try:
				camera.split_recording('/home/pi/cctv/raw/{}/{}.h264'.format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')))
				print("{}/{}".format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')))
			except:
				try:
					camera.stop_recording()
					os.remove('/home/pi/cctv/raw/{}/{}.h264'.format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')))
				except:
					pass
				try:
					camera.start_recording('/home/pi/cctv/raw/{}/{}.h264'.format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')),bitrate=5000000)
					print("{}/{}".format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')))
				except:
					subprocess.Popen("/usr/bin/sudo /sbin/shutdown -r now", shell=True)
					sys.exit()
		camera.stop_recording()
