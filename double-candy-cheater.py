#!/usr/bin/env python

import os
import cv2
import numpy as np
import time

DEBUG=False

while(1):
	window=os.popen("osascript -e 'tell app \"QuickTime Player\" to id of window 1'").read().strip()
	if not DEBUG:
		os.system("screencapture -l" + window + " /tmp/screenshoot.jpg")

	frame = cv2.imread('/tmp/screenshoot.jpg')

	frame = cv2.medianBlur(frame,5)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=100, param2=40, minRadius=0, maxRadius=100)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		y = 0
		balls = {}
		for i in circles[0,:]:
			roi = frame[i[1] - 15:i[1] + 15,i[0] - 15:i[0] + 15]
			balls[i[1]] = cv2.mean(roi)[1] > 175 # Balls present a huge difference on green color

			if DEBUG:
				cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
				cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)

		adjacents = []
		for key in sorted(balls):
			adjacents.append(balls[key])

		if DEBUG:
			cv2.imshow('Debug', gray)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			break

		if len(adjacents) == 3:
			os.system('clear')
			if (adjacents[0] != adjacents[1]) and (adjacents[1] != adjacents[2]):
				print "Tap!"
				os.system("printf \"\a\"")
