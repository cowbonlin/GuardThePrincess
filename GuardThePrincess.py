import cv2
import Character
from Game import Game
from time import clock

def main():
	## capture the webCam
	webCam = cv2.VideoCapture(0)

	## create a game
	game = Game(webCam)

	## detect
	detectStartTime = clock()
	game.detectMode(detectStartTime)

	print "Detect Over, Let's play a game!"

	## play
	game.playMode()

	## leave
	webCam.release()
	cv2.destroyAllWindows()

main()