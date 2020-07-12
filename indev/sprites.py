from settings import *
import pygame
import random

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()

pygame.mixer.init()


def draw_lives(surface, lives):
    x = 400
    x2 = 400
    for ignore in range(3):
        bg_rect = life_bg.get_rect()
        bg_rect.x = x2
        bg_rect.y = 25
        surface.blit(life_bg, bg_rect)
        x2 += 50
    for I in range(lives):
        img_rect = life_img.get_rect()
        img_rect.x = x
        img_rect.y = 25
        surface.blit(life_img, img_rect)
        x += 50

    draw_text(surface, "lives:", 16, WHITE, (470, 5))


def draw_text(surface, text, size, color, center):
    font = pygame.font.Font((path.join(img_dir, "kenvector_future_thin.ttf")), size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.midtop = center
    surface.blit(text, text_rect)
    pygame.display.update(text_rect)

def draw_text_uwe(surface, text, size, color, center):
    font = pygame.font.Font((path.join(img_dir, "kenvector_future_thin.ttf")), size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.midtop = center
    surface.blit(text, text_rect)
    return pygame.Surface((text_rect.width, text_rect.height))


def draw_player_shield(surface, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 15
    outline_height = 18
    fill = (pct / 50) * bar_length
    outline_rect = pygame.Rect(WIDTH / 15, 20, ((100 / 50) * 100), outline_height)
    fill_rect = pygame.Rect(WIDTH / 15 + 2, outline_rect.y + 2, fill - 2, bar_height)
    pygame.draw.rect(surface, WHITE, outline_rect, 4)
    if pct < 20:
        pygame.draw.rect(surface, RED, fill_rect)
    elif pct < 40:
        pygame.draw.rect(surface, YELLOW, fill_rect)
    else:
        pygame.draw.rect(surface, GREEN, fill_rect)
    draw_text(surface, "shield:", 16, WHITE, (outline_rect.centerx, outline_rect.y - 20))
    draw_text(surface, (str(int(pct / 100 * bar_length))) + "%", 16, WHITE, outline_rect.midtop)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_ship
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .35)
        self.shield = 100
        self.lives = 3
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.velx = 0
        self.accx = 0
        self.key_down = None
        self.shoot_delay = 400
        self.last_shoot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer >= 1500 and self.lives != 0:
            self.hidden = False
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = (HEIGHT - 10)

        self.accx = 0
        self.key_down = pygame.key.get_pressed()
        if self.key_down[pygame.K_LEFT]:
            self.accx = -0.4
        if self.key_down[pygame.K_RIGHT]:
            self.accx = 0.4
        if self.key_down[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shoot > self.shoot_delay and not self.hidden:
                self.last_shoot = now
                self.shoot()
                laser_snd.play()
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

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


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
        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        self.rect.x = random.randrange(0, (WIDTH - 20))
        self.rect.bottom = 0
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(1, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.old_center = None
        self.new_image = None
        self.posy = None
        self.posx = None

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


class Explotion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.current_img = 0
        self.image = explotion_anim[self.size][self.current_img]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        explotion_snd.play()
        self.now = None
        self.frame_rate = 70

    def update(self):
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update > self.frame_rate:
            self.last_update = self.now
            self.current_img += 1
            self.image = explotion_anim[self.size][self.current_img]
            if self.current_img >= 8:
                self.kill()


class Points(pygame.sprite.Sprite):
    def __init__(self, surface, points, color, center, time: any):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.surface = surface
        self.points = str(points)
        self.rect.center = center
        self.color = color
        self.time = time
        self.wait = pygame.time.get_ticks()
        self.bound = self.image.get_bounding_rect()

        self.font = pygame.font.Font((path.join(img_dir, "kenvector_future_thin.ttf")), 24)
        self.text = self.font.render(str(self.points), True, self.color)
        self.text_rect = self.text.get_rect()

    def update(self):
        self.text_rect.center = self.rect.center
        self.surface.blit(self.text, self.text_rect)
        pygame.display.update(self.rect)
        if not self.time:
            pass
        else:
            if pygame.time.get_ticks() - self.wait > self.time:
                self.kill()


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        if random.random() > .99:
            self.type = 'live'
        else:
            self.type = 'shield'
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.centery += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Button(pygame.sprite.Sprite):
    def __init__(self, surface, text, color, center):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.image = pygame.Surface((100, 50))
        self.rect = self.image.get_rect()
        self.fill_rect = pygame.Rect(WIDTH/2, HEIGHT/2, 100, 50)
        self.fill = pygame.draw.rect(self.surface, LIGHT_GRAY, self.fill_rect)

        self.rect.center = center
        self.content = str(text)
        self.text_color = color

    def update(self):
        self.mouse_posx, self.mouse_posy = pygame.mouse.get_pos()
        if self.rect.right > self.mouse_posx > self.rect.left and self.mouse_posy > self.rect.top and self.mouse_posy < self.rect.bottom:
            pass


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemy_ship_img)
    def update(self):
        pass



