import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from sounds import Sounds
from scoreboard import ScoreBoard
from load_stats import LoadFile


class AlienInvasion:
    def __init__(self):
        'Inicializa o jogo e cria recursos do jogo'
        pygame.init()
        self.settings = Settings()
        self.active_game = False
        self.stats = GameStats(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.sb = ScoreBoard(self)
        self.load_sb = LoadFile(self)
        self.load_sb.load_score()
        self.sb.prep_high_score()
        self.button = Button(self, "PLAY")
        self.fullscreen_flag = False
        self.clock = pygame.time.Clock()
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        pygame.display.set_caption("Alien Invasion")
        self.sound = Sounds()
        self.sound.play_intro()

    def run_game(self):
        '''Inicia o loop principal do jogo'''
        while True:
            self._check_events()
            self._update_screen()
            if self.active_game:
                self._update_bullets()
                self._aliens_update()
                self.ship.position_update()
            self.clock.tick(60)
    def _create_fleet(self):
        #Cria a frota alienígena
        alien = Alien(self)
        current_x = alien.rect.x
        current_y = alien.rect.y*2
        while current_y < (self.settings.screen_height - 7*alien.rect.y):
            while current_x < (self.settings.screen_width - 2*alien.rect.x):
                self._create_alien(current_x, current_y)
                current_x += 2*alien.rect.x
            current_y += 2*alien.rect.y
            current_x = alien.rect.x

    def _create_alien(self, current_x, current_y):
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)

    def _aliens_update(self):
        self.aliens.update()
        self._check_edge()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

    def _ship_hit(self):
            #Decrementa o número de naves disponíveis
            if self.stats.ships_left > 0:
                self.stats.ships_left -= 1
            else:
                self.active_game = False
                pygame.mouse.set_visible(True)
            #Limpa a tela de projéteis e aliens restantes
            self.reset_game()
            self.sb.prep_ships()

    def reset_game(self):
        self.bullets.empty()
        self.aliens.empty()
        # Recria nova frota alien
        self._create_fleet()
        self.ship._center_ship()
        sleep(0.5)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_alien_direction()
                break

    def _change_alien_direction(self):
        'Muda a direção da frota alienígena'
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        #self.screen.fill(self.bg_color)
        self.screen.blit(self.settings.bg_image, self.screen_rect)
        #Desenha o projétil
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self._update_bullets()
        #Desenha a Spacefighter
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.active_game:
            self.button.draw_button()
        # Deixa a tela desenhada mais recente visível
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        self._check_bullet_collision()
        # Remove o projétil quando antigir o limite da tela
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.stats.score -= self.settings.miss_target_penalty
                self.sb.prep_score()
                self.bullets.remove(bullet)

    def _check_bullet_collision(self):

        # if pygame.sprite.groupcollide(self.bullets, self.aliens, False, False):
        #     self.sound.alien_catch()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.sound.alien_catch()
            for collision in collisions.values():
                self.stats.score += self.settings.alien_points*len(collision)
                self.sb.prep_score()
                self.check_high_score()
            self.sb.prep_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_game_speed()
            self.check_high_score()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        # Observa eventos de teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)

            elif event.type == pygame.KEYUP:
                self._key_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
            self.load_sb.save_score()
            sys.exit()
        elif event.key == pygame.K_p:
            if self.active_game == False:
                self._start_game()
        elif event.key == pygame.K_F10:
            if self.fullscreen_flag == True:
                self.screen = pygame.display.set_mode((800, 600))
                self.fullscreen_flag = False
            elif self.fullscreen_flag == False:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.fullscreen_flag = True
            self.settings.screen_width = self.screen.get_width()
            self.settings.screen_height = self.screen.get_height()
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) < self.settings.bullet_allowed and self.active_game == True:
                self.sound.laser_fire.play()
                self.new_bullet = Bullet(self)
                self.bullets.add(self.new_bullet)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.active_game:
            self._start_game()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_ships()
    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.sound.stop_intro()
        self.sound.play_game()
        self.active_game = True
        pygame.mouse.set_visible(False)


if __name__ == '__main__':
    #Cria uma instância do jogo e executa o jogo
    ai = AlienInvasion()
    ai.run_game()
