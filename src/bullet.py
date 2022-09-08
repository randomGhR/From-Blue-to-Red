
import pygame

pygame.init()
pygame.mixer.init()


class Bullet(pygame.sprite.Sprite):
    # Sound initialization
    sound = pygame.mixer.Sound("..\\assets\\sounds\\hit.wav")
    sound.set_volume(0.4)

    def __init__(self, line_index, screen_height):
        super().__init__()
        self.init_image()
        self.rect = self.image.get_rect(topright=(
            0,
            (line_index + line_index - 1) * screen_height // 6
        ))
        self.velocity = 12

    # Updating bullet attributes
    def update(self, screen):
        self.rect.right += self.velocity
        if self.rect.left >= 800 or self.rect.right <= 0:
            self.kill()
        if self.rect.right >= 670:
            pygame.draw.rect(screen, pygame.Color("#FFFF00"), self.rect, 10)

    # Image initialization
    def init_image(self):
        self.image = pygame.image.load("..\\assets\\sprites\\bullet.png").convert_alpha()
        # Re-scaling the image
        self.image = pygame.transform.scale(
            self.image,
            (18, 9)
        ).convert_alpha()
