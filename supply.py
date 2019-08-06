import pygame
from random import *


class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r'images\bullet_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100

        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if randint(0, 10) == 1:  # 增加随机扰动 暂定10%发生率
                self.rect.left += choice([-1, 1]) * self.speed
        else:
            self.active = False
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r'images\bomb_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100

        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if randint(0, 10) == 1:  # 增加随机扰动 暂定10%发生率
                self.rect.left += choice([-1, 1]) * self.speed
        else:
            self.active = False
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class LifeSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r'images\life_supply.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100

        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if randint(0, 10) == 1:  # 增加随机扰动 暂定10%发生率
                self.rect.left += choice([-1, 1]) * self.speed
        else:
            self.active = False
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class TheworldSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r'images\clock.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), -100

        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if randint(0, 10) == 1:  # 增加随机扰动 暂定10%发生率
                self.rect.left += choice([-1, 1]) * self.speed
        else:
            self.active = False
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100
