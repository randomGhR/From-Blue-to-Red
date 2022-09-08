
import math
import pygame
from player import Player
from enemy import Invader
from bullet import Bullet

pygame.init()
pygame.mixer.init()


class GameScene:
    def __init__(self, window):
        self.init_variables(window)
        self.update_highest_score()
        self.init_backgrounds()
        self.init_and_update_labels()
        self.init_clock()
        self.init_sprite_groups()

    # Variable initialization
    def init_variables(self, window):
        self.state = "Game"
        self.player = Player()
        self.score = 0
        self.highest_score = 0
        self.stage = 1
        self.stage_difference = 50
        self.font = pygame.font.Font("..\\assets\\Fonts\\pocod.ttf", 10)
        self.window = window
        self.window.fill(pygame.Color("Black"))
        self.SCREEN_WIDTH = self.window.get_width()
        self.SCREEN_HEIGHT = self.window.get_height()

        self.spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_timer, 950)

        self.parry_time = 0
        self.is_parrying = False
        self.is_parry_on_cooldown = False

    # Background initialization
    def init_backgrounds(self):
        self.scroll = 0
        self.background = pygame.image.load("..\\assets\\backgrounds\\bloody way\\background.png").convert_alpha()
        self.background = pygame.transform.flip(self.background, True, False)
        self.tiles = math.ceil((self.SCREEN_WIDTH / self.background.get_width())) + 1

    # Clock initialization
    def init_clock(self):
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.ticks = pygame.time.get_ticks()

    # Labels initialization and updating
    def init_and_update_labels(self):
        self.highest_score_label = self.font.render(f"Highest score = {self.highest_score}", True, pygame.Color("White")).convert_alpha()
        self.highest_score_rect = self.highest_score_label.get_rect(topleft=(0, 0))

        self.score_label = self.font.render(f"Score = {self.score}", True, pygame.Color("White")).convert_alpha()
        self.score_rect = self.score_label.get_rect(topleft=self.highest_score_rect.bottomleft)

        self.health_label = self.font.render(f"Health = {self.player.health}", True, pygame.Color("White")).convert_alpha()
        self.health_rect = self.score_label.get_rect(topleft=self.score_rect.bottomleft)

        self.stage_label = self.font.render(f"{self.stage} :Stage", True, pygame.Color("White"))
        self.stage_rect = self.stage_label.get_rect(topright=(self.SCREEN_WIDTH, 0))

    # Updating player highest score
    def update_highest_score(self):
        try:
            data_file = open(file="..\\data\\data.txt", mode='r')
        except FileNotFoundError:
            open(file="..\\data\\data.txt", mode='w').close()
        else:
            data = data_file.readline().replace('\n', '')
            if len(data) != 0:
                self.highest_score = int(data)
            else:
                self.highest_score = 0
            data_file.close()

    # Spawns an enemy
    def spawn_enemy(self):
        self.enemies.add(Invader())

    # Saving the player highest score
    def save_data(self):
        if self.score >= self.highest_score:
            with open(file="..\\data\\data.txt", mode='w') as data_file:
                data_file.write(str(self.score))

    # Sprites group initialization
    def init_sprite_groups(self):
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

    def update(self):
        # Updating parry cooldown
        self.is_parry_on_cooldown = self.is_parrying and pygame.time.get_ticks() - self.parry_time < 3

        # Detecting collision between bullets and enemies
        pygame.sprite.groupcollide(self.bullets, self.enemies, False, True)

        # Detecting collision between player and enemies if players is not invincible
        if not self.player.is_invincible:
            if len(pygame.sprite.spritecollide(self.player, self.enemies, True)) != 0:
                self.player.health -= 2
                self.player.is_invincible = True

        # Detecting collision between player and bullets if player is not invincible
        if not self.player.is_invincible:
            if len(pygame.sprite.spritecollide(self.player, self.bullets, True)):
                self.player.health -= 1
                Bullet.sound.play()

        # Updating background scroller after reaching to the end
        if self.scroll > self.background.get_width():
            self.scroll = 0

        # Plays player running animation
        self.player.update_image()

        # Updates all the enemies
        self.enemies.update(self.SCREEN_HEIGHT)

        # Updates all the bullets
        self.bullets.update(self.window)

        # initializing and updating labels
        self.init_and_update_labels()

        # Scrolls background
        self.scroll += 0.5

        # Updating highest score if player scores higher than it
        if self.score >= self.highest_score:
            self.highest_score = self.score

        # Updating score based on survival time
        self.score = pygame.time.get_ticks() // 1000

        # Applying damage to player if an enemy reaches the end of the screen
        for enemy in self.enemies.sprites():
            if enemy.rect.left >= self.SCREEN_WIDTH:
                self.player.health -= 1
                self.enemies.remove(enemy)

        # Updating player invincibility
        if self.player.is_invincible:
            self.player.invincibility_timer += 0.1
            self.player.image.set_alpha(150)
            if math.floor(self.player.invincibility_timer) == 5:
                self.player.is_invincible = False
                self.player.invincibility_timer = 0
                self.player.image.set_alpha(255)

        # Updating stage
        if self.score > self.stage_difference:
            self.stage += 1
            self.stage_difference += 2 * self.stage_difference

    # Rendering all the components
    def render(self):
        if self.state == "Game":
            # Drawing background
            for i in range(self.tiles):
                self.window.blit(self.background, (-i * self.background.get_width() + self.scroll, 0))

            # Drawing lines
            for row in range(1, 3):
                start_y_pos = row * self.SCREEN_HEIGHT // 3
                pygame.draw.line(self.window, pygame.Color("#0066cc"), (0, start_y_pos), (self.SCREEN_WIDTH, start_y_pos), 2)

            # Rendering Player
            self.window.blit(self.player.image, self.player.rect)
            # Rendering enemies
            self.enemies.draw(self.window)
            # Rendering bullets
            self.bullets.draw(self.window)
            # Rendering player highest score
            self.window.blit(self.highest_score_label, self.highest_score_rect)
            # Rendering player score
            self.window.blit(self.score_label, self.score_rect)
            # Rendering player health
            self.window.blit(self.health_label, self.health_rect)
            # Rendering stage
            self.window.blit(self.stage_label, self.stage_rect)


class Cutscene:
    def __init__(self, window):
        pass


class Menu:
    def __init__(self, window):
        pass


class PauseMenu:
    def __init__(self, window):
        pass
