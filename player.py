import pygame
import constants

from inputHandler import inputHandler

class player:
    def __init__(self, pos):
        self.__texture = pygame.image.load('./assets/player.png').convert()
        self.__pos = pos
        self.isJumping = False
        self.__originalY = self.__pos[1] - (self.__texture.get_height() + constants.PLAYER_HEIGHT_ADJUST)
        self.__currentY = self.__originalY
        self.__jumpPower = constants.PLAYER_JUMP_VELOCITY
        self.distance=0

        #Scale player
        imgSize = self.__texture.get_size()
        self.__texture = pygame.transform.scale(self.__texture, (int(imgSize[0] * constants.PLAYER_SCALE), int(imgSize[0] * constants.PLAYER_SCALE)))

    def updateJump(self, timeElapsed):
        #If jumping
        if self.isJumping:
            if self.__jumpPower >= -constants.PLAYER_JUMP_VELOCITY:
                neg = 1
                if self.__jumpPower < 0:
                    neg = -1
                
                #Modify height
                self.__currentY -= self.__jumpPower**2 * 0.1 * neg * timeElapsed

                #Decay power by gravity
                self.__jumpPower -= constants.GRAVITY

            #Else, done jumping, reset everything
            else:
                self.__jumpPower = constants.PLAYER_JUMP_VELOCITY
                self.__currentY = self.__originalY
                self.isJumping = False

    def draw(self, screen):
        screen.blit(self.__texture, (self.__pos[0] - self.__texture.get_width(), self.__currentY))
        

    