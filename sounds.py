from pygame.mixer import Sound

class Sounds:
    def __init__(self):
        self.intro_music = Sound("sounds/Battle Theme.wav")
        self.laser_fire = Sound("sounds/laser_fire.wav")
        self.alien_explosion = Sound("sounds/alien_explosion.wav")
        self.play = Sound("sounds/start_engine.wav")

    def play_intro(self):
        self.intro_music.play()

    def stop_intro(self):
        self.intro_music.fadeout(1500)

    def play_game(self):
        self.play.play()

    def laser_fire_sound(self):
        self.laser_fire.play()

    def alien_catch(self):
        self.alien_explosion.play()