import pygame
import constants

from datetime import datetime


class statistics:
    def __init__(self, plyr, iHandle, gWorld):
        self.__plyr = plyr
        self.__iHandle = iHandle
        self.__gWorld = gWorld
        self.__gameStart = datetime.now()
        self.__lastDistance = self.__plyr.distance
        self.__lastMoveTime = datetime.now()
        self.__font = pygame.font.SysFont('./assets/FutilePro.ttf', constants.FONT_SIZE)
        self.levelFinished = False
        self.timeLevelFinished = None
        self.FinalScore = 0

    def getScore(self):
        #? For every 10 pixels travelled, get 1 point
        distScore = int(self.__plyr.distance / 10)
        
        #? Score the weighted average of distance travelled and coins collected
        score =  int((0.8 * distScore) + (0.2 * self.__plyr.coinsCollected))

        #It is possible to get a negative score if the player goes backwards... never report this
        if (score < 0):
            return 0
        else:
            return score

    #? Returns the time since the player last travelled some distance
    def getIdleTime(self):
        #If distance hasn't changed, tick idle time
        if (self.__lastDistance == self.__plyr.distance):
            return (datetime.now() - self.__lastMoveTime).total_seconds()
        else:
            self.__lastDistance = self.__plyr.distance
            self.__lastMoveTime = datetime.now()
            return 0.0

    #? Returns the time since the last action
    def getLastActionTime(self):
        return (datetime.now() - self.__iHandle.lastAction).total_seconds()

    def getTimeElapsed(self):
        if not self.levelFinished:
            return (datetime.now() - self.__gameStart).total_seconds()
        else:
            return (self.timeLevelFinished - self.__gameStart).total_seconds()

    def resetTimeElapsed(self):
        self.__gameStart = datetime.now()

    #? Resets the game, generally called when 'R' is pressed
    def resetGame(self):
        self.resetTimeElapsed()
        self.__plyr.reset()

    def drawHud(self):
        #Detect if the level is finished
        if self.__plyr.distance > (constants.LEVEL_LENGTH - self.__plyr.pos[0]):
            self.levelFinished = True
            
            #Record the time finished if we have not done so already
            if self.timeLevelFinished == None:
                self.timeLevelFinished = datetime.now()

            #Record the score if we have not done so already
            if self.FinalScore == 0:
                self.FinalScore = self.getScore()

                #Print out statistics
                print(f'Final Score: {self.FinalScore}')
                print(f'Coints Collected: {self.__plyr.coinsCollected}')
                print(f'Time Elapsed: {self.getTimeElapsed()}')

        if not self.levelFinished:
            hudStr1 = 'Score: ' + str(self.getScore())
            hudStr2 = 'Coins Collected: ' + str(self.__plyr.coinsCollected)
            hudStr3 = 'Idle Time: ' + str(round(self.getIdleTime(), 2))
            hudStr4 = 'Last Action Time: ' + str(round(self.getLastActionTime(), 2))
            hudStr5 = 'Time Elapsed: ' + str(round(self.getTimeElapsed(), 2))
            hud1 = self.__font.render(hudStr1, True, constants.COLOR_BLACK)
            hud2 = self.__font.render(hudStr2, True, constants.COLOR_BLACK)
            hud3 = self.__font.render(hudStr3, True, constants.COLOR_BLACK)
            hud4 = self.__font.render(hudStr4, True, constants.COLOR_BLACK)
            hud5 = self.__font.render(hudStr5, True, constants.COLOR_BLACK)
            self.__gWorld.getScreen().blit(hud1, (10, 10))
            self.__gWorld.getScreen().blit(hud2, (10, 10 + constants.FONT_SIZE))
            self.__gWorld.getScreen().blit(hud3, (10, 10 + constants.FONT_SIZE * 2))
            self.__gWorld.getScreen().blit(hud4, (10, 10 + constants.FONT_SIZE * 3))
            self.__gWorld.getScreen().blit(hud5, (10, 10 + constants.FONT_SIZE * 4))
        else:
            hudStr1 = 'LEVEL FINISHED, Final Score: ' + str(self.FinalScore)
            hudStr2 = 'Time Elapsed: ' + str(round(self.getTimeElapsed(), 2))
            hud1 = self.__font.render(hudStr1, True, constants.COLOR_BLACK)
            hud2 = self.__font.render(hudStr2, True, constants.COLOR_BLACK)
            self.__gWorld.getScreen().blit(hud1, (10, 10))
            self.__gWorld.getScreen().blit(hud2, (10, 10 + constants.FONT_SIZE))
