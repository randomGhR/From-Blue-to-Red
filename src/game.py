
import pygame
import states
import sys as system
from bullet import Bullet

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.init_window()
        self.init_variables()

    # Window initialization
    def init_window(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 450
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    # Variable initialization
    def init_variables(self):
        self.state = "Game"
        self.game_scene = states.GameScene(self.window)
        self.clock = pygame.time.Clock()
        self.FPS = 60

    # Event polling
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_scene.save_data()
                pygame.quit()
                system.exit()

            if self.state == 'Game':
                # Updating player on keypress(move)
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP and self.game_scene.player.line_index > 1:
                        self.game_scene.player.line_index -= 1

                    elif event.key == pygame.K_DOWN and self.game_scene.player.line_index < 3:
                        self.game_scene.player.line_index += 1
                    self.game_scene.player.update()

                    # Shoots on key
                    if event.key == pygame.K_z:
                        self.game_scene.bullets.add(Bullet(self.game_scene.player.line_index, self.SCREEN_HEIGHT))
                        shoot_sound = pygame.mixer.Sound("..\\assets\\sounds\\laser.wav")
                        shoot_sound.set_volume(0.3)
                        shoot_sound.play()

                    # Parry's on key
                    elif event.key == pygame.K_x:
                        # Parrying if it's not on cooldown and there's any bullet
                        if not self.game_scene.is_parry_on_cooldown and len(self.game_scene.bullets.sprites()) != 0:
                            closest_bullet = self.game_scene.bullets.sprites()[0]
                            if closest_bullet.rect.left > 670:
                                self.game_scene.parry_time = pygame.time.get_ticks()
                                closest_bullet.velocity *= -1
                                self.game_scene.player.health += 2

                # Spawn an enemy on timer
                elif event.type == self.game_scene.spawn_timer:
                    self.game_scene.spawn_enemy()

    # Updating game
    def update(self):
        # Polls events
        self.poll_events()

        if self.state == 'Game':
            self.game_scene.update()

        pygame.display.update()
        self.clock.tick(self.FPS)

    # Rendering all the components
    def render(self):
        if self.state == "Game":
            self.game_scene.render()
