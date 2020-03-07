
class Settings():
    """A class to store all settings for Allien Invation."""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen Settings
        self.screen_width = 800
        self.screen_height = 600
        # self.bg_color = (0, 0, 0)
        self.bg_color = (10, 10, 10)

        # Ship
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # bullet
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        # self.bullet_color = (252, 248, 8) # 60, 60, 60
        self.bullet_color = (255,255,0)
        self.bullets_allowed = 3

        # Alien
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 20
        self.fleet_direction = 1  # 1: right; -1: left

        # How quickly the game speed up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 10  # original: 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
