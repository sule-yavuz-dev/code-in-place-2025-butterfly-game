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

class Cloud:
    def __init__(self, y_position):
        self.image = pygame.image.load("cloud.png")
        self.rect = self.image.get_rect(center=(WIDTH, y_position))

        def update(Self, speed):
            self.rect.x -= speed

        def draw(self, screen):
            screen.blit(self.image, self.rect)

def check_collision(butterfly, clouds):
    for cloud in clouds:
        if butterfly.rect.colliderect(cloud.rect):
            return True
    return False

class Score:
    def __init__(self):
        self.score = 0

    def increment(self):
        self.score += 1

    def draw(self, screen, level_number):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}  Level: {level_number}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

class Level:
    def __init__(self):
        self.current_level = 0
        self.backgrounds = ["bg1.jpg", "bg2.jpg", "bg3.jpg"]
        self.cloud_speed = [3, 5, 7]
        self.start_time = time.time()

    def next_level(self):
        self.current_level += 1
        self.start_time = time.time()

    def reset(self):
        self.current_level = 0

    def is_level_completed(self):
        return time.time() - self.start_time >= LEVEL_DURATION
