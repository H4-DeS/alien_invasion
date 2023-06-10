import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self):
        '''Inicializa o jogo e cria recursos do jogo'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        self.fullscreen_flag = True
        self.clock = pygame.time.Clock()
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        '''Inicia o loop principal do jogo'''
        while True:
            self._check_events()
            self._update_screen()
            self.ship.position_update()
            self.clock.tick(60)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        # Deixa a tela desenhada mais recente visível
        self.ship.blitme()
        pygame.display.flip()

    def _check_events(self):
        # Observa eventos de teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)

            elif event.type == pygame.KEYUP:
                self._key_up_events(event)

    def _key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _key_down_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_F10:
            if self.fullscreen_flag == True:
                self.screen = pygame.display.set_mode((800,600))
                self.fullscreen_flag = False
            elif self.fullscreen_flag == False:
                self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                self.fullscreen_flag = True
            self.settings.screen_width = self.screen.get_width()
            self.settings.screen_height = self.screen.get_height()
            self.ship = Ship(self)


if __name__ == '__main__':
    #Cria uma instância do jogo e executa o jogo
    ai = AlienInvasion()
    ai.run_game()
