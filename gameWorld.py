import pygame
import constants

from ground import ground

class gameWorld:
    def __init__(self):
        self.__screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
        self.__gameClouds1 = pygame.image.load('./assets/clouds.png').convert()
        self.__gameClouds1.set_colorkey(constants.COLOR_WHITE)
        self.__gameClouds2 = pygame.image.load('./assets/clouds.png').convert()
        self.__gameClouds2.set_colorkey(constants.COLOR_WHITE)
        self.__gameMountains = pygame.image.load('./assets/mountains.png').convert()
        self.__gameMountains.set_colorkey(constants.COLOR_BLACK)
        self.__gameSky = pygame.image.load('./assets/sky.png').convert()
        self.__backGroundPos1 = (0, 0)
        self.__backGroundPos2 = (constants.SCREEN_WIDTH, 0)

        #Ground class
        self.__grnd1 = ground((0, constants.SCREEN_HEIGHT))
        self.__grnd2 = ground((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    def __drawBackground(self):
        self.__screen.blit(self.__gameSky, (0, 0))
        self.__screen.blit(self.__gameClouds1, self.__backGroundPos1)
        self.__screen.blit(self.__gameClouds2, self.__backGroundPos2)
        self.__screen.blit(self.__gameMountains, (0, 0))

    #Magic stuff happens here
    def updateBackground(self, pos):
        self.__backGroundPos1 = tuple(map(lambda i, j: i - j, self.__backGroundPos1, pos))
        self.__grnd1.setPos(tuple(map(lambda i, j: i - j, self.__grnd1.getPos(), pos)))

        #Determine if the background has room on right
        if (self.__backGroundPos1[0] < 0):
            self.__backGroundPos2 = (constants.SCREEN_WIDTH + self.__backGroundPos1[0], 0)
            self.__grnd2.setPos((constants.SCREEN_WIDTH + self.__grnd1.getPos()[0], constants.SCREEN_HEIGHT))

        #If not, determine if the background has room on the left
        elif (self.__backGroundPos1[0] > 0):
            self.__backGroundPos2 = (-constants.SCREEN_WIDTH + self.__backGroundPos1[0], 0)
            self.__grnd2.setPos((-constants.SCREEN_WIDTH + self.__grnd1.getPos()[0], constants.SCREEN_HEIGHT))

        #Else, place the second image somewhere
        else:
            self.__backGroundPos2 = (constants.SCREEN_WIDTH, 0)
            self.__grnd2.setPos((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

        #If image 1 is off screen swap the images positions
        if (abs(self.__backGroundPos1[0]) > constants.SCREEN_WIDTH):
            temp = self.__backGroundPos1
            self.__backGroundPos1 = self.__backGroundPos2
            self.__backGroundPos2 = temp

            temp = self.__grnd1.getPos()
            self.__grnd1.setPos(self.__grnd2.getPos())
            self.__grnd2.setPos(temp)
        

    def update(self):
        self.__drawBackground()
        self.__grnd1.draw(self.__screen)
        self.__grnd2.draw(self.__screen)
        pygame.display.flip()