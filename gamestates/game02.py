import pygame, os
from pygame.locals import *
from random import randint
from random import choice
from gameobjects import playermouse
from gameobjects.stimulisprite import StimuliSprite

class Game02:

    def __init__(self, statemanager):
        self.sm = statemanager
        self.mouse = playermouse.PlayerMouse()
        self.pivot_img = pygame.image.load('data/img/stimuli/fruits/apple.jpg').convert()
        self.pivot_position = (310, 57) # initial pivot position
        self.pivot = StimuliSprite(self.pivot_img, self.pivot_position, 'pivot')
        self.is_pivot_being_dragged = False
        self.stimuli_positions = [(66, 391), (310, 391), (554, 391)]
        self.current_pivot_target_chosen_position = randint(0, 2)
        self.first_regular_stimuli_position = None
        self.match_stimulis = pygame.sprite.Group()
        self.match_stimulis.add(StimuliSprite(self.pivot_img.copy(), 
                                              self.stimuli_positions[self.current_pivot_target_chosen_position],
                                              'pivot_target'))
        self.fruit_list = []
        for root, dirs, files in os.walk(os.getcwd() + '/data/img/stimuli/fruits'):
            for name in files:                
                self.fruit_list.append(name)

        self.colors = {
                        'DEFAULT': (118, 173, 210),
                        'RIGHT': (119, 209, 128),
                        'WRONG': (230, 53, 50)
                      }
        self.current_color = 'DEFAULT'
        self.hits = 0    
        self.mistakes = 0   
        self.hit_sound = pygame.mixer.Sound('data/audio/right.wav')
        self.level_up_constant = 5 # ammount of accepts to increase difficult
        self.pivot_fruit = 'apple.jpg' # apple index
        self.fruit_list.remove(self.pivot_fruit)
        self.first_regular_stimuli_fruit = None

    # method to get available stimuli position WHEN inserting new
    def get_available_position(self):
        # if there is only pivot target on the match stimulis list        
        if len(self.match_stimulis) == 1:
            pos = 0
            while pos == self.current_pivot_target_chosen_position:
                pos = randint(0, 2)
            self.first_regular_stimuli_position = pos
            return self.stimuli_positions[pos]
        elif len(self.match_stimulis) == 2:    
            positions = [0, 1, 2]            
            positions.remove(self.current_pivot_target_chosen_position)
            print(positions)        
            print(self.first_regular_stimuli_position)        
            positions.remove(self.first_regular_stimuli_position)                        
            return self.stimuli_positions[positions[0]]

    def get_available_fruit(self):        
        rand_value = self.fruit_list[randint(0, len(self.fruit_list) - 1)]
        self.fruit_list.remove(rand_value)
        return rand_value

    def check_score_and_properly_adapt_difficulty(self):        
        if self.hits % self.level_up_constant == 0 and self.hits is not 0 and self.hits < self.level_up_constant * 3:
            self.match_stimulis.add(StimuliSprite(pygame.image.load('data/img/stimuli/fruits/' + self.get_available_fruit()).convert(),
                                                                        self.get_available_position()))
            self.hits += 1 # needed to force algorithm not to enter twice             

    def get_pivot_target(self):
        for p in self.match_stimulis:
            if p.get_type() == 'pivot_target':
                return p

    # forces pivot target stimuli get a new position different from previous one
    def get_new_position_for_pivot_target(self):        
        new_position = self.current_pivot_target_chosen_position
        while new_position == self.current_pivot_target_chosen_position:
            new_position = randint(0, 2)
        self.current_pivot_target_chosen_position = new_position
        return self.stimuli_positions[new_position]        

    # increase or decrease score and rearrange stimulis positions
    def properly_reorganize_targets(self, condition):
        if condition == 'hit':
            self.hits += 1
            self.hit_sound.play()
        elif condition == 'miss':
            self.mistakes += 1                
        #print('hits = ' + str(self.hits) + ' mistakes = ' + str(self.mistakes))
        self.get_pivot_target().set_position(self.get_new_position_for_pivot_target())
                
        position = [0, 1, 2]
        position.remove(self.current_pivot_target_chosen_position)
        cont = 0
        for tgt in self.match_stimulis.sprites():            
            if tgt.get_type() != 'pivot_target':                
                chosen = choice(position)
                if cont <= 0: # force algorithm give position only to the first regular stimuli
                    cont += 1
                    self.first_regular_stimuli_position = chosen
                position.remove(chosen)
                tgt.set_position(self.stimuli_positions[chosen])

    # handle background color changes by detecting if pivot image is colliding with targets
    def handle_background_color(self):
        if self.check_collision()[0]:
            if self.check_collision()[1].get_type() == 'pivot_target':
                self.current_color = 'RIGHT'
            else:                           
                self.current_color = 'WRONG'
        else:
            self.current_color = 'DEFAULT'

    # return if collided and which who collided with
    def check_collision(self):
        has_collided, col = False, None        
        for collided in pygame.sprite.spritecollide(self.pivot, self.match_stimulis, False):
            has_collided = True            
            col = collided
        if not has_collided:
            has_collided = False

        return (has_collided, col)

    def handle_pivot_transparency(self):
        if pygame.sprite.spritecollide(self.pivot, self.match_stimulis, False):
            self.pivot.set_half_transparent(True)
        else:
            self.pivot.set_half_transparent(False)

    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if pygame.sprite.collide_rect(self.mouse, self.pivot):
                self.is_pivot_being_dragged = True                   

        if event.type == MOUSEBUTTONUP:
            self.is_pivot_being_dragged = False
            self.pivot.go_back_to_root_position()
            self.pivot.set_half_transparent(False)
            if self.current_color == 'RIGHT':
                self.properly_reorganize_targets('hit')       
            elif self.current_color == 'WRONG':
                self.properly_reorganize_targets('miss')       
        
    def update(self, dt):
        if self.is_pivot_being_dragged:
            self.pivot.drag()

        self.mouse.update(dt)
        self.handle_pivot_transparency()   
        self.handle_background_color()     

        self.check_score_and_properly_adapt_difficulty()

    def draw(self, screen):
        screen.fill(self.colors[self.current_color])               
                
        self.match_stimulis.draw(screen)

        self.pivot.draw(screen)
        self.mouse.draw(screen)