from os import name
import pygame
from config import *
from game.player import Player
from game.platform import Platform
from game.coin import Coin
from game.enemy import Enemy
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platform.add(ground)
        self.all_sprites.add(ground)

        # Příklad dalších platforem (můžeš upravit / přidat)
        plat1 = Platform(180, SCREEN_HEIGHT - 140, 160, 20)
        plat2 = Platform(420, SCREEN_HEIGHT - 220, 140, 20)
        self.platform.add(plat1, plat2)
        self.all_sprites.add(plat1, plat2)

        # náhodné spawnování coinů na dostupných platformách
        self.spawn_coins(5)
        # spawn enemy (např. 2 enemy) na náhodných platformách
        self.spawn_enemies(2)

    def spawn_coins(self, count):
        plats = list(self.platform)
        if not plats:
            return
        for _ in range(count):
            p = random.choice(plats)
            # x uvnitř šířky platformy, trochu od okrajů
            x = random.randint(p.rect.left + 20, max(p.rect.left + 20, p.rect.right - 20))
            # y těsně nad platformou (dostupné skokem)
            y = p.rect.top - random.randint(30, 70)
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
            
    def spawn_enemies(self, count):
        plats = list(self.platform)
        # neumisťovat enemy na extrémně úzké platformy
        plats = [p for p in plats if p.rect.width > 50]
        if not plats:
            return
        for _ in range(count):
            p = random.choice(plats)
            x = random.randint(p.rect.left + 10, p.rect.right - 10)
            enemy = Enemy(x, p)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            evt_name = pygame.event.event_name(event.type)

            if event.type == pygame.QUIT:
                self.running = False

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                evt_key = pygame.key.name(event.key)
                print(f"{evt_name}: {evt_key}")

            elif event.type == pygame.MOUSEMOTION:
                print(f"{evt_name}: {event.pos}")

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                print(f"{evt_name}: {event.button} at {event.pos}")
    
    def update(self):
        game_over = self.player.update(self.platform)
        if game_over:
            self.running = False

        # aktualizace enemy pohybu
        self.enemies.update()

        collected_count = 0
        # Detekce sběru mincí - coin.kill() se provede pro dokill=True a mince se odstraní ze všech skupin
        collected = pygame.sprite.spritecollide(self.player, self.coins, dokill=True)
        if collected:
            collected_count += 1
            print(f"Sebráno mincí: {collected_count}/5")

        # kolize s enemy
        hits = pygame.sprite.spritecollide(self.player, self.enemies, dokill=False)
        for enemy in hits:
            # pokud hráč padá dolů a narazí na horní část enemy -> stomp
            if getattr(self.player, "velocity_y", 0) > 0 and (self.player.rect.bottom - enemy.rect.top) < 18:
                enemy.kill()
                # lehký odskok po stomp
                self.player.velocity_y = - (JUMP_POWER * 0.8)
                kill_count = 0
                kill_count += 1
                print(f"Enemy zničen stompem {kill_count}/2")
            else:
                print("Hráč zemřel při nárazu na enemy")
                self.running = False
                break

        # Konec hry při sebrání všech mincí
        if len(self.coins) == 0:
            print("Vyhrál jsi! Všechny mince sebrány.")
            self.running = False

    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        for sprite in self.all_sprites:
            sprite.draw(self.screen)
        
        pygame.display.flip()



    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)