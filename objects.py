import pygame
import constants

class objects:
    def __init__(self, ground):
        self.ground=ground;
        self.__test = pygame.image.load('./assets/test_object.png').convert()
        self.__testSize=self.__test.get_size()
        self.__coin = pygame.image.load('./assets/coin.png').convert()
        self.__coin.set_colorkey(constants.COLOR_WHITE)
        self.__coinSize=self.__coin.get_size()
        self.__box = pygame.image.load('./assets/box.png').convert()
        self.__boxSize=self.__box.get_size()
        self.__saw = pygame.image.load('./assets/saw.png').convert()
        self.__saw.set_colorkey(constants.COLOR_WHITE)
        self.__sawSize=self.__saw.get_size()
        self.__ceiling = pygame.image.load('./assets/ceiling.png').convert()
        self.__ceilingSize=self.__ceiling.get_size()
        self.__objectLocations=[('test', (100,0)),('box', (150,0)),('coin', (200,0), True), ('coin', (700,50), True), ('coin', (750,100), True),('coin', (800,50), True), ('saw', (1000,0))]
    
    def draw(self, screen, screenLocation):
        playerLocation=screenLocation+constants.PLAYER_HORIZONTAL_POS

        for obj in self.__objectLocations: #loop through all objects
            if ((obj[1][0]<=screenLocation+constants.SCREEN_WIDTH) and (obj[1][0] >= screenLocation-30)): #if the object is on screen
                if(obj[0]=='test'):
                    screen.blit(self.__test, (obj[1][0]-screenLocation,self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__testSize[1]))
                elif(obj[0]=='saw'):
                    screen.blit(self.__saw, (obj[1][0]-screenLocation,self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__sawSize[1]))
                elif(obj[0]=='box'):
                    screen.blit(self.__box, (obj[1][0]-screenLocation,self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__boxSize[1]))
                elif(obj[0]=='ceiling'):
                    screen.blit(self.__ceiling, (obj[1][0]-screenLocation,self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__ceilingSize[1]))
                elif(obj[0]=='coin'):
                    if obj[2]:
                        screen.blit(self.__coin, (obj[1][0]-screenLocation,self.ground-obj[1][1]+constants.GRASS_OFFSET-self.__coinSize[1]))
            elif(not obj[1][0]<=screenLocation+constants.SCREEN_WIDTH): #stop if the object if off the right side of the screen
                break

    def checkCollisions(self, player):
        playerLocation=player.distance+constants.PLAYER_HORIZONTAL_POS
        screenLocation=player.distance
        xPlayer=(constants.PLAYER_HORIZONTAL_POS-player.size[0]+7, constants.PLAYER_HORIZONTAL_POS-8)
        print((constants.PLAYER_HORIZONTAL_POS-player.size[0], constants.PLAYER_HORIZONTAL_POS))
        print(xPlayer)
        yPlayer=(player.currentY+player.size[1], player.currentY)
        print("screen: ", screenLocation)
        i=0
        for obj in self.__objectLocations: #loop through all objects
            size=(0,0)
            if(obj[0]=='test'):
                size=self.__testSize
            elif(obj[0]=='saw'):
                size=self.__sawSize
            elif(obj[0]=='box'):
                size=self.__boxSize
            elif(obj[0]=='ceiling'):
                size=self.__ceilingSize
            elif(obj[0]=='coin'):
                size=self.__coinSize
            if not ((obj[1][0]-screenLocation)>=xPlayer[1] or xPlayer[0]>=(obj[1][0]-screenLocation+size[0])):
                if not (self.ground-obj[1][1]+constants.GRASS_OFFSET-size[1] >=yPlayer[0] or self.ground-obj[1][1]+constants.GRASS_OFFSET<=yPlayer[1]):
                    print('Collision')
                    if(obj[0]=='test'):
                        size=self.__testSize
                    elif(obj[0]=='saw'):
                        player.died()
                        print("You Died")
                        k=0
                        for item in self.__objectLocations:
                            if(item[0]=='coin'):
                                self.__objectLocations[k]=('coin', item[1], True)
                            k+=1
                    elif(obj[0]=='box'):
                        size=self.__boxSize
                    elif(obj[0]=='ceiling'):
                        size=self.__ceilingSize
                    elif(obj[0]=='coin'):
                        if obj[2]:
                            player.points+=1
                            self.__objectLocations[i]=('coin', obj[1], False)
            i+=1