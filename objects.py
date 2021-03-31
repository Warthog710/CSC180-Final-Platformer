import pygame
import constants

class objects:
    def __init__(self, ground):
        self.ground=ground;
        self.__test = pygame.image.load('./assets/test_object.png').convert()
        self.__testSize=self.__test.get_size();
        self.__objectLocations=[('test', (100,10))]
    
    def draw(self, screen, screenLocation):
        playerLocation=screenLocation+constants.PLAYER_HORIZONTAL_POS

        for obj in self.__objectLocations: #loop through all objects
            if ((obj[1][0]<=screenLocation+constants.SCREEN_WIDTH) and (obj[1][0] >= screenLocation-30)): #if the object is on screen
                if(obj[0]=='test'):
                    screen.blit(self.__test, (obj[1][0]-screenLocation,self.ground-obj[1][1]-self.__testSize[1]/2))
            elif(not obj[1][0]<=screenLocation+constants.SCREEN_WIDTH): #stop if the object if off the right side of the screen
                break

    def checkCollisions(self, player):
        playerLocation=player.distance+constants.PLAYER_HORIZONTAL_POS
        screenLocation=player.distance
        xPlayer=(constants.PLAYER_HORIZONTAL_POS-player.size[0]/2, constants.PLAYER_HORIZONTAL_POS+player.size[0]/2)
        yPlayer=(player.currentY-player.size[1]/2, player.currentY+player.size[1]/2)
        """
        for obj in self.__objectLocations: #loop through all objects
            print((obj[1][0]-screenLocation-self.__testSize[1]/2)," : ",(obj[1][0]-screenLocation+self.__testSize[1]/2))
            print("Player: ", xPlayer,yPlayer)
            """