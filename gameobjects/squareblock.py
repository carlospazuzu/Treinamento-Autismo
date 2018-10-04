import pygame

class SquareBlock(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((180, 180))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.image.fill((100, 100, 100))
        self.image.set_colorkey((100, 100, 100))     
        self.alpha = 255
        self.modifier = -5   

    def update(self, dt):
        self.alpha += self.modifier
        if self.alpha >= 255:
            self.modifier = -5
        elif self.alpha <= 128:
            self.modifier = 5
        
        self.image.set_alpha(self.alpha)
        pygame.draw.rect(self.image, (254, 254, 254), (0, 0, 180, 180))

    def draw(self, screen):
        #pygame.draw.rect(self.image, (254, 254, 254), (0, 0, 180, 180))
        screen.blit(self.image, self.rect)