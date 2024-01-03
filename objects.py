import pygame
import random
import math


# Constants
FPS = 24
WIDTH = 1000
HEIGHT = 700
TARGET_SIZE = 50
BACKGROUND = pygame.image.load("images/background.jpg")
player_picture = pygame.image.load("images/player.png")
target_texture = pygame.image.load("images/target.png")
arrow_texture = pygame.image.load("images/arrow.png")


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))


class Player(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.x_speed = 0

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(player_picture, int(angle))

    def update(self, screen):
        # Horizontal movement
        self.rect.x += self.x_speed

        # Border Check
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

        self.rotate()

        screen.blit(pygame.transform.scale(self.image, (self.width, self.height)), self.rect)
        
    def fire(self, ammo, speed):
        arrow = Arrow(self.rect.right - self.rect.width/2 - 15, self.rect.centery - 100, 30, 100, arrow_texture, speed)
        ammo.add(arrow)


class Arrow(GameSprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image)
        speed_x, speed_y = self.define_speed(speed)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def define_speed(self, speed):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        # angle = (180 / math.pi - 90) * -math.atan2(rel_y, rel_x)
        # self.image = pygame.transform.rotate(arrow_texture, int(angle))
        hyp = math.sqrt(rel_x**2 + rel_y**2)
        sin_a = rel_y / hyp
        cos_a = rel_x / hyp
        return speed * cos_a, speed * sin_a

    def fly(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.kill()


class Target(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0 or self.rect.right >= WIDTH or random.randint(1, 20) == 1:
            self.speed = -self.speed
