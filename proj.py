import pygame, os, sys
from pygame.locals import * 
from gamestates import statemanager

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('PROJETO')

FPSClock = pygame.time.Clock()
FPS = 30

dt = 0

game_engine = statemanager.StateManager()
pygame.mouse.set_visible(False)

while True:

    for e in pygame.event.get():       

        if e.type == KEYDOWN and e.key == K_ESCAPE or e.type == QUIT:
            pygame.quit()
            sys.exit()

        game_engine.handle_input(e)
            
    game_engine.update(dt)
    game_engine.draw(screen)

    pygame.display.update()
    dt = 1.0 / FPSClock.tick(FPS)
