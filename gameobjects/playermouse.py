import pygame

class PlayerMouse(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/img/pointer-strk.png')
        self.rect = self.image.get_rect()
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]

    def update(self, dt):
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)