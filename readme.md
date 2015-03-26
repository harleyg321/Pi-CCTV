# CCTC for the Raspberry pi

This repository consists of three key files

##### record.py
Record uninterrupted footage to the local filesystem, splitting files into 10 minute segments.

##### convert.py
Use MP4Box to add the h264 files into a mp4 container saved on a network share.

##### housekeeping.py
Ensure the network share and local storage don't fill up. Under normal operation the local filesystem will be kept clear by the conversion process.
