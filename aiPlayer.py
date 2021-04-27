import numpy as np
import pygame
import os
import constants

from PIL import Image 

#Tensorflow imports, set log level to only errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf


class aiPlayer:
    def __init__(self):
        # If the ai is not playing, just return
        if not constants.AI_PLAYER:
            self.__modelLoaded = False
            return

        try:
            self.__model = tf.keras.models.load_model('./model/model.hdf5')
            self.__modelLoaded = True
            print(f'Successfully loaded model with Tensorflow {tf.__version__} and Keras {tf.keras.__version__}')
        except Exception as e:
            self.__modelLoaded = False
            print(f'Failed to load model:\n{e}')

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
            pred = self.__model.predict(frameArray)
            return np.argmax(pred, axis=1)
            