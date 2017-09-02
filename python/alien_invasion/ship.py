import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.image = pygame.image.load("images/ship.bmp")
        self.screen_rect = screen.get_rect()
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.move_left = False
        self.move_right = False
        self.centerx = float(self.rect.centerx)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.move_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor

        self.rect.centerx = self.centerx

    def reset(self):
        self.centerx = self.screen_rect.centerx





