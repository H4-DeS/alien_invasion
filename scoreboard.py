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

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_img, self.score_rect)