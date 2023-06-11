import pygame

class Ship:
    '''Classe destinada a criar a espaçonave'''

    def __init__(self, ai_game):
        #Inicializa a espaçonave e sua posição inicial
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load("imgs/ship5.png")

        #Redimensiona tamanho da imagem da espaçonave
        self.image = pygame.transform.scale_by(self.image, 0.15)
        self.rect = self.image.get_rect()

        #Começa cada espaçonava nova no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        '''Desenha a espaçonave'''
        self.screen.blit(self.image, self.rect)

    def position_update(self):
        if self.moving_left and self.rect.x > 0:
            self.x -= self.settings.ship_speed
        elif self.moving_right and self.rect.right < self.settings.screen_width:
            self.x += self.settings.ship_speed
        self.rect.x = self.x

    def _center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)