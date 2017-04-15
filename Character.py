from math import sqrt
import cv2

pink = (255,0,255)
yellow = (0,255,255)
red = (0,0,255)

class Princess(object):
	def __init__(self):
		self.x = 0
		self.y = 0
	def draw(self, image):
		cv2.circle(image, (self.x,self.y), 40, pink, 2)

class Guardian(object):
	def __init__(self):
		self.x = 50
		self.y = 50
	def draw(self, image):
		cv2.circle(image, (self.x,self.y), 40, yellow, 2)

class Bullet(object):
	def __init__(self, gX, gY, pX, pY, frameIndex):
		originV = (gX-pX, gY-pY)
		lengConst = 50

		self.vector = (originV[0]/sqrt(originV[0]**2 + originV[1]**2), originV[1]/sqrt(originV[0]**2 + originV[1]**2))
		self.strPoint = (gX, gY)
		self.endPoint = (int(gX + lengConst*self.vector[0]), int(gY + lengConst*self.vector[1]))

		self.bornIndex = frameIndex

	def updatePosition(self, vConst):
		self.strPoint = (self.strPoint[0]+int(self.vector[0]*vConst), self.strPoint[1]+int(self.vector[1]*vConst))
		self.endPoint = (self.endPoint[0]+int(self.vector[0]*vConst), self.endPoint[1]+int(self.vector[1]*vConst))

	def draw(self, image):
		cv2.line(image, self.strPoint, self.endPoint, red, 5)














