import pygame
import sys
from time import sleep

from bullet import Bullet
from alien import Alien

pygame.init()


def check_key_down(event, ship):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.move_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.move_left = True


def check_key_up(event, ai_settings, screen, stats, ship, bullets, aliens, res):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.move_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.move_left = False
    elif event.key == pygame.K_SPACE or event.key == pygame.K_j:
        fire_bullet(ai_settings, screen, ship, bullets, res)
    elif event.key == pygame.K_b:
        if stats.game_active:
            suspend(stats, res)
        else:
            begin(ai_settings, screen, stats, ship, bullets, aliens, res)
    elif event.key == pygame.K_q:
        sys.exit()


def check_mouse_down(event, ai_settings, screen, stats, ship, bullets, aliens, play_button, res):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        begin(ai_settings, screen, stats, ship, bullets, aliens, res)


def check_event(ai_settings, screen, stats, ship, bullets, aliens, play_button, res):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ship)
        elif event.type == pygame.KEYUP:
            check_key_up(event, ai_settings, screen, stats, ship, bullets, aliens, res)
        elif event.type == pygame.MOUSEBUTTONUP:
            check_mouse_down(event, ai_settings, screen, stats, ship, bullets, aliens, play_button, res)


def update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, score_board):
    screen.fill(ai_settings.screen_bg_color)

    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    score_board.draw_score_board()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, bullets, aliens, score_board, res):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullets_aliens(ai_settings, screen, stats, bullets, aliens, score_board, res)


def fire_bullet(ai_setting, screen, ship, bullets, res):
    if len(bullets) < ai_setting.bullet_limit:
        bullet = Bullet(ai_setting, screen, ship)
        bullets.add(bullet)
        res.fire_sound.play(0, 500)


def update_aliens(ai_settings, screen, stats, ship, bullets, aliens, score_board, res):
    aliens.update()

    check_fleet_edge(ai_settings, screen, stats, ship, bullets, aliens, score_board, res)
    check_ship_aliens(ai_settings, screen, stats, ship, bullets, aliens, score_board, res)


def check_fleet_edge(ai_settings, screen, stats, ship, bullets, aliens, score_board, res):
    for alien in aliens.sprites():
        if alien.rect.left <= 0 or alien.rect.right >= alien.screen_rect.right:
            change_fleet_direction(ai_settings, aliens)
            check_fleet_bottom(ai_settings, screen, stats, ship, bullets, aliens, score_board, res)
            break


def check_fleet_bottom(ai_settings, screen, stats, ship, bullets, aliens, score_board, res):
    for alien in aliens.sprites():
        if alien.rect.bottom >= alien.screen_rect.bottom:
            died(ai_settings, screen, stats, ship, bullets, aliens, score_board, res)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.y += ai_settings.alien_down_speed
        alien.rect.y = alien.y
    ai_settings.alien_speed_factor *= -1


def create_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    col_count = int((ai_settings.screen_width - 20) / (2 * alien_width))
    row_count = int((ai_settings.screen_height - 3 * alien_height) / (1.5 * alien_height))

    for row_num in range(0, row_count):
        for col_num in range(0, col_count):
            alien = Alien(ai_settings, screen)
            alien.x = 20 + col_num * 2 * alien_width
            alien.y = alien_height + row_num * 1.5 * alien_height
            alien.rect.x = alien.x
            alien.rect.y = alien.y
            aliens.add(alien)


def check_bullets_aliens(ai_settings, screen, stats, bullets, aliens, score_board, res):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.update_speed()
        stats.level += 1
        score_board.prep_level()
        res.ship_fly_sound.play()
        create_fleet(ai_settings, screen, aliens)

    for aliens in collisions.values():
        stats.score += len(aliens) * ai_settings.alien_point
        score_board.prep_score()
    check_high_score(stats, score_board)


def check_ship_aliens(ai_settings, screen, stats, ship, bullets, aliens, score_board, res):
    collision = pygame.sprite.spritecollideany(ship, aliens)
    if collision:
        died(ai_settings, screen, stats, ship, bullets, aliens, score_board, res)


def died(ai_settings, screen, stats, ship, bullets, aliens, score_board, res):
    res.ship_fly_sound.stop()
    res.ship_stop_sound.play()

    if stats.ship_limit > 0:
        score_board.prep_ships()
        create_fleet(ai_settings, screen, aliens)
        stats.ship_limit -= 1
        bullets.empty()
        aliens.empty()
        ship.reset()
        res.ship_fly_sound.play()
    else:
        stats.game_active = False
        stats.game_over = True

    sleep(3)


def begin(ai_settings, screen, stats, ship, bullets, aliens, res):
    if stats.game_over:
        stats.reset()
        ship.reset()

        bullets.empty()
        aliens.empty()

        create_fleet(ai_settings, screen, aliens)
        stats.game_over = False

    stats.game_active = True
    res.game_sound.stop()
    res.ship_fly_sound.play()


def suspend(stats, res):
    stats.game_active = False


def check_high_score(stats, score_board):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()


