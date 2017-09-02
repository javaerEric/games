import pygame
from pygame.sprite import Group

from settings import Settings
from game_resources import GameResources
from ship import Ship
from button import Button
from game_stats import GameStats
from score_board import ScoreBoard
import game_functions as gf


def run_game():
    pygame.init()
    pygame.mouse.set_visible(False)
    ai_settings = Settings()
    res = GameResources()

    # screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN, 32)
    pygame.display.set_caption("外星人入侵")

    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    score_board = ScoreBoard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens)
    res.game_sound.play(-1)

    while True:
        gf.check_event(ai_settings, screen, stats, ship, bullets, aliens, play_button, res)

        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, screen, stats, ship, bullets, aliens, score_board, res)
            gf.update_bullets(ai_settings, screen, stats, bullets, aliens, score_board, res)

        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, score_board)


run_game()
