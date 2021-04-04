import pygame
import constants

class obstacles:
    def __init__(self, plyr):
        #Textures
        self.__sawBladeTexture = pygame.image.load('./assets/obstacles/sawbladeScaled.png').convert()
        self.__vineTexture = pygame.image.load('./assets/obstacles/vine.png').convert()
        self.__boxTexture = pygame.image.load('./assets/obstacles/box.png').convert()
        self.__coinTexture = pygame.image.load('./assets/obstacles/coin.png').convert()
        self.__boxTexture.set_colorkey(constants.COLOR_WHITE)
        self.__coinTexture.set_colorkey(constants.COLOR_WHITE)
        self.__vineTexture.set_colorkey(constants.COLOR_BLACK)
        self.__sawBladeTexture.set_colorkey(constants.COLOR_WHITE)

        #Scale textures
        sawBladeSize = self.__sawBladeTexture.get_size()
        vineSize = self.__vineTexture.get_size()
        boxSize = self.__boxTexture.get_size()
        coinSize = self.__coinTexture.get_size()
        self.__sawBladeTexture = pygame.transform.scale(self.__sawBladeTexture, (int(sawBladeSize[0] * constants.OBSTACLES_SCALE), int(sawBladeSize[0] * constants.OBSTACLES_SCALE)))
        self.__vineTexture = pygame.transform.scale(self.__vineTexture, (int((vineSize[0] * constants.OBSTACLES_SCALE)/1.5), int(vineSize[0] * (constants.OBSTACLES_SCALE + 6.6))))
        self.__boxTexture = pygame.transform.scale(self.__boxTexture, (int(boxSize[0] * constants.OBSTACLES_SCALE), int(boxSize[0] * constants.OBSTACLES_SCALE)))
        self.__coinTexture = pygame.transform.scale(self.__coinTexture, (int(coinSize[0]), int(coinSize[0])))


        self.__obstaclesList = [('saw', (200, 0)), ('vine', (600, 0)), ('box', (800, 0)), ('coin', (1000, -10), True), ('coin', (1040, -50), True), ('coin', (1080, -90), True)]

        #Save player reference
        self.__plyr = plyr

    def detectCollision(self):

        for x in range(0, len(self.__obstaclesList)):
            if 'saw' in self.__obstaclesList[x][0]:
                obstacleRect = self.getSawBladeRect(self.__obstaclesList[x][1])
                
                if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                    return True
            
            elif 'vine' in self.__obstaclesList[x][0]:
                obstacleRect = self.getVineRect(self.__obstaclesList[x][1])
                
                if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                    return True

            elif 'box' in self.__obstaclesList[x][0]:
                obstacleRect = self.getBoxRect(self.__obstaclesList[x][1])

                if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                    return True 

            elif 'coin' in self.__obstaclesList[x][0] and self.__obstaclesList[x][2]:
                obstacleRect = self.getCoinRect(self.__obstaclesList[x][1])

                #If we collide, record it, add it to coins collected and remove it from the map
                if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                    self.__plyr.coinsCollected += 1
                    self.__obstaclesList[x] = (self.__obstaclesList[x][0], self.__obstaclesList[x][1], False)


        return False


    def getSawBladeRect(self, pos):
        return pygame.Rect((pos[0] - self.__plyr.distance) + (6 * constants.OBSTACLES_SCALE), (pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)) + (6 * constants.OBSTACLES_SCALE), self.__sawBladeTexture.get_width() - 2 * (6 * constants.OBSTACLES_SCALE), self.__sawBladeTexture.get_height() - 2 * (6 * constants.OBSTACLES_SCALE))

    def getVineRect(self, pos):
        return pygame.Rect(pos[0] - self.__plyr.distance + (12 * constants.OBSTACLES_SCALE), pos[1], self.__vineTexture.get_width() - (12 * constants.OBSTACLES_SCALE), self.__vineTexture.get_height() - (3 * constants.OBSTACLES_SCALE))

    def getBoxRect(self, pos):
        return pygame.Rect(pos[0] - self.__plyr.distance, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET), self.__boxTexture.get_width(), self.__boxTexture.get_height())

    def getCoinRect(self, pos):
        return pygame.Rect(pos[0] - self.__plyr.distance + 7, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET) + 7, self.__coinTexture.get_width() - 14, self.__coinTexture.get_height() - 14)



    def update(self):
        pass

    def draw(self, screen):
        for item in self.__obstaclesList:
            if 'saw' in item[0]: 
                pygame.draw.rect(screen, constants.COLOR_WHITE, self.getSawBladeRect(item[1]))               
                screen.blit(self.__sawBladeTexture, (item[1][0] - self.__plyr.distance, item[1][1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)))
            elif 'vine' in item[0]:
                pygame.draw.rect(screen, constants.COLOR_WHITE, self.getVineRect(item[1]))
                screen.blit(self.__vineTexture, (item[1][0] - self.__plyr.distance, item[1][1]))
            elif 'box' in item[0]:
                pygame.draw.rect(screen, constants.COLOR_WHITE, self.getBoxRect(item[1]))
                screen.blit(self.__boxTexture, (item[1][0] - self.__plyr.distance, item[1][1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)))
            elif 'coin' in item[0]:
                #Only draw if it has not been picked up yet
                if item[2]:
                    pygame.draw.rect(screen, constants.COLOR_WHITE, self.getCoinRect(item[1]))                    
                    screen.blit(self.__coinTexture, (item[1][0] - self.__plyr.distance, item[1][1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)))



