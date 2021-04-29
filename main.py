import pygame
import constants

from inputHandler import inputHandler
from dataRecorder import dataRecorder
from gameWorld import gameWorld
from statistics import statistics
from aiPlayer import aiPlayer

#TODO Record sources for textures in README.md

def main():
    #Intilize pygame
    pygame.init()
    pygame.display.set_caption('Panda Runner')

    #Game clock
    gWorld = gameWorld()
    clock = pygame.time.Clock()
    iHandle = inputHandler(gWorld)
    stat = statistics(gWorld.getPlayer(), iHandle, gWorld)
    running = True

    #Data collection
    dRecorder = dataRecorder(iHandle, stat, gWorld)

    #AI Player
    ai = aiPlayer(stat)

    while running:
        #Ensure game speed
        timeElapsed = clock.tick()

        #Reset key state
        keyState = None
        
        #? 1. Process user input (if human)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #If we get an escape key, kill the program
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    stat.resetGame()
                elif event.key == pygame.K_p and constants.AI_PLAYER:
                    ai.saveModelSummary()
                else:
                    iHandle.registerKeydown(event)
            elif event.type == pygame.KEYUP:
                iHandle.registerKeyup(event)   
            #If the X button on the window is pressed...
            elif event.type == pygame.QUIT:
                running = False

        #? 1.1 Process input for AI
        if constants.AI_PLAYER:
            pred = ai.predictAction(gWorld.getScreen())

            # Pretend that the game is running at 60fps
            timeElapsed = 16.66
            
            # Send the prediction to the input handler
            iHandle.registerPredictedMovement(pred)

        state = pygame.key.get_pressed()
        if state[pygame.K_w]:
            keyState = 'W'
        elif state[pygame.K_s]:
            keyState = 'S'

        #? 2. Update the state of all game objects
        #Update player
        iHandle.update(timeElapsed)
        gWorld.update(timeElapsed)

        #? Take a screenshot of the last frame
        dRecorder.takeScreenshot(keyState)

        #? 3. Update display
        gWorld.draw()
        stat.drawHud()
        pygame.display.update()

        #print(timeElapsed)


    pygame.quit()

#Run the main function on program start
if __name__ == '__main__':
    main()