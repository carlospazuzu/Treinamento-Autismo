import pygame

class CheeringBoy:

    def __init__(self):
        self.expressions = {}
        self.expressions['SMILING'] = pygame.image.load('data/img/smile/smilingx2.png')
        self.expressions['BLINKING'] = pygame.image.load('data/img/smile/blinkingx2.png')
        self.image = self.expressions['SMILING']
        # defining x and y coordinates in center of screen
        self.x = (800 / 2) - 85 
        self.y = (600 / 2) - 85
        self.gravity = 150
        self.moving_force = 600
        self.blink_sound = pygame.mixer.Sound('data/audio/blink2.wav')  
        self.has_played = False      
        self.respawn_delay = 1500
        self.respawn_delay_count = 0
        self.finished = False

    def is_finished(self):
        return self.finished

    def update(self, dt):        
        self.y -= self.moving_force * dt
        self.moving_force -= self.gravity
        if self.y >= 215:
            self.y = 215
            self.image = self.expressions['BLINKING']
            if not self.has_played:
                self.blink_sound.play()
                self.has_played = True
            self.respawn_delay_count += dt * 1000
            if self.respawn_delay_count >= self.respawn_delay:
                self.finished = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))