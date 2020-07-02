# Game constants - settings
from os import path
import pygame





# ---Window settings
WIDTH = 600
HEIGHT = 800
FPS = 60

# ---Define Colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
DARK_GRAY = 55, 55, 55
LIGHT_GRAY = 100, 100, 100
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0

# ---Directories
img_dir = path.join(path.dirname(__file__), "images")
meteor_dir = path.join(img_dir, "meteors")
explotion_dir = path.join(img_dir, "explotion")
snd_dir = path.join(path.dirname(__file__), "sounds")

# ---Global variables
clock = pygame.time.Clock()

# ---Load images/sounds
pygame.mixer.init()

background = pygame.image.load(path.join(img_dir, "black.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

life_img = pygame.image.load(path.join(img_dir, "playerLife2_orange.png"))
player_ship = pygame.image.load(path.join(img_dir, "playerShip2_orange.png"))
laser = pygame.image.load(path.join(img_dir, "laserBlue01.png"))
laser_snd = pygame.mixer.Sound(path.join(snd_dir, "sfx_laser1.wav"))


meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big3.png',
               'meteorBrown_big4.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png',
               'meteorBrown_small2.png', 'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png',
               'meteorGrey_big1.png', 'meteorGrey_big3.png',
               'meteorGrey_big4.png', 'meteorGrey_med1.png',
               'meteorGrey_med2.png', 'meteorGrey_small1.png',
               'meteorGrey_small2.png', 'meteorGrey_tiny1.png',
               'meteorGrey_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(meteor_dir, img)))

explotion_anim = {}
explotion_anim['lg'] = []
explotion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    explotion_anim['sm'].append(pygame.transform.scale(pygame.image.load(path.join(explotion_dir, filename)), (int(192/3), int(192/3))))
    explotion_anim['lg'].append(pygame.image.load(path.join(explotion_dir, filename)))
explotion_snd = pygame.mixer.Sound(path.join(snd_dir, "explosion.wav"))

