from math import sqrt
import cv2

pink = (255,0,255)
yellow = (0,255,255)
red = (0,0,255)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)
scoreRed = (45,38,141)
corianderGreen = (45,137,100)


def normalize(vector):
	if vector==(0,0):
		return (0,0)
	return (vector[0]/sqrt(vector[0]**2+vector[1]**2), vector[1]/sqrt(vector[0]**2+vector[1]**2))

class Princess(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.radius = 30
		self.life = 3
	def draw(self, image):
		cv2.circle(image, (self.x,self.y), self.radius, pink, -1)

class Guardian(object):
	def __init__(self):
		self.x = 50
		self.y = 50
		self.radius = 40
	def draw(self, image):
		cv2.circle(image, (self.x,self.y), self.radius, yellow, -1)

class Coriander(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.radius = 50
		self.death = False
	def draw(self, image):
		cv2.circle(image, (self.x,self.y), self.radius, corianderGreen, -1)
	def updatePosition(self, princess, score):
		vConst = 10 + 5*score/10
		vector = normalize((princess.x-self.x, princess.y-self.y))
		self.x += int(vConst*vector[0])
		self.y += int(vConst*vector[1])

class Bullet(object):
	def __init__(self, gX, gY, pX, pY, frameIndex):
		originV = (gX-pX, gY-pY)
		lengConst = 50
		self.vector = normalize(originV)
		self.strPoint = (gX, gY)
		self.endPoint = (int(gX + lengConst*self.vector[0]), int(gY + lengConst*self.vector[1]))
		self.bornIndex = frameIndex
		self.death = False
	def updatePosition(self):
		vConst = 50
		self.strPoint = (self.strPoint[0]+int(self.vector[0]*vConst), self.strPoint[1]+int(self.vector[1]*vConst))
		self.endPoint = (self.endPoint[0]+int(self.vector[0]*vConst), self.endPoint[1]+int(self.vector[1]*vConst))
	def draw(self, image):
		cv2.line(image, self.strPoint, self.endPoint, red, 5)














