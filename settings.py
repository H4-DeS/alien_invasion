class Settings:
    '''Classe para armazenar as configurações do jogo'''
    def __init__(self):
        '''Inicializa as configurações do jogo'''
        #Confiugrações da tela
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230,230,230)
        self.ship_speed = 2.0