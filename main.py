import pygame
import constants

from inputHandler import inputHandler
from gameWorld import gameWorld

def main():
    #Intilize pygame
    pygame.init()

    #Game clock, set to 60fps
    gWorld = gameWorld()
    clock = pygame.time.Clock()
    iHandle = inputHandler(gWorld)
    running = True

    #Images

    while running:
        #Ensure game speed
        clock.tick(constants.GAME_SPEED)
        
        #? 1. Process user input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #If we get an escape key, kill the program
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    iHandle.registerKeydown(event)
            elif event.type == pygame.KEYUP:
                iHandle.registerKeyup(event)   
            #If the X button on the window is pressed...
            elif event.type == pygame.QUIT:
                running = False

        #? 2. Update the state of all game objects
        #Update player
        iHandle.update()

        #? 3. Update display
        gWorld.update()

    pygame.quit()

#Run the main function on program start
if __name__ == '__main__':
    main()