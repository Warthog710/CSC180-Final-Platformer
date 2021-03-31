import pygame
import constants

from inputHandler import inputHandler

class player:
    def __init__(self, pos):
        #Textures
        self.__texture = pygame.image.load('./assets/player.png').convert()
        self.__slidingTex = pygame.image.load('./assets/sliding.png').convert()

        #Position. CurrentY holds the y cord the texture will be drawn at. OriginalY holds the original value so we can reset it later
        self.__pos = pos
        self.__originalY = self.__pos[1] - (self.__texture.get_height() + constants.PLAYER_HEIGHT_ADJUST)
        self.__currentY = self.__originalY

        #Player speed and jump velocity (power)
        self.__jumpPower = constants.PLAYER_JUMP_VELOCITY
        self.playerSpeed = constants.PLAYER_SPEED

        #Boolean flags
        self.isJumping = False
        self.isSliding = False
        self.movingFwd = False
        self.movingBwd = False
        self.__slidingTextureInUse = False

        #States to maintain the last facing position. This prevent us from restoring the default position if nothing is being pressed
        self.__states = ['bwd', 'fwd']
        self.__lastState = self.__states[1]

        #Scale player (both slidng and normal texture)
        imgSize = self.__texture.get_size()
        slidingSize = self.__slidingTex.get_size()
        self.__texture = pygame.transform.scale(self.__texture, (int(imgSize[0] * constants.PLAYER_SCALE), int(imgSize[0] * constants.PLAYER_SCALE)))
        self.__slidingTex = pygame.transform.scale(self.__slidingTex, (int(slidingSize[0] * constants.PLAYER_SCALE), int(slidingSize[0] * constants.PLAYER_SCALE)))

        #Rotate the sliding image
        self.__slidingTex = pygame.transform.rotate(self.__slidingTex, constants.PLAYER_SLIDING_ROTATION)


    def updateJump(self, timeElapsed):
        #If sliding, reset the slide
        if self.isSliding and self.isJumping:
            self.__slidingTextureInUse = False
            self.isSliding = False
            
            #Reset height
            self.__currentY = self.__originalY

            #Restore player speed
            self.playerSpeed = constants.PLAYER_SPEED

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

    #? Player speed slowly decays while we are sliding...
    def updateSlide(self):            
        #If not jumping, and sliding is true, and I am not rotated...
        if self.isSliding and not self.__slidingTextureInUse:
            #Modifiy player height
            self.__currentY += constants.PLAYER_SLIDING_OFFSET

            #Set sliding texture to true
            self.__slidingTextureInUse = True

        #If I am currently sliding slowly decay the player speed
        elif self.isSliding and self.__slidingTextureInUse:
            self.playerSpeed -= constants.PLAYER_SLIDING_DECAY

            #Speed cannot fall below zero
            if self.playerSpeed < 0:
                self.playerSpeed = 0

        #If I am no longer sliding but still have the sliding texture, reset it
        elif not self.isSliding and self.__slidingTextureInUse:
            self.__slidingTextureInUse = False

            #Reset height
            self.__currentY = self.__originalY

            #Restore player speed
            self.playerSpeed = constants.PLAYER_SPEED

    def draw(self, screen):
        #If we are sliding
        if not self.__slidingTextureInUse:
            #Flip the texture if we are moving back
            if self.movingBwd:
                screen.blit(pygame.transform.flip(self.__texture, True, False), (self.__pos[0] - self.__texture.get_width(), self.__currentY))
                self.__lastState = self.__states[0]
            elif self.movingFwd:
                screen.blit(self.__texture, (self.__pos[0] - self.__texture.get_width(), self.__currentY))
                self.__lastState = self.__states[1]
            #If none of the above are true, draw based on the last state
            else:
                if self.__lastState == self.__states[0]:
                    screen.blit(pygame.transform.flip(self.__texture, True, False), (self.__pos[0] - self.__texture.get_width(), self.__currentY))
                else:
                    screen.blit(self.__texture, (self.__pos[0] - self.__texture.get_width(), self.__currentY))
        else:
            if self.movingBwd:
                #Flip the texture if we are moving back
                screen.blit(pygame.transform.flip(self.__slidingTex, True, False), (self.__pos[0] - self.__texture.get_width(), self.__currentY))
                self.__lastState = self.__states[0]
            elif self.movingFwd:
                screen.blit(self.__slidingTex, (self.__pos[0] - self.__texture.get_width(), self.__currentY))
                self.__lastState = self.__states[0]
            #If none of the above are true, draw based on the last state
            else:
                if self.__lastState == self.__states[0]:
                    screen.blit(pygame.transform.flip(self.__slidingTex, True, False), (self.__pos[0] - self.__texture.get_width(), self.__currentY))
                else:
                    screen.blit(self.__slidingTex, (self.__pos[0] - self.__texture.get_width(), self.__currentY))
        

    