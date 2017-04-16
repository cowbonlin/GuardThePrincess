import numpy as np
import cv2
import Character
from math import sqrt
from time import clock
from random import randint

def distance(a, b):
	return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

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

class Game(object):
	def __init__(self, webCam):
		self.webCam = webCam

	def detectMode(self, detectStartTime):
		height, width, depth = self.webCam.read()[1].shape
		while(clock()-detectStartTime < 5):
			## frame setting
			sucFrame, frame = self.webCam.read()
			frame = cv2.flip(frame, 1)

			cv2.circle(frame, (width/2,height/2), 5, (255,0,255), -1)

			cv2.imshow('Tracking', frame)
			if cv2.waitKey(1) == ord('q'):
				break
	
	def playMode(self):
		height, width, depth = self.webCam.read()[1].shape
		frameIndex = 0.0

		## create characters
		guardian = Character.Guardian()
		princess = Character.Princess()
		bulletList = []
		corianderList = []

		while(True):
			startTime = clock()

			## Read the frame and Flip
			sucFrame, frame = self.webCam.read()
			frame = cv2.flip(frame, 1)

			############################################################################################################
			## mask the desire color and threshold
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			threshYellow = produceMask(hsv, [ 10,140,190], [ 45,230,256])
			threshPink   = produceMask(hsv, [140,140,120], [180,220,256])
			
			## set contours
			setContour(threshYellow, guardian)
			setContour(threshPink, princess)

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

			#### HIT CORIANDERS ####
			for bullet in bulletList:
				for coriander in corianderList:
					if not bullet.death and distance(bullet.endPoint, (coriander.x, coriander.y)) <= coriander.radius:
						coriander.death = True
						bullet.death = True
			
			## remove dead corianders
			for coriander in corianderList:
				if coriander.death:
					corianderList.remove(coriander)
					del coriander

			## remove used bullets
			for bullet in bulletList:
				if bullet.death:
					bulletList.remove(bullet)
					del bullet

			#### Princess Dead ####
			for coriander in corianderList:
				if distance((princess.x,princess.y), (coriander.x,coriander.y)) <= princess.radius+coriander.radius:
					cv2.putText(frame, "GAME OVER", (width/2,height/2), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0))

			############################################################################################################
			#### DRAW ####
			## bullets
			for bullet in bulletList:
				bullet.updatePosition()
				bullet.draw(frame)

			## corianders
			for coriander in corianderList:
				coriander.draw(frame)

			## guardian and princess
			guardian.draw(frame)
			princess.draw(frame)
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
			endTime = clock()
			print 1 / (endTime - startTime)

	def gameOver(self):
		pass