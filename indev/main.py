import sys
import time
from sprites import *


def check_new_game():
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
    pygame.event.clear()


def update():
    all_sprites.update()


class Game:
    # Initialize game window, etc
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Shmup!", "./images/playerLife2_orange.png")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = None
        self.playing = False
        self.player = None
        self.m = None
        self.wait = None

    def spawn_mob(self, num):
        for x in range(num):
            self.m = Mob()
            mobs.add(self.m)
            all_sprites.add(self.m)

    # Start New Game
    def new_game(self):
        all_sprites.empty()
        mobs.empty()
        bullets.empty()
        self.score = 0
        self.player = Player()
        all_sprites.add(self.player)
        all_sprites.add(bullets)
        self.spawn_mob(8)
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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                        game.start_screen()

        # Check if a mob hits the player
        hits = pygame.sprite.spritecollide(self.player, mobs, True, pygame.sprite.collide_circle)
        if hits:
            for hit in hits:
                p = Points(self.screen, "-"+str(int(hit.radius * .75)), RED, hit.rect.center, 500)
                all_sprites.add(p)
                e = Explotion(hit.rect.center, 'sm')
                all_sprites.add(e)
                self.player.shield -= int(hit.radius * 0.75)
                self.spawn_mob(1)

                if self.player.shield <= 0 and self.player.lives > 0:
                    death_explotion = Explotion(self.player.rect.center, 'lg')
                    all_sprites.add(death_explotion)
                    self.player.hide()
                    self.player.lives -= 1
                    self.player.shield = 100
            self.wait = pygame.time.get_ticks()
        if self.player.lives == 0:

            self.player.kill()
            if pygame.time.get_ticks() - self.wait >= 1000:
                self.playing = False
                self.game_over_screen(self.score)

        # Check if a bullet hits a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
        if hits:
            for hit in hits:
                p = Points(self.screen, "+" + str(50 - self.m.radius), WHITE, hit.rect.center, 500)
                all_sprites.add(p)
                e = Explotion(hit.rect.center, 'lg')
                all_sprites.add(e)
                if hit.rect.centery < HEIGHT * .25:
                    if random.random() > .90:
                        powerup = Powerup(hit.rect.center)
                        all_sprites.add(powerup)
                        powerups.add(powerup)
            self.score += (50 - self.m.radius)
            for I in range(1):
                self.spawn_mob(1)

        # Check if a power-up hits the player
        hits = pygame.sprite.spritecollide(self.player, powerups, True, pygame.sprite.collide_circle)
        for hit in hits:
            if hit.type == 'shield':
                self.value = random.randrange(10, 15)
                self.player.shield += self.value
                if self.player.shield > 100:
                    self.player.shield = 100
                    p = Points(self.screen, "+0", GREEN, hit.rect.center, 500)
                    all_sprites.add(p)

                else:
                    p = Points(self.screen, "+" + str(self.value), GREEN, hit.rect.center, 500)
                    all_sprites.add(p)

            if hit.type == 'live':
                self.value = 1
                self.player.lives += self.value
                if self.player.lives > 3:
                    self.player.lives = 3
                    p = Points(self.screen, "+0", ORANGE, hit.rect.center, 500)
                    all_sprites.add(p)
                else:
                    p = Points(self.screen, "+" + str(self.value), ORANGE, hit.rect.center, 500)
                    all_sprites.add(p)

    # Game Loop - Draw
    def draw(self):
        self.screen.blit(background, background_rect)
        all_sprites.draw(self.screen)
        draw_lives(self.screen, self.player.lives)
        draw_text(self.screen, str(game.score), 32, WHITE, (WIDTH / 2, 10))
        draw_player_shield(self.screen, self.player.shield)
        pygame.display.flip()

    # Start Screen
    def start_screen(self):
        def text(self):
            self.screen.blit(background, background_rect)
            draw_text(self.screen, "Shmup!", 64, WHITE, (WIDTH / 2, HEIGHT / 4))
            draw_text(self.screen, "Arrow keys to move, space to fire", 22, WHITE, (WIDTH / 2, HEIGHT / 2))
            draw_text(self.screen, "press any key to continue or Esc to exit", 16, WHITE, (WIDTH / 2, HEIGHT * 3 / 4))
        waiting = True
        while waiting:
            text(self)
            pygame.display.flip()
            self.clock.tick(FPS)
            check_new_game()

    # Game Over/Continue
    def game_over_screen(self, score):
        all_sprites.empty()
        mobs.empty()
        bullets.empty()

        self.wait = pygame.time.get_ticks()
        self.screen.blit(background, background_rect)
        draw_text(self.screen, "GAME OVER", 64, WHITE, (WIDTH / 2, HEIGHT / 4))
        draw_text(self.screen, "Your Score: " + str(score), 32, WHITE, (WIDTH / 2, HEIGHT / 2))
        draw_text(self.screen, "press any key to continue or Esc to exit", 16, WHITE, (WIDTH / 2, HEIGHT * 3 / 4))

        pygame.display.flip()
        waiting = True
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
                        game.start_screen()
            pygame.event.clear()
            

game = Game()
game.start_screen()
