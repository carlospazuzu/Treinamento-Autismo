import pygame

class TitleButton(pygame.sprite.Sprite):

    def __init__(self, x, y, purpose):        
        pygame.sprite.Sprite.__init__(self)
        self.purpose = purpose
        self.btn = pygame.image.load('data/img/button/button.png')
        self.btnpsd = pygame.image.load('data/img/button/button-pressed.png')
        self.image = self.btn
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_image_to(self, state):
            if state == 'NORMAL':
                self.image = self.btn
            elif state == 'PRESSED':
                self.image = self.btnpsd
    
    def get_purpose(self):
        return self.purpose

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    