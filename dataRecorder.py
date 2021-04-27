from gameWorld import gameWorld
import pygame
import constants
import shutil
import os

from datetime import date, datetime

class dataRecorder:
    def __init__(self, iHandle, stat, gWorld):
        self.__iHandle = iHandle
        self.__stat = stat
        self.__gWorld = gWorld

        #If we are not taking screenshots, don't go further
        if not constants.RECORD_SCREENSHOTS:
            return
            
        self.__lastScreenshot = datetime.now()
        self.__screenShotPath = f'./data/run_{str(self.__lastScreenshot.ctime()).replace(":", ".")}/'

        if not os.path.exists('./data'):
            os.mkdir('./data')

        if not os.path.exists(self.__screenShotPath):
            os.mkdir(self.__screenShotPath)

    def takeScreenshot(self, keyState):
        if not constants.RECORD_SCREENSHOTS:
            if self.__gWorld.getPlayer().gameReset:
                self.__stat.resetTimeElapsed()
                self.__gWorld.getPlayer().gameReset = False
            return

        if (datetime.now() - self.__lastScreenshot).total_seconds() > constants.SCREENSHOT_FREQUENCY and not self.__stat.levelFinished:
            self.__lastScreenshot = datetime.now()
            screenName = str(self.__lastScreenshot).split(' ')[1].replace(":", ".") + '_' + str(keyState) + '.jpeg'
            pygame.image.save(self.__gWorld.getScreen(), self.__screenShotPath + screenName)

        if self.__iHandle.forcedScreenshot and not self.__stat.levelFinished:
            self.__iHandle.forcedScreenshot = False
            screenName = str(self.__lastScreenshot).split(' ')[1].replace(":", ".") + '_' + str(keyState) + '.jpeg'
            pygame.image.save(self.__gWorld.getScreen(), self.__screenShotPath + screenName)

        #If the game was reset, remove the current folder and all images and create a new one
        if self.__gWorld.getPlayer().gameReset:
            try:
                self.__gWorld.getPlayer().gameReset = False
                shutil.rmtree(self.__screenShotPath)
                self.__lastScreenshot = datetime.now()
                self.__stat.resetTimeElapsed()
                self.__screenShotPath = f'./data/run_{str(self.__lastScreenshot.ctime()).replace(":", ".")}/'

                if not os.path.exists(self.__screenShotPath):
                    os.mkdir(self.__screenShotPath)

            except OSError:
                print('Unable to remove files after reset')


