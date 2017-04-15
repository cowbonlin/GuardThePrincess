import numpy as np
import cv2
import Character
from math import sqrt
from time import clock

detectX, detectY = 0, 0

def mouseCallback(event, x, y, flag, param):
	global detectX, detectY
	if event == cv2.EVENT_LBUTTONDOWN:
		detectX, detectY = y, x
		print x, y

def produceMask(image, lowerList, upperList):
	lower = np.array(lowerList)
	upper = np.array(upperList)
	mask = cv2.inRange(image, lower, upper)
	sucThresh, thresh = cv2.threshold(mask, 32, 255, cv2.THRESH_BINARY)
	return thresh

def main():

	cap = cv2.VideoCapture(0)
	height, width, depth = cap.read()[1].shape
	frameIndex = 0.0

	## create characters
	guardian = Character.Guardian()
	princess = Character.Princess()
	bulletList = []

	# mouse event capture
	cv2.namedWindow('Tracking')
	cv2.setMouseCallback('Tracking', mouseCallback)
	global detectX, detectY
	detectX, detectY = height/4, width/4

	while(True):
		startTime = clock()
		## read the frame and flip
		sucFrame, frame = cap.read()
		frame = cv2.flip(frame, 1)
		backGround = np.zeros((height,width,3), np.uint8)

		## BGR -> HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		## mask the desire color and threshold
		threshYellow = produceMask(hsv, [ 10,140,190], [ 45,230,256])
		threshPink   = produceMask(hsv, [140,140,120], [180,220,256])

		## display small thresh image
		smallFrame = cv2.resize(threshPink, (0,0), fx=0.25, fy=0.25)
		cv2.circle(smallFrame, (smallFrame.shape[1]/2,smallFrame.shape[0]/2), 3, (0,0,255), -1)
		cv2.imshow('small', smallFrame)
		
		## find and draw contours
		## yellow
		contoursYellow = cv2.findContours(threshYellow.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		if contoursYellow and len(contoursYellow) > 0:
			## largest contour
			maxContour = max(contoursYellow, key=cv2.contourArea)
			((xYellow,yYellow), radiusYellow) = cv2.minEnclosingCircle(maxContour)
			guardian.x, guardian.y = int(xYellow), int(yYellow)

			## draw circles
			if radiusYellow > 10:
				guardian.draw(frame)

		## pink
		contoursPink = cv2.findContours(threshPink.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		if contoursPink and len(contoursPink) > 0:
			## largest contour
			maxContour = max(contoursPink, key=cv2.contourArea)
			((xPink,yPink), radiusPink) = cv2.minEnclosingCircle(maxContour)
			princess.x, princess.y = int(xPink), int(yPink)

			## draw circles
			if radiusPink > 10:
				princess.draw(frame)

		## delete outrange bullets
		for bullet in bulletList:
			if bullet.strPoint[0] > width or bullet.strPoint[0] < 0 or bullet.strPoint[1] > height or bullet.strPoint[1] < 0:
				bulletList.remove(bullet)
				del bullet

		## new bullet
		if frameIndex %3 == 0:
			bullet = Character.Bullet(guardian.x, guardian.y, princess.x, princess.y, frameIndex)
			bulletList.append(bullet)

		## draw bullets
		for bullet in bulletList:
			bullet.updatePosition(30)
			bullet.draw(frame)

		## detect the point
		# print hsv[detectX][detectY]
		# cv2.circle(frame, (detectY, detectX), 5, (255,0,255), -1)

		cv2.imshow('Tracking', frame)
		# cv2.imshow('BG', backGround)

		if cv2.waitKey(1) == ord('q'):
			break

		frameIndex += 1

		## calculate FPS
		endTime = clock()
		# print 1 / (endTime - startTime)

	cap.release()
	cv2.destroyAllWindows()

main()