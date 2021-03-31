import pygame
import constants

class objects:
    def __init__(self, ground):
        self.ground=ground;
        self.__test = pygame.image.load('./assets/test_object.png').convert()
        self.__testSize=self.__test.get_size()
        self.size=self.__test.get_size()
        self.__objectLocations=[('test', (100,0))]
    
    def draw(self, screen, screenLocation):
        playerLocation=screenLocation+constants.PLAYER_HORIZONTAL_POS

        for obj in self.__objectLocations: #loop through all objects
            if ((obj[1][0]<=screenLocation+constants.SCREEN_WIDTH) and (obj[1][0] >= screenLocation-30)): #if the object is on screen
                if(obj[0]=='test'):
                    screen.blit(self.__test, (obj[1][0]-screenLocation,self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__testSize[1]))
            elif(not obj[1][0]<=screenLocation+constants.SCREEN_WIDTH): #stop if the object if off the right side of the screen
                break

    def checkCollisions(self, player):
        playerLocation=player.distance+constants.PLAYER_HORIZONTAL_POS
        screenLocation=player.distance
        xPlayer=(constants.PLAYER_HORIZONTAL_POS-player.size[0], constants.PLAYER_HORIZONTAL_POS)
        yPlayer=(player.currentY+player.size[1], player.currentY)
        print("screen: ", screenLocation)
        for obj in self.__objectLocations: #loop through all objects
            if not ((obj[1][0]-screenLocation)>=xPlayer[1] or xPlayer[0]>=(obj[1][0]-screenLocation+self.__testSize[0])):
                if not (self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__testSize[1] >=yPlayer[0] or self.ground-obj[1][1]+constants.GRASS_OFFSET<=yPlayer[1]):
                   print('Collision') 