import numpy as np
import cv2
import Character
from math import sqrt

detectX, detectY = 0, 0

def mouseCallback(event, x, y, flag, param):
	global detectX, detectY
	if event == cv2.EVENT_LBUTTONDOWN:
		detectX, detectY = y, x
		print x, y

def main():

	cap = cv2.VideoCapture(0)
	height, width, depth = cap.read()[1].shape

	# mouse event capture
	cv2.namedWindow('Tracking')
	cv2.setMouseCallback('Tracking', mouseCallback)
	global detectX, detectY
	detectX, detectY = height/4, width/4

	while(True):
		## read the frame and flip
		sucFrame, frame = cap.read()
		frame = cv2.flip(frame, 1)
		backGround = np.zeros((height,width,3), np.uint8)

		## BGR -> HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		## mask the desire color and threshold
		## yellow
		lowerYellow = np.array([10,140,190])
		upperYellow = np.array([45,230,256])
		maskYellow = cv2.inRange(hsv, lowerYellow, upperYellow)
		sucThresh, threshYellow = cv2.threshold(maskYellow, 32, 255, cv2.THRESH_BINARY)

		## pink
		lowerPink = np.array([140,140,120])
		upperPink = np.array([180,220,256])
		maskPink = cv2.inRange(hsv, lowerPink, upperPink)
		sucThresh, threshPink = cv2.threshold(maskPink, 32, 255, cv2.THRESH_BINARY)

		## display small thresh image
		smallFrame = cv2.resize(threshPink, (0,0), fx=0.25, fy=0.25)
		cv2.circle(smallFrame, (smallFrame.shape[1]/2,smallFrame.shape[0]/2), 3, (0,0,255), -1)
		cv2.imshow('small', smallFrame)

		## create objects
		guardian = Character.Guardian()
		princess = Character.Princess()

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
				cv2.circle(backGround, (guardian.x,guardian.y), 40, (0,255,255), 2)

		## pink
		contoursPink = cv2.findContours(threshPink.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		if contoursPink and len(contoursPink) > 0:
			## largest contour
			maxContour = max(contoursPink, key=cv2.contourArea)
			((xPink,yPink), radiusPink) = cv2.minEnclosingCircle(maxContour)
			princess.x, princess.y = int(xPink), int(yPink)

			## draw circles
			if radiusPink > 10:
				cv2.circle(backGround, (princess.x,princess.y), 40, (255,0,255), 2)

		## draw a line
		bullet = Character.Bullet(guardian.x, guardian.y, princess.x, princess.y)
		cv2.line(backGround, (guardian.x,guardian.y), (bullet.endPointX, bullet.endPointY), (0,0,255), 5)

		## detect the point
		# print hsv[detectX][detectY]
		cv2.circle(frame, (detectY, detectX), 5, (255,0,255), -1)

		cv2.imshow('Tracking', frame)
		cv2.imshow('BG', backGround)

		if cv2.waitKey(1) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

main()