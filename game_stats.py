import os

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # High score shoud never be reset.
        self.high_score = 0
        if os.path.exists("high_score.txt"):
            r = open("high_score.txt", 'r')
            high_score = r.read()
            self.high_score = int(high_score)

        # with open(_score_path) as high_score_file:
        #     self.high_score = int(high_score_file.read())

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
