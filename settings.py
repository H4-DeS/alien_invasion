class Settings:
    '''Classe para armazenar as configurações do jogo'''
    def __init__(self):
        '''Inicializa as configurações do jogo'''
        #Confiugrações da tela
        self.screen_width = 800
        self.screen_height = 640
        self.bg_color = (240,240,240)
        self.ship_speed = 2.0
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_speed = 2.5
        self.bullet_allowed = 3
        self.bullet_color = (60,60,60)
        self.alien_speed = 4.0
        self.fleet_direction = 1
        self.fleet_drop_speed = 10
