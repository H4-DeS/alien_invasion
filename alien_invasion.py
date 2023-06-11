import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        'Inicializa o jogo e cria recursos do jogo'
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.fullscreen_flag = False
        self.clock = pygame.time.Clock()
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        '''Inicia o loop principal do jogo'''
        while True:
            self._check_events()
            self._update_screen()
            self._update_bullets()
            self._check_edge()
            self._aliens_update()
            self.ship.position_update()
            self.clock.tick(60)
    def _create_fleet(self):
        #Cria a frota alienígena
        alien = Alien(self)
        current_x = alien.rect.x
        current_y = alien.rect.y
        while current_y < (self.settings.screen_height - 4*alien.rect.y):
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
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
            #Decrementa o número de naves disponíveis
            self.stats.ships_left -= 1
            #Limpa a tela de projéteis e aliens restantes
            self.bullets.empty()
            self.aliens.empty()
            #Recria nova frota alien
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
        self.screen.fill(self.bg_color)
        #Desenha o projétil
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self._update_bullets()
        #Desenha a Spacefighter
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Deixa a tela desenhada mais recente visível
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        self._check_bullet_collision()
        # Remove o projétil quando antigir o limite da tela
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.remove()
            self._create_fleet()

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
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) < self.settings.bullet_allowed:
                self.new_bullet = Bullet(self)
                self.bullets.add(self.new_bullet)


if __name__ == '__main__':
    #Cria uma instância do jogo e executa o jogo
    ai = AlienInvasion()
    ai.run_game()
