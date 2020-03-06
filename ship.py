import pygame
import os
from pygame.sprite import Sprite
# print("Current working directory: ", os.getcwd())
# os.chdir("./")
# print("After changing the directory: ", os.getcwd())

class Ship(Sprite):

    def __init__(self, settings, screen):
        """Initialize the ship and set its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.settings = settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship_wb.bmp') # return a surface representing the ship
        # self.image = pygame.transform.scale(self.image,
        #          (int(self.image.get_width() * 0.2),
        #           int(self.image.get_height() * 0.2) ))
        # self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's postion based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.settings.ship_speed_factor * 1.5  # add 1.5 muliplier to balance the speeds of moving left and right (don't know why)
        elif self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.settings.ship_speed_factor
        # if self.moving_right:
        #     self.rect.centerx += 1
        # if self.moving_left:
        #     self.rect.centerx -= 1


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
