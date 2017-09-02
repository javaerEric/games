import pygame


class GameResources:
    def __init__(self):
        self.game_sound = pygame.mixer.Sound("audios/alien_invasion.wav")
        self.fire_sound = pygame.mixer.Sound("audios/gun_fire.wav")
        self.ship_fly_sound = pygame.mixer.Sound("audios/ship_fly.wav")
        self.ship_stop_sound = pygame.mixer.Sound("audios/ship_stop.wav")

