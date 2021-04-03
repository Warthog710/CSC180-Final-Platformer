import pygame
import constants

from inputHandler import inputHandler

class player:
    def __init__(self, pos):
        #Textures
        self.__idleTextures = [pygame.image.load('./assets/idle0.png').convert(), pygame.image.load('./assets/idle1.png').convert(), 
                                pygame.image.load('./assets/idle2.png').convert(), pygame.image.load('./assets/idle3.png').convert()]

        self.__runTextures = [pygame.image.load('./assets/run0.png').convert(), pygame.image.load('./assets/run1.png').convert(), 
                                pygame.image.load('./assets/run2.png').convert(), pygame.image.load('./assets/run3.png').convert(), 
                                pygame.image.load('./assets/run4.png').convert(), pygame.image.load('./assets/run5.png').convert()]

        self.__slidingTex = pygame.image.load('./assets/sliding.png').convert()
        self.__jumpingTex = pygame.image.load('./assets/jump.png').convert()
        self.__texture = self.__idleTextures[0]

        #Animation indexes
        self.__idleIndex = 0
        self.__runningIndex = 0

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
        self.__animationStates = ['WALKING', 'IDLE', 'SLIDING', 'JUMPING']
        self.__states = ['bwd', 'fwd']
        self.__lastState = self.__states[1]

        #Scale player textures
        imgSize = self.__texture.get_size()
        slidingSize = self.__slidingTex.get_size()
        jmpSize = self.__jumpingTex.get_size()
        self.__texture = pygame.transform.scale(self.__texture, (int(imgSize[0] * constants.PLAYER_SCALE), int(imgSize[0] * constants.PLAYER_SCALE)))
        self.__slidingTex = pygame.transform.scale(self.__slidingTex, (int(slidingSize[0] * constants.PLAYER_SCALE), int(slidingSize[0] * constants.PLAYER_SCALE)))
        self.__jumpingTex = pygame.transform.scale(self.__jumpingTex, (int(jmpSize[0] * constants.PLAYER_SCALE), int(jmpSize[0] * constants.PLAYER_SCALE)))

        for x in range(0, len(self.__idleTextures)):
            imgSize = self.__idleTextures[x].get_size()
            self.__idleTextures[x] = pygame.transform.scale(self.__idleTextures[x], (int(imgSize[0] * constants.PLAYER_SCALE), int(imgSize[0] * constants.PLAYER_SCALE)))

        for x in range(0, len(self.__runTextures)):
            imgSize = self.__runTextures[x].get_size()
            self.__runTextures[x] = pygame.transform.scale(self.__runTextures[x], (int(imgSize[0] * constants.PLAYER_SCALE), int(imgSize[0] * constants.PLAYER_SCALE)))

        #Rotate the sliding image
        self.__slidingTex = pygame.transform.rotate(self.__slidingTex, constants.PLAYER_SLIDING_ROTATION)

    #Returns the state of the player
    #? Possible States: [WALKING, IDLE, SLIDING, JUMPING]
    def __getAnimationState(self):
        if self.isJumping:
            return self.__animationStates[3]
        elif self.isSliding:
            return self.__animationStates[2]
        elif self.movingBwd or self.movingFwd:
            return self.__animationStates[0]
        else:
            return self.__animationStates[1] 

    #Animate the player based on state
    def __animate(self):
        animationState = self.__getAnimationState()

        if 'IDLE' in animationState:
            self.__texture = self.__idleTextures[self.__idleIndex//constants.PLAYER_ANIMATION_FRAME_REPEAT]
            self.__idleIndex = (self.__idleIndex + 1) % (len(self.__idleTextures) * constants.PLAYER_ANIMATION_FRAME_REPEAT) 
            self.__runningIndex = 0 

            #Flip texture to be equal to last state
            if 'bwd' in self.__lastState:
                return True
            else:
                return False

        elif 'WALKING' in animationState:
            self.__texture = self.__runTextures[self.__runningIndex//constants.PLAYER_ANIMATION_FRAME_REPEAT]
            self.__runningIndex = (self.__runningIndex + 1) % (len(self.__runTextures) * constants.PLAYER_ANIMATION_FRAME_REPEAT)
            self.__idleIndex = 0
            if self.movingBwd:
                self.__lastState = self.__states[0]
                return True
            else:
                self.__lastState = self.__states[1]
                return False

        elif 'SLIDING' in animationState:
            self.__texture = self.__slidingTex
            self.__runningIndex = 0
            self.__idleIndex = 0

            #Flip texture to be equal to last state
            if 'bwd' in self.__lastState:
                return True
            else:
                return False

        else:
            self.__texture = self.__jumpingTex
            self.__runningIndex = 0
            self.__idleIndex = 0

            #Flip texture to be equal to last state
            if 'bwd' in self.__lastState:
                return True
            else:
                return False

    #? The horizontal speed of the player now increases during the jump until it hits a max speed.
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

                #Set jumping speed, does not exceed max speed...
                self.playerSpeed += constants.PLAYER_JUMPING_HORIZONTAL_SPEED_INCREASE * timeElapsed
                if self.playerSpeed > constants.PLAYER_JUMPING_HORIZONTAL_SPEED_MAX_SPEED:
                    self.playerSpeed = constants.PLAYER_JUMPING_HORIZONTAL_SPEED_MAX_SPEED                

            #Else, done jumping, reset everything
            else:
                self.__jumpPower = constants.PLAYER_JUMP_VELOCITY
                self.__currentY = self.__originalY
                self.playerSpeed = constants.PLAYER_SPEED
                self.isJumping = False

    #? Player speed slowly decays while we are sliding...
    #? Not a big fan of this function... it works but its pretty ugly
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
        #Animate!
        flip = self.__animate()

        #Flip texture if moving bwd
        if flip:
            screen.blit(pygame.transform.flip(self.__texture, True, False), (self.__pos[0] - self.__texture.get_width(), self.__currentY))
        else:
            screen.blit(self.__texture, (self.__pos[0] - self.__texture.get_width(), self.__currentY))



        
        

    