import pygame
import spritesheet

class Object(pygame.sprite.Sprite):

    def __init__(self, x, y, image_path, scale=(48,96)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale)
        self.position = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.position)

class Button(Object):

    def __init__(self, x, y, image_path, scale=(48, 96)):

        self.sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        self.unpressed = spritesheet.SpriteSheet(self.sprite_sheet_image).get_image(0, 192, 96)
        self.pressed = spritesheet.SpriteSheet(self.sprite_sheet_image).get_image(1, 192, 96)
        self.image = self.unpressed
        self.position = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
