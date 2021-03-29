import pygame
import constants

class inputHandler:
    def __init__(self, gWorld):     
        #Private internal variables
        self.__wPressed = False
        self.__sPressed = False
        self.__dPressed = False
        self.__aPressed = False

        #Gameworld reference
        self.__gWorld = gWorld


    #Register a keydown event on WASD
    def registerKeydown(self, event):
        if event.key == pygame.K_w:
            self.__wPressed = True
        elif event.key == pygame.K_s:
            self.__sPressed = True
        elif event.key == pygame.K_d:
            self.__dPressed = True
        elif event.key == pygame.K_a:
            self.__aPressed = True

    #Register a keyup event on WASD
    def registerKeyup(self, event):
        if event.key == pygame.K_w:
            self.__wPressed = False
        elif event.key == pygame.K_s:
            self.__sPressed = False
        elif event.key == pygame.K_d:
            self.__dPressed = False
        elif event.key == pygame.K_a:
            self.__aPressed = False

    #Update
    def update(self):
        if self.__wPressed:
            print('w pressed...')
        if self.__sPressed:
            print('s pressed...')
        if self.__dPressed:
            self.__gWorld.updateBackground((constants.PLAYER_SPEED, 0))
        if self.__aPressed:
             self.__gWorld.updateBackground((-constants.PLAYER_SPEED, 0))


