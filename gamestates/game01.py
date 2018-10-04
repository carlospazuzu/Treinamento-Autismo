import pygame
from pygame.locals import *
from random import randint
from gameobjects import squareblock
from gameobjects import playermouse
from gameobjects import cheeringboy

class Game01:

    def __init__(self, statemanager):
        self.sm = statemanager        
        self.mouse = playermouse.PlayerMouse()
        self.cheeringboys = []
        self.possible_positions = [(20, 20), (320, 20), (600, 20), 
                                   (20, 220), (600, 220),
                                   (20, 400), (320, 400), (600, 400)
                                   ]
        self.squares = pygame.sprite.Group()   
        self.squares.add(squareblock.SquareBlock(self.possible_positions[randint(0, 7)]))             

    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if pygame.sprite.spritecollide(self.mouse, self.squares, True):
                self.cheeringboys.append(cheeringboy.CheeringBoy())

    def update(self, dt):        
        self.squares.update(dt)
        for c in self.cheeringboys:
            c.update(dt)    
            if c.is_finished():
                self.cheeringboys.pop()
                self.squares.add(squareblock.SquareBlock(self.possible_positions[randint(0, 7)]))        
        self.mouse.update(dt)

    def draw(self, screen):
        screen.fill((118, 173, 210))
        self.squares.draw(screen)
        for c in self.cheeringboys:
            c.draw(screen)    
        self.mouse.draw(screen)