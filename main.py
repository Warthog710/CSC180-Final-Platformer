import pygame

from inputHandler import inputHandler
from gameWorld import gameWorld

#! Priority... Sliding, obstacles, collisions, scoring

#TODO: Add obstacles (ceiling obstacle, sawblade, stationary box, coin)
#TODO: Obstacles that are visible should be rendered on screen.
#TODO: Only check collisions for the closest obstacle
#TODO: Flip the player sprite when they walk back?
#TODO: Scoring... score is based on how far you go and how many coins you collect (add a weight, going further is worth more than collecting coins)
#TODO: Game will have a finite lenght... determine this length
#TODO: Player animations based on state [WALKING, IDLE, SLIDING, JUMPING]

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