import pygame
import math
import constants
import random

class obstacles:
    def __init__(self, plyr):
        #Textures
        self.__sawBladeTexture = pygame.image.load('./assets/obstacles/saw.png').convert()
        self.__vineTexture = pygame.image.load('./assets/obstacles/vine.png').convert()
        self.__boxTexture = pygame.image.load('./assets/obstacles/box.png').convert()
        self.__coinTexture = pygame.image.load('./assets/obstacles/coin.png').convert()
        self.__boxTexture.set_colorkey(constants.COLOR_WHITE)
        self.__coinTexture.set_colorkey(constants.COLOR_WHITE)
        self.__vineTexture.set_colorkey(constants.COLOR_WHITE)
        self.__sawBladeTexture.set_colorkey(constants.COLOR_BLACK)

        #Scale textures
        sawBladeSize = self.__sawBladeTexture.get_size()
        vineSize = self.__vineTexture.get_size()
        boxSize = self.__boxTexture.get_size()
        coinSize = self.__coinTexture.get_size()
        self.__sawBladeTexture = pygame.transform.scale(self.__sawBladeTexture, (int(sawBladeSize[0] * constants.OBSTACLES_SCALE), int(sawBladeSize[0] * constants.OBSTACLES_SCALE)))
        self.__vineTexture = pygame.transform.scale(self.__vineTexture, (int((vineSize[0] * constants.OBSTACLES_SCALE)/1.5), int(vineSize[0] * (constants.OBSTACLES_SCALE + 6.6))))
        self.__boxTexture = pygame.transform.scale(self.__boxTexture, (int(boxSize[0] * constants.OBSTACLES_SCALE), int(boxSize[0] * constants.OBSTACLES_SCALE)))
        self.__coinTexture = pygame.transform.scale(self.__coinTexture, (int(coinSize[0]), int(coinSize[0])))

        #? Idea: the screen is 1280px wide. Lets split the screen into 16chunks of 80 pixels. We will then place 1 or none obstacles in these chunks.
        #? During collision detection, just detect collisions in the chunks behind or in front
        #? For drawing, only draw the visible chunks
        #? Note: Current chunk = self.__startingPlayerChunk + math.floor(self.__plyr.distance / self.__chunkWidth)

        #Save player reference
        self.__plyr = plyr

        #Chunk info
        self.__chunkWidth = constants.SCREEN_WIDTH / constants.NUM_CHUNKS
        self.__startingPlayerChunk = math.floor(self.__plyr.pos[0] / self.__chunkWidth)

        self.__obstacleDict = self.__loadMap()
        

    #Takes a map object, and loads the map
    def __loadMap(self):
        mapFile = open(constants.GAME_MAP_PATH, 'r')
        obst = {}

        for line in mapFile:
            temp = line.strip('\n').split(',')

            #If its a coin we add a boolean to the tuple
            if 'coin' in temp[1]:
                obst[int(temp[0])] = (temp[1], (int(temp[2]), int(temp[3])), True)
            else:
                obst[int(temp[0])] = (temp[1], (int(temp[2]), int(temp[3])))
        
        mapFile.close()
        return obst          

    #? For collisions, we will look at the the players chunk and before and ahead of it 2 chunks
    def detectCollision(self):
        currentChunk = self.__startingPlayerChunk + math.floor(self.__plyr.distance / self.__chunkWidth)
        startingChunk = currentChunk - 2

        for startingChunk in range(startingChunk, currentChunk + 2):
            #If an object exists in that chunk, perform collision detection
            if startingChunk in self.__obstacleDict:
                #Check object type
                if 'saw' in self.__obstacleDict[startingChunk][0]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    obstacleRect = self.getSawBladeRect(pos)

                    #Check if the player collides
                    if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                        #? Since we hit a saw, we will reset the game
                        self.__plyr.reset()
                        self.__obstacleDict = self.__loadMap()
                        return True
                elif 'box' in self.__obstacleDict[startingChunk][0]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    obstacleRect = self.getBoxRect(pos)

                    #Check if the player collides
                    if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                        return True
                elif 'vine' in self.__obstacleDict[startingChunk][0]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    obstacleRect = self.getVineRect(pos)

                    #Check if the player collides
                    if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                        return True
                elif 'coin' in self.__obstacleDict[startingChunk][0] and self.__obstacleDict[startingChunk][2]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    obstacleRect = self.getVineRect(pos)

                    #Check if the player collides
                    if obstacleRect.colliderect(self.__plyr.getBoundingBox()):
                        #Since this is a coin, collision is handled internally, increment coins collected...
                        self.__plyr.coinsCollected += 1
                        self.__obstacleDict[startingChunk] = (self.__obstacleDict[startingChunk][0], self.__obstacleDict[startingChunk][1], False)
        
        #Return false if no collisions were found
        return False

    def getSawBladeRect(self, pos):
        return pygame.Rect((pos[0] - self.__plyr.distance) + (6 * constants.OBSTACLES_SCALE), (pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)) + (6 * constants.OBSTACLES_SCALE) + 5, self.__sawBladeTexture.get_width() - 2 * (6 * constants.OBSTACLES_SCALE), self.__sawBladeTexture.get_height() - 2 * (6 * constants.OBSTACLES_SCALE) - 5)

    def getVineRect(self, pos):
        return pygame.Rect(pos[0] - self.__plyr.distance + (12 * constants.OBSTACLES_SCALE), pos[1], self.__vineTexture.get_width() - (12 * constants.OBSTACLES_SCALE), self.__vineTexture.get_height() - (3 * constants.OBSTACLES_SCALE))

    def getBoxRect(self, pos):
        return pygame.Rect(pos[0] - self.__plyr.distance, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET), self.__boxTexture.get_width(), self.__boxTexture.get_height())

    def getCoinRect(self, pos):
        return pygame.Rect(pos[0] - self.__plyr.distance + 7, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET) + 7, self.__coinTexture.get_width() - 14, self.__coinTexture.get_height() - 14)

    #Takes a chunk, and returns its starting pixel (x)
    def __transChunkToPxl(self, chunk):
        return chunk * self.__chunkWidth


    def draw(self, screen):
        currentChunk = self.__startingPlayerChunk + math.floor(self.__plyr.distance / self.__chunkWidth)

        #Draw the obstacles starting from the first visible chunk
        startingChunk = currentChunk - self.__startingPlayerChunk

        #Drawing one extra chunk on the end eliminates pop in
        for startingChunk in range(startingChunk, startingChunk + constants.NUM_CHUNKS + 1):
            if startingChunk in self.__obstacleDict:
                if 'box' in self.__obstacleDict[startingChunk][0]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    #pygame.draw.rect(screen, constants.COLOR_WHITE, self.getBoxRect(pos))
                    screen.blit(self.__boxTexture, (pos[0] - self.__plyr.distance, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)))
                elif 'vine' in self.__obstacleDict[startingChunk][0]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    #pygame.draw.rect(screen, constants.COLOR_WHITE, self.getVineRect(pos))
                    screen.blit(self.__vineTexture, (pos[0] - self.__plyr.distance, pos[1]))
                elif 'saw' in self.__obstacleDict[startingChunk][0]:
                    pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                    #pygame.draw.rect(screen, constants.COLOR_WHITE, self.getSawBladeRect(pos))
                    screen.blit(self.__sawBladeTexture, (pos[0] - self.__plyr.distance, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)))
                else:
                    if self.__obstacleDict[startingChunk][2]:
                        pos = (self.__transChunkToPxl(startingChunk) + self.__obstacleDict[startingChunk][1][0], self.__obstacleDict[startingChunk][1][1])
                        #pygame.draw.rect(screen, constants.COLOR_WHITE, self.getCoinRect(pos))
                        screen.blit(self.__coinTexture, (pos[0] - self.__plyr.distance, pos[1] + (constants.SCREEN_HEIGHT - constants.GRASS_OFFSET)))
