import numpy as np
import cv2
import Character
from math import sqrt
from time import clock
from random import randint

def putTextCenter(image, text, position, font, size, color, thickness):
	center = (cv2.getTextSize(text, font, size, thickness)[0][0]/2, cv2.getTextSize(text, font, size, thickness)[0][1]/2)
	cv2.putText(image, text, (position[0]-center[0], position[1]+center[1]), font, size, color, thickness)

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

def countDown(time, clock, startTime, frame, text, timeToCount, position, color):
	if time<clock-startTime<time+1:
		putTextCenter(frame, text.format(timeToCount-time), (position[0], position[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

detectX, detectY = 0, 0
def mouseCallback(event, x, y, flag, param):
	global detectX, detectY
	if event == cv2.EVENT_LBUTTONDOWN:
		detectX, detectY = y, x
		print x, y

class Game(object):
	def __init__(self):
		self.webCam = cv2.VideoCapture(0)
		self.height, self.width, self.depth = self.webCam.read()[1].shape
		self.yellowMax = [0,0,0]
		self.yellowMin = [255,255,255]
		self.pinkMax = [0,0,0]
		self.pinkMin = [255,255,255]
		self.score = 0
		self.gameOver = False

	def prepareToDetect(self, startTime, index):
		while clock()-startTime < 3:
			frame = cv2.flip(self.webCam.read()[1], 1)

			## draw circle 
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
				if   index == 0:
					countDown(time, clock(), startTime, frame, "Detect in {0} seconds", 3, (self.width/2,self.height/2), Character.corianderGreen)
				elif index == 1:
					countDown(time, clock(), startTime, frame, "Detect in {0} seconds", 3, (self.width/7,self.height/7), Character.corianderGreen)
				elif index == 2:
					countDown(time, clock(), startTime, frame, "Detect in {0} seconds", 3, (6*self.width/7,self.height/7), Character.corianderGreen)
				elif index == 3:
					countDown(time, clock(), startTime, frame, "Detect in {0} seconds", 3, (6*self.width/7,6*self.height/7), Character.corianderGreen)
				else:
					countDown(time, clock(), startTime, frame, "Detect in {0} seconds", 3, (self.width/7,6*self.height/7), Character.corianderGreen)
			
			## show frame and key interrup						
			cv2.imshow('Detect', frame)
			if cv2.waitKey(1) == ord('q'):
				break

	# def detectTest(self):
	# 	cv2.namedWindow('Detect')
	# 	cv2.setMouseCallback('Detect', mouseCallback)
	# 	global detectX, detectY
	# 	detectX, detectY = self.height/4, self.width/4
	# 	while True:
	# 		frame = cv2.flip(self.webCam.read()[1], 1)
	# 		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# 		print hsv[detectX][detectY]
	# 		cv2.circle(frame, (detectY,detectX), 10, Character.red, -1)

	# 		cv2.imshow("Detect", frame)
	# 		if cv2.waitKey(1) == ord('q'):
	# 			break

	def detecting(self, startTime, index, type):
		maxHSV  = [0,0,0]
		minHSV  = [255,255,255]

		## detect in 1 seconds
		while clock()-startTime < 1:
			## frame setup
			frame = cv2.flip(self.webCam.read()[1], 1)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			height, width, depth = frame.shape

			## count to 1
			for time in range(1):
				if   index == 0:
					countDown(time, clock(), startTime, frame, "Detecting...", 1, (self.width/2,self.height/2), Character.red)
				elif index == 1:
					countDown(time, clock(), startTime, frame, "Detecting...", 1, (self.width/7,self.height/7), Character.red)
				elif index == 2:
					countDown(time, clock(), startTime, frame, "Detecting...", 1, (6*self.width/7,self.height/7), Character.red)
				elif index == 3:
					countDown(time, clock(), startTime, frame, "Detecting...", 1, (6*self.width/7,6*self.height/7), Character.red)
				else:
					countDown(time, clock(), startTime, frame, "Detecting...", 1, (self.width/7,6*self.height/7), Character.red)
			
			
			## draw detect circle
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
		#### detect yellow ####
		## prepare and detect
		for i in range(5):
			self.prepareToDetect(clock(), i)
			self.detecting(clock(), i, "yellow")
		## store the min and max hsv value
		self.yellowMin = [min(max(self.yellowMin[i]-10, 0), 255) for i in range(3)]
		self.yellowMax = [min(max(self.yellowMax[i]+10, 0), 255) for i in range(3)]
		print "MIN YELLOW: ", self.yellowMin
		print "MAX YELLOW: ", self.yellowMax

		#### detect pink ####
		## prepare and detect
		for i in range(5):
			self.prepareToDetect(clock(), i)
			self.detecting(clock(), i, "pink")
		## store the min and max hsv value
		self.pinkMin = [min(max(self.pinkMin[i]-10, 0), 255) for i in range(3)]
		self.pinkMax = [min(max(self.pinkMax[i]+10, 0), 255) for i in range(3)]
		print "MIN PINK: ", self.pinkMin
		print "MAX PINK: ", self.pinkMax

		## close the detect window
		cv2.destroyAllWindows()
		self.playMode()

	def playMode(self):
		frameIndex = 0.0

		## create characters
		guardian = Character.Guardian()
		princess = Character.Princess()
		bulletList = []
		corianderList = []

		while not self.gameOver:
			startTime = clock()

			## Read the frame and Flip
			frame = cv2.flip(self.webCam.read()[1], 1)

			############################################################################################################
			## mask the desire color and threshold
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			threshYellow = produceMask(hsv, [  3,148,195], [ 34,245,255])
			threshPink   = produceMask(hsv, [140,109,149], [174,216,255])
			# threshYellow = produceMask(hsv, self.yellowMin, self.yellowMax)
			# threshPink   = produceMask(hsv, self.pinkMin,   self.pinkMax)
			
			
			## set contours
			setContour(threshYellow, guardian)
			setContour(threshPink, princess)

			frame = cv2.blur(cv2.cvtColor(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR), (22,22))

			############################################################################################################
			#### BULLET ####
			## delete outrange bullets
			for bullet in bulletList:
				if bullet.strPoint[0] > self.width or bullet.strPoint[0] < 0 or bullet.strPoint[1] > self.height or bullet.strPoint[1] < 0:
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
				 	coriander = Character.Coriander(luckyNumber, self.height)
				elif luckyNumber % 4 == 2:
				 	coriander = Character.Coriander(0, luckyNumber%720)
				else:
					coriander = Character.Coriander(self.width, luckyNumber%720)
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
						self.score += 1
			
			## remove used bullets
			for bullet in bulletList:
				if bullet.death:
					bulletList.remove(bullet)
					del bullet

			#### PPINCESS GETS HIT ####
			for coriander in corianderList:
				if distance((princess.x,princess.y), (coriander.x,coriander.y)) <= princess.radius+coriander.radius:
					princess.life -= 1
					# self.score = 0
					coriander.death = True

			## remove dead corianders
			for coriander in corianderList:
				if coriander.death:
					corianderList.remove(coriander)
					del coriander

			######################################  Princess Die: Game Over  ###########################################
			if princess.life == 0:
				self.gameOver = True

			################################################  Draw  ####################################################
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

			## score
			putTextCenter(frame, "SCORE: "+str(self.score), (self.width/2, self.height/10), cv2.FONT_HERSHEY_SIMPLEX, 1, Character.scoreRed, 2)
			############################################################################################################
			## show the frame
			cv2.imshow('Tracking', frame)

			## key interruption
			if cv2.waitKey(1) == ord('q'):
				break

			frameIndex += 1

			## calculate FPS
			endTime = clock()
			print 1 / (endTime - startTime)

		cv2.destroyAllWindows()

		self.heavenMode()

	def heavenMode(self):
		self.gameOver = False
		enterMode = None

		## create characters
		guardian = Character.Guardian()
		duration = guardian.radius

		while not enterMode:
			frame = cv2.flip(self.webCam.read()[1], 1)

			############################################################################################################
			## mask the desire color and threshold
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			threshYellow = produceMask(hsv, [  3,148,195], [ 34,245,255])
			# threshYellow = produceMask(hsv, self.yellowMin, self.yellowMax)
			
			
			## set contours
			setContour(threshYellow, guardian)

			frame = cv2.blur(frame, (22,22))

			################################################  Enter  ###################################################
			if duration == 2:
				if distance((guardian.x,guardian.y), (self.width/2, 3*self.height/4)) <= 80:
					enterMode = "Again"
				elif distance((guardian.x,guardian.y), (self.width/4, 3*self.height/4)) <= 80:
					enterMode = "Detect"
				elif distance((guardian.x,guardian.y), (3*self.width/4, 3*self.height/4)) <= 80:
					enterMode = "Leave"

			################################################  Select  ###################################################
			if distance((guardian.x,guardian.y), (  self.width/2, 3*self.height/4)) <= 80 or \
			   distance((guardian.x,guardian.y), (  self.width/4, 3*self.height/4)) <= 80 or \
			   distance((guardian.x,guardian.y), (3*self.width/4, 3*self.height/4)) <= 80:
				duration -= 2
			else:
				if duration < 40:
					duration += 2


			################################################  Draw  ####################################################
			## score
			putTextCenter(frame, "Your Score", (self.width/2, self.height/7), cv2.FONT_HERSHEY_SIMPLEX, 0.8, Character.corianderGreen, 2)
			putTextCenter(frame, str(self.score), (self.width/2, self.height/4), cv2.FONT_HERSHEY_SIMPLEX, 3, Character.corianderGreen, 3)
			
			## guardian
			cv2.circle(frame, (guardian.x,guardian.y), duration, Character.yellow, -1)

			## mode selection
			cv2.circle(frame, (self.width/2, 3*self.height/4), 80, Character.corianderGreen, 2)
			putTextCenter(frame, "Again", (self.width/2, 3*self.height/4), cv2.FONT_HERSHEY_SIMPLEX, 1.3, Character.corianderGreen, 3)

			cv2.circle(frame, (self.width/4, 3*self.height/4), 80, Character.corianderGreen, 2)
			putTextCenter(frame, "Detect", (self.width/4, 3*self.height/4), cv2.FONT_HERSHEY_SIMPLEX, 1.3, Character.corianderGreen, 3)

			cv2.circle(frame, (3*self.width/4, 3*self.height/4), 80, Character.corianderGreen, 2)
			putTextCenter(frame, "Leave", (3*self.width/4, 3*self.height/4), cv2.FONT_HERSHEY_SIMPLEX, 1.3, Character.corianderGreen, 3)

			## game over
			putTextCenter(frame, "GAME OVER", (self.width/2, self.height/2), cv2.FONT_HERSHEY_SIMPLEX, 2, Character.corianderGreen, 7)

			############################################################################################################
			cv2.imshow("Heaven", frame)
			if cv2.waitKey(1) == ord('q'):
				break

		cv2.destroyAllWindows()
		if   enterMode == "Again":
			self.score = 0
			self.playMode()
		elif enterMode == "Detect":
			self.detectMode()
		elif enterMode == "Leave":
			self.leaveGame()

	def leaveGame(self):
		self.webCam.release()
		cv2.destroyAllWindows()