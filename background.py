import pygame
import constants

class Background(pygame.sprite.Sprite):
    image = None
    x = 0
    y = 0

    def __init__(self, image_path, x, y, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT):
        bg_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(bg_image, (width, height))
        self.x = x
        self.y = y
        self.velocity = [0, 0]

    def get_position(self):
        return (self.x, self.y)
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        
    def reset(self):
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y
    def update(self, screen_scroll):
        self.x += self.velocity[0] + screen_scroll[0]
        self.y += self.velocity[1] + screen_scroll[1]

    def scroll_up(self):
        self.velocity[1] = 1

    def stop_scrolling(self):
        self.velocity[1] = 0