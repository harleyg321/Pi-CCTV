#!/usr/bin/python3

import picamera
import subprocess
import datetime
import os
import time
import errno
import collections

SHARE = "/media/share/cctv"
DEVNULL = open(os.devnull, 'w')
WIDTH = 1920
HEIGHT = 1080
FRAMERATE = 30

def create_folder(time):
	check_drive()
	try:
		os.makedirs(SHARE + "/{}".format(time.strftime('%Y-%m-%d')))
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	return

def check_drive():
	while not os.path.exists(SHARE + "/DO_NOT_DELETE"):
		time.sleep(60)
	return

class Output:

	def __init__(self, camera):
		self.camera = camera
		self.camera.resolution = (WIDTH, HEIGHT)
		self.camera.framerate = FRAMERATE
		self.running = False
		self.process = collections.deque([],maxlen=3)

	def record(self, now):
		self.setProcess(subprocess.Popen("/usr/bin/avconv -f h264 -r " + str(FRAMERATE) + " -i pipe: -vcodec copy -vsync passthrough -r " + str(FRAMERATE) + " " + SHARE + "/{}/{}.mp4".format(now.strftime('%Y-%m-%d'),now.strftime('%H-%M-%S')), stdin=subprocess.PIPE, stderr=DEVNULL, bufsize=0, shell=True))
		if self.running:
			self.camera.split_recording(self.getstdin())
			self.closestdin()
		else:
			self.camera.start_recording(self.getstdin(), format='h264')
			self.running = True


	def getstdin(self):
		return self.getProcess().stdin

	def closestdin(self):
		if len(self.process)>1:
			self.getProcess(True).stdin.close()
			return

	def wait(self):
		self.getProcess().wait()
		return

	def setProcess(self, process):
		self.process.append(process)
		return

	def getProcess(self, previous=False):
		if previous:
			return self.process[-2]
		else:
			return self.process[-1]

check_drive()
with picamera.PiCamera() as camera:
	now = datetime.datetime.now()
	create_folder(now)
	camera.annotate_text = now.strftime('%H:%M:%S %d/%m/%Y')
	output = Output(camera)
	output.record(now)
	while True:
		start = datetime.datetime.now()
		while(datetime.datetime.now() - start).seconds < 3600:
			camera.annotate_text = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
			camera.wait_recording(0.1)
		output.record(datetime.datetime.now())
	camera.stop_recording()
	output.getstdin().close()
	output.wait()
