import pygame

from datetime import datetime

class inputHandler:
    def __init__(self, gWorld):     
        #Private internal variables
        self.__dPressed = False
        self.__aPressed = False

        #Gameworld reference
        self.__gWorld = gWorld

        #Player reference
        self.__plyr = gWorld.getPlayer()
        self.__obst = gWorld.getObstacles()

        #Last action time
        self.lastAction = datetime.now()

    #Register a keydown event on WASD
    def registerKeydown(self, event):
        if event.key == pygame.K_w:
            #Jump if not already jumping and not sliding
            if not self.__plyr.isJumping and not self.__plyr.isSliding:
                self.__plyr.isJumping = True
                self.__plyr.onObject = False
                self.lastAction = datetime.now()
        elif event.key == pygame.K_s:
            #Set is sliding to true only if we are not jump and not on an object
            if not self.__plyr.isJumping and not self.__plyr.onObject:
                self.__plyr.isSliding = True

                #If sliding would make the player collide, revert the slide
                if self.__obst.detectCollision():
                    self.__plyr.isSliding = False
                else:
                    self.lastAction = datetime.now()
        elif event.key == pygame.K_d:
            self.__dPressed = True
            self.lastAction = datetime.now()
        elif event.key == pygame.K_a:
            self.__aPressed = True
            self.lastAction = datetime.now()

    #Register a keyup event on WASD
    def registerKeyup(self, event):
        if event.key == pygame.K_s:
            #Set is sliding to false on a key up
            self.__plyr.isSliding = False
        elif event.key == pygame.K_d:
            self.__dPressed = False
            self.__plyr.movingFwd = False
        elif event.key == pygame.K_a:
            self.__aPressed = False
            self.__plyr.movingBwd = False

    #Update
    def update(self, timeElapsed):
        if self.__dPressed:
            self.__gWorld.updateBackground((self.__plyr.playerSpeed * timeElapsed, 0))
            self.__plyr.distance += (self.__plyr.playerSpeed * timeElapsed)
            self.__plyr.movingFwd = True
            self.lastAction = datetime.now()

            #If we collide revert the changes
            if self.__obst.detectCollision():
                self.__gWorld.updateBackground((-self.__plyr.playerSpeed * timeElapsed, 0))
                self.__plyr.distance -= (self.__plyr.playerSpeed * timeElapsed)
                self.__plyr.movingFwd = False

        if self.__aPressed:
             self.__gWorld.updateBackground((-self.__plyr.playerSpeed * timeElapsed, 0))
             self.__plyr.distance -= (self.__plyr.playerSpeed * timeElapsed)
             self.__plyr.movingBwd = True
             self.lastAction = datetime.now()

            #If we collide revert the changes
             if self.__obst.detectCollision():
                self.__gWorld.updateBackground((self.__plyr.playerSpeed * timeElapsed, 0))
                self.__plyr.distance += (self.__plyr.playerSpeed * timeElapsed)
                self.__plyr.movingBwd = False
        
        if self.__plyr.forcedSlide:
            self.__plyr.isSliding = False


