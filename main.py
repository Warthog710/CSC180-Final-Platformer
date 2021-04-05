import pygame

from inputHandler import inputHandler
from gameWorld import gameWorld
from statistics import statistics

#TODO Record sources for textures in README.md

#TODO: Game will have a finite lenght... determine this length

def main():
    #Intilize pygame
    pygame.init()

    #Game clock
    gWorld = gameWorld()
    clock = pygame.time.Clock()
    iHandle = inputHandler(gWorld)
    stat = statistics(gWorld.getPlayer(), iHandle, gWorld)
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
        stat.drawHud()
        pygame.display.update()

    pygame.quit()

#Run the main function on program start
if __name__ == '__main__':
    main()