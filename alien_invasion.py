#! /usr/gin/env python3
import sys
import pygame
import os
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard

from pygame.sprite import Group




def run_game():
    # Initialize game and create a screen object
    pygame.init()
    pygame.display.set_caption('Alien Invasion')

    settings = Settings()

    screen_size = (settings.screen_width, settings.screen_height)
    screen = pygame.display.set_mode(screen_size)


    # Create the Play button
    play_button = Button(screen, "Play")


    ship = Ship(settings, screen)
    alien = Alien(settings, screen)

    # Make a group to store bullets in.
    bullets = Group()
    aliens = Group()

    gf.create_fleet(settings, screen, ship, aliens)
    # TODO: create a function which output the state by pickle
    # print("Aliens: ", aliens.sprites())
    # alien_list = aliens.sprites()
    # print(alien_list[0].rect)
    # print(alien_list[1].rect)
    # # quit()
    # print("Ship: ", ship)
    # print(ship[:2])
    # print(type(ship.rect.x))
    # quit()

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    #Start the main loop for the game
    # count = 0
    while True:
        gf.check_events(settings, screen, stats, sb, ship, aliens, bullets, play_button)
        if stats.game_active:
            ship.update()
            reward = gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
            done = gf.update_aliens(settings, stats, sb, screen, ship, aliens, bullets) # update the aliens' positions after the bullets have been updated (checking to see whether any bullets hit any aliens.)
            gf.get_state(aliens, bullets, ship, reward, done)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
