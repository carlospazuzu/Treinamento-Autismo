import pygame, os
from pygame.locals import *
from random import choice
from gameobjects import playermouse
from gameobjects.stimulisprite import StimuliSprite

class Game03:

    def __init__(self, statemanager):
        self.sm = statemanager
        # the mouse
        self.mouse = playermouse.PlayerMouse()
        # groups
        self.pivot_list = pygame.sprite.Group()
        self.target_list = pygame.sprite.Group()
        # booleans
        self.current_pivot_being_dragged = None
        self.is_some_pivot_being_dragged = False
        self.hide_unselected_pivots = False
        # generate first pivots and targets for the current simulation
        self.generate_pivots_and_targets()

        self.colors = {
            'DEFAULT': (118, 173, 210),
            'RIGHT': (119, 209, 128),
            'WRONG': (230, 53, 50)
        }
        self.current_color = 'DEFAULT'

    def generate_pivots_and_targets(self):
        self.pivot_list.empty()
        self.target_list.empty()

        char_list = []
        y_poss_pos = [45, 230, 415] # possible y positions

        for root, dirs, files in os.walk(os.getcwd() + '/data/img/stimuli/characters'):
            for name in files:
                char_list.append(name)
        for idx, n in enumerate(range(0, 3)):
            chosen = choice(char_list)
            chosen_y = choice(y_poss_pos)
            char_list.remove(chosen)
            y_poss_pos.remove(chosen_y)
            self.pivot_list.add(StimuliSprite(pygame.image.load('data/img/stimuli/characters/' + chosen).convert(),
                                              (33, 45 * (idx + 1) + 140 * idx),
                                              'pivot' + str(idx)))
            self.target_list.add(StimuliSprite(pygame.image.load('data/img/stimuli/characters/' + chosen).convert(),
                                               (587, chosen_y),
                                               'target' + str(idx)))

    def handle_background_color_changes(self):
        if self.current_pivot_being_dragged is None:
            return

        collisions = pygame.sprite.spritecollide(self.current_pivot_being_dragged, self.target_list, False)

        if len(collisions) == 0:
            self.current_color = 'DEFAULT'
            self.current_pivot_being_dragged.set_half_transparent(False)
            return

        for collided in collisions:
            self.current_pivot_being_dragged.set_half_transparent(True)
            if self.current_pivot_being_dragged.get_type()[5] == collided.get_type()[6]:
                self.current_color = 'RIGHT'
            else:
                self.current_color = 'WRONG'

    def handle_hiding_and_showing(self):
        if self.is_mouse_colliding_with_pivot() and self.is_some_pivot_being_dragged:
            for pivot in self.pivot_list:
                if pivot.get_type() is not self.current_pivot_being_dragged.get_type():
                    pivot.set_half_transparent(True)
        else:
            for pivot in self.pivot_list:
                pivot.set_half_transparent(False)

    def is_mouse_colliding_with_pivot(self):
        return self.current_pivot_being_dragged is not None

    def handle_mouse_pivot_collisions(self):
        current_collisions = pygame.sprite.spritecollide(self.mouse, self.pivot_list, False)

        if len(current_collisions) == 0:
            self.current_pivot_being_dragged = None
        elif len(current_collisions) == 1:
            for collided in pygame.sprite.spritecollide(self.mouse, self.pivot_list, False):
                self.current_pivot_being_dragged = collided

    def handle_input(self, event):
        if event.type == KEYUP and event.key == K_n:
            self.generate_pivots_and_targets()

        if event.type == MOUSEBUTTONDOWN:
            if self.is_mouse_colliding_with_pivot():
                self.is_some_pivot_being_dragged = True
                self.hide_unselected_pivots = True

        if event.type == MOUSEBUTTONUP:
            if not self.current_pivot_being_dragged is None:
                collisions = pygame.sprite.spritecollide(self.current_pivot_being_dragged, self.target_list, False)
                if not len(collisions) > 1:
                    for collided in collisions:
                        if self.current_pivot_being_dragged.get_type()[5] == collided.get_type()[6]:
                            collided.kill()
                            self.current_pivot_being_dragged.kill()
                            self.current_pivot_being_dragged = None
                            break
            self.current_color = 'DEFAULT'
            self.is_some_pivot_being_dragged = False
            self.hide_unselected_pivots = False
            if self.is_mouse_colliding_with_pivot():
                self.current_pivot_being_dragged.go_back_to_root_position()

    def update(self, dt):
        if self.is_some_pivot_being_dragged:
            self.current_pivot_being_dragged.drag()

        self.mouse.update(dt)
        self.handle_hiding_and_showing()

        self.handle_mouse_pivot_collisions()

        self.handle_background_color_changes()

    def draw(self, screen):
        screen.fill(self.colors[self.current_color])
        self.target_list.draw(screen)
        self.pivot_list.draw(screen)

        self.mouse.draw(screen)