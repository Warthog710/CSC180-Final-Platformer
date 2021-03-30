import pygame
import constants

class ground:
    def __init__(self, startingPos):
        self.__pos = startingPos
        self.__texture = pygame.image.load('./assets/ground.png').convert()
        self.__texture.set_colorkey(constants.COLOR_BLACK)

        #If the texture is not divisible by screen width, weird things will happen
        if (constants.SCREEN_WIDTH % self.__texture.get_width() != 0):
            print('WARNING: Ground texture should be evenly divisible by screen width...')

        #Tile the textures
        self.__groundTextures = []
        for x in range(0, int(constants.SCREEN_WIDTH / self.__texture.get_width())):
            self.__groundTextures.append((self.__pos[0] + (x * self.__texture.get_width()), self.__pos[1] - self.__texture.get_height()))

    def getPos(self):
        return self.__pos

    def setPos(self, pos):
        #Set the new pos
        self.__pos = pos

        #Update all tiles
        for x in range(0, int(constants.SCREEN_WIDTH / self.__texture.get_width())):
            self.__groundTextures[x] = (self.__pos[0] + (x * self.__texture.get_width()), self.__pos[1] - self.__texture.get_height())
            
    def draw(self, screen):
        for ground in self.__groundTextures:
            screen.blit(self.__texture, ground)
    
    def getHeight(self):
        return self.__texture.get_height()
