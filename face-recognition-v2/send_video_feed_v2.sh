#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/Desktop/hotdoc-hubspot-62a03ee3e8ea.json"

while [ True ]; do
	DATE=$(date +"%Y-%m-%d-%T")
	fswebcam -r 1280x720 --no-banner /home/pi/Desktop/Pics/$DATE.jpg
	/usr/local/bin/python3.7 ./python_to_bytes.py --name /home/pi/Desktop/Pics/$DATE.jpg
done
