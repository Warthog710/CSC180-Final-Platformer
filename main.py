import pygame

from inputHandler import inputHandler
from gameWorld import gameWorld

#TODO: Add obstacles (ceiling obstacle, sawblade, )
#TODO: Obstacles that are visble should be rendered and checked against. 

def main():
    #Intilize pygame
    pygame.init()

    #Game clock, set to 60fps
    gWorld = gameWorld()
    clock = pygame.time.Clock()
    iHandle = inputHandler(gWorld)
    running = True

    while running:
        #Ensure game speed
        timeElapsed = clock.tick()
        
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
        iHandle.update(timeElapsed)
        gWorld.update(timeElapsed)

        #? 3. Update display
        gWorld.draw()

    pygame.quit()

#Run the main function on program start
if __name__ == '__main__':
    main()