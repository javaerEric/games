import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.rect = pygame.Rect(0, 0, self.ai_settings.bullet_width, self.ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.ai_settings.bullet_color, self.rect)

    def update(self):
        self.y -= self.ai_settings.bullet_speed_factor
        self.rect.y = self.y


