import pygame
import constants
class player:
    def __init__(self, pos, gWorld):
        #Textures
        self.__idleTextures = [pygame.image.load('./assets/idle0.png').convert(), pygame.image.load('./assets/idle1.png').convert(), 
                                pygame.image.load('./assets/idle2.png').convert(), pygame.image.load('./assets/idle3.png').convert()]

        self.__runTextures = [pygame.image.load('./assets/run0.png').convert(), pygame.image.load('./assets/run1.png').convert(), 
                                pygame.image.load('./assets/run2.png').convert(), pygame.image.load('./assets/run3.png').convert(), 
                                pygame.image.load('./assets/run4.png').convert(), pygame.image.load('./assets/run5.png').convert()]

        self.__slidingTex = pygame.image.load('./assets/sliding.png').convert()
        self.__jumpingTex = pygame.image.load('./assets/jump.png').convert()
        self.texture = self.__idleTextures[0]

        #Gameworld reference
        self.__gWorld = gWorld

        #Player information
        self.distance = 0
        self.coinsCollected = 0

        #Animation indexes
        self.__idleIndex = 0
        self.__runningIndex = 0

        #Position. CurrentY holds the y cord the texture will be drawn at. OriginalY holds the original value so we can reset it later
        self.pos = pos
        self.originalY = self.pos[1] - (self.texture.get_height() + constants.PLAYER_HEIGHT_ADJUST)
        self.currentY = self.originalY

        #Player speed and jump velocity (power)
        self.__jumpPower = -constants.PLAYER_JUMP_VELOCITY
        self.playerSpeed = constants.PLAYER_SPEED

        #Boolean flags
        self.isJumping = False
        self.isSliding = False
        self.movingFwd = False
        self.movingBwd = False
        self.__slidingTextureInUse = False
        self.forcedSlide = False
        self.onObject = False
        self.gameReset = False

        #States to maintain the last facing position. This prevent us from restoring the default position if nothing is being pressed
        self.__animationStates = ['WALKING', 'IDLE', 'SLIDING', 'JUMPING']
        self.__states = ['bwd', 'fwd']
        self.__lastState = self.__states[1]

        #Scale player textures
        imgSize = self.texture.get_size()
        slidingSize = self.__slidingTex.get_size()
        jmpSize = self.__jumpingTex.get_size()
        self.texture = pygame.transform.scale(self.texture, (int(imgSize[0] * constants.PLAYER_SCALE), int(imgSize[0] * constants.PLAYER_SCALE)))
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
            self.texture = self.__idleTextures[self.__idleIndex//constants.PLAYER_ANIMATION_FRAME_REPEAT]
            self.__idleIndex = (self.__idleIndex + 1) % (len(self.__idleTextures) * constants.PLAYER_ANIMATION_FRAME_REPEAT) 
            self.__runningIndex = 0 

            #Flip texture to be equal to last state
            if 'bwd' in self.__lastState:
                return True
            else:
                return False

        elif 'WALKING' in animationState:
            self.texture = self.__runTextures[self.__runningIndex//constants.PLAYER_ANIMATION_FRAME_REPEAT]
            self.__runningIndex = (self.__runningIndex + 1) % (len(self.__runTextures) * constants.PLAYER_ANIMATION_FRAME_REPEAT)
            self.__idleIndex = 0
            if self.movingBwd:
                self.__lastState = self.__states[0]
                return True
            else:
                self.__lastState = self.__states[1]
                return False

        elif 'SLIDING' in animationState:
            self.texture = self.__slidingTex
            self.__runningIndex = 0
            self.__idleIndex = 0

            #Flip texture to be equal to last state
            if 'bwd' in self.__lastState:
                return True
            else:
                return False

        else:
            self.texture = self.__jumpingTex
            self.__runningIndex = 0
            self.__idleIndex = 0

            #Flip texture to be equal to last state
            if 'bwd' in self.__lastState:
                return True
            else:
                return False

    #? The horizontal speed of the player now increases during the jump until it hits a max speed.
    def updateJump(self, timeElapsed):
        #If jumping
        if self.isJumping:
            self.currentY += self.__jumpPower * timeElapsed
            self.__jumpPower += constants.GRAVITY * timeElapsed

            #Increase player horinzontal speed while jumping
            self.playerSpeed += constants.PLAYER_JUMPING_HORIZONTAL_SPEED_INCREASE
            if self.playerSpeed > constants.PLAYER_JUMPING_HORIZONTAL_SPEED_MAX_SPEED:
                self.playerSpeed = constants.PLAYER_JUMPING_HORIZONTAL_SPEED_MAX_SPEED

            #If I collide with an object
            if self.__gWorld.getObstacles().detectCollision():
                #If I am going down
                if self.__jumpPower > 0:
                    #I must be on an object... stop the jump, reset to previous y
                    self.currentY -= self.__jumpPower * timeElapsed
                    self.isJumping = False
                    self.__jumpPower = -constants.PLAYER_JUMP_VELOCITY
                    self.playerSpeed = constants.PLAYER_SPEED
                    self.onObject = True

                #Else, I must be going up, set jump velocity to 0 and restore to previous position
                else:
                    self.currentY -= self.__jumpPower * timeElapsed
                    self.__jumpPower = 0


            if self.currentY > self.originalY:
                self.isJumping = False
                self.__jumpPower = -constants.PLAYER_JUMP_VELOCITY
                self.playerSpeed = constants.PLAYER_SPEED
                self.currentY = self.originalY

    def reset(self):
        self.distance = 0
        self.coinsCollected = 0
        self.__lastState = 'fwd'
        self.gameReset = True

    def getBoundingBox(self):
        if not self.isSliding:
            return pygame.Rect((self.pos[0] - self.texture.get_width()) + (7 * constants.PLAYER_SCALE), self.currentY + 
                    (4 * constants.PLAYER_SCALE), self.texture.get_width() - 2 *(7 * constants.PLAYER_SCALE), 
                    self.texture.get_height() - (4 * constants.PLAYER_SCALE))
        else:
            if 'bwd' in self.__lastState:
                return pygame.Rect((self.pos[0] - self.texture.get_width()) + (9 * constants.PLAYER_SCALE), self.currentY + 
                        (9 * constants.PLAYER_SCALE), self.texture.get_width() - 2 *(7 * constants.PLAYER_SCALE), 
                        self.texture.get_height() - 2 * (8 * constants.PLAYER_SCALE))     
            else:
                return pygame.Rect((self.pos[0] - self.texture.get_width()) + (5 * constants.PLAYER_SCALE), self.currentY + 
                        (9 * constants.PLAYER_SCALE), self.texture.get_width() - 2 *(7 * constants.PLAYER_SCALE), 
                        self.texture.get_height() - 2 * (8 * constants.PLAYER_SCALE))               
        
    #? Player speed slowly decays while we are sliding...
    #? Not a big fan of this function... it works but its pretty ugly
    def updateSlide(self):       
        #If not jumping, and sliding is true, and I am not rotated...
        if self.isSliding and not self.__slidingTextureInUse:
            #Modifiy player height
            self.currentY += constants.PLAYER_SLIDING_OFFSET

            #Set sliding texture to true
            self.__slidingTextureInUse = True

        #If I am currently sliding slowly decay the player speed
        elif self.isSliding and self.__slidingTextureInUse:
            self.playerSpeed -= constants.PLAYER_SLIDING_DECAY

            #Speed cannot fall below min sleed spped
            if self.playerSpeed < constants.PLAYER_MIN_SLIDING_SPEED:
                self.playerSpeed = constants.PLAYER_MIN_SLIDING_SPEED

        #If I am no longer sliding but still have the sliding texture, reset it
        elif not self.isSliding and self.__slidingTextureInUse:

            #If by getting up I collide with an object... don't stop sliding
            if self.__gWorld.getObstacles().detectCollision():
                self.isSliding = True
                self.forcedSlide = True

                if self.forcedSlide:
                    self.playerSpeed -= constants.PLAYER_SLIDING_DECAY

                    #Speed cannot fall below min sleed spped
                    if self.playerSpeed < constants.PLAYER_MIN_SLIDING_SPEED:
                        self.playerSpeed = constants.PLAYER_MIN_SLIDING_SPEED
                return

            self.__slidingTextureInUse = False
            self.forcedSlide = False

            #Reset height
            self.currentY = self.originalY

            #Restore player speed
            self.playerSpeed = constants.PLAYER_SPEED


    def draw(self, screen):
        #Animate!
        flip = self.__animate()
        
        #Flip texture if moving bwd
        if flip:
            screen.blit(pygame.transform.flip(self.texture, True, False), (self.pos[0] - self.texture.get_width(), self.currentY))
        else:
            screen.blit(self.texture, (self.pos[0] - self.texture.get_width(), self.currentY))



        
        

    