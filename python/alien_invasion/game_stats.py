class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings

        self.game_active = False
        self.game_over = False

        self.ship_limit = ai_settings.ship_limit
        self.level = 0
        self.score = 0
        self.high_score = 0

    def reset(self):
        self.ship_limit = self.ai_settings.ship_limit
        self.level = 0
        self.score = 0
        self.ai_settings.init_dynamic_settings()

