import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
CLOUD_SPAWN_INTERVAL = 2
LEVEL_DURATION = 30
GRAVITY_DELAY = 3

class Butterfly:
    def __init__(self):
        self.image = pygame.image.load("butterfly.png")
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.gravity = 0.5
        self.jump_strength = -10
        self.velocity = 0
        self.gravity_active = False
        self.start_time = time.time()

    def jump(self):
        if self.gravity_active:
            self.velocity = self.jump_strength

    def update(self):
        if not self.gravity_active and time.time() - self.start_time >= GRAVITY_DELAY:
            self.gravity_active = True

        if self.gravity_active:
            self.velocity += self.gravity
            self.rect.y += self.velocity
        else:
            self.velocity = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
