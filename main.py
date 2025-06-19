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

    def update(self, speed):
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


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    butterfly = Butterfly()
    clouds = []
    score = Score()
    level = Level()
    running = True
    cloud_timer = 0
    last_cloud_y = -100
    game_over = False
    game_over_time = 0

    while running:
        screen.fill((0, 0, 0))
        background = pygame.image.load(level.backgrounds[level.current_level])
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    butterfly.jump()

        if not game_over:
            butterfly.update()

            if butterfly.gravity_active:
                cloud_timer += 1 / FPS
                if cloud_timer >= CLOUD_SPAWN_INTERVAL:
                    new_cloud_y = random.randint(50, HEIGHT - 50)
                    while abs(new_cloud_y - last_cloud_y) < 100:
                        new_cloud_y = random.randint(50, HEIGHT - 50)
                    clouds.append(Cloud(new_cloud_y))
                    last_cloud_y = new_cloud_y
                    cloud_timer = 0

            speed = level.cloud_speed[level.current_level]
            for cloud in clouds[:]:
                cloud.update(speed)
                if cloud.rect.x < 0:
                    clouds.remove(cloud)
                    score.increment()
                cloud.draw(screen)

            if butterfly.gravity_active:
                if check_collision(butterfly, clouds) or butterfly.rect.y >= HEIGHT:
                    game_over = True
                    game_over_time = time.time()

            if level.is_level_completed():
                print("Level Completed!")
                level.next_level()
                if level.current_level >= len(level.backgrounds):
                    print("You have completed all levels!")
                    running = False

            butterfly.draw(screen)
            score.draw(screen, level.current_level + 1)

            if not butterfly.gravity_active:
                time_left = max(0, GRAVITY_DELAY - (time.time() - butterfly.start_time))
                font = pygame.font.Font(None, 72)
                countdown_text = font.render(f"Starting in: {int(time_left) + 1}", True, (255, 255, 255))
                text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(countdown_text, text_rect)
        else:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

            if time.time() - game_over_time >= 3:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()