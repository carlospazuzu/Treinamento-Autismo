import pygame

class StimuliSprite(pygame.sprite.Sprite):

    def __init__(self, img, pos, type='regular'):
        pygame.sprite.Sprite.__init__(self)      
        self.type = type  
        self.image = img
        self.rect = self.image.get_rect()
        self.root_position = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.alpha = 255

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_type(self):
        return self.type

    # use this function ONLY if its type is pivot
    def go_back_to_root_position(self):
        self.rect.x = self.root_position[0]
        self.rect.y = self.root_position[1]

    def set_half_transparent(self, transparent):
        if transparent:
            self.alpha = 128
        else:
            self.alpha = 255
        self.image.set_alpha(self.alpha)

    def drag(self):
        # sei la que desgraca e essa, so sei que funciona
        self.rect.x += pygame.mouse.get_pos()[0] - self.image.get_width() / 2 - self.rect.x
        self.rect.y += pygame.mouse.get_pos()[1] - self.image.get_height() / 2 - self.rect.y

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)