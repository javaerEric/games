class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.screen_bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_limit = 3

        self.speed_scale = 1.1
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.alien_speed_factor = 1
        self.alien_down_speed = 10
        self.bullet_speed_factor = 3

        self.alien_point = 50

    def update_speed(self):
        self.ship_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        self.alien_down_speed *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale

        self.alien_point *= self.speed_scale