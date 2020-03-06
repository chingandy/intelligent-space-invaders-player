#! /usr/local/bin/python3
import pygame
import os
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien_wb.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        self.alien_speed_factor = 1

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """ Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
