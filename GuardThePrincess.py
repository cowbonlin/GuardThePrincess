import numpy as np
import cv2
import Character
from math import sqrt
from time import clock
from random import randint

detectX, detectY = 0, 0

def distance(a, b):
	return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

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

def setContour(thresh, character):
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	if contours and len(contours) > 0:
		maxContour = max(contours, key=cv2.contourArea)
		((x,y), radius) = cv2.minEnclosingCircle(maxContour)
		character.x, character.y = int(x), int(y)


def main():
	cap = cv2.VideoCapture(0)
	height, width, depth = cap.read()[1].shape
	frameIndex = 0.0

	## create characters
	guardian = Character.Guardian()
	princess = Character.Princess()
	bulletList = []
	corianderList = []

	# mouse event capture
	cv2.namedWindow('Tracking')
	cv2.setMouseCallback('Tracking', mouseCallback)
	global detectX, detectY
	detectX, detectY = height/4, width/4

	while(True):
		# startTime = clock()

		## Read the frame and Flip
		sucFrame, frame = cap.read()
		frame = cv2.flip(frame, 1)

		## mask the desire color and threshold
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		threshYellow = produceMask(hsv, [ 10,140,190], [ 45,230,256])
		threshPink   = produceMask(hsv, [140,140,120], [180,220,256])
		
		## set contours
		setContour(threshYellow, guardian)
		setContour(threshPink, princess)

		## draw guardian and princess
		guardian.draw(frame)
		princess.draw(frame)

		############################################################################################################
		#### BULLET ####
		## delete outrange bullets
		for bullet in bulletList:
			if bullet.strPoint[0] > width or bullet.strPoint[0] < 0 or bullet.strPoint[1] > height or bullet.strPoint[1] < 0:
				bulletList.remove(bullet)
				del bullet

		## new bullet
		fireRate = int(6 * sqrt((guardian.x-princess.x)**2 + (guardian.y-princess.y)**2) / 1000) + 2
		if frameIndex % fireRate == 0:
			bullet = Character.Bullet(guardian.x, guardian.y, princess.x, princess.y, frameIndex)
			bulletList.append(bullet)

		## draw bullets
		for bullet in bulletList:
			bullet.updatePosition()
			bullet.draw(frame)

		#### CORIANDER ####
		## new coriander
		if frameIndex % 10 ==0:
			luckyNumber = randint(0,1280)
			if   luckyNumber % 4 == 0:
				coriander = Character.Coriander(luckyNumber, 0)
			elif luckyNumber % 4 == 1:
			 	coriander = Character.Coriander(luckyNumber, height)
			elif luckyNumber % 4 == 2:
			 	coriander = Character.Coriander(0, luckyNumber%720)
			else:
				coriander = Character.Coriander(width, luckyNumber%720)
			corianderList.append(coriander)

		## move toward the princess
		for coriander in corianderList:
			coriander.updatePosition(princess)

		## bullet hit corianders!
		for bullet in bulletList:
			for coriander in corianderList:
				if not bullet.death and distance(bullet.endPoint, (coriander.x, coriander.y)) <= coriander.radius:
					coriander.death = True
					bullet.death = True
		
		## remove dead corianders and used bullets
		for coriander in corianderList:
			if coriander.death:
				corianderList.remove(coriander)
				del coriander

		for bullet in bulletList:
			if bullet.death:
				bulletList.remove(bullet)
				del bullet

		## draw corianders
		for coriander in corianderList:
			coriander.draw(frame)

		############################################################################################################

		## detect the point
		# print hsv[detectX][detectY]
		# cv2.circle(frame, (detectY, detectX), 5, (255,0,255), -1)

		## show the frame
		cv2.imshow('Tracking', frame)

		## key interruption
		if cv2.waitKey(1) == ord('q'):
			break

		frameIndex += 1

		## calculate FPS
		# endTime = clock()
		# print 1 / (endTime - startTime)

	cap.release()
	cv2.destroyAllWindows()

main()