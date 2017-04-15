import numpy as np
import cv2
import Character

detectX, detectY = 0, 0

def mouseCallback(event, x, y, flag, param):
	global detectX, detectY
	if event == cv2.EVENT_LBUTTONDOWN:
		detectX, detectY = y, x
		print x, y

def removeArray(list, value):
	if len(list) == 1:
		return
	index = 0
	size = len(list)
	while index != size and not np.array_equal(list[index], value):
		index += 1
	if index != size:
		list.pop(index)
	else:
		raise ValueError('array not found in list. cowbon')

def main():

	cap = cv2.VideoCapture(0)
	height, width, depth = cap.read()[1].shape
	cv2.namedWindow('Tracking')
	cv2.setMouseCallback('Tracking', mouseCallback)
	global detectX, detectY
	detectX, detectY = height/4, width/4

	while(True):
		## read the frame and flip
		sucFrame, frame = cap.read()
		frame = cv2.flip(frame, 1)


		## BGR -> HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		## mask the desire color and threshold
		## yellow
		lowerYellow = np.array([10,140,190])
		upperYellow = np.array([45,230,256])
		maskYellow = cv2.inRange(hsv, lowerYellow, upperYellow)
		sucThresh, threshYellow = cv2.threshold(maskYellow, 32, 255, cv2.THRESH_BINARY)

		## pink
		lowerPink = np.array([140,140,170])
		upperPink = np.array([180,220,256])
		maskPink = cv2.inRange(hsv, lowerPink, upperPink)
		sucThresh, threshPink = cv2.threshold(maskPink, 32, 255, cv2.THRESH_BINARY)

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
			((x,y), radius) = cv2.minEnclosingCircle(maxContour)

			# ## second largest contour
			# removeArray(contoursYellow, maxContour)
			# secMaxContour = max(contoursYellow, key=cv2.contourArea)
			# ((x2,y2), radius2) = cv2.minEnclosingCircle(secMaxContour)

			## draw circles
			if radius > 10:
				cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,0), 2)
				# cv2.circle(frame, (int(x2), int(y2)), int(radius2), (255,255,0), 2)

		## pink
		contoursPink = cv2.findContours(threshPink.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		if contoursPink and len(contoursPink) > 0:
			## largest contour
			maxContour = max(contoursPink, key=cv2.contourArea)
			((xPink,yPink), radiusPink) = cv2.minEnclosingCircle(maxContour)

			## draw circles
			if radiusPink > 10:
				cv2.circle(frame, (int(xPink), int(yPink)), int(radiusPink), (255,255,0), 2)


		## detect the point
		# print hsv[detectX][detectY]
		cv2.circle(frame, (detectY, detectX), 5, (255,0,255), -1)

		cv2.imshow('Tracking', frame)

		key = cv2.waitKey(1)
		if key == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

main()