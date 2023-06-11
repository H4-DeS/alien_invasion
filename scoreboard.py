import pygame.font
class ScoreBoard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Cria texto para o scoreboard
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #Cria caixa para o texto do scoreboard
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = f'{rounded_score:,}'
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        rounded_high_score = int(round(self.stats.high_score, -1))
        high_score_str = f'{rounded_high_score:,}'
        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def prep_level(self):
        str_level = str(self.stats.level)
        self.level_img = self.font.render(str_level, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)