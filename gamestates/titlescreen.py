import pygame
from pygame.locals import *
from gameobjects.titlebutton import TitleButton
from gameobjects.playermouse import PlayerMouse

class TitleScreen:

    def __init__(self, statemanager):
        self.sm = statemanager       
        #self.change_state_on_release = (False, None)
        self.mouse = PlayerMouse()
        self.buttons = pygame.sprite.Group()        
        self.buttons.add(TitleButton(50, 200, 'GAME 01'))
        self.buttons.add(TitleButton(300, 200, 'GAME 02'))
        self.buttons.add(TitleButton(550, 200, 'GAME 03'))

    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:            
            for collided in pygame.sprite.spritecollide(self.mouse, self.buttons, False):
                collided.change_image_to('PRESSED')
                
        elif event.type == MOUSEBUTTONUP:            
            for b in self.buttons.sprites():
                b.change_image_to('NORMAL')            
            for collided in pygame.sprite.spritecollide(self.mouse, self.buttons, False):                
                if collided.get_purpose() == 'GAME 01':
                    self.sm.set_state(1) # change state to GAME 01
                if collided.get_purpose() == 'GAME 02':
                    self.sm.set_state(2) # change state to GAME 02
                if collided.get_purpose() == 'GAME 03':
                    self.sm.set_state(3) # change state to GAME 03

    def update(self, dt):
        self.mouse.update(dt)

    def draw(self, screen):
        screen.fill((189, 188, 179))
        self.buttons.draw(screen)
        self.mouse.draw(screen)