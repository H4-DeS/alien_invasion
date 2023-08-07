import pygame.image


class Settings:
    '''Classe para armazenar as configurações do jogo'''
    def __init__(self):
        '''Inicializa as configurações do jogo'''
        #Configurações da tela
        self.screen_width = 800
        self.screen_height = 640
        self.bg_color = (240,240,240)
        self.bg_image = pygame.image.load("imgs/spacefield.jpg")

        #Configuração da spacefighter
        self.ships_limit = 3

        #Configuração dos projéteis
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_allowed = 3
        self.bullet_color = (0,0,250)

        #Configurações da frota alienígena
        self.fleet_direction = 1
        self.fleet_drop_speed = 10

        #Escala de aumento de velocidade do jogo
        self.speedup_scale = 1.2

        #Escala de aumento da pontuação
        self.scoreup_scale = 1.5

        #Inicializa os parâmetros dinâmicos
        self.initialize_dynamic_settings()

        #Configuração de pontuação
        self.alien_points = 50
        self.miss_target_penalty = 15

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.alien_points = 50

    def increase_game_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= self.scoreup_scale
