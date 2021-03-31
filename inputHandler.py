import pygame
import constants

class inputHandler:
    def __init__(self, gWorld):     
        #Private internal variables
        self.__sPressed = False
        self.__dPressed = False
        self.__aPressed = False

        #Gameworld reference
        self.__gWorld = gWorld

        #Player reference
        self.__plyr = gWorld.getPlayer()


    #Register a keydown event on WASD
    def registerKeydown(self, event):
        if event.key == pygame.K_w:
            #Jump if not already jumping
            if not self.__plyr.isJumping:
                self.__plyr.isJumping = True
        elif event.key == pygame.K_s:
            self.__sPressed = True
        elif event.key == pygame.K_d:
            self.__dPressed = True
        elif event.key == pygame.K_a:
            self.__aPressed = True

    #Register a keyup event on WASD
    def registerKeyup(self, event):
        if event.key == pygame.K_s:
            self.__sPressed = False
        elif event.key == pygame.K_d:
            self.__dPressed = False
        elif event.key == pygame.K_a:
            self.__aPressed = False

    #Update
    def update(self, timeElapsed):
        if self.__sPressed:
            print('s pressed...')
        if self.__dPressed:
            self.__gWorld.updateBackground((constants.PLAYER_SPEED * timeElapsed, 0))
            self.__plyr.distance+=constants.PLAYER_SPEED * timeElapsed
        if self.__aPressed:
             self.__gWorld.updateBackground((-constants.PLAYER_SPEED * timeElapsed, 0))
             self.__plyr.distance-=constants.PLAYER_SPEED * timeElapsed
    


