import numpy as np
import pygame
import os
import constants

from PIL import Image 
from contextlib import redirect_stdout

#Tensorflow imports, set log level to only errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

# Folder path for model:
MODEL_FOLDER = './model/'

# Model name: Leave blank for .pb models with assets and variables folders, in model folder
MODEL_NAME = 'model.hdf5'


class aiPlayer:
    def __init__(self, stat):
        # If the ai is not playing, just return
        if not constants.AI_PLAYER:
            self.__modelLoaded = False
            return

        try:
            self.__model = tf.keras.models.load_model(MODEL_FOLDER + MODEL_NAME)
            self.__modelLoaded = True
            print(f'Successfully loaded model with Tensorflow {tf.__version__} and Keras {tf.keras.__version__}')
        except Exception as e:
            self.__modelLoaded = False
            print(f'Failed to load model:\n{e}')

        self.__savedResults = False
        self.__stat = stat

    def saveModelSummary(self):
        saveFile = open(f'{MODEL_FOLDER}modelResults.txt', 'w')

        if self.__stat.levelFinished:
            saveFile.write(f'Score: {self.__stat.FinalScore}\n')
        else:
            saveFile.write(f'Score: {self.__stat.getScore()}\n')

        saveFile.write(f'Coins Collected: {self.__stat.plyr.coinsCollected}\n')
        saveFile.write(f'Time Elapsed: {self.__stat.getTimeElapsed()}\n\n')
        saveFile.close()

        with open(f'{MODEL_FOLDER}modelResults.txt', 'a') as f:
            with redirect_stdout(f):
                self.__model.summary()

        f.close()

    def predictAction(self, screen):
        if self.__modelLoaded:
            # Get the current state of the screen
            frame = pygame.image.tostring(screen, 'RGB')
            frame = Image.frombytes('RGB', (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), frame)
            frame = frame.resize((224, 224))

            # Load into a numpy array and normalize
            frameArray = np.asarray(frame)
            frameArray = frameArray.astype('float32')
            frameArray /= 255
            frameArray = tf.expand_dims(frameArray, axis=0)

            # Predict the action, and return it
            if not self.__stat.levelFinished:
                pred = self.__model.predict(frameArray)
                return np.argmax(pred, axis=1)
            elif not self.__savedResults:
                self.saveModelSummary()
                self.__savedResults = True
            
            # If we are done predicting, just return 0 which is None action
            return 0
