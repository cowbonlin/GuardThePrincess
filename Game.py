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

def countDown(time, clock, startTime, frame, text):
	if time<clock-startTime<time+1:
		cv2.putText(frame, text.format(3-time), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, Character.black)

detectX, detectY = 0, 0
def mouseCallback(event, x, y, flag, param):
	global detectX, detectY
	if event == cv2.EVENT_LBUTTONDOWN:
		detectX, detectY = y, x
		print x, y

class Game(object):
	def __init__(self, webCam):
		self.webCam = webCam
		self.height, self.width, self.depth = webCam.read()[1].shape
		self.yellowMax = [0,0,0]
		self.yellowMin = [255,255,255]
		self.pinkMax = [0,0,0]
		self.pinkMin = [255,255,255]

	def prepareToDetect(self, startTime, index):
		while clock()-startTime < 3:
			frame = cv2.flip(self.webCam.read()[1], 1)
			if index == 0:
				cv2.circle(frame, (self.width/2,self.height/2), 10, Character.red, -1)
			elif index == 1:
				cv2.circle(frame, (self.width/7,self.height/7), 10, Character.red, -1)
			elif index == 2:
				cv2.circle(frame, (6*self.width/7,self.height/7), 10, Character.red, -1)
			elif index == 3:
				cv2.circle(frame, (6*self.width/7,6*self.height/7), 10, Character.red, -1)
			else:
				cv2.circle(frame, (self.width/7,6*self.height/7), 10, Character.red, -1)

			## count to 3
			for time in range(3):
				countDown(time, clock(), startTime, frame, "Please put the ball to the detect point in {0} seconds")
			
			## show frame and key interrup						
			cv2.imshow('Detect', frame)
			if cv2.waitKey(1) == ord('q'):
				break

	def detectTest(self):
		cv2.namedWindow('Detect')
		cv2.setMouseCallback('Detect', mouseCallback)
		global detectX, detectY
		detectX, detectY = self.height/4, self.width/4
		while True:
			frame = cv2.flip(self.webCam.read()[1], 1)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			print hsv[detectX][detectY]
			cv2.circle(frame, (detectY,detectX), 10, Character.red, -1)

			cv2.imshow("Detect", frame)
			if cv2.waitKey(1) == ord('q'):
				break

	def detecting(self, startTime, index, type):
		maxHSV  = [0,0,0]
		minHSV  = [255,255,255]

		while clock()-startTime < 2:
			## frame setup
			frame = cv2.flip(self.webCam.read()[1], 1)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			height, width, depth = frame.shape

			## count to 3
			for time in range(3):
				countDown(time, clock(), startTime, frame, "Detecting... {0} seconds left")
			
			if index == 0:
				cv2.circle(frame, (self.width/2,self.height/2), 10, Character.red, -1)
				detectPoint = hsv[self.height/2][self.width/2]
			elif index == 1:
				cv2.circle(frame, (self.width/7,self.height/7), 10, Character.red, -1)
				detectPoint = hsv[self.height/7][self.width/7]
			elif index == 2:
				cv2.circle(frame, (6*self.width/7,self.height/7), 10, Character.red, -1)
				detectPoint = hsv[self.height/7][6*self.width/7]
			elif index == 3:
				cv2.circle(frame, (6*self.width/7,6*self.height/7), 10, Character.red, -1)
				detectPoint = hsv[6*self.height/7][6*self.width/7]
			else:
				cv2.circle(frame, (self.width/7,6*self.height/7), 10, Character.red, -1)
				detectPoint = hsv[6*self.height/7][self.width/7]
			
			print detectPoint

			## detecting...
			minHSV  = [min(minHSV[i], detectPoint[i]) for i in range(3)]
			maxHSV  = [max(maxHSV[i], detectPoint[i]) for i in range(3)]

			## show frame and key interrup
			cv2.imshow('Detect', frame)
			if cv2.waitKey(1) == ord('q'):
				break
		
		print "min{0} : ".format(index), minHSV
		print "max{0} : ".format(index), maxHSV
		if type == "yellow":
			self.yellowMin = [min(self.yellowMin[i], minHSV[i]) for i in range(3)]
			self.yellowMax = [max(self.yellowMax[i], maxHSV[i]) for i in range(3)]
		elif type == "pink":
			self.pinkMin = [min(self.pinkMin[i], minHSV[i]) for i in range(3)]
			self.pinkMax = [max(self.pinkMax[i], maxHSV[i]) for i in range(3)]

	def detectMode(self):
		# ## detect yellow
		# for i in range(5):
		# 	startTime = clock()
		# 	self.prepareToDetect(startTime, i)
		
		# 	startTime = clock()
		# 	self.detecting(startTime, i, "yellow")
		# self.yellowMin = [min(max(self.yellowMin[i]-20, 0), 255) for i in range(3)]
		# self.yellowMax = [min(max(self.yellowMax[i]+20, 0), 255) for i in range(3)]
		# print "MIN YELLOW: ", self.yellowMin
		# print "MAX YELLOW: ", self.yellowMax

		## detect pink
		for i in range(5):
			startTime = clock()
			self.prepareToDetect(startTime, i)
		
			startTime = clock()
			self.detecting(startTime, i, "pink")
		self.pinkMin = [min(max(self.pinkMin[i]-20, 0), 256) for i in range(3)]
		self.pinkMax = [min(max(self.pinkMax[i]+20, 0), 256) for i in range(3)]
		print "MIN PINK: ", self.pinkMin
		print "MAX PINK: ", self.pinkMax


		

	def playMode(self):
		height, width, depth = self.webCam.read()[1].shape
		frameIndex = 0.0

		## create characters
		guardian = Character.Guardian()
		princess = Character.Princess()
		bulletList = []
		corianderList = []

		while True:
			startTime = clock()

			## Read the frame and Flip
			frame = cv2.flip(self.webCam.read()[1], 1)

			############################################################################################################
			## mask the desire color and threshold
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			# threshYellow = produceMask(hsv, [ 10,140,190], [ 45,230,256])
			# threshPink   = produceMask(hsv, [140,140,120], [180,220,256])
			threshYellow = produceMask(hsv, self.yellowMin, self.yellowMax)
			threshPink   = produceMask(hsv, self.pinkMin,   self.pinkMax)
			
			
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

			############################################################################################################
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

			############################################################################################################
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
					cv2.putText(frame, "GAME OVER", (width/2,height/2), cv2.FONT_HERSHEY_DUPLEX, 2, Character.green)

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
			## show the frame
			cv2.imshow('Tracking', threshPink)

			## key interruption
			if cv2.waitKey(1) == ord('q'):
				break

			frameIndex += 1

			## calculate FPS
			endTime = clock()
			print 1 / (endTime - startTime)

	def gameOver(self):
		pass