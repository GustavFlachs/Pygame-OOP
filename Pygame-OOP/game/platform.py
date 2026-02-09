import pygame
from config import *

class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__
        self.image = pygame.Surface((width, height))
        self.image.fill(platform_color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y