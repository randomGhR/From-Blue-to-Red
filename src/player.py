
import math
import pygame

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.init_image()
        self.init_variables()
        self.rect = self.image.get_rect(midright=(
            800,
            self.line_index * 450 // 3 - self.image.get_height()
        ))

    # Image updating
    def update_image(self):
        self.image_index += 0.1
        if self.image_index > 6:
            self.image_index = 1
        elif isinstance(self.image_index, int):
            self.image = pygame.image.load(f"..\\assets\\sprites\\Player\\{self.image_index}.png").convert_alpha()
        else:
            self.image = pygame.image.load(f"..\\assets\\sprites\\player\\{math.floor(self.image_index)}.png").convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 50, self.image.get_height() + 50)).convert_alpha()

    # Image initialization
    def init_image(self):
        self.image = pygame.image.load("..\\assets\\sprites\\player\\1.png").convert_alpha()
        # Fliping the image
        self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
        # Re-scaling the image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 50, self.image.get_height() + 50)).convert_alpha()

    # Variable initialization
    def init_variables(self):
        self.line_index = 2
        self.image_index = 1
        self.health = 20
        self.is_invincible = False
        self.invincibility_timer = 0

    # Updating player attributes
    def update(self):
        self.rect.centery = self.line_index * 450 // 3 - 82
