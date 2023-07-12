import pygame as pg
import random
import os
from pygame.locals import *

vec = pg.math.Vector2

pg.init()
pg.display.init()
# Title
TITLE = 'Jump'

# Dimensions
WIDTH = 600
HEIGHT = 800
FPS = 60

# Colors
# Primary Colors
RED = (255, 0, 0)
GREEN = (25, 255, 0)
BLUE = (0, 0, 255)

# Secondary Colors
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Other Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# Starting platforms
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_LIST = [
    (0, HEIGHT-40, WIDTH, 40, (220, 200, 100)),
    (WIDTH/2-50, HEIGHT * 3/4, PLATFORM_WIDTH, PLATFORM_HEIGHT, (200, 200, 200)),
    (400, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT, (200, 200, 200)),
    (PLATFORM_HEIGHT, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT, (200, 200, 200)),
    (600, 50, PLATFORM_WIDTH, PLATFORM_HEIGHT, (200, 200, 200))
]


# Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP_POWER = 20
POWERUP_TIME = 5000  # in milliseconds


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image1 = pg.image.load(os.path.join('assets', 'snowman4.png'))
        self.image2 = pg.image.load(os.path.join('assets', 'snowhappy.png'))
        self.current_image = self.image1
        self.rect = self.current_image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH/2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jump_power = PLAYER_JUMP_POWER
        self.jump_timer = 0
        self.powered_up = False

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # Apply Friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0

        if self.pos.x < 0:
            self.pos.x = WIDTH

        # The rectangle's new position
        self.rect.midbottom = self.pos

        if self.game.background_position.y >= -100:
            self.current_image = self.image2
            if self.game.music != "Happy.mp3":
                self.game.music = "Happy.mp3"
                pg.mixer.music.load(os.path.join('assets', self.game.music))
                pg.mixer.music.play(-1)
        else:
            self.current_image = self.image1
            if self.game.music != "stranger.mp3":
                self.game.music = "stranger.mp3"
                pg.mixer.music.load(os.path.join('assets', self.game.music))
                pg.mixer.music.play(-1)

        self.image = self.current_image

        # Check if the powerup time has elapsed
        if self.powered_up:
            if pg.time.get_ticks() - self.jump_timer > POWERUP_TIME:
                self.jump_power = PLAYER_JUMP_POWER
                self.powered_up = False

        # If the jump timer has expired, reset the jump power to the original value
        if self.jump_timer > 0 and pg.time.get_ticks() - self.jump_timer >= 3000:
            self.jump_power = PLAYER_JUMP_POWER

    def jump(self):
        # If the player is on a platform then it is allowed to jump
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -self.jump_power
            self.jump_timer = pg.time.get_ticks()
            self.powered_up = True


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color, has_scarf):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.has_scarf = has_scarf
        if self.has_scarf:
            self.scarf_image = pg.image.load(os.path.join('assets', 'scarff1.png'))
            self.image.blit(self.scarf_image, (0, 0))  # Blit the scarf image onto the platform image

    def update(self):
        if self.has_scarf and self.rect.colliderect(self.game.player.rect):
            self.has_scarf = False
            self.kill()
            self.game.player.jump_power *= 1.5
            self.game.player.jump_timer = pg.time.get_ticks()
            self.game.player.powered_up = True

    def set_game(self, game):
        self.game = game


class Game:
    def __init__(self):
        # Initialize Pygame and Create Window
        self.running = True
        self.gameOver = False
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.background = pg.image.load(os.path.join('assets', 'mount.jpg')).convert()
        self.background_rect = self.background.get_rect()
        self.background_position = vec(0, -5500)
        self.initial_background_position = vec(0, -5500)

        self.music = "stranger.mp3"
        pg.mixer.music.load(os.path.join('assets', self.music))
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        self.font = pg.font.SysFont("Comic Sans Ms", 30)
        self.time = 0

    def new(self):
        # Start a New Game

        # Groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        # Player object
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.PLAYER_SCORE = 0
        self.time = 0

        # Platform Objects
        for plat in PLATFORM_LIST:
            has_scarf = random.random() < 0.1  # Randomly determine if the platform has a scarf
            p = Platform(*plat, has_scarf)
            p.set_game(self)  # Set the game object for the platform
            self.platforms.add(p)
            self.all_sprites.add(p)

        # Reset background position
        self.background_position = vec(0, -5500)

    def run(self):
        # Game Loop
        self.playing = True
        start_time = pg.time.get_ticks()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            if self.gameOver:
                self.show_go_screen()

            current_time = pg.time.get_ticks()
            elapsed_time = current_time - start_time
            if elapsed_time >= 1000:
                start_time = current_time
                if self.background_position.y < -100:
                    self.time += 1

                else:
                    self.time += 0

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # Check if the player hits a platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

        # If player reaches the top quarter of the screen, the window scrolls up
        if self.player.rect.top < HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top > HEIGHT:
                    if self.background_position.y < -100:
                        self.PLAYER_SCORE += 100
                        print(self.PLAYER_SCORE)
                        plat.kill()
                        self.background_position.y += abs(self.player.vel.y) * 5
                    else:
                        self.player.pos.y += 0
                        self.PLAYER_SCORE = 8849
                        self.background_position.y += 0

        # Spawn New platforms
        while len(self.platforms) < 6:
            p = Platform(random.randint(0, 500), -(random.randint(20, 100)), PLATFORM_WIDTH, PLATFORM_HEIGHT,
                         (200, 200, 200), random.random() < 0.1)
            p.set_game(self)  # Set the game object for the platform
            self.platforms.add(p)
            self.all_sprites.add(p)

        if self.player.rect.top > HEIGHT:
            self.playing = False

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BLACK)
        self.screen.blit(self.background, self.background_position)
        self.all_sprites.draw(self.screen)

        if self.background_position.y < -100:
            self.display_text((str(self.PLAYER_SCORE) + "m"), 10, 0, 30, (50, 20, 30))
        else:
            self.display_text((str(self.PLAYER_SCORE) + "m"), 10, 0, 30, (255, 0, 220))

        self.display_text((str(self.time) + "sec"), 10, 30, 30, (50, 20, 30))  # Display time

        pg.display.flip()

    def show_go_screen(self):
        # Game Over Screen
        start_img_path = os.path.join("assets", "everest.jpg")
        self.image = pg.image.load(start_img_path)
        gameOverLoop = False
        while not gameOverLoop:
            self.screen.blit(self.image, (0, 0))
            self.display_text("To The Everest", WIDTH / 3 - 150, HEIGHT / 4 - 100, 70, (50, 20, 30))
            self.display_text("Use A and D to move left and right", WIDTH / 3 - 150, HEIGHT / 3 + 250, 20, WHITE)
            self.display_text("and press space bar to jump", WIDTH / 3 - 90, HEIGHT / 3 + 280, 20, WHITE)
            self.display_text("Press any key to continue...", WIDTH / 3 - 10, HEIGHT * 2 / 3 + 100, 20, WHITE)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.KEYUP:
                    self.gameOver = False
                    gameOverLoop = True
                    self.new()
        self.background_position = self.initial_background_position

    def display_text(self, message, x, y, size, color):
        font = pg.font.SysFont("Comic Sans Ms", size)
        text = font.render(message, False, color)
        self.screen.blit(text, (x, y))


g = Game()
g.show_go_screen()

while g.running:
    g.new()
    g.run()
    g.show_go_screen()
