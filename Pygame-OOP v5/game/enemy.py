import pygame
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, platform):
        super().__init__()
        self.width = 36
        self.height = 36
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = platform.rect.top
        self.platform = platform

        # movement state
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.8, 2.5)
        # next time (ms) to randomize behavior
        self.next_change = pygame.time.get_ticks() + random.randint(400, 2000)
        # if paused, until time (ms)
        self.pause_until = 0

        # small jitter probability per frame (0..1)
        self.jitter_chance = 0.02
        # chance to do a short pause on change
        self.pause_chance = 0.25
        # chance to flip direction on change
        self.flip_chance = 0.35

    def _randomize_behavior(self):
        now = pygame.time.get_ticks()
        # set next change
        self.next_change = now + random.randint(500, 2500)
        # maybe pause for a short while
        if random.random() < self.pause_chance:
            self.pause_until = now + random.randint(200, 800)
            # small chance to flip direction after pause
            if random.random() < self.flip_chance:
                self.direction *= -1
        else:
            # change speed a bit and maybe direction
            self.speed = random.uniform(0.6, 3.0)
            if random.random() < self.flip_chance:
                self.direction *= -1

    def update(self):
        now = pygame.time.get_ticks()

        # randomize periodically
        if now >= self.next_change and now >= self.pause_until:
            self._randomize_behavior()

        # if paused, do nothing except small jitter
        if now < self.pause_until:
            # small visual jitter while paused
            if random.random() < 0.015:
                self.rect.x += random.choice([-1, 1])
        else:
            # movement step
            step = int(self.direction * self.speed)
            self.rect.x += step

            # occasional tiny jitter to be less regular
            if random.random() < self.jitter_chance:
                self.rect.x += random.choice([-1, 0, 1])

        # keep on screen edges and flip if necessary
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
            self.next_change = now + random.randint(200, 800)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1
            self.next_change = now + random.randint(200, 800)

        # pokud enemy vykročil z platformy, otočit směr a vrátit se
        feet_check_rect = self.rect.move(0, 2)
        if not feet_check_rect.colliderect(self.platform.rect):
            # krok zpět
            self.rect.x -= int(self.direction * max(1, self.speed))
            # otočit a krátce pauznout
            self.direction *= -1
            self.pause_until = now + random.randint(150, 600)
            self.next_change = now + random.randint(300, 1200)

    def draw(self, screen):
        screen.blit(self.image, self.rect)