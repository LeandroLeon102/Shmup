import sys
import time, threading
from sprites import *


def draw_text(text, size, color, x, y):
    font = pygame.font.Font((path.join(img_dir, "kenvector_future_thin.ttf")), size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.midtop = (x, y)
    game.screen.blit(text, text_rect)

def draw_points(points, color, x, y):
    draw_text(points, 12, color, x, y)
    time.sleep(1)

def draw_player_shield(pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 15
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(5, 5, 100, bar_height)
    fill_rect = pygame.Rect(5, 5, fill, bar_height)
    if pct < 20:
        pygame.draw.rect(game.screen, RED, fill_rect)
    elif pct < 40:
        pygame.draw.rect(game.screen, YELLOW, fill_rect)
    else:
        pygame.draw.rect(game.screen, GREEN, fill_rect)
    pygame.draw.rect(game.screen, WHITE, outline_rect, 3)
    draw_text((str(int(pct/100 * bar_length))) + "%", 16, WHITE, 55, 4)


def update():
    all_sprites.update()


class Game:

    # Initialize game window, etc
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = None
        self.playing = False
        self.player = None
        self.m = None

    # Start New Game
    def new_game(self):
        self.score = 0
        self.player = Player()
        all_sprites.add(self.player)
        all_sprites.add(bullets)
        for m in range(8):
            self.m = Mob()
            mobs.add(self.m)
        all_sprites.add(mobs)
        self.run()

    # Game Loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            update()
            self.draw()

    # Game Loop - Events
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                    game.start_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser_snd.play()
                    self.player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                        game.start_screen()

        # Check if a mob hits the player
        hits = pygame.sprite.spritecollide(self.player, mobs, True, pygame.sprite.collide_circle)
        if hits:



            self.player.shield += int(-(self.m.radius / 3))
            for i in range(1):
                self.m = Mob()
                all_sprites.add(self.m)
                mobs.add(self.m)
                if self.player.shield <= 0:
                    if self.playing:
                        self.playing = False
                        game.start_screen()

        # Check if a bullet hits a mob
        hits = pygame.sprite.groupcollide(bullets, mobs, True, True, pygame.sprite.collide_circle)
        if hits:
            for hit in hits:
                e = Explotion(hit.rect.center)
                all_sprites.add(e)
            #print("mob radius =", self.m.radius, ", points =", (50 - self.m.radius))
            self.score += (50 - self.m.radius)
            for i in range(1):
                self.m = Mob()
                all_sprites.add(self.m)
                mobs.add(self.m)

    # Game Loop - Draw
    def draw(self):
        self.screen.blit(background, background_rect)
        draw_text(str(game.score), 32, WHITE, WIDTH/2, 10)
        draw_player_shield(self.player.shield)
        all_sprites.draw(self.screen)
        pygame.display.flip()

    # Start Screen
    def start_screen(self):
        all_sprites.empty()
        mobs.empty()
        bullets.empty()
        self.screen.blit(background, background_rect)

        draw_text("Shmup!", 64, WHITE, WIDTH / 2, HEIGHT / 4)
        draw_text("Arrow keys to move, space to fire", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        draw_text("press a key to begin or scape to exit", 18, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        waiting = True
        pygame.display.flip()
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.running = False
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key != pygame.K_ESCAPE:
                        game.new_game()
                        waiting = False

    # Game Over/Continue
    def game_over_screen(self):
        pass


game = Game()
game.start_screen()
