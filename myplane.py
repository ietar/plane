import pygame


class Myplane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(r'images\me1.png').convert_alpha()
        self.image2 = pygame.image.load(r'images\me2.png').convert_alpha()
        self.life_image = pygame.image.load(r'images\life.png').convert_alpha()
        self.life_rect = self.life_image.get_rect()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r'images\me_destroy_1.png').convert_alpha(),
                                    pygame.image.load(r'images\me_destroy_2.png').convert_alpha(),
                                    pygame.image.load(r'images\me_destroy_3.png').convert_alpha(),
                                    pygame.image.load(r'images\me_destroy_4.png').convert_alpha()
                                    ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 60
        self.speed = 10
        self.life = 3

        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.wudi = False  # cheating code
        self.rebornprotect = False

    def moveup(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def movedown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveleft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveright(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 60
        self.active = True
