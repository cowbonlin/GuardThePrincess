from math import sqrt

class Princess(object):
	def __init__(self):
		self.x = 0
		self.y = 0

class Guardian(object):
	def __init__(self):
		self.x = 50
		self.y = 50

class Bullet(object):
	def __init__(self, gX, gY, pX, pY):
		originVX, originVY = gX - pX, gY - pY
		constant = 50
		self.vecterX = originVX / sqrt(originVX**2 + originVY**2)
		self.vecterY = originVY / sqrt(originVX**2 + originVY**2)
		self.endPointX = int(gX + self.vecterX * constant)
		self.endPointY = int(gY + self.vecterY * constant)