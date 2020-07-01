from settings import *
import pygame
import random
from os import path

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()

pygame.mixer.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_ship
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .35)
        # pygame.draw.circle(self.image, GREEN, (self.rect.center), self.radius)
        self.shield = 100
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT-10
        self.velx = 0
        self.accx = 0
        self.key_down = None

    def update(self):
        self.accx = 0
        self.key_down = pygame.key.get_pressed()
        if self.key_down[pygame.K_LEFT]:
            self.accx = -0.5
        if self.key_down[pygame.K_RIGHT]:
            self.accx = 0.5
        self.rect.x += self.velx
        if self.rect.left < 0:
            self.velx = 0
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.velx = 0
            self.rect.right = WIDTH
        self.velx += self.accx
        self.rect.centerx += self.velx

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)
        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        #pygame.draw.circle(self.image_orig, RED, (self.rect.center), self.radius)
        self.rect.x = random.randrange(0, (WIDTH - 20))
        self.rect.bottom = 0
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(1, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.new_image = pygame.transform.rotate(self.image_orig, self.rot)
            self.old_center = self.rect.center
            self.image = self.new_image
            self.rect = self.image.get_rect()
            self.rect.center = self.old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, (WIDTH - 20))
            self.rect.bottom = 0
        self.posx = self.rect.centerx
        self.posy = self.rect.centery


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -10
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy


class Explotion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.current_img = 0
        self.image = explotion_anim[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        explotion_snd.play()

    def update(self):
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update > 60:
            self.last_update = self.now
            self.current_img += 1
            self.image = explotion_anim[self.current_img]
            if self.current_img >= 8:
                self.kill()


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200, 50))
        self.image.fill(DARK_GRAY)
        self.content =  None
        self.rect = self.image.get_rect()
        self.rect.center.x = x
        self.rect.center.y = y

    def update(self):
        self.focussed = pygame.mouse.get_focused()
        if self.focussed:
            self.image.fill(LIGHT_GRAY)
        else:
            self.image.fill(DARK_GRAY)

