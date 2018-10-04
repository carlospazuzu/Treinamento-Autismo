import pygame   
from pygame.locals import *
import titlescreen
import game01
import game02
import game03

class StateManager:

    def __init__(self):
        self.states = []
        self.current_state = 0
        self.states.append(titlescreen.TitleScreen(self)) # 0 TITLE
        self.states.append(game01.Game01(self)) # 1 GAME 01
        self.states.append(game02.Game02(self)) # 2 GAME 02
        self.states.append(game03.Game03(self)) # 3 GAME 03

    def set_state(self, state):
        self.current_state = state

    def handle_input(self, event):
        if event.type == KEYUP and event.key == K_q:
            self.set_state(0) # return to title
        self.states[self.current_state].handle_input(event)

    def update(self, dt):
        self.states[self.current_state].update(dt)

    def draw(self, screen):
        self.states[self.current_state].draw(screen)