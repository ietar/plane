import pygame
from random import *

miss = [0, 0, 0]
create = [2, 6, 15]


class SmallEnemy(pygame.sprite.Sprite):
    energy = 1

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'images\enemy1.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r'images\enemy1_down1.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy1_down2.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy1_down3.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy1_down4.png').convert_alpha()
                                    ])
        self.initpos1 = 5
        self.initpos2 = 0
        self.speed = 2
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]

        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.maxenergy = SmallEnemy.energy
        self.energy = SmallEnemy.energy
        self.hit = False
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-self.initpos1 * self.height, -self.initpos2 * self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            miss[2] += 1
            self.reset()

    def reset(self):
        create[2] += 1
        self.active = True
        self.energy = self.maxenergy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-self.initpos1 * self.height, -self.initpos2 * self.height)


class MidEnemy(pygame.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'images\enemy2.png').convert_alpha()
        self.image_hit = pygame.image.load(r'images\enemy2_hit.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r'images\enemy2_down1.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy2_down2.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy2_down3.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy2_down4.png').convert_alpha()
                                    ])
        self.initpos1 = 10
        self.initpos2 = 5
        self.speed = 1
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]

        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.maxenergy = MidEnemy.energy
        self.energy = MidEnemy.energy
        self.hit = False
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-self.initpos1 * self.height, -self.initpos2 * self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            miss[1] += 1
            self.reset()

    def reset(self):
        create[1] += 1
        self.active = True
        self.energy = self.maxenergy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-self.initpos1 * self.height, -self.initpos2 * self.height)


class BigEnemy(pygame.sprite.Sprite):
    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load(r'images\enemy3_n1.png').convert_alpha()
        self.image = self.image1
        self.image2 = pygame.image.load(r'images\enemy3_n2.png').convert_alpha()
        self.image_hit = pygame.image.load(r'images\enemy3_hit.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r'images\enemy3_down1.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy3_down2.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy3_down3.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy3_down4.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy3_down5.png').convert_alpha(),
                                    pygame.image.load(r'images\enemy3_down6.png').convert_alpha()
                                    ])
        self.initpos1 = 15
        self.initpos2 = 5
        self.speed = 1
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]

        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.maxenergy = BigEnemy.energy
        self.energy = BigEnemy.energy
        self.hit = False
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-self.initpos1 * self.height, -self.initpos2 * self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            miss[0] += 1
            self.reset()

    def reset(self):
        create[0] += 1
        self.active = True
        self.energy = self.maxenergy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-self.initpos1 * self.height, -self.initpos2 * self.height)
